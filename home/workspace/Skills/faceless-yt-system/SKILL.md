---
name: faceless-yt-system
description: Orchestrator for the 6-stage faceless YouTube system. Run niche-brand → content-engine → discoverability → retention-script → monetization → video-production in order, writing numbered files into a per-channel project directory.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# faceless-yt-system

Orchestrate the 6 stages of the faceless-youtube-system. Each stage is its own skill; this one owns the order, the output directory, and the handoff contract between stages.

## The 6 stages

| # | Stage | Skill | Output file |
| --- | --- | --- | --- |
| 1 | Niche & brand | `Skills/faceless-yt-niche-brand/` | `01-niche-and-brand.md` |
| 2 | 30-day content engine | `Skills/faceless-yt-content-engine/` | `02-30-day-calendar.md` |
| 3 | Discoverability engine | `Skills/faceless-yt-discoverability/` | `03-discoverability-pack.md` |
| 4 | Retention script system | `Skills/faceless-yt-retention-script/` | `04-script-<slug>.md` |
| 5 | Monetization roadmap | `Skills/faceless-yt-monetization/` | `05-monetization-roadmap.md` |
| 6 | Video production | `Skills/faceless-yt-video-production/` | `06-production-<slug>.md` |

## Required input

- **Niche** — the topic area, or a `[your niche]` placeholder.
- **Output directory** — where to create the per-channel project. Default: `~/Projects/youtube/<channel-slug>/`.

## How to run

```bash
# 1. Create the per-channel directory.
mkdir -p ~/Projects/youtube/<channel-slug>
cd ~/Projects/youtube/<channel-slug>

# 2. Run the 6 stages in order. Each stage reads the previous stage's output.
# Stage 1 — niche, audience, pillars, tool stack.
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 1 "<NICHE>"

# Stage 2 — 30-day calendar (consumes stage 1).
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 2

# Stage 3 — discoverability pack (consumes stages 1 + 2).
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 3

# Stage 4 — retention script for one video (consumes stages 1, 2, 3).
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 4 "<VIDEO-SLUG>"

# Stage 5 — monetization roadmap (consumes stages 1, 2, 3).
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 5

# Stage 6 — production plan for one video (consumes stage 4's script + Section 5 beats).
bun run /home/workspace/Skills/faceless-yt-system/scripts/run.ts stage 6 "<VIDEO-SLUG>"
```

The runner checks that the required previous-stage output exists before invoking a stage, so you cannot run stage 4 before stage 1. Stage 6 is per-video and parallelizable with other stage-6 runs, like stage 4.

## Handoff contract (what each stage must consume + produce)

| Stage | Consumes | Produces |
| --- | --- | --- |
| 1 | Niche (input) | `01-niche-and-brand.md` |
| 2 | `01-niche-and-brand.md` | `02-30-day-calendar.md` |
| 3 | `01-`, `02-` | `03-discoverability-pack.md` |
| 4 | `01-`, `02-`, `03-` + 1 video slug | `04-script-<slug>.md` |
| 5 | `01-`, `02-`, `03-` | `05-monetization-roadmap.md` |
| 6 | `04-script-<slug>.md` + stage 1 brand | `06-production-<slug>.md` |

## Caching + idempotency

- Each stage writes to a fixed filename. Re-running a stage overwrites the file.
- Stage 4 takes a video slug so multiple scripts can coexist in the same channel directory.

## When to deviate from the order

Almost never. The handoff contract is the point — each stage's output is the next stage's input. Reordering produces calendars that ignore the brand, scripts that ignore the packaging, or production plans that ignore the script's beats.

The exceptions: **stage 4 (script) and stage 6 (production) can run in parallel for multiple videos** once stages 1, 2, and 3 are complete. Each is independent per video; stage 6 for one slug requires that slug's stage-4 script.

## Related skills

- `Skills/faceless-yt-niche-brand/` — stage 1
- `Skills/faceless-yt-content-engine/` — stage 2
- `Skills/faceless-yt-discoverability/` — stage 3
- `Skills/faceless-yt-retention-script/` — stage 4
- `Skills/faceless-yt-monetization/` — stage 5
- `Skills/faceless-yt-video-production/` — stage 6; turns a stage-4 script into a shot-by-shot production plan (visual beats, stock terms, transitions, voice direction, music bed)
- `Skills/hook-generator/` — generates the opening lines stage 4 places in the script
- `Skills/faceless-explainer/` — render layer; takes a stage-6 production plan and produces video frames
- `Skills/youtube-channel-framework/` — empty stub; this system is the implementation that fills it
