---
name: faceless-yt-niche-brand
description: Stage 1 of the faceless-youtube-system. For a given niche, produce 3 differentiated channel angles, 5 memorable channel-name candidates with taglines, a detailed target-viewer profile, 4 content pillars, recommended video formats/length/frequency/tone, and a beginner tool stack for scripting, voiceover, visuals, stock footage, thumbnails, editing, and AI video.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# faceless-yt-niche-brand

Use this skill as **stage 1** of the faceless-youtube-system. The 5 stages are: niche-brand → content-engine → discoverability → retention-script → monetization. Run them in order; downstream stages consume the previous stage's output.

## Required input

- **Niche** — the topic area. Pass as `[your niche]` placeholder or as a real niche string.

## Output (single markdown document)

### 1. Three differentiated channel angles

For each angle, write 2–3 sentences explaining:

- **The viewer problem the channel solves** (the reason someone subscribes).
- **The differentiation vs. existing competitors** (the reason someone chooses this channel over a similar one).
- **The faceless angle** (why this channel works without an on-camera presenter — voiceover over stock, motion graphics, screencast, etc.).

All three angles must serve the same niche but compete on different axes (e.g., one depth-first, one entertainment-first, one update-first). Do not produce three near-duplicates.

### 2. Five memorable channel-name candidates

For each: name, short tagline (≤ 7 words), one-line rationale (why it sticks, what it signals, why it works for the niche). The name must:

- Be pronounceable in one read (no clever spellings of common words).
- Be searchable — no near-duplicate of an existing major channel in the same niche.
- Be ≤ 3 words; long names die in subscriber recall.
- Allow a tagline that does the niche signaling the name itself does not.

### 3. Detailed target viewer profile

A single concrete persona, not a demographic blur. Cover:

- **Who they are** — age range, life situation, prior knowledge of the niche.
- **What they have already tried** — the books, channels, products, or methods they bounced off of.
- **What they believe about the niche** — the assumption that brought them to YouTube for this topic.
- **The specific moment they reach for a new video** — the trigger, not the topic.
- **What would make them unsubscribe** — the failure mode the channel must actively avoid.

### 4. Four core content pillars

Each pillar is a recurring content category the channel returns to. For each pillar:

- **Pillar name** — 2–4 words.
- **What it covers** — 1 sentence.
- **What it does NOT cover** — 1 sentence (to keep pillars from bleeding into each other).
- **Example video titles** — 3, to make the pillar concrete.

The four pillars must collectively cover the niche without overlap. A viewer should be able to say "this is pillar 2" from the title alone.

### 5. Recommended video formats, length, frequency, and tone

| Field | Default starting point | When to deviate |
| --- | --- | --- |
| **Primary format** | Long-form 8–12 min. | Niche with shorter attention (Top 10, news): 6–8 min. Tutorial-heavy: 12–18 min. |
| **Secondary format** | Shorts 30–60s repurposed from long-form. | Niche with strong visual payoff: original Shorts. |
| **Length sweet spot** | 10 min for ad-revenue eligibility + watch time. | Tutorial +18 min if retention holds >50%. |
| **Posting frequency** | 2 long-form + 2 Shorts/week. | Solo creator: 1 long + 2 Shorts. |
| **Tone** | Define in 3 adjectives (e.g., "calm, specific, evidence-led"). | Niche with personality expectation: add 1 energy adjective. |

### 6. Beginner tool stack (table form)

Cover each of: scripting, AI voiceover, visuals, stock footage, thumbnails, editing, AI-assisted video creation. For each:

- 1 free or freemium default
- 1 paid upgrade (when the creator outgrows the default)
- 1 sentence on when the upgrade becomes worth it

The stack must assume a solo creator with $0–50/month to start. No enterprise tiers.

## Quality rules

- Niche must be honored — every channel angle, name, and pillar must be a credible fit, not generic "How to X" boilerplate.
- Differentiation claims must be specific. "We go deeper" is not differentiation; "we test every recommendation against a 30-day measurement" is.
- The tool stack should assume Mac/Windows/browser; do not list tools the user would need to compile from source.
- Tone adjectives must be paired with behavioral consequences (e.g., "evidence-led → always cite a source, never assert from authority alone").

## Output file structure

```
<channel-name-candidate>/
  01-niche-and-brand.md       ← this skill's full output
  02-30-day-calendar.md       ← Skills/faceless-yt-content-engine output
  03-discoverability-pack.md  ← Skills/faceless-yt-discoverability output
  04-script-<video-title>.md  ← Skills/faceless-yt-retention-script output
  05-monetization-roadmap.md  ← Skills/faceless-yt-monetization output
```

The skill writes `01-niche-and-brand.md` and the directory; downstream skills write their own numbered files into the same directory.

## Related skills

- `Skills/faceless-yt-content-engine/` — stage 2; consumes pillars + audience.
- `Skills/faceless-yt-discoverability/` — stage 3; consumes angle + niche.
- `Skills/faceless-yt-retention-script/` — stage 4; consumes angle + tone + format.
- `Skills/faceless-yt-monetization/` — stage 5; consumes niche + audience + content mix.
- `Skills/brand-builder/` — for the brand-side work (identity, voice, launch checklist) when the user wants more than this stage provides.
- `Skills/audience-profile/` — for the viewer profile; this skill produces a single persona, that skill produces a richer set.
