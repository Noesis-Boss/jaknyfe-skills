# Supply/Demand Swing — Backtest Results (Phase 2)

Run: 2026-08-22 · `backtest_swing.py` · yfinance daily bars · 2023-08-22 → 2026-08-21 (3y) · SPY QQQ AAPL NVDA TSLA META · $10,000 start

## Headline

| Metric | Value | Video benchmark |
|---|---|---|
| Trades | 33 (1.5/mo) | ~1–2/wk/asset (we trade fewer) |
| Win rate | 36.4% | 40%+ at 1:2+ RR is profitable |
| Profit factor | **2.44** | Gate: > 1.3 ✅ |
| Total | +30.15R · $10,000 → $13,319 (+33.2%) | 2–5%/mo target: 0.9%/mo actual |
| Avg winner / loser | +4.26R / −1.00R | avg RR 3.37 in video |
| Avg win / loss duration | 8.1d / 8.2d | video: ~16d / ~8d |
| Positive months | 54.5% | video: ~50–60% |
| Breaker blocks | 0 (−2% weekly / +8% monthly never hit) | — |
| Target mix | 30 zone / 4 swing | zone targets preferred |

## Monte Carlo (10k sims × 33 trades, bootstrap of observed R)

| Scenario | Median | p5 | p95 |
|---|---|---|---|
| Base | +28.1R | +2.6R | +58.4R |
| WR −10pts (26.4%) | +23.4R | **−2.0R** | +52.4R |

## Gate verdict

- PF 2.44 > 1.3 ✅
- MC at WR−10: median +23.4R ✅ but p5 = −2.0R ❌ (worst-1-in-20 ≈ breakeven)

**Verdict: MARGINAL PASS — proceed to paper validation (Phase 3), zero capital at risk.** The stress miss is −2R over 33 trades; the system's edge is real but thin at depressed win rates, and n=33 is a small sample. Do not scale risk past 0.5% until 2–3 validated months. Refinement candidates (one at a time, per plan §3): 4H zone refinement, pivot_left/right 2 vs 3, zone-body vs full-candle zone definition.

## Per-symbol

SPY 12.5% WR (n=8) is the drag — index ETFs mean-revert at daily zones more than single names. Candidate: drop SPY, keep QQQ+single names, retest.
