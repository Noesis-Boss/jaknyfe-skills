---
name: principles
description: Engineering principles for writing, reviewing, and debugging software. Use when deciding how to structure a change, whether to build a tool instead of doing work by hand, whether a bug is really fixed, how to sequence a migration, or how to cut reader load. Covers 23 one-page principles: attack-the-premise, boundary-discipline, build-the-lever, encode-lessons-in-structure, exhaust-the-design-space, experience-first, fix-root-causes, foundational-thinking, guard-the-context-window, laziness-protocol, make-operations-idempotent, migrate-callers-then-delete-legacy-apis, minimize-reader-load, model-the-domain, never-block-on-the-human, outcome-oriented-execution, prove-it-works, redesign-from-first-principles, separate-before-serializing-shared-state, sequence-verifiable-units, subtract-before-you-add, test-behavior-not-implementation, type-system-discipline. Ported from the MIT-licensed pstack plugin for Cursor, (c) 2026 Lauren Tan.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  upstream: cursor/plugins pstack v0.15.5, MIT
---

# Principles

23 engineering principles, one page each. Upstream ships them as 23 separate
Cursor skills so the model auto-selects by trigger; this port bundles them behind one Zo skill with
a routing table, because Zo only reads the top-level `SKILL.md` frontmatter and a flat 23-skill
namespace would collide with existing workspace skills.

**How to use:** read the table, match the situation, read that one reference file. Do not read all
of them. If two match, read both — they are written to compose.

## Usage

```
Read: Skills/principles/SKILL.md                # routing table
Read: Skills/principles/references/<name>.md    # one principle, one page
```

## Routing table

| Principle | Apply when |
|---|---|
| [`attack-the-premise`](references/attack-the-premise.md) | Apply when two or more fixes that share one premise have failed the same gate. |
| [`boundary-discipline`](references/boundary-discipline.md) | Apply when wiring validation, error handling, or framework adapters. |
| [`build-the-lever`](references/build-the-lever.md) | Apply to any non-trivial work, not just bulk work: edits, migrations, analyses, checks. |
| [`encode-lessons-in-structure`](references/encode-lessons-in-structure.md) | Apply when you catch yourself writing the same instruction a second time, or notice a recurring correction. |
| [`exhaust-the-design-space`](references/exhaust-the-design-space.md) | Apply when facing a novel UI interaction or architectural decision with no precedent in the codebase. |
| [`experience-first`](references/experience-first.md) | Apply when product, UX, or feature-scope tradeoffs come up. |
| [`fix-root-causes`](references/fix-root-causes.md) | Apply when debugging. |
| [`foundational-thinking`](references/foundational-thinking.md) | Apply before writing logic: choosing core types and data structures, sequencing scaffold-vs-feature work, asking what concurrent actors share. |
| [`guard-the-context-window`](references/guard-the-context-window.md) | Apply when context is filling up: large outputs, long files, repeated reads, fan-out planning. |
| [`laziness-protocol`](references/laziness-protocol.md) | Apply when refactoring, evaluating diff size, or tempted to add abstractions, layers, or signal threading. |
| [`make-operations-idempotent`](references/make-operations-idempotent.md) | Apply when designing commands, lifecycle steps, or processing loops that run amid crashes, restarts, and retries. |
| [`migrate-callers-then-delete-legacy-apis`](references/migrate-callers-then-delete-legacy-apis.md) | Apply when introducing a new internal API while old callers still exist. |
| [`minimize-reader-load`](references/minimize-reader-load.md) | Apply when reviewing or shaping code that's hard to trace. |
| [`model-the-domain`](references/model-the-domain.md) | Apply when writing stateful logic, or when code branches a lot or repeats a shape assumption across files. |
| [`never-block-on-the-human`](references/never-block-on-the-human.md) | Apply when tempted to ask 'should I do X?' on reversible work. |
| [`outcome-oriented-execution`](references/outcome-oriented-execution.md) | Apply during planned rewrites and migrations with explicit phase boundaries. |
| [`prove-it-works`](references/prove-it-works.md) | Apply after completing a task, before declaring done. |
| [`redesign-from-first-principles`](references/redesign-from-first-principles.md) | Apply when integrating a new requirement into an existing design. |
| [`separate-before-serializing-shared-state`](references/separate-before-serializing-shared-state.md) | Apply when concurrent actors might write to the same file, branch, key, or state object. |
| [`sequence-verifiable-units`](references/sequence-verifiable-units.md) | Apply to multi-step work (sweeps, migrations, runs of similar edits) and to how you stack commits and PRs. |
| [`subtract-before-you-add`](references/subtract-before-you-add.md) | Apply when sequencing an addition, refactor, or rewrite. |
| [`test-behavior-not-implementation`](references/test-behavior-not-implementation.md) | Apply when you write, change, or keep a test. |
| [`type-system-discipline`](references/type-system-discipline.md) | Apply when designing types, reviewing a function signature, or writing code in any statically-typed language. |

## Compositions worth knowing

- **Debugging a failure that keeps coming back:** `fix-root-causes` → if a second fix on the same
  premise also fails, `attack-the-premise`.
- **Any non-trivial change:** `subtract-before-you-add` → `foundational-thinking` →
  `build-the-lever` → `sequence-verifiable-units` → `prove-it-works`.
- **Reviewing hard-to-trace code:** `minimize-reader-load` + `boundary-discipline`.
- **New work with no precedent:** `exhaust-the-design-space` → `experience-first`.
- **A recurring correction:** `encode-lessons-in-structure` (and consider a user rule instead of
  re-adding it to this file).

## Zo term mapping

Upstream is written for Cursor. The reasoning is platform-neutral; three words are not:

- **subagent** → a child invocation via `POST /zo/ask` (`Skills/` scripts that fan out), or a
  separate process. Keep the fan-out script outside the delegates' write scope.
- **PR** → a GitHub pull request; `gh` is available on this host.
- **model routing / `opus` / `grok` / `sol` lines** → not applicable. The upstream
  `pstack-models.mdc` rule has no Zo equivalent; choose models in [Settings](/?t=settings&s=ai&d=models).

## Scope

Ported verbatim except for two mechanical changes: sibling links were rewritten to point inside
`references/`, and the one dangling reference to a non-ported sibling skill (`show-me-your-work`,
used once in `prove-it-works`) was made plain prose. No principle text was rewritten.

## Attribution

Ported from the **pstack** plugin (`cursor/plugins`, v0.15.5) by Lauren Tan, MIT licensed. The
upstream license is included verbatim as `LICENSE`. MIT requires the notice to travel with the
work; do not strip it when copying these files elsewhere.
