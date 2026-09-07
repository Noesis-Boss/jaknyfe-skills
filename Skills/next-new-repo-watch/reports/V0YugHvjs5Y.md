# This Tool Gives AI a Map of Your Codebase

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-08-31T21:12:46+00:00
- **Video**: https://www.youtube.com/shorts/V0YugHvjs5Y

## Description

Graphify turns any codebase — including its docs, SQL schemas, configs, and PDFs — into a queryable knowledge graph. Instead of an agent like Claude Code, Cursor, or Codex reading through source files from scratch every time to figure out what relates to what, Graphify analyzes the project up front and builds a structure the agent can navigate directly. It uses local deterministic AST parsing with every edge explained — no vector store required. Big time-saver for anyone working on large or complex codebases.

#Graphify #ClaudeCode #Cursor #OpenSource #devtools 

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=tX9ANddpAqc 

🔗 GitHub: https://github.com/Graphify-Labs/graphify

## Transcript

Graphify, you're going to turn a folder of code into queryable knowledge graph. We've seen this actually is an issue that's come up a lot. How do you make your data basically put an index like you would on a book on the data that you have so that it's more searchable, that it's faster to get access to. What do you think of Graphify? >> So, I mean just to really hammer home the concept of what this is, if you go into a code base with something like clawcode or codex and you say change something within this app and that change involves lots of different parts of the app. What those agents have to do is they have to read the source code files, figure out what relates to what and then work out how they can make the change surgically by changing oh I need to change this piece of the app. Maybe I need to look at these docs that are within the app. It has to kind of figure all of that out as it goes. Something like Graphify, what it does is it will go through an analyzer project first and figure out okay, this documentation file is for this piece and this piece and it will figure out which parts of an app are related to each other and then kind of put this together into a structure an agent can navigate through rather than having to try to figure out everything from first you know principles every single time you want to make a change. >> Download it in the link in the bio.

## Auto-extracted repos

- **Graphify-Labs/graphify** — 115191★ · Python · pushed 2026-09-05 · license Apache-2.0
  - Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.
  - https://github.com/Graphify-Labs/graphify

## Agent eval

- **Graphify-Labs/graphify** — Turns a codebase (source, docs, SQL schemas, configs, PDFs) into a queryable knowledge graph via local deterministic AST parsing, so coding agents navigate pre-mapped structure instead of re-discovering relationships each session; ships as a `/graphify` skill for Claude Code, Cursor, Codex, and Gemini CLI.
  - Signals: 115,198★ · Python · Apache-2.0 · pushed 2026-09-05 · not archived.
  - Recommendation: **TRIAL** — Python/Apache-2.0, actively maintained, no overlap with installed tooling; test it as an index over the large local repos (robinhood-trading-bot, jaknyfe-skills) before adopting it as standing agent infrastructure.

## Eval

Evaluated 2026-09-07 from transcript + description of https://www.youtube.com/shorts/V0YugHvjs5Y.

Repos/products identified: **Graphify-Labs/graphify** (the featured project). Conversational mentions — "clawcode" (spoken form of Claude Code), Codex, Cursor, Gemini CLI — are established agent tools referenced only as consumers of the graph, not presented projects: N/A-repo (Claude Code/Cursor are closed products; Don already runs Claude Code and Codex via Zo).

- **Graphify-Labs/graphify** — https://github.com/Graphify-Labs/graphify
  - **Functionality:** Indexes a codebase — source, docs, SQL schemas, configs, PDFs — into a queryable knowledge graph using local deterministic AST parsing, with every edge explained and no vector store. Ships as a `/graphify` skill so agents (Claude Code, Cursor, Codex, Gemini CLI) navigate pre-mapped relationships instead of re-discovering them each session. Verified live: 115,397★, Python, Apache-2.0, created 2026-04, pushed 2026-09-05, not archived, 11.2k forks / 1,255 open issues.
  - **Fit:** Python tool that runs locally as a skill — slots directly into the Zo Skills system; useful for indexing the larger local repos (robinhood-trading-bot, jaknyfe-skills, scholarsearch) where agents repeatedly re-derive file relationships. No Bun/TS conflict since it's a standalone CLI/skill, not a library dependency.
  - **Verdict:** TRIAL — actively maintained, no overlap with installed tooling; index one large repo (robinhood-trading-bot) and measure whether agent navigation actually improves before adopting as standing infrastructure.
