#!/usr/bin/env python3
"""Mine power words/phrases from a post-performance ledger and emit a remix word bank.

Accepts:
  - The X Growth Analysis markdown ledger (table with | First 20 chars | Topic | Hook | ... | Score |)
  - CSV with columns: text,score[,topic,hook]
  - Plain JSON list of {"text":..., "score":..., "topic":..., "hook":...}

Usage:
  python3 mine_power_words.py --ledger /home/workspace/x-growth-analysis.md [--min-score 0] [--top 15]
  python3 mine_power_words.py --ledger posts.csv --format csv
"""
import argparse, csv, json, re, sys
from collections import defaultdict

STOP = set("""a an the and or but if then than of for to in on at by with from as is are was were be been
it its this that these those i you he she we they my your his her our their not no yes do does did done
have has had will would can could should just so up out about into over under again once only very own
same too also here there when where why how what which who whom whose me him them us via one two both
follow back following got it you're don't i'm we're that's it's let's more most some such new news source
""".split())

TOKEN_RE = re.compile(r"[a-zA-Z][a-zA-Z'+-]*")


def parse_md_ledger(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        lines = [ln for ln in f.read().splitlines() if ln.strip().startswith("|")]
    if len(lines) < 2:
        return rows
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    idx = {name: i for i, name in enumerate(header)}

    def col(row, *names):
        for n in names:
            i = idx.get(n)
            if i is not None and i < len(row):
                return row[i].strip()
        return ""

    for ln in lines[2:]:
        row = [c.strip() for c in ln.strip().strip("|").split("|")]
        if not row or row[0] in ("---", ""):
            continue
        url = col(row, "URL")
        if not url.startswith("http"):
            continue
        score_raw = col(row, "Score")
        try:
            score = float(score_raw) if score_raw not in ("", "none", "None") else 0.0
        except ValueError:
            score = 0.0
        rows.append({
            "text": col(row, "Full text", "First 20 chars", "text", "Text"),
            "score": score,
            "topic": col(row, "Topic"),
            "hook": col(row, "Hook"),
        })
    return rows


def parse_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                score = float(r.get("score", "") or 0)
            except ValueError:
                score = 0.0
            rows.append({"text": r.get("text", ""), "score": score,
                         "topic": r.get("topic", ""), "hook": r.get("hook", "")})
    return rows


def parse_json(path):
    with open(path, encoding="utf-8") as f:
        rows = json.load(f)
    for r in rows:
        r.setdefault("score", 0)
        r.setdefault("topic", "")
        r.setdefault("hook", "")
    return rows


def mine(rows, min_score=0.0):
    uni = defaultdict(lambda: [0.0, 0])
    bi = defaultdict(lambda: [0.0, 0])
    by_bucket = defaultdict(list)

    for r in rows:
        score = r["score"]
        if score < min_score:
            continue
        toks = [t.lower() for t in TOKEN_RE.findall(r["text"])
                if t.lower() not in STOP and len(t) >= 4]
        for t in toks:
            uni[t][0] += score + 1.0
            uni[t][1] += 1
        for a, b in zip(toks, toks[1:]):
            bi[f"{a} {b}"][0] += score + 1.0
            bi[f"{a} {b}"][1] += 1
        key = r["topic"] or (r["hook"] or "general")
        by_bucket[key].append(r)

    ranked_uni = sorted(
        ((w, s, n) for w, (s, n) in uni.items() if n >= 1),
        key=lambda x: (-x[1], -x[2]))[:15]
    ranked_bi = sorted(
        ((w, s, n) for w, (s, n) in bi.items() if n >= 2),
        key=lambda x: (-x[1], -x[2]))[:10]

    buckets = {k: sorted(v, key=lambda r: -r["score"])[:3] for k, v in by_bucket.items()}
    return ranked_uni, ranked_bi, buckets


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ledger", required=True, help="Path to markdown ledger, CSV, or JSON file")
    ap.add_argument("--format", choices=["md", "csv", "json"], default=None)
    ap.add_argument("--min-score", type=float, default=0.0)
    ap.add_argument("--top", type=int, default=15, help="Max words in output bank")
    ap.add_argument("--json-out", help="Optional path to write word bank JSON")
    args = ap.parse_args()

    fmt = args.format
    if fmt is None:
        fmt = {"md": "md", ".csv": "csv"}.get(
            args.ledger[args.ledger.rfind("."):].lstrip("."), "md")
        if args.ledger.endswith(".json"):
            fmt = "json"

    rows = {"md": parse_md_ledger, "csv": parse_csv, "json": parse_json}[fmt](args.ledger)
    if not rows:
        sys.exit("No ledger rows parsed — check file format.")

    uni, bi, buckets = mine(rows, args.min_score)
    uni, bi = uni[: args.top], bi[:10]

    print(f"POWER WORD BANK (from {len(rows)} posts, weighted by engagement score)")
    print("=" * 60)
    print("\nTOP PHRASES (2-gram, min 2 occurrences):")
    for w, s, n in bi:
        print(f'  "{w}"  (weight {s:.0f}, seen {n}x)')
    print("\nTOP WORDS:")
    print("  " + ", ".join(w for w, _, _ in uni))
    print("\nTOP POSTS BY BUCKET:")
    for b, posts in buckets.items():
        best = posts[0]
        print(f'  [{b}] score {best["score"]:.0f}: "{best["text"]}"')
    print("\nREMIX PROMPT (paste into generate_hooks.py topic):")
    if bi:
        print(f'  Use "{bi[0][0]}" as the anchor phrase, plus words: {", ".join(w for w, _, _ in uni[:8])}')
    else:
        print(f'  Use words: {", ".join(w for w, _, _ in uni[:8])}')

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"top_words": [w for w, _, _ in uni],
                       "top_phrases": [w for w, _, _ in bi],
                       "buckets": {k: [{"text": p["text"], "score": p["score"]} for p in v]
                                   for k, v in buckets.items()},
                       "source": args.ledger, "posts_mined": len(rows)}, f, indent=2)
        print(f"\nWord bank JSON: {args.json_out}")


if __name__ == "__main__":
    main()
