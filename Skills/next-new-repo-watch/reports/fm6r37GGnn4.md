# Impeccable: The Free AI Design Tool That Could Replace Figma?

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-11-02T21:30:04+00:00
- **Video**: https://www.youtube.com/shorts/fm6r37GGnn4

## Description

Impeccable: https://github.com/pbakaus/impeccable
More free AI tools: https://thenextnewthing.ai/Resources

Presented by Zapier: https://zapier.com/

Is this a Figma killer? Andrew and Adam explore Impeccable, a free AI design tool that helps coding agents create better-looking interfaces, understand your design preferences, and make changes through visual feedback.

🎬 Watch the full podcast on The Next New Thing:
https://youtu.be/-6SHbxdXMRU

🎙️ Watch Andrew's interview with the creator of Impeccable:
https://youtu.be/EUavfcfHtu4

#impeccable  #figma  #aidesign  #claudecode  #aicoding  #uidesign  #opensource

## Transcript

This looks to me like a Figma killer. What I like about impeccable is once you install it, it will work with you to understand what you think is good design, what you're trying to accomplish, and then it will create something for you based on your needs, not its own personal taste. And then after that, Adam, I really like how you can give your agent feedback, where you can just touch a thing on the screen and say, "I don't like it." You can draw on your screen and say, "I want this moved over there." That little bit of feedback is super helpful for working with your agent. And that was something that I hadn't Here it is, right here. You can see how you're you're interacting with the agent to give it feedback. It's something that I hadn't pointed out before cuz I didn't notice it. >> I mean, as I watch you click around in here, Andrew, I I'm just thinking, and this is free? >> I know. >> I can use this for free? >> Download it in the link in the bio.

## Auto-extracted repos

- **pbakaus/impeccable** — 101077★ · Rust · pushed 2026-11-02 · license Apache-2.0
  - The design vocabulary for your coding agent. Steer with polish and bolder, review with critique and audit, catch AI slop before it ships.
  - https://github.com/pbakaus/impeccable

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

**Evidence note:** Transcript is short-form (Shorts) and names only Impeccable. Eval uses the show notes, the auto-extracted repo, and GitHub metadata pulled 2026-11-02.

### pbakaus/impeccable — https://github.com/pbakaus/impeccable
- Functionality: A design vocabulary for coding agents: polish and bolder steer output, critique and audit review it, and it flags generic AI-looking UI before it ships. The video also covers visual click-and-draw feedback to the agent.
- Signals: 101,077★ · Apache-2.0 · pushed 2026-11-02 · not archived · primary language Rust (CLI/tooling; the skill content itself is agent-facing markdown).
- Recommendation: **TRIAL** — overlaps `frontend-design`, `ui-ux-pro-max`, and `add-motion` already in `Skills/`, so it must earn its slot. Test `critique` and `audit` on the live zo.space homepage and one project page, then compare output against that project's `DESIGN.md`; `DESIGN.md` tokens win on any conflict. Run the SkillSpector gate before install, and check whether its installer writes into agent directories host-wide (the `hyperframes init` lesson). Effort: about 1 hour.
