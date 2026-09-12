# 10 Repos conserve your token usage

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-09T21:34:31+00:00
- **Video**: https://www.youtube.com/watch?v=Jv050l7y6ik

## Description

Link to Resources: https://thenextnewthing.ai/l/github-repos-sep9
Presented by Zapier: https://zapier.com/
👉 Mat Nolen (LinkedIn): https://www.linkedin.com/in/mat-nolen
Andrew Warner and Mat Nolen explore 11 GitHub repos designed to help developers and AI agents save tokens, reduce context usage, route between AI providers, and make coding agents more efficient.

Andrew Warner sits down with Mat Nolen to test a collection of GitHub projects focused on one of the biggest challenges with AI coding agents: context and token costs. They explore Free LLM API, which combines free tiers from multiple AI providers and automatically switches between them; Magic Compact, a lossless context compressor that moves tool output to disk; Headroom, which compresses tool output before it reaches the agent; and PX Pipe, a viral experiment that converts context into images to reduce context-window usage.

They also test LeanCTX, a prompt compressor that removes low-value words to reduce token usage, Token Optimizer MCP, which helps agents avoid repeating expensive calls, and Context Mode, which stores raw tool output in a local index instead of keeping it inside the context window. The episode continues with Ponytail, which pushes agents toward simpler implementations, Graphify, which turns a codebase into a knowledge graph, and OmniRoute, which combines provider routing, free tiers, and context compression into a single gateway.

Repos featured:

- freellmapi — https://github.com/tashfeenahmed/freellmapi
- magic-compact — https://github.com/aerovato/magic-compact
- headroom — https://github.com/headroomlabs-ai/headroom
- pxpipe — https://github.com/teamchong/pxpipe
- leanctx — https://github.com/jia-gao/leanctx
- token-optimizer-mcp — https://github.com/ooples/token-optimizer-mcp
- context-mode — https://github.com/mksglu/context-mode
- ponytail — https://github.com/DietrichGebert/ponytail
- graphify — https://github.com/Graphify-Labs/graphify
- OmniRoute — https://github.com/diegosouzapw/OmniRoute
- codebase-memory-mcp — https://github.com/DeusData/codebase-memory-mcp

00:00 - Free LLM API: Combine free AI tiers and save on tokens.
01:18 - Magic Compact: Move context to disk instead of deleting it.
02:32 - Headroom: Compress coding-agent tool output before it hits the context window.
03:49 - Zapier SDK: Connect 8,000+ tools to the software you build.
04:12 - PX Pipe: Turn context into images to reduce context-window usage.
05:26 - LeanCTX: Cut token usage with prompt compression.
06:45 - Token Optimizer MCP: Stop agents from repeating expensive calls.
08:07 - Context Mode: Keep raw tool output outside the context window.
09:26 - Ponytail: Make AI agents write less code and use what already exists.
10:27 - Graphify: Turn your codebase into a knowledge graph.
11:51 - OmniRoute: Route requests across hundreds of AI providers.
12:46 - RTK Compression: Reduce context usage while routing between providers.
13:12 - Weekly GitHub Roundup: More trending repositories to explore.

👉 Send us your AI builds: hi@thenextnewthing.ai

👉 Media/Sponsorship Inquiries: https://thenextnewthing.ai/l/sponsor

👉 Join us: https://thenextnewthing.ai/

## Transcript

