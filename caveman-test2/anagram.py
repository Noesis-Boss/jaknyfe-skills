from collections import defaultdict


def group_anagrams(words: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for word in words:
        key = "".join(sorted(word))
        groups[key].append(word)
    return list(groups.values())


if __name__ == "__main__":
    words = ["eat", "tea", "tan", "ate", "nat", "bat"]
    result = group_anagrams(words)
    print(result)
