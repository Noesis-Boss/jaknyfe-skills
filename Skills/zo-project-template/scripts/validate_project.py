#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED = ("README.md", "AGENTS.md", "SOUL.md", "src", "tests", "scripts", "docs", ".env.example", ".git")
SUPPORTED_HARNESSES = {"zo", "codex", "claude-code", "cursor", "gemini", "opencode"}


def validate_manifest(root: Path) -> list[str]:
    path = root / "project.manifest.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        return [f"project.manifest.json: {error}"]
    errors = []
    if data.get("version") != 1:
        errors.append("project.manifest.json: version must be 1")
    if not isinstance(data.get("capabilities"), list) or not data["capabilities"]:
        errors.append("project.manifest.json: capabilities must be a non-empty list")
    harnesses = data.get("harnesses", [])
    if not isinstance(harnesses, list):
        errors.append("project.manifest.json: harnesses must be a list")
    else:
        for harness in harnesses:
            if not isinstance(harness, str) or harness not in SUPPORTED_HARNESSES:
                errors.append(f"project.manifest.json: unsupported harness {harness!r}")
    for index, capability in enumerate(data.get("capabilities", [])):
        if not isinstance(capability, dict):
            errors.append(f"project.manifest.json: capability {index} must be an object")
            continue
        for key in ("id", "description"):
            if not isinstance(capability.get(key), str) or not capability[key].strip():
                errors.append(f"project.manifest.json: capability {index} needs {key}")
    return errors


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
    manifest_errors = validate_manifest(root)
    if manifest_errors:
        print("FAIL: " + "; ".join(manifest_errors))
        return 1
    print(f"PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
