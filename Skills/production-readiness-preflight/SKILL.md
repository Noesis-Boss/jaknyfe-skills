---
name: production-readiness-preflight
description: Run a fail-closed, evidence-backed production-readiness review of a software repository and the exact release candidate. Use when asked whether an app or codebase is ready to ship, deploy, launch, or go to production; when asked for a preflight, launch gate, or production security/readiness audit. Reports GO, HOLD, or NO-GO; does not certify security or change code by default.
metadata:
  author: jaknyfe.zo.computer
---

# Production Readiness Pre-Flight

Assess the exact source revision and deployment artifact under review. Return an evidence-backed release decision, not a score or certification. Treat the user's project instructions and current request as authoritative.

## Safety and review boundaries

- Start read-only. Do not edit code, configuration, tests, dependencies, migrations, or project documentation; install/update tools; deploy; contact production systems; or write a report into the repository unless the user explicitly authorizes that action.
- Before running a command, inspect what it does and whether it can write data, call external services, incur cost, or target production. Run only safe existing local tests and scanners by default. Never run destructive or billable tests against production.
- Never print, copy into a report, or send secret values. For secret scans, use redacted output. Report the path and type of exposure, then recommend revocation/rotation; do not attempt rotation.
- Do not treat an AI review, a clean scanner result, a successful build, or a passing happy-path test as proof of overall readiness. Verify material findings against source, configuration, tests, and tool output.
- Use **NOT VERIFIED** when evidence is missing or a check cannot be established. Unknown is not PASS. Use **N/A** only with a short reason.
- Do not silently invent environment details, workloads, applicable controls, or risk acceptance. Ask one focused question only when missing information materially changes scope or the release decision.
- Keep findings and fixes separate. Present the audit first. Make only specifically approved changes, then rerun relevant checks.

## Workflow

1. **Resolve scope.** Identify the repository, requested scope (one gate or full preflight), target environment, release commit, and intended artifact. If the target is unclear and multiple repositories or candidates are plausible, ask which one. Read the applicable `AGENTS.md`, `README.md`, release/deployment documentation, manifests, and tests before drawing conclusions. Read `DESIGN.md` when reviewing frontend behavior or design constraints.
2. **Freeze the candidate.** Inspect branch, commit, working-tree state, and release diff. Record uncommitted changes; do not imply they are included in a commit or artifact. Determine whether the build artifact is traceable to the reviewed source. For stateful changes, establish backup/recovery and rollback ownership from evidence.
3. **Map actual system surfaces.** Trace entry points, data flows, trust boundaries, integrations, and paid operations. Mark only applicable checks; explain every N/A.
4. **Review the gates below.** Run one gate at a time when the user requests focused passes. For a full pass, review all applicable gates and gather evidence from code plus safe, available tests/scanners. Do not infer a pass from missing evidence.
5. **Verify findings.** For each material finding, identify the concrete failure or abuse path and exact file/line, configuration, test, or scanner evidence. Separate confirmed defects from hypotheses. Treat scanner output as a lead to triage, not a verdict.
6. **Issue the decision.** Use the output contract. A one-gate review is scoped and cannot produce an overall GO for the release.

## Release gates

For each gate record **PASS**, **FAIL**, **N/A**, or **NOT VERIFIED**, with evidence and a brief rationale.

### 0. Candidate, recovery, and ownership

- Identify source commit, branch, release diff, build/artifact identity, target environment, reviewer, expected workload, data sensitivity, dependencies, and rollback owner/procedure.
- Confirm no unreviewed changes are silently included. For stateful changes, verify an appropriate backup/recovery path and a usable rollback plan.
- **Hold** if the deployed artifact cannot be tied to reviewed source, or required recovery/rollback is unknown.

### 1. Attack and data surface

- Inventory routes, APIs, webhooks, CLI entry points, scheduled jobs, background workers, admin actions, databases, integrations, sensitive data, and paid operations.
- Trace user-controlled input to storage, shell/process calls, file paths, HTML, and external services. Check for forgotten, debug-only, or test endpoints reachable in production.
- Evidence: entry-point inventory and concrete data-flow references.

### 2. Secrets and production configuration

- Check the working tree, Git history, credential/environment files, ignore rules, and built client assets for exposed keys, tokens, passwords, connection strings, or private configuration. Use a real secret scanner such as Gitleaks when available; redact output.
- Confirm required production settings are documented and supplied through the deployment's secret/config mechanism. Client-delivered configuration must not contain server-only secrets.
- If a credential was exposed, its removal from current source is insufficient: mark FAIL until revocation/rotation is confirmed.

### 3. Input validation and injection

- Trace forms, path/query parameters, headers, uploads, and webhook payloads from trust boundary to use.
- Check type, size, format, and allowed values; parameterized database operations; safe shell/process use; path traversal protections; output encoding; and safe upload handling where applicable.
- Use stack-appropriate tests or static analysis (for example, Semgrep) if already available. Require evidence tied to a concrete input path.

### 4. Authentication and object-level authorization

- Separately verify authentication and authorization for every relevant read/update/delete action.
- Check record, tenant, and action ownership; IDOR through changed IDs; server-side role checks; privilege escalation; and unauthenticated access.
- **No-go** for verified cross-user/cross-tenant data access or unauthorized privileged actions.

