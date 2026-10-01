# WeKnora — Tencent Built an AI That Turns Your Files Into a Wiki

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-30T23:00:16+00:00
- **Video**: https://www.youtube.com/shorts/Ie6IlSIYAfc

## Description

WeKnora is Tencent's open-source knowledge platform — think Obsidian, RAG, AI, and a graph database all rolled into one. It automatically figures out how your files relate to each other (say, noticing something in your downloads folder connects to an existing project) and builds out a navigable knowledge graph and wiki on its own. You can click through your own documents the way you'd click through Wikipedia links, with the system doing the organizing and retrieval work behind the scenes. Genuinely impressive way to make sense of everything scattered across your computer.

#WeKnora #Tencent #RAG #KnowledgeGraph #OpenSource

🔗 GitHub: https://github.com/Tencent/WeKnora
🔗 Website: https://weknora.weixin.qq.com/

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=Ie6IlSIYAfc! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8406★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **Tencent/WeKnora** — 31596★ · Go · pushed 2026-10-01 · license NOASSERTION
  - Open-source LLM knowledge platform: turn raw documents into a queryable RAG, an autonomous reasoning agent, and a self-maintaining Wiki.
  - https://github.com/Tencent/WeKnora

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### jdepoix/youtube-transcript-api

**Functionality:** Python library for retrieving manually created and auto-generated YouTube captions without an API key or browser automation. It is the dependency the watcher uses to fetch transcripts, rather than the subject of this video.

**Signals:** 8,406 stars; Python; MIT License; last push 2026-09-10; active, not archived.

**Recommendation: SKIP** — already used by this watcher and adds no new capability to Don’s projects; the current transcript failure is YouTube/IP blocking, not a missing repository feature.

### Tencent/WeKnora

**Functionality:** Go-based open-source knowledge platform that turns documents into a queryable RAG system, reasoning agent, and self-maintaining wiki. It is aimed at organizing a document corpus into linked, searchable knowledge.

**Signals:** 31,596 stars; Go; repository reports “Other” license; last push 2026-10-01; active, not archived.

**Recommendation: TRIAL** — sandbox it against a copy of `memory/` and selected publishing research notes; test local deployment, document ingestion, citation quality, graph navigation, model configuration, and resource use. Rough effort: 2–4 hours for a disposable evaluation; do not connect production credentials or live workspace data until its license and data-handling behavior are verified.
