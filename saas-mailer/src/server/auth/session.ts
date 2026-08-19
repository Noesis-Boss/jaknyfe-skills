import type { Database } from "bun:sqlite";
import { createHash, randomBytes, randomUUID, timingSafeEqual } from "node:crypto";

export type Session = { id: string; token: string; userId: string; organizationId: string; expiresAt: string };
export const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;

function hashToken(token: string): Buffer { return createHash("sha256").update(token).digest(); }

export async function createSession(database: Database, userId: string, organizationId: string): Promise<Session> {
  const membership = database.query<{ role: string }>("SELECT role FROM organization_members WHERE user_id = ? AND organization_id = ?").get(userId, organizationId);
  if (!membership) throw new Error("Organization access denied");
  const token = randomBytes(32).toString("base64url");
  const expiresAt = new Date(Date.now() + SESSION_TTL_MS).toISOString();
  const id = randomUUID();
  database.query("INSERT INTO auth_sessions (id, user_id, organization_id, token_hash, expires_at) VALUES (?, ?, ?, ?, ?)").run(id, userId, organizationId, hashToken(token).toString("hex"), expiresAt);
  return { id, token, userId, organizationId, expiresAt };
}

export function revokeSession(database: Database, token: string): void { database.query("UPDATE auth_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE token_hash = ? AND revoked_at IS NULL").run(hashToken(token).toString("hex")); }

export function lookupSession(database: Database, token: string): { userId: string; organizationId: string; role: string; expiresAt: string } | null {
  const presented = hashToken(token);
  const rows = database.query<{ token_hash: string; user_id: string; organization_id: string; role: string; expires_at: string }>("SELECT s.token_hash, s.user_id, s.organization_id, m.role, s.expires_at FROM auth_sessions s JOIN organization_members m ON m.user_id = s.user_id AND m.organization_id = s.organization_id WHERE s.revoked_at IS NULL AND s.expires_at > CURRENT_TIMESTAMP").all();
  for (const row of rows) {
    const stored = Buffer.from(row.token_hash, "hex");
    if (stored.length === presented.length && timingSafeEqual(stored, presented)) return { userId: row.user_id, organizationId: row.organization_id, role: row.role, expiresAt: row.expires_at };
  }
  return null;
}
