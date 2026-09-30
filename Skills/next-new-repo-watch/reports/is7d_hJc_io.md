# Context-Mode — The Fix for AI Coders That Forget Mid-Task

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-29T20:30:14+00:00
- **Video**: https://www.youtube.com/shorts/is7d_hJc_io

## Description

Context-Mode already has 23,000 GitHub stars, and it's solving a real problem — your AI coding agent forgetting things or burning tokens midway through a task. It works by spinning up a disposable side sandbox: instead of your main session loading a bunch of files, making tool calls, and stumbling toward the right answer, that messy digging happens in the sandbox. Once it finds the answer, it hands it straight to your main Claude or Codex session — clean, already vetted — and the sandbox conversation gets thrown away. That keeps your main conversation focused on the actual work instead of all the side digging, with up to a 98% reduction in tool output clutter.

#ContextMode #ClaudeCode #AIAgents #DevTools #OpenSource

🔗 GitHub: https://github.com/mksglu/context-mode
🔗 Website: https://context-mode.com/

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=is7d_hJc_io! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8405★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **mksglu/context-mode** — 24300★ · TypeScript · pushed 2026-09-30 · license NOASSERTION
  - Context window optimization for AI coding agents. Sandboxes tool output (98% reduction), persists session memory, and   enforces routing across 17 platforms via MCP + hooks.
  - https://github.com/mksglu/context-mode

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### mksglu/context-mode
Functionality: TypeScript tooling for AI coding agents that routes exploratory work into disposable sandboxes, persists useful context, and reduces tool-output clutter before returning a distilled result to the main session.
Signals: 24,300 stars; TypeScript; Other/nonstandard license metadata; last push 2026-09-30; active, not archived.
Recommendation: **TRIAL** — run it in an isolated environment against the Zo/Codex workflow and measure context reduction, tool compatibility, persistence, and security boundaries. Effort: 1 day.

### jdepoix/youtube-transcript-api
Functionality: Python library for retrieving manually created and automatically generated YouTube subtitles without an API key or browser automation.
Signals: 8,405 stars; Python; MIT; last push 2026-09-10; active, not archived.
Recommendation: **SKIP** — this is the watcher's existing transcript dependency, and the current host is blocked by YouTube.

## Overall verdict
Context-Mode is worth a controlled sandbox trial because it directly targets the context and tool-output problem in this environment. The transcript was unavailable because YouTube blocked the fetch from this host; repo identity came from the video description and auto-extracted links.
