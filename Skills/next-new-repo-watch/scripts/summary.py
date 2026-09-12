#!/usr/bin/env python3
"""Regenerate RECOMMENDATIONS.md index from per-video eval reports.

Parses reports/*.md (skipping digest-*), extracts per-repo verdicts from
all eval formats found in the reports (### sections with Recommendation /
Verdict lines, and bullet items with inline or Verdict verdicts), and
writes a linked index with GitHub repo links, report paths, and YouTube
video links. Rerun after each eval batch.
"""
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
REPORTS = SKILL / "reports"
OUT = SKILL / "RECOMMENDATIONS.md"
CHANNEL = "UCNZEktrsM5oJZ-MK4jKPMOQ"

VERDICTS = ("INCLUDE", "TRIAL", "SKIP")
V = r"(INCLUDE|TRIAL|SKIP|N/A-repo)"


def _find_verdict(blob: str):
    m = re.search(rf"\*\*Recommendation:\s*\**\s*{V}\b", blob)
    if m:
        return m.group(1)
    m = re.search(rf"\*\*Verdict:\*{{0,2}}\s*{V}\b", blob)
    if m:
        return m.group(1)
    m = re.search(rf"^\s*-?\s*Recommendation:\s*\**\s*{V}\b", blob, re.M)
    if m:
        return m.group(1)
    return None


def _inline_verdict(rest: str):
    m = re.search(rf"(?:—|->|→)\s*\**\s*{V}\b", rest)
    return m.group(1) if m else None


def _clean_name(raw: str) -> str:
    name = re.sub(r"\*{1,2}", "", raw).strip()
    name = re.sub(r"^\d+\.\s*", "", name)
    if " — " in name:
        name = name.split(" — ")[0].strip()
    return name.strip()


def _gh_url(text: str):
    m = re.search(r"https://github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", text)
    return m.group(0).rstrip(".,)") if m else None


def _desc(blob: str) -> str:
    for ln in blob.split("\n"):
        ln = ln.strip().lstrip("-").strip()
        if not ln:
            continue
        if ln.startswith("**Functionality:**"):
            return ln.replace("**Functionality:**", "").strip()
        if not ln.startswith(("*", "!", "#")):
            return ln
    return ""


def _add(items, name, verdict, url, desc):
    key = name.lower()
    existing = items.get(key)
    if existing:
        if (not existing.get("url")) and url:
            existing["url"] = url
        if existing["verdict"] == "PENDING" and verdict != "PENDING":
            existing["verdict"] = verdict
        return
    items[key] = {"name": name, "verdict": verdict or "PENDING",
                  "url": url or "", "desc": desc[:140]}


def parse_report(path: Path):
    text = path.read_text(errors="replace")
    m = re.match(r"#\s*(.+)", text)
    title = m.group(1).strip() if m else path.stem
    title = re.sub(r"^New:\s*", "", title)

    items = {}

    # --- ### section-based items (### name — https://github.com/...) ---
    for sec in re.split(r"\n###\s+", text)[1:]:
        lines = sec.split("\n")
        name = _clean_name(lines[0].strip())
        if not name or name.startswith(("http", "!")):
            continue
        blob = re.split(r"(?m)^## ", "\n".join(lines[1:]))[0]
        verdict = _find_verdict(blob) or _inline_verdict(lines[0].split(" — ", 1)[1] if " — " in lines[0] else "")
        if verdict == "N/A-repo" or name.endswith(":") or name == "owner/repo" or name.startswith(("N/A", "Not identified")):
            continue
        _add(items, name, verdict, _gh_url(lines[0]) or _gh_url("\n".join(blob.split("\n")[:4])), _desc(blob))

    # --- bullet-based items inside "## Eval" sections ---
    for eval_block in re.split(r"(?m)^## Eval\s*$", text)[1:]:
        eval_block = re.split(r"(?m)^## ", eval_block)[0]
        parts = re.split(r"(?m)^- \*\*((?!(?:Functionality|Fit|Verdict|Signals|Recommendation|Note|Notes|Why|Desc|Description|Reason)\b)[^*\n]+?)\*\*(.*)$", eval_block)
        # parts: [pre, name1, rest1, blob1, name2, rest2, blob2, ...]
        LABELS = ("Functionality:", "Fit:", "Verdict:", "Signals:", "Recommendation:", "Why:")
        cur = None
        for i in range(1, len(parts) - 2, 3):
            name_raw, rest, blob = parts[i], parts[i + 1], parts[i + 2]
            name = _clean_name(name_raw)
            if not name:
                continue
            if name.endswith(tuple(LABELS)) and cur is not None:
                cur[2] += name_raw + rest + blob + "\n"
                continue
            cur = [name, rest, blob]
            verdict = _inline_verdict(rest) or _find_verdict(blob)
            url = _gh_url(rest) or _gh_url(blob)
            if "/" not in name and not url and not verdict:
                continue
            _add(items, name, verdict, url, _desc(blob))

    repos = [x for x in items.values() if x["verdict"] != "N/A-repo" and not x["name"].startswith(("N/A", "Not identified"))]
    pending = "## Eval" not in text and "Recommendation" not in text
    return {"vid": path.stem, "title": title, "repos": repos, "pending": pending}


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

    def item_line(r, repo):
        name = repo["name"]
        url = repo["url"]
        report = f"reports/{r['vid']}.md"
        video = f"https://youtu.be/{r['vid']}"
        label = f"**[{name}]({url})**" if url else f"**{name}**"
        return (f"- {label} — {repo['desc']}\n"
                f"  - Report: `{report}` · Video: {video} · *{r['title']}*")

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
                lines.append(item_line(r, repo))
        if not any_row:
            lines.append("_(none)_")
        lines.append("")

    lines.append("## SKIP")
    lines.append("")
    for r in rows:
        for repo in r["repos"]:
            if repo["verdict"] != "SKIP":
                continue
            name = repo["name"]
            url = repo["url"]
            label = f"[{name}]({url})" if url else name
            lines.append(f"- {label} — `reports/{r['vid']}.md`")
    lines.append("")

    pend = [r for r in rows if r["pending"] or any(x["verdict"] == "PENDING" for x in r["repos"])]
    if pend:
        lines.append("## Pending eval")
        lines.append("")
        for r in pend:
            np = sum(1 for x in r["repos"] if x["verdict"] == "PENDING")
            lines.append(f"- `reports/{r['vid']}.md` — {r['title']} ({np} unevaled)")
        lines.append("")

    OUT.write_text("\n".join(lines))
    print(f"Wrote {OUT} — {len(rows)} videos, INCLUDE={counts['INCLUDE']} TRIAL={counts['TRIAL']} SKIP={counts['SKIP']} PENDING={counts['PENDING']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
