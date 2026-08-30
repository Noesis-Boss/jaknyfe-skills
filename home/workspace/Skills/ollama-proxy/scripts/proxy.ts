const OLLAMA = process.env.OLLAMA_URL || "http://127.0.0.1:11434";
const BONSAI = process.env.BONSAI_URL || "http://127.0.0.1:8081";

// Timeout (ms) before the proxy gives up on the primary model and retries a fallback.
const PRIMARY_TIMEOUT_MS = parseInt(process.env.PRIMARY_TIMEOUT_MS || "25000");
const REQUEST_TIMEOUT_MS = parseInt(process.env.REQUEST_TIMEOUT_MS || "90000");
// Send an SSE comment (": hb") every N ms while Ollama is thinking, so Zo's
// provider never sees a silent stream and never reports "response interrupted".
const HEARTBEAT_MS = parseInt(process.env.HEARTBEAT_MS || "15000");
const ADHD_STYLE = process.env.ADHD_STYLE !== "false";

const ADHD_SYSTEM_PROMPT = `Response style:
- Lead with the next concrete action.
- Put the answer or command first. No preamble or closing pleasantries.
- Number multi-step work. Keep each step bounded.
- State current progress and the next step.
- Use concrete filenames, commands, values, and time estimates.
- Keep lists to 5 items or fewer.
- Suppress tangents. Separate unrelated issues.
- State errors plainly: cause, fix, verification.
- Prefer concise paragraphs and short bullets.
- Do not repeat the user's request.`;

const FALLBACK_MODELS = (process.env.FALLBACK_MODELS || "gemma3:4b").split(",").map((model) => model.trim()).filter(Boolean);
const PRIMARY_CONTEXT = parseInt(process.env.PRIMARY_CONTEXT || "65536");
const FALLBACK_CONTEXT = parseInt(process.env.FALLBACK_CONTEXT || "32768");

// Backend routing: Bonsai models go to the llama-server on 8081, Ollama models on 11434.
function backendForModel(model: string): string {
  const m = model.toLowerCase();
  if (m.startsWith("bonsai") || m.includes("ternary-bonsai")) return BONSAI;
  return OLLAMA;
}

function hostHeaderForBackend(backend: string): string {
  if (backend === BONSAI) return "localhost:8081";
  return "localhost:11434";
}

function stripUnsupportedParams(b: any) {
  delete b.tools;
  delete b.tool_choice;
  delete b.functions;
  delete b.services;
  b.stream_options = undefined;
}

function buildRequest(body: any, model: string): any {
  const b = { ...body, model };
  if (ADHD_STYLE && Array.isArray(b.messages)) {
    const messages = [...b.messages];
    const systemIndex = messages.findIndex((message: any) => message?.role === "system");
    if (systemIndex >= 0) {
      messages[systemIndex] = {
        ...messages[systemIndex],
        content: `${messages[systemIndex].content || ""}\n\n${ADHD_SYSTEM_PROMPT}`,
      };
    } else {
      messages.unshift({ role: "system", content: ADHD_SYSTEM_PROMPT });
    }
    b.messages = messages;
  }
  if (model.startsWith("bonsai") && !b.chat_template_kwargs) {
    b.chat_template_kwargs = { enable_thinking: false };
  } else if (backendForModel(model) === OLLAMA) {
    // Ollama truncates prompts longer than its loaded context window from the
    // START, silently dropping the system prompt and early turns. That makes
    // long multi-turn chats "forget" the task and derail. Keep OLLAMA_CONTEXT_LENGTH
    // at 65536 on the server and pin per-model num_ctx so this cannot regress.
    b.options = { ...(b.options || {}), num_ctx: model === "llama3.2:3b" ? PRIMARY_CONTEXT : FALLBACK_CONTEXT };
  }
  stripUnsupportedParams(b);
  return b;
}

function fetchWithTimeout(target: string, opts: any, ms: number) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  return {
    promise: fetch(target, { ...opts, signal: controller.signal }),
    done: () => clearTimeout(timer),
    abortRemote: () => { clearTimeout(timer); try { controller.abort(); } catch {} },
  };
}

// Wrap an upstream (Ollama) response body in an SSE response to the client,
// adding heartbeat comments so the stream is never silent.
function sseResponse(
  upstream: ReadableStream<Uint8Array>,
  meta: { model: string; startTime: number; client: string; pathname: string },
) {
  const enc = new TextEncoder();
  let contentBytes = 0;
  let sawDone = false;
  let firstTokenT: number | null = null;

  const heartbeat = setInterval(() => {
    try {
      // Write directly into the controller if still open via the transform's
      // controller ref captured in the closure below.
      hbEnqueue?.(enc.encode(`: hb ${Date.now()}\n\n`));
    } catch {}
  }, HEARTBEAT_MS);
  let hbEnqueue: ((chunk: Uint8Array) => void) | null = null;

  const stream = new TransformStream<Uint8Array, Uint8Array>({
    start(controller) {
      hbEnqueue = (chunk) => { try { controller.enqueue(chunk); } catch {} };
      // Prime the stream immediately so the client gets bytes right away.
      try { controller.enqueue(enc.encode(`: connected ${Date.now()}\n\n`)); } catch {}
    },
    transform(chunk, controller) {
      const text = new TextDecoder().decode(chunk);
      const m = text.match(/"content":"([^"\\]*[^\\s"][^"\\]*)"/g);
      if (m) contentBytes += m.join("").length;
      if (firstTokenT === null && m) {
        firstTokenT = Date.now();
        console.log(`[${new Date().toISOString()}] ${meta.client} ${meta.pathname} (first content token ${firstTokenT - meta.startTime}ms, model=${meta.model})`);
      }
      if (text.includes("[DONE]")) sawDone = true;
      controller.enqueue(chunk);
    },
    flush(controller) {
      clearInterval(heartbeat);
      if (sawDone && contentBytes === 0) {
        const fallback = `data: {"id":"chatcmpl-fallback","object":"chat.completion.chunk","created":${Math.floor(Date.now() / 1000)},"model":"${meta.model}","choices":[{"index":0,"delta":{"content":"..."},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n`;
        controller.enqueue(enc.encode(fallback));
      }
    },
  });

  return new Response(upstream.pipeThrough(stream), {
    status: 200,
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-store",
      "Connection": "keep-alive",
      "X-Accel-Buffering": "no",
    },
  });
}

