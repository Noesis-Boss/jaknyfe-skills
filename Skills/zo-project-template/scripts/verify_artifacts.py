#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def publish_paths(root: Path) -> list[str]:
    manifest = root / "project.manifest.json"
    if not manifest.exists():
        return []
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"project.manifest.json: {error}"]
    errors = []
    publish = data.get("publish", [])
    if not isinstance(publish, list):
        return ["project.manifest.json: publish must be a list"]
    for index, surface in enumerate(publish):
        if not isinstance(surface, dict):
            continue
        value = surface.get("path")
        if not isinstance(value, str) or not value.strip():
            continue
        path = root / value
        if not path.exists():
            errors.append(f"publish surface {index} missing path {value}")
        elif path.is_file() and path.stat().st_size == 0:
            errors.append(f"publish surface {index} is empty {value}")
        elif path.is_dir() and not any(path.iterdir()):
            errors.append(f"publish surface {index} is empty {value}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify declared Zo project release artifacts.")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    root = args.path.resolve()
    errors = publish_paths(root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"ARTIFACT CHECK PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
