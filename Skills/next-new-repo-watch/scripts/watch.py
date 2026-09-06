#!/usr/bin/env python3
"""Watch The Next New Thing (YouTube) for new videos, pull transcripts,
extract GitHub repos, and emit per-video report stubs for agent evaluation.

Zero-dependency (stdlib + youtube_transcript_api for transcripts).

Commands:
  scan              Find new videos, fetch transcripts, write report stubs, update state.
  scan --dry-run    Show new videos without fetching or updating state.
  status            Print state summary (processed videos, report paths).
  refetch <vid>     Re-fetch transcript + rewrite stub for one video (state untouched).
"""
import argparse
import json
import re
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
STATE_FILE = SKILL_DIR / "state.json"
REPORTS_DIR = SKILL_DIR / "reports"
CHANNEL_ID = "UCNZEktrsM5oJZ-MK4jKPMOQ"
CHANNEL_NAME = "The Next New Thing (Andrew Warner)"
RSS_URL = f"https://www.youtube.com/feeds/videos.xml?channel_id={CHANNEL_ID}"

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}

GH_REPO_RE = re.compile(
    r"(?:https?://)?(?:www\.)?github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)"
)


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": {}}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2) + "\n")


def fetch_rss():
    req = urllib.request.Request(RSS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return ET.fromstring(r.read())


def list_entries(root):
    out = []
    for e in root.findall("a:entry", NS):
        vid = e.find("yt:videoId", NS).text
        title = e.find("a:title", NS).text
        published = e.find("a:published", NS).text
        link = e.find("a:link", NS).attrib.get("href", f"https://youtu.be/{vid}")
        desc_el = e.find("media:group/media:description", NS)
        desc = (desc_el.text or "") if desc_el is not None else ""
        out.append({"id": vid, "title": title, "published": published, "link": link, "description": desc})
    return out


def fetch_transcript(video_id):
    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        api = YouTubeTranscriptApi()
        t = api.fetch(video_id)
        return " ".join(seg.text for seg in t)
    except Exception as exc:
        return f"[transcript unavailable: {exc}]"


def extract_github_repos(text):
    """Return normalized owner/repo strings from raw text."""
    found = []
    for m in GH_REPO_RE.finditer(text):
        owner, repo = m.group(1), m.group(2)
        if repo.endswith(".git"):
            repo = repo[:-4]
        if owner.lower() in {"topics", "trending", "features", "about", "pricing", "sponsors"}:
            continue
        pair = f"{owner}/{repo}"
        if pair not in found:
            found.append(pair)
    return found


def gh_repo_meta(owner_repo):
    """Fetch repo metadata via gh CLI. Returns dict or None."""
    try:
        raw = subprocess.run(
            [
                "gh", "api", f"repos/{owner_repo}",
                "--jq", '{"full_name":.full_name,"description":.description,'
                '"stars":.stargazers_count,"language":.language,'
                '"pushed_at":.pushed_at,"license":.license.spdx_id,'
                '"archived":.archived,"url":.html_url}',
            ],
            capture_output=True, text=True, timeout=30,
        )
        if raw.returncode == 0:
            return json.loads(raw.stdout)
    except Exception:
        pass
    return None


def report_path(video_id):
    return REPORTS_DIR / f"{video_id}.md"


def write_stub(entry, transcript):
    REPORTS_DIR.mkdir(exist_ok=True)
    repos = extract_github_repos(transcript + "\n" + entry["description"])
    lines = [
        f"# {entry['title']}",
        "",
        f"- **Channel**: {CHANNEL_NAME}",
        f"- **Published**: {entry['published']}",
        f"- **Video**: {entry['link']}",
        "",
        "## Description",
        "",
        entry["description"] or "(empty)",
        "",
        "## Transcript",
        "",
        transcript,
        "",
        "## Auto-extracted repos",
        "",
    ]
    if repos:
        for r in repos:
            meta = gh_repo_meta(r)
            if meta:
                lines.append(
                    f"- **{meta['full_name']}** — {meta['stars']}★ · {meta['language'] or '?'} · "
                    f"pushed {meta['pushed_at'][:10]} · license {meta['license'] or 'none'}"
                    f"{' · ARCHIVED' if meta['archived'] else ''}\n"
                    f"  - {meta['description'] or '(no description)'}\n"
                    f"  - {meta['url']}"
                )
            else:
                lines.append(f"- `{r}` (metadata fetch failed — verify manually)")
    else:
        lines.append("(none auto-extracted — read the transcript above and identify repo names, then search GitHub)")
    lines += [
        "",
        "## Agent eval",
        "",
        "<!-- For each repo: functionality (1-2 sentences), stats, and a recommendation: ",
        "     INCLUDE (install/adapt now) / TRIAL (worth testing) / SKIP (with reason). ",
        "     Tie recommendations to this environment: Bun/TS + Python stack, Zo automations, ",
        "     trading bot, publishing pipeline. -->",
        "",
    ]
    p = report_path(entry["id"])
    p.write_text("\n".join(lines))
    return p, repos


def cmd_scan(args):
    state = load_state()
    entries = list_entries(fetch_rss())
    new = [e for e in entries if e["id"] not in state["processed"]]
    if not new:
        print("No new videos.")
        return
    print(f"{len(new)} new video(s):")
    for e in new:
        print(f"  - {e['id']} | {e['title']} | {e['published'][:10]}")
    if args.dry_run:
        return
    for e in new:
        print(f"Processing {e['id']}…")
        transcript = fetch_transcript(e["id"])
        path, repos = write_stub(e, transcript)
        state["processed"][e["id"]] = {
            "title": e["title"],
            "published": e["published"],
            "processed_at": datetime.now(timezone.utc).isoformat(),
            "report": str(path),
            "auto_repos": repos,
        }
        print(f"  report: {path}")
        print(f"  auto-extracted: {', '.join(repos) if repos else '(none)'}")
    save_state(state)
    print(f"State updated: {len(state['processed'])} videos processed total.")


def cmd_status(_args):
    state = load_state()
    print(f"Processed videos: {len(state['processed'])}")
    for vid, info in sorted(state["processed"].items(), key=lambda kv: kv[1]["published"], reverse=True)[:10]:
        print(f"  {info['published'][:10]} | {vid} | {info['title'][:60]} | {info['report']}")


def cmd_refetch(args):
    state = load_state()
    entries = {e["id"]: e for e in list_entries(fetch_rss())}
    if args.vid not in entries:
        print(f"Video {args.vid} not in feed.", file=sys.stderr)
        sys.exit(1)
    e = entries[args.vid]
    path, repos = write_stub(e, fetch_transcript(e["id"]))
    print(f"Stub rewritten: {path} (repos: {', '.join(repos) if repos else 'none'})")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="scan for new videos and process them")
    s.add_argument("--dry-run", action="store_true")
    sub.add_parser("status", help="show processed history")
    r = sub.add_parser("refetch", help="re-fetch one video's transcript stub")
    r.add_argument("vid")
    args = ap.parse_args()
    {"scan": cmd_scan, "status": cmd_status, "refetch": cmd_refetch}[args.cmd](args)


if __name__ == "__main__":
    main()
