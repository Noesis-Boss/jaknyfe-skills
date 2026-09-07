# Zorro Stack — Presentation & Course Materials

Materials for teaching the architecture behind the **Zorro persona/agent** on Zo Computer, built around three pillars:

1. **Memory** — three-layer system: Clarion file tree → zobodhi fast facts → AstraDB unified hybrid search (local embeddings, $0 embedding cost).
2. **Low token usage** — token-saver (80–97% compression on verbose CLI output), bounded skill injection, terse personas, SSE streaming through a local proxy (first token ~700 ms).
3. **Free LLM connections** — Ollama local models (qwen3:14b primary; gemma3:1b fallback) behind an OpenAI-compatible proxy shim, plus BYOK/free-tier cloud APIs (Gemini flash, ViroScope, TinyFish).

## Files

| File | What it is |
|------|-----------|
| `01-presentation-outline.md` | 15-slide deck outline with speaker notes, live demos, and a demo checklist |
| `02-course-outline.md` | 6-module hands-on course ("Zero-Cost Zo") with labs, success checks, and troubleshooting cheat sheet |
| `zorro-stack-architecture.d2` | Architecture diagram source (render with the d2 CLI: `d2 zorro-stack-architecture.d2 out.png`) |

> **Full Ollama-on-Zo install guide + every fix log:** see
> [`Skills/ollama-proxy/SETUP.md`](../Skills/ollama-proxy/SETUP.md) —
> step-by-step installation, the proxy script, both services, and the
> complete "stream interrupted" war story (private/public trap,
> stale container IPs, SSE passthrough).

## Verified facts baked into these materials (2026-07-31)

- AstraDB: 67 memories (29 zobodhi facts, 16 daily, 12 projects, 6 bootstrap, 2 topics, 1 feedback, 1 reference); last sync inserted 8, skipped 57 (idempotent).
- token-saver v2.6.3: `git log --oneline -50 --stat` → 4,097 → 131 tokens (**96.8%**); `git log --oneline -50` → 804 → 157 (**80.5%**).
- Ollama live through proxy: `curl localhost:11435/v1/chat/completions` (qwen3:14b) → HTTP 200, valid reply.
- Zorro persona model: custom BYOK endpoint (`byok:ee9b6e08-…`).
