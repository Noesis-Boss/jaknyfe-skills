#!/usr/bin/env python3
"""Reply to an X post via browser automation (agent-browser), NOT the X API.

Usage:
  python3 reply.py --tweet-id ID [--user NAME] --text "..."
      [--cookies /path/cookies.json] [--restore x-main]

Opens the status page, opens the inline reply composer (intent URL fallback),
types the reply, submits, verifies it posted. Exit 2 = not logged in.
"""
import argparse, json, subprocess, sys, time

sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from ab_common import ab, js, load_cookies

SKIP = ("jak_nyfe", "zdsentry")


def logged_in():
    expr = """(() => {
  if (location.pathname.startsWith('/login') || location.pathname.startsWith('/i/flow')) return 'LOGINWALL';
  if (document.querySelector('a[data-testid="loginButton"]')) return 'LOGINWALL';
  if (document.querySelector('[data-testid="SideNav_AccountSwitcher_Button"], a[data-testid="AppTabBar_Profile_Link"]')) return 'OK';
  return 'UNKNOWN';
})()"""
    for _ in range(3):
        out = js(expr)
        if out in ("OK", "LOGINWALL"):
            return out == "OK"
        time.sleep(3)
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--tweet-id", required=True)
    p.add_argument("--user", default="")
    p.add_argument("--text", required=True)
    p.add_argument("--cookies", default="")
    p.add_argument("--restore", default="x-main")
    a = p.parse_args()

    tid = a.tweet_id.strip()
    if not tid.isdigit():
        print(json.dumps({"error": f"invalid tweet id: {tid!r}"}))
        sys.exit(1)

    if a.cookies:
        ok, err = load_cookies(a.cookies)
        if not ok:
            print(json.dumps({"error": f"cookie load failed: {err}"}))
            sys.exit(2)

    status_url = f"https://x.com/{a.user}/status/{tid}" if a.user else f"https://x.com/i/web/status/{tid}"
    rc, _, err = ab("open", status_url, timeout=30)
    if rc != 0:
        print(json.dumps({"error": f"navigation failed: {err}"}))
        sys.exit(1)
    time.sleep(5)

    if not logged_in():
        print(json.dumps({"error": "not logged in to x.com (cookies/session expired)"}))
        sys.exit(2)

    # Confirm the tweet exists
    expr = '(() => !!document.querySelector(\'article[data-testid="tweet"]\'))()'
    if js(expr) != "true":
        # try intent fallback
        rc, _, err = ab("open", f"https://x.com/intent/tweet?in_reply_to={tid}", timeout=30)
        time.sleep(5)
        if js(expr) != "true":
            print(json.dumps({"error": "tweet not found or account protected"}))
            sys.exit(1)

    # Open the inline reply composer
    rc, out, err = ab("click", '[data-testid="reply"]', timeout=30)
    if rc != 0:
        rc, out, err = ab("click", '[data-testid="tweetButtonInline"]~* [data-testid="reply"], a[href$="/compose/post"]', timeout=30)
    time.sleep(3)

    # Type the reply text
    rc, out, err = ab("click", '[data-testid="tweetTextarea_0"]', timeout=30)
    if rc != 0:
        print(json.dumps({"error": f"reply textarea not found: {err or out}"}))
        sys.exit(1)
    ab("type", '[data-testid="tweetTextarea_0"]', a.text, timeout=60)
    time.sleep(2)

    # Submit
    rc, out, err = ab("click", '[data-testid="tweetButton"]', timeout=30)
    if rc != 0:
        rc, out, err = ab("click", '[data-testid="tweetButtonInline"]', timeout=30)
    time.sleep(4)

    # Verify: toast, or textarea emptied
    expr = """(() => {
  const ta = document.querySelector('[data-testid="tweetTextarea_0"]');
  const empty = !ta || (ta.textContent || '').trim() === '';
  const toast = !!document.querySelector('[data-testid="toast"]');
  return (empty || toast) ? 'POSTED' : 'UNCLEAR';
})()"""
    result = js(expr)
    if result != "POSTED":
        print(json.dumps({"error": f"submit verification failed: {result}"}))
        sys.exit(1)

    print(json.dumps({"ok": True, "tweet_id": tid, "reply": a.text[:120]}))
    sys.exit(0)


if __name__ == "__main__":
    main()