---
name: pr-summarizer
description: Generate a structured PR description from current branch changes. Reads git history and diff output, then produces a clean PR ready to paste into GitHub. Use when asked to "summarize this PR", "generate PR description", "write a pull request", or after completing a feature branch.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# PR Summarizer

Generate a structured pull request description from the current branch's changes.

## Workflow

1. Run `git log main..HEAD --oneline` to get all commits on the branch.
2. Run `git diff main...HEAD --stat` for a changed-files summary.
3. Read the key changed files to understand full context of the changes.
4. Generate the PR description in this exact format:

```
## What
[One paragraph describing what this PR does]

## Why
[One paragraph explaining why this change is needed]

## Changes
[Bullet list of key changes grouped by area]

## Testing
[How this was tested or how to test it]
```

## Rules
- Output only the formatted PR description, ready to paste.
- Group changes logically by feature area or concern.
- If no `main` branch exists, use `master` or detect the default branch.
- Keep the description concise — target 200-400 words total.
