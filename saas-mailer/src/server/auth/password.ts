import type { Database } from "bun:sqlite";
import { randomUUID } from "node:crypto";

export type AuthUser = { id: string; email: string; organizationId?: string };

export async function registerUser(database: Database, email: string, password: string, organizationName: string, role = "owner"): Promise<AuthUser> {
  const normalizedEmail = email.trim().toLowerCase();
  const normalizedOrganizationName = organizationName?.trim();
  if (!/^\S+@\S+\.\S+$/.test(normalizedEmail) || password.length < 12 || !normalizedOrganizationName) throw new Error("Invalid registration");
  if (database.query("SELECT id FROM users WHERE email = ?").get(normalizedEmail)) throw new Error("Email already registered");
  const userId = randomUUID();
  const organizationId = randomUUID();
  const hash = await Bun.password.hash(password, { algorithm: "argon2id" });
  database.exec("BEGIN IMMEDIATE");
  try {
    database.query("INSERT INTO organizations (id, name) VALUES (?, ?)").run(organizationId, normalizedOrganizationName);
    database.query("INSERT INTO users (id, email) VALUES (?, ?)").run(userId, normalizedEmail);
    database.query("INSERT INTO auth_passwords (user_id, password_hash) VALUES (?, ?)").run(userId, hash);
    database.query("INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)").run(organizationId, userId, role);
    database.exec("COMMIT");
  } catch (error) {
    database.exec("ROLLBACK");
    throw error;
  }
  return { id: userId, email: normalizedEmail, organizationId };
}

export async function verifyPassword(database: Database, email: string, password: string): Promise<AuthUser | null> {
  const row = database.query<{ id: string; email: string; password_hash: string }>("SELECT u.id, u.email, p.password_hash FROM users u JOIN auth_passwords p ON p.user_id = u.id WHERE u.email = ?").get(email.trim().toLowerCase());
  if (!row) return null;
  const valid = await Bun.password.verify(password, row.password_hash);
  return valid ? { id: row.id, email: row.email } : null;
}
