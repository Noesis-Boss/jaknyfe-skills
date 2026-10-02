# Invoice Ninja: Stop Chasing Clients for Payment

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-01T23:00:40+00:00
- **Video**: https://www.youtube.com/shorts/g-CG1PD7iTc

## Description

Andrew explains how he avoids awkward payment follow-ups by letting Invoice Ninja handle the chasing. He also shares why service businesses should consider switching to auto-billing.

🔗 GitHub: https://github.com/invoiceninja/invoiceninja
🔗 Website: https://invoiceninja.com/

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://youtu.be/kMPyFWFqX5I

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=g-CG1PD7iTc! This is most likely caused by:

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
- **invoiceninja/invoiceninja** — 10199★ · PHP · pushed 2026-10-01 · license NOASSERTION
  - A source-available invoice, quote, project and time-tracking app built with Laravel
  - https://github.com/invoiceninja/invoiceninja

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Evaluated 2026-10-02 for this environment: Bun/TypeScript + Python, Zo automations, the trading bot, publishing, and the Skills repository.

### invoiceninja/invoiceninja — https://github.com/invoiceninja/invoiceninja
Functionality: A self-hostable Laravel application for invoicing, quotes, projects, time tracking, and payment collection. It fits service businesses that need recurring billing and automated payment reminders.
- Signals: 10,199 stars · PHP · no declared SPDX license (NOASSERTION) · last push 2026-10-01 · active, not archived.
- Recommendation: **TRIAL** — run a sandbox instance and test invoice creation, recurring billing, payment reminders, export, and webhook/API integration with Noesis client operations; rough effort 1–2 days. Its source-availability and licensing need review before any production adoption.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api
Functionality: A Python library that retrieves manually created and auto-generated YouTube subtitles without an API key or browser automation. It was used by this watcher to attempt transcript retrieval; it was not a product featured in the video.
- Signals: 8,411 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **SKIP** — keep it as the watcher's existing dependency; it is not an adoption candidate for the trading bot, Zo automations, or publishing pipeline, and YouTube blocking caused this run's transcript fetches to fail.
