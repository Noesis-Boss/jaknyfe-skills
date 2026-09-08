---
name: new-strategy
description: One-shot onboarding for new strategies in the robinhood-trading-bot Strategy Lab. Borrowed from tradesdontlie/tradingview-mcp's "paste this into Claude Code and it will handle the rest" install prompt — turn a plain-English strategy description into a scaffolded file, registry wiring, and a verified smoke backtest with no manual steps.
compatibility: Created for Zo Computer
metadata:
  author: jaknyfe.zo.computer
  source_idea: https://github.com/tradesdontlie/tradingview-mcp
---

# new-strategy

Borrowed idea: tradingview-mcp ships a single one-shot prompt the user pastes
into their agent, and the agent does clone → install → configure → launch →
verify end to end. This skill applies the same pattern to the trading bot:
one instruction in, a runnable + registered + smoke-tested strategy out.

## Usage

Give the agent a strategy description in plain English. Example:

> "onboard a new strategy: VWAP mean-reversion in the first 15 minutes"

The agent then executes the whole flow itself — no steps are delegated back:

1. **Scaffold**:
   `python3 Skills/new-strategy/scripts/scaffold.py --slug <snake_case> --description "<one-liner>"`
   This writes `robinhood-trading-bot/src/<slug>.py` with the full interface
   (`generate_signal`, `on_trade_entered`, `check_exit`, risk, journaling,
   session windows) and a marked placeholder entry block (9-EMA cross).
2. **Implement**: replace the `BEGIN/END PLACEHOLDER` block in
   `src/<slug>.py` with the real entry logic. Keep the interface methods and
   the `config.get("<slug>", {})` config namespace intact.
3. **Register** in `src/backtest_runner.py` (the script prints the exact
   anchors): import, `STRATEGY_MAP["<slug>"] = <Class>Strategy`, and add the
   slug to the session-based set in the day loop (~line 271).
4. **Config** (optional): add a `<slug>:` block to `config.yaml` for tunables
   the script lists (session_start, session_end, rr_ratio, ...).
5. **Verify — no completion claim without this**: run
   `cd robinhood-trading-bot && python3 backtest.py --strategy <slug> \
   --symbols SPY QQQ AAPL TSLA NVDA --start <start> --end <end>`
   and report trade count, win rate, and P&L. A strategy that registers but
   produces no trades is reported as a failure, not shipped.

## Rules

- Paper research only. Never wire a scaffolded strategy into live execution.
- Never overwrite an existing strategy file — the script refuses; pick a new slug.
- Report zero-trade backtests as failures and iterate on the entry logic
  before yielding back.
