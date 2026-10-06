# Top repo explained: builds product + lands customers

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-05T22:24:12+00:00
- **Video**: https://www.youtube.com/watch?v=BcNAQynKUk4

## Description

Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Andrew Warner sits down with Affaan Mustafa to explore ECC, an open-source toolkit that helps turn ideas into products using structured AI coding workflows, research, testing, marketing, and user feedback.

Affaan demonstrates how ECC can take an idea, plan and build a prototype, run tests, create marketing videos, identify potential customers, and send highly targeted outreach. He explains how ECC combines deterministic engineering workflows with AI agents, including planning, test-driven development, specialized skills, orchestration, and deep research. The conversation also covers how ECC evolved beyond Claude Code, why Affaan built it around repeatable engineering practices, how users can chain skills together, and how the open-source community has contributed hundreds of specialized skills.

Links featured:

- ECC: https://github.com/affaan-m/ECC
- ECC Tools: https://ecc.tools/

00:00 - ECC: Build products with AI workflows
00:39 - Orchestrator: Build products using ECC skills
01:29 - Roast Your Idea: Analyze startup pitches
02:47 - 1Password: Securely manage environment credentials
03:21 - Tmux: Run multiple agent panes
03:57 - Orchestrator: Monitor parallel agents efficiently
04:31 - Claude Code: Fix failing tests automatically
06:29 - ECC: Reduce startup time significantly
07:30 - ECC Skills: Apply engineering workflows consistently
08:14 - ECC: Chain skills into complete workflows
09:03 - Roast Your Idea: Get real user feedback
10:05 - User Feedback: Iterate before scaling products
12:14 - X Network: Find targeted potential customers
13:29 - ECC: Personalize outreach using private context
14:17 - Marketing Video: Create targeted product promotion
15:28 - ECC: Expand beyond Claude Code
16:01 - Planning: Research and refine ideas
16:48 - Sub-Agents: Build detailed product specifications
17:31 - X Outreach: Send targeted customer messages
18:03 - ECC: Send personalized product outreach
18:51 - Open Source: Share and improve workflows
19:25 - ECC: Grow through community contributions

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=BcNAQynKUk4! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8422★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **affaan-m/ECC** — 273963★ · JavaScript · pushed 2026-10-05 · license MIT
  - The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.
  - https://github.com/affaan-m/ECC

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### affaan-m/ECC

Functionality: ECC is a large collection of agent skills, workflows, and operating practices for turning an idea into a researched, tested, and shipped product. It targets several coding-agent runtimes and includes orchestration, planning, testing, research, marketing, and outreach workflows.

Signals: 273,963 stars; JavaScript; MIT; last pushed 2026-10-05; active, not archived.

Recommendation: TRIAL — sandbox the smallest useful subset in a disposable project and test skill compatibility, scope control, secret handling, and whether its agent orchestration duplicates Zo skills. Do not install the full bundle into the live workspace; rough effort: 2–4 hours.

### jdepoix/youtube-transcript-api

Functionality: Python library for retrieving manually created and auto-generated YouTube subtitles without an API key or browser automation. It is the dependency used by this watcher and was extracted from the transcript error text, not clearly presented as a tool in the episode.

Signals: 8,422 stars; Python; MIT; last pushed 2026-09-10; active, not archived.

Recommendation: SKIP — already present as the watcher's documented dependency; no separate installation or adaptation is needed.
