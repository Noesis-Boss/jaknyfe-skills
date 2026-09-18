# Your Own Private Google Photos — Self-Hosted

- **Channel**: The Next New Thing (Andrew Warner)
- **Published**: 2026-08-28T20:30:19+00:00
- **Video**: https://www.youtube.com/shorts/zjvSs1VNDSQ

## Description

Immich is a self-hosted photo and video backup app you run on your own server — giving you an Apple Photos or Google Photos-style experience without a big tech company hosting your memories. Install the app on Android or iPhone and sync your photos and videos straight to your own hardware instead. It's mature, works really well, and is a great pick if you're already moving away from services like Dropbox for your files. 

#Immich #SelfHosted #Privacy #OpenSource #DevTools 

Link to the Resource Vault: https://thenextnewthing.ai/Resources
(There is also a clickable link in my bio)

Link to the full video: https://www.youtube.com/watch?v=tX9ANddpAqc 

🔗 GitHub: https://github.com/immich-app/immich
🔗 Website: https://immich.app/

## Transcript

Your own private Google photos running on your server? Image is a self-hosted photo and video backup app you run on your own hardware. If you want something that is a bit like the Apple Photos experience, but you don't want Apple to be hosting that for you, you can run Image on your own server. You can install the app on your Android and iPhone, and then sync your photos and videos up to your own personal server instead. I know this is something that you've spoken about before that you were looking into, you know, hosting your own files and stuff like that without relying on things like Dropbox. This is the same idea but for photos and videos. You know, it's very mature, it works very well. >> So, it's something that people might want to do. Download it in the link in the bio.

## Auto-extracted repos

- **immich-app/immich** — 113505★ · TypeScript · pushed 2026-09-06 · license AGPL-3.0
  - High performance self-hosted photo and video management solution.
  - https://github.com/immich-app/immich

## Agent eval

**immich-app/immich** — Self-hosted Google Photos / Apple Photos replacement: mobile apps auto-backup photos and videos to your own server, with ML face/object search, albums, sharing, and a web timeline. Ships as a Docker Compose stack (server + Postgres + Redis + ML container), not a library.
- **Signals**: 113,507★ · TypeScript · AGPL-3.0 · pushed 2026-09-06 (same day) · not archived · very active.
- **Recommendation**: TRIAL — mature and active, and it matches Don's self-hosting/privacy direction plus photo-heavy media work (memorial slideshows, video stills, book covers), but it is a standalone server product: no integration point for the Bun/TS + Python stack, Zo automations, trading bot, or zo.space routes, and its Docker+Postgres+ML stack is too heavy for the Zo sandbox. Worth trialing on dedicated hardware (home server/NAS), not in this environment.
Recommendation: TRIAL
- Video verdict: single-repo feature short; no other evaluable repos presented.

## Eval

- **immich-app/immich** — TRIAL | Self-hosted Google Photos replacement (TS/Python, very active). Genuine value: private photo/video backup from phones to your Debian server. Cost: real storage + Docker infra. Recommend a trial only if you want phone-photo backup off Google; otherwise skip — it's a household infra project, not a workflow tool.

## Recommendation
TRIAL — worth standing up only if getting family photos off Google Photos is a goal. High storage/compute cost, high personal value.
