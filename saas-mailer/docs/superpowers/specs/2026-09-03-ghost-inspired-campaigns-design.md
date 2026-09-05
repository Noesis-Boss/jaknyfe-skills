# Ghost-Inspired Campaigns Design

**Date:** 2026-09-03
**Project:** SaaS-Mailer
**Status:** Approved design; implementation pending

## Objective

Add Ghost's strongest user-facing ideas to SaaS-Mailer while preserving its multi-tenant outbound delivery architecture. The release serves newsletter publishing and sales/outreach campaigns equally.

## Chosen approach

Use one unified campaign system. Add newsletter behavior to the existing campaign model and reuse tenant scoping, approval, queue processing, suppression, sending accounts, and event history. Do not create a separate newsletter subsystem or require Ghost integration.

## Campaign model

- Add `campaign_type`: `newsletter` or `sequence`.
- Preserve existing multi-step sequence behavior.
- Newsletters use one rich content step with subject, preview text, body, template, and scheduled send time.
- All campaign and recipient operations remain organization-scoped.
- Subscriber preferences supplement, but never weaken, unsubscribe and suppression rules.

## User experience

- “Create campaign” offers Newsletter or Sequence.
- Newsletter composer supports subject, preview text, rich body editing, reusable templates, audience selection, preview/send-test, approval, and scheduling.
- A subscriber preferences center supports topic selection, pause, and unsubscribe.
- Analytics shows delivery, opens, clicks, unsubscribes, and campaign performance.
- Existing sequence screens and actions remain available and behaviorally unchanged.

## Data flow and safeguards

1. Composer saves drafts through tenant-scoped campaign routes.
2. Approval is required before scheduling or sending.
3. Scheduled newsletters enter the existing durable queue.
4. Each recipient produces delivery, open, click, and unsubscribe events.
5. Tracking links and pixels are tenant-scoped.
6. Preference changes suppress future sends immediately.
7. Mock delivery remains the development and test default.

## Testing and definition of done

- Cover SQLite and PostgreSQL migrations and repositories.
- Test newsletter creation, editing, preview, approval, scheduling, queue delivery, suppression, preferences, and analytics events.
- Confirm sequence campaigns retain their current behavior.
- Browser-test composer, preferences, analytics, and responsive layouts.
- Screenshot-verify the finished dashboard.

Done means a tenant can create, preview, approve, schedule, and deliver a newsletter through the existing queue, manage subscriber preferences, and view analytics without changing sequence campaign behavior.

## Explicit exclusions

- No Ghost API integration.
- No replacement of the existing queue or provider adapters.
- No paid memberships or subscription billing in this release.
- No unrelated refactoring.
