# SaaS-Mailer

- 2026-09-02: Added optional shared Authentik OIDC login routes at `/api/auth/oidc/start` and `/api/auth/oidc/callback`, with PKCE state and existing tenant-session reuse. UI exposes “Sign in with Noesis” when configured. `bun test`: 32/32 passed. Authentik client provisioning and Momball integration remain pending.

- 2026-09-02: Added CSV import feedback: multipart uploads now preserve browser boundaries, and Contacts shows imported, skipped, and invalid-row totals after each import. Commit `cd36ba7`; 32/32 tests pass and the live dashboard screenshot renders.

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
- 2026-09-03: Added dashboard scheduling for approved newsletters, including queue confirmation and scheduled-time display, plus per-campaign analytics summaries. `bun test` 32/32 and server bundle pass; Vite build remains blocked by the existing missing `index.html`; local browser screenshots verify the dashboard and newsletter composer render.
- 2026-09-03: Began Ghost-inspired unified campaigns: added newsletter/sequence campaign metadata, preview/template/schedule fields, tenant-scoped subscriber preferences with unsubscribe suppression, preference API routes, and newsletter-aware composer controls. Existing 32-test suite passes; server bundle and diff checks pass. Vite wrapper remains blocked by the pre-existing missing `index.html` entry.
- 2026-09-02: Extended CSV import feedback with invalid-row reasons and downloadable `invalid-contacts.csv`; imports can assign valid rows to an existing list, create a new list, or use a CSV list column. Tests pass and the live dashboard renders the updated import panel. Commit `f6fd1b8`.
- 2026-09-02: Added tenant-scoped sending-account removal for SQLite and PostgreSQL, with confirmation UI and foreign-key protection when an account is still used by campaigns or messages. Tests pass; live dashboard verification completed.
- 2026-09-01: Cleared the confirmed `don@noesisgroup.com` SaaS-Mailer tenant contact list. Deleted 1,101 contacts; campaigns, sending accounts, and contact-linked history were preserved because no dependent records existed.
- 2026-09-01: Fixed contact management for both SQLite and PostgreSQL detail, edit, and delete routes; bumped client assets to `20260901-2` to force browsers to load the management UI. Tests pass and production restarted.
- 2026-09-01: Fixed contact management discoverability: the Overview Contacts metric now opens the Contacts management panel, and the contact edit form now keeps first/last-name edits in React state before saving. Tests pass; live site restarted for verification.
- 2026-08-31: Shipped the multi-step campaign editor: dynamic step rows (subject, body, per-step delay minutes), add/remove steps at creation, step_count in campaign lists (SQLite and Postgres), step totals on campaign rows, and the Enroll action moved to approved campaigns. Browser-verified end-to-end (3-step create, approve, enroll; API step_count=3) and live on the production site; commit `032bdc4`; 32/32 tests pass.
- 2026-08-31: Added sending-account connect UI: "Connect Gmail" and "Connect Microsoft" OAuth buttons that call `GET /api/oauth/<provider>/start` (verified: 302 to Google consent with signed state and correct redirect URI), plus a mock test-account connect form that POSTs `{provider:"mock", email}` to `POST /api/sending-accounts`, shows the account with provider and status, and updates the header's active-accounts pill. Verified in-browser (mock account connected; list and pill updated) and on the live production site after restart; commit `b7e16b7`.
- 2026-08-31: Dashboard rebuilt from single-screen MVP into five working sections (Overview, Contacts, Campaigns, Sending accounts, Events) with live counts, real nav, CSV import in-section, campaign create (name + first step) and draft approval, and provider list. Added tenant-scoped `GET /api/contacts` and `GET /api/campaigns`; sending-accounts and campaigns list responses wrapped as `{accounts}`/`{campaigns}`; cache-bust bumped to `v=20260831-1`. Verified in-browser: CSV import (3 contacts), campaign create/refresh/approve, empty states for accounts/events. `bun test` 32/32; screenshot-verified per section.

- 2026-08-31: Added enroll-into-campaign UI: each approved campaign gets an "Enroll contacts" action that enrolls all imported contacts via `POST /api/campaigns/:id/enroll`, shows the count in a notice, hides the button after success, and is idempotent on repeat (INSERT OR IGNORE). Verified in-browser (2 contacts enrolled; second call returns 0) and on the live production site after restart; commit `83aa463`.

- 2026-08-22: Fixed Google Contacts CSV imports by recognizing `E-mail 1 - Value` and equivalent numbered email columns after header normalization. The supplied export parses to 649 valid contacts; 13 contact tests pass.

- 2026-08-22: Contact CSV import now detects common CRM/export aliases for email and names, splits full-name columns, and preserves all other columns as custom fields. Dedicated parser tests pass.

- 2026-08-21: Published the dashboard as a private production Zo Site at `https://saas-mailer-jaknyfe.zo.computer`. The Site entrypoint sources `~/.zo_secrets`; the public browser verification correctly reached Zo's sign-in gate.

## Issue Log

- 2026-09-02: Provisioned the SaaS-Mailer OIDC client, applied production OIDC secrets, and changed account signup to link directly to the Noesis self-signup flow. Tests passed 32/32; live login screenshot verified.

- 2026-09-02: Gmail test send initially reached the API but failed because the MIME builder emitted literal `\\r\\n` text instead of CRLF line endings, causing Gmail to report `Recipient address required`. Fixed `src/server/sending/gmail-adapter.ts`; 32 tests pass. One live test to `don@noesisgroup.com` succeeded with Gmail message ID `1a060b7dc5de6bd6`; live dashboard screenshot verified.

- 2026-08-31: The production worker was in BACKOFF because the managed command called the missing `start:worker` package script, not because `CREDENTIAL_ENCRYPTION_KEY` was absent. Restored the script to run `src/worker/main.ts`; the worker started successfully with the configured 64-character key. `bun test` passes 32/32.

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
