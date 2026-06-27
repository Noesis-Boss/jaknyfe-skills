#!/usr/bin/env python3
"""
Discovery helper for vibe-coding-assistant.

Given a product idea, returns:
  - a refined one-line problem statement
  - a 3-7 feature V1 list
  - a "parked for V2+" list
  - the next 3-5 questions to ask the user

Usage:
  python3 discovery.py "I want to build an app that..."
"""

import sys
import json
import re

GOAL_BUCKETS = {
    "exploring": "Exploring — prove the idea works for you, polish optional",
    "personal": "Personal Use — polish matters, but only for you",
    "share": "Share with Others — must look good to a few people, no auth/maybe no payments",
    "launch": "Public Launch — must be production-grade, secure, and scalable",
}

# Heuristics: keyword -> phase flag
SENSITIVE = ["payment", "stripe", "charge", "credit card", "subscription", "login", "auth", "oauth", "user account", "pii", "health", "medical", "financ", "invest", "crypto", "wallet"]
VISUAL = ["design", "ui", "ux", "look", "feel", "branding", "theme", "color", "landing page"]
DATA_HEAVY = ["dashboard", "analytics", "chart", "graph", "report", "crm", "scrape", "crawl", "etl"]
REALTIME = ["realtime", "live", "websocket", "chat", "messaging", "collab"]
MOBILE = ["mobile", "ios", "android", "react native", "flutter", "swift", "kotlin"]

def detect_signals(text: str) -> dict:
    t = text.lower()
    return {
        "sensitive": any(k in t for k in SENSITIVE),
        "visual_heavy": any(k in t for k in VISUAL),
        "data_heavy": any(k in t for k in DATA_HEAVY),
        "realtime": any(k in t for k in REALTIME),
        "mobile": any(k in t for k in MOBILE),
    }

def rate_complexity(signals: dict, has_auth: bool, has_payments: bool) -> str:
    score = 0
    if has_payments: score += 3
    if has_auth: score += 1
    if signals["sensitive"]: score += 2
    if signals["realtime"]: score += 2
    if signals["data_heavy"]: score += 1
    if signals["mobile"]: score += 2
    if signals["visual_heavy"]: score += 0  # visual alone is not complex
    if score <= 1: return "Simple"
    if score <= 4: return "Medium"
    return "Ambitious"

def derive_questions(text: str) -> list:
    """Return the first 3-5 discovery questions, in priority order."""
    t = text.lower()
    qs = []
    if "for me" not in t and "for myself" not in t and "personal" not in t:
        qs.append("Who is this for — you, a small group, or the public?")
    if not re.search(r"\b(problem|pain|struggle|annoying|tired|frustrat)", t):
        qs.append("What are you (or your users) doing today without it? What's the painful part?")
    qs.append("What does success look like — what's the smallest version that would still feel useful?")
    qs.append("What's the ONE feature you would build first if you could only build one?")
    qs.append("What have you already tried, looked at, or ruled out?")
    return qs[:5]

def has_payment_intent(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in ["payment", "charge", "sell", "subscription", "paid", "stripe", "checkout"])

def has_auth_intent(text: str) -> bool:
    t = text.lower()
    return any(k in t for k in ["login", "sign in", "sign up", "account", "user", "auth"])

def main():
    if len(sys.argv) < 2:
        print("Usage: discovery.py \"<product idea>\"")
        sys.exit(1)
    idea = " ".join(sys.argv[1:]).strip()
    if not idea:
        print("Empty idea.")
        sys.exit(1)

    signals = detect_signals(idea)
    has_payments = has_payment_intent(idea)
    has_auth = has_auth_intent(idea)
    complexity = rate_complexity(signals, has_auth, has_payments)

    # Suggest a goal bucket
    if signals["sensitive"] or has_payments or "public" in idea.lower() or "launch" in idea.lower():
        goal = GOAL_BUCKETS["launch"]
    elif has_auth or "share" in idea.lower() or "friends" in idea.lower():
        goal = GOAL_BUCKETS["share"]
    elif "personal" in idea.lower() or "myself" in idea.lower() or "for me" in idea.lower():
        goal = GOAL_BUCKETS["personal"]
    else:
        goal = GOAL_BUCKETS["exploring"] + "  (confirm with user)"

    out = {
        "raw_idea": idea,
        "signals": signals,
        "implied_has_payments": has_payments,
        "implied_has_auth": has_auth,
        "suggested_goal_bucket": goal,
        "complexity_rating": complexity,
        "next_questions": derive_questions(idea),
        "discovery_prompts": [
            "V1 (must have) = ?",
            "V2 (next) = ?",
            "Someday (parked) = ?",
        ],
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
