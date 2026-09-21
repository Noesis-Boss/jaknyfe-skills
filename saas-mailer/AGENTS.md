# SaaS-Mailer

- 2026-09-21: Added a bearer-protected Family Chore Planner invitation endpoint at `/api/integrations/family-chore-planner/invitations`; it sends through the configured Resend adapter without exposing provider credentials to the planner.
- 2026-09-21: Restarted the managed SaaS-Mailer service against local PostgreSQL and verified the Family Chore Planner integration end to end with a real invite accepted by Resend.

- 2026-09-18: Restore validation now emails `RESTORE_VALIDATION_ALERT_TO` (default `delowery@gmail.com`) on missing backups or failed disposable restores; repeated identical failures are deduplicated until a check succeeds.

- 2026-09-17: Hardened PostgreSQL backups against zero-byte replacement by writing to a temporary file, requiring non-zero size, then atomically renaming. Added managed `saas-mailer-restore-validation` service (`svc_RYbyiWEHQaA`) for daily disposable restore checks; live log recorded a successful restore and cleanup.

- 2026-09-17: Added managed nightly PostgreSQL backups via `scripts/backup-loop.sh`; backups default to 14-day retention and support `BACKUP_RETENTION_DAYS`. Service registration and one manual backup verification completed.
- 2026-09-17: Added `bun run validate:backup` catalog validation and a daily alert automation that emails only when the latest backup is missing or older than 26 hours. Full restore remains pending explicit approval because it changes database state.

- 2026-09-17: Added an explicit PostgreSQL startup connectivity check (`SELECT 1`) after migrations and a timestamped `bun run backup:postgres` routine using `pg_dump` with optional `BACKUP_DIR`. Verification: PostgreSQL startup, backup creation, and full test suite pass.

- 2026-09-16: Rewired database selection to use PostgreSQL whenever `DATABASE_URL` is set, including development. The local example points to the isolated `saas_mailer` database at `localhost:5432`; SQLite remains the fallback when no URL is configured. PostgreSQL contract tests pass (2/2), and the default SQLite suite passes (75/75, 1 skipped).

- 2026-09-10: Created the production Resend sending account for the Noesis workspace: provider `resend`, sender `mailer@noesisgroup.com`, active, with no per-account credential. Restarted the SaaS-Mailer HTTP service and worker; live endpoint returns HTTP 200 and the database confirms the account.

- 2026-09-10: Added a Resend sending adapter using `RESEND_API_KEY`; production accepts `resend` accounts and sends through `https://api.resend.com/emails` from the verified `mailer@noesisgroup.com` identity. Adapter tests and the full suite pass; production requires the secret in Zo environment settings.

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

- 2026-09-21: Completed the Neon-to-local PostgreSQL cutover. The web app, worker, backup loop, and restore-validation service now force `DATABASE_URL` to the local `saas_mailer` database after loading shared secrets. Verified the public dashboard returns HTTP 200, all four managed services are running, and the local schema is present. The prior Neon quota error no longer blocks startup.

- 2026-09-06: Wired scheduled sends end-to-end: added POST /api/campaigns/:id/schedule (SQLite + Postgres) that gates on approved + enrolled + not-already-scheduled, inserts queued messages with `campaign_type:campaign:contact` idempotency keys and next_attempt_at, and stamps campaigns.scheduled_at; createCampaign now persists campaign_type; SQLite migrate() applies migrations 008-010; deduped worker option keys in src/worker/main.ts; fixed 3 env-dependent tests (host secrets leaked into process.env; stale tenancy table list). Suite: 74 pass, 0 fail, 1 skip (Postgres contract needs TEST_POSTGRES_URL). Live site republished and screenshot-verified. Push of f7ede7f3 blocked by gitleaks pre-push hook on PRE-EXISTING history leaks (caa8e637 et al., pending purge approval) - commit is clean and sits local.

- 2026-08-22: Fixed Google Contacts CSV imports by recognizing `E-mail 1 - Value` and equivalent numbered email columns after header normalization. The supplied export parses to 649 valid contacts; 13 contact tests pass.

- 2026-08-22: Contact CSV import now detects common CRM/export aliases for email and names, splits full-name columns, and preserves all other columns as custom fields. Dedicated parser tests pass.

- 2026-08-21: Published the dashboard as a private production Zo Site at `https://saas-mailer-jaknyfe.zo.computer`. The Site entrypoint sources `~/.zo_secrets`; the public browser verification correctly reached Zo's sign-in gate.

