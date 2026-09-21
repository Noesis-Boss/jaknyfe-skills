#!/usr/bin/env bash
set -euo pipefail

goal="${1:?goal required}"
project_root="${2:-.}"
task_dir="$project_root/.task"
mkdir -p "$task_dir"

if [[ ! -e "$task_dir/plan.md" ]]; then
  { printf '# Task Plan\n\n'; printf '%s\n\n' "Goal: $goal"; printf '## Success criteria\n\n- [ ] Define and verify the user-visible result.\n\n## Phases\n\n- [ ] Research\n- [ ] Implement\n- [ ] Verify\n\n## Decisions\n\n'; } > "$task_dir/plan.md"
fi

if [[ ! -e "$task_dir/findings.md" ]]; then
  printf '# Findings\n\n' > "$task_dir/findings.md"
fi

if [[ ! -e "$task_dir/progress.md" ]]; then
  printf '# Progress\n\n' > "$task_dir/progress.md"
fi

printf '%s\n' "$task_dir"
