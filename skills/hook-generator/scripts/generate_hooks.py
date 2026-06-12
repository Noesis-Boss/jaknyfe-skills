#!/usr/bin/env python3
"""
Hook Generator — produce 5 hook variants across different styles
plus a recommendation and a second-line suggestion.

CLI:  python3 generate_hooks.py "topic" [--surface x|article|subject|linkedin|video|newsletter]
                                            [--audience "busy founders"]
                                            [--goal "share, click, agree, act"]
                                            [--count 5]
                                            [--json]
"""

import argparse
import json
import re
import sys
from typing import List, Dict


STYLES = [
    "curiosity",
    "contrarian",
    "stat",
    "story",
    "bold claim",
    "question",
    "confession",
    "specific",
]

SURFACE_LIMITS = {
    "x": 90,           # tweet hook length
    "article": 280,    # article intro first line
    "subject": 60,     # email subject
    "linkedin": 140,   # linkedin opener
    "video": 70,       # youtube title
    "newsletter": 50,  # newsletter subject
}


def clean_topic(t: str) -> str:
    t = t.strip().strip('"').strip("'")
    t = re.sub(r"\s+", " ", t)
    return t


def extract_signal(topic: str) -> Dict[str, List[str]]:
    """Heuristics to grab useful signals from the topic sentence."""
    text = topic.lower()
    signals: Dict[str, List[str]] = {
        "nouns": [],
        "verbs": [],
        "numbers": re.findall(r"\b\d[\d,.]*\b", topic),
        "named_entities": [],
    }
    # Pull out a few content words — very rough
    stop = {"the", "a", "an", "and", "or", "but", "is", "are", "was", "were",
            "to", "of", "in", "on", "for", "with", "as", "by", "at", "from",
            "this", "that", "it", "i", "you", "we", "they", "my", "your",
            "be", "been", "have", "has", "had", "do", "does", "did",
            "about", "into", "over", "under", "than", "so", "if", "no", "not"}
    words = re.findall(r"[A-Za-z][A-Za-z0-9'-]+", topic)
    signals["nouns"] = [w for w in words if w.lower() not in stop and len(w) > 3][:6]
    return signals


def variant_curiosity(t: str) -> str:
    return f"I was wrong about {t} for longer than I'd like to admit."


def variant_contrarian(t: str) -> str:
    return f"Most advice on {t} is written for people who've never done it."


def variant_stat(t: str, signals: Dict) -> str:
    n = signals["numbers"][0] if signals["numbers"] else "92"
    n = re.sub(r"[^\d]", "", n) or "92"
    return f"The {n}% of people who skip {t} are the ones who end up winning."


def variant_story(t: str) -> str:
    return f"It was 2:14am when I finally understood what {t} actually means."


def variant_bold_claim(t: str) -> str:
    return f"{t.capitalize()} is the most overhyped thing in { 'this space' if len(t) < 30 else '2026' }."


def variant_question(t: str) -> str:
    return f"Why does {t} still work when the entire internet says it shouldn't?"


def variant_confession(t: str) -> str:
    return f"I avoided {t} for two years. It cost me a lot more than I thought."


def variant_specific(t: str) -> str:
    return f"Austin, March 4th, 4:02pm — the moment {t} clicked for me."


VARIANTS = {
    "curiosity": variant_curiosity,
    "contrarian": variant_contrarian,
    "stat": variant_stat,
    "story": variant_story,
    "bold claim": variant_bold_claim,
    "question": variant_question,
    "confession": variant_confession,
    "specific": variant_specific,
}


def generate(topic: str, surface: str = "x", audience: str = "", goal: str = "",
             count: int = 5) -> Dict:
    topic = clean_topic(topic)
    signals = extract_signal(topic)

    # Pick a diverse 5 (or N) styles
    chosen_styles = STYLES[:count]
    hooks: List[Dict] = []
    for style in chosen_styles:
        if style == "stat":
            text = variant_stat(topic, signals)
        else:
            text = VARIANTS[style](topic)
        char_count = len(text)
        limit = SURFACE_LIMITS.get(surface, 280)
        over = char_count > limit
        hooks.append({
            "style": style,
            "text": text,
            "char_count": char_count,
            "over_limit": over,
        })

    # Pick a recommendation: first style whose length is under the surface limit.
    rec = next((h for h in hooks if not h["over_limit"]), hooks[0])
    recommendation = {
        "pick": rec["style"],
        "text": rec["text"],
        "why": "First hook that fits the surface character budget and earns the second look.",
    }
    second_line = f"The reason matters more than the headline."

    return {
        "input": {"topic": topic, "surface": surface, "audience": audience, "goal": goal},
        "hooks": hooks,
        "recommendation": recommendation,
        "second_line": second_line,
    }


def render_text(out: Dict) -> str:
    lines: List[str] = []
    inp = out["input"]
    lines.append(f"HOOKS for: {inp['topic']}")
    lines.append(f"Surface: {inp['surface']}  |  Audience: {inp['audience'] or '—'}  |  Goal: {inp['goal'] or '—'}")
    lines.append("")
    for i, h in enumerate(out["hooks"], 1):
        over = "  (over limit)" if h["over_limit"] else ""
        lines.append(f'HOOK {i} — [{h["style"]}]{over}')
        lines.append(f'"{h["text"]}"')
        lines.append(f"Length: {h['char_count']}")
        lines.append("")
    rec = out["recommendation"]
    lines.append(f"RECOMMENDED: {rec['pick']} — \"{rec['text']}\"")
    lines.append(f"Why: {rec['why']}")
    lines.append("")
    lines.append(f"SECOND LINE: \"{out['second_line']}\"")
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description="Generate attention-grabbing first lines for X, articles, etc.")
    p.add_argument("topic", help="The subject the hook should introduce")
    p.add_argument("--surface", default="x",
                   choices=list(SURFACE_LIMITS.keys()),
                   help="Where the hook will live")
    p.add_argument("--audience", default="", help="One-phrase audience description")
    p.add_argument("--goal", default="", help="Desired reaction: share, click, agree, act, curiosity")
    p.add_argument("--count", type=int, default=5, help="Number of hook variants to produce")
    p.add_argument("--json", action="store_true", help="Output JSON instead of text")
    args = p.parse_args()

    out = generate(args.topic, args.surface, args.audience, args.goal, args.count)
    if args.json:
        print(json.dumps(out, indent=2))
    else:
        print(render_text(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
