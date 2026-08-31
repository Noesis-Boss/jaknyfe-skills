import { randomUUID } from "node:crypto";
import { createSession } from "../src/server/auth/session";
import { database } from "../src/server";
import { execute } from "../src/server/db";

export async function authFor(organizationId: string): Promise<string> {
  const userId = randomUUID();
  const email = `${userId}@example.com`;
  const passwordHash = await Bun.password.hash("test-password-123");
  execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)", [organizationId, organizationId]);
  execute(database, "INSERT INTO users (id, email) VALUES (?, ?)", [userId, email]);
  execute(database, "INSERT INTO auth_passwords (user_id, password_hash) VALUES (?, ?)", [userId, passwordHash]);
  execute(database, "INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)", [organizationId, userId, "owner"]);
  const session = await createSession(database, userId, organizationId);
  return `saas_mailer_session=${encodeURIComponent(session.token)}`;
}
