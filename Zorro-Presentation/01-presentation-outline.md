# Presentation Outline — "The Zorro Stack"

**Title:** The Zorro Stack: Persistent Memory, Token Discipline, and Free LLMs on Zo Computer
**Audience:** Zo users, agent-curious builders
**Format:** 15 slides, \~20–25 min + live demos
**Companion diagram:** `file zorro-stack-architecture.png` / `.d2`

---

## Act 0 — Hook

### Slide 1 — Title

- Title + one-line promise: "An agent that remembers everything, spends almost nothing on tokens, and runs on models that cost $0."
- Speaker note: open with the pain — every AI agent you've used forgets you between chats and every message costs money.

### Slide 2 — The problem

- Default agent behavior: no memory (each session starts cold), verbose tool output eats your context window, and every model call is metered.
- Three failures users hit: "it forgot who I am", "my context filled up with a git log", "I can't afford / don't want to pay for tokens".
- Proof point: this was a real problem — the "model stream interrupted" bug (Zo vs. Ollama streaming mismatch) required a 70-line proxy fix.

### Slide 3 — What Zorro is

- Zorro is a *persona*, not a separate app: a self-improving agent definition that runs on Zo Computer.
- It routes every task through a skill (`file Skills/zorro/scripts/zorro.ts`) with subcommands: `task`, `memory`, `remember`, `improvements`, `plan`.
- The persona prompt itself encodes the memory rule and the token-saver rule — behavior lives in the persona, machinery lives in skills.
- Architecture diagram: show `file zorro-stack-architecture.png` — three pillars labeled.

---

## Act 1 — Pillar: Memory

### Slide 4 — Three-layer memory

- Layer 1 — **Clarion file tree** (structured): `file USER.md` (who you are), `file MEMORY.md` (one-line index), `memory/daily|projects|feedback|reference` with frontmatter schema.
- Layer 2 — **zobodhi-memory** (fast facts): flat `file memory.json`, substring search, for quick cross-session retrieval.
- Layer 3 — **AstraDB** (unified search): everything mirrored into one DataStax AstraDB collection with local embeddings.
- Why three? Each layer is a different speed/cost tradeoff: files you can read with any tool, JSON for grep-speed facts, vector DB for fuzzy "what did we say about X" recall.

### Slide 5 — The AstraDB layer (the magic)

- `file sync.ts` mirrors both sources → `memories` collection in AstraDB.
- Local embeddings: `nomic-embed-text-v1.5` (768-dim), run on the machine — no embedding API cost.
- Hybrid search: semantic (embedding similarity) + lexical (keyword) merged with RRF ranking. Misspelled or paraphrased questions still match.
- Proof point: 67 memories live today (29 facts, 16 daily sessions, 12 projects, rest bootstrap/topics/feedback/reference); last sync inserted 8, skipped 57 (idempotent upserts keyed on `source + text[:200]`).
- Live demo: `bun run Skills/astra-memory/scripts/sync.ts query "<weird phrasing>" --json` returns the right memory.

### Slide 6 — Capture rules (how memory stays fresh without effort)

- Start of every conversation: read `file USER.md` → `file MEMORY.md` → newest `memory/daily/` → run the hybrid memory query.
- During conversation: auto-save on new preference, correction, project context, external system references.
- End of session: offer a daily note (`file memory/daily/YYYY-MM-DD.md`), append never overwrite.
- Corrections are absolute dates, not "last week".
- Speaker note: memory is a *discipline*, not a database — the rules are what make the DB useful.

---

## Act 2 — Pillar: Low Token Usage

### Slide 7 — Where tokens leak

