#!/usr/bin/env python3
import argparse
from pathlib import Path


REQUIRED = ("README.md", "AGENTS.md", "SOUL.md", "src", "tests", "scripts", "docs", ".env.example", ".git")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Zo project structure.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--frontend", action="store_true")
    args = parser.parse_args()
    root = args.path.resolve()
    required = list(REQUIRED)
    if args.frontend:
        required.append("DESIGN.md")
    missing = [item for item in required if not (root / item).exists()]
    if missing:
        print("FAIL: " + ", ".join(missing))
        return 1
    print(f"PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
