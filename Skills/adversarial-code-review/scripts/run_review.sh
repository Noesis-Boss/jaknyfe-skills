#!/usr/bin/env bash
# Run each rendered reviewer prompt through a reviewer CLI, then summarize.
#
# Usage:
#   run_review.sh --out <prompts-dir> [--repo <dir>] [--target codex|claude]
#                 [--timeout 600]
#
# The whole point of this skill is to break the author's mental model. A reviewer
# on the same model family that wrote the code shares its blind spots, so by
# default this spawns `codex exec` (opposing family) and you review the output
# yourself. Pass --target claude to invert.
#
# Prompts are read from <out>/*.prompt.md. Reviews, stderr captures, and the
# summary go to a fresh mktemp -d directory whose path is printed on the first
# summary line, so a second run never overwrites a first run's results.
#
# --repo is the repository reviewers read. It defaults to the current directory
# and is NOT the prompts directory: the rendered diff names files by relative
# path, so a reviewer started in the prompts directory cannot resolve the
# callers and callees the rubric tells it to inspect.
#
# Exit: 0 only if every reviewer produced a nonempty review.

set -uo pipefail

OUT=""
REPO=""
TARGET="codex"
TIMEOUT=600

die() { echo "error: $1" >&2; exit 1; }

# Count finding headers of the shape the template pins: `### N. [severity]`.
# With no severity argument, prints "unparseable" when the file has review
# prose but no pinned header at all, so a formatting failure is never reported
# as "zero findings".
count_severities() {
  local file="$1" severity="${2-}" found
  if [ -z "$severity" ]; then
    found=$(grep -cE '^### [0-9]+\. \[(critical|warning|nit)\]' "$file" 2>/dev/null) || found=0
    if [ "$found" -eq 0 ] && grep -qE '[Cc]ritical|[Ww]arning|\[nit\]|\[Nit\]' "$file"; then
      echo "unparseable"
    else
      echo "$found"
    fi
    return
  fi
  local n
  n=$(grep -cE "^### [0-9]+\\. \\[$severity\\]" "$file" 2>/dev/null) || n=0
  echo "$n"
}

# Read the value for a value-taking option into VALUE, or die. `shift 2` on a
# missing argument is a no-op, so an unguarded `--out` at the end of argv loops
# forever. A global, not `$(...)`, because `die` inside a command substitution
# would only exit the subshell.
VALUE=""
need_value() {
  # Reject a missing value: absent, empty, or actually the next option.
  if [ $# -lt 2 ] || [ -z "$2" ] || [ "${2#--}" != "$2" ]; then
    die "$1 requires a value"
  fi
  VALUE="$2"
}

while [ $# -gt 0 ]; do
  case "$1" in
    --out) need_value "$1" "${2-}"; OUT="$VALUE"; shift 2 ;;
    --repo) need_value "$1" "${2-}"; REPO="$VALUE"; shift 2 ;;
    --target) need_value "$1" "${2-}"; TARGET="$VALUE"; shift 2 ;;
    --timeout) need_value "$1" "${2-}"; TIMEOUT="$VALUE"; shift 2 ;;
    *) die "unknown arg: $1" ;;
  esac
done

case "$TARGET" in
  codex | claude) ;;
  *) die "--target must be codex or claude (got: $TARGET)" ;;
esac
case "$TIMEOUT" in
  '' | *[!0-9]*) die "--timeout must be a whole number of seconds (got: $TIMEOUT)" ;;
  0*) die "--timeout must be greater than zero; 0 disables the deadline entirely" ;;
esac

[ -n "$OUT" ] || die "--out <prompts-dir> is required"
[ -d "$OUT" ] || die "not a directory: $OUT"
command -v "$TARGET" >/dev/null 2>&1 || die "$TARGET not on PATH"
[ -n "$REPO" ] || REPO="."
[ -d "$REPO" ] || die "not a directory: $REPO"

