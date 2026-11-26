---
name: adversarial-code-review
description: "Adversarial code review with multiple independent reviewers (Skeptic, Architect, Minimalist, Security, Verifier) built from one canonical prompt template. Use when reviewing a diff, branch, PR, or a specific file before merge, when asked to 'review this code adversarially', 'stress-test this change', or when Claude has been too agreeable about its own code quality."
compatibility: "Created for Zo Computer. Reviewer spawning requires the claude and/or codex CLIs on PATH; prompt rendering works without them."
metadata:
  author: jaknyfe.zo.computer
---

# Adversarial Code Review

Multi-reviewer code review. Each reviewer gets the *same* rubric and the *same*
code, but a different lens, so they fail independently and disagree in useful
ways. The point is to break the self-review monoculture: an author reviewing
their own code shares its assumptions.

## Process

1. **Establish intent.** Write the author's stated goal in one or two sentences,
   from their message or the commit/PR description. If there is no stated intent,
   derive it from the diff and label it as your inference.

2. **Collect the code.** A diff (`--diff`) or a file (`--code-file`). For a diff
   review, reviewers also read the surrounding code — callers, callees, types —
   via their own tools. Pass a `--paths` scope when the change is one area of a
   large repo.

3. **Pick lenses by change size.** Do not force every lens onto every change.

   | Change size | Signal | Lenses |
   |---|---|---|
   | Small | < ~100 changed lines, single concern | `skeptic` |
   | Medium | touches a shared module or contract | `skeptic,architect` |
   | Large | new subsystem, refactor, infra/permissions/data | `skeptic,architect,minimalist` |
   | Any change touching auth, secrets, input handling, or network | add `security` |
   | Any change that should be provable | add `verifier` |

4. **Render the prompts** and hand each to a separate reviewer context.

5. **Synthesize.** Merge findings by location, not by reviewer. When reviewers
   disagree, say so and show both. Deduplicate: three reviewers reporting the
   same thing is one finding with three confirmations, not three findings.
   Promote severity when independent reviewers converge on the same location.

## Rendering prompts

```bash
# Diff against a base, default three lenses
bun scripts/render_prompts.ts --intent "Add paper-only validation gate to the trading bot" --diff --base origin/master

# A single file, security + correctness
bun scripts/render_prompts.ts --intent "Auth middleware for the admin API" \
  --code-file src/api/admin.ts --lenses security,skeptic

# Scoped to specific paths, machine-readable output
bun scripts/render_prompts.ts --intent "..." --diff --base main --paths src/auth,src/db --json
```

Each render creates a **fresh** directory `<out>/acr-review-XXXXXX/` and prints
the path of every prompt it wrote. One render is one immutable job, so a prompt
set can never be a mix of two changes. Pass the printed path to the runner.
Exit `0` on success, `1` on bad arguments or missing input, `2` if the template
is malformed (a template bug, not a review result).

## Spawning reviewers

Rendered prompts are plain text and can be handed to any reviewer context. To
get genuine independence, spawn a fresh CLI reviewer per lens rather than
reviewing the lens yourself in the same context. The bundled runner does this
and writes a per-lens tally:

```bash
./scripts/run_review.sh --out /tmp/acr-review-eIVUrI --repo . --target codex --timeout 600
```

Writes `<lens>.review.md` per lens plus `summary.md` with critical/warning/nit
counts into a **fresh** results directory (printed as `Results:`), so a second
run never overwrites a first. Exit `0` only if every lens produced a parseable
review; `1` on bad args, a missing prompts dir, a missing CLI, a lens timing
out, or a review whose output has no finding headers.

`--repo` is the repository reviewers read, and it is **not** the prompts
directory: a rendered diff names files by relative path, so a reviewer started
in the prompts directory cannot resolve the callers and callees the rubric
requires it to inspect. Both backends run from it.

To drive the CLIs yourself:

```bash
D=/tmp/acr-review-eIVUrI
claude -p "$(cat "$D/skeptic.prompt.md")" > "$D/skeptic.out" 2>/dev/null &
codex exec -C "$PWD" "$(cat "$D/architect.prompt.md")" > "$D/architect.out" 2>/dev/null &
wait
```

Reviewers on different model families catch different things. `--target codex`
is the default because the reviewer is meant to oppose the author. When
delegating to a CLI, do not fabricate a verdict — read the actual review file.

## The lenses

- **Skeptic** — correctness and root cause. Breaks the change; traces call
  chains instead of flagging that something "could be nil."
- **Architect** — layer, contract, and complexity budget. Bolted-on logic,
  duplicated helpers, legacy dual-paths, dead code.
- **Minimalist** — code judo. Names the behavior-preserving restructuring that
  deletes branches or layers. No named deletion, no finding.
- **Security** — only security, only with a traced input path to a sink.
- **Verifier** — the test surface. Whether the work is provable from the code,
  and whether any check reads a proxy instead of the real value.

## Output contract

Findings are `critical` / `warning` / `nit`, each with location, the concrete
problem, the evidence, and an optional concrete alternative. A finding that
restates what the code does is not a finding. Zero findings is a valid result —
say so and stop. Never praise the code.

Full template with the complete rubric and code-quality lens:
`references/reviewer-prompt-template.md`.

## Notes

- The template asserts the intent is correct and challenges only the execution.
  Keep it that way unless the user explicitly asks for intent critique.
- Do not run every lens on a trivial change. A one-line typo fix needs the
  Skeptic, not five reviewers.
- Reviewers are read-only reviewers. Fixes are a separate, explicit step.
