#!/usr/bin/env python3
"""Validate Skills/humanizer/SKILL.md structure. No external dependencies."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_PATH = ROOT / "SKILL.md"
SKILL = SKILL_PATH.read_text(encoding="utf-8")
errors: list[str] = []

m = re.match(r"\A---\n(.*?)\n---\n", SKILL, re.DOTALL)
if not m:
    errors.append("SKILL.md must begin with YAML frontmatter")
else:
    yaml = m.group(1)
    name_m = re.search(r"(?m)^name:\s*(\S+)\s*$", yaml)
    if not name_m:
        errors.append("frontmatter must set name")
    elif name_m.group(1) != ROOT.name:
        errors.append(f"name '{name_m.group(1)}' must match directory '{ROOT.name}'")
    elif not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name_m.group(1)):
        errors.append(f"name '{name_m.group(1)}' must be lowercase alphanumeric with hyphens")
    if not re.search(r"(?m)^description:\s*(\||\S)", yaml):
        errors.append("frontmatter must set description")
    if not re.search(r"(?m)^metadata:\s*$", yaml) or "author:" not in yaml:
        errors.append("frontmatter metadata.author is required")

for section in ("## When to Use", "## Pattern Catalog", "## Reference"):
    if section not in SKILL:
        errors.append(f"missing required section: {section}")

numbers = [int(n) for n in re.findall(r"(?m)^\*\*([0-9]+)\. ", SKILL)]
if numbers != list(range(1, max(numbers or [0]) + 1)):
    missing = sorted(set(range(1, max(numbers or [0]) + 1)) - set(numbers))
    errors.append(f"pattern numbering must be contiguous from 1: missing {missing}")

if len(SKILL.splitlines()) > 800:
    errors.append(f"SKILL.md exceeds 800 lines ({len(SKILL.splitlines())})")

if errors:
    raise SystemExit("FAILED:\n- " + "\n- ".join(errors))
print(f"humanizer skill valid: {len(numbers)} patterns, {len(SKILL.splitlines())} lines")
