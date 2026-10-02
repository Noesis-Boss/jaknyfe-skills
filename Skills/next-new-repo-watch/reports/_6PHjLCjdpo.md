# WorkTrunk — Run Multiple AI Agents at Once Without Merge Conflicts

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-01T20:30:17+00:00
- **Video**: https://www.youtube.com/shorts/_6PHjLCjdpo

## Description

Worktrunk is an open-source CLI for Git worktree management, designed for parallel AI agent workflows. Instead of juggling branches and stashing changes, each AI agent gets its own clean worktree, so you can run several at once on the same repo without them stepping on each other. If you're working with AI coding agents, this makes your setup much easier to manage.

#WorkTrunk #Git #GitWorktree #AIAgents #AICoding #DevTools #OpenSource

🔗 GitHub: https://github.com/max-sixty/worktrunk
🔗 Website: https://worktrunk.dev/

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=_6PHjLCjdpo! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8411★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **max-sixty/worktrunk** — 8645★ · Rust · pushed 2026-10-02 · license NOASSERTION
  - Worktrunk is a CLI for Git worktree management, designed for parallel AI agent workflows
  - https://github.com/max-sixty/worktrunk

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Evaluated 2026-10-02 for this environment: Bun/TypeScript + Python, Zo automations, the trading bot, publishing, and the Skills repository.

### max-sixty/worktrunk — https://github.com/max-sixty/worktrunk
Functionality: A Rust CLI that manages Git worktrees so several coding agents can work in isolated checkouts of one repository. It reduces branch and stash collisions during parallel implementation and review.
- Signals: 8,645 stars · Rust · no declared SPDX license (NOASSERTION) · last push 2026-10-02 · active, not archived.
- Recommendation: **TRIAL** — test it in a disposable repository with two concurrent agent worktrees, dirty files, rebases, merge conflict handling, and cleanup; rough effort 2–4 hours. It could improve the Skills repository workflow, but the missing declared license and added CLI dependency prevent INCLUDE.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api
Functionality: A Python library for retrieving YouTube subtitles. It was auto-extracted by the watcher and was not presented as the subject of this video.
- Signals: 8,411 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **SKIP** — existing watcher dependency only; no new fit for the environment, and transcript requests were blocked by YouTube during this run.
