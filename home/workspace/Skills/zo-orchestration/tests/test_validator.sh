#!/usr/bin/env bash
set -euo pipefail

root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd -P)"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

cat >"$tmp/valid.json" <<'JSON'
{"objective":"ship","success_criteria":["tests pass"],"nodes":[{"id":"build","purpose":"build","dependencies":[],"ownership":"src","expected_output":"diff","verification":"test","stop_condition":"stop on failure","risk":"medium","agent":"codex"},{"id":"verify","purpose":"verify","dependencies":["build"],"ownership":"tests","expected_output":"report","verification":"inspect report","stop_condition":"stop after report","risk":"low","agent":"codex"}]}
JSON

cat >"$tmp/cycle.json" <<'JSON'
{"objective":"ship","success_criteria":["pass"],"nodes":[{"id":"a","purpose":"a","dependencies":["b"],"ownership":"a","expected_output":"a","verification":"a","stop_condition":"a","risk":"low","agent":"x"},{"id":"b","purpose":"b","dependencies":["a"],"ownership":"b","expected_output":"b","verification":"b","stop_condition":"b","risk":"low","agent":"x"}]}
JSON

bun run "$root/scripts/validate_task_graph.ts" "$tmp/valid.json"
if bun run "$root/scripts/validate_task_graph.ts" "$tmp/cycle.json" >/dev/null 2>&1; then
  echo "cycle was accepted" >&2
  exit 1
fi
echo "PASS: zo orchestration validator"
