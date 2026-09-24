# New release: fewer tokens & reliable AI

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-23T19:37:09+00:00
- **Video**: https://www.youtube.com/watch?v=U6ptUFMyaJg

## Description

Link to Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Zapier X Post: https://x.com/zapier/status/2102829768332767453?s=20
Andrew Warner sits down with Zapier co-founder and CEO Wade Foster to show how Next Gen Zaps can make AI agents more reliable, reduce unnecessary token costs, and prevent agents from making expensive or unexpected mistakes.

Andrew shares two real-world examples of the problem: spending $264 in just two days because an AI agent repeatedly checked websites, and an agent that replaced his own video thumbnails in sponsor emails with thumbnails from other creators because it decided they would perform better. Wade explains how Next Gen Zaps solve this by combining deterministic automation with agentic decision-making, so agents can handle the parts that require judgment while predictable actions are “hardened” to run the same way every time.

Wade demonstrates the approach using a Granola-to-Google Drive workflow. The system checks for new meeting transcripts, uses AI to determine whether a transcript contains sensitive topics that should not be automatically shared, and then deterministically saves approved transcripts to Google Drive. He also walks through a fantasy football workflow that researches rosters, waiver wires, injuries, and trade opportunities, uses AI for the managerial decisions, and then sends Wade a consistent weekly report.

The episode breaks down exactly where AI should be probabilistic and creative—and where it should be deterministic, predictable, and locked down. Wade also explains how agentically managed workflows can recover from errors automatically, giving you the flexibility of AI without making every step dependent on an agent.

Links featured:

- Zapier — https://zapier.com/
- Zapier Next Gen Zaps / Early Access — http://zapier.com/workflow/early-access
- Zapier X Post: https://x.com/zapier/status/2102829768332767453?s=20

Timestamps:

00:00 Why AI Agents Make Expensive Mistakes
01:30 Introducing Zapier Next Gen Zaps
01:39 Granola + Google Drive Demo
02:24 Adding AI to a Deterministic Workflow
03:09 Deciding What Should Stay Private
03:54 How Next Gen Zaps Work Under the Hood
04:57 Why Deterministic Workflows Matter
05:42 Agentically Managed Workflows
06:45 Why Hardened Automation Is Useful
08:15 Fantasy Football AI Workflow
09:27 Using AI to Analyze a Fantasy League
10:48 Turning the Analysis Into a Weekly Workflow
12:00 The Weekly Waiver & Trade Report
13:30 What Is Agentic vs. Deterministic?
14:15 Where AI Makes the Decisions
15:18 What Goes Wrong Without Deterministic Rules?
16:30 Why Hardened Workflows Matter
16:48 How to Get Early Access

Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=U6ptUFMyaJg! This is most likely caused by:

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

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Transcript retrieval was blocked by YouTube for this run. The description identifies a hosted Zapier workflow product but no public repository.

### Zapier Next Gen Zaps — https://zapier.com/workflow/early-access

Functionality: The demonstrated system combines AI decisions with deterministic workflow steps, approvals, and recovery behavior. It is a hosted automation feature rather than a repository that can be installed locally.

- Signals: No public repository identified; hosted early-access product.
- Recommendation: **TRIAL** — review it only as a possible pattern for Zo automations, especially deterministic guards around AI actions; do not adopt or pay for access until availability, data handling, and overlap with existing Zo automations are clear. Rough effort: 1–2 hours.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without browser automation. It is the transcript backend used by this watcher.

- Signals: 8,366 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency.
