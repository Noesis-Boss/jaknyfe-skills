"""
Heuristic tweet-quality scorer. 0-100.

Not a substitute for human review — quick screen only.

Weights (from SKILL.md):
  - under 280 chars: 25
  - has opinion / take, not just summary: 25
  - hashtag count in [1, 2]: 15
  - no em-dash chain: 15
  - no obvious AI vocab: 20
"""
from __future__ import annotations

import re

# AI-vocab from the humanizer skill pattern catalog.
# Match whole-word, case-insensitive.
AI_VOCAB = [
    "delve", "pivotal", "underscore", "underscores", "underscored",
    "tapestry", "foster", "fostering", "fosters",
    "garner", "garners", "garnered",
    "showcase", "showcases", "showcased",
    "landscape",  # only abstract use, but tweet-level it's almost always AI
    "vibrant", "breathtaking", "renowned", "nestled",
    "additionally", "moreover", "furthermore",
    "interplay", "intricate",
    "enduring", "aligns with", "align with",
    "testament", "elevate", "elevates", "elevated",
    "in the heart of", "boasts", "serves as", "stands as",
    "not only", "but also",
    "it is important to note", "it bears mentioning", "it should be pointed out",
    "in order to", "due to the fact that", "at this point in time",
]

# Opinion signals — sentence-level take, not just topic statement.
# Heuristic: presence of a verb that asserts/judges.
OPINION_VERBS = [
    "is", "isn't", "are", "aren't", "was", "wasn't",
    "means", "shows", "proves", "reminds", "kills", "wins",
    "isn't just", "isn't about", "isn't really", "isn't even",
    "won't", "doesn't", "can't", "won't change", "doesn't change",
    "should", "shouldn't", "must", "needs", "needs to",
    "look", "look at", "watch", "see", "notice", "remember",
    "everyone's", "nobody's", "no one",
    "actually", "really", "exactly", "truly",
    "the real", "the point", "the trick", "the catch",
    "still", "already", "going to",
    "lies", "lives", "dies", "sits",
    "because", "since", "so ",
    "want", "wanted", "need", "needed",
    "hate", "love", "fear", "hope",
    "wrong", "right", "true", "false",
    "over", "under", "behind", "beyond",
]


def _count_hashtags(t: str) -> int:
    return len(re.findall(r"#\w+", t))


def _has_em_dash_chain(t: str) -> bool:
    # 2+ em dashes in a single tweet = the humanizer's em-dash-overuse pattern
    return t.count("—") >= 2 or t.count(" -- ") >= 2


def _has_ai_vocab(t: str) -> list[str]:
    lo = t.lower()
    hits = []
    for w in AI_VOCAB:
        # word-boundary for short tokens, substring for multi-word phrases
        if " " in w or "'" in w:
            if w in lo:
                hits.append(w)
        else:
            if re.search(rf"\b{re.escape(w)}\b", lo):
                hits.append(w)
    return hits


def _has_opinion(t: str) -> bool:
    lo = t.lower().strip()
    if not lo:
        return False
    # hard disqualifier: pure summary phrasing
    summary_only = (
        lo.startswith(("according to ", "reports say ", "officials say ", "sources say "))
        or lo.endswith("…")
        or "according to " in lo[:40]
    )
    if summary_only:
        return False
    # positive signal: any opinion verb appears, OR a sentence ends with assertion
    for v in OPINION_VERBS:
        if v in lo:
            return True
    if re.search(r"[.!?]$", lo):
        # has terminating punctuation + at least one declarative sentence
        sentences = [s.strip() for s in re.split(r"[.!?]+", lo) if s.strip()]
        if len(sentences) >= 1 and any(len(s.split()) >= 4 for s in sentences):
            return True
    return False


def score_tweet(tweet: str) -> int:
    if not tweet:
        return 0
    score = 0
    breakdown: list[str] = []

    # 1) length cap
    if len(tweet) <= 280:
        score += 25
        breakdown.append("len:25")
    else:
        breakdown.append(f"len:0 (over 280: {len(tweet)})")

    # 2) opinion / take
    if _has_opinion(tweet):
        score += 25
        breakdown.append("opinion:25")
    else:
        breakdown.append("opinion:0")

    # 3) hashtag count
    hn = _count_hashtags(tweet)
    if 1 <= hn <= 2:
        score += 15
        breakdown.append(f"tags:15 ({hn})")
    else:
        breakdown.append(f"tags:0 (n={hn})")

    # 4) em-dash chain
    if not _has_em_dash_chain(tweet):
        score += 15
        breakdown.append("dashes:15")
    else:
        breakdown.append("dashes:0")

    # 5) AI vocab
    hits = _has_ai_vocab(tweet)
    if not hits:
        score += 20
        breakdown.append("vocab:20")
    else:
        # partial credit, 4 pts per hit, floor at 0
        partial = max(0, 20 - 4 * len(hits))
        score += partial
        breakdown.append(f"vocab:{partial} (hits={hits[:3]})")

    return min(score, 100)


if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        line = line.rstrip("\n")
        if not line:
            continue
        print(f"{score_tweet(line)}\t{line}")
