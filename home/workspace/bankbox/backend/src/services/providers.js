class ProviderError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
  }
}

class BaseProvider {
  constructor(name) { this.name = name; }

  assertLiveSupport() {
    if (process.env.ENABLE_LIVE_MONEY_MOVEMENT !== 'true') return;
    throw new ProviderError('LIVE_PROVIDER_NOT_IMPLEMENTED', `${this.name} live adapter is not enabled`);
  }

  async createFundingRequest(input) {
    this.assertLiveSupport();
    return { status: 'pending', mode: 'scaffold', provider: this.name, ...input };
  }

  async submitPurchase(input) {
    this.assertLiveSupport();
    return { status: 'pending', mode: 'scaffold', provider: this.name, ...input };
  }
}

class StripeProvider extends BaseProvider {
  constructor() { super('stripe'); }
}

class PlaidProvider extends BaseProvider {
  constructor() { super('plaid'); }

  async createFundingRequest(input) {
    this.assertLiveSupport();
    return { status: 'pending', mode: 'scaffold', provider: this.name, flow: 'plaid_transfer', ...input };
  }
}

function getProvider(name = process.env.MONEY_PROVIDER) {
  if (name === 'stripe') return new StripeProvider();
  if (name === 'plaid') return new PlaidProvider();
  throw new ProviderError('PROVIDER_NOT_CONFIGURED', 'Money provider is not configured');
}

module.exports = { BaseProvider, StripeProvider, PlaidProvider, ProviderError, getProvider };
