#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

from validate_project import LOCKFILE_NAMES


def git_clean(root: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print("FAIL: Git status could not be checked")
        return False
    if result.stdout.strip():
        print("FAIL: Git worktree is not clean")
        return False
    return True


def manifest_paths(root: Path) -> list[str]:
    path = root / "project.manifest.json"
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"project.manifest.json: {error}"]
    errors = []
    for index, capability in enumerate(data.get("capabilities", [])):
        if not isinstance(capability, dict):
            continue
        for field in ("entrypoints", "checks"):
            values = capability.get(field, [])
            if not isinstance(values, list) or not values:
                errors.append(f"project.manifest.json: capability {index} needs {field}")
                continue
            for value in values:
                if not isinstance(value, str) or not value.strip():
                    errors.append(f"project.manifest.json: capability {index} has invalid {field}")
                elif not (root / value).exists():
                    errors.append(f"project.manifest.json: missing path {value}")
    for index, surface in enumerate(data.get("publish", [])):
        if not isinstance(surface, dict):
            continue
        value = surface.get("path")
        if isinstance(value, str) and value.strip() and not (root / value).exists():
            errors.append(f"project.manifest.json: publish surface {index} missing path {value}")
    for index, dependency in enumerate(data.get("dependencies", [])):
        if not isinstance(dependency, dict):
            continue
        value = dependency.get("file")
        if isinstance(value, str) and value.strip() and not (root / value).exists():
            errors.append(f"project.manifest.json: dependency {index} missing file {value}")
        manager = dependency.get("manager")
        lockfile = dependency.get("lockfile")
        candidates = (lockfile,) if isinstance(lockfile, str) and lockfile.strip() else LOCKFILE_NAMES.get(manager, ())
        if candidates and not any((root / candidate).exists() for candidate in candidates):
            errors.append(f"project.manifest.json: dependency {index} missing lockfile ({', '.join(candidates)})")
        elif isinstance(value, str) and value.strip() and candidates:
            dependency_path = root / value
            existing = next((root / candidate for candidate in candidates if (root / candidate).exists()), None)
            if existing and existing.stat().st_mtime < dependency_path.stat().st_mtime:
                errors.append(f"project.manifest.json: dependency {index} lockfile is older than {value}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Zo project release gate.")
    parser.add_argument("path", type=Path)
    parser.add_argument("--frontend", action="store_true")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args()
    root = args.path.resolve()
    validator = Path(__file__).with_name("validate_project.py")
    validation = subprocess.run(
        [sys.executable, str(validator), str(root), *( ["--frontend"] if args.frontend else [] )],
        check=False,
    )
    artifact_check = subprocess.run(
        [sys.executable, str(Path(__file__).with_name("verify_artifacts.py")), str(root)],
        check=False,
    )
    errors = manifest_paths(root)
    if errors:
        print("FAIL: " + "; ".join(errors))
    clean = args.allow_dirty or git_clean(root)
    if validation.returncode or artifact_check.returncode or errors or not clean:
        return 1
    print(f"RELEASE GATE PASS: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
