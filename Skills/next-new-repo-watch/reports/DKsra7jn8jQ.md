# FreeLLMAPI – Access Free AI Models With Automatic Switching

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-30T20:30:17+00:00
- **Video**: https://www.youtube.com/shorts/DKsra7jn8jQ

## Description

More free AI tools: https://thenextnewthing.ai/Resources

What if you could dramatically reduce your AI subscription costs using free AI models?

Andrew pays $200/month for Claude, but not every AI task needs an expensive subscription.

FreeLLMAPI brings together free AI models from different providers, automatically switching between them when your free credits run out. That means you can keep your AI agents working without relying entirely on expensive subscriptions.

Andrew interviewed the founder to find out how it works and whether it could actually help eliminate AI subscription costs.

🎥 Watch the full episode featuring 7 free alternatives to paid AI tools:
https://youtu.be/7rVTo_sy4Po

🎙️ Watch Andrew's interview with the founder of FreeLLMAPI:
https://youtu.be/ANJTdT0Ggrw

#FreeLLMAPI #ClaudeCode #AITools #FreeAI #OpenSource

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=DKsra7jn8jQ! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

(none auto-extracted — read the transcript above and identify repo names, then search GitHub)

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

**Evidence note:** Transcript blocked (YouTube IP block from cloud host). The eval uses the show notes and GitHub search results. The video names FreeLLMAPI without a link, so the repo was matched by name.

### tashfeenahmed/freellmapi — https://github.com/tashfeenahmed/freellmapi
- Functionality: One OpenAI-compatible `/v1` endpoint that routes requests across about 34 free LLM providers, with failover and encrypted keys.
- Signals: 44,961★ · TypeScript · MIT · pushed 2026-10-31 · not archived. The README says "Personal experimentation only."
- Recommendation: **TRIAL** — sandbox only, with no real provider keys. Confirm each underlying provider's free-tier terms before any production use, because many prohibit aggregation. Note that this workspace already has a `freellmapi/` folder, which leaked provider keys into `jaknyfe-skills` history on 2026-09-06. Any run must keep keys in gitignored env files or Settings > Advanced. Effort: about 1 hour.

Unofficial mirrors (`Srvankit/freellmapi`, `sunsky89757/freellmapi`, `nglmercer/freellmapiV2`) were not evaluated; they are forks or low-star copies.

Overall: TRIAL for tashfeenahmed/freellmapi. No INCLUDE repos in this video.
