# Ghidra  — AI Agents Can Now Use the NSA’s Ghidra to Open a Vault

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-20T20:30:17+00:00
- **Video**: https://www.youtube.com/shorts/avZKjaaD2Zo

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=kqn_mSjSWMs

Ghidra is the NSA’s free, open-source software reverse engineering framework, and AI agents can now drive it. In this demo, the agent installs Java, builds a small app called “the vault,” and tests it with a wrong password, which gets denied. Then it decompiles the app with Ghidra, spots a hex value in the code, prints it out, and uses it to open the vault it built. Ghidra was released to the public in 2019 and is widely used by security analysts, malware researchers, and students as a free alternative to expensive proprietary tools. Watching an agent chain these steps together on its own shows how quickly AI is changing security work.

This demo used an app the agent built itself. Only analyze software you own or have permission to test.

#Ghidra #NSA #AIAgents #ReverseEngineering #CyberSecurity #OpenSource #AITools

🔗 GitHub: https://github.com/nationalsecurityagency/ghidra

## Transcript

Ghidra, AI agents now drive the NSA's decompiler. This one I actually do want to show and so it comes from the NSA. I do want to show how it works. What we've got here is we put Java on the system then the agent created this app called the vault and then it tested it with the wrong password to open up the vault and it said, "Nope, you cannot come through." Then it said, "Okay, I want you to decompile this." And it did and one of the lines in the code is this. This is a hex, is that what it's called? >> Atom. >> Yeah. >> That's it. >> And then it said, "Okay, now print what that is." And here it is the code. It is 4271 and then it used that code to open up the vault that it made and sure enough it worked. Download it in the link in the bio.

## Auto-extracted repos

- **NationalSecurityAgency/ghidra** — 92416★ · Java · pushed 2026-10-20 · license Apache-2.0
  - Ghidra is a software reverse engineering (SRE) framework
  - https://github.com/NationalSecurityAgency/ghidra

## Agent eval

> **Transcript note**: Transcript was available (shorts format). Analysis drawn from transcript + video description + live GitHub metadata.

### NationalSecurityAgency/ghidra — https://github.com/NationalSecurityAgency/ghidra

**Functionality**: Ghidra is the NSA's free, open-source software reverse-engineering framework — a decompiler, disassembler, and SRE GUI that supports x86, ARM, and many other architectures. The video demo shows an AI agent installing Java, building a small "vault" app, decompiling it with Ghidra, extracting a hardcoded hex password from the code, and using it to open the vault — a textbook illustration of agentic binary analysis.

**Signals**: 92,416★ · Java · Apache-2.0 license · pushed 2026-10-20 · not archived · 10,350 forks · 2,139 open issues. Extremely mature and active. The repo is under the official `NationalSecurityAgency` org and has been public since 2019.

**Recommendation: TRIAL** — One concrete reason not to SKIP: the demo's pattern (agent builds something → decompiles it → extracts a secret → uses it) is directly relevant to our agent-orchestration and security-analysis work, and Ghidra's headless mode (`analyzeHeadless`) lets an agent drive it without the GUI. What to test: run `analyzeHeadless` on a tiny self-built binary (the vault app pattern) from a Bun/TS script and confirm the decompile + extraction loop works in ~30 min of setup. Rough effort: moderate — Ghidra requires Java 17+ and a multi-GB download; install once on a sandbox box, not on the Zo host. Not INCLUDE because it is a heavy Java GUI framework with zero overlap with our Bun/TS + Python stack, the trading bot, or the publishing pipeline — there is nothing here to "install and adapt" for our day-to-day work. It is worth knowing about as a capability in the security-analysis toolbox, and as a reference for what agentic reverse-engineering looks like.

