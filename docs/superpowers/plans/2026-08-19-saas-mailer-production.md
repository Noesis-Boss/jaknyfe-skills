# SaaS-Mailer Production Readiness Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the tested SaaS-Mailer MVP into a deployable multi-tenant outbound-email SaaS with authenticated organizations, durable PostgreSQL persistence, real provider delivery, a complete dashboard, and production operations.

**Architecture:** Keep the current Bun/Hono API, React client, adapter boundary, and organization-scoped service layer. Replace provisional tenant headers and SQLite persistence behind stable interfaces, add provider-specific OAuth/SMTP adapters, and run queue processing as a managed process backed by PostgreSQL. Release in stages with a mock-provider environment, internal pilot, and controlled production rollout.

**Tech Stack:** Bun, TypeScript, Hono, React, PostgreSQL, managed Zo Site/service, provider APIs, encrypted secrets, and Bun tests.

## Global Constraints

- Every tenant-owned query must enforce authenticated organization membership server-side.
- Provider credentials never reach the browser and are encrypted at rest.
- Approval remains required by default; automatic sending is an explicit campaign setting.
- Suppression, reply, bounce, complaint, schedule, and account-limit checks run immediately before every send.
- Every send has an idempotency key and durable attempt/event history.
- No tracking pixels or click tracking unless explicitly enabled per campaign.
- The mock adapter remains available for tests and staging; no production test may send externally.
- No billing, CRM synchronization, newsletter marketing, or autonomous copy agents are included in this production-readiness scope.

---

### Task 1: Establish production contracts and environment boundaries

**Files:**
- Create: `saas-mailer/.env.example`
- Create: `saas-mailer/src/server/config.ts`
- Create: `saas-mailer/tests/config.test.ts`
- Modify: `saas-mailer/README.md`
- Modify: `saas-mailer/AGENTS.md`

**Interfaces:**
- Produces `loadConfig(): AppConfig` with required production variables validated at startup.
- Defines `APP_ENV`, `DATABASE_URL`, `SESSION_SECRET`, `CREDENTIAL_ENCRYPTION_KEY`, provider OAuth variables, and worker settings.
- Rejects production startup when secrets, database URL, or callback origins are missing.

- [ ] **Step 1: Write failing tests for missing and valid configuration.** Test that development permits the mock adapter, production rejects missing `DATABASE_URL` and `SESSION_SECRET`, and malformed encryption keys fail.
- [ ] **Step 2: Implement `loadConfig()` with typed environment parsing and no secret logging.** Use a 32-byte encryption key and explicit numeric parsing for worker intervals and send limits.
- [ ] **Step 3: Add `.env.example` containing names only, never secret values.** Document local mock mode separately from production mode.
- [ ] **Step 4: Run `bun test tests/config.test.ts` and `bun test`; expect all tests to pass.**
- [ ] **Step 5: Commit `chore: define saas-mailer production configuration`.**

### Task 2: Replace provisional tenant context with authentication and memberships

**Files:**
- Create: `saas-mailer/db/migrations/007_auth_sessions.sql`
- Create: `saas-mailer/src/server/auth/password.ts`
- Create: `saas-mailer/src/server/auth/session.ts`
- Create: `saas-mailer/src/server/auth/middleware.ts`
- Create: `saas-mailer/src/server/routes/auth.ts`
- Create: `saas-mailer/tests/auth.test.ts`
- Modify: `saas-mailer/src/server/tenancy.ts`
- Modify: `saas-mailer/src/server.ts`

**Interfaces:**
- Produces `createSession(userId, organizationId): Promise<Session>` and `requireTenant(request): AuthenticatedTenant`.
- `AuthenticatedTenant` contains `userId`, `organizationId`, and `role` loaded from the database, never from a request header.
- Auth routes support password login/session creation and logout; OAuth provider wiring is added only after this boundary is tested.

- [ ] **Step 1: Write failing tests for registration, login, logout, expired sessions, missing sessions, and cross-organization membership denial.** Include requests that provide a forged `x-organization-id` and assert it cannot change the authenticated tenant.
- [ ] **Step 2: Add session and password tables with hashed passwords, expiry, revocation, and indexes.** Store only password hashes and opaque session tokens.
- [ ] **Step 3: Implement constant-time session lookup and membership-aware `requireTenant()`.** Remove direct route dependence on `getOrganizationId()`.
- [ ] **Step 4: Convert contacts, accounts, campaigns, events, and future routes to the authenticated tenant.** Preserve browser-safe error responses.
- [ ] **Step 5: Run the auth and full test suites, then capture a browser screenshot of login and authenticated dashboard states.**
- [ ] **Step 6: Commit `feat: add authenticated organization sessions`.**

### Task 3: Migrate persistence from SQLite to PostgreSQL

**Files:**
- Create: `saas-mailer/db/migrations/postgres/001_initial.sql`
- Create: `saas-mailer/src/server/postgres.ts`
- Create: `saas-mailer/src/server/repositories/`
- Create: `saas-mailer/tests/postgres-repositories.test.ts`
- Modify: `saas-mailer/src/server/db.ts`
- Modify: `saas-mailer/src/server/contacts/service.ts`
- Modify: `saas-mailer/src/server/campaigns/service.ts`
- Modify: `saas-mailer/src/server/events/service.ts`
- Modify: `saas-mailer/src/server/sending/service.ts`

