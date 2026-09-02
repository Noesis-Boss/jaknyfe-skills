const Database = require('better-sqlite3');
const path = require('path');

const DB_PATH = process.env.DB_PATH || path.join(__dirname, '../../layaway.db');

let db;

function getDb() {
  if (!db) {
    db = new Database(DB_PATH);
    db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
    initSchema();
  }
  return db;
}

function initSchema() {
  const d = db;

  d.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      name TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      onboarding_completed INTEGER NOT NULL DEFAULT 0,
      last_login DATETIME,
      last_activity DATETIME
    );

    CREATE TABLE IF NOT EXISTS users_onboarding (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
      completed INTEGER NOT NULL DEFAULT 0,
      template TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS savings_goals (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      name TEXT NOT NULL,
      description TEXT,
      target_amount REAL NOT NULL CHECK(target_amount > 0),
      current_amount REAL NOT NULL DEFAULT 0 CHECK(current_amount >= 0),
      color TEXT DEFAULT '#6366f1',
      icon TEXT DEFAULT '🎯',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS transactions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      goal_id INTEGER NOT NULL REFERENCES savings_goals(id) ON DELETE CASCADE,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      type TEXT NOT NULL CHECK(type IN ('deposit', 'withdrawal', 'transfer_in', 'transfer_out')),
      amount REAL NOT NULL CHECK(amount > 0),
      note TEXT,
      related_goal_id INTEGER REFERENCES savings_goals(id) ON DELETE SET NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS subscriptions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
      plan TEXT NOT NULL DEFAULT 'free' CHECK(plan IN ('free', 'premium')),
      status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'past_due', 'canceled')),
      provider TEXT NOT NULL DEFAULT 'manual',
      current_period_start TEXT,
      current_period_end TEXT,
      trial_ends_at TEXT,
      canceled_at TEXT,
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS billing_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      subscription_id INTEGER NOT NULL REFERENCES subscriptions(id) ON DELETE CASCADE,
      event_type TEXT NOT NULL,
      payload_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS affiliate_campaigns (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      name TEXT NOT NULL,
      slug TEXT NOT NULL UNIQUE,
      destination_url TEXT NOT NULL,
      commission_type TEXT NOT NULL CHECK(commission_type IN ('cpa', 'revshare', 'fixed')),
      commission_rate_bps INTEGER NOT NULL DEFAULT 0 CHECK(commission_rate_bps >= 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'paused', 'archived')),
      postback_secret TEXT NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS affiliate_clicks (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      campaign_id INTEGER NOT NULL REFERENCES affiliate_campaigns(id) ON DELETE CASCADE,
      click_token TEXT NOT NULL UNIQUE,
      landing_url TEXT NOT NULL,
      referrer_url TEXT,
      user_agent TEXT,
      metadata_json TEXT,
      converted_at DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS affiliate_conversions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      campaign_id INTEGER NOT NULL REFERENCES affiliate_campaigns(id) ON DELETE CASCADE,
      click_id INTEGER REFERENCES affiliate_clicks(id) ON DELETE SET NULL,
      external_order_id TEXT NOT NULL UNIQUE,
      revenue_cents INTEGER NOT NULL CHECK(revenue_cents >= 0),
      commission_cents INTEGER NOT NULL CHECK(commission_cents >= 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      status TEXT NOT NULL DEFAULT 'approved' CHECK(status IN ('approved', 'pending', 'rejected')),
      raw_payload TEXT,
      approved_at DATETIME,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS financial_accounts (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      provider TEXT NOT NULL,
      provider_account_id TEXT UNIQUE,
      account_type TEXT NOT NULL DEFAULT 'pooled_fbo',
      currency TEXT NOT NULL DEFAULT 'usd',
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'active', 'restricted', 'closed')),
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS funding_sources (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      provider TEXT NOT NULL,
      provider_account_id TEXT,
      provider_payment_method_id TEXT,
      type TEXT NOT NULL CHECK(type IN ('bank_account', 'card', 'paypal_wallet')),
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'verified', 'disabled')),
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS money_movements (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      financial_account_id INTEGER REFERENCES financial_accounts(id),
      funding_source_id INTEGER REFERENCES funding_sources(id),
      type TEXT NOT NULL CHECK(type IN ('deposit', 'withdrawal', 'purchase', 'refund')),
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'processing', 'succeeded', 'failed', 'reversed')),
      amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      provider TEXT NOT NULL,
      provider_transaction_id TEXT UNIQUE,
      idempotency_key TEXT NOT NULL UNIQUE,
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS ledger_entries (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      movement_id INTEGER REFERENCES money_movements(id),
      goal_id INTEGER REFERENCES savings_goals(id) ON DELETE SET NULL,
      entry_type TEXT NOT NULL CHECK(entry_type IN ('credit', 'debit', 'reserve', 'release')),
      amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS purchase_intents (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      goal_id INTEGER REFERENCES savings_goals(id) ON DELETE SET NULL,
      merchant_name TEXT NOT NULL,
      item_reference TEXT,
      amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'funded', 'reserved', 'submitted', 'succeeded', 'failed', 'canceled')),
      provider TEXT,
      provider_payment_id TEXT,
      idempotency_key TEXT NOT NULL UNIQUE,
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS cost_profiles (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      provider TEXT NOT NULL,
      operation TEXT NOT NULL,
      pricing_model TEXT NOT NULL CHECK(pricing_model IN ('percentage', 'fixed', 'custom', 'none')),
      rate_bps INTEGER NOT NULL DEFAULT 0 CHECK(rate_bps >= 0),
      fixed_cents INTEGER NOT NULL DEFAULT 0 CHECK(fixed_cents >= 0),
      cap_cents INTEGER CHECK(cap_cents IS NULL OR cap_cents >= 0),
      currency TEXT NOT NULL DEFAULT 'usd',
      source TEXT NOT NULL DEFAULT 'planning_estimate',
      is_active INTEGER NOT NULL DEFAULT 1,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(provider, operation)
    );

    CREATE TABLE IF NOT EXISTS movement_costs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      money_movement_id INTEGER NOT NULL REFERENCES money_movements(id) ON DELETE CASCADE,
      cost_profile_id INTEGER REFERENCES cost_profiles(id),
      provider TEXT NOT NULL,
      operation TEXT NOT NULL,
      amount_cents INTEGER NOT NULL CHECK(amount_cents >= 0),
      estimated INTEGER NOT NULL DEFAULT 1,
      currency TEXT NOT NULL DEFAULT 'usd',
      metadata_json TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      UNIQUE(money_movement_id, operation)
    );

    CREATE TABLE IF NOT EXISTS engagement_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      event_type TEXT NOT NULL,
      metadata JSON,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_engagement_events_user_id ON engagement_events(user_id);
    CREATE INDEX IF NOT EXISTS idx_engagement_events_created_at ON engagement_events(created_at);
    CREATE INDEX IF NOT EXISTS idx_engagement_events_type ON engagement_events(event_type);

    CREATE INDEX IF NOT EXISTS idx_affiliate_campaigns_user_created
      ON affiliate_campaigns(user_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_affiliate_clicks_campaign_created
      ON affiliate_clicks(campaign_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_affiliate_conversions_campaign_created
      ON affiliate_conversions(campaign_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_transactions_user_id_created_at
      ON transactions(user_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_transactions_goal_id_created_at
      ON transactions(goal_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_billing_events_user_created_at
      ON billing_events(user_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_money_movements_user_created_at
      ON money_movements(user_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_ledger_entries_user_created_at
      ON ledger_entries(user_id, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_purchase_intents_user_status
      ON purchase_intents(user_id, status, created_at DESC);
    CREATE INDEX IF NOT EXISTS idx_movement_costs_created_at
      ON movement_costs(created_at);
    CREATE INDEX IF NOT EXISTS idx_movement_costs_provider_operation
      ON movement_costs(provider, operation);
  `);

  const costProfiles = [
    ['stripe', 'ach_deposit', 'percentage', 80, 0, 500, 'planning_estimate'],
    ['stripe', 'ach_purchase', 'percentage', 80, 0, 500, 'planning_estimate'],
    ['stripe', 'card_purchase', 'percentage', 290, 30, null, 'planning_estimate'],
    ['stripe', 'bank_payout', 'percentage', 75, 150, null, 'planning_estimate'],
    ['stripe', 'instant_payout', 'percentage', 100, 0, null, 'planning_estimate'],
    ['stripe', 'failed_ach', 'fixed', 0, 400, null, 'planning_estimate'],
    ['stripe', 'ach_return', 'fixed', 0, 1500, null, 'planning_estimate'],
    ['plaid', 'bank_link', 'custom', 0, 0, null, 'vendor_quote_required'],
    ['plaid', 'transfer', 'custom', 0, 0, null, 'vendor_quote_required'],
    ['sponsor_bank', 'fbo_service', 'custom', 0, 0, null, 'vendor_quote_required'],
    ['bankbox', 'service_fee', 'percentage', 500, 0, null, 'business_policy'],
  ];
  const insertCostProfile = d.prepare(`
    INSERT OR IGNORE INTO cost_profiles
      (provider, operation, pricing_model, rate_bps, fixed_cents, cap_cents, source)
    VALUES (?, ?, ?, ?, ?, ?, ?)
  `);
  for (const profile of costProfiles) insertCostProfile.run(...profile);

  const goalColumns = new Set(d.prepare('PRAGMA table_info(savings_goals)').all().map(column => column.name));
  for (const column of ['milestone_25_reached', 'milestone_50_reached', 'milestone_75_reached', 'milestone_100_reached', 'last_activity']) {
    if (!goalColumns.has(column)) d.exec(`ALTER TABLE savings_goals ADD COLUMN ${column} DATETIME`);
  }

  d.prepare(`
    INSERT OR IGNORE INTO financial_accounts (id, provider, account_type, currency, status)
    VALUES (1, ?, 'pooled_fbo', 'usd', 'pending')
  `).run(process.env.MONEY_PROVIDER || 'unconfigured');
}

module.exports = { getDb };
