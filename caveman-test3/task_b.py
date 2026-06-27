def flatten(nested: list) -> list:
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result


if __name__ == "__main__":
    tests = [
        ([1, [2, [3, 4], 5], 6], [1, 2, 3, 4, 5, 6]),
        ([], []),
        ([1, [2, [3, [4, [5]]]]], [1, 2, 3, 4, 5]),
        ([[1, 2], [3, 4], [5, 6]], [1, 2, 3, 4, 5, 6]),
        ([1, 2, 3], [1, 2, 3]),
    ]

    for i, (input_val, expected) in enumerate(tests):
        result = flatten(input_val)
        status = "PASS" if result == expected else "FAIL"
        print(f"Test {i + 1}: flatten({input_val}) -> {result} [{status}]")
