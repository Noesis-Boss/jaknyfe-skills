# REA use cases you'll love

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-19T23:47:32+00:00
- **Video**: https://www.youtube.com/watch?v=BctbCJP9lKU

## Description

Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Andrew Warner tests what Reverse Engineer Anything can actually do by reacting to real software-cloning demos.

Andrew Warner looks at REA, or Reverse Engineer Anything, through a series of YouTube demos showing how coding agents can inspect closed-source apps, understand how features work, and rebuild or adapt them. The episode covers cloning QuickTime Player, TickTick, WhisperFlow, a video editor inspired by CapCut, and Loom, plus using REA to find bugs in your own software. Andrew also digs into the bigger question behind all of this: when does reverse engineering become a legitimate way to learn, customize, or improve software, and when does it cross the line into copying?

00:00 - Reverse Engineer Anything: See how REA lets coding agents inspect closed-source software and rebuild features from it.
01:12 - REA Setup: Install the MCP server and skill that teaches your coding agent how to investigate applications.
01:39 - QuickTime Player Clone: Rebuild QuickTime with more granular playback speed controls and extra features.
03:27 - How REA Works: Use tools like Ghidra, Hopper, and IDA Pro through plain-language agent commands.
04:30 - TickTick Clone: Reverse engineer a task manager and rebuild its task lists, calendar, tags, and workflows.
06:54 - Premium Features: See REA recreate functionality that was hidden behind TickTick’s paid plan.
07:39 - Where the Clone Fails: Look at missing features, UI differences, and the extra prompting still needed.
09:54 - WhisperFlow Clone: Rebuild a voice-to-text desktop app with local transcription and multilingual input.
13:39 - Bug Testing: Use REA on your own app to uncover issues that might not be obvious from reading the code.
16:03 - CapCut-Inspired Video Editor: Build a simpler editor with timeline controls, splitting, captions, and export.
19:21 - Inspiration vs Copying: Andrew explores whether using an existing app as a starting point becomes legitimate once you change the product.
19:48 - Loom Clone: Recreate Loom-style recording, movable camera bubbles, and local file storage without copying the exact UI.
21:00 - Final Take: Andrew weighs the practical value of REA against the ethical questions around cloning software.

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=BctbCJP9lKU! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

(none auto-extracted — read the transcript above and identify repo names, then search GitHub)

## Agent eval

> **Transcript note**: Transcript unavailable (YouTube IP-blocked). All analysis below is drawn from the video description and chapter titles. The episode demos REA against QuickTime Player, TickTick, WhisperFlow, a CapCut-inspired editor, and Loom — these are **demonstration targets**, not standalone repos. Only one actual repository is presented.

### morluto/rea — https://github.com/morluto/rea

**Functionality**: REA (Reverse Engineer Anything) is an MCP server and CLI that arms AI coding agents (Claude Code, Codex, Cursor, Gemini CLI) with reverse-engineering tooling. It decompiles native binaries, Electron apps, .NET assemblies, and Android APKs, and captures network traffic — returning evidence-backed pseudocode, module graphs, and request logs so the agent can understand and rebuild closed-source software. Install is one command: `npx rea-agents setup`.

**Signals**: 343,183★ · TypeScript · MIT license · pushed 2026-10-20 · not archived · 86,529 forks · homepage rea.tools · npm package `rea-agents`. One of the fastest-growing repos on GitHub (115K stars within a week of October 2026).

**Recommendation: TRIAL** — REA is the most interesting agent-tooling release of the month and directly relevant to our Bun/TS stack. The static analysis paths (JavaScript, .NET, website, network capture) work with zero extra engines; deep native binary analysis needs Hopper, Ghidra 12.1+, or IDA (commercial/separate licenses). Test plan: install `npx rea-agents setup`, point it at a small Electron app or a saved HAR capture, and check whether the evidence model (file digests, byte ranges, explicit unknowns) is as rigorous as advertised. Rough effort: 30 min install + 1–2 hour test session. Not INCLUDE outright because the headline native-binary use case requires tools we don't own, and the MCP surface area is large (207 tool definitions loaded eagerly in some clients). If the static path proves useful, promote to INCLUDE for the Zo automation and Skills-repo tooling workflows.
