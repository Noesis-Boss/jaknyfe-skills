import type { Database } from "bun:sqlite";
import { randomUUID } from "node:crypto";

export type AuthUser = { id: string; email: string };

export async function registerUser(database: Database, email: string, password: string, organizationId: string, role = "owner"): Promise<AuthUser> {
  const normalizedEmail = email.trim().toLowerCase();
  if (!/^\S+@\S+\.\S+$/.test(normalizedEmail) || password.length < 12) throw new Error("Invalid registration");
  const organization = database.query<{ id: string }>("SELECT id FROM organizations WHERE id = ?").get(organizationId);
  if (!organization) throw new Error("Organization not found");
  if (database.query("SELECT 1 FROM organization_members WHERE organization_id = ? LIMIT 1").get(organizationId)) throw new Error("Organization registration is closed");
  if (database.query("SELECT id FROM users WHERE email = ?").get(normalizedEmail)) throw new Error("Email already registered");
  const userId = randomUUID();
  const hash = await Bun.password.hash(password, { algorithm: "argon2id" });
  database.exec("BEGIN");
  try {
    database.query("INSERT INTO users (id, email) VALUES (?, ?)").run(userId, normalizedEmail);
    database.query("INSERT INTO auth_passwords (user_id, password_hash) VALUES (?, ?)").run(userId, hash);
    database.query("INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)").run(organizationId, userId, role);
    database.exec("COMMIT");
  } catch (error) {
    database.exec("ROLLBACK");
    throw error;
  }
  return { id: userId, email: normalizedEmail };
}

export async function verifyPassword(database: Database, email: string, password: string): Promise<AuthUser | null> {
  const row = database.query<{ id: string; email: string; password_hash: string }>("SELECT u.id, u.email, p.password_hash FROM users u JOIN auth_passwords p ON p.user_id = u.id WHERE u.email = ?").get(email.trim().toLowerCase());
  if (!row) return null;
  const valid = await Bun.password.verify(password, row.password_hash);
  return valid ? { id: row.id, email: row.email } : null;
}
