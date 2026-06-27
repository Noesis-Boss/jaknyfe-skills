import re
from collections import Counter


def word_count(text: str) -> dict:
    words = re.findall(r"[a-z0-9']+", text.lower())
    counts = Counter(words)
    return dict(sorted(counts.items(), key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    text = "The quick brown fox jumps over the lazy dog. The dog barked at the fox!"
    result = word_count(text)
    for word, count in result.items():
        print(f"{word}: {count}")
