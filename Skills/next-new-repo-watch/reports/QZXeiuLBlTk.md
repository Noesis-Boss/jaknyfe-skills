# This Tool Feeds All Your Business Data to One AI Agent

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-16T20:30:31+00:00
- **Video**: https://www.youtube.com/shorts/QZXeiuLBlTk

## Description

Supernova acts as the glue between all your business tools — Stripe and everything else — pulling all that data into a single data lake and making it accessible to Claude, Codex, or your agent of choice via MCP. Instead of your agent having to query one tool at a time, everything lives in one place it can pull from directly. And if there's a connector for a tool you use that they don't have yet, they claim they can build it for you in 24 hours. Genuinely useful piece of infrastructure, and I think we're going to see a lot more tools like this pop up.

#Supernova #AIAgents #MCP #DataPipeline #DevTools 

🔗 Website: https://supernova.ai/ 

Link to the full video: https://www.youtube.com/watch?v=klqyY5SAQvc

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=QZXeiuLBlTk! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8342★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### jdepoix/youtube-transcript-api

**Functionality:** Python library for retrieving manual and auto-generated YouTube subtitles without a browser or API key. It is the transcript dependency already used by this watcher.

**Signals:** 8,342 stars; Python; MIT; last push 2026-09-10; active; not archived.

**Recommendation: INCLUDE** — retain as the transcript backend for the watcher. YouTube blocked transcript retrieval from this server IP during this run.

**Identity uncertainty:** No transcript was available; the repo was auto-extracted and is a watcher dependency.
