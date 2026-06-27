---
name: ifixai
description: "Run iFixAi — an open-source diagnostic for AI misalignment. Runs up to 32 inspections against any AI agent across five categories (sycophancy, prompt injection, fabrication, governance, reliability) and produces a scored fixture-driven report. Use when the user wants to test/evaluate an AI agent, run alignment diagnostics, benchmark model behavior, compare two scorecards, or validate a custom fixture. Supports providers: openai, anthropic, gemini, azure, bedrock, huggingface, openrouter, mock. Commands: run, init, list, validate, compare."
compatibility: "Created for Zo Computer"
metadata:
  author: jaknyfe.zo.computer
---

# iFixAi — AI Misalignment Diagnostic

iFixAi runs up to 32 inspections against any AI agent and reports where behavior diverges from common alignment expectations. Five categories: sycophancy, prompt injection, fabrication, governance, reliability ([GitHub](https://github.com/ifixai-ai/iFixAi)).

## Prerequisites

```bash
cd /home/workspace/iFixAi
pip install -e ".[openai,anthropic,gemini,openrouter]"
```

Repo lives at `/home/workspace/iFixAi/`. Re-install after pulling updates.

## Commands

All from repo root:

```bash
cd /home/workspace/iFixAi && ifixai <command>
```

### `ifixai run` — Execute inspections

```bash
ifixai run \
  --provider <provider> \
  --mode standard \
  --api-key <KEY> \
  [--model <model-id>] \
  [--fixture <name-or-path>] \
  [--output ./ifixai-results/] \
  [--format json|markdown|both] \
  [--eval-mode self|deterministic|single|full] \
  [--judge-provider <provider>] \
  [--strategic] \
  [--test B01] [--test B02] \
  [--concurrency 5] \
  [--min-score 0.85] \
  [--dry-run]
```

**Common patterns:**

| Goal | Command |
|---|---|
| Smoke test | `ifixai run --provider mock --mode standard --eval-mode self --api-key x` |
| Real model | `ifixai run --provider openrouter --mode standard -k $OPENROUTER_API_KEY --eval-mode self --model anthropic/claude-haiku-4.5` |
| Strategic only (top 8) | add `--strategic` |
| Full reference-grade | `--mode full --judge-provider anthropic --judge-api-key $ANTHROPIC_API_KEY` |
| Custom fixture | `--fixture /path/to/my-fixture.yaml` |

**Providers:** mock, openai, anthropic, gemini, azure, bedrock, huggingface, openrouter, http

**Modes:** standard (default CI-friendly) | full (reference-grade, needs hand-built fixture + multi-judge)

### `ifixai init` — Detect available keys and suggest first run

```bash
ifixai init
ifixai init --non-interactive
```

### `ifixai list` — List tests or fixtures

```bash
ifixai list tests              # all 32 inspection IDs
ifixai list tests --verbose    # with descriptions
ifixai list fixtures           # available domain fixtures
```

### `ifixai validate` — Validate fixtures

```bash
ifixai validate                          # validate test layout
ifixai validate /path/to/fixture.yaml    # custom fixture
```

### `ifixai compare` — Compare two scorecards

```bash
ifixai compare baseline-results.json enhanced-results.json
```

## Reports

Results save to `./ifixai-results/` (override `--output`). JSON has per-test scores, category scores, overall score, grade. Markdown has a human-readable summary.

Exit code 2 if overall score < `--min-score` threshold.

## Environment Variables

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | Provider credential |
| `ANTHROPIC_API_KEY` | Provider credential |
| `GEMINI_API_KEY` | Provider credential |
| `OPENROUTER_API_KEY` | Provider credential |
| `IFIXAI_CONCURRENCY` | Default concurrency (1–20) |
| `IFIXAI_SUT_TEMPERATURE` | SUT sampling temperature (default 0.0) |
