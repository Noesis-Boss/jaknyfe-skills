---
name: last30days
version: "3.0.0"
description: "Multi-query social search with intelligent planning. Agent plans queries when possible, falls back to Gemini/OpenAI when not. Research any topic across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web."
argument-hint: 'last30days-3 AI video tools, last30days-3 best noise cancelling headphones'
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
homepage: https://github.com/mvanhorn/last30days-skill
repository: https://github.com/mvanhorn/last30days-skill
author: mvanhorn
license: MIT
user-invocable: true
metadata:
  openclaw:
    emoji: "📰"
    requires:
      env:
        - SCRAPECREATORS_API_KEY
      optionalEnv:
        - OPENAI_API_KEY
        - XAI_API_KEY
        - OPENROUTER_API_KEY
        - PARALLEL_API_KEY
        - BRAVE_API_KEY
        - APIFY_API_TOKEN
        - AUTH_TOKEN
        - CT0
        - BSKY_HANDLE
        - BSKY_APP_PASSWORD
        - TRUTHSOCIAL_TOKEN
      bins:
        - node
        - python3
    primaryEnv: SCRAPECREATORS_API_KEY
    files:
      - "scripts/*"
    homepage: https://github.com/mvanhorn/last30days-skill
    tags:
      - research
      - deep-research
      - reddit
      - x
      - twitter
      - youtube
      - tiktok
      - instagram
      - hackernews
      - polymarket
      - bluesky
      - truthsocial
      - trends
      - recency
      - news
      - citations
      - multi-source
      - social-media
      - analysis
      - web-search
      - ai-skill
      - clawhub
---

# last30days v3.0.0: Research Any Topic from the Last 30 Days

## ⚠️ X/Twitter Credentials: OAuth Keys vs Cookie Auth

The `bird` search client used by last30days for X/Twitter uses **cookie-based auth** (`auth_token` + `ct0` cookies). It does **NOT** support OAuth 1.0a keys. If you have OAuth credentials stored in **Zo Settings → Advanced → Secrets** (e.g. `X_OAUTH1_API_KEY`, `X_OAUTH1_ACCESS_TOKEN`, `X_OAUTH1_ACCESS_TOKEN_SECRET`, `X_OAUTH2_CLIENT_ID`, `X_OAUTH2_CLIENT_SECRET`), they **cannot be used directly** by last30days.

**Options to unlock X search:**

| Option | What to store in Zo Secrets | Notes |
|--------|---------------------------|-------|
| Cookie auth (recommended) | `AUTH_TOKEN` + `CT0` | Extract from browser DevTools → Application → Cookies → x.com |
| xAI API key | `XAI_API_KEY` | No browser needed; get at api.x.ai |
| Zo built-in tool | (none — just use `x_search`) | Works automatically; no skill credential setup needed |

**To extract cookies from your browser session:**
1. Log into x.com in Chrome or Firefox
2. Open DevTools (F12) → Application → Cookies → `https://x.com`
3. Copy `auth_token` and `ct0` values
4. Store as `AUTH_TOKEN` and `CT0` in **Zo Settings → Advanced → Secrets**

Use `last30days` when the user wants recent, cross-source evidence from the last 30 days.