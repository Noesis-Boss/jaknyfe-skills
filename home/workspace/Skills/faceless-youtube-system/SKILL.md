---
name: faceless-youtube-system
description: Orchestrate the end-to-end build of a faceless YouTube channel — niche + brand, 30-day content plan, discoverability packaging, retention script system, and 6-month monetization. Use when: starting a faceless channel from zero, restarting after a slump, or onboarding a new niche. Pairs with hook-generator, video-script, keyword-cluster, brand-builder, growth-plan, and faceless-explainer.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Faceless YouTube System

Five-stage build for a faceless YouTube channel. Run the stages in order, or jump in at any stage if the upstream artifact already exists.

## The five stages

| # | Stage | Skill | Output |
|---|---|---|---|
| 1 | Niche & brand | `faceless-yt-niche-brand` | `channel-brief.md` — angles, names, viewer profile, pillars, tool stack |
| 2 | 30-day content engine | `faceless-yt-content-engine` | `content-30d.md` — 30 ideas in publish order with hooks, keywords, intent |
| 3 | Discoverability engine | `faceless-yt-discoverability` | `packaging.md` — title formulas, thumbnail text, description template, metadata |
| 4 | Retention script system | `faceless-yt-retention-script` | `script-framework.md` — time-coded beats, hook + transition formulas |
| 5 | Monetization roadmap | `faceless-yt-monetization` | `monetization-6mo.md` — staged plan, milestones, sponsorship template |

## Inputs

- **Niche** (required) — topic area the channel will cover
- **Starting point** (optional) — zero subscribers / stalled channel / pivot
- **Upload capacity** (optional) — 1, 2, or 3 videos/week
- **Tool stack** (optional) — if you already pay for tools, list them so the brief doesn't duplicate

## Process

1. Confirm the niche and starting point with the user.
2. Run stage 1 first. Capture the brief.
3. Each subsequent stage reads the previous stage's artifact. Don't skip the dependency.
4. After stage 4, run a sample script through the existing `Skills/faceless-explainer/` to confirm the framework produces renderable output.
5. Stage 5 is the last step. It does not depend on the script framework, only on the channel brief + content plan + packaging.

## Unique aspects to preserve across all stages

- **Faceless-first** — every recommendation assumes no on-camera host. Visuals are AI footage, stock, motion graphics, screen recordings, or text-on-screen.
- **Useful-not-stuffed** — discoverability prioritizes viewer benefit over keyword density. No "keyword stuffing."
- **Realistic over promising** — monetization targets sustainable growth at 6 months, not viral lottery wins.
- **Momentum-ordered** — content engine plans publish in the order that builds audience between videos (search → suggested → trend).
- **Beginner-friendly default** — 60% of ideas beginner, 40% advanced, unless overridden.
- **Anti-clickbait** — every hook and title must be deliverable by the video's content.

## Output

A folder per channel build (e.g. `Channels/[niche-slug]/`) containing the five stage artifacts plus a `channel-brief.md` summary linking them.

## Anti-patterns

- Do not start a channel with the "high-CPM niche" mindset. Niche first, monetization at month 4+.
- Do not run all five stages in one LLM call. The stages exist so the user can course-correct between them.
- Do not recommend tools you cannot name. If a tool is unfamiliar, say so and suggest a known alternative.
