import re


def is_palindrome(s: str) -> bool:
    cleaned = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return cleaned == cleaned[::-1]


if __name__ == "__main__":
    tests = [
        "racecar",
        "A man a plan a canal Panama",
        "hello",
        "Was it a car or a cat I saw?",
        "noon",
    ]
    for t in tests:
        print(f"{t!r} -> {is_palindrome(t)}")
