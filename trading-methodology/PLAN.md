# Trading Methodology Build Plan
Source: JeaFx — "How to Become a Profitable Trader" (LTV framework: Learn → Test → Validate → Earn)
Adapted for: Don's stack (Alpaca free IEX data, `robinhood-trading-bot/`, ~60 min/day, small capital)
Created: 2026-08-22

---

## 0. Core Thesis (what the video actually claims)

1. **Target 2–5%/month, not account flips.** Consistency beats size. At $100K–$200K funded, 3–5%/month = $3K–$10K/month.
2. **Systemize everything.** Repeatable rules for analysis, risk, entries, exits, and management — same rules every trade. No concept-hopping.
3. **The edge is math:** fixed risk per trade + minimum 1:2 RR means you profit even at a 40% win rate (100 trades at 1:3 RR, 40% WR = +60R).
4. **Most traders fail because they skip testing.** Backtest first, validate second, earn third. No real money at risk until the system is proven.
5. **One mentor, one system.** Mixing concepts from multiple sources creates conflict and non-repeatability.

---

## 1. The Methodology (strategy spec, exactly as taught)

**Style:** Swing trading, daily timeframe. Fits ~15–30 min/day. No screen-watching.

### 1.1 Analysis process (daily, ~15 min)
1. **Identify trend on the Daily** — sequence of higher highs/higher lows (uptrend) or lower highs/lower lows (downtrend). Trade only with the trend.
2. **Trend-shift confirmation:** wait for a daily candle **close** beyond the most recent opposing swing point before flipping bias (wicks don't count).
3. **Mark supply/demand zones** in line with trend: use the **last candle before the impulse** that caused the break of structure.
4. **4H refinement (optional):** if the daily zone/stop is too wide for 1:2 RR, refine the entry zone to the 4H version of the same zone. 4H is for refinement only — bias stays daily.

### 1.2 Entry rules
- **Buy limit** at the demand zone (uptrend) / **sell limit** at the supply zone (downtrend).
- Stop loss: below the zone low (longs) / above the zone high (shorts) — the daily zone low, even when entering on 4H refinement.
- **Minimum 1:2 RR or skip the trade.** No exceptions.

### 1.3 Targets
1. Primary: nearest **open (untapped) supply/demand zone** in the trade direction.
2. Fallback: next **swing high/low** (acceptable, slightly lower quality).

### 1.4 Trade management
- **Set and forget.** No breakeven moves, no trailing, no partials, no interference. Entry → stop or target.

### 1.5 Risk rules (the operating limits)
| Rule | Value |
|---|---|
| Risk per trade | **1.0% fixed** (never dynamic, never case-by-case) |
| Minimum RR | **1:2** |
| Loss limit | Stop trading for the week at **−2%** |
| Profit limit | Stop trading for the month at **+8%** (lock it in) |
| Trade frequency | Max ~1–2 setups/week/asset; no revenge trades |
| Universe | Start with 2 liquid assets (e.g. SPY + QQQ); add assets only after validation |

### 1.6 Mindset rules
- Ego removal: the math wins even when you're wrong 60% of the time.
- Patience: know average trade duration from your own data (video's system: ~16 days to win, ~8 days to lose) so you don't panic-exit.
- Long-term focus: judge over quarters, not days.

---

## 2. Build Phases (LTV mapped to this workspace)

### Phase 1 — LEARN + codify (Week 1, ~2 hrs) ✅ DONE 2026-08-22
- [x] Write this spec into machine-readable config: `src/supply_demand_swing.py` + `config_swing.yaml` in `robinhood-trading-bot/` (trend detection via swing structure, zone marking, limit entries, set-and-forget exits, 1% fixed risk, weekly loss/monthly profit circuit breakers).
- [x] Success: strategy module passes unit tests for trend detection, zone identification, and RR filtering. (7/7 in tests/test_supply_demand_swing.py)

### Phase 2 — TEST / backtest (Weeks 2–3) ✅ DONE 2026-08-22 — verdict MARGINAL PASS, see RESULTS.md
- [x] Backtest run 3 years daily bars (yfinance reaches further than free Alpaca IEX), 6 assets: SPY QQQ AAPL NVDA TSLA META.
- [x] Collected the video's required metrics: win rate, avg RR, trades/month, avg winner %, avg loser %, avg win/loss duration, monthly P&L distribution, per-asset breakdown → trading-methodology/RESULTS.md + robinhood-trading-bot/results_swing.json.
- [x] Monte Carlo base + WR−10 stress (10k sims × 33 trades): median +23.4R, p5 −2.0R.
- [x] **Gate:** PF 2.44 ✅; MC WR−10 p5 −2.0R ❌ → MARGINAL PASS. Paper validation only, risk ≤0.5%, no live capital until 2–3 validated months.

### Phase 3 — VALIDATE (Months 1–3)
- [x] Paper runner live 2026-08-22: `python3 robinhood-trading-bot/paper_swing.py` (idempotent daily run; anchor 2026-08-22, 6-symbol universe, 0.5% risk, journal `paper_journal.jsonl`, state `paper_state.json`). Bootstrap verified: 33 pre-anchor trades replayed, 0 counted yet.
- [ ] 1 month paper (existing paper-sim mode), then 2 months small live ($200–300 account, 0.5% risk).
- [ ] Goal is NOT profit — it's execution fidelity: did every trade match the spec? Journal every entry with setup screenshot, zone, RR, outcome.
- [ ] **Gate:** 2–3 consecutive months of correct execution (not necessarily winning months — losing months ≤1% are fine per the video's distribution) → proceed.

### Phase 4 — EARN / scale (Month 4+)
- [ ] **Tradeoff to know:** the video's prop-firm path (FTMO-style $100K funded, 70–90% split) is FX/futures-centric. US-stock equivalents are rare and weaker. Realistic equity path: scale personal capital + compound, or evaluate a futures prop firm only if the methodology is ported to futures (MES/MNQ), which changes the spec.
- [ ] Scale risk only after 3 profitable validated months: 0.5% → 1% → 2% max.
- [ ] Withdraw profits on a schedule; keep trading capital and living money separate.

---

## 3. Continuous Loop (runs forever after Phase 2)

1. **Journal every trade** (JSONL journal already exists in `robinhood-trading-bot/src/journal.py`): setup grade (open-zone target vs swing fallback), RR achieved, duration, rule violations (target: zero).
2. **Monthly review:** compare live stats vs backtest stats. Drift >10% on WR or avg RR = stop and investigate before continuing.
3. **Quarterly re-backtest** with fresh data; retire/refine rules that decayed. One variable at a time — same discipline as the bot's rejected-strategy process (ema_cci_macd, ema-12-26 both rejected on data, not hope).
4. **Kill-switches:** 2 losing weeks → halt, review. Any rule violation → halt, review. System drift → halt, re-backtest.

---

## 4. Success Criteria (definition of done for the whole methodology)

- Codified strategy with tests passing.
- 6–12 month backtest with full metric set + Monte Carlo stress, documented in the bot's AGENTS.md.
- 3 months of validated execution with journal evidence and ≤1 rule violation.
- Written verdict: trade it, refine it, or reject it — decided by data, recorded in memory.
