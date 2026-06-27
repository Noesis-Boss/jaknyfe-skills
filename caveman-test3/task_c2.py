import string


def word_count(text: str) -> dict:
    """Count word frequencies, case-insensitive, strips punctuation.

    Returns a dict sorted by count descending.
    """
    # Lowercase
    text = text.lower()

    # Strip punctuation characters
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)

    # Split into words and count
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1

    # Sort by count descending
    sorted_counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_counts


if __name__ == "__main__":
    test_text = "The quick brown fox jumps over the lazy dog. The dog barked at the fox!"
    result = word_count(test_text)
    for word, count in result.items():
        print(f"{word}: {count}")
