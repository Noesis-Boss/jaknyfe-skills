#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the Zo project hook installation.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    root = args.path.resolve()
    hook = root / ".githooks" / "pre-commit"
    errors = []
    if not hook.is_file():
        errors.append("missing .githooks/pre-commit")
    elif not hook.stat().st_mode & 0o111:
        errors.append(".githooks/pre-commit is not executable")
    result = subprocess.run(
        ["git", "-C", str(root), "config", "--get", "core.hooksPath"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0 or result.stdout.strip() != ".githooks":
        errors.append("Git core.hooksPath is not .githooks")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"INSTALL CHECK PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
