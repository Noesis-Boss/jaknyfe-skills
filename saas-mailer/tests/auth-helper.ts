import { execute } from "../src/server/db";
import { createSession } from "../src/server/auth/session";
import { database } from "../src/server";

let sequence = 0;
export async function authFor(organizationId: string): Promise<string> {
  execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)", [organizationId, organizationId]);
  const email = `test-${organizationId}-${sequence++}@example.com`;
  const userId = `user-${organizationId}-${sequence}`;
  execute(database, "INSERT INTO users (id, email) VALUES (?, ?)", [userId, email]);
  execute(database, "INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)", [organizationId, userId, "owner"]);
  const session = await createSession(database, userId, organizationId);
  return `saas_mailer_session=${encodeURIComponent(session.token)}`;
}
