# 9 things you’ll actually do with Jev

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-26T18:00:06+00:00
- **Video**: https://www.youtube.com/watch?v=pxaMzr7al3I

## Description

Resources: https://thenextnewthing.ai/l/jev-reaction-sept26
Presented by Zapier: https://zapier.com/
Andrew Warner breaks down the most useful real-world ways people are using Jev for fast, cheap decision-making.

Andrew Warner reviews the best Jev demos and use cases he found across YouTube, focusing on where the model is actually useful: classifying email, routing tasks between models, triaging support tickets, qualifying leads, searching agent memory, scoring video clips, controlling smart-home actions, and filtering content ideas. The bigger idea is that Jev is not a general-purpose writing model — it works best as a fast decision engine that returns probabilities and makes constrained choices cheaply enough to sit inside larger agent workflows.

Links featured:

Nate Herk — https://www.youtube.com/watch?v=ymgH8jS6Wb8&t=515s
Lukas Margerie —  https://www.youtube.com/watch?v=ZZcI9Bfe8AM&t=156s
Nate Herk —  https://www.youtube.com/watch?v=ymgH8jS6Wb8&t=328s
Mayank Aggarwal —  https://www.youtube.com/watch?v=d9lCIVc5AyU&t=634s
David Ondrej —  https://www.youtube.com/watch?v=f6We53TnkbU&t=772s
Jay E —  https://www.youtube.com/watch?v=tTnUcSj-QPA&t=305s
Moritz —  https://www.youtube.com/watch?v=Nq_lu5QT-fI&t=693s
Greg Isenberg —  https://www.youtube.com/watch?v=4mTLpuQpB80&t=1443s
Matthew Berman —  https://www.youtube.com/watch?v=2z-7pIj57f8&t=391s
Nate Herk —  https://www.youtube.com/watch?v=ymgH8jS6Wb8&t=597s
Moritz —  https://www.youtube.com/watch?v=Nq_lu5QT-fI&t=359s
Syntax —  https://www.youtube.com/watch?v=QbYBRjOaGOo&t=940s
Eric Siu —  https://www.youtube.com/watch?v=fdsJT0BCkvA&t=183s
Eric Siu —  https://www.youtube.com/watch?v=B9QCiV9MN6A&t=196s
Greg Isenberg —  https://www.youtube.com/watch?v=4mTLpuQpB80&t=1371s

00:00 - Jev: See why the model is built for fast, cheap decisions instead of writing.
00:36 - Email Categorization: Sort 500 emails and identify which ones need a response.
01:30 - Setup: Connect Jev to Codex, Claude Code, GrokBot, or another agent using TypeSafe AI.
02:42 - Voice-Controlled Browser: Build a browser that reacts to spoken commands in real time.
04:39 - How Jev Works: Turn decisions into multiple-choice and yes-or-no questions with probability scores.
07:12 - Zapier + Jev: Use Jev inside Zapier workflows for inexpensive, high-speed decisions.
08:15 - Model Routing: Automatically decide which tasks need an expensive model and which can use a cheaper one.
09:27 - Customer Support Triage: Route support tickets to automation or a human based on urgency.
11:15 - Lead Qualification: Score form submissions instantly and decide who should get a Calendly link.
14:06 - Agent Memory: Search large folders of Markdown memory with fewer tokens and lower cost.
18:09 - Video Clip Scoring: Analyze a transcript and rank the strongest moments for short-form clips.
19:30 - Smart Home Control: Use Jev for near-instant decisions behind Home Assistant actions.
21:00 - GrokBot + Jev: Filter content ideas inside a long-running agent without burning through expensive model usage.
23:33 - Where Jev Fails: See why it should not be trusted blindly for trading or other high-stakes predictions.

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=pxaMzr7al3I! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8382★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### jdepoix/youtube-transcript-api

- **Functionality:** Python library for retrieving manually created and automatically generated YouTube captions without an API key or browser automation. It is the transcript retrieval dependency used by this watcher.
- **Signals:** 8,382 stars; Python; MIT license; last push 2026-09-10; not archived. The current run still hit YouTube's cloud IP blocking, so operational reliability from this server is the limiting factor.
- **Recommendation: INCLUDE** — keep it as the watcher's transcript backend in `Skills/next-new-repo-watch/`. Add a browser or alternate transcript fallback later if missed videos become a recurring problem; do not treat this dependency alone as sufficient coverage.

### Other tools mentioned

The video discusses Jev, TypeSafe AI, Zapier, Home Assistant, and several hosted/model workflows, but the available description and transcript contain no additional public GitHub repository identities. No repository identity was invented for those products.

- **Functionality:** Named products only — Jev (agent memory layer), TypeSafe AI, Zapier, and Home Assistant are commercial or hosted offerings, not open repositories installable on this host.
- **Signals:** No GitHub repository was presented in the description or transcript, so there are no stars, language, license, or push signals to report.
- **Recommendation: SKIP** — nothing installable was named, and inventing a repository identity would be a guess. Revisit only if a future episode links an actual public repo.
