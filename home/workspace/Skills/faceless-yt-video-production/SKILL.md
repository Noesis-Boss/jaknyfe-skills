---
name: faceless-yt-video-production
description: Stage 6 of the faceless YouTube system — turn a stage-4 script into a shot-by-shot production plan with visual beats, stock search terms, pacing, transitions, subtitle styling, voice direction, and BGM. Borrows the MoneyPrinterTurbo production mechanics (script-ordered visual terms, clip-length pacing, transition rotation, multi-variant output).
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# faceless-yt-video-production

Consume a stage-4 script (`04-script-<slug>.md`) and produce a per-video production plan a renderer (human editor, `Skills/faceless-explainer/`, or a MoneyPrinterTurbo-style pipeline) can execute without further decisions. The problem this stage exists to fix: informational scripts read fine but the resulting videos look monotonous and the voiceover has no performance. Fix both here, on paper, before render time.

Mechanics below are borrowed from the MoneyPrinterTurbo pipeline (`Skills/money-printer-turbo/app/services/`): `task.generate_terms` (script-ordered visual search terms), `video.combine_videos` (max clip duration + clip speed), `video_effects` (transition rotation), `subtitle` (styled captions), and `voice` (per-provider voice parameters).

## Required input

- `04-script-<slug>.md` — the retention-script output for this video.
- Stage 1 brand doc — for visual identity (colors, fonts, tone) and the tool stack.
- Video slug — same slug as the script.

## Output file

`06-production-<slug>.md` in the channel project directory. One per video, matching its script.

## Section 1 — Visual beat sheet (script-ordered)

Split the script into scenes of **≤ 1 sentence of narration each**. For every scene produce:

1. **Timestamp range** — cumulative from the script's time codes.
2. **Narration line** — verbatim from the script.
3. **Visual** — what is on screen. Vary the visual type across scenes; never the same type twice in a row (see the variety ladder below).
4. **Stock search terms** — 1–3 words each, `subject + noun`, in the same order as the narration. Terms must describe *this* scene's visual moment, not the video's overall topic. This is the MPT rule: keywords follow script order, so the edit's imagery tracks the narration instead of recycling a handful of global topic clips.
5. **On-screen text** — ≤ 6 words, only if it adds a number, contrast, or name the narration doesn't carry.
6. **Motion note** — one of: static / slow push-in / slow pull-out / pan L→R / pan R→L. Never the same motion note twice in a row.

### The variety ladder (anti-monotony rules)

Rotate across five visual types; no type may appear more than twice consecutively:

| Type | Use for | Cadence |
| --- | --- | --- |
| Stock b-roll | context, atmosphere | the default, ~50% of scenes |
| Text-on-screen card | numbers, lists, the "first pattern change" | every 20–30s minimum |
| Data/chart build | any claim with a number | every stat gets one |
| Diagram/mapping shot | relationships, flows, before→after | when narration explains how two things connect |
| Full-frame quote or question | open loops, section resets | at each phase boundary from the script |

Also enforce:

- **Max clip duration 4s** for b-roll (MPT's `video_clip_duration` discipline). If a visual must hold longer, add a slow push-in so it still has motion.
- **Clip speed variation** — render 1–2 b-roll clips per video at 0.8x or 1.25x (`clip_speed`) so motion energy is not uniform.
- **Transition rotation** — cycle fade-in, fade-out, slide-in, slide-out, zoom-in, zoom-out (MPT's `video_effects` set). No transition twice in a row; no transition on the first 3 seconds (the hook cut is hard).
- **Aspect discipline** — one aspect per video; crops decided here, not at render time.

## Section 2 — Voice performance direction

The script is information; the voiceover is a performance. For each script phase (hook / establish / deep payoff / middle / payoff+CTA) record:

1. **Pace** — words-per-minute target and whether it ramps. Hook: fastest. Deep payoff: measured. CTA: brisk.
2. **Energy arc** — one line per phase, e.g. "hook: urgent, conspiratorial" → "deep payoff: authoritative, slower on the number."
3. **Emphasis words** — the 3–5 words per minute the voice must punch (numbers, contrasts, names).
4. **Pause marks** — where silence replaces transition words. Minimum: after the hook, before each payoff.
5. **TTS parameters** — voice ID, speed (0.9–1.1 range; ≠ 1.0 by default so delivery is not flat), and a per-section direction string usable verbatim in ElevenLabs/Kokoro prompts. MPT exposes voice speed/volume as first-class params; we do the same at the plan level.

## Section 3 — Subtitle + caption plan

- **Style tokens** — font, size band, stroke/outline color, highlight color for emphasis words, screen position (lower-third default). Pull from stage 1 brand tokens.
- **Emphasis karaoke** — highlight the Section-2 emphasis words in captions. MPT's subtitle service styles captions per-word; replicate by marking them in the plan.
- **Caption cadence** — max ~5 words per caption card; numbers and quotes get their own card.

## Section 4 — Music bed

- **Bed track source** — one track per video from the approved library (e.g. `Skills/money-printer-turbo/resource/songs/` or the channel's library), chosen for tone, not default.
- **Volume** — 8–15% under voice; duck to ~5% during emphasis pauses.
- **Music-off rule** — if a provider-generated bed fails, ship voice-only and log it (MPT degrades to no-BGM rather than blocking the video). Never let a failed music call block the render.

## Section 5 — Variants

Produce **2 complete variants** of Sections 1–4 for the same script (MPT's `video_count` concept), differing in at least: hook b-roll, transition order, and music bed. Render both when budget allows and let real CTR/retention pick the winner; otherwise render variant A and keep B as the pre-approved alternate.

## Quality rules

- Every scene has a visual, a search term, and a motion note — no "TBD".
- The visual-beat sheet must cover 100% of narration timestamps with zero gaps.
- Search terms are concrete nouns, not abstractions ("shipping container yard", not "economy").
- Voice direction is per-phase, never one global line like "energetic".
- The plan must be executable by someone who has never seen the script.

## Related skills

- `Skills/faceless-yt-retention-script/` — stage 4; produces the script this stage consumes.
- `Skills/faceless-yt-discoverability/` — stage 3; packaging contract (thumbnail/title) this plan must not contradict.
- `Skills/faceless-explainer/` — the render layer that can execute this plan.
- `Skills/money-printer-turbo/` — upstream production pipeline these mechanics are borrowed from.
- `Skills/hook-generator/` — hook lines referenced by the script.
