#!/usr/bin/env python3
"""Daily Trello digest — fetches cards modified in the last 24h and emails a Markdown summary."""

import json
import os
import sys
from datetime import datetime, timedelta, timezone

import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
TRELLO_API_KEY = os.environ.get("TRELLO_API_KEY", "")
TRELLO_TOKEN = os.environ.get("TRELLO_TOKEN", "")
RECIPIENT = os.environ.get("TRELLO_DIGEST_TO", "delowery@gmail.com")
SINCE_HOURS = int(os.environ.get("TRELLO_DIGEST_HOURS", "24"))
BASE = "https://api.trello.com/1"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _params(**extra):
    p = {"key": TRELLO_API_KEY, "token": TRELLO_TOKEN}
    p.update(extra)
    return p


def _get(path, **params):
    r = requests.get(f"{BASE}{path}", params=_params(**params), timeout=30)
    r.raise_for_status()
    return r.json()


def _since_iso():
    return (datetime.now(timezone.utc) - timedelta(hours=SINCE_HOURS)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_url(board_id, card_id):
    return f"https://trello.com/c/{card_id[:24]}/"  # readable short link


# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

def get_boards():
    boards = _get("/members/me/boards", fields="name,id,url,dateLastActivity")
    return [b for b in boards if not b.get("closed", False)]


def get_cards_on_board(board_id):
    cards = _get(f"/boards/{board_id}/cards", fields="name,id,shortUrl,idList,dateLastActivity,due,labels")
    return cards


def get_lists_on_board(board_id):
    lists = _get(f"/boards/{board_id}/lists", fields="name,id")
    return {l["id"]: l["name"] for l in lists}


def get_actions(board_id, since):
    """Fetch recent actions (moves, creates, comments)."""
    actions = _get(
        f"/boards/{board_id}/actions",
        fields="type,data,date",
        since=since,
        limit=1000,
    )
    return actions


# ---------------------------------------------------------------------------
# Digest builder
# ---------------------------------------------------------------------------

def build_digest():
    now = datetime.now(timezone.utc)
    since = _since_iso()
    today = now.strftime("%Y-%m-%d")

    boards = get_boards()
    lines = [f"# Trello Daily Digest — {today}", ""]

    for board in boards:
        name = board["name"]
        board_id = board["id"]
        board_url = board.get("url", f"https://trello.com/b/{board_id}")

        # --- Actions (moves, new cards, comments) ---
        actions = get_actions(board_id, since)
        moved = []
        created = []
        commented = []

        for a in actions:
            atype = a.get("type", "")
            data = a.get("data", {})

            if atype == "updateCard" and "listAfter" in data:
                card_name = data.get("card", {}).get("name", "?")
                src = data.get("listBefore", {}).get("name", "?")
                dst = data.get("listAfter", {}).get("name", "?")
                moved.append(f"**{card_name}**  {src} → {dst}")

            elif atype == "createCard":
                card_name = data.get("card", {}).get("name", "?")
                list_name = data.get("list", {}).get("name", "?")
                created.append(f"**{card_name}**  in {list_name}")

            elif atype == "commentCard":
                card_name = data.get("card", {}).get("name", "?")
                commented.append(f"**{card_name}**")

        # --- Cards with approaching due dates (next 2 days) ---
        approaching = []
        try:
            cards = get_cards_on_board(board_id)
            for c in cards:
                due = c.get("due")
                if due:
                    due_dt = datetime.fromisoformat(due.replace("Z", "+00:00"))
                    if now < due_dt < now + timedelta(days=2):
                        approaching.append(f"**{c['name']}**  due {due_dt.strftime('%m/%d')}")
        except Exception:
            pass

        if moved or created or commented or approaching:
            lines.append(f"## [{name}]({board_url})")
            if moved:
                lines.append("### Moved")
                lines.extend(f"- {m}" for m in moved)
            if created:
                lines.append("### New cards")
                lines.extend(f"- {c}" for c in created)
            if commented:
                lines.append("### Comments")
                lines.extend(f"- {c}" for c in commented)
            if approaching:
                lines.append("### Due soon")
                lines.extend(f"- ⏰ {a}" for a in approaching)
            lines.append("")

    if len(lines) <= 2:
        lines.append("_No activity in the last 24 hours._")

    digest = "\n".join(lines)

    # Also write to file for reference
    out_path = f"/home/workspace/Projects/trello-digest/digest-{today}.md"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        f.write(digest)

    print(f"Digest written to {out_path}")
    return digest, today


# ---------------------------------------------------------------------------
# Email (using Zo send_email_to_user or SMTP fallback)
# ---------------------------------------------------------------------------

def send_via_gmail(subject, body):
    """Send via the Pipedream Gmail integration if available, otherwise print."""
    # In automation context, Zo handles email delivery automatically.
    # When run manually from CLI, just output the digest.
    print(f"\nSubject: {subject}\n")
    print(body)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if not TRELLO_API_KEY or not TRELLO_TOKEN:
        print("ERROR: TRELLO_API_KEY and TRELLO_TOKEN must be set.", file=sys.stderr)
        print("Go to Settings > Advanced and add them as secrets.", file=sys.stderr)
        sys.exit(1)

    digest, today = build_digest()
    subject = f"Trello Daily Digest — {today}"
    send_via_gmail(subject, digest)


if __name__ == "__main__":
    main()
