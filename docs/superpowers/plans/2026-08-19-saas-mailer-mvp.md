# SaaS-Mailer MVP Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first working SaaS-Mailer vertical slice: organization → sending account → CSV contacts → campaign → approved send → event history.

**Architecture:** Create a standalone Zo Site with a React dashboard, TypeScript API, PostgreSQL persistence, and a managed worker. Keep provider delivery behind an adapter interface; the MVP uses a deterministic mock adapter while Gmail, Outlook, and SMTP adapters are added behind the same contract.

**Tech Stack:** Bun, TypeScript, React, PostgreSQL, Vitest, and the Zo Site runtime.

## Global Constraints

- Every tenant-owned record includes `organization_id`.
- Approval is required by default before sending.
- Provider credentials never reach the browser.
- Suppression checks happen immediately before every send.
- Duplicate sends are prevented with idempotency keys.
- Tracking pixels and click tracking are disabled by default.
- No CRM integrations, billing, autonomous agents, newsletter marketing, or self-operated SMTP infrastructure in this slice.

---

### Task 1: Scaffold the standalone site

**Files:**
- Create: `saas-mailer/package.json`
- Create: `saas-mailer/zosite.json`
- Create: `saas-mailer/src/server.ts`
- Create: `saas-mailer/src/client/main.tsx`
- Create: `saas-mailer/src/client/styles.css`
- Create: `saas-mailer/tests/health.test.ts`

**Interfaces:**
- Produces `GET /api/health` returning `{ "ok": true }`.
- Produces a dashboard shell at `/`.

- [ ] **Step 1: Create the site directory and minimal package metadata.**
- [ ] **Step 2: Add the health endpoint and dashboard shell.**
- [ ] **Step 3: Write the health test against the exported server handler.**
- [ ] **Step 4: Run `bun test tests/health.test.ts`; expect PASS.**
- [ ] **Step 5: Commit `feat: scaffold saas-mailer site`.**

### Task 2: Add database schema and tenant primitives

**Files:**
- Create: `saas-mailer/db/migrations/001_initial.sql`
- Create: `saas-mailer/src/server/db.ts`
- Create: `saas-mailer/src/server/tenancy.ts`
- Create: `saas-mailer/tests/tenancy.test.ts`

**Interfaces:**
- `getOrganizationId(request): string` rejects missing organization context.
- `assertOrganizationRecord(record, organizationId): void` rejects cross-tenant access.
- Tables include organizations, users, organization_members, sending_accounts, contacts, campaigns, campaign_steps, campaign_contacts, messages, events, suppression_list, and audit_log.

- [ ] **Step 1: Write tests proving matching organization IDs pass and mismatches fail.**
- [ ] **Step 2: Add the migration with foreign keys and organization indexes.**
- [ ] **Step 3: Implement tenancy helpers and parameterized query helpers.**
- [ ] **Step 4: Run the tenancy tests and migration against a disposable test database.**
- [ ] **Step 5: Commit `feat: add tenant-safe database foundation`.**

### Task 3: Implement contacts and CSV import

**Files:**
- Create: `saas-mailer/src/server/contacts/csv.ts`
- Create: `saas-mailer/src/server/contacts/service.ts`
- Create: `saas-mailer/src/server/routes/contacts.ts`
- Create: `saas-mailer/tests/contacts.test.ts`

**Interfaces:**
- `parseContactsCsv(csvText): ParsedContact[]` requires a normalized email and preserves custom columns.
- `importContacts(organizationId, contacts): ImportResult` deduplicates within the organization.
- `POST /api/contacts/import` returns inserted, skipped, and invalid counts.

- [ ] **Step 1: Write tests for valid rows, missing email, malformed email, duplicate email, and custom fields.**
- [ ] **Step 2: Implement CSV parsing and email normalization without adding a package.**
- [ ] **Step 3: Implement organization-scoped persistence and import results.**
- [ ] **Step 4: Run `bun test tests/contacts.test.ts`; expect PASS.**
- [ ] **Step 5: Commit `feat: import tenant contacts from csv`.**

### Task 4: Implement sending accounts and adapter contract

**Files:**
- Create: `saas-mailer/src/server/sending/types.ts`
- Create: `saas-mailer/src/server/sending/mock-adapter.ts`
- Create: `saas-mailer/src/server/sending/service.ts`
- Create: `saas-mailer/src/server/routes/sending-accounts.ts`
- Create: `saas-mailer/tests/sending.test.ts`

**Interfaces:**
- `SendingAdapter.send(input): Promise<SendResult>` returns provider ID and accepted timestamp.
- `MockSendingAdapter` records sent messages for tests and never sends externally.
- `connectSendingAccount` stores account metadata and encrypted credential placeholder server-side.

