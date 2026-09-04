# Zo Conductor skill

## Objective

Create a local, dependency-light orchestration skill for Zo Computer that turns complex work into bounded task graphs, routes by actual capability, isolates implementation changes, and requires evidence-based acceptance.

## Design

The skill is a control-layer document with a deterministic task-graph validator. It does not run a daemon, proxy, dashboard, model registry, or autonomous worker pool. The main Zo session remains responsible for scope, approvals, integration, and the final report.

## Zo constraints

The workflow reads workspace and project instructions, searches memory before resuming work, uses Graphify for repository retrieval, uses token-saver for verbose commands, requires screenshots for frontend or hosted changes, protects secrets, preserves unrelated dirty changes, and keeps deployment, messaging, spending, and destructive actions behind their normal approval boundaries.

## Repository basis

The design draws bounded principles from `wshobson/agents`, `alp82/forge`, `andyyaro/orkestra`, `realgarit/fable-baton`, and `codejunkie99/fable-orchestrator`. Their roles and adopted limits are documented in `Skills/zo-conductor/references/repository-bases.md`.

## Acceptance criteria

- The skill has valid Agent Skills frontmatter.
- The workflow defines T0–T3 routing, task ownership, verification, stop conditions, approvals, and completion reporting.
- The validator rejects malformed, cyclic, incomplete, or invalid-risk graphs.
- The validator accepts a valid dependency graph.
- Repository lineage and Zo-specific additions are documented.
- Tests run without third-party dependencies.
