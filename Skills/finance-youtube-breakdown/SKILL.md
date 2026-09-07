---
name: finance-youtube-breakdown
description: Build research-backed, faceless YouTube finance-breakdown content from competitor evidence. Use whenever the user asks for finance YouTube niche research, faceless channel ideas, competitor transcript analysis, video scripts, scene prompts, thumbnails, titles, metadata, or a repeatable content pipeline. Treat revenue, RPM, growth, and monetization claims as hypotheses that require verification.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
---

# Finance YouTube Breakdown

Turn a narrow finance-business topic into a defensible content slate and one publish-ready video brief.

## Operating rules

- Research first. Separate observed facts, estimates, and inference.
- Do not copy a competitor's wording, structure line-for-line, thumbnail, branding, or distinctive creative expression.
- Finance content is educational, not personalized financial advice. Flag claims needing primary sources and current data.
- Never promise income, monetization, virality, or a timeline to success.
- Prefer public, attributable sources. Record URLs and access dates.
- Default to a human approval gate before narration, upload, sponsorship, affiliate links, or paid promotion.

## Workflow

1. **Define the channel thesis.** State audience, geography, business category, educational promise, and exclusions.
2. **Validate the market.** Inspect at least 5 relevant channels and 15 recent videos. Record upload date, views, duration, title promise, thumbnail pattern, and visible engagement. Mark third-party revenue estimates as estimates.
3. **Extract style DNA.** Compare 2–3 transcripts or detailed summaries for hook, pacing, sections, proof, transitions, pattern interrupts, and recurring promise. Use the analysis to create original conventions.
4. **Find gaps.** Generate 10 candidate topics, compare them against competitor catalogs, remove duplicates, and score each for evidence quality, audience value, freshness, production effort, legal/reputational risk, and repeatability.
5. **Create the video brief.** Include a sourced outline, original hook options, script target, scene map, visual prompts, thumbnail directions, title options, description, tags, and required disclaimers.
6. **Prepare production assets after approval.** Generate or collect original visuals, create narration through an approved voice provider, create captions, and write a render manifest. Each major narration beat must have a scene-specific visual; static full-video backgrounds are not acceptable. Do not use competitor footage, music, scripts, branding, or thumbnails.
7. **Render a draft after approval.** Use the bundled FFmpeg renderer to assemble a 16:9 MP4 with scene timing, animated motion graphics, evidence bullets, charts or diagrams, narration, captions, and optional background music. Save the draft and a QC report under the video folder.
8. **Quality-control.** Run a factuality pass, originality pass, finance-risk pass, production-feasibility pass, and rendered-media pass. Mark unresolved items explicitly.

## Required output

Return these sections:

1. Verdict: what is supported, what is weak, and whether to test.
2. Evidence table with source URL, observed fact, confidence, and caveat.
3. Channel thesis and audience.
4. Competitor/content-gap table.
5. Ranked 10-video slate.
6. Full brief for the top video.
7. 30-day test plan with a stop/continue rule.
8. Risks: platform policy, financial misinformation, copyright, AI disclosure, and source freshness.

## Test design

Recommend a small test: 8–12 original videos over 30 days, consistent packaging, and a measurement sheet tracking impressions, click-through rate, average view duration, retention, returning viewers, subscribers per 1,000 views, and revenue only after verified analytics access. Do not use the article's $40–$50 RPM or $5,700/month figures as forecasts.

## Video production contract

The production handoff lives at `noesis_content/youtube/finance-breakdown/<slug>/` and contains `brief.md`, `manifest.json`, `audio/`, `visuals/`, `captions.srt`, `thumbnail.png`, and rendered output under `draft/`. The manifest must identify the source URL for every factual claim and the license or generation provenance for every visual/audio asset.

Run the renderer with:

```bash
python3 Skills/finance-youtube-breakdown/scripts/render_video.py --manifest noesis_content/youtube/finance-breakdown/<slug>/manifest.json
```

The renderer is deterministic and local. It does not call YouTube, sponsors, ad platforms, or social networks.

## Shared media transfer

The ElevenLabs connector may return generated audio from an isolated `/tmp` environment that is not visible to local FFmpeg. For production renders, use the shared Zo `ELEVENLABS_API_KEY` with the official ElevenLabs text-to-speech endpoint and write the response directly into the video's `audio/` directory. Do not rely on the connector's returned `/tmp` path as a local filesystem path.

## Automation handoff

The weekly automation should research the opportunity, produce the brief and slate, and stop at an explicit human approval gate. After approval, it may generate narration, visuals, captions, thumbnails, and a local draft MP4. Once all QC checks pass, it may publish the approved video only to `https://youtube.com/@Noesisgroup` through the connected YouTube Data API integration. It must not publish elsewhere, contact sponsors, spend money, or alter channel settings.
