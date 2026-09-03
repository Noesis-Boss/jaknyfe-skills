import { randomBytes } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { createSession, type Session } from "./session";
import { createSessionPostgres } from "./postgres";

export type OidcConfig = { issuer: string; clientId: string; clientSecret: string; callbackOrigin: string };
export type OidcState = { state: string; verifier: string; expiresAt: number };

export function oidcConfig(env: NodeJS.ProcessEnv = process.env): OidcConfig | null {
  const issuer = env.AUTH_ISSUER?.trim(), clientId = env.AUTH_CLIENT_ID?.trim(), clientSecret = env.AUTH_CLIENT_SECRET?.trim(), callbackOrigin = env.AUTH_CALLBACK_ORIGIN?.trim();
  return issuer && clientId && clientSecret && callbackOrigin ? { issuer: issuer.replace(/\/$/, ""), clientId, clientSecret, callbackOrigin } : null;
}

export function createState(): OidcState { return { state: randomBytes(24).toString("base64url"), verifier: randomBytes(32).toString("base64url"), expiresAt: Date.now() + 10 * 60_000 }; }
export async function authorizationUrl(config: OidcConfig, state: OidcState): Promise<string> {
  const discovery = await fetch(`${config.issuer}/.well-known/openid-configuration`).then(r => r.json()) as { authorization_endpoint: string };
  const challenge = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(state.verifier));
  const challengeText = Buffer.from(challenge).toString("base64url");
  const p = new URLSearchParams({ client_id: config.clientId, redirect_uri: `${config.callbackOrigin}/api/auth/oidc/callback`, response_type: "code", scope: "openid profile email", state: state.state, code_challenge: challengeText, code_challenge_method: "S256" });
  return `${discovery.authorization_endpoint}?${p}`;
}
export async function exchange(config: OidcConfig, code: string, verifier: string) {
  const discovery = await fetch(`${config.issuer}/.well-known/openid-configuration`).then(r => r.json()) as { token_endpoint: string; userinfo_endpoint: string };
  const body = new URLSearchParams({ grant_type: "authorization_code", code, redirect_uri: `${config.callbackOrigin}/api/auth/oidc/callback`, client_id: config.clientId, client_secret: config.clientSecret, code_verifier: verifier });
  const token = await fetch(discovery.token_endpoint, { method: "POST", headers: { "content-type": "application/x-www-form-urlencoded" }, body }).then(r => r.json()) as { access_token?: string };
  if (!token.access_token) throw new Error("OIDC token exchange failed");
  return fetch(discovery.userinfo_endpoint, { headers: { authorization: `Bearer ${token.access_token}` } }).then(r => r.json()) as Promise<{ sub?: string; email?: string }>;
}
export async function sessionForIdentity(database: Database | PostgresDatabase, email: string): Promise<Session | Awaited<ReturnType<typeof createSessionPostgres>> | null> {
  const normalized = email.trim().toLowerCase();
  if ("sql" in database) {
    const rows = await database.query<{ id: string; organization_id: string }>("SELECT u.id, m.organization_id FROM users u JOIN organization_members m ON m.user_id=u.id WHERE u.email=$1 ORDER BY m.created_at LIMIT 1", [normalized]);
    return rows[0] ? createSessionPostgres(database, rows[0].id, rows[0].organization_id) : null;
  }
  const row = database.query<{ id: string; organization_id: string }>("SELECT u.id, m.organization_id FROM users u JOIN organization_members m ON m.user_id=u.id WHERE u.email=? ORDER BY m.created_at LIMIT 1").get(normalized);
  return row ? createSession(database, row.id, row.organization_id) : null;
}
