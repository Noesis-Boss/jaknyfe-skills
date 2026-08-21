# SaaS-Mailer

- 2026-08-20: Added production `start` and `start:worker` scripts, changed the Site entrypoint from hot development mode to `bun run start`, wired worker polling/batch settings through `loadConfig()`, and removed SMTP from the production adapter list. Registered private managed service `saas-mailer-worker` (`svc_eZzzmcvdlKk`); it is currently in BACKOFF because Zo secrets do not yet include a valid 32-byte `CREDENTIAL_ENCRYPTION_KEY`.

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

- 2026-08-21: Published the dashboard as a private production Zo Site at `https://saas-mailer-jaknyfe.zo.computer`. The Site entrypoint sources `~/.zo_secrets`; the public browser verification correctly reached Zo's sign-in gate.

## Issue Log

- 2026-08-21: Live menu and import failures traced to a duplicate Bun listener in `src/server.ts`. The managed `bun run start` wrapper already serves the exported Hono app; removing the second listener and exporting `app` directly restored the current client bundle and API actions.

- 2026-08-21: Published dashboard controls appeared clickable but several had no handlers. Replaced inert navigation links with interactive buttons, made checklist rows actionable, added visible section feedback, and made the avatar sign out. Live public page screenshot verified after republishing.

- 2026-08-21: Applied Zo Support's managed-service workaround to `saas-mailer-worker`: entrypoint sources `~/.zo_secrets`, service env vars no longer contain literal secret references, and PostgreSQL startup migration now repairs missing durable-queue columns on existing databases. Worker verified RUNNING against Neon.

- 2026-08-21: Zo support bug report saved in `ZO_SUPPORT_BUG_REPORT.md`. Managed process `saas-mailer-worker` receives literal `$CREDENTIAL_ENCRYPTION_KEY`/`$DATABASE_URL` references instead of resolved secret values; shell secrets are valid, but restart and service recreation do not fix propagation.

- 2026-08-20: OAuth start/callback routes and sending-account send routes now support PostgreSQL. Production startup opens the configured PostgreSQL database, and Gmail/Microsoft sends decrypt stored OAuth credentials before invoking provider adapters. Bun server build and focused provider/account/callback tests pass.
- 2026-08-20: Added Gmail/Microsoft OAuth refresh-token exchange, expiry-aware refresh before sending, and encrypted persistence of refreshed credentials in PostgreSQL. Provider, callback, OAuth, and account tests pass; Bun server build passes.

- 2026-08-20: Added network-mocked Gmail and Microsoft Graph sending adapters with normalized provider IDs and typed authentication, quota, transient, and permanent error classification. No external network calls occur in tests. Full suite: 52 passed, 1 skipped.

- 2026-08-20: Event listing and event recording now support PostgreSQL with tenant-scoped async repositories and transactional contact-state pauses; SQLite behavior remains unchanged. Full suite: 48 passed, 1 skipped.
- 2026-08-20: Added PostgreSQL account lookup, contact lookup, message status updates, and sending-adapter boundary primitives for the worker cutover. Full suite: 48 passed, 1 skipped; Bun server build passed.
- 2026-08-20: Added PostgreSQL worker send processing with transactional idempotency claims, retry re-queuing, tenant-scoped contact/account access, provider failure handling, account pausing, message status persistence, and delivery/failure events. Focused worker tests pass; full suite remains 48 passed, 1 skipped.
- 2026-08-20: Added durable PostgreSQL queue leases, expired-lease recovery, bounded exponential retry backoff, graceful worker shutdown, and a Bun worker entrypoint at `src/worker/main.ts`. Full suite: 50 passed, 1 skipped; worker bundle builds with Bun.

- 2026-08-20: Campaign create, approve, enroll, and eligibility routes now select PostgreSQL async services when using the PostgreSQL adapter; SQLite behavior remains unchanged. Bun server build and full suite pass: 48 passed, 1 skipped.

- 2026-08-20: Contacts import and sending-account create/list routes now accept the PostgreSQL adapter, use async tenant authentication, and persist through tenant-scoped repositories. SQLite behavior remains unchanged. Full suite: 48 passed, 1 skipped. Commit `cb57fa99`.

- 2026-08-20: Added PostgreSQL-backed password registration, password verification, membership selection, session creation/revocation, and tenant lookup in `src/server/auth/postgres.ts` and `src/server/auth/middleware.ts`. Existing SQLite auth routes remain unchanged until the route factory is switched during the broader PostgreSQL cutover.

- 2026-08-20: Auth route factory now supports both SQLite and PostgreSQL databases. Registration, login, logout, `/api/auth/me`, and tenant lookup select the correct async/sync implementation from the database adapter.

- 2026-08-20: Live Neon connection verified with the supplied `DATABASE_URL`; PostgreSQL migration and repository contract tests passed (2 tests, 13 assertions). The credential was used ephemerally and not written to the repository. Production route/service cutover remains required before app traffic can use Neon.
- 2026-08-20: Production startup now fails closed instead of silently opening SQLite. The remaining Task 3 work is the async PostgreSQL route/service cutover.

- 2026-08-19: Task 3 added the PostgreSQL initial migration, Bun pooled adapter, tenant-scoped repository contracts, production backup/restore documentation, and a PostgreSQL parity test. Existing SQLite services and tests remain unchanged pending the async service/repository cutover; `TEST_POSTGRES_URL` is required to execute the disposable PostgreSQL contract test.

- 2026-08-19: Completed the MVP vertical slice through end-to-end delivery, event history, tenant isolation tests, and dashboard screenshot verification. Commit `e491a9db` contains the dashboard; Task 8 verification is the next commit.

- 2026-08-19: Task 1 added typed environment parsing and production startup boundaries in `src/server/config.ts`, with focused configuration tests and a secret-free `.env.example`.
- 2026-08-19: Task 2 replaced provisional `x-organization-id` tenant context with password authentication, membership-aware sessions, HttpOnly cookies, logout/revocation, and authenticated route tenancy. Browser login and authenticated dashboard states were screenshot-verified.
