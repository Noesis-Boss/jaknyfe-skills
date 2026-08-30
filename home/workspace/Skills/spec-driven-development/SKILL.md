---
name: spec-driven-development
description: Run a Spec-Driven Development (SDD) workflow on any new project or major feature. Produces a constitution, a spec, a technical plan, a task breakdown, and an implementation loop — each stage gated on the previous, each artifact living under `.specify/` so the work stays auditable. Use when the user asks for SDD, "spec it first," "constitution and plan," or wants the github/spec-kit pipeline (constitution → specify → plan → tasks → implement) without leaving the workspace. Stops if scope is fuzzy; pairs with `brainstorming` for unclear asks and with `zo-code-builder` for the build itself.
metadata:
  author: jaknyfe.zo.computer
---

# Spec-Driven Development

A five-stage pipeline that forces "what" before "how" before "code." Borrowed in spirit from [github/spec-kit](https://github.com/github/spec-kit); simplified to fit Zo workflows.

## When to use

- New project, new service, or major feature with non-obvious shape.
- User says "spec it first," "constitution," "SDD," or "plan-then-build."
- The work touches >1 subsystem or has unclear acceptance criteria.

## When NOT to use

- Single-file change, copy edit, or bug fix with a known root cause. Use `incremental-implementation` or just fix it.
- Scope is fuzzy and the user has not decided direction yet. Hand off to `brainstorming` first.

## The five stages

1. **Constitution** — the project's non-negotiables. Quality bar, security posture, scope boundaries, decision rules. One page, durable, edited rarely.
2. **Specify** — the *what* and *why*. User-facing behavior, acceptance criteria, out-of-scope list. No tech choices here.
3. **Plan** — the *how*. Tech stack, data model, API surface, file layout, dependencies, risks. References the spec by id.
4. **Tasks** — ordered, atomic, testable work items. Each task has: id, spec ref, estimated effort, blocking deps, acceptance check.
5. **Implement** — execute tasks in order, updating task state and surfacing blockers. Each task closes with proof (screenshot, curl, log, test).

The pipeline is **linear and gated**. Don't skip stages. The constitution can be edited later, but only with explicit reason logged in `.specify/memory/changes.md`.

## File layout

```
project-root/
├── .specify/
│   ├── constitution.md      # Stage 1
│   ├── spec.md              # Stage 2
│   ├── plan.md              # Stage 3
│   ├── tasks.md             # Stage 4
│   ├── memory/
│   │   ├── decisions.md     # Why we chose X over Y
│   │   └── changes.md       # Edits to constitution/spec
│   └── templates/           # Reusable templates
└── ...
```

Run `scripts/init.sh <project-root>` to scaffold the folder and copy templates.

## Workflow

1. Read this file and any existing project `AGENTS.md`.
2. If scope is unclear, invoke `brainstorming` and stop there. Return to this skill once the user picks a direction.
3. If scope is clear, ask the user one confirmation: "Spec first, or just dive in?" Default if no answer: produce the constitution only, then ask again.
4. Walk the stages in order. Each stage's output becomes the next stage's input. Don't write code until stage 4 (tasks) is approved.
5. After implementation, mark each task `[x]` with the proof artifact (commit hash, screenshot path, URL).
6. If a stage reveals the previous one was wrong, fix the previous stage first, log the change in `.specify/memory/changes.md`, and continue.

## Pairing with other skills

- **`brainstorming`** — use before stage 1 if the user can't articulate the goal in one sentence.
- **`zo-code-builder`** — hand off at stage 5 for the build loop itself.
- **`plan-code-changes`** — use as a lighter alternative for a single-file change.
- **`incremental-implementation`** — break a large stage-4 task list into shipping chunks.
- **`writing-plans`** — use *instead* of this skill if the user just wants a plan, not the full pipeline.

## Anti-patterns to flag

- Constitution is longer than one page. Cut.
- Spec contains tech choices. Move them to plan.
- Plan contains task ordering. Move to tasks.
- Tasks have no acceptance check. Reject.
- Implementation starts before tasks are approved. Stop and surface the gap.

## Templates

Templates live in `templates/`. The init script copies them into the target project. See:
- `templates/constitution.md`
- `templates/spec.md`
- `templates/plan.md`
- `templates/tasks.md`
- `templates/memory-decisions.md`
- `templates/memory-changes.md`

## Script

`scripts/init.sh <project-root>` — scaffolds `.specify/`, copies templates, prints a checklist of the five stages.

## Verification (Definition of Done)

- [ ] `.specify/constitution.md` exists and is < 1 page.
- [ ] `.specify/spec.md` lists acceptance criteria and out-of-scope.
- [ ] `.specify/plan.md` names the tech stack and references spec sections.
- [ ] `.specify/tasks.md` has every task with an acceptance check.
- [ ] All tasks closed with proof, or blockers explicitly logged in `memory/changes.md`.
- [ ] No code committed before stage 4 approval.
