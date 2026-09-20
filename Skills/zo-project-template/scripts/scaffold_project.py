#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path


def write_if_missing(path: Path, content: str) -> None:
    if not path.exists():
        path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the standard Zo project structure.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--name", required=True)
    parser.add_argument("--frontend", action="store_true")
    parser.add_argument("--manifest", action="store_true", help="Add an optional project.manifest.json template")
    args = parser.parse_args()
    root = args.path.resolve()
    root.mkdir(parents=True, exist_ok=True)
    for directory in ("src", "tests", "scripts", "docs"):
        (root / directory).mkdir(exist_ok=True)
    write_if_missing(root / "README.md", f"# {args.name}\n\nProject purpose and setup.\n")
    write_if_missing(root / "AGENTS.md", f"# {args.name}\n\nProject-specific instructions and current status.\n")
    write_if_missing(root / "SOUL.md", "---\nname: project-soul\ndescription: Project identity and working principles\ntype: soul\n---\n\n# Project Soul\n\nDefine the project's identity and quality bar.\n")
    write_if_missing(root / ".env.example", "# Copy to .env and fill locally. Never commit secrets.\n")
    if args.frontend:
        write_if_missing(root / "DESIGN.md", "# Design System\n\nDefine colors, typography, spacing, shape, and interaction rules here.\n")
    if args.manifest:
        manifest = {
            "version": 1,
            "capabilities": [
                {
                    "id": "replace-with-capability",
                    "description": "Replace with a concrete capability this project provides.",
                    "entrypoints": ["src/"],
                    "checks": ["tests/"],
                }
            ],
        }
        write_if_missing(root / "project.manifest.json", json.dumps(manifest, indent=2) + "\n")
    if not (root / ".git").exists():
        subprocess.run(["git", "init", str(root)], check=True, stdout=subprocess.DEVNULL)
    validator = Path(__file__).with_name("validate_project.py")
    subprocess.run(["python3", str(validator), str(root), *( ["--frontend"] if args.frontend else [] )], check=True)
    print(root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
