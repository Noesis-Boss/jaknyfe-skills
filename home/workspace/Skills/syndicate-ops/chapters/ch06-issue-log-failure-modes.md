---
name: ch06-issue-log-failure-modes
description: "Known task-worker failure modes from the issue log and their fixes."
---

# Chapter 6 — Issue Log: Known Failure Modes

## 2026-06-24 — Task Worker boot and Syndicate API fix
**Problem:** Task Worker started with a hardcoded localhost Syndicate API URL; failed to authenticate with `ConnectionRefused` and could not poll tasks.

**Tried:**
1. Ran `bun run /home/workspace/Skills/task-worker/scripts/task-worker.ts` directly → **Failed:** `http://localhost:57548/api/auth/login` → ConnectionRefused
2. Checked `list_user_services`, `service_doctor`, worker source → **Worked:** confirmed service existed but had wrong runtime path/working directory and no live API override
3. Updated worker service to run from `Skills/task-worker`; changed worker code to default to the production URL → **Worked:** authenticated successfully
4. Set `SYNDICATE_API_URL` on the running service, rechecked logs → **Worked:** log shows `Worker authenticated`

**Final result:** Worker running, polling live Syndicate backend.

## 2026-06-25 — JSON parsing and stale export cleanup
**Problem:** Worker script carried a stale Hono route block at the bottom and brittle JSON handling, causing Bun to abort with `Unexpected export` and the loop to spam `Failed to parse JSON` on empty/non-JSON responses.

**Tried:**
1. Ran worker directly → **Worked:** authenticated + started polling; **Failed:** repeated JSON parse errors
2. Inspected `task-worker.ts`, Syndicate API responses, service logs → **Worked:** API returns JSON; failure was in the worker script
3. Replaced direct `r.json()` with a safer `fetchJson()` helper; `/zo/ask` reads text first, parses JSON only when present → **Worked:** removed brittle parsing path
4. Removed stale Hono route block; restarted `task-worker` service → **Worked:** clean start, healthy, polling without stale route code

**Final result:** Worker is a clean long-lived process.

## Debugging playbook (from these two incidents)
1. Run the worker directly to isolate script vs. service config
2. Verify service env: `SYNDICATE_API_URL` (production, not localhost) and `ZO_CLIENT_IDENTITY_TOKEN` (real token, not placeholder)
3. Fix code, then update the service config, then restart and check logs
4. Use a resilient `fetchJson()` helper — read text first, parse only when present
