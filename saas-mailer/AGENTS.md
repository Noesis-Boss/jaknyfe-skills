# SaaS-Mailer

Standalone Bun/Hono/React MVP for multi-tenant outbound email. Run commands from `saas-mailer/`.

## Current state

- Tasks 1–8 complete for the MVP vertical slice.
- SQLite is the current local persistence layer despite the original PostgreSQL target.
- Mock delivery is deterministic and never sends externally.
- `x-organization-id` is provisional tenant context until authentication and membership checks are implemented.

## Verification

Run `bun test` for the full suite. The dashboard must also be screenshot-verified after frontend changes. Keep provider credentials server-side and preserve organization-scoped composite constraints.

## Feature Log

- 2026-08-19: Completed the MVP vertical slice through end-to-end delivery, event history, tenant isolation tests, and dashboard screenshot verification. Commit `e491a9db` contains the dashboard; Task 8 verification is the next commit.
