# Agent Skills — Give Your AI Coding Agent Senior Engineer Skills

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-06T19:42:07+00:00
- **Video**: https://www.youtube.com/shorts/2hh5B_IzuoU

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

Agent Skills by Addy Osmani is a collection of production-grade engineering skills for AI coding agents. Instead of letting your agent improvise, you give it proven, reusable workflows for the kind of work experienced engineers do every day, so its output is more reliable and closer to production quality. If you build with AI coding agents, this is an easy way to raise the bar on what they produce.

#AgentSkills #AddyOsmani #AIAgents #AICoding #DevTools #OpenSource

🔗 GitHub: https://github.com/addyosmani/agent-skills
🔗 Website: https://skills.addy.ie/

## Transcript

Agent skills, 25 workflows that stop your agent from taking shortcuts. This is another skill pack and again, when we went through this before, you said Andrew scroll down to this and show this. What is this? Why is this the important thing? >> this is it. Some of these that we look at, it's a bunch of random skills or it's a collection of workflows. This is one workflow. You're meant to run these skills in this order. This is exactly how a professional software engineer would develop something too. They'd say, well, first I need to define what the thing is and I need to make sure that the definition is good. I need to turn that definition of I want to add a and what you know, whatever the feature is. Well, a plan. Okay, if we wanted to add a login page, we need the page. We need a logout page. We need the button. We need a users table in the database. The plan takes your visual spec and turns it into something that could actually be built that's hopefully exhaustive. Then you build it. Then you code, which is probably where most people start normally, right? They skip spec, they skip plan, and they just say, "Build a login page for me right now. Go." And then you miss out on all these other things that have to change, too. Then, you know, test, review, and ship. Test and review are the biggest parts that are skipped, you know, after you're building. So, well, did it work? Was it complete? Did you test it? Did the AI test it? And then for ship, you know, the idea of testing doesn't stop when you've tested it on your computer. I've seen a lot of people send me something and say, "Well, it worked on localhost, but then when I deployed it to Railway or Netlify or whatever, it didn't work there, but I didn't know until users started complaining." Well, you got to test there, too. So, part of ship is this like production validation. Download it in the link in the bio.

## Auto-extracted repos

- **addyosmani/agent-skills** — 103188★ · JavaScript · pushed 2026-10-03 · license MIT
  - Production-grade engineering skills for AI coding agents.
  - https://github.com/addyosmani/agent-skills

## Agent eval

Evaluated 2026-10-08 for this environment: Bun/TypeScript + Python, Zo automations, the trading bot, publishing pipeline, and the Skills repository.

### addyosmani/agent-skills — https://github.com/addyosmani/agent-skills
Functionality: 25 production-grade engineering skills for AI coding agents, organized as an ordered workflow — spec, plan, build, code, test, review, ship — including production-environment validation so "it worked on localhost" failures surface before users see them.
- Signals: 103,191★ · JavaScript · MIT · pushed 2026-10-03 · active, not archived.
- Recommendation: **SKIP** — consistent with the 1fHsIveXRa8 verdict: existing workspace skills already cover project templates (zo-project-template), agent contracts (agent-contracts), verification (blast-radius, adversarial-code-review, interrogate), and copy gates (voxwerx, hook-generator); importing this pack would create overlapping policy. The spec→plan→build→test→review→ship order it preaches is already encoded in SOUL.md.