You're about to get tools that will let you and your agent build more for less with these repos. In fact, one of them is going to let you build for free. Let's get into it. [music] Presented by Zapier, the AI automation company. Okay, the first one is free LLM API. I'm actually going to be interviewing the founder Tosh about this because what he did was he created a way to take all those free tiers at multiple providers and make them accessible. And when you run out of access on one free tier, he automatically will switch you to the next and the next and the next. And I asked him if uh these providers are angry at him. He said, "Actually, they're pitching me on being included because they want this to be the entry point for users to come and experiment with them and try them out." So, super easy. I think this one is just a clear easy one for saving tokens. What do you think? >> [snorts] >> I think it's it's awesome that you can kind of if you stack enough of the free tiers, you're not paying anything and it gives you a chance to kind of play around with you know, maybe there's you know, some projects or something that you want to try or do that you don't want to eat your tokens up and you can just get it on play and go. >> Yeah, and he's got a Mac app and Android app, Windows, super easy to use and we'll have a link to that and everything else below. Let's go on to the next one. Magic Compact. You've used this. Tell me about it. >> Yeah, so this one is a a lossless uh context compressor. So, what it does is it swaps the big tool output for kind of like a one-line note and then it goes uh directly to your disk. So, you know, the concept is is context is expensive, disk is cheap. So, move it, don't delete it is I think was their tagline on there. So, I tested it about eight times and eight times it came back identical. So, you um basically, you're not compressing anything. You're really just moving it off disk. It's it's it's it's looking at the cache there. It's looking at the information there and bringing it back in and going back and forth. >> And you know what? It has very few stars. So, nice finding you found Uh uh 147 stars. And, what do you think about this? That the developer paused development on this to switch over to operator memory. Were you still able to get value out of it? >> Uh yeah, I think I think as he worked this project, he realized that he could tweak a few things. So, I think he pushed it to the direction of the operator memory. This one still works. It's just he's not, you know, putting any updates to it. He's not He's not putting anything thing into it. But, I I think he just stumbled upon other ideas and architecture to work with. So, I think he went that route. >> All right. Next, Headroom. Super popular. I've seen a lot of YouTube videos on this. What is Headroom and what did you find when you used it? >> So, for Headroom, that's uh pretty much the compression layer for the coding agents. It's how they have it tagged. It So, it sits between your agent and the API. And, what it does is it squeezes uh the tool output all the way through. So, if um So, the concept is is your prompt is small, what comes back from the tool isn't. So, it basically it shortens what you read, not what you write. So, what uh it's Basically, if you look at the compression algorithm there, it compressed my file to like 37% going back and forth to take kind of that context uh window down. >> I see. I'm writing something to the agent. The agent spits out a lot of text and a lot of information. It compresses just what it sends back to me to make it less so when it looks at it again. Do I have that right? >> Yes. >> Okay. And, it works. You got good results with it. >> I had great results from it. I had no complaints. I mean, it I feel like it it at times it even performed a little bit better than what they claimed like in the read me or any other information that they had. So, yeah. It worked really really flawless. >> It's incredibly popular. Incredibly popular. All right. Let's go on to Oh, Zapier. Listen, you all, if you're building anything, you should know that Zapier SDK will allow you to bring over 8,000 tools that your users already want access to and connect it into the apps that you're building. If you want to try it out right now, go to zapier.com/sdk. Get your users the apps they need in the software you write. Next. I can't believe you used this one. PX Pipe. This is the one. I kind of like it cuz it's just adds some lightheartedness to this conversation. This is the one that went super >> try it just cuz I wanted to see if it would even work. Cuz I just couldn't believe it worked. So, this one is supposed to take your context, put it into pictures, send it off, render it, go back and forth. And so, instead of using that context window back and forth, it's like, I'm going to use this picture and read this picture. >> Yeah, like if I look at this, this is a picture that takes the big prompt. Okay, all right. So, this is This one really viral on X a while back, and you can see how many stars it got from that. People were talking about it. Did it actually work? >> It worked. Uh and the accuracy was not quite there. one of the biggest problems I saw right off the bat is if you're not using the you know, the most up-to-date model, some of the older models, if you're trying to work, maybe you're, you know, trying to use like your local models instead, some of those just are not great at reading those images, and they get a lot of that information wrong, which then could cause possible hallucination or get the information wrong. So, it was more of a project just to see if I could get it to work. >> That was fun. I'm glad that you tried it. It does actually have a lot of action over 7,000 stars on GitHub. Let's go on to the next. Lean CTX. Change one import line and cut the token bill. How does this work, and what did you find when you used it? >> It's a a prompt compressor, so it just starts swapping text lines, you know, drops all the low-value words out of there. Um you know, a lot of those fillers. I think there's like uh caveman ADHD. I think those are kind of on the along the same lines where they're just stripping out some of the stuff that's not useful that the the LLM does not need to see or hear to to get from point A to point B. So, it works pretty good. I mean, the it the claim held. It uh it says that they it'll do anywhere from 40 to 60 uh tokens per saving, and mine did 52. So, I mean, it it was on par. It's just I guess it would be dependent upon what you're working on. I the value of of actually, you know, pulling out some of that information or the fear of maybe it pulling out something it shouldn't cuz you don't really get to see, you know, the exact words or the the the yeah, the words or the what they're swapping out. >> Okay. It doesn't look like you're super high on this one, but it did it did deliver what it promised. >> It did deliver what it promised. >> All right. Next, token optimizer MCP. Explain to me what this does and why you actually didn't want to install it. >> So, this one is an MCP server, so that's a little bit different than just the um just downloading the repos. So, with this MCP server, it's supposed to block the expensive calls, and then it's supposed to help remember what the agent worked out. So, it's almost like uh it's basically almost like creating its own memory is what the MCP server's doing. So, um you know, if when it reaches for a file it's already read, it'll refuse and go, "Nope, you've already got that." And and it just tries to say to point it in the right direction to say, "Hey, this this is what we already did. Don't keep keep asking for it. Don't keep looking for it. You literally have it right here." So, it's it's it works. It's just one of those where you have to decide if you want to go the whole MCP route. >> And you also had like a big no-no or a big watch out a a cautionary note on this. What's that? >> Yeah, unfortunately this one when you install the MCP, it actually turns off your cloud codes trust prompt when you install it and you know, that's usually a big no-no in your production you know side you you need to know what you're doing. If you're going to turn that off and you need to know the consequences of that. >> All right. And by the way, we're going to have a link to Matt if you want to connect with him and find out more about him right below in the description. Let's go on to context mode. Keep raw tool output out of the window entirely. How does this work and what do you think of it? >> So this one here this one that keeps that tool output out of your context. So the output goes into a local index um outside of the window. So basically a I guess you could say in in layman's term a database. So the output goes into that local index or database instead of the window and then anytime you do the call the model will then query and go back and forth to that. So that way it doesn't have to read the whole file to answer your question. It can go straight to that index or that database that it's looking at. >> What do you think of it? >> Um I'm trying to remember about this one. I want to say this one did good. I'm I'm trying to I'm trying to remember that. The only one I ran I want to say this one hit the number cuz they claim that you can get like 98 >> Mhm. >> 98 and I think I got 98 on that one. >> Yeah, here the readme claims 98% reduction and you you look at this. In fact, as soon as you click in they're basically big with >> Yeah, and I want I want to say I got like 95%. So you're even mid 90s is really good. >> Okay. All right. Next ponytail. This one is incredibly popular with developers. Um think of this I like this line. Think of this as is senior developer sitting inside your agent. You ask for a date picker and where a junior developer might give you the library and wrap uh it what might start installing library and wrapping it, it reaches for the one browsers already have. It basically is looking for the easy answer instead of like the more complicated one that's over eager. I think of this is like a way I need to live my life like ponytail. What do you think of ponytail? >> This one is nice. It basically it makes your agent just write less code in general, which is I mean ideal. So, it basically pushes it to use what already exists instead of installing it or going out and looking for it. Um and I want to say this one had like the the the the cheapest amount of tokens to use no matter what you write. When you use the ponytail, it does seem to stay, you know, on par with exactly what it's claiming it does. >> Okay. Um and we'll have this I know I've been flipping through these pages pretty quickly. We'll have a link to this website that I that I've been going through in the description. Graphify maybe the most popular tool for something like this. How would you explain uh Graphify? >> So, this one is kind of like one of the other ones. It's basically it's a a knowledge graph for your code base. So, basically it parses all your information into a graph map and then the agent asks the map instead of opening files or calling to it. So, it's kind of it queries your code base into the the the graph map versus just straight context text is what it does. Um it's pretty neat. It basically it builds that map though and it costs you zero tokens. It doesn't require any models when it when it builds out that map. So, you can really try it out without using anything just to see if you can actually get the savings from it or if you like the way the speed that it communicates back and forth. >> And uh over 100,000 stars keeps showing up. It is actually from a Y Combinator startup from a recent batch. So, I actually don't think this is a warning. I think this is exciting that they're getting into this. Y Combinator now is noticing and and participating. By the way, if you all like this, I'd love it if you leave a like and subscribe. Or if you don't, comment. One thing that I'm looking for is what other collections do you want us to find? And if you tell me in the comments, you'll see I'll engage and we'll see if we can find another collection like this. This was a request from from viewers from a past show. Finally, OmniRoute. One endpoint, hundreds of providers, free tier. First, here's essentially what this is. You and I went through this and spent a lot of time on it. This is very similar to the first one in the sense that you can get a bunch of free providers in here and it will route the requests to the free providers. But unlike the first one, this will also have um your paid providers in this and it will route them based on what you tell it to. And if you run out of uh usage on Anthropic's models, you can go to um to Open AI's and so on. Right? And and that's even just the beginning of what it does to help save tokens. What do you think, Matt? >> So, this one kind of threw me off. And I'd say we talked about a little bit because I was confused. It does like you said, it does a few things. One, it's doing some compression. It's using the RTK engine. So, that alone is is is a great tool to have that is doing some sort of compression with your context window. But then, it goes to like you said, it's a it's a gateway where you can go to all these different providers. So, you're now using other tokens besides your paid ones. >> All right. Yeah, it's it's the one that does the most of everything that we've had here, which is why we saved it for the end. And if you like this collection, you should know that every week I do a roundup of the top GitHub repos, the ones that are trending. And I've got the most recent one for you right here to click to and I'll see you in that one next.

