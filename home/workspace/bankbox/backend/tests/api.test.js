/**
 * LayAway Backend E2E Tests
 * Uses Node 22's built-in test runner. Tests run against a real Express server
 * with an in-memory SQLite DB (temp file, cleaned up after tests).
 */

const { test, before, after, describe } = require('node:test');
const assert = require('node:assert/strict');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const fs = require('node:fs');

// Use a temp DB file so tests are isolated
const TMP_DB = path.join(os.tmpdir(), `layaway-test-${Date.now()}.db`);
process.env.DB_PATH = TMP_DB;
process.env.PORT = '0'; // OS assigns random port

let server;
let baseApiUrl;
let baseRootUrl;
let token;
let userId;
let goalId;
let secondGoalId;
let affiliateSlug;
let affiliateSecret;

// ---- Helper ----
async function req(method, path, body, authToken) {
  return new Promise((resolve, reject) => {
    const url = new URL(baseApiUrl + path);
    const data = body ? JSON.stringify(body) : undefined;
    const headers = {
      'Content-Type': 'application/json',
      ...(authToken ? { Authorization: `Bearer ${authToken}` } : {}),
    };

    const request = http.request({
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method,
      headers,
    }, (res) => {
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            body: raw ? JSON.parse(raw) : {},
            headers: res.headers,
          });
        } catch {
          resolve({
            status: res.statusCode,
            body: raw,
            headers: res.headers,
          });
        }
      });
    });
    request.on('error', reject);
    if (data) request.write(data);
    request.end();
  });
}

async function reqPublic(method, path, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(baseRootUrl + path);
    const data = body ? JSON.stringify(body) : undefined;
    const headers = {
      'Content-Type': 'application/json',
    };

    const request = http.request({
      hostname: url.hostname,
      port: url.port,
      path: url.pathname + url.search,
      method,
      headers,
    }, (res) => {
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try {
          resolve({
            status: res.statusCode,
            body: raw ? JSON.parse(raw) : {},
            headers: res.headers,
          });
        } catch {
          resolve({
            status: res.statusCode,
            body: raw,
            headers: res.headers,
          });
        }
      });
    });
    request.on('error', reject);
    if (data) request.write(data);
    request.end();
  });
}

before(async () => {
  // Build a minimal express app for testing
  const cors = require('cors');
  const app = require('express')();
  app.use(cors());
  app.use(require('express').json());

  // Re-init DB with the temp path already set via env
  const { getDb } = require('../src/db');
  getDb(); // init schema

  app.get('/r/:slug', require('../src/routes/affiliate').handleAffiliateRedirect);
  app.post('/api/affiliate/campaigns/:slug/conversions', require('../src/routes/affiliate').handleAffiliateConversion);
  app.use('/api/auth', require('../src/routes/auth'));
  app.use('/api/goals', require('../src/routes/goals'));
  app.use('/api/goals', require('../src/routes/funds'));
  app.use('/api/affiliate', require('../src/routes/affiliate'));
  app.use('/api/money', require('../src/routes/money'));
  app.get('/api/health', (_, res) => res.json({ status: 'ok' }));

  server = app.listen(0);
  await new Promise(resolve => server.on('listening', resolve));
  const { port } = server.address();
  baseApiUrl = `http://127.0.0.1:${port}/api`;
  baseRootUrl = `http://127.0.0.1:${port}`;
});

after(() => {
  server?.close();
  try { fs.unlinkSync(TMP_DB); } catch {}
  try { fs.unlinkSync(TMP_DB + '-shm'); } catch {}
  try { fs.unlinkSync(TMP_DB + '-wal'); } catch {}
});

