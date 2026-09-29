#!/usr/bin/env bash
# Re-vendor the gitignored bundle bodies from https://github.com/openai/plugins.
#
# The eight `plugin/` bundle bodies are gitignored (third-party reference code; the repo
# ships no LICENSE except plugins/supabase). Only the hand-written Zo routers and
# Skills/TRIAL-openai-plugins.md are tracked. After a workspace restore from git, the
# routers exist but the bodies do not. This script rebuilds them from upstream.
#
# Usage:
#   revendor-openai-plugins.sh            # clone upstream, copy all 8, apply patches
#   revendor-openai-plugins.sh --check    # report which bodies are missing/stale, write nothing
#   revendor-openai-plugins.sh --only NAME[,NAME...]   # limit to named targets
#
# Targets (Zo skill dir <-- upstream path within the repo):
#   hyperframes             <-- plugins/hyperframes
#   public-equity-investing <-- plugins/public-equity-investing
#   plugin-eval             <-- plugins/plugin-eval
#   data-analytics          <-- plugins/data-analytics
#   postgres-best-practices <-- plugins/supabase
#   react-best-practices    <-- plugins/build-web-apps/skills/react-best-practices
#   shadcn-best-practices   <-- plugins/build-web-apps/skills/shadcn-best-practices
#   stripe-best-practices   <-- plugins/build-web-apps/skills/stripe-best-practices/references
#                             (partial: only the 4 reference files are kept)
#
# post-copy patch:
#   shadcn-best-practices strips the Codex auto-execute frontmatter directive
#   (!`npx shadcn@latest info --json`) that would shell out on every load in Codex and is
#   meaningless in Zo.
set -euo pipefail

REPO="https://github.com/openai/plugins.git"
SKILLS_DIR="${SKILLS_DIR:-/home/workspace/Skills}"
UPSTREAM_REF="${UPSTREAM_REF:-HEAD}"
CHECK_ONLY=0
ONLY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check) CHECK_ONLY=1; shift ;;
    --only) ONLY="${2:-}"; shift 2 ;;
    -h|--help) sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

# name|upstream path|copy mode (tree|files)
TARGETS=(
  "hyperframes|plugins/hyperframes|tree"
  "public-equity-investing|plugins/public-equity-investing|tree"
  "plugin-eval|plugins/plugin-eval|tree"
  "data-analytics|plugins/data-analytics|tree"
  "postgres-best-practices|plugins/supabase|tree"
  "react-best-practices|plugins/build-web-apps/skills/react-best-practices|tree"
  "shadcn-best-practices|plugins/build-web-apps/skills/shadcn-best-practices|tree"
  "stripe-best-practices|plugins/build-web-apps/skills/stripe-best-practices/references|files"
)

STRIPE_FILES=(payments.md treasury.md connect.md billing.md)

count_files() { [[ -d "$1" ]] && find "$1" -type f | wc -l | tr -d ' '; }

selected() {
  [[ -z "$ONLY" ]] && return 0
  [[ ",$ONLY," == *",$1,"* ]]
}

SRC=""
cleanup() { [[ -n "$SRC" && -d "$SRC" ]] && rm -rf "$SRC"; return 0; }
trap cleanup EXIT

if [[ $CHECK_ONLY -eq 0 ]]; then
  SRC="$(mktemp -d)"
  echo "==> cloning $REPO @ $UPSTREAM_REF"
  git clone --depth 1 --branch "$UPSTREAM_REF" "$REPO" "$SRC" >/dev/null 2>&1 \
    || git clone --depth 1 "$REPO" "$SRC" >/dev/null 2>&1
fi

fail=0
for entry in "${TARGETS[@]}"; do
  IFS='|' read -r name path mode <<<"$entry"
  selected "$name" || continue
  dest="$SKILLS_DIR/$name/plugin"

  if [[ $CHECK_ONLY -eq 1 ]]; then
    if [[ -d "$dest" ]] && [[ -n "$(find "$dest" -type f -print -quit)" ]]; then
      printf '  ok      %-26s %s files\n' "$name" "$(count_files "$dest")"
    else
      printf '  MISSING %-26s (router present: %s)\n' "$name" "$([[ -f "$SKILLS_DIR/$name/SKILL.md" ]] && echo yes || echo NO)"
      fail=1
    fi
    continue
  fi

  if [[ ! -d "$SRC/$path" ]]; then
    echo "  ERROR   $name: upstream path missing: $path" >&2
    fail=1
    continue
  fi

  rm -rf "$dest"
  mkdir -p "$dest"
  if [[ "$mode" == "tree" ]]; then
    cp -a "$SRC/$path/." "$dest/"
  else
    mkdir -p "$dest/references"
    for f in "${STRIPE_FILES[@]}"; do
      [[ -f "$SRC/$path/$f" ]] && cp -a "$SRC/$path/$f" "$dest/references/$f"
    done
  fi

  if [[ "$name" == "shadcn-best-practices" ]]; then
    python3 - "$dest/SKILL.md" <<'PY'
import sys
p = sys.argv[1]
old = '''```json
!`npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'`
```

The JSON above contains the project config and installed components.'''
new = '''Upstream ran `npx shadcn@latest info --json` inline at load time through a Codex-plugin shell directive. That directive is removed here \u2014 Zo has no inline shell execution, so it would only render as dead text. Run it yourself when you need it, from the project root:

```bash
npx shadcn@latest info --json 2>/dev/null || echo '{"error": "No shadcn project found. Run shadcn init first."}'
```

That JSON contains the project config and installed components.'''
s = open(p, encoding="utf-8").read()
if old in s:
    open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
    print("  patched shadcn-best-practices (auto-execute directive removed)")
elif new in s:
    print("  patched shadcn-best-practices (already patched)")
else:
    print("  WARNING shadcn-best-practices: directive block not found; upstream may have changed", file=sys.stderr)
PY
  fi

  printf '  copied  %-26s %s files\n' "$name" "$(count_files "$dest")"
done

if [[ $CHECK_ONLY -eq 1 ]]; then
  [[ $fail -eq 0 ]] && echo "all bundle bodies present" || echo "one or more bundle bodies missing (run without --check)"
  exit $fail
fi

echo "done. bodies are gitignored by design; routers + Skills/TRIAL-openai-plugins.md stay tracked."
