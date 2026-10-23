# This AI Tool Can Rebuild Apps — But Is It Copying?

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-22T20:30:22+00:00
- **Video**: https://www.youtube.com/shorts/ZgAG5v_QPt4

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

🔗 Watch the full podcast here: https://youtu.be/BctbCJP9lKU

What if you could recreate your favorite software using AI?

REA (Reverse Engineer Anything) lets AI coding agents inspect how existing applications work and rebuild their features.

Andrew Warner reacts to a CapCut-inspired video editor built using REA and explores an interesting question: When does copying software become creating something new?

🔗 Explore REA Tools: https://rea.tools/

#ai  #REATools #reverseengineering  #claudecode  #softwaredevelopment

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=ZgAG5v_QPt4! This is most likely caused by:

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

### morluto/rea — REA (Reverse Engineer Anything)
- **Functionality**: MCP toolchain that lets AI coding agents inspect how existing applications work and rebuild their features, from app behavior down to native binaries. Targets Claude Code / agent workflows for reverse-engineering software.
- **Signals**: 370,279★ · TypeScript · MIT · pushed 2026-10-23 · not archived · homepage rea.tools.
- **Recommendation**: TRIAL — large community and MIT license, but the tool grants an agent broad reverse-engineering/shell-style access to inspect and rebuild apps, so it must not be INCLUDE'd outright. Sandbox-test on a throwaway project first: verify what it actually reads/writes, confirm no credential leakage, and check whether it duplicates work already doable with our existing Claude Code setup. Effort: ~1-2 hours.
- Related derivatives surfaced by search (not directly presented): `JoasASantos/REA-Prompts` (1,577★, no license) prompt pack for REA; `aicodeking/leanrea` (1,564★, MIT, Python) claims a lighter 8 KB skill replacement benchmarked 38% faster/35% cheaper — worth a side-by-side comparison during the trial.
