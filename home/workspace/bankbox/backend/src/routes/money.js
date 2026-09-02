const express = require('express');
const crypto = require('node:crypto');
const { getDb } = require('../db');
const authMiddleware = require('../middleware/auth');
const { providerName, createFundingRequest, submitPurchase } = require('../services/money-provider');

const router = express.Router();

router.get('/status', (req, res) => {
  res.json({ provider: providerName, liveTransfersEnabled: process.env.ENABLE_LIVE_MONEY_MOVEMENT === 'true' });
});

router.use(authMiddleware);

function estimateCost(profile, amountCents) {
  const percentage = Math.round(amountCents * profile.rate_bps / 10000);
  const calculated = percentage + profile.fixed_cents;
  return profile.cap_cents == null ? calculated : Math.min(calculated, profile.cap_cents);
}

router.get('/costs/report', (req, res) => {
  const db = getDb();
  const profiles = db.prepare(`
    SELECT provider, operation, pricing_model, rate_bps, fixed_cents, cap_cents,
      currency, source, is_active, updated_at
    FROM cost_profiles ORDER BY provider, operation
  `).all();
  const totals = db.prepare(`
    SELECT provider, operation, COUNT(*) AS movement_count,
      COALESCE(SUM(amount_cents), 0) AS total_cost_cents,
      SUM(CASE WHEN estimated = 1 THEN amount_cents ELSE 0 END) AS estimated_cost_cents,
      SUM(CASE WHEN estimated = 0 THEN amount_cents ELSE 0 END) AS actual_cost_cents
    FROM movement_costs GROUP BY provider, operation ORDER BY provider, operation
  `).all();
  res.json({ currency: 'usd', profiles, totals });
});

router.get('/costs/profiles', (req, res) => {
  const db = getDb();
  res.json({ profiles: db.prepare('SELECT * FROM cost_profiles ORDER BY provider, operation').all() });
});

router.post('/costs/profiles', (req, res) => {
  const { provider, operation, pricing_model, rate_bps = 0, fixed_cents = 0, cap_cents = null, source = 'vendor_quote' } = req.body;
  if (!provider || !operation || !['percentage', 'fixed', 'custom', 'none'].includes(pricing_model)) {
    return res.status(400).json({ error: 'provider, operation, and valid pricing_model are required' });
  }
  const db = getDb();
  db.prepare(`UPDATE cost_profiles SET pricing_model = ?, rate_bps = ?, fixed_cents = ?, cap_cents = ?, source = ?, updated_at = CURRENT_TIMESTAMP WHERE provider = ? AND operation = ?`)
    .run(pricing_model, Number(rate_bps), Number(fixed_cents), cap_cents == null ? null : Number(cap_cents), source, provider, operation);
  const existing = db.prepare('SELECT id FROM cost_profiles WHERE provider = ? AND operation = ?').get(provider, operation);
  if (!existing) db.prepare(`INSERT INTO cost_profiles (provider, operation, pricing_model, rate_bps, fixed_cents, cap_cents, source) VALUES (?, ?, ?, ?, ?, ?, ?)`)
    .run(provider, operation, pricing_model, Number(rate_bps), Number(fixed_cents), cap_cents == null ? null : Number(cap_cents), source);
  res.status(existing ? 200 : 201).json({ profile: db.prepare('SELECT * FROM cost_profiles WHERE provider = ? AND operation = ?').get(provider, operation) });
});

router.get('/account', (req, res) => {
  const db = getDb();
  const account = db.prepare('SELECT id, provider, account_type, currency, status, created_at FROM financial_accounts ORDER BY id LIMIT 1').get();
  const balance = db.prepare(`
    SELECT COALESCE(SUM(CASE WHEN entry_type IN ('credit', 'release') THEN amount_cents ELSE 0 END), 0) -
      COALESCE(SUM(CASE WHEN entry_type IN ('debit', 'reserve') THEN amount_cents ELSE 0 END), 0) AS available_cents
    FROM ledger_entries WHERE user_id = ?
  `).get(req.user.id);
  res.json({ account: account || null, balance: { available_cents: balance.available_cents, currency: 'usd' } });
});

