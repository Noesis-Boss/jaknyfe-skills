---
name: ollama-proxy
description: OpenAI-compatible HTTP proxy that fronts a local Ollama server. Strips unsupported params and forces non-streaming so Zo's provider layer can use free local models (qwen3:14b primary; gemma3:1b fallback) as an LLM provider. Use when configuring or running the local model bridge for a Zo workspace.
compatibility: Created for Zo Computer
---

# Ollama Proxy

Bridges Ollama's native API to the OpenAI-compatible `/v1/chat/completions`
shape that Zo's provider layer expects.

## Run (managed)

Register as a managed service so it auto-starts:

```
mode=http, label="ollama-proxy", local_port=11435,
entrypoint="bash -c 'cd /home/workspace/Skills/ollama-proxy/scripts && PORT=11435 bun proxy.ts'"
```

## What the proxy does

- Forwards `/v1/chat/completions` and `/api/*` to `http://127.0.0.1:11434`
  (Ollama's default bind).
- Forces `stream: false` on completions — Zo's "model stream was interrupted"
  error comes from streaming a local model; this disables it server-side.
- Strips unsupported params (`services`, `tools`, `functions`, ...) that
  Zo sends but Ollama rejects.
- Listens on `*:11435` so it is reachable from outside the container.

## Verify

```bash
curl -s http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}],"stream":false}'
```

Expect HTTP 200 with `"role":"assistant"`.
