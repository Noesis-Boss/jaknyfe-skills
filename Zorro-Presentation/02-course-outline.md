# Course Outline — "Zero-Cost Zo: Memory, Token Efficiency, and Free LLMs"

A hands-on course that takes a new Zo user from "what is a persona?" to a working, self-remembering agent running on free local models — the same architecture Don runs as the Zorro stack.

---

## Course metadata

| Field | Value |
|-------|-------|
| Title | Zero-Cost Zo: Memory, Token Efficiency, and Free LLMs |
| Audience | New Zo users; comfortable with a terminal and JSON; no prior Zo knowledge |
| Prerequisites | A Zo Computer account, 30 min of setup (Settings → Advanced for secrets), basic bash |
| Format | 6 modules: concept → demo → lab → success check. Self-paced or 2 half-day workshops |
| Total time | ~8–10 hours hands-on (or ~4 hours if skipping AstraDB deep dive) |
| Outcome | Each student ships a "mini-Zorro": persona + memory + token-saver + free local model, verified end-to-end |

## Teaching principles (from how Don's stack is actually run)

1. **Verify, don't guess** — every lab ends with a check the student can run (curl, screenshot, log line). "Done = visible result."
2. **Ship small, iterate** — each module produces something working; no big-bang builds.
3. **Minimum viable machinery** — start with files and grep; add vector search only when plain search stops working.
4. **Scope isolation** — when touching one account/provider, name the others and leave them alone.

---

## Module 0 — Orientation (45 min)

**Objectives:** student can name the four Zo primitives and where they live in the UI.

- What Zo is: a personal server, not a chat app. Files are the soul — everything is plain text the user owns.
- The four primitives:
  - **Personas** ([Settings → AI → Personas](/?t=settings&s=ai&d=personas)) — identity + behavior rules + model choice
  - **Skills** (`Skills/`) — executable workflows, each a `SKILL.md` + scripts
  - **Automations** — scheduled agents
  - **Services / Sites / Space** — hosted processes and pages
- Rules ([Settings → AI → Rules](/?t=settings&s=ai&d=rules)) — the user's persistent behavioral preferences; the highest-priority layer.
- **Lab 0:** create a throwaway persona with one behavior rule; chat with it; confirm the rule changed a reply.
- **Success check:** screenshot of persona selector + one reply that obeys the rule.

---

## Module 1 — Memory from zero (2–2.5 hrs)

**Objectives:** student builds a three-layer memory system and proves cross-session recall.

### 1a. Layer 1 — the file tree (structured memory)
- Concepts: `USER.md` (who am I), `MEMORY.md` (one-line index), `memory/daily|projects|feedback|reference`, frontmatter schema (`name`, `description`, `type`).
- Rules of capture: load at conversation start; save on preference/correction/project context; daily notes append-only; index stays one line per entry.
- **Lab 1a:** write your own `USER.md` + `MEMORY.md` + first `memory/daily/YYYY-MM-DD.md`. Start a new chat, confirm the agent picks up a fact from the file.
- **Success check:** new chat knows your name/project without being told.

### 1b. Layer 2 — fast facts (zobodhi-memory)
- Concepts: flat `memory.json`, substring search, `--add` for quick facts; complements the structured tree.
- **Lab 1b:** add 5 facts, run `memory.ts --query`, confirm retrieval.
- **Success check:** a fact added in chat is found by query in a new session.

### 1c. Layer 3 — AstraDB (unified hybrid search) *optional but recommended*
- Concepts: why vector search (fuzzy recall: "that thing we discussed about the red project" matches by meaning); embeddings run locally (`nomic-embed-text-v1.5`, 768-dim) so embedding costs $0; hybrid semantic+lexical RRF ranking; idempotent sync (`source + text[:200]` upsert key).
- Setup: DataStax AstraDB free tier → endpoint + token into [Settings → Advanced](/?t=settings&s=advanced) as `ASTRA_DB_ENDPOINT` / `ASTRA_DB_APPLICATION_TOKEN`.
- Commands: `sync.ts sync | query | add | status | tail`.
- **Lab 1c:** sync both sources, run a deliberately misspelled/paraphrased query, watch hybrid search still return the right memory; check `status` for the source/layer breakdown.
- **Success check:** `sync.ts status` shows both sources, and a paraphrased query hits the right memory.

---

## Module 2 — Token discipline (2 hrs)

**Objectives:** student can find where tokens leak and can cut 80–97% of CLI noise.

- Where tokens leak: verbose CLI output, oversized prompts, retry loops, chatty replies.
- token-saver (v2.6.3): content-aware compressor, 32 processors, preserves errors/diffs.
- Zo reality: no PreToolUse hooks in Zo — the agent is the trigger; the wrapper (`Skills/token-saver/scripts/run.ts`) is the fix; `ts` alias.
- Prompt hygiene: bounded skill injection (only relevant skill bodies, capped length), terse personas, no recaps in replies.
- **Lab 2a:** `bun run Skills/token-saver/scripts/run.ts benchmark git log --oneline -50 --stat` — record your before/after token counts (expect ~90%+).
- **Lab 2b:** run a real task twice — once with raw verbose output, once wrapped — and compare context consumption.
- **Lab 2c:** enable a terse persona (e.g. Caveman-style rule) and watch reply size drop.
- **Success check:** student can demonstrate ≥80% token reduction on a real command and explain when wrapping is/ isn't worth it (skip trivial, short output).

---

## Module 3 — Free LLMs (2–2.5 hrs)

**Objectives:** student runs a local model, wires it into Zo through a compatibility proxy, and knows when free tiers are enough.