router.post('/funding-sources', (req, res) => {
  const { type, provider, provider_account_id, provider_payment_method_id } = req.body;
  if (!['bank_account', 'card', 'paypal_wallet'].includes(type) || !provider) {
    return res.status(400).json({ error: 'type and provider are required' });
  }
  const db = getDb();
  const result = db.prepare(`
    INSERT INTO funding_sources (user_id, provider, provider_account_id, provider_payment_method_id, type)
    VALUES (?, ?, ?, ?, ?)
  `).run(req.user.id, provider, provider_account_id || null, provider_payment_method_id || null, type);
  res.status(201).json(db.prepare('SELECT * FROM funding_sources WHERE id = ?').get(result.lastInsertRowid));
});

router.post('/deposits', async (req, res) => {
  const amountCents = Number(req.body.amount_cents);
  const fundingSourceId = Number(req.body.funding_source_id);
  if (!Number.isInteger(amountCents) || amountCents <= 0 || !Number.isInteger(fundingSourceId)) {
    return res.status(400).json({ error: 'amount_cents and funding_source_id are required' });
  }
  const db = getDb();
  const source = db.prepare('SELECT * FROM funding_sources WHERE id = ? AND user_id = ?').get(fundingSourceId, req.user.id);
  if (!source) return res.status(404).json({ error: 'Funding source not found' });
  const idempotencyKey = req.get('Idempotency-Key') || crypto.randomUUID();
  try {
    const providerResult = await createFundingRequest({ amountCents, currency: 'usd', fundingSourceId, idempotencyKey });
    const movement = db.prepare(`
      INSERT INTO money_movements (user_id, funding_source_id, type, status, amount_cents, provider, idempotency_key, metadata_json)
      VALUES (?, ?, 'deposit', 'pending', ?, ?, ?, ?)
    `).run(req.user.id, fundingSourceId, amountCents, providerName, idempotencyKey, JSON.stringify(providerResult));
    const profile = db.prepare(`SELECT * FROM cost_profiles WHERE provider = ? AND operation = 'ach_deposit' AND is_active = 1`).get(providerName);
    if (profile) db.prepare(`INSERT INTO movement_costs (money_movement_id, cost_profile_id, provider, operation, amount_cents, estimated) VALUES (?, ?, ?, ?, ?, 1)`)
      .run(movement.lastInsertRowid, profile.id, profile.provider, profile.operation, estimateCost(profile, amountCents));
    res.status(202).json({ movement: db.prepare('SELECT * FROM money_movements WHERE id = ?').get(movement.lastInsertRowid) });
  } catch (error) {
    if (error.code === 'PROVIDER_NOT_CONFIGURED') return res.status(503).json({ error: error.message, liveTransfersEnabled: false });
    throw error;
  }
});

router.post('/purchase-intents', async (req, res) => {
  const amountCents = Number(req.body.amount_cents);
  const merchantName = String(req.body.merchant_name || '').trim();
  if (!Number.isInteger(amountCents) || amountCents <= 0 || !merchantName) {
    return res.status(400).json({ error: 'amount_cents and merchant_name are required' });
  }
  const db = getDb();
  const idempotencyKey = req.get('Idempotency-Key') || crypto.randomUUID();
  const result = db.prepare(`
    INSERT INTO purchase_intents (user_id, goal_id, merchant_name, item_reference, amount_cents, idempotency_key, metadata_json)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `).run(req.user.id, req.body.goal_id || null, merchantName, req.body.item_reference || null, amountCents, idempotencyKey, JSON.stringify({ auto_submit: false }));
  res.status(201).json({ purchase_intent: db.prepare('SELECT * FROM purchase_intents WHERE id = ?').get(result.lastInsertRowid), ready_to_reserve: false });
});

router.post('/purchase-intents/:id/submit', async (req, res) => {
  const db = getDb();
  const intent = db.prepare('SELECT * FROM purchase_intents WHERE id = ? AND user_id = ?').get(req.params.id, req.user.id);
  if (!intent) return res.status(404).json({ error: 'Purchase intent not found' });
  try {
    const result = await submitPurchase({ amountCents: intent.amount_cents, currency: intent.currency, merchantName: intent.merchant_name, idempotencyKey: intent.idempotency_key });
    db.prepare('UPDATE purchase_intents SET status = ?, provider = ?, metadata_json = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?')
      .run('submitted', providerName, JSON.stringify(result), intent.id);
    res.status(202).json({ purchase_intent: db.prepare('SELECT * FROM purchase_intents WHERE id = ?').get(intent.id) });
  } catch (error) {
    if (error.code === 'PROVIDER_NOT_CONFIGURED') return res.status(503).json({ error: error.message, liveTransfersEnabled: false });
    throw error;
  }
});

module.exports = router;
