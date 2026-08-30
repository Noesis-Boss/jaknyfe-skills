---
name: zorro
description: Self-improving agent with persistent memory via AstraDB. Remembers everything across sessions, learns from feedback, and continuously improves its performance.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---
# Zorro — Self-Improving Agent with Persistent Memory

Zorro is an autonomous agent that:
- **Never forgets**: All facts, preferences, decisions, and context stored in AstraDB via the astra-memory skill
- **Learns from every interaction**: Feedback, corrections, and outcomes are captured and used to improve future responses
- **Self-improves**: Analyzes its own performance, identifies patterns in failures/successes, and adapts
- **Works across sessions**: Memory persists indefinitely — no context loss between conversations

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   User Chat     │────▶│   Zorro Agent    │────▶│  AstraDB Memory │
│   (any channel) │     │  (this skill)    │     │  (astra-memory) │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  Self-Improvement│
                       │  Loop            │
                       │  - Error analysis│
                       │  - Pattern detect│
                       │  - Strategy upd  │
                       └──────────────────┘
```

## Memory Layers (via Clarion model)

| Layer | Purpose | Retention |
|-------|---------|-----------|
| **Fact** | Verifiable facts, preferences, decisions | Permanent |
| **Semantic** | Project knowledge, procedures, concepts | Long-term |
| **Session** | Ephemeral context, in-progress work | Short-term |

## Setup

```bash
# 1. Ensure astra-memory is configured (ASTRA_DB_ENDPOINT, ASTRA_DB_APPLICATION_TOKEN in Settings > Advanced)
# 2. Run initial sync
cd /home/workspace/Skills/astra-memory/scripts
bun run sync.ts sync

# 3. Install Zorro (this skill)
# No additional deps needed — uses astra-memory as library
```

## Usage

```bash
# Start Zorro agent for a task
cd /home/workspace/Skills/zorro/scripts
bun run zorro.ts "task description"

# Query memory
bun run zorro.ts memory "search query"

# Add a fact manually
bun run zorro.ts remember "User prefers X over Y"

# View improvement log
bun run zorro.ts improvements

# List all workspace skills (or match by query)
bun run zorro.ts skills
bun run zorro.ts skills "debug"
```

## Core Capabilities

### 1. Persistent Memory
- Auto-syncs with astra-memory on every interaction
- Queries relevant context before responding
- Stores new facts, corrections, preferences automatically

### 2. Self-Improvement Loop
After each task completion:
1. **Outcome analysis** — Did the result match expectations?
2. **Error categorization** — Was it a tool error, reasoning error, memory gap, etc.?
3. **Pattern detection** — Recurring failure modes across sessions
4. **Strategy update** — Adjust approach for similar future tasks
5. **Memory consolidation** — Promote session learnings to semantic/fact layers

### 3. Cross-Session Continuity
- Loads relevant memories at session start
- Maintains project state in `memory/projects/<name>.md` (Clarion format)
- Tracks "what worked" and "what didn't" per project/domain

## Skill Methodology (wired from github.com/obra/superpowers)

Zorro is skill-aware: it loads relevant `SKILL.md` files from `/home/workspace/Skills` and injects them as execution methodology into the prompts it sends to sub-agents.

- A curated core set is **always** injected during planning/execution:
  `using-superpowers`, `brainstorming`, `writing-plans`, `verification-before-completion`, `systematic-debugging`, `test-driven-development`, `subagent-driven-development`, `dispatching-parallel-agents`.
- Additional skills are matched by the task query (substring scoring against skill name/description) and injected on top.
- The `skills [query]` subcommand lists every installed skill (superpowers ones tagged `[superpowers]`) or previews matches.

To add more skills, drop a skill folder (with `SKILL.md`) under `/home/workspace/Skills/` — Zorro discovers it automatically.

## Integration with astra-memory

Zorro uses the astra-memory skill as its memory backend:
- `bun run /home/workspace/Skills/astra-memory/scripts/sync.ts query <text>` — recall relevant context
- `bun run /home/workspace/Skills/astra-memory/scripts/sync.ts add "<fact>"` — store new facts
- `bun run /home/workspace/Skills/astra-memory/scripts/sync.ts sync` — full sync after session

## Files

- `scripts/zorro.ts` — Main agent entry point
- `scripts/improve.ts` — Self-improvement logic
- `scripts/recall.ts` — Memory retrieval helpers
- `references/MEMORY_PROTOCOL.md` — How memories are structured and queried
## Token-Saver Integration (bash compression)

Zorro auto-wraps compressible bash commands through the token-saver skill to save context tokens. Zo has NO PreToolUse hooks — the persona instruction is the trigger (see Zorro persona prompt, section "Token-Saver Bash Compression").

- Wrapper: `bun run /home/workspace/Skills/token-saver/scripts/run.ts <command>`
- Auto-passthrough for non-compressible commands (ssh, generic python3, interactive); preserves stderr and exit codes.
- Routing check: `... run.ts explain '<command>'`; savings preview: `... run.ts benchmark '<cmd>' --show-removed`
- Upstream: https://github.com/ppgranger/token-saver (v2.6.3). Installed binary: /root/.token-saver. Alias: `ts` in ~/.bashrc.
- Verified 2026-07-31: git log --oneline -50 --stat → 4,097→131 tokens (96.8%); errors/exit codes survive wrapping.
