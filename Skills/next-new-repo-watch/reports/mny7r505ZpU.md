# He Built an Agent That Calls Customers

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-21T18:34:32+00:00
- **Video**: https://www.youtube.com/shorts/mny7r505ZpU

## Description

Achint shows GrokBot making a real outbound sales call, qualifying a lead, and moving them toward a booked meeting. The full episode breaks down how the system works and how to set it up step by step.

Link to the full video: https://youtu.be/WPUAZm5rnGc

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=mny7r505ZpU! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8353★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Transcript retrieval was blocked by YouTube for this run. The description identifies a hosted outbound voice-agent stack but no public GitHub repository.

### Hosted GrokBot / ElevenLabs / Twilio / Netlify / Attio stack

Functionality: The system calls unbooked leads, qualifies them, sends a calendar link, and writes conversation context into a CRM for human follow-up. These are hosted products and services rather than repositories that can be installed in the Skills repo.

- Signals: No public repository identified; product and service names only.
- Recommendation: **SKIP** — no repo to install or adapt, and outbound calling, voice cloning, CRM writes, and lead data require a separate consent, privacy, and cost review before any Zo automation trial.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without an API key or browser automation. It is the transcript backend used by this watcher.

- Signals: 8,353 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency.
