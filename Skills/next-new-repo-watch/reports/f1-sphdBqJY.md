# This Free Tool Turns Your Browser Into a Spy Satellite

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-23T20:30:28+00:00
- **Video**: https://www.youtube.com/shorts/f1-sphdBqJY

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

God's Eye View pulls together publicly available open data — live traffic, CCTV camera feeds, planes overhead, and more — and displays it all on a stunning, zoomable, photorealistic 3D globe. Hover over a camera to see a snapshot, click in for a live view, and watch planes move overhead in real time. It genuinely feels unreal to interact with. If you don't want to set it up yourself through GitHub, there's also a simple downloadable app version (available on Pinokio) built by the creator, so you can just install it and start exploring.

#GodsEyeView #OpenData #SpatialIntelligence #OpenSource #DevTools

🔗 GitHub: https://github.com/bilawalsidhu/gods-eye-view
🔗 Website: https://maptheworld.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=f1-sphdBqJY! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8366★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **bilawalsidhu/gods-eye-view** — 42178★ · JavaScript · pushed 2026-09-24 · license NOASSERTION
  - A spy satellite simulator in your browser, except the data is real. Live open source spatial intelligence on a photorealistic 3D globe.
  - https://github.com/bilawalsidhu/gods-eye-view

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Transcript retrieval was blocked by YouTube for this run. The description identifies the featured repository directly.

### bilawalsidhu/gods-eye-view — https://github.com/bilawalsidhu/gods-eye-view

Functionality: A browser-based 3D globe that combines public live data such as traffic, cameras, and aircraft into an interactive spatial-intelligence view. It is primarily an exploration and visualization product rather than a reusable backend library.

- Signals: 42,178 stars · JavaScript · license not detected by GitHub metadata · last push 2026-09-24 · active, not archived.
- Recommendation: **SKIP** — impressive demo, but it has no clear connection to the trading bot, publishing pipeline, or Zo automations, and the missing license blocks safe adaptation into the Skills repo.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without a browser automation layer. It is the transcript backend used by this watcher.

- Signals: 8,366 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency; the current YouTube IP block is an operational limitation, not a reason to replace it.
