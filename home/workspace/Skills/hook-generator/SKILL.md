---
name: hook-generator
description: Generate varied, audience-specific hooks for X, articles, videos, newsletters, LinkedIn, and email subjects.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Hook Generator

Use this skill for first-line copy on posts, articles, videos, newsletters, LinkedIn, and cold-email subjects. Replies and quote-tweets are excluded because the original post is the hook.

## Required input

- Niche or subject
- Target audience
- Content topic
- Surface/platform
- Goal: share, click, agree, or act
- Desired emotion when known

## Output contract

Generate 20 original hooks by default. Use varied psychological triggers: curiosity gaps, unexpected insights, pain points, contrarian opinions, mistakes, transformation, open loops, specificity, and authority.

For every hook provide:

1. Exact opening line.
2. Psychological trigger.
3. One-sentence reason it works for the audience.
4. Best format: video, text, carousel, reel, or other.
5. Retention bridge into the content without revealing the payoff too early.

Finish by ranking the top five for scroll-stopping power, retention, shares, comments, and audience relevance. Name the one to publish first.

## Quality rules

- Make every hook specific to the topic and audience.
- Do not repeat the same opening structure.
- Avoid generic "Here are five tips" openings unless the topic requires a list.
- Avoid empty clickbait, fake statistics, unsupported promises, and claims the content cannot deliver.
- Keep hooks concise, conversational, credible, and varied in tone.
- Use concrete numbers or situations only when relevant.
- Never default to "I was wrong about X for longer than I'd like to admit."

## CLI

```bash
python3 /home/workspace/Skills/hook-generator/scripts/generate_hooks.py "TOPIC" \
  --surface x --audience "AUDIENCE" --goal click
```

The CLI defaults to 20 hooks. Use `--count 5` for smaller automation batches, `--json` for machine-readable output, and `--seed VALUE` for reproducible tests. Production LLM calls should preserve the output contract above rather than relying on a single fixed template.

## Surface-specific guidance

The hook contract above is universal. Each surface adds its own rules — when the surface is one of these, follow the surface rules **on top of** the contract.

### Video (YouTube, TikTok, Reels) — retention-script stage 1

Video hooks live or die in the first **3–5 seconds**. The opening line is one part of a three-part hook system:

1. **Opening line (0–3s)** — the line the viewer hears first. Must name the specific payoff or interrupt the scroll. "Today we're talking about X" is not a hook.
2. **Visual hook (0–5s)** — what the viewer sees. Text overlay, motion, or image that does the work the opening line can't do on its own.
3. **Retention bridge (3–15s)** — the second line that converts a scrolled-past viewer into a viewer who keeps watching. Must open a curiosity loop, set stakes, or deliver the first small payoff. **Do not reveal the video's full payoff here.**

For a 3–5s video hook, the answer to "why am I still here in 10 seconds?" must be in the bridge, not the opener. Output the opening line + a retention-bridge candidate for each hook when `--surface video` is passed.

For a full high-retention script framework (time-coded beats across 0–15s, 15–60s, 1–3min, middle, final 30s + 5 hook formulas + 5 transition formulas), use `Skills/faceless-yt-retention-script/`. This skill produces the **opening hooks only**; that skill consumes them and builds the rest of the structure.

## Related skills

- `Skills/faceless-yt-niche-brand/` — stage 1 of the faceless-youtube-system; defines the niche + audience that the hook must serve.
- `Skills/faceless-yt-retention-script/` — stage 4; consumes hooks and builds the rest of the script framework.
- `Skills/video-script/` — full production-ready video script with timestamps, visual direction, and accessibility notes; can use hook-generator output as the opening section.
- `Skills/faceless-explainer/` — render layer for the final script; produces motion-graphics frames + narration.

## Hook formulas (kept fresh)

When the user wants **fill-in-the-blank hook formulas** they can reuse across many videos (not bespoke hooks for one video), use these five from `Skills/faceless-yt-retention-script/`:

1. **Specific payoff** — "In the next [N] minutes, you'll know [specific outcome] without [common pain]."
2. **Curiosity loop** — "There's a [obscure thing] that [audience] doesn't know about [topic], and it changes [outcome]."
3. **Pattern interrupt** — "[Common advice] is wrong. Here's what works instead."
4. **Numbered promise** — "[N] [things] that [outcome]. #3 is the one most people miss."
5. **Stakes opener** — "If you [common action] without [missing step], you'll [specific bad outcome]."

Fill in the slots, never the structure. Re-test against the audience definition in `Skills/faceless-yt-niche-brand/`.
