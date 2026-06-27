#!/usr/bin/env python3
"""
memory-search.py — Grep-based keyword search across all Clarion memory files.

Usage:
    python3 /home/workspace/scripts/memory-search.py <keyword> [keyword ...]
    python3 /home/workspace/scripts/memory-search.py --list
"""

import os
import sys
import re
from pathlib import Path

MEMORY_ROOT = Path("/home/workspace/memory")
WORKSPACE_ROOT = Path("/home/workspace")

# File extensions to search
EXTENSIONS = {".md", ".txt"}

# Folders to skip
SKIP_DIRS = {".git", "node_modules", "__pycache__", ".Trash", "Trash"}


def should_skip(path: Path) -> bool:
    for part in path.parts:
        if part in SKIP_DIRS:
            return True
    return False


def search_files(query: str) -> list[tuple[Path, str, int]]:
    """
    Search all memory files for a query string.
    Returns list of (filepath, matching_line, line_number).
    """
    results = []
    query_lower = query.lower()
    terms = query_lower.split()

    # Search workspace root too (USER.md, MEMORY.md)
    search_paths = [WORKSPACE_ROOT] + [MEMORY_ROOT]

    for root in search_paths:
        if not root.exists():
            continue
        for filepath in root.rglob("*"):
            if filepath.is_dir() or should_skip(filepath):
                continue
            if filepath.suffix not in EXTENSIONS:
                continue
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        line_lower = line.lower()
                        if all(term in line_lower for term in terms):
                            results.append((filepath, line.strip(), line_no))
            except Exception:
                pass

    return results


def print_results(results: list[tuple[Path, str, int]], query: str):
    if not results:
        print(f"🔎 No results for: {query}")
        return

    print(f"🔍 {len(results)} result(s) for: {query}")
    print()
    current_file = None
    for filepath, line, line_no in results:
        if filepath != current_file:
            print(f"  📄 {filepath}")
            current_file = filepath
        print(f"     L{line_no}: {line[:120]}{'...' if len(line) > 120 else ''}")
    print()


def list_memory_files() -> None:
    """List all memory files with a brief description."""
    files = []
    for ext in EXTENSIONS:
        for filepath in MEMORY_ROOT.rglob(f"*{ext}"):
            if should_skip(filepath):
                continue
            rel = filepath.relative_to(MEMORY_ROOT)
            files.append(rel)

    # Also include root workspace memory files
    for name in ["USER.md", "MEMORY.md"]:
        fp = WORKSPACE_ROOT / name
        if fp.exists():
            files.append(Path(name))

    if not files:
        print("📂 No memory files found.")
        return

    print(f"📂 {len(files)} memory file(s):")
    for f in sorted(files):
        print(f"  • {f}")


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(0)

    if args[0] == "--list":
        list_memory_files()
        sys.exit(0)

    query = " ".join(args)
    results = search_files(query)
    print_results(results, query)