## Auto-extracted repos

- **tashfeenahmed/freellmapi** — 25672★ · TypeScript · pushed 2026-09-10 · license MIT
  - 7.4 billion tokens per month. 34 free LLM providers. 635 free model endpoints. All behind one /v1 endpoint, plus any custom OpenAI-compatible endpoint. Smart routing, automatic failover, encrypted keys. Personal experimentation only.
  - https://github.com/tashfeenahmed/freellmapi
- **aerovato/magic-compact** — 167★ · TypeScript · pushed 2026-08-24 · license BSD-3-Clause
  - Lossless context compression plugin for Claude Code & OpenCode.
  - https://github.com/aerovato/magic-compact
- **headroomlabs-ai/headroom** — 71674★ · Python · pushed 2026-09-12 · license Apache-2.0
  - Compress tool outputs, logs, files, and RAG chunks before they reach the LLM. 20% fewer tokens for coding agents, 60-95% fewer tokens for JSON, same answers. Library, proxy, MCP server.
  - https://github.com/headroomlabs-ai/headroom
- **teamchong/pxpipe** — 7384★ · TypeScript · pushed 2026-09-11 · license MIT
  - cut Claude Code token usage by rendering text context as images
  - https://github.com/teamchong/pxpipe
- **jia-gao/leanctx** — 327★ · Python · pushed 2026-08-22 · license MIT
  - Drop-in prompt compression for production LLM apps. Cut your token bill 40-60% without changing your code. Python SDK, LLMLingua-2, MIT.
  - https://github.com/jia-gao/leanctx
