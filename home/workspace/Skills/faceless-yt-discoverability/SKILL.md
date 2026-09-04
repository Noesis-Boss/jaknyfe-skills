---
name: faceless-yt-discoverability
description: Stage 3 of the faceless-youtube-system. For a niche and audience, produce 10 high-potential topic/keyword opportunities, 5 reusable title formulas, per-topic 3 title variations + 3 thumbnail-text ideas + curiosity gap + main promise, a reusable YouTube description template with natural keyword placement and metadata strategy, and an actionable plan to improve CTR, watch time, returning viewers, and subscribers.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# faceless-yt-discoverability

Use this skill as **stage 3** of the faceless-youtube-system. Stages: niche-brand → content-engine → discoverability → retention-script → monetization.

This is the **packaging** stage. The video is built; this stage decides how it presents to the algorithm and the viewer.

## Required input

- **Niche + audience** — from `Skills/faceless-yt-niche-brand/`.
- **Content calendar** — from `Skills/faceless-yt-content-engine/` (titles + primary keywords).
- **Existing top videos in the niche** — optional; if present, the skill uses them as Suggested-pair targets.

## Output (single markdown document)

### Section A — 10 high-potential topic/keyword opportunities

For each:

- **Primary keyword** (the explicit search term the video is built around).
- **Secondary keywords** (3–5 related terms that go in the description and tags).
- **Search volume band** (Low / Medium / High — do not invent numbers; use bands, not fake absolutes).
- **Competition band** (Low / Medium / High).
- **Why it's high-potential** (the specific viewer problem it solves, not the keyword metrics).
- **Pillar** — which of the 4 pillars from stage 1 it serves.

Order by potential, not by volume. A Low-volume Low-competition keyword that perfectly matches a pillar can outrank a High-volume High-competition keyword that does not.

### Section B — 5 reusable title formulas

Each formula must be reusable across many videos. Format: structure + 2 worked examples + 1 anti-example (the thing this formula is **not** for).

The five formulas must cover different psychological triggers — not five variations of the same trick. Recommended coverage:

1. **Specificity** (concrete number + concrete outcome).
2. **Curiosity gap** (open a loop the title does not close).
3. **Contrarian / pattern interrupt** (claim the opposite of mainstream advice).
4. **How-to with stakes** (action + cost of inaction).
5. **List with a twist** (N items where one is different).

### Section C — Per-topic packaging (for each of the 10 topics)

For each topic from Section A:

- **3 title variations** (use 3 of the 5 formulas from Section B; pick the formulas that fit the topic, not all 5 on every topic).
- **3 thumbnail-text ideas** (≤ 5 words each, designed to combine with a visual — text alone is not a thumbnail).
  - Variant 1: text + number ("3 mistakes").
  - Variant 2: text + emotion word ("scary simple").
  - Variant 3: text + outcome ("in 7 days").
- **The viewer curiosity gap** — the one specific question the title/thumbnail combo must open in the viewer's mind. If the title does not open a gap, the title is not a curiosity-gap title; rewrite.
- **The main promise of the video** — the one thing the video must deliver to keep the click. If the video does not deliver on this, the click is a betrayal, and the algorithm will know.

### Section D — Reusable YouTube description template

A template with placeholders. Must include:

- **First 2 lines** (visible above the fold) — the value proposition in plain English, with the primary keyword in the first line.
- **Body** (150–300 words) — what the video covers, with secondary keywords placed naturally (not stuffed).
- **Timestamps** (placeholder, optional) — used by YouTube for chapter markers + Google rich snippets.
- **Resources / links section** — placeholder for affiliate links, sponsor CTAs, related videos.
- **Hashtags** (3–5) — placed at the bottom; the first 3 are visible above the title.
- **Standard CTA block** — subscribe + next-video link.

The template must be written in a tone consistent with the channel's tone from stage 1. Do not ship a generic template.

### Section E — Metadata strategy

- **Title length**: target ≤ 60 characters; never truncate mid-word. Mobile title cutoff is around 50–60 chars.
- **Description length**: target 150–300 words; first 2 lines do the most work.
- **Tags**: 5–15 tags, mostly long-tail; tags are minor for ranking but help with misspellings.
- **Category**: pick the most-specific YouTube category (do not default to "Education" or "Entertainment" if a tighter fit exists).
- **Language + captions**: upload a manual caption file in the channel's primary language; YouTube's auto-captions underperform in retention.
- **End screen + cards**: configured to send to the next video in the publish-order sequence from stage 2.

### Section F — Actionable improvement plan

Organized by the four metrics named in the prompt: **click-through rate, watch time, returning viewers, subscribers**. For each:

- **What to measure** (the specific YouTube Studio metric).
- **What "good" looks like** for the channel's niche (a band, not a number).
- **3 concrete changes** to make this week that move the metric.
- **What to do if it's stuck** — the next thing to try when the first 3 changes don't move the needle.

Prioritize the plan ruthlessly. The biggest gains in the first 30 days almost always come from CTR (packaging) and watch time (script), not from tag tweaks or upload time.

### Section F — Outlier format mining

Keyword opportunity (Section A) answers "what should this video be about?" Outlier mining answers "what should this video look like?" Do both before packaging anything.

- **Build a competitor watchlist** — 5–10 channels in the niche, similar size or one band larger. Follow their output, not their advice.
- **Identify outliers** — a video whose views are a large multiple of that channel's own median. Ignore subscriber count; the outlier signal is relative to the channel's own baseline.
- **Ask AI to analyze why it worked** — title structure, thumbnail composition/text, hook pacing, format (tutorial vs. story vs. list), length. The deliverable is a written breakdown, not a vibe.
- **Copy the format, never the content.** Reuse the structural elements (format, packaging pattern, promise shape) with the channel's own topic, voice, and spin. A near-identical copy reads as déjà vu and gets dismissed; the format is the transferable asset.
- **Combine frameworks** — the channel's own best-performing format merged with an outlier's format beats either alone.
- **Packaging triad rule** — thumbnail + title + hook are one unit. If any of the three is weak, the video does not surface, regardless of content quality. Section C outputs must be judged as a triad, not as separate fields.

## Quality rules

- **Useful beats keyword-stuffed.** "Prioritize ideas that are useful to viewers — not keyword stuffing" is a hard constraint, not a guideline. If a "high-potential" keyword serves no viewer, drop it.
- **No fake numbers in CTR/watch-time bands.** Use bands derived from publicly reported YouTube norms (e.g., "channel-level CTR: 2–10%"), not invented absolutes.
- **No two topics in the same calendar window** (per stage 2's 7-day anti-cannibalization rule) — this stage's 10 topics should be drawn from across the calendar, not clustered.
- **Thumbnail text is ≤ 5 words.** More is unreadable on mobile.- **Thumbnail text is ≤ 5 words.** More is unreadable on mobile.
- **Outlier mining is mandatory before packaging.** A topic with no format evidence behind it gets flagged, not packaged.

## Output file

Writes `03-discoverability-pack.md` into the channel project directory created by `Skills/faceless-yt-niche-brand/`.

## Related skills

- `Skills/faceless-yt-niche-brand/` — produces niche + audience + pillars.
- `Skills/faceless-yt-content-engine/` — produces the 30-day calendar of titles + keywords this stage reworks.
- `Skills/faceless-yt-retention-script/` — stage 4; the main-promise field from Section C is the contract the script must deliver on.
- `Skills/keyword-cluster/` / `Skills/keyword-research/` — for deeper keyword work if the user wants more than the 10 opportunities this stage produces.
- `Skills/image-prompt-builder/` — for generating the actual thumbnail image from a thumbnail-text idea.
