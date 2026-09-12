#!/usr/bin/env python3
"""Regenerate RECOMMENDATIONS.md index from per-video eval reports.

Parses reports/*.md (skipping digest-*), extracts per-repo verdicts
(### repo-name sections with "Recommendation: INCLUDE/TRIAL/SKIP"),
and writes a linked index with GitHub repo links, report paths, and
YouTube video links. Rerun after each eval batch.
"""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPORTS = SKILL / "reports"
OUT = SKILL / "RECOMMENDATIONS.md"
CHANNEL = "UCNZEktrsM5oJZ-MK4jKPMOQ"

VERDICTS = ("INCLUDE", "TRIAL", "SKIP")


def parse_report(path: Path):
    text = path.read_text(errors="replace")
    m = re.match(r"#\s*(.+)", text)
    title = m.group(1).strip() if m else path.stem
    title = re.sub(r"^New:\s*", "", title)

    repos = []
    sections = re.split(r"\n###\s+", text)
    for sec in sections[1:]:
        lines = sec.split("\n")
        name = re.sub(r"\*{1,2}", "", lines[0].strip()).strip()
        if "/" not in name or name.startswith(("http", "!")):
            continue
        name = name.strip("*").strip()
        blob = "\n".join(lines[1:])
        vm = re.search(r"\*\*Recommendation:\s*(INCLUDE|TRIAL|SKIP)\b", blob)
        verdict = vm.group(1) if vm else "PENDING"
        dm = re.search(r"\[([^\]]+)\]\((https://github\.com/[^)]+)\)", blob)
        if dm:
            url = dm.group(2)
        else:
            um = re.search(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", blob)
            if um:
                url = um.group(0).rstrip(".,)")
            else:
                url = f"https://github.com/{name}"
        desc = ""
        for ln in lines[1:]:
            ln = ln.strip()
            if ln and not ln.startswith(("**", "-", "!", "#")):
                desc = ln
                break
        repos.append({"name": name, "verdict": verdict, "url": url, "desc": desc})
    return {"vid": path.stem, "title": title, "repos": repos, "pending": verdict_pending(text)}


def verdict_pending(text: str) -> bool:
    return "Recommendation:" not in text


def main():
    rows = []
    for p in sorted(REPORTS.glob("*.md")):
        if p.stem.startswith("digest-"):
            continue
        rows.append(parse_report(p))

    counts = {"INCLUDE": 0, "TRIAL": 0, "SKIP": 0, "PENDING": 0}
    for r in rows:
        for repo in r["repos"]:
            counts[repo["verdict"]] = counts.get(repo["verdict"], 0) + 1
        if not r["repos"]:
            counts["PENDING"] += 1

    lines = [
        "# Next New Thing — Repo Recommendations",
        "",
        f"Auto-generated from `reports/` by `scripts/summary.py`. Last run: {__import__('datetime').date.today().isoformat()}.",
        "",
        f"**Totals**: {counts['INCLUDE']} INCLUDE · {counts['TRIAL']} TRIAL · {counts['SKIP']} SKIP · {counts['PENDING']} pending eval",
        "",
    ]
    for verdict in ("INCLUDE", "TRIAL"):
        lines.append(f"## {verdict}")
        lines.append("")
        any_row = False
        for r in rows:
            for repo in r["repos"]:
                if repo["verdict"] != verdict:
                    continue
                any_row = True
                repo_link = repo["url"] or repo["name"]
                video = f"https://youtu.be/{r['vid']}"
                report = f"reports/{r['vid']}.md"
                desc = repo["desc"][:140]
                lines.append(
                    f"- **[{repo['name']}]({repo_link})** — {desc}\n"
                    f"  - Report: `{report}` · Video: {video} · *{r['title']}*"
                )
        if not any_row:
            lines.append("_(none)_")
        lines.append("")

    lines.append("## SKIP")
    lines.append("")
    for r in rows:
        for repo in r["repos"]:
            if repo["verdict"] != "SKIP":
                continue
            repo_link = repo["url"] or repo["name"]
            lines.append(f"- [{repo['name']}]({repo_link}) — `reports/{r['vid']}.md`")
    lines.append("")

    pend = [r for r in rows if r["pending"] or any(x["verdict"] == "PENDING" for x in r["repos"])]
    if pend:
        lines.append("## Pending eval")
        lines.append("")
        for r in pend:
            lines.append(f"- `reports/{r['vid']}.md` — {r['title']} ({len(r['repos'])} repos)")
        lines.append("")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT} — {len(rows)} videos, INCLUDE={counts['INCLUDE']} TRIAL={counts['TRIAL']} SKIP={counts['SKIP']} PENDING={counts['PENDING']}")


if __name__ == "__main__":
    sys.exit(main())
