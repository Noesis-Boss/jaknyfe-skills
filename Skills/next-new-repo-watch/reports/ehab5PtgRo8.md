# Why is everyone using these?

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-16T17:07:11+00:00
- **Video**: https://www.youtube.com/watch?v=ehab5PtgRo8

## Description

Resources: https://thenextnewthing.ai/l/top-skills-sep16
Presented by Zapier: https://zapier.com/
Andrew Warner and Robbie Abed break down the 10 most-installed AI skills from GitHub, including skills that help agents find other skills, improve software design, browse the web, follow engineering best practices, and become better tutors.

Andrew and Robbie start with Find Skills, a Vercel skill that works like an app store for AI skills, helping agents discover and install the right capabilities for a task. They then explore Matt Pocock’s Grill Me and Grilling skills, which push AI to ask better questions and stress-test ideas before work begins. Anthropic’s Frontend Design skill is next, helping agents create more distinctive interfaces instead of falling into the familiar “AI-generated” design patterns. They also look at Vercel’s Agent Browser, which gives agents headless control of a web browser, and Matt Pocock’s setup skill for bringing engineering workflows and best practices into a repository.

The list also includes Vercel’s React Best Practices skill, which helps agents follow performance recommendations for React and Next.js, Lark Doc for interacting with ByteDance’s workplace platform, and Matt Pocock’s Teach skill, which turns an AI agent into a persistent tutor that builds lessons over time and remembers what you've already learned. Finally, they explore Vercel’s Web Design Guidelines, covering accessibility, forms, typography, animation, and other practical web standards. Throughout the episode, Andrew and Robbie show what these skills actually do, how they work together, and why packaging repeatable workflows into skills can make AI agents more capable.

Links featured:

- **find-skills** — vercel-labs/skills — (https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)
- **grill-me** —  mattpocock/skills — (https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md)
- **frontend-design** —  anthropics/skills — (https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md)
- **agent-browser** — vercel-labs/agent-browser — (https://github.com/vercel-labs/agent-browser/blob/main/skills/agent-browser/SKILL.md)
- **setup-matt-pocock-skills** — mattpocock/skills — (https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md)
- **vercel-react-best-practices** — vercel-labs/agent-skills — (https://github.com/vercel-labs/agent-skills/blob/main/skills/react-best-practices/SKILL.md)
- **grilling** — mattpocock/skills — (https://github.com/mattpocock/skills/blob/main/skills/productivity/grilling/SKILL.md)
- **lark-doc** — (https://github.com/larksuite/cli/blob/main/skills/lark-doc/SKILL.md)
- **teach** — mattpocock/skills — (https://github.com/mattpocock/skills/blob/main/skills/productivity/teach/SKILL.md)
- **web-design-guidelines** —  vercel-labs/agent-skills — (https://github.com/vercel-labs/agent-skills/blob/main/skills/web-design-guidelines/SKILL.md)

00:00 - Top 10 AI Skills
00:27 - Find Skills
01:03 - Grill Me
02:15 - Frontend Design
03:02 - Robbie Abed & NoMiddle
03:54 - Agent Browser
05:33 - Setup Matt Pocock Skills
06:27 - Vercel React Best Practices
07:39 - Grilling
08:42 - Lark Doc
09:36 - Teach
10:48 - Web Design Guidelines
11:24 - Why AI Skills Are Easy to Use
12:18 - Deep Dive With Matt Pocock

👉 Send us your AI builds: hi@thenextnewthing.ai

Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable:
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=ehab5PtgRo8! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
- **vercel-labs/skills** — 31845★ · TypeScript · pushed 2026-09-16 · license MIT
  - The open agent skills tool - npx skills
  - https://github.com/vercel-labs/skills
- **mattpocock/skills** — 264033★ · Shell · pushed 2026-09-17 · license MIT
  - Skills for Real Engineers. Straight from my .agents directory.
  - https://github.com/mattpocock/skills
- **anthropics/skills** — 176803★ · Python · pushed 2026-09-10 · license none
  - Public repository for Agent Skills
  - https://github.com/anthropics/skills
- **vercel-labs/agent-browser** — 42765★ · Rust · pushed 2026-09-17 · license Apache-2.0
  - Browser automation CLI for AI agents
  - https://github.com/vercel-labs/agent-browser
- **vercel-labs/agent-skills** — 31269★ · JavaScript · pushed 2026-08-28 · license none
  - Vercel's official collection of agent skills
  - https://github.com/vercel-labs/agent-skills
- **larksuite/cli** — 17261★ · Go · pushed 2026-09-17 · license MIT
  - The official Lark/飞书 CLI tool, maintained by the larksuite team — built for humans and AI Agents. Covers core business domains including Messenger, Docs, Base, Sheets, Calendar, Mail, Tasks, Meetings, and more, with 200+ commands and 20+ AI Agent Skills.
  - https://github.com/larksuite/cli
## Agent eval

### vercel-labs/skills
- Functionality: The open agent skills tool - npx skills.
- Signals: 31845★ · TypeScript · pushed 2026-09-16 · license MIT.
- Recommendation: TRIAL — review one workflow for a gap in Skills, test it in a disposable project, and run SkillSpector before adoption; budget about 1 hour.
- Repository: https://github.com/vercel-labs/skills

### mattpocock/skills
- Functionality: Skills for Real Engineers. Straight from my .agents directory.
- Signals: 264033★ · Shell · pushed 2026-09-17 · license MIT.
- Recommendation: TRIAL — review one workflow for a gap in Skills, test it in a disposable project, and run SkillSpector before adoption; budget about 1 hour.
- Repository: https://github.com/mattpocock/skills

### anthropics/skills
- Functionality: Public repository for Agent Skills.
- Signals: 176803★ · Python · pushed 2026-09-10 · license none.
- Recommendation: TRIAL — review one workflow for a gap in Skills, test it in a disposable project, and run SkillSpector before adoption; budget about 1 hour.
- Repository: https://github.com/anthropics/skills

### vercel-labs/agent-browser
- Functionality: Browser automation CLI for AI agents.
- Signals: 42765★ · Rust · pushed 2026-09-17 · license Apache-2.0.
- Recommendation: INCLUDE — the agent-browser CLI is already installed for browser automation and screenshots.
- Repository: https://github.com/vercel-labs/agent-browser

### vercel-labs/agent-skills
- Functionality: Vercel's official collection of agent skills.
- Signals: 31269★ · JavaScript · pushed 2026-08-28 · license none.
- Recommendation: TRIAL — review one workflow for a gap in Skills, test it in a disposable project, and run SkillSpector before adoption; budget about 1 hour.
- Repository: https://github.com/vercel-labs/agent-skills

### larksuite/cli
- Functionality: The official Lark/飞书 CLI tool, maintained by the larksuite team — built for humans and AI Agents. Covers core business domains including Messenger, Docs, Base, Sheets, Calendar, Mail, Tasks, Meetings, and more, with 200+ commands and 20+ AI Agent Skills.
- Signals: 17261★ · Go · pushed 2026-09-17 · license MIT.
- Recommendation: TRIAL — review one workflow for a gap in Skills, test it in a disposable project, and run SkillSpector before adoption; budget about 1 hour.
- Repository: https://github.com/larksuite/cli

Source note: Transcript was unavailable from this host. Repository identities and summaries are drawn from the available video description and GitHub metadata.
