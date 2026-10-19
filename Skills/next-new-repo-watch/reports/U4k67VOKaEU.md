# First look: How agents manage WordPress

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-18T15:00:20+00:00
- **Video**: https://www.youtube.com/watch?v=U4k67VOKaEU

## Description

Link to Resources: https://thenextnewthing.ai/my-resources
Presented by Zapier: https://zapier.com/
WordPress is becoming agent-first. In this live demo, Andrew Warner and WPVibe founder John Turner show how AI agents like Claude can build, edit, and manage WordPress websites using simple prompts.

Discover how WPVibe lets you create landing pages, add countdown timers and exit popups, build membership courses, and customize your website without manually handling the code. John also explains how agents can connect WPVibe with other tools through MCP, including Google Analytics and Zapier, to build more powerful workflows.

Andrew explores why WordPress’s open-source infrastructure and extensive plugin ecosystem still matter in the age of AI, how you can keep control of your website, and why you may not need to rebuild everything from scratch. Plus, learn about WPVibe’s free plan, which includes up to 100 tool calls per day, and its offer of 15% off a year of any paid plan.

**Links featured:**

- WPVibe: https://wpvibe.ai
- https://wordpress.org/plugins/vibe-ai/
- Zapier: https://zapier.com/

00:00 - WPVibe: Make WordPress Agent-First
00:36 - Live Demo: Build and Edit a WordPress Website
00:54 - Claude: Turn a Static Header Into a Video Background
01:21 - Browser vs. Terminal: Making AI Accessible
01:39 - Connect WPVibe to Claude and ChatGPT
02:15 - MCP Setup: Connect Other AI Agents
02:39 - Build a Landing Page From a Simple Prompt
03:36 - Landing Page Review: What AI Creates
04:03 - Improve the Page With Iterative Prompts
04:57 - Add a Countdown Timer and Fix Layout Issues
05:33 - Create a More Effective Landing Page
06:00 - Exit Popups: Add a 10% Discount Offer
06:45 - Zapier: Connect Popups to Email Marketing
07:12 - Build a Membership Website With WordPress
07:39 - Create a Membership Course With AI
08:24 - Review the Course Structure and Content
09:09 - Test Membership Access and Enrollment
10:12 - Edit Website Pages With Simple Prompts
10:30 - Why Use WordPress Instead of Vibe Coding?
11:24 - The Value of WordPress Plugins and Infrastructure
12:09 - Customize WordPress With AI-Generated Code
12:45 - Connect Analytics to Improve Landing Pages
13:30 - Let Different AI Agents Work Together
13:57 - Do You Still Own Your Website Without WPVibe?
14:24 - SaaS Subscriptions and Ongoing Website Maintenance
15:09 - WPVibe Pricing: Free Access and 15% Off
15:36 - Build a Website With AI in Just Two Hours

Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=U4k67VOKaEU! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

(none auto-extracted — read the transcript above and identify repo names, then search GitHub)

## Agent eval

**Overall verdict**: The episode is a live demo of WPVibe, a commercial WordPress MCP plugin (SeedProd/Awesome Motive). One open-source GitHub repo is presented: the plugin's own source. Recommendation below. Evaluated against the video description + GitHub signals (transcript unavailable — YouTube blocked requests from this IP).

### awesomemotive/wpvibe-ai-mcp — https://github.com/awesomemotive/wpvibe-ai-mcp
- **Functionality**: WPVibe is an MCP server plugin for self-hosted WordPress that gives AI agents (Claude, ChatGPT, Cursor, Windsurf) a structured interface to read content, create/edit posts and pages, manage media, run WP-CLI commands, edit themes, and trigger SeedProd builder saves — all via natural-language prompts. It is the open-source core behind the commercial `wpvibe.ai` service; the WordPress.org plugin slug is `vibe-ai`.
- **Signals**: 21 stars · PHP · GPL-2.0 · last push 2026-10-14 · active, not archived · maintained by Awesome Motive (WPForms, SeedProd, MonsterInsights, OptinMonster, Duplicator) · installable from WordPress.org.
- **Recommendation: TRIAL** — Test by spinning up a throwaway WordPress install, installing the plugin, and connecting it to Claude Code / Codex via `claude mcp add wpvibe`. Verify it can create a draft post, run a WP-CLI command, and trigger a SeedProd save from an agent prompt. Effort: ~30 min. If it works cleanly, it is a direct plug-in point for the Noesis publishing pipeline (WordPress → newsletter/ScholarSearch/zo.space content ingestion) and for any Zo automation that needs to write to a WordPress site. Not an immediate INCLUDE because it is PHP + WordPress-dependent and our stack is Bun/TS + Python; it only pays off if a WordPress site is in scope.

### Zapier — N/A-repo
- Zapier (https://zapier.com/) is mentioned as a sponsor and MCP integration partner, but it is a proprietary SaaS, not a GitHub repo. No action.
### seedprod/vibe-ai — https://github.com/seedprod/vibe-ai
- Functionality: GitHub mirror of the WPVibe plugin distributed on wordpress.org/plugins/vibe-ai. Same MCP-server functionality as the Awesome Motive repo above; this copy is the canonical plugin distribution.
- Signals: 3 stars · PHP · GPL-2.0 · last push 2026-04-01 · stale ~6 months.
- Recommendation: **SKIP** — Install from wordpress.org/plugins/vibe-ai, not from this mirror. The repo is stale and adds nothing over the live plugin. If the Awesome Motive MCP repo trials well, use that one for development and the WP repo for production installs.

### seedprod/wpvibe-integrations — https://github.com/seedprod/wpvibe-integrations
- Functionality: Official WPVibe remote MCP integration configs for Cursor, Grok Build, and Gemini CLI — client-side connection snippets pointing at the WPVibe MCP server.
- Signals: 0 stars · no declared language · MIT · pushed 2026-09-29 · active. No server code; wiring diagrams only.
- Recommendation: **SKIP** — Zero functionality of its own. Only makes sense after the WPVibe plugin is installed, and even then it is just a per-client config snippet. Nothing to install or adapt here.

