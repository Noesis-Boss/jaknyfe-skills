const { getProvider } = require('./providers');
const providerName = process.env.MONEY_PROVIDER || 'unconfigured';

function provider() { return getProvider(providerName); }

async function createFundingRequest({ amountCents, currency, fundingSourceId, idempotencyKey }) {
  return provider().createFundingRequest({ amountCents, currency, fundingSourceId, idempotencyKey });
}

async function submitPurchase({ amountCents, currency, merchantName, idempotencyKey }) {
  return provider().submitPurchase({ amountCents, currency, merchantName, idempotencyKey });
}

module.exports = { providerName, createFundingRequest, submitPurchase, getProvider };
