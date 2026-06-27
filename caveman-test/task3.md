# Task 3: CSV Parser

Write a Python file at `/home/workspace/caveman-test/csv_parser.py` that:
- Has a function `parse_csv(text: str) -> list[dict]` that parses CSV text into a list of dicts
- First row is headers, becomes dict keys
- Handles quoted fields with commas inside them
- Has a `if __name__ == "__main__":` block that tests with this sample data:
  ```
  name,age,city
  "Alice, Jr.",30,New York
  Bob,25,"San Francisco, CA"
  Charlie,35,Chicago
  ```
- Prints the parsed result
