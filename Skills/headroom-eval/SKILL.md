---
name: headroom-eval
description: >-
  A/B harness for evaluating headroom-ai token compression against the current
  zdsentry trending→X pipeline. Runs identical inputs through both paths, scores
  the outputs, and writes a Markdown report. Use when deciding whether to add
  headroom to the trending/X automation, or when re-running the comparison after
  headroom updates.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  category: eval
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Headroom A/B harness

A small, self-contained Python harness that runs the same (slot, headline, context-chunks) inputs through two arms and reports the deltas.

- **control** — the current pipeline, with no compression. This is your baseline.
- **headroom** — the same prompt, with context chunks first run through the local headroom proxy at `http://localhost:8787`. If the proxy is down or the input is already short, it passes through.

## What it measures

Per arm, per sample:

- input chars + tiktoken tokens (the bytes the LLM would see)
- output tweet chars
- heuristic quality score (see `score.py` — opinion present, AI-vocab check, hashtag balance, em-dash count, length window)
- LLM cost estimate (best-effort, based on the model you pass in)

Per arm, aggregated:

- mean quality score
- mean input tokens and % reduction vs control
- estimated $ per run
- tweet validity (under 280, contains take, no AI tells)

## When to use

- Once a month: re-run with fresh trending headlines to check that headroom still helps and still preserves quality.
- After any headroom release: bump the pin, re-run, compare to the previous report.
- Before turning it on in prod: run with `--arms control headroom --n 3` to get statistical signal.

## How to use

1. **Bootstrap once per sandbox** (installs deps, optionally starts the headroom proxy):

   ```bash
   bash /home/workspace/Skills/headroom-eval/scripts/bootstrap.sh
   ```

   The bootstrap is idempotent. If the `headroom` CLI isn't installed, the harness still runs in control-only mode.

2. **Run the harness**:

   ```bash
   python3 /home/workspace/Skills/headroom-eval/scripts/run_ab.py \
     --input /home/workspace/Skills/headroom-eval/sample-input/sample.json \
     --arms control headroom \
     --n 1 \
     --model gpt-4o-mini
   ```

   Flags:

   - `--input` — path to a JSON array of `{slot, headline, context_chunks}`
   - `--arms` — any subset of `control` and `headroom`
   - `--n` — repeat each arm N times (default 1) for noise estimation
   - `--model` — model name for both cost estimation and (if you wire it in) generation
   - `--max-cost` — bail out before spend exceeds this many USD across all arms (default 0.50)
   - `--out` — output report path (default `reports/report-YYYYMMDD-HHMMSS.md`)

3. **Read the report**. The harness writes a Markdown report next to the script. Skim the per-sample table and the aggregated table. Then decide:
   - If headroom reduces tokens by ≥30% with quality delta ≤ 5 points → adopt.
   - If headroom reduces tokens <20% on this corpus → it's not worth the proxy hop.
   - If quality drops >10 points on any sample → the compression is losing semantic content. Read the diff.

## What it does NOT do

- It does not call any LLM by default — it only measures input compression. To get a quality delta, wire in a generation function in `run_ab.py::call_llm` (or use the `--llm` flag I left as a TODO).
- It does not post to X. It does not touch the trending pipeline.
- It does not judge whether the *take* is good — that's your call, on the 3 headlines you actually publish.

## Files

- `scripts/run_ab.py` — main harness
- `scripts/score.py` — heuristic quality scorer
- `scripts/bootstrap.sh` — venv + proxy bootstrap
- `scripts/requirements.txt` — just `tiktoken`
- `sample-input/sample.json` — three real recent zdsentry slot examples
- `reports/` — auto-created, holds dated Markdown reports