- **ooples/token-optimizer-mcp** — 520★ · JavaScript · pushed 2026-09-11 · license MIT
  - Measure token savings per AI coding agent, optimize context, and share a live local knowledge graph across 16 CLI clients.
  - https://github.com/ooples/token-optimizer-mcp
- **mksglu/context-mode** — 22276★ · TypeScript · pushed 2026-09-12 · license NOASSERTION
  - Context window optimization for AI coding agents. Sandboxes tool output (98% reduction), persists session memory, and   enforces routing across 17 platforms via MCP + hooks.
  - https://github.com/mksglu/context-mode
- **DietrichGebert/ponytail** — 136233★ · JavaScript · pushed 2026-09-07 · license MIT
  - Makes your AI agent think like the laziest senior dev in the room. The best code is the code you never wrote.
  - https://github.com/DietrichGebert/ponytail
- **Graphify-Labs/graphify** — 117127★ · Python · pushed 2026-09-10 · license Apache-2.0
  - Turn any codebase, with its docs, SQL schemas, configs, and PDFs, into a queryable knowledge graph. A /graphify skill for Claude Code, Cursor, Codex, and Gemini CLI: local deterministic AST parsing, every edge explained, no vector store.
  - https://github.com/Graphify-Labs/graphify
- **diegosouzapw/OmniRoute** — 65090★ · TypeScript · pushed 2026-09-12 · license MIT
  - Never stop coding. Free MIT AI gateway: one endpoint, 352 providers (150+ free), 1200+ models Kimi, Claude, GPT, Gemini, GLM, DeepSeek, MiniMax. Works with Claude Code, Codex, Cursor, OpenCode, Cline & Copilot. Quota-aware auto-fallback, RTK+Caveman compression saves 15-95% tokens, MCP/A2A, Desktop/PWA. Built by 550+ contributors
  - https://github.com/diegosouzapw/OmniRoute
