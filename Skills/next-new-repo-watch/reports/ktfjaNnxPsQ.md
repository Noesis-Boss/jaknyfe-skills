# Alibaba's Free Tool Catches Security Bugs Vibe Coders Miss

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-22T20:30:37+00:00
- **Video**: https://www.youtube.com/shorts/ktfjaNnxPsQ

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

Open-Code-Review is Alibaba's open-source tool for catching common — and not-so-common — security problems in your code. In one demo, someone deliberately snuck in issues like a plaintext password just to test it, and it caught them right away. Run one command and you get a full, readable HTML report instead of just red and green markers. If you're vibe coding and not reading every line yourself, or relying on an AI to "build it securely," this kind of automated check is quickly becoming table stakes. Everyone shipping AI-generated code should be running something like this.  

#OpenCodeReview #Alibaba #CodeSecurity #VibeCoding #DevTools 

🔗 GitHub: https://github.com/alibaba/open-code-review

## Transcript

Open code review from Alibaba. This is the thing that will let you check your code to find common or maybe even uncommon problems. I saw this one demo where someone said, "I'm intentionally going to sneak stuff into deliberate problems into my code. I want to see if it finds it." And sure enough, it did find those problems. Like he had a password that was just written in plain text. And then he said, "You know what? I want this to not give me just the red and green on my screen. I want to actually see a nice HTML report." And all he did was fire off one command and he got it. This makes sense coming from Alibaba, especially. >> Yeah, I mean, this is starting to be pretty standard practice where if you're out there, you're vibe coding stuff, you're not reading all the lines of code. You don't exactly know how the integrations work. And you've asked Claude to build it in a secure way, but did it? Did it make mistakes? Did some of the changes that you make open up doors that you didn't know were open? So, having something like this run, and even better run automatically, is table stakes. I I think everybody should be doing this. >> Download it in the link in the bio.

## Auto-extracted repos

- **alibaba/open-code-review** — 40045★ · Go · pushed 2026-09-23 · license Apache-2.0
  - Secure, fast, efficient, battle-tested at Alibaba's scale. Hybrid architecture code review tool: deterministic pipelines + LLM Agent, precise line-level comments, built-in multi-language ruleset (NPE, thread-safety, XSS, SQL injection), OpenAI & Anthropic compatible.
  - https://github.com/alibaba/open-code-review

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### alibaba/open-code-review — https://github.com/alibaba/open-code-review

Functionality: A Go code-review tool combining deterministic checks with an LLM-assisted reviewer. It reports line-level findings across common security and correctness issues and can emit readable HTML reports.

- Signals: 40,045 stars · Go · Apache-2.0 · last push 2026-09-23 · active, not archived.
- Recommendation: **INCLUDE** — add it to the Skills repository and project release gates alongside Gitleaks, using the HTML or machine-readable output to review AI-generated changes before commits and pushes. Start with a sandbox run against representative Skills and Zo route fixtures; rough effort: 2–4 hours.
