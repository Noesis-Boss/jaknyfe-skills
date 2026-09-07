# Installing Ollama as a Service on Zo Computer + Connecting as a BYOK Provider

**Status:** verified working 2026-08-04. Live at `https://ollama-proxy-<your-handle>.zocomputer.io/v1` with `qwen3:14b` (primary) / `gemma3:1b` (fallback).

This guide walks through installing Ollama on Zo Computer as a managed (supervised) service, wrapping it in an OpenAI-compatible proxy so Zo's provider layer can talk to it, and wiring that proxy as a Bring-Your-Own-Key (BYOK) provider in Zo's AI settings.

---

## Why a proxy is required

Zo's provider layer (Settings → AI → Providers) **runs in Zo's cloud backend, not inside your container.** That means:

- `localhost:11435` resolves inside Zo's backend — your container is invisible.
- A **private** hosted service is only reachable from your own apps/sites, not from the cloud provider layer.
- Only a **public** URL (`https://<something>-<handle>.zocomputer.io`) reaches your container.

So the chain is always:

```
Zo chat box → Zo cloud provider layer → https://ollama-proxy-<handle>.zocomputer.io/v1
                                                      │  (public hosted HTTP service)
                                                      ▼
                                        proxy.ts (Bun, port 11435)
                                        OpenAI-compatible /v1/* shim
                                                      │
                                                      ▼
                                        Ollama server (127.0.0.1:11434)
                                        models: qwen3:14b (primary), gemma3:4b, gemma3:1b (failover chain)
```

---

## Prerequisites

- A Zo Computer account with access to [Services](/?t=sites&s=services), [Settings → AI → Providers](/?t=settings&s=ai&d=providers), and the terminal.
- `bun` available on the Zo terminal (`bun --version`).
- `curl` and `python3` available.

---

## Step 1 — Install the Ollama binary

```bash
# Preferred: official installer (works headless; falls back to tarball on no-systemd containers)
curl -fsSL https://ollama.com/install.sh | sh

# Fallback if the above fails on containers without systemd:
curl -fsSL -o /tmp/ollama.tgz https://ollama.com/download/ollama-linux-amd64.tgz
tar -xzf /tmp/ollama.tgz -C /usr/local
rm -f /tmp/ollama.tgz

ollama --version   # expect v0.32.x
```

---

## Step 2 — Pull models

```bash
ollama pull qwen3:14b   # ~9 GB, primary chat model
ollama pull gemma3:1b   # ~1 GB, fast fallback
```

---

## Step 3 — Register the `ollama-server` service

Go to [Services](/?t=sites&s=services) and create one managed service. Or paste the request block from `Skills/install-zorro/references/SERVICES-REQUEST.md` into a Zo chat.

| Field | Value |
|---|---|
| Label | `ollama-server` |
| Mode | **process** (no public endpoint, no port) |
| Entrypoint | `/usr/local/bin/ollama serve` |
| Env vars | `OLLAMA_HOST=127.0.0.1:11434` |

Verify Ollama is answering on loopback:

```bash
curl -s http://127.0.0.1:11434/api/tags   # → JSON listing qwen3:14b, gemma3:1b
```

---

## Step 4 — Create the proxy script

Create the file `Skills/ollama-proxy/scripts/proxy.ts` (or place it wherever you like). This is the OpenAI-compatible bridge.