# Both targets may run from inside REPO, so every path the runner passes to a
# reviewer is absolute first. A relative prompt path would otherwise resolve
# against the wrong tree.
OUT="$(cd "$OUT" && pwd)" || die "could not resolve $OUT"
REPO="$(cd "$REPO" && pwd)" || die "could not resolve $REPO"

shopt -s nullglob
PROMPTS=("$OUT"/*.prompt.md)
shopt -u nullglob
[ ${#PROMPTS[@]} -gt 0 ] || die "no *.prompt.md in $OUT"

REV="$(mktemp -d "${TMPDIR:-/tmp}/acr-review.XXXXXXXX")" || die "could not create results directory"

FAILED=0
RESULTS=()

for p in "${PROMPTS[@]}"; do
  lens="$(basename "$p" .prompt.md)"
  dest="$REV/$lens.review.md"
  err="$REV/$lens.err"
  if [ "$TARGET" = "codex" ]; then
    CMD=(codex exec --skip-git-repo-check -C "$REPO" -o "$dest" -)
  else
    # Claude has no -C. Run it in a subshell that changes to REPO so a
    # validated --repo is actually applied rather than silently ignored.
    CMD=(bash -c 'cd "$1" && shift && exec "$@"' bash "$REPO" \
      claude -p --model claude-opus-5 --permission-mode plan --output-format text)
  fi

  # `timeout` is the supervisor: it reports the reviewer's own exit status
  # (124 on timeout) and kills the tree. `--kill-after` is what makes that
  # promise real — without it, a reviewer that stalls on SIGTERM blocks here
  # forever and no summary is ever written.
  timeout --kill-after=10s "$TIMEOUT" "${CMD[@]}" < "$p" > "$dest" 2> "$err"
  status=$?

  if [ "$status" -eq 124 ] || [ "$status" -eq 137 ]; then
    RESULTS+=("TIMEOUT	$lens	after ${TIMEOUT}s")
    FAILED=1
  elif [ "$status" -ne 0 ]; then
    RESULTS+=("FAILED	$lens	exit $status, see $err")
    FAILED=1
  elif [ ! -s "$dest" ]; then
    RESULTS+=("EMPTY	$lens	no output, see $err")
    FAILED=1
  else
    RESULTS+=("ok	$lens	$dest")
  fi
done

# Summary is written once, after every lens is settled, so a failure record
# cannot be overwritten by the summary block. A summary that cannot be
# published is itself a failure: a zero exit with no summary is indistinguishable
# from success.
{
  echo "# Review summary"
  echo
  echo "Target model CLI: $TARGET"
  echo "Results: $REV"
  echo "Lenses attempted: ${#PROMPTS[@]}"
  echo
  for row in "${RESULTS[@]}"; do
    IFS=$'\t' read -r state lens detail <<<"$row"
    if [ "$state" != "ok" ]; then
      printf -- "- **%s**: %s (%s)\n" "$lens" "$state" "$detail"
      continue
    fi
    # Counts come from the exact header shape the template pins. A review whose
    # text contains severity words but no pinned header is unparseable, not a
    # zero-finding review.
    total=$(count_severities "$detail")
    if [ "$total" = "unparseable" ]; then
      # Output that is neither findings nor a declared zero-findings review is a
      # reviewer that did not do the job, not a clean review. Counting it as
      # success would report a pass that never happened.
      printf -- "- **%s**: UNPARSEABLE (no finding headers; see %s)\n" "$lens" "$detail"
      FAILED=1
      continue
    fi
    printf -- "- **%s**: %s critical, %s warning, %s nit\n" \
      "$lens" \
      "$(count_severities "$detail" critical)" \
      "$(count_severities "$detail" warning)" \
      "$(count_severities "$detail" nit)"
  done
} > "$REV/summary.md" || die "could not write $REV/summary.md"

cat "$REV/summary.md"
exit "$FAILED"
