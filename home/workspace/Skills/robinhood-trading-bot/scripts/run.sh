#!/bin/bash
# Run the Robinhood Trading Bot in various modes.
# Usage: bun run.sh run.sh <backtest|paper|live> [args...]
# Or directly: bash run.sh backtest

set -e
cd /home/workspace/robinhood-trading-bot

case "${1:-backtest}" in
  backtest)
    shift
    python3 backtest.py "$@"
    ;;
  paper|live)
    # paper = simulation mode, live = real Robinhood
    python3 -m src.bot "$@"
    ;;
  *)
    echo "Usage: $0 {backtest|paper|live} [args...]"
    echo "  backtest  — run backtest.py with optional args (--symbol, --breakout-strength, etc.)"
    echo "  paper     — run bot in simulation mode"
    echo "  live      — run bot with real Robinhood (requires credentials)"
    ;;
esac