// ---- Auth Tests ----
describe('Auth', () => {
  test('GET /health returns ok', async () => {
    const r = await req('GET', '/health');
    assert.equal(r.status, 200);
    assert.equal(r.body.status, 'ok');
  });

  test('POST /auth/register - missing fields returns 400', async () => {
    const r = await req('POST', '/auth/register', { email: 'x@x.com' });
    assert.equal(r.status, 400);
    assert.ok(r.body.error);
  });

  test('POST /auth/register - invalid email returns 400', async () => {
    const r = await req('POST', '/auth/register', { email: 'notanemail', password: 'pass123', name: 'Test' });
    assert.equal(r.status, 400);
  });

  test('POST /auth/register - short password returns 400', async () => {
    const r = await req('POST', '/auth/register', { email: 'a@b.com', password: 'abc', name: 'Test' });
    assert.equal(r.status, 400);
  });

  test('POST /auth/register - success returns token and user', async () => {
    const r = await req('POST', '/auth/register', { email: 'user@test.com', password: 'pass123', name: 'Test User' });
    assert.equal(r.status, 201);
    assert.ok(r.body.token);
    assert.equal(r.body.user.email, 'user@test.com');
    assert.equal(r.body.user.name, 'Test User');
    assert.ok(!r.body.user.password_hash, 'password_hash must not be exposed');
    token = r.body.token;
    userId = r.body.user.id;
  });

  test('POST /auth/register - duplicate email returns 409', async () => {
    const r = await req('POST', '/auth/register', { email: 'user@test.com', password: 'pass123', name: 'Dup' });
    assert.equal(r.status, 409);
  });

  test('POST /auth/login - wrong password returns 401', async () => {
    const r = await req('POST', '/auth/login', { email: 'user@test.com', password: 'wrongpass' });
    assert.equal(r.status, 401);
  });

  test('POST /auth/login - success returns token', async () => {
    const r = await req('POST', '/auth/login', { email: 'user@test.com', password: 'pass123' });
    assert.equal(r.status, 200);
    assert.ok(r.body.token);
  });

  test('GET /auth/me - no token returns 401', async () => {
    const r = await req('GET', '/auth/me');
    assert.equal(r.status, 401);
  });

  test('GET /auth/me - valid token returns user', async () => {
    const r = await req('GET', '/auth/me', undefined, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.user.id, userId);
  });
});

describe('Money movement scaffolding', () => {
  test('GET /money/status reports provider disabled by default', async () => {
    const r = await req('GET', '/money/status');
    assert.equal(r.status, 200);
    assert.equal(r.body.provider, 'unconfigured');
    assert.equal(r.body.liveTransfersEnabled, false);
  });

  test('GET /money/account returns the pooled account and zero ledger balance', async () => {
    const r = await req('GET', '/money/account', undefined, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.account.account_type, 'pooled_fbo');
    assert.equal(r.body.balance.available_cents, 0);
  });

  test('GET /money/costs/report returns configurable planning costs', async () => {
    const r = await req('GET', '/money/costs/report', undefined, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.currency, 'usd');
    assert.ok(r.body.profiles.some(profile => profile.provider === 'stripe' && profile.operation === 'ach_deposit' && profile.rate_bps === 80));
    assert.ok(r.body.profiles.some(profile => profile.provider === 'bankbox' && profile.operation === 'service_fee' && profile.rate_bps === 500));
    assert.deepEqual(r.body.totals, []);
  });

  test('POST /money/funding-sources creates a tokenized source record', async () => {
    const r = await req('POST', '/money/funding-sources', {
      type: 'bank_account',
      provider: 'plaid',
      provider_account_id: 'item_test',
      provider_payment_method_id: 'pm_test',
    }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.status, 'pending');
  });

  test('POST /money/deposits remains disabled until a provider is configured', async () => {
    const r = await req('POST', '/money/deposits', { amount_cents: 2500, funding_source_id: 1 }, token);
    assert.equal(r.status, 503);
    assert.equal(r.body.liveTransfersEnabled, false);
  });

  test('POST /money/purchase-intents creates a purchase target without spending', async () => {
    const r = await req('POST', '/money/purchase-intents', {
      merchant_name: 'Test Merchant',
      item_reference: 'item-123',
      amount_cents: 9900,
    }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.purchase_intent.status, 'pending');
    assert.equal(r.body.ready_to_reserve, false);
  });
});

