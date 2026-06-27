/** Called once at startup (after initDb) and on PUT /api/settings/proxy. */
export declare function applyProxyUrl(dbValue: string): void;
export declare function getProxyUrl(): string;
/** Toggle the proxy on/off without losing the URL. */
export declare function applyProxyEnabled(enabled: boolean): void;
export declare function isProxyEnabled(): boolean;
/** Set which platforms bypass the proxy. Comma-separated string from DB. */
export declare function applyProxyBypass(platformsCsv: string): void;
export declare function getProxyBypassPlatforms(): string[];
/**
 * Drop-in replacement for `fetch(url, init)` that routes through the
 * configured proxy.  Pass an optional `platform` string to respect the
 * per-platform bypass list.
 *
 * When no proxy is configured, or proxy is disabled, or the platform is
 * in the bypass list, this is a direct pass-through to `fetch()`.
 */
export declare function proxyFetch(url: string, init?: RequestInit, platform?: string): Promise<Response>;
/**
 * Returns true when the proxy is configured AND enabled. Used by the dashboard
 * to show the "Active" badge. Intentionally does NOT construct a dispatcher (so
 * it never triggers the lazy undici import) — "configured + enabled" is exactly
 * what the badge means.
 */
export declare function isProxyActive(): boolean;
//# sourceMappingURL=proxy.d.ts.map