---
name: interrogate
description: "Adversarial multi-reviewer code review. Each reviewer is an independent Zo session that gets the same prompt and rubric and cannot see the other reviews. Use for 'interrogate this', 'adversarial review', 'multi-model review', 'challenge this', 'stress test this code', 'find blind spots', or 'tear this apart'."
compatibility: Created for Zo Computer. Requires the ZO_CLIENT_IDENTITY_TOKEN already present in the agent environment. Each reviewer is a billed Zo session.
metadata:
  author: jaknyfe.zo.computer
  license: MIT
  source: https://github.com/cursor/plugins/tree/main/pstack/skills/interrogate
  upstream-author: Lauren Tan
---

# Interrogate

Run several independent reviewers over the same change, then synthesize one verdict. The adversarial signal comes from the reviewers *not sharing context* — not from assigned personas. A reviewer that can see the parent's reasoning just agrees with it.

Each reviewer is a full independent Zo session via `/zo/ask`. It receives the intent, the code, the rubric, and the quality lens. It does not receive the conversation, the other reviews, or your conclusions.

**Distinguish this from `adversarial-code-review`,** which is already in the workspace. That skill is *lens* diversity: one prompt per angle (skeptic, architect, minimalist, security, verifier), dispatched to local `claude`/`codex` CLIs, with reviewers free to read the repo. This skill is *model* diversity: no assigned lenses, full rubric to each reviewer, and independence enforced by separate Zo sessions on different models. Reviewer prompts forbid delegating to another skill, so a reviewer will not silently switch methods. Use this one when you want genuinely different models, or when the `claude`/`codex` CLIs are not installed — as in this workspace, where they are not on PATH and the sibling skill's runner has no target that works.

**The deliverable is a verdict. Do not auto-apply anything.**

## Usage

Ask for it directly ("interrogate this change", "stress test this"), or run the fan-out directly:

```bash
# 1. build the manifest
cat > /tmp/interrogate.json <<'JSON'
{
  "intent": "One paragraph of what this change is supposed to accomplish.",
  "scope": "The diff or file contents, inline in this file.",
  "models": ["byok:2e03a024-1bd1-4819-b7de-06dbb577e664",
             "byok:ee9b6e08-3859-4d08-91ec-bfc683010ef4"]
}
JSON

# 2. fan out
bun run Skills/interrogate/scripts/review.ts /tmp/interrogate.json
```

The script prints one `## Reviewer X` section per reviewer. You then apply the lead judgment below to produce the verdict. Read Step 3 before you pick models — the diversity caveat decides whether the Agreement Map is evidence or just a consistency check.

**Child sessions inherit your active persona.** A persona with hard output-format rules (a mandatory date prefix, a fixed tone) shows up in the reviewer's response, usually as a preamble line. There is no API parameter to disable it — `persona_id`, empty and null, and an empty `instructions` field all leave the persona active. It is cosmetic: the findings still land under the `## Reviewer X` header. Strip the preamble when you read the results, and do not let a persona's opinions substitute for the rubric.

## Which one you want

`adversarial-code-review` already exists in this workspace and looks like this. It is not a duplicate — the two differ in what creates the adversarial signal:

| | `adversarial-code-review` | `interrogate` |
|---|---|---|
| Signal comes from | **assigned lenses** — skeptic, architect, minimalist, security, verifier | **model diversity** — same prompt, different models |
| Diversity axis | one context per lens, same model family | one context per model family |
| Reviewers | 3–5, chosen by change size | 1–3, explicit cost decision |
| Runs on | local `claude` / `codex` CLIs | `/zo/ask` child sessions, any configured model |

Upstream's own note is that personas are *not* the source of the signal: "the adversarial signal comes from model diversity, not assigned personas." So use `adversarial-code-review` when you want structured coverage of a known change shape, and this when you want genuinely different models arguing about the same thing. Running both on one diff is reasonable and cheap relative to the value.

A reviewer spawned by this skill is told not to use other review skills. That guard is deliberate: without it, a child session that finds `adversarial-code-review` on disk will run that instead, and one billed review silently becomes four.

## Step 1 — Scope## Step 1 — Scope

Decide what is under review, and say which you chose:

- The user named files or a diff → use that.
- On a feature branch → `git diff main...HEAD` (or the real base).
- The user referred to recent work → gather the relevant files.

Package the diff, plus only the surrounding context a reviewer needs to make sense of it. A reviewer that cannot read the call site cannot tell whether the null check matters.

## Step 2 — State the intent

One paragraph, before any reviewer runs. Derive it from the user's message, the commit messages, a PR description, and the code. If the intent is genuinely ambiguous, ask rather than guessing — every reviewer inherits this paragraph.

## Step 3 — Run the reviewers

Choose the models first. Two is the working default; three is the cap.

- **Same model twice is a consistency check, not independent corroboration.** Two runs of one model mostly measure run-to-run variance. Use different providers whenever real diversity is available, and the script prints a caveat when the configured models do not span distinct families.
- **Do not fan out casually.** Each reviewer is a full billed session with its own tool access. One is 1 session; three is 3.
- **One is allowed** and the script will say so, but then you have an adversarial review, not a multi-model one.

The script fills `references/reviewer-prompt.md` with the intent, the scope, the rubric from `references/rubric.md`, and the lens from `references/code-quality-review.md`. The same filled prompt goes to every reviewer.

## Step 4 — Synthesize

1. **Parse** all findings from all reviewers.
2. **Find consensus.** Anything raised independently by 2+ reviewers is the highest-signal material here.
3. **Weight lone findings.** Still worth reading; weight by severity and whether the reasoning is concrete.
4. **Deduplicate.** Different reviewers describe the same issue differently. Merge and record who raised it.
5. **Note disagreements.** One reviewer flagging something another explicitly clears is useful, not noise — it usually marks a spot where the change is genuinely ambiguous.

## Step 5 — Lead judgment

You are the lead reviewer: a pragmatic senior engineer, not a neutral aggregator. The reviewers saw a slice of the code and a one-paragraph intent. You have the conversation. Read `references/lead-judgment.md` for the full framework.

Buckets:

- **Act on** — real correctness, security, or maintainability problems given the actual goals. These would block a real PR.
- **Consider** — legitimate, but you are not sure it outweighs the cost of fixing right now.
- **Noted** — technically valid, not actionable, or premature at this stage.
- **Dismissed** — wrong, nitpicky, or missing context, with a one-line reason.

For each finding: which reviewers raised it, which bucket, one line of rationale.

## Output format

### Intent
> [the paragraph from Step 2]

### Reviewers
- Reviewer A: [model], N findings
- Reviewer B: [model], N findings

### Act On
[Each with description, who raised it, why it matters.]

### Consider
[Each with description, who raised it, the tradeoff.]

### Noted
[Short list.]

### Dismissed
[Each with a brief reason.]

### Agreement Map
[Where the reviewers agreed, where they diverged, and what the pattern actually tells you — including the model-diversity caveat if it applies.]

---

MIT licensed, ported from `cursor/plugins` by Lauren Tan. The rubric, quality lens, and judgment framework are carried over substantially intact; the Cursor `Task`/`subagent_type` fan-out and the hardcoded `claude-opus-5-5-max` / `gpt-5.6-sol-max` / `grok-4.7-xhigh-fast` model table are replaced by `/zo/ask` with caller-supplied models.