// ---- Affiliate Tests ----
describe('Affiliate', () => {
  test('POST /affiliate/campaigns - creates campaign with tracking metadata', async () => {
    const r = await req('POST', '/affiliate/campaigns', {
      name: 'Summer Sale',
      destination_url: 'https://merchant.example/checkout',
      commission_type: 'revshare',
      commission_rate_bps: 750,
      currency: 'usd',
    }, token);
    assert.equal(r.status, 201);
    assert.ok(r.body.campaign);
    assert.ok(r.body.postback_secret);
    affiliateSlug = r.body.campaign.slug;
    affiliateSecret = r.body.postback_secret;
    assert.equal(r.body.campaign.tracking_path, `/r/${affiliateSlug}`);
    assert.equal(r.body.campaign.postback_path, `/api/affiliate/campaigns/${affiliateSlug}/conversions`);
  });

  test('GET /r/:slug - redirects and stamps click token', async () => {
    const r = await reqPublic('GET', `/r/${affiliateSlug}?utm_source=newsletter&utm_campaign=summer`);
    assert.equal(r.status, 302);
    assert.ok(r.headers.location.includes('bankbox_click_id='));
    assert.ok(r.headers.location.startsWith('https://merchant.example/checkout'));
  });

  test('POST /affiliate/campaigns/:slug/conversions - records idempotent conversion', async () => {
    const redirect = await reqPublic('GET', `/r/${affiliateSlug}`);
    const clickToken = new URL(redirect.headers.location).searchParams.get('bankbox_click_id');
    const r = await req('POST', `/affiliate/campaigns/${affiliateSlug}/conversions`, {
      external_order_id: 'order-1001',
      revenue_cents: 12999,
      currency: 'usd',
      click_token: clickToken,
    }, affiliateSecret);
    assert.equal(r.status, 201);
    assert.equal(r.body.conversion.external_order_id, 'order-1001');
    assert.equal(r.body.conversion.revenue_cents, 12999);
    assert.ok(r.body.conversion.commission_cents > 0);

    const duplicate = await req('POST', `/affiliate/campaigns/${affiliateSlug}/conversions`, {
      external_order_id: 'order-1001',
      revenue_cents: 12999,
      currency: 'usd',
      click_token: clickToken,
    }, affiliateSecret);
    assert.equal(duplicate.status, 200);
    assert.equal(duplicate.body.idempotent, true);
  });

  test('GET /affiliate/overview - aggregates campaign metrics', async () => {
    const r = await req('GET', '/affiliate/overview', undefined, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.campaigns, 1);
    assert.equal(r.body.conversions, 1);
    assert.equal(r.body.clicks, 2);
  });
});

// ---- Goals Tests ----
describe('Goals', () => {
  test('GET /goals - unauthenticated returns 401', async () => {
    const r = await req('GET', '/goals');
    assert.equal(r.status, 401);
  });

  test('GET /goals - empty list initially', async () => {
    const r = await req('GET', '/goals', undefined, token);
    assert.equal(r.status, 200);
    assert.deepEqual(r.body, []);
  });

  test('POST /goals - missing fields returns 400', async () => {
    const r = await req('POST', '/goals', { name: 'Test' }, token);
    assert.equal(r.status, 400);
  });

  test('POST /goals - negative target returns 400', async () => {
    const r = await req('POST', '/goals', { name: 'Test', target_amount: -100 }, token);
    assert.equal(r.status, 400);
  });

  test('POST /goals - creates goal successfully', async () => {
    const r = await req('POST', '/goals', { name: 'Vacation', target_amount: 2000, icon: '✈️', color: '#06b6d4' }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.name, 'Vacation');
    assert.equal(r.body.target_amount, 2000);
    assert.equal(r.body.current_amount, 0);
    goalId = r.body.id;
  });

  test('POST /goals - creates second goal', async () => {
    const r = await req('POST', '/goals', { name: 'Emergency Fund', target_amount: 5000 }, token);
    assert.equal(r.status, 201);
    secondGoalId = r.body.id;
  });

  test('GET /goals - lists both goals', async () => {
    const r = await req('GET', '/goals', undefined, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.length, 2);
  });

  test('PATCH /goals/:id - updates name', async () => {
    const r = await req('PATCH', `/goals/${goalId}`, { name: 'Europe Trip' }, token);
    assert.equal(r.status, 200);
    assert.equal(r.body.name, 'Europe Trip');
  });

  test('PATCH /goals/:id - target below current balance rejected', async () => {
    // First deposit some money, then try to lower target below it
    await req('POST', `/goals/${goalId}/deposit`, { amount: 500 }, token);
    const r = await req('PATCH', `/goals/${goalId}`, { target_amount: 100 }, token);
    assert.equal(r.status, 400);
  });

  test('DELETE /goals/:id - wrong user gets 404', async () => {
    // Register a second user and try to delete first user's goal
    const r2 = await req('POST', '/auth/register', { email: 'user2@test.com', password: 'pass123', name: 'User 2' });
    const token2 = r2.body.token;
    const r = await req('DELETE', `/goals/${goalId}`, undefined, token2);
    assert.equal(r.status, 404);
  });
});

