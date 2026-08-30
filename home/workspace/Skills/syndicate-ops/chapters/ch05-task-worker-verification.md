---
name: ch05-task-worker-verification
description: "Task worker verification results, 429 retry behavior, and required service configuration."
---

# Chapter 5 — Task Worker Verification & Operations

## Verified working components
1. **API authentication** — worker authenticates with `worker@test.local` credentials
2. **Company/task fetching** — from `https://syndicate-jaknyfe.zocomputer.io`
3. **Task claiming** — claims tasks assigned to CTO/engineer roles via `POST /api/tasks/:id/claim`
4. **Task execution** — executes via `/zo/ask` with role-based instructions
5. **Retry logic** — handles 429 rate limiting with exponential backoff (5 attempts, 15s base delay)

## Rate limiting (429) — expected behavior
- Workspace limit of 5 concurrent `/zo/ask` requests causes throttling in high-concurrency periods
- **Not a bug** — the worker correctly retries rather than failing
- Backoff sequence observed: 15s / 30s / 45s / 60s / 60s

## Required service configuration
The task worker service (svc_30dqJ3qDpNQ) must have:
- `SYNDICATE_API_URL` = `https://syndicate-jaknyfe.zocomputer.io` (NOT a localhost URL)
- `ZO_CLIENT_IDENTITY_TOKEN` = a valid token (not a placeholder)

Both were once wrong/missing; that is the most common worker failure cause.

## Task status flow
`backlog → ready → running → done/blocked` (working correctly)

## Example verification record
Task `tsk_a092cce9e7c5f` "Fresh test task" — CTO agent (Atlas, agt_b502a6ac0223) for BankBox (slug `bankbox`, ticker `BBX`): claimed and executed successfully, marked done with a full infrastructure verification report in the task result.