- **DeusData/codebase-memory-mcp** — 43013★ · C · pushed 2026-09-12 · license MIT
  - High-performance code intelligence MCP server. Indexes codebases into a persistent knowledge graph — average repo in milliseconds. 158 languages, sub-ms queries, 99% fewer tokens. Single static binary, zero dependencies.
  - https://github.com/DeusData/codebase-memory-mcp

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->
## Eval

Evaluated 2026-09-12 for this environment: Bun/TypeScript + Python, Zo automations, the trading bot, publishing, and the Skills repository.

### tashfeenahmed/freellmapi — https://github.com/tashfeenahmed/freellmapi
Functionality: A single OpenAI-compatible gateway that aggregates free LLM providers and model endpoints, with routing and failover. It also handles provider keys and custom endpoints.
- Signals: 25,672 stars · TypeScript · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **SKIP** — it centralizes many provider credentials and duplicates Zo's model access; this exact project also caused credential-handling risk in the workspace, so it should not be installed here.

### aerovato/magic-compact — https://github.com/aerovato/magic-compact
Functionality: A lossless context-compaction plugin for Claude Code and OpenCode. It aims to reduce context size while preserving the information needed by the agent.
- Signals: 167 stars · TypeScript · BSD-3-Clause · last push 2026-08-24 · active, not archived.
- Recommendation: **TRIAL** — compare token savings and answer fidelity with `Skills/token-saver/` on representative coding sessions; keep it in a sandbox. Rough effort: 1–2 hours.

### headroomlabs-ai/headroom — https://github.com/headroomlabs-ai/headroom
Functionality: A Python library, proxy, and MCP server that compresses tool output, logs, files, and retrieval chunks before they reach an LLM. It targets lower token cost without changing application behavior.
- Signals: 71,674 stars · Python · Apache-2.0 · last push 2026-09-12 · active, not archived.
- Recommendation: **TRIAL** — benchmark it against token-saver on transcripts and large repository output, measuring savings, latency, and answer fidelity before any integration. Rough effort: 2–3 hours.

### teamchong/pxpipe — https://github.com/teamchong/pxpipe
Functionality: A Claude Code token-reduction tool that renders text context as images instead of sending all text directly. It trades a visual representation for lower textual token usage.
- Signals: 7,384 stars · TypeScript · MIT · last push 2026-09-11 · active, not archived.
- Recommendation: **TRIAL** — test image-context accuracy on code diffs and logs, especially accessibility and exact-string tasks; do not use it in production until fidelity is proven. Rough effort: 2 hours.

