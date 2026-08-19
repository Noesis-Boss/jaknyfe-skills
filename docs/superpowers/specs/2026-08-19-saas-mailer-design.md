# SaaS-Mailer MVP Design

Date: 2026-08-19
Status: Design approved; awaiting written-spec review

## Brief

Build a public multi-tenant SaaS for personalized outreach and campaign sending. Zo owns the dashboard, database, queue, scheduling, analytics, and AI drafting. Gmail, Microsoft Outlook, and generic SMTP provide delivery. CSV import is the MVP acquisition path; CRM integrations and billing are later work.

The MVP must support multiple organizations, team members, multiple sending accounts, approval-first sending, optional campaign automation, suppression handling, event history, and strict tenant isolation.

## Architecture

- Standalone Zo Site named `saas-mailer`.
- React dashboard and TypeScript API.
- PostgreSQL for durable application state.
- Managed worker for scheduling, throttling, retries, pauses, and queue processing.
- Email/password plus Google/Microsoft sign-in.
- Gmail API, Microsoft Graph, and encrypted SMTP credentials behind a shared sending-adapter interface.
- Provider credentials remain server-side and are encrypted at rest.

Every tenant-owned record includes `organization_id`. The worker is the only component responsible for executing queued sends.

## MVP workflow

1. Create a workspace and invite team members.
2. Connect Gmail, Outlook, or SMTP sending accounts.
3. Import contacts by CSV and map standard or custom fields.
4. Create a campaign with steps, delays, sending windows, limits, and account assignment.
5. Draft messages manually or with AI assistance.
6. Require approval by default; allow explicit campaign automation.
7. Queue and send through assigned accounts.
8. Track delivery, replies, bounces, unsubscribes, failures, opens, and clicks when tracking is enabled.
9. Pause future steps after reply, bounce, unsubscribe, or manual suppression.

## Data model

Core entities:

- `organizations`, `users`, `organization_members`
- `sending_accounts`
- `contacts`, `lists`
- `campaigns`, `campaign_steps`, `campaign_contacts`
- `messages`, `events`
- `suppression_list`, `audit_log`

Contacts are deduplicated per organization using normalized email addresses. Campaign enrollment stores per-contact state. Messages retain rendered content and provider IDs. Events provide the operational history used by reporting and follow-up behavior.

## Security and sending safety

- Enforce tenant boundaries on every request and database query.
- Apply owner, admin, and member permissions.
- Never expose provider credentials to the browser.
- Require approval before sending unless campaign automation is explicitly enabled.
- Enforce per-account limits, sending windows, throttling, and pause controls.
- Apply organization-wide suppression for unsubscribes, bounces, complaints, and manual do-not-contact records.
- Record login, account changes, campaign activation, approvals, sends, and suppression changes in an immutable audit log.
- Disable tracking pixels and click tracking unless the customer enables them.

## API and sending flow

The MVP API covers authentication, organization membership, sending-account connections, CSV import, lists, campaigns, steps, enrollments, drafts, approvals, queue state, events, replies, suppression, and audit logs.

The first vertical slice is:

`organization → sending account → CSV contacts → campaign → approved send → event history`

For each queued message, the worker verifies suppression state, approval state, sending window, account limits, and contact state. The selected adapter sends the message, stores the provider ID, and records the result. Provider events update message and contact state.

## Error handling

- Retry temporary provider errors with exponential backoff.
- Pause accounts after repeated authentication or quota failures.
- Mark permanent failures without retrying.
- Use idempotency keys to prevent duplicate sends.
- Store every send attempt and provider response securely.
- Return safe generic errors to the browser and retain diagnostic details in protected logs.

## Testing and definition of done

Automated tests cover tenant isolation, roles, CSV validation, deduplication, suppression, approval, limits, sending windows, retries, account pauses, state transitions, and duplicate-send prevention.

MVP is complete when two test organizations can independently execute the vertical slice through the dashboard, all automated tests pass, provider behavior is mocked reliably, and no organization can access another organization's contacts, campaigns, credentials, or message history.

## Explicitly out of scope

- CRM integrations
- Billing and subscriptions
- Advanced autonomous AI agents
- Newsletter-style mass marketing
- Direct SMTP infrastructure operated by SaaS-Mailer itself
