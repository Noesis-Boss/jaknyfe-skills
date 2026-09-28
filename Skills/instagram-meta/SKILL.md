---
name: instagram-meta
description: "Read and publish to Instagram via the Meta Graph API (Content Publishing API). Use when: posting images, Reels, or carousels to Instagram, checking the IG account or publishing quota, pulling post reach/engagement insights, or reading comments. No third-party app needed."
compatibility: Requires an Instagram Business or Creator account linked to a Facebook Page, plus a Meta access token stored in Settings > Advanced as INSTAGRAM_ACCESS_TOKEN.
metadata:
  author: jaknyfe.zo.computer
---

# Instagram via Meta Graph API

Direct Instagram access from Zo. No Pipedream catalog app exists for Instagram
publishing — this skill calls the Graph API directly.

## What works today in Zo

- **Facebook Pages** integration: page posts and comments (separate path).
- **`social_fetch` integration**: Instagram *read* only (profile, posts, reels search).
- **This skill**: Instagram *read + write* — profile, media list, insights, comments,
  publishing quota, image/Reel/carousel publishing, deletion, token refresh.

## Account requirements

The Instagram Graph API only works on **Business** or **Creator** accounts, and the
account must be **linked to a Facebook Page**. Personal (@username only) accounts cannot
use this API at all — switching to Creator in the app is free and takes about a minute.

## Setup (Don does these steps once)

1. Instagram app on phone → Profile → Settings → Account type and tools → switch to
   **Creator** (or Business) if currently Personal. Then Settings → Account → Link
   accounts → link the Facebook Page.
2. Meta for Developers → create/select an app → Facebook Login for Business → add
   `INSTAGRAM_ACCESS_TOKEN` to [Settings > Advanced](/?t=settings&s=advanced) as a secret.
3. Run `check` to confirm. The script prints the exact missing scope if the token is
   short on permissions.

Required scopes: `instagram_basic`, `instagram_content_publish`, `pages_show_list`,
`pages_read_engagement`, and `instagram_manage_insights` for `insights`.

Reading comments is **not** implemented here — use the connected `social_fetch` app for
Instagram reads, or ask before adding a `comments` command.

## Commands

Run from `/home/workspace`:

```
bun run Skills/instagram-meta/scripts/instagram.ts <command> [options]
```

| Command | What it does |
|---|---|
| `check` | Validate token, print IG user, account type, publishing quota |
| `profile` | Username, follower count, bio, website, media count |
| `posts --limit 10` | Recent media with type, caption, permalink, timestamp |
| `insights <MEDIA_ID>` | Reach, likes, comments, saves, shares, total interactions |
| `quota` | Containers published in the last 24h vs the 50/24h limit |
| `post --url <PUBLIC_IMAGE_URL> --caption <TEXT>` | Publish a single-image feed post |
| `reel --url <PUBLIC_MP4_URL> --caption <TEXT>` | Publish a Reel (≤ 15 min) — polls, then publishes |
| `carousel --url <U1> --url <U2> [--url <U3>...] --caption <TEXT>` | Publish 2–10 images in one post |
| `status <CREATION_ID>` | Container processing state (`FINISHED` / `ERROR`) |
| `delete <MEDIA_ID>` | Delete a published post |
| `refresh` | Exchange for a new long-lived token (~60 days; prints it once) |

Every command prints JSON on stdout. `--id <IGSID>` targets a specific account.
Media IDs, container IDs, and refresh output are secrets — never paste them into chat, a
file, or Git.

## Media hosting rules

Meta fetches media from **publicly reachable URLs** over HTTP. It will not read from
`/home/workspace` and it will not accept a session-authenticated Zo route.

- Already public: pass the URL straight through (`https://news.noesisgroup.com/logo.jpeg`).
- Local file: upload it first, then pass the public URL.
  ```bash
  zopub sync ig-media <source-dir>
  # → https://zo.pub/jaknyfe/ig-media/photo.jpg
  ```
  For a public Zo site, the file is already reachable at its asset path.

## Reel requirements

H.264 + AAC MP4, 3 s–15 min, under 1 GB, no watermark. Meta processes asynchronously:
`reel` returns a container ID immediately, then polls for up to 5 minutes, then publishes.
Keep terminal output open for the whole poll.

## Common errors

| Error | Cause | Fix |
|---|---|---|
| `OAuthException: (#190)` | Token expired (short-lived, or 60-day long-lived lapsed) | `refresh`, or re-authorize and replace the secret |
| `(#10)` / `Unsupported get request` | Graph API version too new for the app | Set `INSTAGRAM_API_VERSION=v23.0` in [Settings > Advanced](/?t=settings&s=advanced) |
| `(#200)` | Account is Personal, or not linked to a Page | Switch to Creator, link the Page |
| `subcode 2207085` | Known Meta-side Reel publish bug (images work) | Fall back to carousel of frames, or publish via the app |
| `ImageDownloadError` | URL is not publicly fetchable, or file > 8 MB | Verify with `curl -I`, re-host publicly |

## Quota

50 published containers per rolling 24 hours. A carousel counts as one. Stories and
comment replies count against the same bucket. Check before batch posting: `quota`.

## Hard rules

- Never paste a token, media ID, or container ID into chat, a file, or Git. They live only
  in [Settings > Advanced](/?t=settings&s=advanced) or in that command's own stdout.
- Confirm with Don before publishing anything to a live account. Draft locally, show the
  caption and media path, then post only on an explicit go.
- Reels publish immediately once processing finishes. There is no undo other than
  `delete <MEDIA_ID>`.
