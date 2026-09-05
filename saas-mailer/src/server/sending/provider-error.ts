export type ProviderErrorKind = "auth_failed" | "quota_exceeded" | "provider_error" | "permanent_failure" | "hard_bounce";

export class ProviderError extends Error {
  constructor(public readonly code: ProviderErrorKind, message: string, public readonly retryable = false) {
    super(message);
    this.name = "ProviderError";
  }
}

const bounceMarkers = /(invalid|not found|does not exist|no such|user unknown|unknown user|mailbox (unavailable|not found|disabled)|address rejected|bounced?|undeliverable|recipient)/i;

export function providerError(response: Response, body: string): ProviderError {
  if (response.status === 401 || response.status === 403) return new ProviderError("auth_failed", "Provider authentication failed");
  if (response.status === 429) return new ProviderError("quota_exceeded", "Provider quota exceeded", true);
  if (response.status >= 500) return new ProviderError("provider_error", "Provider temporarily unavailable", true);
  if (bounceMarkers.test(body)) return new ProviderError("hard_bounce", body || "Provider rejected the recipient");
  return new ProviderError("permanent_failure", body || "Provider rejected the message");
}
