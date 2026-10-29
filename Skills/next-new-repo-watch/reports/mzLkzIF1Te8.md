# Epic Games’ RAD Debugger Fills AI’s Biggest Gap in Game Dev

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-28T20:30:17+00:00
- **Video**: https://www.youtube.com/shorts/mzLkzIF1Te8

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=Wsru44p-J14 

The RAD Debugger is an open-source, graphical debugger from Epic Games. It’s a native, user-mode, multi-process debugger that currently supports local-machine x64 debugging on Windows and Linux, with Linux support still very early. Why does it matter for AI? AI can code the games, but it’s still not great at visual debugging, performance monitoring, and performance profiling. This is a real tool built for exactly that, so you can pair your powerful coding agent with a top-tier debugger, tell the agent how to use it and where it lives, and let it do the heavy lifting. Combine it with a couple of other tools, and you could make an impressive game that would have taken around $150,000 three years ago.

#RADDebugger #EpicGames #AIAgents #GameDev #Debugging #OpenSource #AITools

🔗 GitHub: https://github.com/EpicGames/raddebugger

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=mzLkzIF1Te8! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **EpicGames/raddebugger** — 8708★ · C · pushed 2026-10-29 · license MIT
  - A native, user-mode, multi-process, graphical debugger.
  - https://github.com/EpicGames/raddebugger

## Agent eval

**Evidence note:** YouTube transcript requests were blocked from this cloud IP. This evaluation uses the Short's description plus current GitHub metadata and README; it does not claim transcript-derived facts.

### EpicGames/raddebugger — https://github.com/EpicGames/raddebugger
- Functionality: Native, user-mode, multi-process graphical debugger from Epic Games; local x64 debugging on Windows, with Linux support described as "very early."
- Signals: 8,708 stars; C; MIT; pushed 2026-10-29; not archived; README states the project is ALPHA.
- Recommendation: **SKIP** — ALPHA status, early Linux support, and a C/native debugging target that is not part of the Bun/TS, Python, or Zo automation stack in use. Revisit only if a native game or C project enters scope.

**Recommendation (episode):** SKIP — the single repo is out of scope for the current stack.
