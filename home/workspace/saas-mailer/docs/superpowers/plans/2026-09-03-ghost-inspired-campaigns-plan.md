# Ghost-Inspired Campaigns Implementation Plan

**Spec:** `docs/superpowers/specs/2026-09-03-ghost-inspired-campaigns-design.md`

## Phase 1: Data model and repositories

1. Add campaign type, newsletter fields, schedule state, and preference tables to SQLite and PostgreSQL migrations.
2. Extend campaign types and repository methods for create, update, list, approve, schedule, and recipient selection.
3. Add tenant-scoped preference and analytics repository operations.
4. Add migration, repository, tenant-isolation, and backward-compatibility tests.

## Phase 2: Newsletter and tracking routes

1. Add newsletter create/update/preview/schedule routes using existing authentication and approval boundaries.
2. Add preference-center read/update/unsubscribe routes with safe tokenized recipient access.
3. Add tracking routes for opens and clicks with tenant-scoped lookup and event recording.
4. Extend queue eligibility and message rendering for newsletter recipients without changing sequence behavior.
5. Add route and worker tests, including suppression and idempotency cases.

## Phase 3: Dashboard experience

1. Add Newsletter versus Sequence campaign selection.
2. Build the newsletter composer with subject, preview text, rich body input, template selection, audience selection, preview, approval, and scheduling.
3. Add subscriber preference management and analytics views.
4. Preserve the current sequence editor and actions.
5. Update styles only as needed for responsive layouts and accessible controls.

## Phase 4: Verification and release

1. Run the full test suite and migration checks.
2. Browser-test newsletter creation, preview, approval, scheduling, preferences, tracking, and analytics using mock delivery.
3. Browser-test an existing multi-step sequence for regression.
4. Capture screenshots of composer, preference center, analytics, and responsive dashboard states.
5. Update `AGENTS.md`, project visibility, and the Trello progress card after verified completion.

## Guardrails

- Do not add Ghost API integration.
- Do not replace queue or provider adapters.
- Do not send real email during tests.
- Do not weaken suppression or tenant isolation.
- Do not modify unrelated projects or repositories.
