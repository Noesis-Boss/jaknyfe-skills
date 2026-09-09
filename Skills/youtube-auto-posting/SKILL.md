---
name: youtube-auto-posting
description: >
  Run a YouTube channel like a $2,000/month manager. Six ordered prompts —
  define the channel, understand the audience, find video ideas, create titles
  & hooks, write a high-retention script, optimize for retention — followed by
  auto-upload to YouTube. Use when the user wants YouTube strategy, video
  ideas, titles/hooks, scripts, retention passes, or to upload/schedule a video
  to their channel.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  source: "6-prompt ChatGPT channel-manager carousel (cover claim: most people ask for a script before the model knows their niche, audience, and content style)"
---
# YouTube Auto-Posting

Core claim this skill is built on: an AI can run your YouTube channel like a
$2,000/month manager — but only if you run the six prompts **in order**.
Never write a script before the channel profile exists.

## State layout

All artifacts live under `/home/workspace/youtube/<channel-slug>/`:

```
youtube/<channel-slug>/
├── channel-profile.md      # Stage 1 + 2 output. Reused for EVERY video.
├── ideas/YYYY-MM-DD.md     # Stage 3 output: 30 ideas, top 10 ranked
└── videos/<video-slug>/
    ├── titles-hooks.md     # Stage 4: 10 titles, 5 hooks, winner + why
    ├── script.md           # Stage 5: high-retention script
    ├── retention-notes.md  # Stage 6: retention audit + fixes
    ├── final-metadata.md   # title, description, tags, thumbnail file path
    └── video.mp4 / thumbnail.png
```

Stage 1–2 output is written ONCE per channel and loaded for every later run.
If `channel-profile.md` exists, skip stages 1–2 and go straight to ideas.

## Stage 1 — Define the channel (once per channel)

> "Act as a YouTube strategist. Before generating any content, help me define
> my channel's **niche, target audience, and content pillars, tone of voice,
> and video format**. Give me examples from competitors. Give me a clear
> content strategy I can use for every video." 

## Stage 2 — Understand the audience (once per channel)

> "Based on the channel strategy above, create a detailed profile of my ideal
> viewer. Explain what they want, what problems they have, what makes them
> click, how long they'll watch, and what would make them subscribe. This
> profile will guide every video we create."

Append the audience profile to `channel-profile.md`.

## Stage 3 — Find video ideas

> "Using the channel strategy and audience profile above, generate **30
> YouTube video ideas** with strong viral potential. Focus on topics people
> are already interested in, strong curiosity gaps, emotional triggers, and
> ideas that can realistically get clicks. Rank the top 10 ideas by potential."

Save to `ideas/YYYY-MM-DD.md`. The user picks one (or says which number).

## Stage 4 — Create titles & hooks

> "Take this video idea: **[IDEA]**. Generate **10 highly clickable YouTube
> titles** and **5 opening hooks**. Make them create curiosity without being
> misleading. Then choose the strongest title and hook and explain why they
> are likely to get viewers to click and keep watching."

Save to `videos/<slug>/titles-hooks.md`. Cross-check: `Skills/hook-generator/`
can draft alternates if the user wants more variants.

## Stage 5 — Write a high-retention script

> "Using everything we've established so far, write a **high-retention YouTube
> script** for **[TITLE]**. Start with a powerful hook, eliminate unnecessary
> filler, create open loops throughout the video, and structure the story so
> viewers have a reason to keep watching until the end. Write it in our
> established brand voice."

Save to `videos/<slug>/script.md`. Brand voice comes from
`channel-profile.md` — never invent one.

## Stage 6 — Optimize for retention

> "Analyse the script above like a YouTube retention expert. Identify any
> weak points where viewers might drop off and suggest specific improvements
> such as stronger transitions, better examples, pattern interrupts, B-roll
> ideas, pacing changes, or restructured hooks to keep viewers engaged until
> the end."

Apply the accepted fixes to `script.md`, log them in `retention-notes.md`.

## Publish (auto-post)

Video production is agent work; **upload needs explicit user approval**.
Default `privacyStatus` is `private` unless the user says otherwise.

Upload via the connected `youtube_data_api` integration:

1. `list_app_tools("youtube_data_api")` (already known — skip re-checking).
2. Upload: `use_integration(app_slug="youtube_data_api",
   tool_name="youtube_data_api-upload-video", configured_props={
   "title": <winner title>, "description": <description with chapters>,
   "filePath": "/home/workspace/youtube/<slug>/videos/<video>/video.mp4",
   "privacyStatus": "private", "tags": [...], "notifySubscribers": false})`
   — `use_integration` stages local files automatically.
3. Thumbnail (account must be verified):
   `tool_name="youtube_data_api-upload-thumbnail"` with the returned videoId.
4. Report the videoId and watch URL to the user.
5. Schedule option: `privacyStatus: "private"` + `publishAt` ISO timestamp
   (Partner accounts only; fall back to telling the user to flip privacy).

## Batch / automation mode

To run the pipeline on a schedule, use `create_agent` (confirm with the user
first — each run is a full session). A scheduled agent can run stages 3–6 per
cycle and queue finished packages; uploads still require user approval per the
rule above.

## Guardrails

- Never skip stages 1–2 for a new channel.
- Never upload without the user's explicit go-ahead.
- Titles/hooks: curiosity, never misleading (Stage 4 rule).
- `final-metadata.md` is the single source of truth for what gets uploaded.
