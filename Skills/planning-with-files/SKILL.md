---
name: planning-with-files
description: Maintain durable task plans, findings, and progress files for multi-step work that may span compaction, interruptions, or multiple sessions.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Planning with files

Use this skill for work with multiple phases, research, implementation, verification, or a likely context interruption.

## Files

Create a `.task/` directory in the active project and maintain:

- `plan.md` — goal, success criteria, phases, decisions, and blockers.
- `findings.md` — evidence, commands, references, and unresolved questions.
- `progress.md` — dated actions, results, failures, and the next action.

## Workflow

1. Inspect the project's `README.md`, `AGENTS.md`, and `DESIGN.md` when present.
2. Run `scripts/init-plan.sh "<goal>" <project-root>` before substantive work.
3. Read `.task/plan.md` and `.task/progress.md` before each major phase.
4. Record evidence in `.task/findings.md` as it is discovered. Record failures and fixes in `.task/progress.md`.
5. Keep one active plan per project. Update it instead of creating competing plans.
6. Mark a phase complete only after its stated verification passes.
7. Before handoff, run `scripts/verify-plan.sh <project-root>` and record the result.

## Zo conventions

Keep durable project guidance in the project `AGENTS.md`; keep task-specific execution state in `.task/`. Use workspace memory for cross-session facts. Never copy secrets into planning files.
