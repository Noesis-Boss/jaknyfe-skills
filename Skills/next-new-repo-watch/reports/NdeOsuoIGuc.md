# Have Astra do this right now

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-12T14:00:13+00:00
- **Video**: https://www.youtube.com/watch?v=NdeOsuoIGuc

## Description

Resources: https://thenextnewthing.ai/l/astra-reaction-sep12
Presented by Zapier: https://zapier.com/
Andrew Warner breaks down the best real-world GPT-6 Astra use cases and how it compares with Fable 5.1.

Andrew Warner tests where GPT-6 Astra actually stands out by reviewing real-world demos from Riley Brown, Jason Lee, Claire Vo, Matthew Berman, Mark Kashef, Creator Magic, Nate Herk, and Dan Shipper. The episode covers app building, browser and computer control, iPhone automation, DaVinci Resolve editing through MCP, meeting analysis, writing, and presentation creation, while comparing Astra with Fable 5.1 on quality, speed, cost, and practical usefulness.

Links featured:

Riley Brown — https://www.youtube.com/watch?v=Ju41cQSe7hY&t=489s
Jason Lee — https://www.youtube.com/watch?v=hjAugywVkOw&t=1180s
Claire Vo (How I AI) — https://www.youtube.com/watch?v=AniiF8rOu9c&t=350s
Matthew Berman — https://www.youtube.com/watch?v=xdXLzFzxA9Q&t=706s
Mark Kashef — https://www.youtube.com/watch?v=tU-fO6cADvQ&t=836s
Creator Magic — https://www.youtube.com/watch?v=V7CtHz8JFWA&t=510s
Nate Herk — https://www.youtube.com/watch?v=WfJPBVXPt8k&t=865s
Dan Shipper (Every) — https://www.youtube.com/watch?v=1EEw36H2zLo&t=73s

00:00 - GPT-6 Astra: Andrew breaks down the best real-world use cases he found after testing Astra and watching hours of demos.
00:27 - Raycast-Style App: Build a custom desktop utility from a simple prompt in under 20 minutes.
01:39 - $60K/Month App Clone: Replicate a receipt-scanning bookkeeping app using GPT-6 Astra and Fable 5.1.
02:51 - GPT-6 Astra App Build: Scan receipts, extract data with Claude, and generate a polished working app from one prompt.
04:12 - Fable 5.1 App Build: Compare Fable’s version of the same receipt-scanning app against Astra.
06:18 - Computer Use: Let GPT-6 Astra take over Chrome and modify a complex browser-based workflow hands-free.
07:39 - Zapier MCP: Connect AI agents to thousands of apps while controlling what they can access and change.
08:42 - Browser Control: Use GPT-6 Astra to draw in Excalidraw, research products, and plan routes in Google Maps.
10:12 - iPhone Control: Control an iPhone through Mac’s iPhone Mirroring using GPT-6 Astra.
12:00 - DaVinci Resolve MCP: Connect GPT-6 Astra directly to DaVinci Resolve for faster AI-powered video editing.
15:18 - AI Video Editing: Turn more than 150GB of event footage into a finished recap with GPT-6 Astra and Fable 5.1.
19:12 - Meeting Analysis: Analyze dozens of meetings to uncover business problems and automation opportunities.
22:12 - AI Writing: See why Dan Shipper considers GPT-6 Astra a strong writing model.
24:09 - Consulting Decks: Compare GPT-6 Astra and Fable 5.1 creating a McKinsey-style presentation from the same prompt.
27:27 - GPT-6 Astra vs Fable 5.1: Andrew gives his overall verdict on computer use, writing, design, speed, and cost.

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=NdeOsuoIGuc! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8319★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api

## Agent eval

The transcript could not be retrieved because YouTube blocked the server IP. The description and chapters identify products and demonstrations, but no additional open-source repository besides the transcript tool itself. Closed products and model names are not counted as repositories.

### jdepoix/youtube-transcript-api

- **Functionality**: Python library for retrieving YouTube captions, including automatically generated subtitles, without an API key or browser automation. It is the dependency used by this watch skill to fetch video transcripts.
- **Signals**: 8,319 stars; Python; MIT; last push 2026-09-10; not archived.
- **Recommendation**: **INCLUDE** — keep it as the transcript dependency for `Skills/next-new-repo-watch/`; it is already the correct fit for the existing Python scan pipeline. The current run installed it successfully, but YouTube still blocked this server IP, so transcript fetches need a proxy or another retrieval fallback.