**Interfaces:**
- Repositories expose organization-scoped methods for contacts, accounts, campaigns, messages, events, suppressions, and audit records.
- `openDatabase()` becomes a PostgreSQL pool factory in hosted mode; SQLite remains an explicit test adapter until parity tests pass.
- Transactions, unique constraints, composite tenant foreign keys, and row locks must preserve current isolation behavior.

- [ ] **Step 1: Write repository contract tests against both SQLite and a disposable PostgreSQL database.** Cover inserts, reads, updates, duplicate idempotency keys, and cross-tenant failures.
- [ ] **Step 2: Translate all current migrations to PostgreSQL types, constraints, indexes, and concurrent-safe queue fields.** Include a version table and rollback-safe startup migration behavior.
- [ ] **Step 3: Implement repositories and keep service-layer signatures stable.** Services must receive a repository context rather than issuing SQLite-specific SQL.
- [ ] **Step 4: Run parity tests and the full suite against PostgreSQL.** Require zero SQLite-only code paths in production configuration.
- [ ] **Step 5: Document backup, restore, connection-pool, and migration commands in `README.md`.**
- [ ] **Step 6: Commit `feat: add postgres persistence layer`.**

### Task 4: Implement real sending-account providers

**Files:**
- Create: `saas-mailer/src/server/sending/gmail-adapter.ts`
- Create: `saas-mailer/src/server/sending/microsoft-adapter.ts`
- Create: `saas-mailer/src/server/sending/smtp-adapter.ts`
- Create: `saas-mailer/src/server/sending/oauth.ts`
- Create: `saas-mailer/src/server/routes/provider-callbacks.ts`
- Create: `saas-mailer/tests/providers/`
- Modify: `saas-mailer/src/server/sending/types.ts`
- Modify: `saas-mailer/src/server/sending/service.ts`

**Interfaces:**
- Every provider implements `send(input): Promise<SendResult>` and classifies errors as retryable, authentication, quota, or permanent.
- OAuth tokens are encrypted, refreshable, revocable, and never returned by account routes.
- SMTP credentials use the existing AES-256-GCM credential envelope and are tested with a local SMTP fixture.

- [ ] **Step 1: Write adapter contract tests for accepted sends, provider IDs, retryable errors, auth errors, quota errors, and permanent failures.** Use mocked HTTP clients and a local SMTP fixture only.
- [ ] **Step 2: Implement Gmail and Microsoft OAuth start/callback/refresh flows.** Bind callback state to the authenticated organization and reject replayed or mismatched state.
- [ ] **Step 3: Implement Gmail, Microsoft, and SMTP adapters behind the existing adapter registry.** Normalize provider responses into `SendResult` and typed errors.
- [ ] **Step 4: Add account health checks, revoke controls, and pause/unpause routes.** Record every provider error in audit history without exposing tokens.
- [ ] **Step 5: Run provider tests with network calls disabled, then run the full suite.**
- [ ] **Step 6: Commit `feat: add production sending providers`.**

### Task 5: Build the durable worker and queue scheduler

**Files:**
- Create: `saas-mailer/src/worker/main.ts`
- Create: `saas-mailer/src/worker/lease.ts`
- Create: `saas-mailer/src/worker/scheduler.ts`
- Create: `saas-mailer/src/worker/backoff.ts`
- Create: `saas-mailer/tests/worker/queue-recovery.test.ts`
- Modify: `saas-mailer/src/server/worker/process-send.ts`
- Modify: `saas-mailer/src/server/worker/queue.ts`
- Modify: `saas-mailer/db/migrations/postgres/001_initial.sql`

**Interfaces:**
- `claimQueuedSends(workerId, now, batchSize): Promise<QueuedSendJob[]>` claims jobs with leases and prevents concurrent workers from duplicating sends.
- `runWorker(signal): Promise<void>` polls, processes, retries, and releases leases.
- Retry schedule is bounded exponential backoff with a maximum attempt count; permanent failures stop retrying.

- [ ] **Step 1: Write failing tests for leasing, concurrent claims, crash recovery, retry timing, maximum attempts, and graceful shutdown.**
- [ ] **Step 2: Add durable queue, lease, next-attempt, and attempt-history fields.** Enforce idempotency with a database constraint.
- [ ] **Step 3: Implement atomic claim/update transactions and reuse `processQueuedSend()` for delivery.**
- [ ] **Step 4: Implement the managed worker entrypoint with structured logs, health heartbeat, and graceful shutdown.**
- [ ] **Step 5: Run worker tests under simulated process crashes and provider failures.**
- [ ] **Step 6: Commit `feat: add durable outbound queue worker`.**

### Task 6: Complete the dashboard workflow

