# This Free GitHub Tool Lets You Charge Per Token

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-30T20:30:02+00:00
- **Video**: https://www.youtube.com/shorts/wgdFn5JXXb8

## Description

Autumn lets you add usage-based pricing to your app, including per-token, per-request, and per-minute billing. Andrew also compares it with Chargebee and explains why it can be useful for AI apps.

🔗 GitHub: https://github.com/useautumn/autumn
🔗 Website: https://useautumn.com/

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://youtu.be/kMPyFWFqX5I

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=wgdFn5JXXb8! This is most likely caused by:

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
- **useautumn/autumn** — 2750★ · TypeScript · pushed 2026-10-01 · license Apache-2.0
  - Autumn is an open-source pricing & billing platform
  - https://github.com/useautumn/autumn

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### jdepoix/youtube-transcript-api

**Functionality:** Python library for retrieving manually created and auto-generated YouTube captions without an API key or browser automation. It is the dependency the watcher uses to fetch transcripts, rather than the subject of this video.

**Signals:** 8,406 stars; Python; MIT License; last push 2026-09-10; active, not archived.

**Recommendation: SKIP** — already used by this watcher and adds no new capability to Don’s projects; the current transcript failure is YouTube/IP blocking, not a missing repository feature.

### useautumn/autumn

**Functionality:** TypeScript usage-based billing platform for metering and charging by tokens, requests, minutes, or other units. It targets AI products that need entitlements, usage tracking, and subscription or credit-based pricing.

**Signals:** 2,750 stars; TypeScript; Apache License 2.0; last push 2026-10-01; active, not archived.

**Recommendation: TRIAL** — test it in a disposable Zo Site or SaaS-Mailer-style billing prototype with Stripe test mode; verify token-meter accuracy, webhook retries, plan changes, idempotency, and whether its deployment model fits Bun. Rough effort: 3–6 hours. It could later support metered AI features, but payment and entitlement logic needs a controlled trial before adoption.
