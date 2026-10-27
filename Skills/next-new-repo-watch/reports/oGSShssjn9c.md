# AI Agents Finally Share One Memory (Claude Mem Explained)

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-21T18:39:31+00:00
- **Video**: https://www.youtube.com/watch?v=oGSShssjn9c

## Description

Link to Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/

What if Claude, ChatGPT, and GrokBot could share memories and pick up each other’s work without you having to repeat instructions? Alex Newman demonstrates Claude Mem, an open-source tool designed to connect AI agents through shared memory.

Andrew Warner shows how he uses Claude Mem to bring work from Claude Code into ChatGPT, generate clear visual summaries from coding tasks, and access ideas and context from previous projects. Alex and Andrew explore how to install Claude Mem, connect different agents, keep memory local or run a self-hosted server, and reduce the manual work involved in switching between AI tools.

The bigger vision is a universal memory layer for AI agents—one that lets you use the best model for each task while keeping your projects, research, and ideas connected across tools.

Links featured:

- Claude Mem: https://github.com/thedotmack/claude-mem
- Grok Mem: https://grok-mem.ai/

00:00 - Claude Mem: Share Memory Across AI Agents
00:36 - Live Demo: Bring Claude Code Work Into ChatGPT
01:12 - Generate Infographics From Coding Tasks
02:06 - Connect Claude, ChatGPT, and GrokBot
02:24 - Privacy and Security: Where Is Your Memory Stored?
02:42 - Run Claude Mem Locally or With Your Own Server
03:36 - Install Claude Mem and Connect Your Agents
04:12 - Connect GrokBot to Shared Memory
04:30 - Use the Best AI Model for Each Task
05:15 - Eliminate Manual Handoffs Between AI Tools
05:33 - Can AI Agents Hand Work Off to Each Other?
05:51 - The Vision: A Universal Memory Adapter for AI Agents
06:18 - Explore the Top 10 Trending GitHub Repositories

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=oGSShssjn9c! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **thedotmack/claude-mem** — 102242★ · TypeScript · pushed 2026-10-22 · license Apache-2.0
  - Persistent Context Across Sessions for Every Agent –  Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions. Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More
  - https://github.com/thedotmack/claude-mem

## Agent eval

**Transcript note:** Transcript was unavailable from the cloud host (YouTube IP block). All analysis below is drawn from the video description plus current GitHub evidence.

### thedotmack/claude-mem

- **Functionality:** Claude Mem is a persistent context layer that captures everything an AI agent does during a session, compresses it with an LLM, and injects relevant context back into future sessions — so work carries across tool boundaries (Claude Code → ChatGPT → Grok, etc.) without re-explaining. It runs as a local daemon or self-hosted server with per-project memory stores and supports a wide agent surface (Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode and more).
- **Signals:** 102,242★ · TypeScript · Apache-2.0 · last push 2026-10-22 · not archived · extremely actively maintained
- **Recommendation: INCLUDE** — Install/adapt now. It plugs directly into the Zo automation layer as a cross-session memory store for scheduled agents and skills, and it is a natural fit for the robinhood-trading-bot (persist strategy tuning, market notes, and session state across daily runs). The TypeScript/Bun stack matches the Zo and Skills ecosystem, Apache-2.0 is permissive, and the agent-surface breadth means it can sit behind multiple Zo personas without rework. Self-host the daemon on the Zo server; the Claude Code / Codex hooks are the entry point to validate first, then extend to the Zo automation channel.

**Non-repo links mentioned**

- **grok-mem.ai** — a companion product to Claude Mem (same author, thedotmack). The only associated GitHub repo is `thedotmack/grok-mem`, which is a 1★ static marketing site (HTML, last pushed 2026-09-03), not a substantive codebase. No eval; SKIP as a repo, but the product itself is part of the same memory ecosystem and worth watching.
