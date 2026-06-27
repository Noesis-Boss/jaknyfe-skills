---
name: autoresearch
description: Run Karpathy's autoresearch — an autonomous agent that modifies a single-GPU nanoGPT training setup (prepare.py/train.py/program.md), trains for a fixed 5-minute budget per experiment, and keeps or discards changes based on val_bpb (lower = better). Use when the user wants to spin up overnight autonomous ML research on a single NVIDIA GPU, iterate on training code autonomously, or run the karpathy/autoresearch workflow.
metadata:
  author: jaknyfe.zo.computer
---

# autoresearch

Wraps [karpathy/autoresearch](https://github.com/karpathy/autoresearch) as a Zo skill. One idea: give an agent a real-but-small LLM training setup and let it experiment overnight. It edits `train.py`, trains 5 minutes, checks `val_bpb`, keeps or discards, repeats.

## Files

- `prepare.py` — fixed constants, data prep (downloads data, trains BPE), dataloader + eval utilities. **Do not modify.**
- `train.py` — model, optimizer (Muon + AdamW), training loop. **Agent modifies this.**
- `program.md` — agent instructions. **Human edits this** to steer the research org.
- `pyproject.toml` — uv-managed deps (PyTorch + small extras).
- `README.md` — upstream docs.

## Requirements

- Single NVIDIA GPU (tested H100).
- Python 3.10+.
- [`uv`](https://docs.astral.sh/uv/) package manager.

## Quick start (manual single run)

```bash
cd /home/workspace/Skills/autoresearch
curl -LsSf https://astral.sh/uv/install.sh | sh   # one-time
uv sync
uv run prepare.py                                   # one-time, ~2 min
uv run train.py                                     # one ~5 min experiment
```

`val_bpb` is the metric. **Lower = better.** Vocab-size-independent, so architecture changes are fairly compared.

## Autonomous mode

Point Claude/Codex/anything at this directory and prompt:

```
Hi have a look at program.md and let's kick off a new experiment! let's do the setup first.
```

`program.md` is the lightweight "skill" the agent reads. Expect ~12 experiments/hour, ~100 overnight.

## Design constraints baked in

- **Single file to modify.** Agent only touches `train.py`.
- **Fixed 5-min wall-clock budget per run.** Comparable across model sizes/batch sizes.
- **Self-contained.** PyTorch + a few small deps. No distributed training.

## Small-platform tuning (Macbooks, smaller GPUs)

From upstream README — tune these in order:

1. Swap to a low-entropy dataset like `karpathy/tinystories-gpt4-clean`.
2. Drop `vocab_size` (8192 → 4096 → 2048 → 1024 → 256 byte-level).
3. In `prepare.py`: lower `MAX_SEQ_LEN` (e.g. 256); raise `DEVICE_BATCH_SIZE` to compensate.
4. In `prepare.py`: lower `EVAL_TOKENS`.
5. In `train.py`: primary complexity knob is `DEPTH` (default 8 → try 4).
6. Use `WINDOW_PATTERN = "L"` (the `"SSSL"` banded pattern is slow on small GPUs).
7. Drop `TOTAL_BATCH_SIZE` (e.g. `2**14`).

## Editing workflow

When iterating as the human:
- Edit `program.md` to steer strategy ("focus on optimizer", "try smaller models first").
- Never edit `prepare.py`.
- `train.py` is the agent's playground — review diffs after each experiment cycle.

## Source

Upstream: https://github.com/karpathy/autoresearch (Karpathy, March 2026).
Files vendored into `Skills/autoresearch/` for self-contained runs.