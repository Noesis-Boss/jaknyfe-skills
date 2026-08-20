import { createHmac, randomBytes, timingSafeEqual } from "node:crypto";

type OAuthProvider = "gmail" | "microsoft";
type OAuthState = { provider: OAuthProvider; organizationId: string; userId: string; nonce: string; expiresAt: number };

const usedNonces = new Map<string, number>();

function secret(): string {
  const value = process.env.SESSION_SECRET;
  if (!value) throw new Error("OAuth state signing is not configured");
  return value;
}

function sign(payload: string): string { return createHmac("sha256", secret()).update(payload).digest("base64url"); }

export function createOAuthState(input: { provider: OAuthProvider; organizationId: string; userId: string }, now = Date.now()): string {
  const state: OAuthState = { ...input, nonce: randomBytes(18).toString("base64url"), expiresAt: now + 10 * 60_000 };
  const payload = Buffer.from(JSON.stringify(state)).toString("base64url");
  return `${payload}.${sign(payload)}`;
}

export function consumeOAuthState(value: string, expected: { provider: OAuthProvider; organizationId: string; userId: string }, now = Date.now()): OAuthState {
  const [payload, signature] = value.split(".");
  if (!payload || !signature) throw new Error("Invalid OAuth state");
  const expectedSignature = sign(payload);
  if (signature.length !== expectedSignature.length || !timingSafeEqual(Buffer.from(signature), Buffer.from(expectedSignature))) throw new Error("Invalid OAuth state");
  let state: OAuthState;
  try { state = JSON.parse(Buffer.from(payload, "base64url").toString("utf8")); } catch { throw new Error("Invalid OAuth state"); }
  if (state.expiresAt <= now || state.provider !== expected.provider || state.organizationId !== expected.organizationId || state.userId !== expected.userId) throw new Error("Invalid OAuth state");
  if (usedNonces.has(state.nonce)) throw new Error("OAuth state already used");
  usedNonces.set(state.nonce, state.expiresAt);
  for (const [nonce, expiresAt] of usedNonces) if (expiresAt <= now) usedNonces.delete(nonce);
  return state;
}

export function oauthAuthorizationUrl(provider: OAuthProvider, state: string, config: { callbackOrigin: string; googleClientId?: string; microsoftClientId?: string }): string {
  if (provider === "gmail") {
    if (!config.googleClientId) throw new Error("Google OAuth is not configured");
    const params = new URLSearchParams({ client_id: config.googleClientId, redirect_uri: `${config.callbackOrigin}/api/oauth/gmail/callback`, response_type: "code", access_type: "offline", prompt: "consent", scope: "https://www.googleapis.com/auth/gmail.send", state });
    return `https://accounts.google.com/o/oauth2/v2/auth?${params}`;
  }
  if (!config.microsoftClientId) throw new Error("Microsoft OAuth is not configured");
  const params = new URLSearchParams({ client_id: config.microsoftClientId, redirect_uri: `${config.callbackOrigin}/api/oauth/microsoft/callback`, response_type: "code", response_mode: "query", scope: "offline_access https://graph.microsoft.com/Mail.Send User.Read", state });
  return `https://login.microsoftonline.com/common/oauth2/v2.0/authorize?${params}`;
}
