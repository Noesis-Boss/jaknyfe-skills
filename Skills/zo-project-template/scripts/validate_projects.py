#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate multiple Zo project structures.")
    parser.add_argument("paths", nargs="+", type=Path)
    parser.add_argument("--frontend", action="store_true")
    args = parser.parse_args()
    failed = False
    validator = Path(__file__).with_name("validate_project.py")
    for path in args.paths:
        result = subprocess.run(
            [sys.executable, str(validator), str(path), *(["--frontend"] if args.frontend else [])],
            check=False,
        )
        failed |= result.returncode != 0
    return int(failed)


if __name__ == "__main__":
    raise SystemExit(main())
