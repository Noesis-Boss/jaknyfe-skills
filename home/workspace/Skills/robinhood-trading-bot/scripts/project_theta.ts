#!/usr/bin/env -s bun
/** Project Theta Farming profit curves from a starting capital.
 * Usage: bun project_theta.ts
 */

const BOT_DIR = "/home/workspace/robinhood-trading-bot";

// Hardcode the key params (from config.yaml) since we can't parse YAML here
const capital = 10000;
const thetaCfg = {
  enabled: true,
  min_days_to_expiry: 2,
  target_pop: 0.80,
  max_spread_width_pct: 0.05,
  contracts_per_trade: 1,
  max_risk_per_trade_pct: 0.02,
};

const creditPerTrade = 35;
const maxLossPerTrade = 65;
const winRate = 0.72;
const tradesPerYear = 52;

const scales = [
  { label: "$100 capital (risk: 65% / trade — VERY high risk)", base: 100, risk: 0.65 },
  { label: "$1,000 capital (risk: 6.5% / trade — high risk)", base: 1000, risk: 0.065 },
];

for (const scale of scales) {
  console.log(`\n=== ${scale.label} ===\n`);

  const periods: [string, number][] = [
    ["1-day", Math.max(1, Math.floor(tradesPerYear / 365))],
    ["1-week", Math.max(1, Math.floor(tradesPerYear / 52))],
    ["1-month", Math.max(1, Math.floor(tradesPerYear / 12))],
    ["3-months", Math.max(1, Math.floor(tradesPerYear / 4))],
    ["6-months", Math.max(1, Math.floor(tradesPerYear / 2))],
    ["1-year", tradesPerYear],
  ];

  for (const [period, nTrades] of periods) {
    let finalCap = scale.base;
    for (let i = 0; i < nTrades; i++) {
      const win = Math.random() < winRate;
      const pnl = win ? creditPerTrade : -maxLossPerTrade;
      finalCap += pnl;
      if (finalCap <= 0) finalCap = 0;
    }
    const profit = finalCap - scale.base;
    const pct = (profit / scale.base) * 100;
    console.log(`  ${period.padEnd(10)}: ${String(nTrades).padStart(3)} trades → $${finalCap.toFixed(2)} (+$${profit.toFixed(2)}, +${pct.toFixed(1)}%)`);
  }
}
