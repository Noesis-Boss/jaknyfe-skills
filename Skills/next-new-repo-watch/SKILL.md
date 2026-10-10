---
name: next-new-repo-watch
description: Watches "The Next New Thing" (Andrew Warner) and GitHub Trending Digest YouTube channels for new videos, extracts GitHub repos from transcripts/descriptions, and produces per-repo eval reports with INCLUDE/TRIAL/SKIP recommendations. Use when asked to check for new videos, evaluate showcased repos, or run the repo watch.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  channels:
    - UCNZEktrsM5oJZ-MK4jKPMOQ
    - UCApTsoLsKHl-tVhWKNupUKw
---
# next-new-repo-watch

Watches **The Next New Thing** (Andrew Warner's YouTube show that demos open-source repos) and **GitHub Trending Digest**, turning each new video into a repo eval report.

## How it works

1. `scripts/watch.py scan` reads the configured channel RSS feed. Pass one or more `--channel CHANNEL_ID CHANNEL_NAME` pairs to scan multiple channels in one run; without them it defaults to The Next New Thing. YouTube caps each feed at the 15 most recent videos, so run daily to avoid missing videos.
2. New video IDs from all selected feeds are deduplicated and diffed against the shared `state.json`; report stubs retain the source channel name.
3. For each new video: transcript is fetched, `github.com/owner/repo` URLs are auto-extracted, and a report stub is written to `reports/<videoId>.md` containing description, transcript, and repo metadata (stars, language, license, last push via `gh`).
4. The agent then completes the eval (see below).

## Commands

```bash
python3 Skills/next-new-repo-watch/scripts/watch.py scan --channel UCNZEktrsM5oJZ-MK4jKPMOQ "The Next New Thing (Andrew Warner)" --channel UCApTsoLsKHl-tVhWKNupUKw "GitHub Trending Digest (@GitHubTrendingDigest)"
python3 Skills/next-new-repo-watch/scripts/watch.py scan --dry-run --channel UCNZEktrsM5oJZ-MK4jKPMOQ "The Next New Thing (Andrew Warner)" --channel UCApTsoLsKHl-tVhWKNupUKw "GitHub Trending Digest (@GitHubTrendingDigest)"
python3 Skills/next-new-repo-watch/scripts/watch.py status          # processed history
python3 Skills/next-new-repo-watch/scripts/watch.py refetch <vid> --channel <id> <name>  # redo one stub
python3 Skills/next-new-repo-watch/scripts/summary.py   # rebuild RECOMMENDATIONS.md index (links + verdicts)
```

## Agent eval step (required — the stub is not the deliverable)

For each report stub in `reports/`:

1. **Read the transcript.** Warner usually names repos conversationally ("outbid.lol", "Hermes Agent") without saying the full GitHub URL. Identify every repo presented, then find each on GitHub with `gh search repos "<name>" --limit 5 --json fullName,description,stargazersCount` or web search. Add found repos to the report.
2. **Eval each repo** in the report's "Agent eval" section:
   - **Functionality**: 1–2 plain sentences — what it does, what problem it solves.
   - **Signals**: stars, language, license, last push, maintained/archived.
   - **Recommendation**, one of:
     - **INCLUDE** — install/adapt now; name where it plugs in (e.g. trading bot, Zo automation, publishing pipeline, Skills repo).
     - **TRIAL** — worth a sandbox test; say what to test and rough effort.
     - **SKIP** — with one concrete reason (wrong stack, maintenance risk, overlaps existing tooling, security concerns).
3. **Deliverable**: a digest file `reports/digest-<YYYY-MM-DD>.md` summarizing all repos from all videos processed this run, sorted by recommendation (INCLUDE first). State where repo identity was uncertain.
4. Mark the videos' state only via `watch.py scan` (it handles state automatically). Do not hand-edit `state.json`.

## Rules of thumb for recommendations

- Prefer Bun/TypeScript or Python tools that drop into existing projects (robinhood-trading-bot, Skills, publishing, zo.space).
- Archived repos, zero stars AND zero releases, or no license → default SKIP unless the transcript shows something exceptional.
- Overlap with an existing installed skill → SKIP and name the existing one.
- Anything that wants to run an agent with shell access → TRIAL, never INCLUDE outright.

## Dependency

Transcripts require `youtube_transcript_api` (`pip install youtube-transcript-api`). Verify with `python3 -c "import youtube_transcript_api"`.
