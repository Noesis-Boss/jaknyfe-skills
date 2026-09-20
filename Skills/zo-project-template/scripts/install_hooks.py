#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


HOOK = """#!/usr/bin/env bash
set -e
project_root=$(git rev-parse --show-toplevel)
python3 {validator} "$project_root"
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Install the Zo project structure pre-commit hook.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--check", action="store_true", help="Verify the existing hook installation without changing files")
    args = parser.parse_args()
    root = args.path.resolve()
    if args.check:
        verifier = Path(__file__).with_name("verify_install.py")
        return subprocess.run(["python3", str(verifier), str(root)], check=False).returncode
    subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], check=True, stdout=subprocess.DEVNULL)
    hooks = root / ".githooks"
    hooks.mkdir(exist_ok=True)
    hook = hooks / "pre-commit"
    validator = (Path(__file__).with_name("validate_project.py")).resolve()
    hook.write_text(HOOK.format(validator=validator), encoding="utf-8")
    hook.chmod(0o755)
    subprocess.run(["git", "-C", str(root), "config", "core.hooksPath", ".githooks"], check=True)
    print(f"Installed: {hook}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
