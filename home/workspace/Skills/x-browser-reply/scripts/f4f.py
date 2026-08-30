#!/usr/bin/env python3
"""F4F automation: search X for follow-for-follow posts, reply, and follow."""
import json
import subprocess
import sys
import time
import os
import urllib.request
from pathlib import Path
from datetime import datetime, timezone

SKILL_DIR = Path("/home/workspace/Skills/x-browser-reply")
STATE_FILE = SKILL_DIR / "f4f_state.json"
API_URL = "https://api.zo.computer/zo/ask"
MODEL = "byok:ee9b6e08-3859-4d08-91ec-bfc683010ef4"

ACCOUNTS = {
    "jak_nyfe": {"cookies": str(SKILL_DIR / "cookies.json")},
    "zdsentry": {"cookies": str(SKILL_DIR / "zdsentry_cookies.json")},
}

SEARCH_QUERIES = [
    "follow for follow",
    "follow back if following",
    "F4F follow back",
    "follow train",
    "follow everyone who follows",
]


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"processed": [], "last_run": None}


def save_state(state):
    STATE_FILE.write_text(json.dumps(state, indent=2))


def search_posts(query, limit=15):
    """Search X for posts using x_search via the Zo API."""
    token = os.environ.get("ZO_CLIENT_IDENTITY_TOKEN")
    if not token:
        print("ERROR: No ZO_CLIENT_IDENTITY_TOKEN", file=sys.stderr)
        return []

    prompt = (
        f"Search X (Twitter) for posts containing the phrase: \"{query}\"\n"
        "Use x_search with time_range=\"day\".\n"
        "For each post that explicitly offers to follow back or asks people to follow them first, extract: tweet_id (numeric ID), username (without @), full_text.\n"
        "Return ONLY a valid JSON array of objects with keys: tweet_id, username, text.\n"
        "Do not include commentary or markdown outside the JSON array. Return [] if no matching posts found."
    )
    try:
        request = urllib.request.Request(
            API_URL,
            data=json.dumps({"input": prompt, "model_name": MODEL}).encode(),
            headers={"authorization": token, "content-type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.loads(response.read().decode())
        output = data.get("output", "").strip()

        # Find JSON array
        start = output.find("[")
        end = output.rfind("]") + 1
        if start >= 0 and end > start and end > start + 1:
            items = json.loads(output[start:end])
            results = []
            for item in items:
                tid = str(item.get("tweet_id", "")).strip()
                user = str(item.get("username", "")).strip().lstrip("@")
                text = str(item.get("text", "")).strip()
                if tid and tid.isdigit() and user:
                    results.append({"tweet_id": tid, "username": user, "text": text})
            return results[:limit]
        return []
    except Exception as e:
        print(f"Warning: Search failed for '{query}': {e}", file=sys.stderr)
        return []


def reply_and_follow(tweet_id, text, cookies_path, target_username):
    """Reply to a tweet and follow the user."""
    reply_script = SKILL_DIR / "scripts" / "reply.py"

    print(f"  Replying to {tweet_id} with: {text!r}")
    result = subprocess.run(
        ["python3", str(reply_script), "--tweet-id", tweet_id, "--text", text, "--cookies", cookies_path],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"  Reply failed: {result.stderr.strip()}", file=sys.stderr)
        return False
    print(f"  Reply OK")

    follow_script = SKILL_DIR / "scripts" / "follow.py"
    print(f"  Following @{target_username}...")
    result = subprocess.run(
        ["python3", str(follow_script), "--username", target_username, "--cookies", cookies_path],
        capture_output=True, text=True, timeout=120,
    )
    if result.returncode != 0:
        print(f"  Follow failed: {result.stderr.strip()}", file=sys.stderr)
        return False
    print(f"  Follow OK")
    return True


def determine_reply_text(post_text):
    """Return an appropriate reply based on the post content."""
    lower = post_text.lower()
    if "follow back" in lower or "f4f" in lower:
        return "Following you back! 👍"
    elif "follow train" in lower:
        return "On the train! Following back 🚂"
    elif "follow everyone" in lower:
        return "Following everyone back! 🚀"
    elif "follow for follow" in lower:
        return "F4F 👍 Following you back!"
    else:
        return "Following you back! 👍"


def main():
    import argparse
    parser = argparse.ArgumentParser(description="F4F automation")
    parser.add_argument("--limit", type=int, default=5, help="Max posts to process per account")
    parser.add_argument("--dry-run", action="store_true", help="Search only, don't reply/follow")
    args = parser.parse_args()

    state = load_state()
    processed = set(state.get("processed", []))

    # Search across all queries
    all_posts = {}
    for q in SEARCH_QUERIES:
        results = search_posts(q, limit=10)
        for r in results:
            tid = r["tweet_id"]
            if tid not in all_posts and tid not in processed:
                all_posts[tid] = r
        time.sleep(2)

    new_posts = list(all_posts.values())
    print(f"Found {len(new_posts)} new posts to process across all queries")

    if args.dry_run:
        for p in new_posts[: args.limit]:
            print(f"  - {p['tweet_id']}: @{p['username']} - {p['text'][:80]}")
        return

    for account_name, cfg in ACCOUNTS.items():
        print(f"\n=== @{account_name} ===")
        count = 0
        for post in new_posts:
            if count >= args.limit:
                break
            tid = post["tweet_id"]
            user = post["username"]
            reply_text = determine_reply_text(post["text"])

            success = reply_and_follow(
                tweet_id=tid,
                text=reply_text,
                cookies_path=cfg["cookies"],
                target_username=user,
            )
            if success:
                processed.add(tid)
                count += 1
                print(f"[{account_name}] Done: @{user} ({tid})")
            else:
                print(f"[{account_name}] Failed: @{user} ({tid})")
            time.sleep(3)

    state["processed"] = list(processed)
    state["last_run"] = datetime.now(timezone.utc).isoformat()
    save_state(state)
    print(f"\nDone. Total processed: {len(processed)}")


if __name__ == "__main__":
    main()