### 3a. Local models with Ollama
- Install Ollama, pull the primary model `qwen3:14b` (~9 GB); optionally `gemma3:1b` (~0.8 GB) as a fast fallback.
- Run as a managed process (never ad-hoc): `register_user_service` with `/usr/local/bin/ollama serve`, process mode, no public port.
- **Lab 3a:** `curl http://127.0.0.1:11434/api/tags` shows your models; direct generate call works.

### 3b. The OpenAI-compatible proxy shim
- Why it's needed: Zo's provider layer speaks OpenAI semantics + streaming; Ollama differs.
- What the proxy does (4 moves): stream real SSE when the client asks (first byte ~700 ms); strip `tools`/`tool_choice`/`functions`/`services`; rewrite the Host header; inject a fallback chunk if a stream ends empty. ~100 lines of Bun.
- Wire-up: proxy on `:11435` as a **public** managed HTTP service (`ollama-proxy-<handle>.zocomputer.io`); provider config: Base URL `https://ollama-proxy-<handle>.zocomputer.io/v1`, key `ollama`, model `qwen3:14b` (primary). The public URL matters: a private service resolves `localhost` in Zo's cloud backend, not your container.
- **Lab 3b:** `curl http://localhost:11435/v1/chat/completions -d '{"model":"qwen3:14b","messages":[{"role":"user","content":"Say OK"}]}'` → 200 with a reply. Then use the model in a real chat.
- **Success check:** a Zo chat session answers using the local model, verifiable by provider logs.

### 3c. BYOK and free tiers
- BYOK providers: OpenAI, Anthropic, OpenRouter, custom OpenAI-compatible endpoints ([Settings → AI → Providers](/?t=settings&s=ai&d=providers)).
- Free-tier candidates: Gemini 2.5-flash (generous free quota), OpenRouter `:free` models, no-key services (ViroScope idea API, TinyFish search).
- Decision rule: local for routine → free tier for special → paid BYOK only when the job demands it.
- **Lab 3c:** wire one free-tier provider; switch a persona to it; run one task.
- **Success check:** persona model dropdown shows the free/BYOK model and a task completes through it.

---

## Module 4 — Verification culture (45 min)

**Objectives:** student adopts proof-based completion — the habit that keeps the whole stack reliable.

- Rules: "done = visible result" (curl, screenshot, health endpoint, log line); never trust a build alone; screenshot deployed pages.
- AGENTS.md as living documentation: fix logs with date, root cause, worked/failed, next step (real example: the "model stream interrupted" log, 2026-07-19 → 2026-07-26).
- **Lab 4:** take a task you completed in Module 3, add a Fix/Feature Log entry to your project's `AGENTS.md` with the exact verification evidence.
- **Success check:** a peer (or instructor) can reproduce your task from your log alone.

---

## Module 5 — Capstone: build your mini-Zorro (2 hrs)

**Objectives:** student integrates all modules into one working agent and presents it.

Build:
1. A persona (name, image, model = your free/BYOK model) whose prompt encodes: memory query at start, memory save on facts, terse replies.
2. A skill `Skills/<name>/` with a `SKILL.md` + one script (e.g. a memory wrapper) that the persona calls.
3. Memory: `USER.md` + `MEMORY.md` + 3 daily notes + 5 zobodhi facts (+ AstraDB if covered).
4. Token-saver wrapped in at least one real workflow.
5. Verification: a one-page `AGENTS.md` with the fix/feature log.

Capstone demo (5 min each): start a *new* conversation; show the agent recalling a fact from a previous session, running a compressed command, and answering via the local/free model. Screenshot the proof.

**Success criteria (pass = all five):**
- [ ] Recalls a fact from an earlier session without being reminded
- [ ] Daily note exists for today, append-only
- [ ] One command run through token-saver with measured reduction
- [ ] Chat answered by local (Ollama) or free-tier model
- [ ] `AGENTS.md` log entry with verifiable evidence

---

## Materials & references

- This repo's `01-presentation-outline.md` (slide deck mirrors the course modules)
- `zorro-stack-architecture.d2` (diagram source)
- Key paths students will touch:
  - `Skills/zorro/scripts/zorro.ts` (reference implementation)
  - `Skills/astra-memory/scripts/sync.ts` (hybrid memory CLI)
  - `Skills/token-saver/scripts/run.ts` (compression wrapper)
  - `Skills/ollama-proxy/scripts/proxy.ts` (compatibility shim)
- Settings links to hand out: [Personas](/?t=settings&s=ai&d=personas), [Rules](/?t=settings&s=ai&d=rules), [Providers](/?t=settings&s=ai&d=providers), [Advanced/secrets](/?t=settings&s=advanced)

## Troubleshooting cheat sheet (from real incidents)

| Symptom | Cause | Fix |
|---------|-------|-----|
| "model stream interrupted" / "streamed response ended without content or tool calls" | Provider hit the wrong target (direct Ollama `:11434`, stale container IP, or private proxy URL) or got buffered JSON when it expected SSE | Use the **public** proxy URL `https://ollama-proxy-<handle>.zocomputer.io/v1`; proxy streams real SSE since 2026-08-01 |
| Provider connection timeout | stale container IP in Base URL | Use the public `*.zocomputer.io` URL — it never goes stale; container IPs change every restart |
| Memory query returns nothing | layers not synced | `sync.ts sync`, then `status` |
| token-saver not auto-running | Zo has no PreToolUse hooks | invoke via `run.ts` wrapper / `ts` alias |
| Chat too verbose | persona/rules don't constrain | add terse-reply rule or terse persona |

## Follow-up

- Community: publish your capstone skill to the Zo skills registry (`zocomputer/skills` — precedent: astra-memory PR #94).
- Extension paths: automations that post to X/email on a schedule, hosted services exposing your proxy/API, custom BYOK endpoints for niche models.
