#!/usr/bin/env bash
# Scaffold a .specify/ folder with the spec-driven-development templates.
# Usage: init.sh <project-root>
set -euo pipefail

ROOT="${1:-.}"
TARGET="$ROOT/.specify"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TPL_DIR="$SCRIPT_DIR/../templates"

if [ ! -d "$ROOT" ]; then
  echo "Project root $ROOT does not exist." >&2
  exit 1
fi

mkdir -p "$TARGET/memory"
cp "$TPL_DIR/constitution.md" "$TARGET/constitution.md"
cp "$TPL_DIR/spec.md"         "$TARGET/spec.md"
cp "$TPL_DIR/plan.md"         "$TARGET/plan.md"
cp "$TPL_DIR/tasks.md"        "$TARGET/tasks.md"
cp "$TPL_DIR/memory-decisions.md" "$TARGET/memory/decisions.md"
cp "$TPL_DIR/memory-changes.md"   "$TARGET/memory/changes.md"

cat <<EOF
Scaffolded $TARGET/

Stages (linear, gated):
  1. constitution.md  — non-negotiables (< 1 page)
  2. spec.md           — what & why, acceptance criteria
  3. plan.md           — how, tech stack, spec coverage matrix
  4. tasks.md          — ordered, atomic, every task has acceptance
  5. implement         — execute tasks, log proof per task

Don't start stage 5 until stage 4 is approved.
EOF
