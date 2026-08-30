const OLLAMA = process.env.OLLAMA_URL || "http://127.0.0.1:11434";

// Timeout (ms) before the proxy gives up on the primary model and retries with a fallback.
// qwen3:14b on 4 CPUs can take >25s for first byte; falling back to gemma3:4b keeps us well under Zo's 120s window.
const PRIMARY_TIMEOUT_MS = parseInt(process.env.PRIMARY_TIMEOUT_MS || "25000");
const REQUEST_TIMEOUT_MS = parseInt(process.env.REQUEST_TIMEOUT_MS || "90000");

// Model fallback chain: if the requested model is slow or times out, try smaller models.
// The proxy only downgrades — never upgrades — so quality preferences are respected.
const FALLBACK_MODELS = ["samuser3/gemma-3-4b-vl-it-gemini-pro"];

function stripUnsupportedParams(b: any) {
  delete b.tools;
  delete b.tool_choice;
  delete b.functions;
  delete b.services;
  b.stream_options = undefined;
}

function buildRequest(body: any, model: string): any {
  const b = { ...body, model };
  stripUnsupportedParams(b);
  return b;
}

function fetchWithTimeout(target: string, opts: any, ms: number) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), ms);
  const promise = fetch(target, { ...opts, signal: controller.signal });
  return { promise, abort: () => { clearTimeout(timer); controller.abort(); } };
}

const server = Bun.serve({
  port: Number(process.env.PORT) || 11435,
  async fetch(req, server) {
    const url = new URL(req.url);
    const client = req.headers.get("x-forwarded-for") || req.remoteAddress || "unknown";

    let body: any = null;
    if (req.method !== "GET" && req.method !== "HEAD") {
      try { body = await req.json(); } catch { /* pass raw if not JSON */ }
    }

    let wantStream = false;
    if (body && typeof body === "object") {
      wantStream = body.stream === true;
    }

    // OpenAI-style SDKs signal streaming via Accept header even when body.stream is unset
    const accept = req.headers.get("accept") || "";
    if (accept.includes("text/event-stream")) wantStream = true;
    if (body && typeof body === "object" && wantStream) body.stream = true;

    // Fix doubled paths like /v1/chat/completions/chat/completions
    let pathname = url.pathname;
    pathname = pathname.replace(/\/v1\/chat\/completions\/chat\/completions/, "/v1/chat/completions");
    pathname = pathname.replace(/\/v1\/v1\//, "/v1/");

    const target = `${OLLAMA}${pathname}${url.search}`;
    const startTime = Date.now();

    // Determine the model chain: requested model first, then fallbacks
    const primaryModel = (body && body.model) || "qwen3:14b";
    const modelChain = [primaryModel, ...FALLBACK_MODELS.filter(m => m !== primaryModel)];

    console.log(`[${new Date().toISOString()}] ${client} ${req.method} ${url.pathname} stream=${wantStream} model=${primaryModel} → ${target}`);
    if (body) console.log(`  req: ${JSON.stringify(body).slice(0, 200)}`);

    let currentModel = primaryModel;
    let attempt = 0;

    while (attempt < modelChain.length) {
      const modelName = modelChain[attempt];
      const isFallback = modelName !== primaryModel;
      if (isFallback) {
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ↻ FAILOVER: trying ${modelName} (timeout on ${currentModel})`);
      }

      const fetchOpts: any = {
        method: req.method,
        headers: new Headers({
          "Host": "localhost:11434",
          "Accept": "application/json",
          "Content-Type": req.headers.get("content-type") || "application/json",
        }),
        body: body ? JSON.stringify(buildRequest(body, modelName)) : undefined,
      };

      const timeoutForThisAttempt = isFallback ? REQUEST_TIMEOUT_MS : PRIMARY_TIMEOUT_MS;
      const { promise, abort } = fetchWithTimeout(target, fetchOpts, timeoutForThisAttempt);

      let ollamaRes: Response;
      try {
        ollamaRes = await promise;
      } catch (err: any) {
        const aborted = err?.name === "AbortError";
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${aborted ? "TIMEOUT" : "ERROR"}: ${err} (${Date.now() - startTime}ms), model=${modelName}`);
        abort();
        attempt++;
        currentModel = modelName;
        continue;
      }

      if (!ollamaRes.ok) {
        const raw = await ollamaRes.text();
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms), model=${modelName}`);
        if (raw.length < 400) console.log(`  body: ${raw.slice(0, 300)}`);
        abort();

        // On 4xx/5xx from Ollama, try a fallback model (except the last one)
        if (attempt < modelChain.length - 1) {
          attempt++;
          currentModel = modelName;
          continue;
        }

        return new Response(raw, {
          status: ollamaRes.status,
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(raw).toString(),
            "Cache-Control": "no-cache",
          },
        });
      }

      // Success — stream or buffer the response
      abort();

      if (wantStream && ollamaRes.body) {
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (streaming, first byte ${Date.now() - startTime}ms, model=${modelName})`);
        const enc = new TextEncoder();
        let contentBytes = 0;
        let sawDone = false;
        const stream = new TransformStream<Uint8Array, Uint8Array>({
          transform(chunk, controller) {
            const text = new TextDecoder().decode(chunk);
            const m = text.match(/"content":"([^"\\]*[^"\\]"[^"\\]*)"/g);
            if (m) contentBytes += m.join("").length;
            if (text.includes("[DONE]")) sawDone = true;
            controller.enqueue(chunk);
          },
          flush(controller) {
            if (sawDone && contentBytes === 0) {
              const fallback = `data: {"id":"chatcmpl-fallback","object":"chat.completion.chunk","created":${Math.floor(Date.now() / 1000)},"model":"gemma","choices":[{"index":0,"delta":{"content":"..."},"finish_reason":"stop"}]}\n\ndata: [DONE]\n\n`;
              controller.enqueue(enc.encode(fallback));
            }
          },
        });
        return new Response(ollamaRes.body.pipeThrough(stream), {
          status: 200,
          headers: {
            "Content-Type": "text/event-stream; charset=utf-8",
            "Cache-Control": "no-cache, no-store",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
          },
        });
      }

      const raw = await ollamaRes.text();
      console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms), model=${modelName}`);
      if (raw.length < 400) console.log(`  body: ${raw.slice(0, 300)}`);

      return new Response(raw, {
        status: ollamaRes.status,
        headers: {
          "Content-Type": "application/json",
          "Content-Length": Buffer.byteLength(raw).toString(),
          "Cache-Control": "no-cache, no-store, must-revalidate",
          "Connection": "close",
          "X-Accel-Buffering": "no",
        },
      });
    }

    // All models in the chain failed — return error
    console.error(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ALL MODELS FAILED (${Date.now() - startTime}ms)`);
    return new Response(JSON.stringify({
      error: {
        message: `All models failed (tried: ${modelChain.join(", ")})`,
        type: "proxy_error",
      },
    }), {
      status: 504,
      headers: { "Content-Type": "application/json" },
    });
  },
});

console.log(`ollama-proxy listening on 0.0.0.0:${server.port} → ${OLLAMA}`);
console.log(`  primary timeout: ${PRIMARY_TIMEOUT_MS}ms, request timeout: ${REQUEST_TIMEOUT_MS}ms`);
console.log(`  fallback chain: ${FALLBACK_MODELS.join(" → ")}`);
