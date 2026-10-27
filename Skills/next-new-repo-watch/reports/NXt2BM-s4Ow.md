# Text-to-CAD — Describe a Part, Get a Real 3D Model

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-26T20:30:18+00:00
- **Video**: https://www.youtube.com/shorts/NXt2BM-s4Ow

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=Wsru44p-J14 

Text-to-CAD is a plugin that gives your AI agent CAD superpowers: you describe a part, and it generates a real 3D model. 3D modeling is really hard, and sites like Thingiverse and Printables just let you download someone else’s design. Here, the agent designs it for you. In the video, I built a conference room recorder with a touchscreen on the front, a big microphone on top, curvy sides, and a three-part clip-together enclosure, and I don’t know how to design any of that in CAD. The whole print used about $2 worth of plastic. The plugin generates STEP, GLB, STL, or 3MF files, runs design-for-manufacturing checks, creates engineering drawings, and connects to 3D printing, sheet metal, and CNC services. It works with agents that support plugins or skills, including Claude Code, Codex, Cursor, Gemini, and Grok.

#TextToCAD #3DPrinting #AIAgents #CAD #OpenSource #aitools 

🔗 GitHub: https://github.com/earthtojake/text-to-cad
🔗 Website: https://www.texttocad.dev/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=NXt2BM-s4Ow! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **earthtojake/text-to-cad** — 23449★ · Python · pushed 2026-10-27 · license MIT
  - Give your agent CAD superpowers.
  - https://github.com/earthtojake/text-to-cad

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

**Transcript note:** Transcript unavailable (YouTube blocks cloud-host requests). Repos identified from the description and GitHub search.

### earthtojake/text-to-cad

- **Functionality:** Gives a coding agent the ability to generate real parametric 3D CAD models from text descriptions.
- **Signals:** 23,449★ · Python · MIT · pushed 2026-10-27 · not archived.
- **Recommendation: TRIAL** — Sandbox test on a throwaway project. Check the CAD kernel and Python dependencies, then run two or three parts and verify the output file opens in a standard CAD viewer. Fits as a Skills entry for product-design tasks, not as an always-on automation. Effort: ~2 hours.
