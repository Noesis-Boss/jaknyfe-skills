---
name: hook-generator
description: Skill + cross-session rule that generates attention-grabbing first lines for auto-posted content (X, articles, cold emails, LinkedIn)
type: project
---

# hook-generator

**Location:** `Skills/hook-generator/` (SKILL.md + scripts/generate_hooks.py + references/auto-pipeline.md)

**Cross-session rule:** Active. Triggers on any X/tweet/post event or use_app_x call. Auto-injects the hook-generation workflow into every posting flow.

## Posting surfaces covered

- `use_app_x` / `x-post-tweet` (native Zo X integration)
- `bird tweet` (Twitter CLI)
- `node xpost.mjs tweet` (x-twitter-by-altf1be)
- Scheduled automations: zdsentry posting, trending-topics tweet automation
- Other: articles, blog headlines, video captions, cold email subject lines, LinkedIn openers

## How to skip

Manual one-off posts where Don types the first line himself. Replies and quote-tweets (the original post IS the hook). Thread bodies (only the first tweet needs a hook).

## CLI

```bash
python3 /home/workspace/Skills/hook-generator/scripts/generate_hooks.py "TOPIC" \
  --surface x|article|subject|linkedin|video|newsletter \
  --audience "AUDIENCE" \
  --goal share|click|agree|act
```

## Variety fix (2026-06-13)

**Bug:** Multiple auto-posted tweets (notably Jun 12 evening + Jun 13 morning) reused the same opening line shape — typically the curiosity variant "I was wrong about X for longer than I'd like to admit." Same template, different topics, every post.

**Root cause:** The `generate_hooks.py` script had exactly ONE template per style (8 styles, 1 string each). The default seed was deterministic from the topic+surface hash, so the same input always produced the same output.

**Fix applied to `/home/workspace/Skills/hook-generator/scripts/generate_hooks.py`:**
- Expanded each style pool to 8-10 templates (curiosity/contrarian/stat/story/bold/question/confession/specific + 5 more styles: list, observation, comparison, warning, forecast)
- Per-call random seed by default (overridable with --seed for reproducibility)
- Per-call shuffled number pool (no more "73/91" pair dominating every stat template)
- Anti-repetition guard: each new hook is checked against the others (first-5-words Jaccard > 0.6 = reroll up to 8 times)
- Variety in second lines (CLOSER_POOL of 14 options, picked randomly)
- Removed the "I was wrong about X for longer than I'd like to admit" pattern from the CURIOSITY pool
- Fixed extract_signals to handle multi-word proper nouns better and drop suffixes like "Inc/AI/Co"
- Synced to `/home/workspace/jaknyfe-skills/skills/hook-generator/` mirror (uncommitted - Don can push when ready)
- SKILL.md updated with a Variety section + the CURIOSITY example reframed away from the "I was wrong" pattern

**Verified:** 10 runs on the same topic produce 10 distinct sets of hooks with rotating numbers, styles, and templates.