- [ ] **Step 1: Write tests for account creation, provider selection, and mock delivery.**
- [ ] **Step 2: Define the adapter interface and mock implementation.**
- [ ] **Step 3: Add organization-scoped account persistence with browser-safe response fields.**
- [ ] **Step 4: Run `bun test tests/sending.test.ts`; expect PASS.**
- [ ] **Step 5: Commit `feat: add sending account adapter boundary`.**

### Task 5: Implement campaigns, approval, suppression, and queue state

**Files:**
- Create: `saas-mailer/src/server/campaigns/service.ts`
- Create: `saas-mailer/src/server/campaigns/eligibility.ts`
- Create: `saas-mailer/src/server/routes/campaigns.ts`
- Create: `saas-mailer/tests/campaigns.test.ts`

**Interfaces:**
- `createCampaign(input): Campaign` starts in `draft`.
- `approveCampaign(campaignId, organizationId): Campaign` records approval audit data.
- `isEligibleToSend(contact, campaign, now): EligibilityResult` checks approval, suppression, reply/bounce state, schedule, and account limits.

- [ ] **Step 1: Write tests for draft rejection, approval success, suppression rejection, and account-limit rejection.**
- [ ] **Step 2: Implement campaign and enrollment persistence.**
- [ ] **Step 3: Implement the eligibility function with explicit rejection reasons.**
- [ ] **Step 4: Run `bun test tests/campaigns.test.ts`; expect PASS.**
- [ ] **Step 5: Commit `feat: add campaign approval and eligibility`.**

### Task 6: Implement worker send processing and event history

**Files:**
- Create: `saas-mailer/src/server/worker/queue.ts`
- Create: `saas-mailer/src/server/worker/process-send.ts`
- Create: `saas-mailer/src/server/events/service.ts`
- Create: `saas-mailer/src/server/routes/events.ts`
- Create: `saas-mailer/tests/worker.test.ts`

**Interfaces:**
- `processQueuedSend(job): Promise<SendAttempt>` performs eligibility, idempotency, adapter send, message persistence, and event creation.
- `recordEvent(input): Event` updates contact/campaign state for reply, bounce, unsubscribe, or failure.

- [ ] **Step 1: Write tests for successful send, duplicate job, suppressed contact, and permanent adapter failure.**
- [ ] **Step 2: Implement idempotency keys and send-attempt persistence.**
- [ ] **Step 3: Implement retryable versus permanent failure handling.**
- [ ] **Step 4: Implement event recording and automatic pause transitions.**
- [ ] **Step 5: Run `bun test tests/worker.test.ts`; expect PASS.**
- [ ] **Step 6: Commit `feat: process approved sends and record events`.**

### Task 7: Build the dashboard vertical slice

**Files:**
- Create: `saas-mailer/src/client/api.ts`
- Modify: `saas-mailer/src/client/main.tsx`
- Modify: `saas-mailer/src/client/styles.css`
- Create: `saas-mailer/tests/dashboard.test.tsx`

**Interfaces:**
- Dashboard views: organization header, account setup, CSV import, campaign creation, approval action, send status, and event history.
- Browser responses never include credential values.

- [ ] **Step 1: Write component tests for the import, approval, send-status, and event-history states.**
- [ ] **Step 2: Add API client methods for contacts, accounts, campaigns, and events.**
- [ ] **Step 3: Implement the minimum dashboard flow with explicit loading, empty, success, and error states.**
- [ ] **Step 4: Run `bun test tests/dashboard.test.tsx`; expect PASS.**
- [ ] **Step 5: Start the Zo Site preview and verify the rendered dashboard with a screenshot.**
- [ ] **Step 6: Commit `feat: add saas-mailer vertical-slice dashboard`.**

### Task 8: End-to-end isolation and delivery verification

**Files:**
- Create: `saas-mailer/tests/e2e/vertical-slice.test.ts`
- Create: `saas-mailer/tests/e2e/tenant-isolation.test.ts`
- Create: `saas-mailer/README.md`
- Create: `saas-mailer/AGENTS.md`

- [ ] **Step 1: Seed two organizations with separate accounts and contacts.**
- [ ] **Step 2: Execute both organizations through import, campaign creation, approval, send, and event history.**
- [ ] **Step 3: Assert organization A cannot read or mutate organization B data.**
- [ ] **Step 4: Run the complete test suite.**
- [ ] **Step 5: Capture a final dashboard screenshot showing the completed flow.**
- [ ] **Step 6: Commit `test: verify saas-mailer vertical slice and isolation`.**

## Self-review

- Spec coverage: architecture, tenancy, CSV import, accounts, campaigns, approval, suppression, queue processing, retries, idempotency, event history, dashboard states, and screenshot verification are represented above.
- Scope: the plan covers one independently testable vertical slice; Gmail, Outlook, SMTP, billing, CRM, and advanced AI remain later plans.
- Placeholders: no implementation step depends on an unspecified function or undefined external file.
- Consistency: all service interfaces use `organizationId`, the worker calls the adapter contract, and the dashboard consumes the route outputs without credentials.
