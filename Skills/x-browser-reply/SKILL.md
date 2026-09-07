---
name: x-browser-reply
description: Find follow-back (f4f) posts on X and reply + follow via browser automation (agent-browser), NOT the X API. Requires a logged-in X session via cookies.json or --restore session.
metadata:
  author: jaknyfe.zo.computer
---

# x-browser-reply

Rebuilt 2026-09-07 after the workspace deletion incident (original lost ~2026-09-05). Browser-automation path by design — avoids the X API integration.

## Scripts

- `scripts/find_follow_back.py --max 5` — finds f4f posts (agent-browser search; returns [] if not logged in). Falls back to web_search queries in the SKILL description: `site:x.com "I follow back"` etc., extract `x.com/USER/status/ID`.
- `scripts/reply.py --tweet-id ID --text "..." [--user NAME] [--cookies cookies.json | --restore NAME]` — opens `x.com/intent/reply?tweet_id=...`, types, submits, verifies. Exit 2 = not logged in.
- `scripts/follow.py --username NAME [--cookies ... | --restore NAME]` — opens profile, clicks Follow button, verifies "Following".

## Session (required)

Scripts use agent-browser, which does NOT share Zo's browser session. Two options:

1. `--cookies /home/workspace/Skills/x-browser-reply/cookies.json` — export cookies from a logged-in browser session (Netscape/cURL/JSON cookie-header formats all accepted via `agent-browser cookies set --curl`).
2. Sign in once inside agent-browser and persist: `agent-browser --restore x-jak session` — cookies auto-save/restore per session name.

Fallback account: `cookies_zdsentry.json` / `--restore x-zds`.

## Rules

- Max 5 posts/day. Relevant (non-generic) reply text. Follow AFTER replying. 2–3s delays. Skip jak_nyfe/zdsentry posts. Track processed IDs in `processed_tweets.json`.
