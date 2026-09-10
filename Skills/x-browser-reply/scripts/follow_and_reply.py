#!/usr/bin/env python3
"""Follow-back engagement orchestrator for X (recovered 2026-09-08).

Composes the three canonical x-browser-reply scripts (never existed as a
single file before — rebuilt to match the automation's CLI):

  python3 follow_and_reply.py --cookies cookies_zdsentry.json --account zdsentry \
      --max 5 --headless true --slow-mo 150

Flow: find f4f posts -> reply to each -> follow the author -> track state.
Prints summary JSON: {posts_found, replies_posted, followed, errors}.
"""
import argparse, json, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
STATE = "/home/workspace/Skills/x-browser-reply/processed_tweets.json"
RESTORE_SESSIONS = {"zdsentry": "x-zds", "jak_nyfe": "x-jak"}
REPLY_TEMPLATES = [
    "Following back, welcome to the community! 🚀",
    "Done — follow back complete. Let's grow together!",
    "Followed you back! 🤝",
    "Mutual now — thanks for connecting!",
]


def run_script(name, *args, timeout=300):
    r = subprocess.run(
        [sys.executable, os.path.join(HERE, name), *args],
        capture_output=True, text=True, timeout=timeout,
    )
    out = (r.stdout or "").strip()
    try:
        data = json.loads(out)
    except Exception:
        data = None
    return r.returncode, data, out, (r.stderr or "").strip()


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--cookies", default="")
    p.add_argument("--account", default="jak_nyfe")
    p.add_argument("--max", type=int, default=5)
    p.add_argument("--headless", default="true")
    p.add_argument("--slow-mo", type=int, default=150, dest="slow_mo")
    a = p.parse_args()

    restore = RESTORE_SESSIONS.get(a.account, "x-jak")
    delay = max(a.slow_mo, 150) / 1000.0 * 10  # scale ms flag to usable delay

    # Find candidate f4f posts
    args = ["find_follow_back.py", "--max", str(a.max)]
    if a.cookies:
        args += ["--cookies", a.cookies]
    rc, found, raw, err = run_script(*args[:1], *args[1:])
    if rc != 0 or found is None:
        detail = ((found or {}).get("error") if isinstance(found, dict) else None) or err or raw[:300]
        print(json.dumps({
            "posts_found": 0, "replies_posted": 0, "followed": 0,
            "errors": [f"find_follow_back failed (rc={rc}): {detail}"],
        }))
        sys.exit(1)
    found = found if isinstance(found, list) else []
    errors = []

    replies, followed = 0, 0
    replied_ids = set()
    for i, post in enumerate(found):
        tid, user = post["tweet_id"], post["username"]
        text = REPLY_TEMPLATES[i % len(REPLY_TEMPLATES)]

        rargs = ["reply.py", "--tweet-id", tid, "--text", text,
                 "--restore", restore]
        if user:
            rargs += ["--user", user]
        if a.cookies:
            rargs += ["--cookies", a.cookies]
        rc, data, raw, err = run_script(*rargs)
        if rc == 0 and data and data.get("ok"):
            replies += 1
            replied_ids.add(tid)
        elif rc == 2:
            errors.append(f"reply @{user}/{tid}: not logged in — aborting run")
            break
        else:
            errors.append(f"reply @{user}/{tid}: {((data or {}).get('error') if data else err or raw[:200])}")
        time.sleep(delay)

        fargs = ["follow.py", "--username", user, "--restore", restore]
        if a.cookies:
            fargs += ["--cookies", a.cookies]
        rc, data, raw, err = run_script(*fargs)
        if rc == 0 and data and data.get("ok"):
            followed += 1
        elif rc != 2:
            errors.append(f"follow @{user}: {((data or {}).get('error') if data else err or raw[:200])}")
        time.sleep(delay)

    # Update state statuses
    try:
        with open(STATE) as f:
            state = json.load(f)
        for post in found:
            tid = post["tweet_id"]
            if tid in state and state[tid].get("status") == "found" and tid in replied_ids:
                state[tid]["status"] = "replied"
        with open(STATE, "w") as f:
            json.dump(state, f, indent=2)
    except Exception as e:
        errors.append(f"state update failed: {e}")

    print(json.dumps({
        "posts_found": len(found),
        "replies_posted": replies,
        "followed": followed,
        "errors": errors,
    }))


if __name__ == "__main__":
    main()
