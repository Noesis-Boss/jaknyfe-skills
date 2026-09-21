#!/usr/bin/env bash
set -euo pipefail

project_root="${1:-.}"
task_dir="$project_root/.task"
for file in plan.md findings.md progress.md; do
  test -s "$task_dir/$file" || { printf 'missing or empty: %s\n' "$task_dir/$file" >&2; exit 1; }
done
printf 'valid: %s\n' "$task_dir"