**Files:**
- Create: `saas-mailer/src/client/api.ts`
- Create: `saas-mailer/src/client/components/AccountSetup.tsx`
- Create: `saas-mailer/src/client/components/ContactImport.tsx`
- Create: `saas-mailer/src/client/components/CampaignBuilder.tsx`
- Create: `saas-mailer/src/client/components/EventHistory.tsx`
- Create: `saas-mailer/tests/dashboard.test.tsx`
- Modify: `saas-mailer/src/client/main.tsx`
- Modify: `saas-mailer/src/client/styles.css`

**Interfaces:**
- Dashboard supports account connection, CSV upload, campaign steps, contact enrollment, approval, send status, suppression, and event history.
- `src/client/api.ts` sends authenticated requests and converts browser-safe API failures into visible error states.
- Credentials are never represented in client state or rendered HTML.

- [ ] **Step 1: Write component tests for loading, empty, success, error, approval-required, paused-account, and completed-send states.**
- [ ] **Step 2: Implement typed API methods for accounts, contacts, campaigns, approvals, enrollments, sends, and events.**
- [ ] **Step 3: Replace the demo import action with actual file upload and campaign creation flow.**
- [ ] **Step 4: Add account health, queue status, suppression controls, and event filtering.**
- [ ] **Step 5: Run component tests and verify desktop/mobile screenshots with the authenticated browser.**
- [ ] **Step 6: Commit `feat: complete saas-mailer dashboard workflow`.**

### Task 7: Add production security, compliance, and abuse controls

**Files:**
- Create: `saas-mailer/src/server/security/rate-limit.ts`
- Create: `saas-mailer/src/server/security/csrf.ts`
- Create: `saas-mailer/src/server/security/retention.ts`
- Create: `saas-mailer/tests/security/`
- Modify: `saas-mailer/src/server/routes/`
- Modify: `saas-mailer/README.md`

**Interfaces:**
- Login, provider callbacks, import, campaign activation, and send endpoints have rate limits and CSRF protection where applicable.
- Unsubscribe, bounce, complaint, and manual suppression are enforced across all campaigns.
- Audit and message retention rules are configurable and documented.

- [ ] **Step 1: Write security tests for rate limits, CSRF, authorization, suppression precedence, oversized imports, and unsafe template input.**
- [ ] **Step 2: Implement request limits, CSRF tokens, origin checks, payload limits, and safe template rendering.**
- [ ] **Step 3: Add unsubscribe and complaint ingestion paths that immediately pause future contact sends.**
- [ ] **Step 4: Add retention and deletion jobs that preserve required audit records while removing expired message content.**
- [ ] **Step 5: Run dependency, secret, static, and security tests; document compliance responsibilities and acceptable-use limits.**
- [ ] **Step 6: Commit `feat: harden saas-mailer for production abuse cases`.**

### Task 8: Deploy staging, observe, back up, and release gradually

**Files:**
- Create: `saas-mailer/ops/healthcheck.ts`
- Create: `saas-mailer/ops/backup.sh`
- Create: `saas-mailer/ops/restore-drill.sh`
- Create: `saas-mailer/tests/e2e/staging-readiness.test.ts`
- Modify: `saas-mailer/zosite.json`
- Modify: `saas-mailer/README.md`
- Modify: `saas-mailer/AGENTS.md`

**Interfaces:**
- Health endpoint reports API, database, worker heartbeat, encryption configuration, and provider connectivity without exposing secrets.
- Backups are encrypted, restorable, and tested on a schedule.
- Staging uses mock delivery by default; production sending requires an explicit environment flag and verified provider accounts.

- [ ] **Step 1: Write staging-readiness tests for migrations, health, worker heartbeat, backup/restore, and mock-only delivery.**
- [ ] **Step 2: Register the private staging Site and managed worker service.** Configure secrets through Zo Advanced settings, not repository files.
- [ ] **Step 3: Deploy, run migrations, seed a non-production organization, and execute the full end-to-end workflow.**
- [ ] **Step 4: Add structured logs, metrics, alerts for queue age, provider errors, paused accounts, failed jobs, and database health.**
- [ ] **Step 5: Perform a restore drill and a controlled internal pilot with real provider accounts and low daily limits.**
- [ ] **Step 6: Release to production using a canary organization, then expand only after 24 hours of clean queue and provider metrics.**
- [ ] **Step 7: Commit `ops: add staging and production release controls`.**

## Release gates

- Gate 1: Tasks 1–3 pass with authenticated tenant tests and PostgreSQL parity.
- Gate 2: Tasks 4–5 pass with provider mocks, durable retry recovery, and no duplicate sends.
- Gate 3: Task 6 passes desktop/mobile screenshot verification for the complete user workflow.
- Gate 4: Task 7 passes security and suppression tests with no credentials in browser responses or logs.
- Gate 5: Task 8 passes staging restore, health, monitoring, and canary-send checks.

## Self-review

- MVP gaps covered: authentication, PostgreSQL, real providers, durable worker, complete dashboard, and production operations/security.
- Explicitly deferred: billing, CRM integrations, newsletter marketing, autonomous agents, and self-operated SMTP infrastructure.
- No task depends on the provisional `x-organization-id` after Task 2.
- Every task has files, interfaces, tests, acceptance criteria, and a commit boundary.
