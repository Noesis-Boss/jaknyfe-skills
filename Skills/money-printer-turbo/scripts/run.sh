#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"

SKILLS_DIR="$(dirname "$PROJECT_DIR")"
VIROSCOPE_SCRIPT="$SKILLS_DIR/viroscope-ideas/scripts/viroscope.ts"

TOPIC="${1:-}"
if [ -z "$TOPIC" ]; then
  if [ ! -f "$VIROSCOPE_SCRIPT" ]; then
    echo "No topic provided and ViroScope skill not found at $VIROSCOPE_SCRIPT"
    echo "Usage: bash scripts/run.sh \"<video topic>\""
    exit 1
  fi
  echo "No topic provided — generating one via ViroScope..."
  SEED="${VIROSCOPE_SEED:-trending viral content}"
  VIRO_JSON="$(bun run "$VIROSCOPE_SCRIPT" generate "$SEED" --json)"
  TOPIC="$(printf '%s' "$VIRO_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); ideas=sorted(d.get("ideas",[]), key=lambda i: i.get("viralityScore",0), reverse=True); print(ideas[0]["title"] if ideas else "")')"
  if [ -z "$TOPIC" ]; then
    echo "ViroScope failed to generate an idea:"
    printf '%s\n' "$VIRO_JSON" | head -5
    exit 1
  fi
  echo "ViroScope picked: $TOPIC"
fi

echo "MoneyPrinterTurbo — generating video for: $TOPIC"

# Install deps if needed
if [ ! -d ".venv" ] || [ ! -f ".venv/bin/python" ]; then
  echo "Installing dependencies with uv..."
  uv sync 2>&1 | tail -5
fi

# Run the generation pipeline via the upstream mpt_agent.py
echo "Starting video generation..."
export MPT_LLM_PROVIDER="${MPT_LLM_PROVIDER:-openai}"
case "$MPT_LLM_PROVIDER" in
  gemini)
    export MPT_LLM_API_KEY="${MPT_LLM_API_KEY:-${GEMINI_API_KEY:-}}"
    export MPT_LLM_MODEL_NAME="${MPT_LLM_MODEL_NAME:-gemini-2.5-flash}"
    ;;
  anthropic)
    export MPT_LLM_API_KEY="${MPT_LLM_API_KEY:-${ANTHROPIC_API_KEY:-}}"
    export MPT_LLM_MODEL_NAME="${MPT_LLM_MODEL_NAME:-claude-sonnet-4-20250514}"
    ;;
  *)
    export MPT_LLM_API_KEY="${MPT_LLM_API_KEY:-${OPENAI_API_KEY:-}}"
    export MPT_LLM_MODEL_NAME="${MPT_LLM_MODEL_NAME:-gpt-5-nano}"
    ;;
esac
export MPT_PEXELS_API_KEY="${PEXELS_API_KEY:-}"

UV_PROJECT_ENVIRONMENT=.venv uv run --no-project python docs/skill/mpt_agent.py --subject "$TOPIC" 2>&1 | tail -30

echo "Done. Check the output above for the video file path."
