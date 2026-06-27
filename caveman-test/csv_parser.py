import csv
import io


def parse_csv(text: str) -> list[dict]:
    """Parse CSV text into a list of dicts. First row is headers."""
    reader = csv.DictReader(io.StringIO(text))
    return list(reader)


if __name__ == "__main__":
    sample = """name,age,city
"Alice, Jr.",30,New York
Bob,25,"San Francisco, CA"
Charlie,35,Chicago
"""
    result = parse_csv(sample)
    for row in result:
        print(row)
