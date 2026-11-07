# CLIProxyAPI — This Proxy Keeps Your AI Coding Agents Logged In Forever

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-11-06T21:30:07+00:00
- **Video**: https://www.youtube.com/shorts/4M-ZFI_EbEU

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=Wsru44p-J14  

CLIProxyAPI is an open-source proxy server that sits between your local coding agents and the Claude, Codex, and other model APIs. It does two big things. First, it automatically re-logs you in: about every 10 minutes it checks whether your session is about to expire and renews it before it does, so you never get booted out mid-task. Second, if you have multiple coding accounts, it can balance them for you, so one setup can serve several computers sharing accounts. It works with OpenAI-, Gemini-, and Claude-compatible clients and SDKs, and it runs locally. If you’re tired of constantly logging back in to your coding agents, this takes care of it for you.

Check the terms of each AI provider before sharing or combining accounts.

#CLIProxyAPI #AIAgents #AICoding #ClaudeCode #Codex #OpenSource #AITools 

🔗 GitHub: https://github.com/router-for-me/CLIProxyAPI
🔗 Docs: https://help.router-for.me/introduction/what-is-cliproxyapi

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=4M-ZFI_EbEU! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **router-for-me/CLIProxyAPI** — 57849★ · Go · pushed 2026-11-07 · license MIT
  - Wrap Antigravity, ChatGPT Codex, Claude Code, Grok Build, Muse Code, Devin as an OpenAI/Gemini/Claude/Codex compatible API service, allowing you to enjoy the free Gemini Series, GPT Series, Grok Series, Claude model through API
  - https://github.com/router-for-me/CLIProxyAPI

## Agent eval

Transcript unavailable (YouTube blocked the cloud IP); eval based on the video description and GitHub metadata.

### router-for-me/CLIProxyAPI — https://github.com/router-for-me/CLIProxyAPI
- Functionality: Local Go proxy that exposes OpenAI/Gemini/Claude-compatible endpoints and re-authenticates logged-in coding-agent sessions (Claude Code, ChatGPT Codex, and others) so they stay logged in. It can also pool multiple accounts.
- Signals: 57,849★ · Go · MIT · pushed 2026-11-07 · active.
- Recommendation: **SKIP** — It works by routing subscription OAuth sessions through a third-party proxy, which puts account credentials in an intermediary and likely breaks provider terms for account pooling. Zo already has native Claude Code and Codex providers (Settings → AI → Providers), so there is no gap to fill.
