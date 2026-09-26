# This Skill Gives Your AI Agent a Browser

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-25T20:30:23+00:00
- **Video**: https://www.youtube.com/shorts/qfRMHqh7tNI

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Agent Browser lets AI agents navigate websites, fill forms, click buttons, take screenshots, test web apps, and automate browser tasks behind the scenes. In this clip, Andrew and Robbie break down why it’s such a powerful skill.

Github: https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md

Full podcast: https://youtu.be/ehab5PtgRo8

## Transcript

The ancient browser skill, this one is from Vercel. Basically, let your agent have access to a web browser. Can I actually see it control my browser? Is it controlling the browser on my computer? >> So, there's two ways with this agent. This agent is headless, meaning that it does everything like under the under the covers. So, they call like a CLI agent, which is command line interface. So, it has full control of your web browser. It can move things like and technically called your DOM or it can move things within the website, but doesn't ever actually show the mouse moving. But, this is more even more powerful way, which is it works behind the scenes, but it's it's actually moving and controlling your browser. You just don't see it. >> Okay. And the examples I've got here is log in to the dashboard and screenshot the billing page. Another example here is open the staging, sign up as a test user, and then tell me if it works. >> It is a super powerful tool because even like the screenshot, you're getting a screenshot of a web browser without the web browser ever opening.

## Auto-extracted repos

- **vercel-labs/agent-browser** — 43216★ · Rust · pushed 2026-09-24 · license Apache-2.0
  - Browser automation CLI for AI agents
  - https://github.com/vercel-labs/agent-browser

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### vercel-labs/agent-browser

Functionality: Rust CLI for headless browser control, DOM interaction, screenshots, and browser workflows for agents.

Signals: 43,216 stars; Rust; Apache-2.0; pushed 2026-09-24; active, not archived.

Recommendation: **INCLUDE** — use it as the default browser-verification layer for Zo site checks and webapp-testing workflows.
