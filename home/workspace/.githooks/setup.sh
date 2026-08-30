#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GIT_DIR="$(git rev-parse --git-dir 2>/dev/null)"
if [ -z "$GIT_DIR" ]; then echo "Not in a git repo"; exit 1; fi
cp "$SCRIPT_DIR/pre-commit" "$GIT_DIR/hooks/pre-commit"
cp "$SCRIPT_DIR/post-commit" "$GIT_DIR/hooks/post-commit"
chmod +x "$GIT_DIR/hooks/pre-commit" "$GIT_DIR/hooks/post-commit"
echo "Hooks installed"