// ---- Fund Management Tests ----
describe('Fund Management', () => {
  test('GET /goals/:id/transactions - empty initially (goal has one deposit from prior test)', async () => {
    const r = await req('GET', `/goals/${goalId}/transactions`, undefined, token);
    assert.equal(r.status, 200);
    assert.ok(Array.isArray(r.body));
    // Has 1 deposit from the target-below-balance test
    assert.equal(r.body.length, 1);
    assert.equal(r.body[0].type, 'deposit');
    assert.equal(r.body[0].amount, 500);
  });

  test('POST /goals/:id/deposit - adds funds', async () => {
    const r = await req('POST', `/goals/${goalId}/deposit`, { amount: 300, note: 'Top-up' }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.transaction.type, 'deposit');
    assert.equal(r.body.transaction.amount, 300);
    assert.equal(r.body.transaction.note, 'Top-up');
    assert.equal(r.body.goal.current_amount, 800);
  });

  test('POST /goals/:id/deposit - zero amount returns 400', async () => {
    const r = await req('POST', `/goals/${goalId}/deposit`, { amount: 0 }, token);
    assert.equal(r.status, 400);
  });

  test('POST /goals/:id/deposit - fully funded goal returns 400', async () => {
    // Fill the goal first
    await req('POST', `/goals/${goalId}/deposit`, { amount: 9999 }, token); // will cap at target
    // Try to add more
    const r = await req('POST', `/goals/${goalId}/deposit`, { amount: 1 }, token);
    assert.equal(r.status, 400);
  });

  test('POST /goals/:id/withdraw - removes funds', async () => {
    const r = await req('POST', `/goals/${goalId}/withdraw`, { amount: 100, note: 'Small withdrawal' }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.transaction.type, 'withdrawal');
    assert.equal(r.body.transaction.amount, 100);
    assert.equal(r.body.goal.current_amount, 1900);
  });

  test('POST /goals/:id/withdraw - more than balance returns 400', async () => {
    const r = await req('POST', `/goals/${goalId}/withdraw`, { amount: 99999 }, token);
    assert.equal(r.status, 400);
    assert.ok(r.body.error.includes('Insufficient'));
  });

  test('POST /goals/:id/transfer - moves funds between goals', async () => {
    const r = await req('POST', `/goals/${goalId}/transfer`, {
      to_goal_id: secondGoalId,
      amount: 200,
      note: 'Move to emergency fund',
    }, token);
    assert.equal(r.status, 201);
    assert.equal(r.body.transactions.out.type, 'transfer_out');
    assert.equal(r.body.transactions.in.type, 'transfer_in');
    assert.equal(r.body.transactions.out.amount, 200);
    assert.equal(r.body.transactions.in.amount, 200);
    assert.equal(r.body.from_goal.current_amount, 1700);
    assert.equal(r.body.to_goal.current_amount, 200);
  });

  test('POST /goals/:id/transfer - same goal returns 400', async () => {
    const r = await req('POST', `/goals/${goalId}/transfer`, { to_goal_id: goalId, amount: 100 }, token);
    assert.equal(r.status, 400);
  });

  test('POST /goals/:id/transfer - insufficient funds returns 400', async () => {
    const r = await req('POST', `/goals/${goalId}/transfer`, { to_goal_id: secondGoalId, amount: 99999 }, token);
    assert.equal(r.status, 400);
    assert.ok(r.body.error.includes('Insufficient'));
  });

  test('GET /goals/:id/transactions - history shows all types', async () => {
    const r = await req('GET', `/goals/${goalId}/transactions`, undefined, token);
    assert.equal(r.status, 200);
    const types = r.body.map(t => t.type);
    assert.ok(types.includes('deposit'));
    assert.ok(types.includes('withdrawal'));
    assert.ok(types.includes('transfer_out'));
  });

  test('GET /goals/:id/transactions - second goal shows transfer_in', async () => {
    const r = await req('GET', `/goals/${secondGoalId}/transactions`, undefined, token);
    assert.equal(r.status, 200);
    const types = r.body.map(t => t.type);
    assert.ok(types.includes('transfer_in'));
    // Check related_goal_name is populated
    const transferIn = r.body.find(t => t.type === 'transfer_in');
    assert.ok(transferIn.related_goal_name, 'related_goal_name should be populated');
  });

  test('DELETE /goals/:id - deletes goal and cascades transactions', async () => {
    // Create a temp goal, deposit, delete
    const g = await req('POST', '/goals', { name: 'Temp', target_amount: 100 }, token);
    await req('POST', `/goals/${g.body.id}/deposit`, { amount: 10 }, token);
    const del = await req('DELETE', `/goals/${g.body.id}`, undefined, token);
    assert.equal(del.status, 200);
    // Confirm it's gone
    const get = await req('GET', `/goals/${g.body.id}`, undefined, token);
    assert.equal(get.status, 404);
  });
});