### 5. Failure behavior and resilience

- Check external-call timeouts and deliberate retries; ensure retries cannot duplicate non-idempotent actions.
- Check database/service failures, null/empty/malformed values, partial writes, and payment/write outcomes. User responses must not reveal stack traces, secrets, or internal topology.
- Verify important failure paths with safe tests or controlled checks; do not claim live behavior from source inspection alone.

### 6. Dependencies and supply chain

- Compare declared dependencies with actual use. Check unexpected or misspelled packages, dependency sources, lockfiles, reproducible builds, and abandoned or vulnerable components.
- Run the ecosystem's existing vulnerability scanner when available. Record dated output and disposition for material findings. Do not install, upgrade, or remove dependencies during the audit.

### 7. Critical user-flow tests

- Identify the most consequential flows for this product. For each, assess success, invalid input, and unauthorized access cases where applicable.
- Run safe existing unit, integration, and end-to-end tests relevant to the release. Report failures as defects; do not change app behavior merely to make a generated test pass.
- **Hold** if a critical flow fails or a material security case lacks credible verification.

### 8. Logging and security signals

- Check whether errors have useful safe context (service/route, request ID, timestamp, and appropriate user/tenant identifier); whether logs exclude passwords, tokens, full payment data, and unnecessary personal data; and whether security events are recorded consistently.
- Confirm operators can access the logs needed to respond. Inspect representative success, failure, and denied-access events when safely available.

### 9. Performance at expected workload

- Check for N+1 queries, unbounded collections, missing indexes on actual query paths, oversized assets, repeated per-request work, and resource-heavy operations.
- Verify pagination and limits. Use the workload supplied by the project/user; never substitute an arbitrary user count or unsupported performance estimate.
- Evidence may be profiling/load results or a code-based finding clearly labeled as such.

### 10. Spend and abuse controls

- Inventory endpoints that invoke paid APIs, messaging, uploads, or heavy computation.
- Check authentication, per-user/per-IP rate limits, input-size and concurrency limits, quotas, and provider-side alerts/caps where applicable.
- **Hold** if an unauthenticated or unbounded request can cause material spend and no effective limit is evidenced.

### 11. Production configuration and deployability

- Check that debug/development modes, sample credentials, verbose errors, and dev-only tools are disabled; CORS is limited to required origins; HTTPS and appropriate security headers are configured; and auth cookies use appropriate `Secure`, `HttpOnly`, and `SameSite` settings.
- Apply HSTS only after HTTPS and domain/subdomain behavior are confirmed. Verify versioned/repeatable migrations and compatibility, health checks, and a staging/smoke-test procedure.
- Confirm production URLs, flags, and variable names are documented without placing secret values in source.

### 12. Independent final review

- Identify likely first-month outage/security risks and gaps that would block another operator from deploying safely.
- Confirm deployment instructions are reproducible and critical/high findings are fixed and re-tested or release is held. Residual-risk acceptance needs an explicit owner and approval; an AI review finding nothing is not evidence of safety.
- If the user specifically asks for a multi-model adversarial review, use the existing `adversarial-code-review` skill. If they specifically ask what a code change could break, use `blast-radius`. Do not duplicate those specialized workflows by default.

## Decision rules

- **GO:** Every required/applicable gate is PASS with adequate evidence; no release-blocking finding remains; the artifact, recovery, and post-deploy verification path are identified.
- **HOLD:** Required evidence is missing, a check is NOT VERIFIED, or a fix/retest/approval is pending.
- **NO-GO:** A confirmed release-blocking security, correctness, data-recovery, or operational failure remains.
- A gate-specific review reports only its scoped result; it must not imply full production readiness.
- Do not use a numeric readiness score. State uncertainty and accepted residual risk explicitly.

## Output contract

Return a concise Markdown report in this order:

1. **Decision:** GO / HOLD / NO-GO, with one-sentence reason.
2. **Scope:** repository, commit/artifact, environment, working-tree caveat, and review gates.
3. **Release record:** workload/data/dependencies/owner, using “Not provided” where evidence is absent.
4. **Findings:** severity, gate, exact evidence/location, concrete impact, status, and smallest recommended next step. Put blockers first. Do not reproduce secret values.
5. **Gate matrix:** status and evidence reference for each reviewed gate; explain N/A and NOT VERIFIED.
6. **Verification run:** safe commands/tests/scanners actually run and their observed results. Distinguish not run from failed.
7. **Release action:** specific condition to move from HOLD/NO-GO to GO, or post-deploy checks to perform. Do not claim to have deployed or verified live behavior unless it was actually requested and done.

## Focused review prompt

When asked to prepare a prompt for a coding agent, use this pattern and substitute the actual gate, commit, and environment:

> Review **Gate [number and name] only** in this repository against release commit **[commit]** and target environment **[environment]**. Inspect relevant source, configuration, and tests. Do not modify files, install/update dependencies, or contact production services. For each finding, give severity, exact file/line or configuration, the concrete failure/abuse path, and evidence that confirms it. Separate verified findings from hypotheses. Mark unsupported checks **NOT VERIFIED**, not PASS. End with the smallest safe test or scan needed to validate the result.
