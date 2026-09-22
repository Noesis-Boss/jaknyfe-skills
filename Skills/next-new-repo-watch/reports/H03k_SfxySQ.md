# He Built an AI Tool to Help Families Facing Cancer

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-09-21T20:30:38+00:00
- **Video**: https://www.youtube.com/shorts/H03k_SfxySQ

## Description

Peter Yang open-sourced a skill called /fuck-cancer, built after his mom's own diagnosis, to help patients and caregivers navigate one of the hardest experiences a family can go through. It creates and keeps updated a practical, plain-language brief covering: patient and care-team info for quick reference during calls, the next specific actions to take, what's confirmed vs. still unclear, medical terms explained simply, and a running care log of updates and decisions. It pulls from your documents and trusted sources like the National Cancer Institute and ClinicalTrials.gov, and works with tools like Claude Code and ChatGPT/Codex — you can keep it as a local file or a shared Google Doc the whole family can use.

If this could help you or someone you love, it's free and open-source. Please share it with someone who needs it.

🔗 GitHub: https://github.com/petergyang/fuck-cancer/ 

#PatientAdvocacy #CancerSupport #AIforGood #OpenSource #CaregiverSupport  

Link to the full video: https://www.youtube.com/watch?v=klqyY5SAQvc

## Transcript

[transcript unavailable: 
Could not retrieve a transcript for the video https://www.youtube.com/watch?v=H03k_SfxySQ! This is most likely caused by:

YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.

There are two things you can do to work around this:
1. Use proxies to hide your IP address, as explained in the "Working around IP bans" section of the README (https://github.com/jdepoix/youtube-transcript-api?tab=readme-ov-file#working-around-ip-bans-requestblocked-or-ipblocked-exception).
2. (NOT RECOMMENDED) If you authenticate your requests using cookies, you will be able to continue doing requests for a while. However, YouTube will eventually permanently ban the account that you have used to authenticate with! So only do this if you don't mind your account being banned!

If you are sure that the described cause is not responsible for this error and that a transcript should be retrievable, please create an issue at https://github.com/jdepoix/youtube-transcript-api/issues. Please add which version of youtube_transcript_api you are using and provide the information needed to replicate the error. Also make sure that there are no open issues which already describe your problem!]

## Auto-extracted repos

- **jdepoix/youtube-transcript-api** — 8353★ · Python · pushed 2026-09-10 · license MIT
  - This is a python API which allows you to get the transcript/subtitles for a given YouTube video. It also works for automatically generated subtitles and it does not require an API key nor a headless browser, like other selenium based solutions do!
  - https://github.com/jdepoix/youtube-transcript-api
- **petergyang/fuck-cancer** — 144★ · Python · pushed 2026-08-26 · license MIT
  - Create and update a practical brief to help patients and caregivers advocate for themselves.
  - https://github.com/petergyang/fuck-cancer

## Agent eval

<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: 
     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). 
     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, 
     trading bot, publishing pipeline. -->

## Eval

Transcript retrieval was blocked by YouTube for this run. The description identifies the featured repository directly.

### petergyang/fuck-cancer — https://github.com/petergyang/fuck-cancer

Functionality: A Python/Markdown workflow that turns a patient's documents and trusted medical sources into a plain-language care brief. It tracks care-team details, next actions, confirmed versus unclear information, explanations, and a running care log for patients and caregivers.

- Signals: 144 stars · Python · MIT · last push 2026-08-26 · active, not archived.
- Recommendation: **TRIAL** — test it in a fully separate, non-production workspace using synthetic medical records; check source citations, document handling, update behavior, and whether the resulting brief preserves uncertainty. Rough effort: 2–4 hours. Do not connect real health data or treat generated content as medical advice without a human care team.

### jdepoix/youtube-transcript-api — https://github.com/jdepoix/youtube-transcript-api

Functionality: Python API for retrieving manual and auto-generated YouTube subtitles without an API key or browser automation. It is the transcript backend used by this watcher.

- Signals: 8,353 stars · Python · MIT · last push 2026-09-10 · active, not archived.
- Recommendation: **INCLUDE** — retain it as the watcher’s transcript dependency; this run confirms the dependency is useful even though YouTube blocked the server IP.
