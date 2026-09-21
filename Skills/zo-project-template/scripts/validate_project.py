#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


REQUIRED = ("README.md", "AGENTS.md", "SOUL.md", "src", "tests", "scripts", "docs", ".env.example", ".git")
SUPPORTED_HARNESSES = {"zo", "codex", "claude-code", "cursor", "gemini", "opencode"}
SUPPORTED_PUBLISH_TYPES = {"skill", "agent", "command", "plugin"}
SUPPORTED_DEPENDENCY_MANAGERS = {"bun", "cargo", "go", "npm", "pip", "pnpm", "poetry", "yarn"}
LOCKFILE_NAMES = {
    "bun": ("bun.lock", "bun.lockb"),
    "cargo": ("Cargo.lock",),
    "go": ("go.sum",),
    "npm": ("package-lock.json",),
    "pip": ("requirements.lock",),
    "pnpm": ("pnpm-lock.yaml",),
    "poetry": ("poetry.lock",),
    "yarn": ("yarn.lock",),
}


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
    publish = data.get("publish", [])
    if not isinstance(publish, list):
        errors.append("project.manifest.json: publish must be a list")
    else:
        for index, surface in enumerate(publish):
            if not isinstance(surface, dict):
                errors.append(f"project.manifest.json: publish surface {index} must be an object")
                continue
            for key in ("id", "type", "path"):
                if not isinstance(surface.get(key), str) or not surface[key].strip():
                    errors.append(f"project.manifest.json: publish surface {index} needs {key}")
            if surface.get("type") not in SUPPORTED_PUBLISH_TYPES:
                errors.append(f"project.manifest.json: unsupported publish type {surface.get('type')!r}")
    dependencies = data.get("dependencies", [])
    if not isinstance(dependencies, list):
        errors.append("project.manifest.json: dependencies must be a list")
    else:
        for index, dependency in enumerate(dependencies):
            if not isinstance(dependency, dict):
                errors.append(f"project.manifest.json: dependency {index} must be an object")
                continue
            for key in ("name", "manager", "file"):
                if not isinstance(dependency.get(key), str) or not dependency[key].strip():
                    errors.append(f"project.manifest.json: dependency {index} needs {key}")
            if dependency.get("manager") not in SUPPORTED_DEPENDENCY_MANAGERS:
                errors.append(f"project.manifest.json: unsupported dependency manager {dependency.get('manager')!r}")
            lockfile = dependency.get("lockfile")
            if lockfile is not None and (not isinstance(lockfile, str) or not lockfile.strip()):
                errors.append(f"project.manifest.json: dependency {index} has invalid lockfile")
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