- Verbose CLI output (git logs, npm installs, test runs) — the #1 context-window killer.
- Bloated system prompts (every skill's full text injected every time).
- Streaming chatter and unsupported params round-tripped through proxies.
- Chatty responses (the model re-explaining itself).

### Slide 8 — token-saver: the 96.8% fix

- token-saver v2.6.3: content-aware CLI output compressor, 32 specialized processors (git, docker, npm/bun, cargo, pytest, gh, kubectl, terraform, ...).
- Each processor understands its tool's output and strips noise while preserving errors, diffs, and actionable lines.
- Verified on this machine (2026-07-31):
  - `git log --oneline -50 --stat`: **4,097 → 131 tokens (96.8%)**
  - `git log --oneline -50`: **804 → 157 tokens (80.5%)**
- Live demo: run `bun run Skills/token-saver/scripts/run.ts git log --oneline -50 --stat`, show the before/after token count via `benchmark`.
- Honest caveat: Zo does not run Claude Code PreToolUse hooks, so there is no auto-trigger — the agent is the trigger via a wrapper (`file run.ts`), aliased as `ts`.

### Slide 9 — Token discipline beyond compression

- **Bounded skill injection:** Zorro loads skills by substring rank and caps each body at 2,500 chars (`SKILL_HEAD_LIMIT`) — only the relevant methodology enters the prompt.
- **Terse personas:** the Caveman Ultra persona restricts responses to 1–3 word sentences; rules forbid recaps and meta-commentary.
- **No buffered waits:** the proxy streams real SSE when asked (first token \~700 ms) and strips unsupported params — no 30–47 s buffered JSON stalls.
- **Verification loops:** "done = visible result" (curl, screenshot, log line) — fewer failed retry loops, which are the real token killer.

---

## Act 3 — Pillar: Free LLM Connections

### Slide 10 — The local model: Ollama

- Ollama runs on the Zo server itself (`ollama-server` service), models on disk: `qwen3:14b` (primary), `gemma3:1b` and `gemma3:4b` (fallback).
- Free (no API metering), runs locally (models never leave the machine), always available.
- Live demo: `curl http://localhost:11435/v1/chat/completions -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}]}'` → 200 OK.
- Full step-by-step install + lesson log: `file Skills/ollama-proxy/SETUP.md`.

### Slide 11 — The proxy shim (why it works)

- Ollama's API isn't a drop-in OpenAI replacement; Zo's provider layer expects OpenAI semantics and streaming.
- `ollama-proxy` (`file Skills/ollama-proxy/scripts/proxy.ts`, \~100 lines of Bun) fixes it in four moves:
  1. **Streams real SSE** when the client asks (`body.stream` or `Accept: text/event-stream`) — first byte \~700 ms, ends `[DONE]`.
  2. Strips params Ollama doesn't support (`tools`, `tool_choice`, `functions`, `services`).
  3. Rewrites the Host header so Ollama accepts the call.
  4. Injects a fallback chunk if a stream somehow ends with zero content.
- Zo provider config: Base URL `https://ollama-proxy-<handle>.zocomputer.io/v1`, API key `ollama`, model `qwen3:14b` (primary).
- **The proxy must be a public hosted service** — a private service makes Zo's cloud provider resolve `localhost` in its own backend, not your container.
- Full history: the "model stream interrupted" fix log in `file Skills/ollama-proxy/SETUP.md` (private/public trap 07-31, SSE passthrough 08-01).

### Slide 12 — BYOK and free tiers

- Zo supports Bring Your Own Key: OpenAI, Anthropic, OpenRouter, custom OpenAI-compatible endpoints.
- Zorro itself runs on a `byok:` model — a custom endpoint wired into the persona.
- Free-tier cloud APIs in the stack: Gemini 2.5-flash (used for the video pipeline when the OpenAI key ran dry), ViroScope idea generation (no key, \~5/day), TinyFish (web search/browser with vault credentials).
- Speaker note: the pattern is "local for the routine, free tier for the special, paid BYOK as the fallback" — you only pay when the job demands it.

---

## Act 4 — Closing

### Slide 13 — The self-improvement loop

- Zorro logs every task: `improvements.log`, `session.log`, `plans.log` — success/outcome/lesson/strategy per run.
- Superpowers methodology (14 skills, e.g. brainstorming, writing-plans, verification-before-completion) is injected into execution prompts, so the agent improves *how it works*, not just what it knows.
- Memory improvements get promoted: "Reinforce the approach used; promote successful patterns to semantic memory."

### Slide 14 — Verification culture (why this stack survives)

- Every "done" is backed by: curl output, screenshot, health endpoint, or log line.
- AGENTS.md keeps a fix log with dates, root causes, and what worked/failed (see the "stream interrupted" log: 2026-07-19 → 2026-08-01 — private-vs-public proxy trap, then true SSE passthrough).
- The setup is documented as code: skills, rules, and memory files are all plain text the user owns.

### Slide 15 — Takeaway / call to action

- The recipe: **persona that encodes behavior + layered memory + compression discipline + a local/free model behind a compatibility shim.**
- Cost of the core stack: $0 in model fees (Ollama), $0 in embedding fees (local nomic), $0 in idea APIs.
- Next: the course — "Zero-Cost Zo" — teaches each layer hands-on. (See `file 02-course-outline.md`.)

---

## Appendix — live demo checklist

1. AstraDB query with a deliberately vague/paraphrased question (hybrid RRF).
2. token-saver `benchmark git log --oneline -50 --stat` (show 96.8%).
3. Ollama through the proxy: curl 200 + reply body.
4. `sync.ts status` (67 memories, source/layer breakdown).
5. Zo provider page screenshot showing Base URL → `https://ollama-proxy-<handle>.zocomputer.io/v1` (mask the key).