# AnyPS5  — This AI Rewrites a PS5 Game to Run on Your PC

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-10-19T20:30:16+00:00
- **Video**: https://www.youtube.com/shorts/BL3UQPoPG7Y

## Description

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=Wsru44p-J14

AnyPS5 is an open-source tool that uses AI to read a PS5 game’s files and convert them into a version that runs natively on Windows or Linux. It isn’t an emulator, which is what makes it different, and it’s taking off even though it only works with one game so far. The big catch is that PS5 games are encrypted on the disc, so the tool can’t work on just any new release. The community is already debating whether this is a glimpse of where AI porting is headed or whether it will get taken down quickly, since Sony’s lawyers are almost certainly paying attention.

This video is for information only, so please respect copyright and only use software and games you have the legal right to use.

#AnyPS5 #PS5 #AI #OpenSource #GitHub #Gaming #AITools

🔗 GitHub: https://github.com/boykopovar/AnyPS5
🔗 Website: https://boykopovar.github.io/AnyPS5/

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=BL3UQPoPG7Y! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **boykopovar/AnyPS5** — 45020★ · C++ · pushed 2026-10-20 · license GPL-2.0
  - Tool for automatic PS5 executables porting to Linux and Windows
  - https://github.com/boykopovar/AnyPS5

## Agent eval

> **Transcript note**: Transcript unavailable (YouTube IP-blocked). Analysis drawn from the video description and the auto-extracted repo metadata.

### boykopovar/AnyPS5 — https://github.com/boykopovar/AnyPS5

**Functionality**: AnyPS5 uses AI to read a PS5 game's files and convert them into a version that runs natively on Windows or Linux. It is not an emulator — it rewrites the game's own code rather than emulating the console. Currently works with only one game; PS5 disc titles are encrypted, so it cannot handle new releases without a decryption step first.

**Signals**: 45,022★ · C++ · GPL-2.0 license · pushed 2026-10-20 · not archived · 4,126 forks · homepage boykopovar.github.io/AnyPS5. Extremely fast-growing (45K stars in days), but the community is already debating whether Sony's lawyers will take it down.

**Recommendation: SKIP** — Three concrete reasons. (1) **Legal risk**: any porting tool for first-party console titles sits squarely in Sony's enforcement crosshairs; this is not a risk we want attached to our infrastructure. (2) **Wrong stack**: pure C++ game-binary rewriting has zero overlap with our Bun/TS + Python environment, Zo automations, trading bot, or publishing pipeline. (3) **Narrow utility**: it works on one game and cannot handle encrypted new releases. The project may be historically interesting as an example of AI-driven binary porting, but there is nothing here to install or adapt.