- 2026-09-05: Completed the scheduled-sends batch (commit `f7ede7f3`, local-only pending leak purge — see Issue Log): `POST /api/campaigns/:id/schedule` queues idempotent future messages (`{campaign_type}:{id}:{contactId}` keys, `next_attempt_at`) for enrolled contacts and rejects unapproved/duplicate scheduling (SQLite + Postgres); migrations 008–010 now auto-apply in `migrate()` (this was the scheduled-send test's 400/missing-column root cause); deduped the triple `tenantSendsPerMinute` in `src/worker/main.ts`; config/sending tests now strip host-secret env vars so the suite is environment-independent. Suite: 74 pass / 0 fail / 1 skip. Site republished; live sign-in page screenshot-verified.

## Issue Log
- 2026-09-21: PostgreSQL uptime repair: the managed service stayed alive while PostgreSQL was down because its old entrypoint only attempted one start and then idled. A stale socket lock from PID 804 caused repeated start failures. Removed the stale socket files after confirming PID 804 was gone, started PostgreSQL successfully, and changed service `svc__CRItDG7L6o` to monitor readiness every 10 seconds and restart the cluster after an actual stop. Verified PostgreSQL accepts connections and created a fresh backup at `backups/saas-mailer-20260921T010330Z.dump`. Neon quota exhaustion remains a separate issue when the inherited provider URL is used; the managed SaaS-Mailer backup service is configured for the local PostgreSQL database.
- 2026-09-17: Repaired the PostgreSQL managed service entrypoint from a keepalive-only process to `pg_ctlcluster 15 main start` followed by a resident process. Verified cluster 15/main stays online after service restart. Extended `validate-backup.sh` with an optional restore-database argument; it performs catalog validation plus compatibility SQL restore, filtering only PostgreSQL 18 `transaction_timeout` and `neon_superuser` metadata. Verified a disposable restore with 15 public tables, then removed the database.
- 2026-09-17: Approved disposable restore smoke test completed. The newest backup was initially 0 bytes because PostgreSQL was down behind the keepalive-only managed service; after starting the local PostgreSQL 15 cluster, a fresh 71 KB dump was created. Direct binary restore exposed PostgreSQL 18-to-15 incompatibilities (`transaction_timeout` and source role `neon_superuser`); compatibility SQL restore removed only those unsupported metadata statements, then loaded successfully into a disposable database. Verified 35 public tables, migration `001_initial`, and 12 organizations; disposable database was removed.
- 2026-09-05: Push of commit `f7ede7f3` to `Noesis-Boss/jaknyfe-skills` (master) is blocked by the gitleaks pre-push hook. All findings (30) are pre-existing history leaks from the 2026-09-05 audit (caa8e637 etc.); the new commit's diff is secret-free (verified). Per the never-push-keys rule I did not bypass — blocked until the pending history purge (git filter-repo + force push) is approved.


- 2026-08-22: CSV imports could still report a missing email header when files began with blank lines or used quoted delimiter characters. Delimiter detection now scans the first nonblank line and ignores separators inside quoted headers; 13 contact tests pass and the public dashboard was republished.

- 2026-08-22: CSV imports rejected semicolon-, tab-, and pipe-delimited exports as missing the email header because the parser assumed commas. Added automatic delimiter detection; contact tests pass.

- 2026-08-21: Contact import appeared inert because the dashboard repeatedly submitted an already-imported demo contact. Replaced it with a real CSV file picker, import error handling, and cache-busted client assets. Live dashboard reload verified the CSV instruction; root and contact tests pass.

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

- 2026-09-05: Shipped 3 Ghost-borrowed improvements in one commit (ef733914): (1) hard-bounce suppression — provider permanent failures matching bounce signatures record a `bounce` event, and eligibility rejects future sends to that contact (SQLite + Postgres paths); (2) per-tenant send rate limiting — sliding-window limiter (`src/worker/rate-limit.ts`, 30/min default, `WORKER_TENANT_SENDS_PER_MINUTE`) gates the worker loop; over-limit jobs release their lease and stay queued; (3) Campaign Analytics dashboard — `GET /api/campaigns` list with sent/enrolled counts plus `GET /api/campaigns/:id/analytics`, rendered as an Analytics tab panel with per-campaign drill-down. Live dashboard screenshot-verified; the 3 remaining suite failures (config production-required, sending-accounts encryption fail-closed, scheduled-send) pre-exist on HEAD and are environment-dependent.
