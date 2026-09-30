#!/usr/bin/env python3
"""Find X follow-back posts via browser automation (agent-browser), NOT the X API.

Usage:
  python3 find_follow_back.py [--max 5] [--cookies /path/cookies.json]

Searches x.com live with multiple f4f queries, parses /<user>/status/<id>
links from the timeline, dedupes against processed_tweets.json, skips
own accounts, prints JSON array: [{tweet_id, username, url, text}].
Also appends found IDs to processed_tweets.json as "found" (status
updated to "replied"/"followed" by the other scripts' callers).

Uses `eval` (15s) instead of `read` — read hangs on some X pages.
"""
import argparse, json, os, re, subprocess, sys, time
from urllib.parse import quote

AB = "agent-browser"
STATE = "/home/workspace/Skills/x-browser-reply/processed_tweets.json"
SKIP = ("jak_nyfe", "zdsentry")
QUERIES = [
    '"follow back" min_faves:0 -filter:replies lang:en',
    '"I follow back" -filter:replies lang:en',
    '"follow for follow" -filter:replies lang:en',
    '"#f4f" -filter:replies lang:en',
]
CHALLENGE_MARKERS = ("just a moment", "checking your browser", "verify you are human", "challenge")
LINK_RE = re.compile(r"https://x\.com/([A-Za-z0-9_]{1,15})/status/(\d+)")


def ab(*args, timeout=15):
    try:
        r = subprocess.run([AB, *args], capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "").strip(), (r.stderr or "").strip()
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def eval_js(expr, timeout=15):
    """Run a JS expression; return stripped stdout or '' on failure."""
    rc, out, err = ab("eval", expr, timeout=timeout)
    if rc != 0:
        return ""
    return out.strip().strip('"')


def load_state():
    try:
        with open(STATE) as f:
            return json.load(f)
    except Exception:
        return {}


def save_state(state):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    with open(STATE, "w") as f:
        json.dump(state, f, indent=2)


def extract(text, state):
    """Parse tweet links from rendered page text, return candidates."""
    seen = {}
    for m in LINK_RE.finditer(text):
        user, tid = m.group(1), m.group(2)
        if user.lower() in SKIP:
            continue
        if tid in state:
            continue
        seen[tid] = {"tweet_id": tid, "username": user, "url": f"https://x.com/{user}/status/{tid}"}
    return list(seen.values())


def challenge_check():
    """Return True if current page shows a challenge wall."""
    expr = "(() => { const t = (document.body && document.body.innerText || '').toLowerCase(); return (t.includes('just a moment') || t.includes('checking your browser') || t.includes('verify you are human') || t.includes('challenge')) ? 'CHALLENGE' : 'OK'; })()"
    return eval_js(expr) == "CHALLENGE"


def collect_links():
    """Eval a small JS snippet that returns all status URLs on the page."""
    expr = "(() => Array.from(document.querySelectorAll('a[href*=\"/status/\"]')).map(a => a.href))()"
    raw = eval_js(expr)
    if not raw:
        return ""
    return raw


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--max", type=int, default=5)
    p.add_argument("--cookies", default="")
    a = p.parse_args()

    state = load_state()
    if a.cookies:
        import x_cookies
        ok, err = x_cookies.load(a.cookies)
        if not ok:
            print(json.dumps({"error": f"cookie load failed: {err}"}))
            sys.exit(2)

    results, q_used, challenge_seen = [], 0, False
    for q in QUERIES:
        if len(results) >= a.max:
            break
        q_used += 1
        rc, _, err = ab("open", f"https://x.com/search?q={quote(q)}&f=live", timeout=20)
        if rc != 0:
            continue
        time.sleep(6)
        if challenge_check():
            challenge_seen = True
            continue
        for scroll in range(2):
            raw = collect_links()
            results.extend(extract(raw, state))
            if len(results) >= a.max:
                break
            ab("scroll", "down", "1200", timeout=10)
            time.sleep(3)
        # dedupe by tweet_id
        uniq = {r["tweet_id"]: r for r in results}
        results = list(uniq.values())[: a.max]

    if challenge_seen and not results:
        print(json.dumps({"error": "X challenge page blocked timeline access", "challenge": True}))
        sys.exit(2)

    # Record found tweets in state
    for r in results:
        state.setdefault(r["tweet_id"], {
            "tweet_id": r["tweet_id"],
            "username": r["username"],
            "status": "found",
            "found_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        })
    save_state(state)

    print(json.dumps(results[: a.max], indent=2))
    sys.exit(0)


if __name__ == "__main__":
    main()