```typescript
const OLLAMA = process.env.OLLAMA_URL || "http://127.0.0.1:11434";

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
      delete body.tools;
      delete body.tool_choice;
      delete body.functions;
      delete body.services;
      body.stream_options = undefined;
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

    console.log(`[${new Date().toISOString()}] ${client} ${req.method} ${url.pathname} stream=${wantStream} → ${target}`);
    if (body) console.log(`  req: ${JSON.stringify(body).slice(0, 200)}`);

    try {
      const ollamaRes = await fetch(target, {
        method: req.method,
        headers: new Headers({
          "Host": "localhost:11434",
          "Accept": "application/json",
          "Content-Type": req.headers.get("content-type") || "application/json",
        }),
        body: body ? JSON.stringify(body) : undefined,
      });

      if (!ollamaRes.ok) {
        const raw = await ollamaRes.text();
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms)`);
        if (raw.length < 400) console.log(`  body: ${raw.slice(0, 300)}`);
        return new Response(raw, {
          status: ollamaRes.status,
          headers: {
            "Content-Type": "application/json",
            "Content-Length": Buffer.byteLength(raw).toString(),
            "Cache-Control": "no-cache",
          },
        });
      }

      // True SSE passthrough: first token reaches the client in ~1-2s instead of after full generation
      if (wantStream && ollamaRes.body) {
        console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (streaming, first byte ${Date.now() - startTime}ms)`);
        // Safeguard: if the model returns zero content bytes, inject a fallback chunk
        // so Zo never sees a stream that "ended without content or tool calls".
        const enc = new TextEncoder();
        let contentBytes = 0;
        let sawDone = false;
        const stream = new TransformStream<Uint8Array, Uint8Array>({
          transform(chunk, controller) {
            const text = new TextDecoder().decode(chunk);
            const m = text.match(/"content":"([^"\\]*[^\\s"][^"\\]*)"/g);
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
      console.log(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ${ollamaRes.status} (${raw.length} bytes, ${Date.now() - startTime}ms)`);
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
    } catch (err) {
      console.error(`[${new Date().toISOString()}] ${client} ${url.pathname} ← ERROR: ${err}`);
      return new Response(JSON.stringify({ error: String(err) }), {
        status: 500,
        headers: { "Content-Type": "application/json" },
      });
    }
  },
});

console.log(`ollama-proxy listening on 0.0.0.0:${server.port} → ${OLLAMA}`);
```

**What each part does (the four moves):**

1. **Streams real SSE** when the client asks (`body.stream === true` *or* `Accept: text/event-stream` — OpenAI SDKs signal streaming this way). First byte lands in ~700 ms. If we buffered instead, the client's SSE parser sees an empty stream and reports "streamed response ended without content or tool calls."
2. **Strips unsupported params** (`tools`, `tool_choice`, `functions`, `services`, `stream_options`) — Ollama rejects or ignores these; Zo's provider layer sends them.
3. **Rewrites the Host header** to `localhost:11434` so Ollama accepts the call.
4. **Injects a fallback chunk** if a stream somehow ends with zero content bytes, so Zo never fails with an empty-stream error.

---

## Step 5 — Register the `ollama-proxy` service (**MUST be public**)

Go to [Services](/?t=sites&s=services) and create a second managed service:

| Field | Value |
|---|---|
| Label | `ollama-proxy` |
| Mode | **http** |
| Visibility | **public** (NOT private — a private service breaks chat) |
| Local port | `11435` |
| Entrypoint | `bash -c 'cd /home/workspace/Skills/ollama-proxy && bun run scripts/proxy.ts'` |
| Workdir | `/home/workspace/Skills/ollama-proxy` |

The service URL becomes `https://ollama-proxy-<your-handle>.zocomputer.io`. Supervisor auto-restarts it — killing the process relaunches with current code, so you never need manual `nohup`.

---

## Step 6 — Smoke tests

```bash
# 1. In-container: proxy → Ollama, non-streaming
curl -s http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}],"stream":false}'
# → 200, JSON with assistant reply

# 2. In-container: streaming (the exact contract Zo uses)
curl -s -N http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}],"stream":true}'
# → SSE chunks: data: {...delta...} ... data: [DONE]

# 3. Public URL (what Zo's cloud provider actually calls)
curl -s https://ollama-proxy-<your-handle>.zocomputer.io/v1/models
# → JSON model list — this MUST return 200 from outside
```

**Critical:** test #3 (the public URL) is the real proof. Test #1 alone always passes because `curl localhost` only proves the proxy works inside the container — not that the cloud provider layer can reach it.

---

## Step 7 — Configure Zo's BYOK provider

Go to [Settings → AI → Providers](/?t=settings&s=ai&d=providers) → **Bring Your Own Key** → **OpenAI-compatible**.

