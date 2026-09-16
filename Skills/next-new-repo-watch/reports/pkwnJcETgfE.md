# Amazing: FREE AI Agent from Meta

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-15T23:15:18+00:00
- **Video**: https://www.youtube.com/watch?v=pkwnJcETgfE

## Description

Link to Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Andrew Warner and Michael Galpert take an inside look at Muse, Meta’s new AI agent with its own computer, and explore what it can actually do across Instagram, Facebook, WhatsApp, web browsing, and everyday workflows.

Andrew sits down with Michael Galpert, an early OpenClaw user, to test Muse and see how far its agent capabilities go. Michael demonstrates how Muse can access Instagram data, export information into an Excel file, visualize relationships between followers, manage messages, and work with Meta’s ecosystem in ways that other AI agents often cannot. They explore Muse’s human-in-the-loop approval system, persistent memory, identity and personality settings, side chats, connectors, and its ability to communicate through channels like WhatsApp. Muse can also operate a cloud computer, open a browser, research products, and let users take control when needed.

The conversation also explores where Muse shines—and where it still falls short. Michael explains why the agent is particularly useful for people working with Facebook Marketplace, Facebook Ads, and Instagram, while Andrew and Michael test its ability to connect tools that don't have a built-in integration. They discuss Tailscale access to other computers, security and anti-spam protections, limitations with websites like Costco, and the difference between having one persistent agent versus multiple specialized agents. They also explore Muse’s personalized feeds and Ideas tab, which can suggest useful automations based on what the agent knows about you. After using Muse for several days, Michael shares why he sees it as a serious contender for how people may interact with AI agents in the future.

Links featured:

Muse — https://www.muse.ai/
OpenClaw — https://openclaw.ai/
Tailscale — https://tailscale.com/
Zapier SDK — https://zapier.com/sdk

00:00 - Introducing Muse
00:19 - Exporting Instagram Followers
01:38 - What Makes Muse Different
02:00 - Messaging on Facebook & Instagram
02:46 - Inbox, Memory & Agent Identity
03:25 - Human Approval for Messages
04:05 - Bulk Messaging
04:29 - Muse's Personality & Memory
05:11 - One Persistent Agent + Side Chats
06:12 - Muse's Connectors
07:34 - A Free Computer in the Cloud
07:53 - Using Muse Through WhatsApp
08:57 - Muse Controls a Web Browser
10:29 - Connecting Tools Without Built-In Integrations
11:20 - Creating Connectors on the Fly
12:51 - How Fast Is Muse?
13:18 - What Muse Is Good For
13:33 - Muse for Facebook & Instagram
14:27 - Security & Privacy
15:10 - Where Muse Still Falls Short
15:47 - One Agent vs. Multiple Personalities
16:17 - Trying Agents for Free
16:42 - Muse's Personalized Feeds
18:02 - Muse's Ideas Tab
18:47 - Michael's Muse Hot Take

Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=pkwnJcETgfE! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8337★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api

## Agent eval

Transcript retrieval was blocked by YouTube, so repo identity below is based on the video description and featured links. No additional repository could be confirmed from the unavailable transcript.

### `openclaw/openclaw`

Functionality: An open-source personal AI agent that can operate across local computers, browsers, messaging channels, and connected tools. It is the closest GitHub project match for the OpenClaw product named in the description.

Signals: 389,835 stars; TypeScript; license metadata reports `Other`; last push 2026-09-16; active and not archived.

- Recommendation: **TRIAL** — sandbox it outside production and test the approval gates, credential isolation, browser actions, and channel integrations against Zo’s existing automations. Agent shell and browser access create a meaningful security boundary; allow 2–4 hours for a contained evaluation.

### `zapier/zapier-platform`

Functionality: Zapier’s JavaScript toolkit for building custom integrations and actions. It could support a narrow connector needed by the publishing or marketing-channel pipeline when no native integration exists.

Signals: 554 stars; JavaScript; license metadata reports `Other`; last push 2026-09-16; active and not archived.

- Recommendation: **TRIAL** — build one read-only connector against a low-risk marketing workflow and measure setup time, auth handling, and maintenance burden before adopting it broadly. Rough effort: 1–2 hours.

### `jdepoix/youtube-transcript-api`

Functionality: Python library for retrieving YouTube captions, including auto-generated subtitles, without an API key or browser automation. The watcher already uses it for transcript retrieval.

Signals: 8,337 stars; Python; MIT; last push 2026-09-10; active and not archived.

- Recommendation: **SKIP** — it is already the implementation dependency of `Skills/next-new-repo-watch`, and this run confirmed its operational weakness in this environment: YouTube blocked the transcript request.

### Named products without a confirmed repository

Muse (`muse.ai`), Tailscale (`tailscale.com`), and the Muse product itself were named as products or services, but no GitHub repository was identified from the available description. They remain pending transcript verification rather than receiving invented repo verdicts.
