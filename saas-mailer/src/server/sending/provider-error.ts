export type ProviderErrorKind = "auth_failed" | "quota_exceeded" | "provider_error" | "permanent_failure";

export class ProviderError extends Error {
  constructor(public readonly code: ProviderErrorKind, message: string, public readonly retryable = false) {
    super(message);
    this.name = "ProviderError";
  }
}

export function providerError(response: Response, body: string): ProviderError {
  if (response.status === 401 || response.status === 403) return new ProviderError("auth_failed", "Provider authentication failed");
  if (response.status === 429) return new ProviderError("quota_exceeded", "Provider quota exceeded", true);
  if (response.status >= 500) return new ProviderError("provider_error", "Provider temporarily unavailable", true);
  return new ProviderError("permanent_failure", body || "Provider rejected the message");
}