| Field | Value |
|---|---|
| Name | `ollama-local` |
| Base URL | `https://ollama-proxy-<your-handle>.zocomputer.io/v1` |
| API key | `ollama` (any non-empty string — the proxy doesn't check it) |
| Model | `qwen3:14b` (default/primary) — `gemma3:1b` for a fast fallback |

**Streaming:** leave enabled. The proxy passes real SSE; first token arrives in ~1 second.

> **Never** use `http://localhost:11435/v1` or a container IP (`172.20.x.x`) here. Both fail from the cloud provider layer. The public `*.zocomputer.io` URL is the only stable, reachable endpoint.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| "streamed response ended without content or tool calls" | Provider Base URL must be the **public** proxy URL (`https://ollama-proxy-<handle>.zocomputer.io/v1`), not `:11434`, not `localhost`, not a container IP. If proxy code changed, kill the `ollama-proxy` process — supervisor relaunches with current code. |
| Provider connection timeout / refused | Use the public URL. Check the service is enabled in the [Services](/?t=sites&s=services) panel and that `curl https://ollama-proxy-<handle>.zocomputer.io/v1/models` returns 200. |
| `ollama` binary missing after install | `curl -fsSL -o /tmp/ollama.tgz https://ollama.com/download/ollama-linux-amd64.tgz && tar -C /usr/local -xzf /tmp/ollama.tgz` |
| Ollama not answering on `127.0.0.1:11434` | The `ollama-server` service must be enabled and running. Verify with `curl -s http://127.0.0.1:11434/api/tags`. |
| Proxy returns 500 in logs | Check `/dev/shm/ollama-proxy.log`. Most common causes: model name typo, or Ollama is busy pulling another model. |
| Container IP changed after restart | Don't use container IPs in the provider config — that's why this guide uses the stable public URL. Verify current IP with `hostname -I` only if you're debugging the in-container proxy directly. |

---

## Fix log — lessons learned (in order)

| Date | Symptom | Root cause | Fix |
|---|---|---|---|
| 2026-07-19 | "model stream interrupted" from Zo provider | Zo provider → Ollama directly, mismatch in semantics/streaming | First proxy shim on :11435; forced `stream:false` (short-term workaround, later became the bug) |
| 2026-07-23 | Connection failure after restart | Stale container IP (`172.20.24.4` → `172.20.17.188`) in Base URL | Corrected IP in provider settings. **Lesson: container IPs change on every restart — don't put them in provider config** |
| 2026-07-26 | "model stream interrupted" again | Provider Base URL pointed at old IP after another restart | Updated AGENTS.md; instructed to use public URL instead of localhost |
| 2026-07-31 | "model stream was interrupted" | Proxy service was **private**; Zo's cloud provider resolved `localhost:11435` in its own backend, not the container | Flipped `ollama-proxy` to **public** → `https://ollama-proxy-<handle>.zocomputer.io/v1`. **Lesson: Zo's provider layer runs cloud-side; only public URLs reach your container** |
| 2026-08-01 | "streamed response ended without content or tool calls" (final fix) | Proxy forced `stream:false` and returned buffered JSON after 30–47 s; Zo's SSE parser saw no `data:` lines → empty stream | Rewrote `proxy.ts`: **true SSE passthrough** when `stream:true` or `Accept: text/event-stream`; strips `tools`/`tool_choice`/`functions`/`services`; keeps buffered JSON path for non-streaming; injects fallback chunk on empty streams. Verified: localhost + public URL, first byte ~700 ms, 19 SSE chunks ending `[DONE]` |

### Mistakes that wasted the most time

1. **Trusting in-container `curl` as proof.** `curl localhost:11435` always worked — chat still failed, because the real client (Zo's cloud provider) goes over the public URL. **Always test the public URL too.**
2. **Putting the container IP in provider settings.** It works until the next restart. The public URL is stable.
3. **Assuming "private" was fine.** A private hosted service is reachable from your own apps/sites but NOT from Zo's provider layer, which resolves localhost in its backend.
4. **Forcing `stream:false` as a "fix"** for the streaming mismatch. It papered over the error for weeks and became the cause of the next failure. The real fix was faithful SSE passthrough.

---

## Related

- `Skills/ollama-proxy/SETUP.md` — full setup guide with architecture diagrams.
- `Skills/install-zorro/SKILL.md` — one-shot installer that installs Ollama + proxy + memory tree + skills together.
- `Skills/install-zorro/references/MANUAL-STEPS.md` — the 4 UI steps that follow the installer.
- `Skills/install-zorro/references/SERVICES-REQUEST.md` — paste-ready service creation request for Zo chat.
