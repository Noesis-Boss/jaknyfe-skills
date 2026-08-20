# SaaS-Mailer

Standalone Bun/Hono/React MVP for multi-tenant outbound email. Run commands from `saas-mailer/`.

## Current state

- Tasks 1–8 complete for the MVP vertical slice.
- SQLite is the current local persistence layer despite the original PostgreSQL target.
- Mock delivery is deterministic and never sends externally.
- `x-organization-id` is provisional tenant context until authentication and membership checks are implemented.
- `src/server/config.ts` is the Task 1 startup contract. Production requires database, session, credential-encryption, and OAuth callback configuration; development uses the mock adapter by default. Keep secrets out of logs and `.env.example`.

## Verification

Run `bun test` for the full suite. The dashboard must also be screenshot-verified after frontend changes. Keep provider credentials server-side and preserve organization-scoped composite constraints.

## Feature Log

- 2026-08-20: Live Neon connection verified with the supplied `DATABASE_URL`; PostgreSQL migration and repository contract tests passed (2 tests, 13 assertions). The credential was used ephemerally and not written to the repository. Production route/service cutover remains required before app traffic can use Neon.
- 2026-08-20: Production startup now fails closed instead of silently opening SQLite. The remaining Task 3 work is the async PostgreSQL route/service cutover.

- 2026-08-19: Task 3 added the PostgreSQL initial migration, Bun pooled adapter, tenant-scoped repository contracts, production backup/restore documentation, and a PostgreSQL parity test. Existing SQLite services and tests remain unchanged pending the async service/repository cutover; `TEST_POSTGRES_URL` is required to execute the disposable PostgreSQL contract test.

- 2026-08-19: Completed the MVP vertical slice through end-to-end delivery, event history, tenant isolation tests, and dashboard screenshot verification. Commit `e491a9db` contains the dashboard; Task 8 verification is the next commit.

- 2026-08-19: Task 1 added typed environment parsing and production startup boundaries in `src/server/config.ts`, with focused configuration tests and a secret-free `.env.example`.
- 2026-08-19: Task 2 replaced provisional `x-organization-id` tenant context with password authentication, membership-aware sessions, HttpOnly cookies, logout/revocation, and authenticated route tenancy. Browser login and authenticated dashboard states were screenshot-verified.
