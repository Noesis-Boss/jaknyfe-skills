# Better than Jev - because you can build with it

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-22T22:24:19+00:00
- **Video**: https://www.youtube.com/watch?v=tsWOiibaaxA

## Description

Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Andrew Warner and Henry Ndubuaku show how Needle brings small, private AI models directly into software and devices.

Andrew Warner talks with Henry Ndubuaku about Needle, Cactus Compute’s tiny on-device LLM built for reliable automation without requiring an internet connection or external API calls. Henry demonstrates how Needle turns natural-language requests into structured tool calls, powers software features and hardware like robot vacuums, and uses tightly scoped actions and confidence scores to reduce mistakes. They also compare Needle with Jev and explain why running an 8–29 MB model locally can matter for privacy, cost, and bringing AI into smaller devices.

Links featured:

Needle: https://github.com/cactus-compute/needle

00:00 - Needle: Run a small, free LLM locally for private and reliable automation.
00:18 - Smart Home Demo: Turn lights on and off by translating natural-language requests into structured tool calls.
01:39 - Search & Matching: Use Needle inside software for reminders, search, extraction, and other defined actions.
03:18 - Local App Integration: Add Needle to software without relying on Anthropic or another external LLM API.
04:12 - LLM.txt: Give Claude the context it needs to incorporate Needle directly into an app.
04:48 - On-Device AI: Put Needle into hardware instead of limiting it to desktop software.
05:06 - Robot Vacuum: Control a vacuum with natural-language commands while keeping the model on the device.
06:09 - Zapier SDK: Add integrations with thousands of apps alongside Needle-powered local automation.
07:12 - Reliability: Restrict Needle to carefully defined tools and actions to reduce unexpected behavior.
08:51 - Confidence Scores: Use Needle’s confidence output to decide whether an automated action should execute.
10:12 - Phones & Laptops: Organize photos, start timers, copy screen content, and automate device actions locally.
11:42 - Needle vs Jev: Compare their shared focus on constrained outputs and safer automation.
13:21 - 8–29 MB Models: Run Needle on small devices like smartwatches, remotes, AirPods, and other privacy-sensitive hardware.
14:15 - GitHub Origins: Andrew explains how Needle first caught his attention after trending among the week’s top GitHub repos.

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=tsWOiibaaxA! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8366★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **cactus-compute/needle** — 12472★ · Python · pushed 2026-09-23 · license Apache-2.0
  - Automation foundation model for tiny devices: 2-bit, 8-29 MB, tool calls, structured extraction and embeddings on phones, wearables, smart homes, robots, cars and microcontrollers.
  - https://github.com/cactus-compute/needle

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Transcript retrieval was blocked by YouTube for this run. The description identifies the featured repository directly.

### cactus-compute/needle — https://github.com/cactus-compute/needle

Functionality: A compact on-device model for constrained natural-language commands, structured tool calls, extraction, and embeddings. Its target is private, low-resource devices and embedded automation.

- Signals: 12,472 stars · Python · Apache-2.0 · last push 2026-09-23 · active, not archived.
- Recommendation: **TRIAL** — test it in a sandbox for small deterministic helpers or offline device workflows, comparing accuracy, latency, and tool-call safety with current model APIs. Rough effort: 2–4 hours; it is too specialized for immediate adoption in the trading bot or publishing pipeline.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without browser automation. It is the transcript backend used by this watcher.

- Signals: 8,366 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency.
