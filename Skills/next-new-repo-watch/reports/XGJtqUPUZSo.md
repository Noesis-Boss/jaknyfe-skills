# ECC — This Skill Pack Teaches Your AI to Code the Right Way

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-28T20:30:28+00:00
- **Video**: https://www.youtube.com/shorts/XGJtqUPUZSo

## Description

Link to this week's Github Show resources: https://thenextnewthing.ai/l/github-repos-sep25

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=1fHsIveXRa8

ECC is a collection of skills and workflows that inject years of real software engineering best practices directly into your AI coding sessions. Instead of jumping straight to building a feature, it can guide Claude Code (or Codex, Cursor, and others) through proper planning mode and a TDD (test-driven development) workflow — writing the tests first, then building the code, so you can validate that it actually works before you're deep into it. It's a smart way to bring decades of hard-won engineering discipline to people who are vibe coding without that background.

#ECC #ClaudeCode #TDD #VibeCoding #DevTools

🔗 GitHub: https://github.com/affaan-m/ecc
🔗 Website: https://ecc.tools/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=XGJtqUPUZSo! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8395★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **affaan-m/ECC** — 269325★ · JavaScript · pushed 2026-09-28 · license MIT
  - The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond.
  - https://github.com/affaan-m/ECC

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

### affaan-m/ECC

Functionality: A large collection of skills and workflows for coding agents, covering planning, TDD, security, research, memory, and review. It is designed to add repeatable engineering discipline to Claude Code, Codex, Cursor, and related tools.

Signals: 269,325 stars; JavaScript; MIT; last pushed 2026-09-28; active, not archived.

Recommendation: INCLUDE — adapt the strongest workflows into the existing `Skills/zo-project-template/` and agent-contracts release gates. The workspace has already borrowed several ECC patterns, so install only narrowly selected pieces after review rather than vendoring the full bundle.

### jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without an API key or browser automation. It appears here because the watcher used it to fetch this video's transcript; it was not presented as a product in the video.

Signals: 8,395 stars; Python; MIT; last pushed 2026-09-10; active, not archived.

Recommendation: SKIP for this episode. The watcher already depends on it, so adding it again would not improve the ECC evaluation.
