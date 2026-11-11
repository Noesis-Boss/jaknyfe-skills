# Claude-Mem Gives Your AI Agent a Memory You Can Control

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-11-10T15:30:06+00:00
- **Video**: https://www.youtube.com/shorts/yuz3VbdQm5M

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=Wsru44p-J14

Claude-Mem is an open-source tool that helps your AI agent remember. It captures what your agent does during sessions, compresses it with AI, and feeds the relevant context back into future sessions. It’s similar to what people who use OpenClaw and Hermes already do: keeping their own memory files, with a new markdown file each day logging what they did. Claude-Mem does the same for Grokbot. Grokbot already has a good memory layer, but it can be hard to customize, so this lets you store your daily activity and have the agent pull it up when it needs it. It also works with other agents, including Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, and OpenCode. If your agent keeps forgetting what it did yesterday, this is worth a look.

#ClaudeMem #AIAgents #AIMemory #ClaudeCode #OpenClaw #OpenSource #AITools 

🔗 GitHub: https://github.com/thedotmack/claude-mem
🔗 Website: https://cmem.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=yuz3VbdQm5M! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **thedotmack/claude-mem** — 116038★ · TypeScript · pushed 2026-11-11 · license Apache-2.0
  - Persistent Context Across Sessions for Every Agent –  Captures everything your agent does during sessions, compresses it with AI, and injects relevant context back into future sessions. Works with Claude Code, OpenClaw, Codex, Gemini, Hermes, Copilot, OpenCode + More
  - https://github.com/thedotmack/claude-mem

## Agent eval

Transcript unavailable (YouTube IP block); evaluated from the description.

### thedotmack/claude-mem — https://github.com/thedotmack/claude-mem

- **Functionality:** Captures agent session activity, compresses it with AI, and injects relevant context into future sessions across Claude Code, Codex, Gemini, Hermes, and others.
- **Signals:** 116,038★ · TypeScript · Apache-2.0 · pushed 2026-11-11 · not archived
- **Recommendation: SKIP** — duplicates the existing memory stack (astra-memory, zobodhi-memory, Zorro's AstraDB store). A second memory store creates conflicting sources of truth, and it installs its own hooks into Claude Code.

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->
