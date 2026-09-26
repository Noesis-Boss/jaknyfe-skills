# This Tiny LLM Can Run on Almost Anything

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-24T20:30:08+00:00
- **Video**: https://www.youtube.com/shorts/fD8k0Qbuu7A

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)


Needle is a tiny, fully customizable local LLM built for structured actions rather than open-ended chatting. Developers can define exactly what tools and options it has access to, then tune it for a specific task or device. Its models are small enough to run on hardware like smartwatches, remotes, and other embedded devices, and because it runs locally, it can work without sending data to the cloud.

Github: https://github.com/cactus-compute/needle
Full podcast: https://youtu.be/tsWOiibaaxA

## Transcript

Niddle actually generates like structured instructions for some kind of execution system, automation systems to kind of carry out. And we kind of just call them tool calls. >> The reason that we started talking about you on the channel was you guys were trending like crazy on GitHub. And what people are excited about was it was going beyond the computer to actually put it on devices. And so you have other examples here that show what's possible. Give me one. >> For example, you have like like vacuum systems where you just leave them laying around. But sometimes they just do things. We wish you could actually tell them what exactly we want them to do. With Niddle installed, you can actually get them to do stuff. You can explain to clean the kitchen and not the bedroom for instance, and it just clean the kitchen. And then you can follow up with like uh uh go to the dock and it goes back to charge itself. You're able to command your home system the way you want it natural voice. Our models are kind of 8 to 29 megabytes. So we design them to run on like your smart TV remote, your smart watch, your like devices like that. And you know, where you need like ultimate privacy.

## Auto-extracted repos

- **cactus-compute/needle** — 12664★ · Python · pushed 2026-09-23 · license Apache-2.0
  - Automation foundation model for tiny devices: 2-bit, 8-29 MB, tool calls, structured extraction and embeddings on phones, wearables, smart homes, robots, cars and microcontrollers.
  - https://github.com/cactus-compute/needle

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### cactus-compute/needle

Functionality: A tiny 2-bit automation model for tool calls, structured extraction, and embeddings on constrained devices.

Signals: 12,664 stars; Python; Apache-2.0; pushed 2026-09-23; active, not archived.

Recommendation: **TRIAL** — benchmark CPU inference and structured extraction against a small local workload before considering it for offline automations; allow 1–2 hours.
