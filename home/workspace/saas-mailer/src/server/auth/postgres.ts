import type { PostgresDatabase } from "../postgres";
import { createHash, randomBytes, randomUUID } from "node:crypto";

export type PostgresAuthUser = { id: string; email: string; organizationId?: string };
export type PostgresSession = { id: string; token: string; userId: string; organizationId: string; role: string; expiresAt: string };
const SESSION_TTL_MS = 7 * 24 * 60 * 60 * 1000;

const hashToken = (token: string) => createHash("sha256").update(token).digest("hex");

export async function registerUserPostgres(database: PostgresDatabase, email: string, password: string, organizationName: string, role = "owner"): Promise<PostgresAuthUser> {
  const normalizedEmail = email.trim().toLowerCase();
  const normalizedOrganizationName = organizationName?.trim();
  if (!/^\S+@\S+\.\S+$/.test(normalizedEmail) || password.length < 12 || !normalizedOrganizationName) throw new Error("Invalid registration");
  const hash = await Bun.password.hash(password, { algorithm: "argon2id" });
  const userId = randomUUID();
  const organizationId = randomUUID();
  await database.transaction(async tx => {
    if ((await tx.query("SELECT id FROM users WHERE email = $1", [normalizedEmail])).length) throw new Error("Email already registered");
    await tx.execute("INSERT INTO organizations (id, name) VALUES ($1, $2)", [organizationId, normalizedOrganizationName]);
    await tx.execute("INSERT INTO users (id, email) VALUES ($1, $2)", [userId, normalizedEmail]);
    await tx.execute("INSERT INTO auth_passwords (user_id, password_hash) VALUES ($1, $2)", [userId, hash]);
    await tx.execute("INSERT INTO organization_members (organization_id, user_id, role) VALUES ($1, $2, $3)", [organizationId, userId, role]);
  });
  return { id: userId, email: normalizedEmail, organizationId };
}

export async function verifyPasswordPostgres(database: PostgresDatabase, email: string, password: string): Promise<PostgresAuthUser | null> {
  const row = (await database.query<{ id: string; email: string; password_hash: string }>("SELECT u.id, u.email, p.password_hash FROM users u JOIN auth_passwords p ON p.user_id = u.id WHERE u.email = $1", [email.trim().toLowerCase()]))[0];
  if (!row || !(await Bun.password.verify(password, row.password_hash))) return null;
  return { id: row.id, email: row.email };
}

export async function firstMembershipPostgres(database: PostgresDatabase, userId: string) {
  return (await database.query<{ organization_id: string }>("SELECT organization_id FROM organization_members WHERE user_id = $1 ORDER BY created_at LIMIT 1", [userId]))[0] || null;
}

export async function createSessionPostgres(database: PostgresDatabase, userId: string, organizationId: string): Promise<PostgresSession> {
  const membership = (await database.query<{ role: string }>("SELECT role FROM organization_members WHERE user_id = $1 AND organization_id = $2", [userId, organizationId]))[0];
  if (!membership) throw new Error("Organization access denied");
  const token = randomBytes(32).toString("base64url");
  const expiresAt = new Date(Date.now() + SESSION_TTL_MS).toISOString();
  const id = randomUUID();
  await database.execute("INSERT INTO auth_sessions (id, user_id, organization_id, token_hash, expires_at) VALUES ($1, $2, $3, $4, $5)", [id, userId, organizationId, hashToken(token), expiresAt]);
  return { id, token, userId, organizationId, role: membership.role, expiresAt };
}

export async function revokeSessionPostgres(database: PostgresDatabase, token: string): Promise<void> {
  await database.execute("UPDATE auth_sessions SET revoked_at = CURRENT_TIMESTAMP WHERE token_hash = $1 AND revoked_at IS NULL", [hashToken(token)]);
}

export async function lookupSessionPostgres(database: PostgresDatabase, token: string) {
  const row = (await database.query<{ user_id: string; organization_id: string; role: string; expires_at: string }>("SELECT s.user_id, s.organization_id, m.role, s.expires_at FROM auth_sessions s JOIN organization_members m ON m.user_id = s.user_id AND m.organization_id = s.organization_id WHERE s.token_hash = $1 AND s.revoked_at IS NULL AND s.expires_at > CURRENT_TIMESTAMP", [hashToken(token)]))[0];
  return row ? { userId: row.user_id, organizationId: row.organization_id, role: row.role, expiresAt: row.expires_at } : null;
}