const server = Bun.serve({
  port: Number(process.env.PORT) || 11435,
  async fetch(req) {
    const url = new URL(req.url);
    const client = req.headers.get("x-forwarded-for") || req.remoteAddress || "unknown";

    if (req.method === "GET" && (url.pathname === "/health" || url.pathname === "/healthz")) {
      return new Response(JSON.stringify({ ok: true, ts: Date.now() }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    let body: any = null;
    if (req.method !== "GET" && req.method !== "HEAD") {
      try { body = await req.json(); } catch { /* pass raw if not JSON */ }
    }

    const accept = req.headers.get("accept") || "";
    const isChat = /\/v1\/(chat\/)?completions?$/.test(url.pathname);

    // Force streaming on chat completions: Zo holds the connection with NO
    // bytes until completion otherwise, and reports "response interrupted"
    // when the model thinks >~120s. Streaming + heartbeat prevents that.
    let wantStream = false;
    if (body && typeof body === "object" && body.stream === true) wantStream = true;
    if (accept.includes("text/event-stream")) wantStream = true;
    if (isChat) wantStream = true;
    if (body && typeof body === "object" && wantStream) body.stream = true;

    let pathname = url.pathname;
    pathname = pathname.replace(/\/v1\/chat\/completions\/chat\/completions/, "/v1/chat/completions");
    pathname = pathname.replace(/\/v1\/v1\//, "/v1/");

    const startTime = Date.now();

    const primaryModel = (body && body.model) || "llama3.2:3b";
    const modelChain = [primaryModel, ...FALLBACK_MODELS.filter((m) => m !== primaryModel)];

    console.log(`[${new Date().toISOString()}] ${client} ${req.method} ${url.pathname} stream=${wantStream} model=${primaryModel}`);
    if (body) console.log(`  req: ${JSON.stringify(body).slice(0, 200)}`);

    for (let attempt = 0; attempt < modelChain.length; attempt++) {
      const modelName = modelChain[attempt];
      const isFallback = attempt > 0;
      if (isFallback) {
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ↻ FAILOVER: trying ${modelName} (${Date.now() - startTime}ms)`);
      }

      const backend = backendForModel(modelName);
      const target = `${backend}${pathname}${url.search}`;

      const fetchOpts: any = {
        method: req.method,
        headers: new Headers({
          "Host": hostHeaderForBackend(backend),
          "Accept": "application/json",
          "Content-Type": req.headers.get("content-type") || "application/json",
        }),
        body: body ? JSON.stringify(buildRequest(body, modelName)) : undefined,
      };

      const timeoutThis = isFallback ? REQUEST_TIMEOUT_MS : PRIMARY_TIMEOUT_MS;
      const { promise, done, abortRemote } = fetchWithTimeout(target, fetchOpts, timeoutThis);

      let ollamaRes: Response;
      try {
        ollamaRes = await promise;
      } catch (err: any) {
        const aborted = err?.name === "AbortError";
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${aborted ? "TIMEOUT" : "ERROR"}: ${aborted ? "aborted" : String(err)} (${Date.now() - startTime}ms), model=${modelName}`);
        continue;
      }
      done();

      if (!ollamaRes.ok) {
        const raw = await ollamaRes.text();
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms), model=${modelName}`);
        abortRemote();
        if (attempt < modelChain.length - 1) continue;
        return new Response(raw, {
          status: ollamaRes.status,
          headers: { "Content-Type": "application/json", "Cache-Control": "no-cache" },
        });
      }

      if (wantStream && ollamaRes.body) {
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (streaming open ${Date.now() - startTime}ms, model=${modelName})`);
        return sseResponse(ollamaRes.body, { model: modelName, startTime, client, pathname: url.pathname });
      }

      const raw = await ollamaRes.text();
      console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms), model=${modelName}`);
      return new Response(raw, {
        status: ollamaRes.status,
        headers: { "Content-Type": "application/json", "Cache-Control": "no-cache" },
      });
    }

    console.error(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ALL MODELS FAILED (${Date.now() - startTime}ms)`);
    return new Response(JSON.stringify({ error: { message: `All models failed (tried: ${modelChain.join(", ")})`, type: "proxy_error" } }), {
      status: 504,
      headers: { "Content-Type": "application/json" },
    });
  },
});

console.log(`ollama-proxy listening on 0.0.0.0:${server.port} → ollama=${OLLAMA} bonsai=${BONSAI}`);
console.log(`  primary timeout: ${PRIMARY_TIMEOUT_MS}ms, request timeout: ${REQUEST_TIMEOUT_MS}ms, heartbeat: ${HEARTBEAT_MS}ms`);
console.log(`  fallback chain: ${FALLBACK_MODELS.join(" → ")}`);
console.log(`  ADHD response style: ${ADHD_STYLE ? "enabled" : "disabled"}`);
