---
name: zoastra-model-router
description: Delegate a materially complex, read-only consultation from ZoAstra to GPT-6.1 Sol or GPT-6 Astra through Zo's per-request model_name override. Routine work stays on ZoAstra's GPT-6 Luna default.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# ZoAstra Model Router

Use this skill only when a different model is likely to improve a non-routine analysis. The current ZoAstra turn remains on GPT-6 Luna; this creates one separate Zo child session. Child output is advisory, and the parent remains responsible for implementation, external actions, and verification.

## Route choice

- Keep routine, bounded, and low-risk work in the current Luna turn. Do not create a child session just to change models.
- Use `sol` for substantial technical reasoning, complex debugging, or architecture within one project.
- Use `astra` only for exceptionally difficult, ambiguous, or broad cross-system analysis.
- Use the existing `interrogate` skill for an explicitly requested adversarial or multi-reviewer review.
- Make at most one routed call per task. Do not retry automatically: a timed-out request may still have completed and incurred usage.

## Safety boundary

The child is asked to provide read-only advice, but it may inherit broad tool access from the active persona. Use this skill only for consultation; do not delegate edits, publishing, messages, purchases, or other side effects. The parent must inspect and verify any recommendation before acting. Do not include passwords, tokens, API keys, or other secrets in the manifest. Child sessions create additional Zo model usage; do not assume a specific credit cost.

## Run

Prepare one self-contained JSON manifest with `route`, `objective`, and optional `context`, then pipe it to the script. The script checks the live model catalog before submitting the request.

```sh
cat <<'JSON' | bun run /home/workspace/Skills/zoastra-model-router/scripts/route.ts -
{
  "route": "sol",
  "objective": "Analyze the bounded technical question and recommend a safe approach.",
  "context": "Relevant code, facts, constraints, and verification criteria."
}
JSON
```

Use `"route": "astra"` only for the exceptional cases above. If the selected model is unavailable or the call fails, continue in the parent Luna session and report that no alternate-model result was obtained. Never claim that the parent conversation itself switched models.

## Validation

- `bun run /home/workspace/Skills/zoastra-model-router/scripts/route.ts --help`
- Pipe a sample manifest to the same command with `--dry-run -` to verify the selected route without starting a model call.
