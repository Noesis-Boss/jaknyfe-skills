# Easy step-by-step setup

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-21T14:00:35+00:00
- **Video**: https://www.youtube.com/watch?v=WPUAZm5rnGc

## Description

Link to Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
Andrew Warner and Achint Singh show how an AI voice agent can call leads, qualify prospects, book sales calls, and automatically pass conversation context into a CRM.

Achint walks Andrew through the system he built for Belong, a service helping founders and technical engineers move to the US on legal work visas. When a potential customer completes a form but doesn’t book a call, GrokBot triggers an outbound voice agent that calls the lead, asks qualification questions, handles the conversation, and can text them a calendar link. Achint says the bot had already helped book $16,000 in revenue after roughly two weeks of being live.

They then build the system from scratch, starting with a simple voice-note “ramble” that GrokBot turns into a technical plan. The setup uses GrokBot as the orchestrator, ElevenLabs for the voice agent, Twilio for the phone number, Netlify for the website forms, and Attio as the CRM. They also explain how conversation data is captured and passed into the CRM so a human sales agent has the full context before speaking with the customer.

The episode also covers cloning a founder’s voice, connecting agents together, testing the system, avoiding bad customer experiences, and why clearly defining the customer journey matters when AI can build and deploy systems so quickly.

Links featured:

- GrokBot — https://grok.com/
- ElevenLabs — https://elevenlabs.io/
- Twilio — https://www.twilio.com/
- Netlify — https://www.netlify.com/
- Attio — https://attio.com/
- Belong — https://belonglaw.com/

Timestamps:

00:00 AI Agent Calls Customers
00:18 Live GrokBot Sales Call Demo
02:51 $16K in Revenue
03:00 How the System Works
04:21 Building the Agent From a Voice Note
05:15 Turning a Ramble Into a Build Plan
06:00 ElevenLabs + Twilio Setup
06:45 Why Use a Cloned Voice?
07:21 Getting a Phone Number
08:15 Testing the Voice Agent
08:33 How the Agents Work Together
09:36 Saving Conversations to the CRM
10:03 Full Tech Stack
10:12 Does the AI Sound Robotic?
10:30 Advice for Building AI Sales Agents
11:06 More GrokBot Use Cases
11:15 GrokBot vs Other Coding Agents

Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=WPUAZm5rnGc! This is most likely caused by:

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

Transcript retrieval was blocked by YouTube for this run. The description identifies a hosted voice-agent implementation but no public GitHub repository.

### Hosted GrokBot / ElevenLabs / Twilio / Netlify / Attio stack

Functionality: The system calls leads who submitted a form but did not book, qualifies them, texts a calendar link, and passes the conversation context into a CRM. The described implementation is a hosted service composition, not a repository presented for local installation.

- Signals: No public repository identified; product and service names only.
- Recommendation: **SKIP** — no repo to install or adapt, and the workflow needs explicit consent, privacy, voice-cloning, CRM-permission, and operating-cost review before a trial.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without an API key or browser automation. It is the transcript backend used by this watcher.

- Signals: 8,353 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency.
