# SERVICES-REQUEST.md — paste this into a Zo chat

Paste the block below into your Zo chat (this chat is fine). Zo will
create both services, then confirm they're enabled.

```
Please create these two managed services:

1. Service "ollama-server"
   - mode: process (no public endpoint, no port)
   - entrypoint: /usr/local/bin/ollama serve
   This runs the local Ollama LLM server, bound to loopback 127.0.0.1:11434
   by default. The proxy reaches it from inside the container.

2. Service "ollama-proxy"
   - mode: http, PUBLIC (not private), local port 11435
   - entrypoint: bash -c 'cd /home/workspace/Skills/ollama-proxy && bun run scripts/proxy.ts'
   - workdir: /home/workspace/Skills/ollama-proxy
   This exposes an OpenAI-compatible /v1/chat/completions endpoint at
   localhost:11435 (and the public *.zocomputer.io URL) that forwards to
   Ollama at 127.0.0.1:11434. It streams real SSE when the client
   requests streaming (body.stream=true or Accept: text/event-stream),
   otherwise returns buffered JSON; it strips unsupported params
   (tools, tool_choice, functions, services).

   IMPORTANT: the service MUST be public. Zo's provider layer runs in
   Zo's cloud backend, not in this container — a private service makes
   it resolve "localhost" against the wrong host and every chat fails.
   You can verify the public URL responds before continuing:
   curl -s https://ollama-proxy-<your-handle>.zocomputer.io/v1/models

Then run this smoke test and show me the result:
curl -s http://localhost:11435/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}],"stream":false}'
```
