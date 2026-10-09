# NewsJack — This GitHub Repo Turns Your AI Into a PR Manager

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-08T20:30:23+00:00
- **Video**: https://www.youtube.com/shorts/vsHEX2YVNHM

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=hlOk-EFUITQ

NewsJack is an open-source set of skills that turns your AI agent into a full PR team. It watches the news for stories you can ride, finds the angle, checks which reporters actually cover that topic, and roasts your pitch before you send it. It's getting a lot of attention this week because of how quickly and cheaply a new small model can make the decisions behind it, like judging whether a story fits one client or another, in a fraction of the time and for pennies compared to Opus 5. Cheap, fast models like this make it practical to build tools that used to be too complicated or expensive to bother with.

#NewsJack #PR #AIAgents #OpenSource #AITools #GitHub

🔗 GitHub: https://github.com/elvisun/newsjack
🔗 Website: https://newsjack.sh/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=vsHEX2YVNHM! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8434★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **elvisun/newsjack** — 1528★ · Go · pushed 2026-10-07 · license MIT
  - The open-source skills that turn your agent into a full PR team.
  - https://github.com/elvisun/newsjack

## Eval

### elvisun/newsjack — https://github.com/elvisun/newsjack
Functionality: Open-source agent skills (Claude Code-style SKILL.md packs plus a Go CLI) that turn an AI agent into a full PR team: it monitors the news for stories you have standing to ride, generates angles, researches which reporters actually cover the topic, drafts and roasts the pitch, and tracks coverage.
Signals: 1,528 stars; Go; MIT; created 2026-05-19; pushed 2026-10-07; active, not archived; 154 forks; homepage newsjack.sh.
Recommendation: **INCLUDE** — MIT-licensed skills map one-to-one onto this Skills repo. Three are already adapted here (pr-strategist, newsworthiness-check, news-search, installed 2026-09-26); the remaining coverage-tracker, media-list, and pitch-roast skills plug into the publishing pipeline and any client PR desk. Live news search, PR calendar, and journalist enrichment require a free Medialyst account; core skills run local-first without it.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api
Functionality: Python library that fetches YouTube transcripts/subtitles without an API key or headless browser.
Signals: 8,434 stars; Python; MIT; pushed 2026-09-10; active, not archived.
Recommendation: **N/A-repo** — not presented in the video; this is the watcher's own transcript-fetching dependency, auto-extracted from the report's transcript-error text. Kept for the record only.
