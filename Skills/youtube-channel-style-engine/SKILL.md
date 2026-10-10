---
name: youtube-channel-style-engine
description: Analyze a YouTube channel's transcripts and visual samples to extract high-level storytelling and visual mechanics, then create original scripts, beat-by-beat image/video prompts, thumbnail concepts, and an optional Word export in a strict, resumable 11-state workflow. Use when asked to clone, model, or reverse-engineer a channel's content approach. Never copy wording or distinctive creative expression.
metadata:
  author: jaknyfe.zo.computer
---

# YouTube Channel Style Engine

Turn a channel study into original production assets. Model broad craft mechanics; do not impersonate a creator or reproduce their expression.

## Hard rules

- Follow the 11 states in order. Handle exactly one state per assistant turn. Never merge, skip, reorder, or preview a state.
- Track the current state from this conversation. Do not claim hidden or cross-chat persistence. If state is genuinely unclear, ask one brief question to identify it.
- On `status`, reply only with the current state name and number. On `restart`, reset and output the State 1 request. Match commands case-insensitively.
- For incomplete or invalid input, ask once for the specific missing piece and stay in that state. Do not treat partial material as approval to advance.
- Do not ask for, describe, or reason about visuals before State 6. States 1–5 are text-only.
- Never quote or reuse transcript wording in generated material. Do not copy signature phrases, distinctive metaphors, a creator's persona, an exact section-by-section script, branded assets, or a thumbnail's particular layout/artwork. Abstract general techniques and recombine them with original choices.
- Use only material the user provides or ordinary public information. Do not bypass access controls, download private videos, or imply affiliation with the studied channel.
- Treat factual claims as claims to verify, not as style. For finance topics, verify current facts with primary sources when research is requested, distinguish fact from inference, and avoid personalized financial advice.
- All content is a draft. Do not upload, publish, schedule, contact sponsors, or spend money without explicit approval for that specific action. For AI for the Rest of Us videos, require Don's explicit per-video approval before any YouTube upload, publication, or scheduling.
- Keep user-facing responses terse and free of greetings or process preambles. Higher-priority system, safety, and workspace rules still apply.

## State tracking and transitions

A state may either request input or produce that state's artifact. After a state artifact, stop and wait; the user can say `continue` to enter the next state. Do not silently produce the next state's request in the same turn. For states that request source material, analyze it only after the user supplies it. The only exception is State 3's idea list, which is part of that state and must end by asking the user to choose.

## State 1 — Channel Link

On the first turn, and whenever restarted, output exactly:

> Please provide the YouTube channel link.

Stop. If the link is missing or not recognizably a YouTube channel URL/handle, request a valid channel link and remain in State 1. Once accepted, the next response is State 2's request only.

## State 2 — Transcripts

Output exactly:

> Paste 2–3 full video transcripts from this channel (complete, not summaries).

Stop. Accept 2–3 usable, distinct transcripts. To calculate WPS, each transcript must include timestamps or an associated full video runtime. If duration data is missing, ask only for the missing runtime(s) or timestamped transcript(s) and stay in State 2. Once the transcripts and timing data are usable, the next response is State 3's request only.

## State 3 — Topic / Ideas

Output exactly:

> Do you want me to generate video ideas, or do you already have a topic? If you have one, paste it.

If the user requests ideas, generate 8–10 titled ideas that fit the niche and audience evident from the provided channel material. Do not make visual suggestions. Ask the user to choose one, then stop. When the user picks an idea, confirm the locked topic in one line and stop. If the user supplies a topic, confirm it in one line and stop. In either case, remain in State 3 until the user says `continue`.

## State 4 — Analysis + Style DNA

After `continue`, analyze the accepted transcripts and topic. Describe repeatable mechanics, not transcript content. Do not quote examples. Output a structured STYLE DNA block covering:

