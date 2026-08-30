---
name: faceless-yt-content-engine
description: Build a 30-day publishing calendar for a faceless YouTube channel. Produces a strategic mix of evergreen, trending, searchable tutorials, curiosity-driven videos, and opinion/debate pieces, each with title, hook, primary keyword, viewer intent, difficulty, and content type, ordered for momentum.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# faceless-yt-content-engine

Use this skill to plan a 30-day publishing calendar for a faceless YouTube channel. Produces a calendar of ideas that build momentum on each other, not a flat list of standalone topics.

## Required input

- **Niche** — the channel's topic area (output of `Skills/faceless-yt-niche-brand/`).
- **Target viewer** — the audience profile from stage 1.
- **Pillars** — the 4 content pillars from `Skills/faceless-yt-niche-brand/`.
- **Posting frequency** — videos per week (default 2/week → 8 videos in 30 days).
- **Video formats in rotation** — from stage 1's format recommendation.
- **Constraints** — production capacity, batch-days, evergreen vs. trend ratio target.

## Content type taxonomy (one per idea)

| Type | Definition | Strength | Weakness |
| --- | --- | --- | --- |
| **Search** | Targets an explicit query the viewer types into YouTube. Slow, compounding. | Always-on demand; back catalog keeps earning. | Slow first-30-days growth. |
| **Browse** | Targets the Home / Suggested feed. High CTR, broad appeal. | Fast impressions. | Needs strong packaging. |
| **Suggested** | Built to appear next to one specific popular video. Borrows that video's audience. | High retention once it lands. | Audience mismatch risk. |
| **Trend** | React to a current event, release, or viral topic in the niche. | Spike in views, new subscribers. | Short shelf life; can date the channel. |

A 30-day calendar should weight roughly: **40% Search / 25% Browse / 20% Suggested / 15% Trend**, adjusted for the niche. New channels with low authority lean harder on Search; established channels can spend more on Trend.

## Difficulty mix (default)

- **60% Beginner-friendly** — entries the niche's noob would search for. Drive new viewer flow and broad comment participation.
- **40% Advanced** — depth that earns watch time, returning viewers, and authority. Use sparingly so the channel does not feel exclusionary.

## For every idea, produce

1. **Working title** — not the final; subject to A/B from `Skills/faceless-yt-discoverability/`.
2. **Opening hook** — the 3–5s line. Generate via `Skills/hook-generator/`, surface=video.
3. **Primary keyword / topic** — the explicit search term this video is built around.
4. **Viewer intent** — what the viewer expects to walk away with (1 sentence).
5. **Difficulty level** — Beginner or Advanced.
6. **Content type** — Search, Browse, Suggested, or Trend.
7. **Pillar** — which of the 4 pillars it serves (from stage 1).
8. **Pillar coverage check** — at the end, confirm all 4 pillars are represented proportionally; flag any pillar with 0 entries.
9. **Suggested-pair video** (for `Suggested` type) — the specific public video this one is built to appear next to.
10. **Trend trigger** (for `Trend` type) — the specific event/release this video must ship before.

## Publishing order — momentum logic

Do not arrange the calendar chronologically by idea quality. Arrange it so each video hands the audience to the next:

1. **Day 1–2 (Anchor video)** — the single best Search-targeted Beginner piece. Highest evergreen value, lowest production risk. This is the channel's first impression.
2. **Day 3–4 (Trust video)** — an Advanced Search piece that demonstrates the channel is not a beginner-only channel. Builds authority that the Anchor video's broad traffic can convert.
3. **Day 5–7 (Breadth video)** — a Browse or Suggested piece aimed at the second-largest adjacent audience in the niche. Diversifies the audience the algorithm is learning.
4. **Day 8–14 (Pillar coverage)** — fill in the 4 pillars, leaning Search + Browse. Add 1 Trend piece if a relevant event is in window.
5. **Day 15–21 (Suggested stacking)** — Suggested-type pieces built to appear next to the niche's top 5 public videos. This is where subscribers start coming from "watched next" panels.
6. **Day 22–30 (Trend + retention)** — 1–2 more Trend pieces if a real event is live; otherwise a retention-focused Advanced piece that rewards returning viewers (longer watch time, more comments).

If posting frequency is **1/week instead of 2/week**, halve the per-week count but keep the Anchor → Trust → Breadth sequence at the top of the calendar.

## Comment-bait — opinion/debate pieces

Reserve **3 of the 30** slots for opinion/debate-style videos whose explicit job is to drive comments. Recipe:

- Take a position the niche's mainstream view disagrees with, then back it with one specific, defensible piece of evidence.
- Title must take a side, not pose a question ("Why X is wrong about Y" works; "Is X right about Y?" does not).
- Pin a comment that disagrees with your own take and replies to it on launch day.
- Do not make these the anchor or trust videos; they spike comments but often tank watch time if the comments are from drive-by disagree-views.

## Quality rules

- The opening hook must be specific to the video, not a template the channel will repeat. Variation in hooks is what stops the channel from feeling formulaic by month 3.
- No two videos in the same 7-day window can target the same primary keyword — keyword cannibalization kills the older video.
- The Trend slots must be reserved for real, scheduled events. If no event is in window, replace with a Suggested or Search piece and note the swap.

## Output

A single markdown file with:

- 30 ideas in publish order (or as many as the posting frequency produces)
- Per-idea fields above
- Closing 4-pillar coverage table
- Trend-event watchlist (the specific events this calendar is built around, with their dates)

## Related skills

- `Skills/faceless-yt-niche-brand/` — produces the niche, audience, pillars, and formats this calendar consumes.
- `Skills/faceless-yt-discoverability/` — picks the final titles, thumbnails, and descriptions; consumes the calendar's titles + primary keywords.
- `Skills/faceless-yt-retention-script/` — consumes an individual idea from the calendar and produces a full time-coded script.
- `Skills/faceless-yt-monetization/` — receives the completed 30-day calendar plus the niche/audience; chooses which content types carry affiliate/SPS/digital-product placements.
