---
name: meerkat-mcp
description: Meerkat (getmeerkat.dev) prompt-engineering MCP — evaluation, auth flow, and discovered server-side bug
type: project
---

# Meerkat MCP — evaluation, auth, and blocker

**Vendor:** Schmade (https://getmeerkat.dev)
**MCP endpoint:** https://getmeerkat.dev/api/mcp (Streamable HTTP, OAuth 2.0 + PKCE)
**Backend:** Supabase (project ref `voqipssxofhwnsrbutnf`)

## What Meerkat is

Prompt engineering service. Three frontier models (Gemini 3.1 Pro, Claude Opus 4.8, GPT-5.5) generate and judge prompts; user gets the best result. Five MCP tools: `list_projects`, `search_shelf`, `chat_with_meerkat`, `refactor_prompt`, `auto_file`.

## Auth — what works, what doesn't

**MCP server (the official connector path) — paywalled.** `https://getmeerkat.dev/api/mcp` requires a Supabase JWT with `tier != free` on Don's account. Auth succeeded as `delowery@gmail.com`, tool listing worked, but every tool call returned the Pro upgrade message. Confirmed it's the same paywall on all 5 tools (including read-only `list_projects` and `search_shelf`).

**Web app session cookie — works.** Captured via agent-browser magic-link sign-in. Cookies: `__stripe_mid`, `__stripe_sid`, `sb-voqipssxofhwnsrbutnf-auth-token`. Web app `/api/*` routes accept this cookie, no paywall. Don't have to add the Meerkat Pro subscription.

**Free-tier caps on web API:** 300 `chatTurns` per cycle, 40 `promptRuns` per cycle. `unlimited: false`. Server charges quota even on 500 errors — important caveat if this ever gets wired into an automation.

## Working endpoints (verified)

| Route | Method | Result |
|---|---|---|
| `/api/usage` | GET | returns tier, signedIn, caps, used counters |
| `/api/teams/mine` | GET | returns `{teams:[]}` |
| `/api/roast` | POST | works. Returns `{token, severity, headline, subhead, burns[], why, fix, lesson, lesson_link, used}` |
| `/api/custom-chat` | POST | **500 server error on every call** — see Blocker |

## Discovered route surface (17 routes in the SPA bundles)

`/api/custom-chat`, `/api/roast`, `/api/head-to-head`, `/api/save-prompt`, `/api/auto-file`, `/api/delete-prompt`, `/api/share`, `/api/data`, `/api/usage`, `/api/verify`, `/api/teams/mine`, `/api/teams/upsert`, `/api/teams/members`, `/api/track-visit`, `/api/followup-message`, `/api/init-prompt`, `/api/gallery`.

Model slugs accepted: `anthropic/claude-sonnet-4.6`, `anthropic/claude-opus-4.8`, `openai/gpt-5.5`, `google/gemini-3.1-pro`.

## Blocker: `/api/custom-chat` returns 500

Every request returns:
```json
{"message":"Meerkat hit a snag finishing that turn: Cannot read properties of undefined (reading 'map'). Your message is safe; give it another go."}
```

- Happens with all 4 model slugs
- Happens with minimal `{messages:[{role:'user', content:'hi'}]}` payload
- Server increments `chatTurns` counter anyway
- **Same generic 500 the docs example returns** — looks like a real production bug on Schmade's side, not a wrong API shape
- Likely tied to the free tier: chatTurns is being recorded but the multi-model-judge pipeline is erroring out

## Decision: don't ship as a skill

Two strikes:
1. MCP path is paywalled
2. Free web path is broken on the main endpoint

What works (`/api/roast`) is too narrow to justify a full skill on its own. Could revisit if:
- Don upgrades to Pro and the MCP path opens up
- Schmade fixes the `/api/custom-chat` 500
- A narrower workflow is identified (e.g. just "roast any prompt I write")

## Artifacts left in /tmp (may be auto-cleaned)

- `/tmp/meerkat_api.py` — Python client (cookie-based, 5 working functions)
- `/tmp/meer_chunks/` — Next.js JS bundles for endpoint discovery
- Cookies in agent-browser session only; not persisted to workspace

## Reconnect steps if picking this back up

1. `agent-browser open https://getmeerkat.dev/auth/sign-in` (or click SIGN IN on home)
2. Switch to MAGIC LINK tab
3. Fill `delowery@gmail.com`, submit — magic link arrives in inbox
4. Click magic link IN THE SAME BROWSER (don't paste URL into a different session — token binds to browser)
5. Land on `/library`, run `document.cookie` in eval to grab the `sb-voqipssxofhwnsrbutnf-auth-token` value
6. Test `/api/custom-chat` first — if it still 500s, the bug is unresolved