- Niche and sub-niche
- Target audience: who, sophistication, desires, and pain points
- Hook mechanics in the first 1–2 lines: pattern, promise, and tension
- Script flow: reusable section-level skeleton
- Sentence rhythm: short/long mix, fragments, and cadence
- Tone and voice: high-level register/personality traits, without imitating identity or quoting phrases
- Transitions
- Curiosity gaps: how loops open and resolve
- Emotional triggers and their order
- Retention mechanics: callbacks, teasers, stakes, and pacing changes
- Direct address: how and when the audience is addressed
- Average transcript word count
- WPS, calculated as total transcript words divided by total spoken-duration seconds. Prefer timestamped spoken intervals; otherwise use supplied full runtimes and label the result runtime-based. Never invent duration or call an estimate measured.
- `TARGET_WORD_COUNT = <average transcript word count>` (±5%)
- `WPS = <measured value>`

If timing data cannot support a defensible WPS, stay in State 4 and ask for the missing data; do not fabricate beat timing. Stop after the block. Wait for `continue` before State 5.

## State 5 — Script (Style Locked)

After `continue`, first output:

> Target word count: <TARGET_WORD_COUNT> (±5%).

Then write the complete script on the locked topic. Follow the abstract Style DNA, but use a fresh structure where needed to avoid copying the source's exact sequence. The script must be original, contain no visual direction, use no transcript wording, and land within ±5% of the target. Count the words consistently; revise before presenting if outside tolerance. End with:

> Final word count: <actual>.

Stop. Wait for `continue` before State 6.

## State 6 — Visual Input + Analysis

After `continue`, output exactly:

> Upload 3–5 sample images from this channel's videos (NOT thumbnails).

Stop. After the user supplies 3–5 images, analyze them and output a VISUAL STYLE PROFILE with:

- Art style
- Color palette
- Lighting style
- Camera style / lens feel
- Composition rules
- Detail level / texture
- Mood

Describe abstract production traits, not identifiable frames or branding. Lock this profile for later prompts. Stop and wait for `continue` before State 7.

## State 7 — Image Prompts (Every Beat)

After `continue`, divide the entire State 5 script into sequential, contiguous beats of approximately `WPS × 4` words (about four seconds each). Cover 100% of the script in order; no gaps, overlap, or omitted lines. Keep each beat label as the exact corresponding script segment.

For every beat, provide:

- Beat number and exact script segment
- Image prompt, fully standalone
- Camera angle
- Lighting
- Mood
- Action

Every standalone image prompt must independently describe subject, setting, composition/camera, lighting, mood, and the complete locked VISUAL STYLE PROFILE. Do not refer to another beat or rely on shared context. Keep each prompt original and avoid repeating recognizable source-channel imagery. Stop and wait for `continue` before State 8.

## State 8 — Video Prompts (Optional)

Output exactly:

> Do you want video prompts for each image prompt? (yes / no)

Stop and wait. If the answer is `yes`, create one motion prompt for every State 7 image prompt. Include subject motion, camera movement, pacing, and duration of about 3–5 seconds; retain the locked VISUAL STYLE PROFILE and keep every prompt standalone. Stop. If the answer is `no`, acknowledge nothing else and stop. In either case, wait for `continue` before State 9.

## State 9 — Thumbnail Input + Analysis

After `continue`, output exactly:

> Upload 2–3 thumbnail images from this channel.

Stop. After the user supplies 2–3 thumbnails, analyze them and output a THUMBNAIL DNA block covering:

- Text style: weight, size, placement, and typical word count
- Composition: subject placement and focal hierarchy
- Color contrast: palette, saturation, and contrast/pop treatment
- Emotional triggers: expression, tension, and curiosity devices

Abstract general design mechanics only. Do not reproduce a particular thumbnail or its branding. Stop and wait for `continue` before State 10.

## State 10 — Thumbnails

After `continue`, create five distinct thumbnail concepts. Each includes:

- Visual concept
- Short, high-impact text overlay
- Emotion trigger
- Standalone generation prompt following the abstract THUMBNAIL DNA

Keep concepts original; do not replicate a source thumbnail's exact layout, artwork, wording, or branding. Stop and wait for `continue` before State 11.

## State 11 — Export (Optional)

Output exactly:

> Do you want everything exported into a Word document? (yes / no)

Stop and wait. If `yes`, compile the Style DNA, script, image prompts, any video prompts, and thumbnail concepts into one structured `.docx`. Use Pandoc when available; keep intermediate files in scratch space and save the requested artifact in an appropriate location under `/home/workspace` without overwriting an existing file. If no safe destination is evident, ask one focused location question and remain in State 11. If `no`, end the workflow.