### jia-gao/leanctx — https://github.com/jia-gao/leanctx
Functionality: A drop-in Python prompt-compression SDK based on LLMLingua-2. It claims to reduce prompt cost by 40–60% without requiring application changes.
- Signals: 327 stars · Python · MIT · last push 2026-08-22 · active, not archived.
- Recommendation: **TRIAL** — run a small benchmark on research prompts and trading-bot backtest context, checking whether compression changes decisions. Rough effort: 2 hours.

### ooples/token-optimizer-mcp — https://github.com/ooples/token-optimizer-mcp
Functionality: An MCP server that measures token savings per coding agent, optimizes context, and shares a local knowledge graph across CLI clients. It is both an observability and context-management layer.
- Signals: 520 stars · JavaScript · MIT · last push 2026-09-11 · active, not archived.
- Recommendation: **TRIAL** — compare its measured savings and graph behavior with token-saver plus Astra memory; sandbox only until duplicate state and client permissions are understood. Rough effort: 2–3 hours.

### mksglu/context-mode — https://github.com/mksglu/context-mode
Functionality: A context-optimization layer that sandboxes tool output, persists session memory, and routes work through MCP and hooks. The scan claims up to 98% output reduction across multiple agent platforms.
- Signals: 22,276 stars · TypeScript · no declared license (NOASSERTION) · last push 2026-09-12 · active, not archived.
- Recommendation: **TRIAL** — benchmark it against token-saver and Astra memory in a disposable checkout; licensing and overlap must be resolved before adoption. Rough effort: 2–3 hours.

### DietrichGebert/ponytail — https://github.com/DietrichGebert/ponytail
Functionality: A minimalism-oriented coding-agent skill that pushes the agent to reuse existing code and avoid unnecessary implementation. Its goal is less generated code and fewer speculative changes.
- Signals: 136,233 stars · JavaScript · MIT · last push 2026-09-07 · active, not archived.
- Recommendation: **TRIAL** — test it on a small trading-bot or Skills-repo change; verify that it reduces churn without suppressing required fixes. Rough effort: 1–2 hours.

### Graphify-Labs/graphify — https://github.com/Graphify-Labs/graphify
Functionality: A Python skill that parses code, documentation, SQL schemas, configs, and PDFs into a queryable knowledge graph. It emphasizes deterministic AST-based edges instead of a vector store.
- Signals: 117,127 stars · Python · Apache-2.0 · last push 2026-09-10 · active, not archived.
- Recommendation: **TRIAL** — run it on the trading bot and Skills repository, then compare query usefulness and build time with codebase-memory-mcp. Rough effort: 2–4 hours.

### diegosouzapw/OmniRoute — https://github.com/diegosouzapw/OmniRoute
Functionality: An MIT AI gateway exposing many providers and models through one endpoint, with quota-aware fallback, MCP/A2A support, and optional token compression. It is designed to keep agent work running when a provider fails.
- Signals: 65,090 stars · TypeScript · MIT · last push 2026-09-12 · active, not archived.
- Recommendation: **TRIAL** — test routing with non-sensitive models and no production credentials; measure reliability, cost, latency, and secret-handling before considering it for Zo automations. Rough effort: 3–4 hours.

### DeusData/codebase-memory-mcp — https://github.com/DeusData/codebase-memory-mcp
Functionality: A static C binary that indexes a codebase into a persistent knowledge graph and answers code-intelligence queries. It supports many languages with low runtime overhead.
- Signals: 43,013 stars · C · MIT · last push 2026-09-12 · active, not archived.
- Recommendation: **TRIAL** — benchmark it on the trading bot and a large Skills checkout against Graphify; keep the winner only if query accuracy is materially better than current repository search. Rough effort: 2–4 hours.
