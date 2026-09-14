---
name: zorro
description: Zorro — self-improving orchestrator with persistent AstraDB-backed memory. Routes tasks starting with "Zorro"/"zorro" or "/z". Provides memory recall (hybrid semantic+lexical), planning, verification, and cross-session continuity. Always use for tasks needing memory, learning, or continuity.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Zorro — self-improving orchestrator

Rebuilt 2026-09-07 after workspace deletion (original script unrecoverable; rebuilt against the surviving astra-memory skill recovered from /mnt/pub).

## Invocation

- Message starts with `Zorro` / `zorro` / `/z` → route here.
- Persona: persistent memory via AstraDB, recall → plan → verify → self-improve.

## Commands (all via `bun run Skills/zorro/scripts/zorro.ts`)

```
memory "<query>" [--limit=N] [--json]   # hybrid semantic+lexical recall
autosync                                # mirror interaction facts into astra-memory
plan "<task>"                           # emit plan → do → verify checklist
```

## Loop for any routed task

1. **Recall** first: `bun run Skills/zorro/scripts/zorro.ts memory "<query>"` — context before action.
2. **Execute** the task with the recalled context (plan for multi-step work).
3. **Verify** the user-facing result (screenshot/endpoint/log — backend green ≠ done).
4. **Autosync**: `bun run Skills/zorro/scripts/zorro.ts autosync` to persist durable facts.
5. **Log** the run with `Skills/agent-contracts/scripts/agent-contract.ts` when the task changes files, services, or external state.

## Backing store

- Memory lives in `Skills/astra-memory/` (recovered 2026-09-07 from /mnt/pub/astra-memory).
- `zorro.ts memory` shells out to `Skills/astra-memory/scripts/sync.ts query "<q>" --json`.
- `zorro.ts autosync` runs `Skills/astra-memory/scripts/sync.ts sync`.
- If astra-memory's backend is unreachable, zorro.ts reports the error plainly instead of guessing.
