import app from "../src/server";
import { execute } from "../src/server/db";
import { database } from "../src/server";

let sequence = 0;
export async function authFor(organizationId: string): Promise<string> {
  execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)", [organizationId, organizationId]);
  const email = `test-${organizationId}-${sequence++}@example.com`;
  const response = await app.fetch(new Request("http://localhost/api/auth/register", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email, password: "correct horse battery staple", organization_id: organizationId }) }));
  if (response.status !== 201) throw new Error(`auth setup failed: ${response.status}`);
  return response.headers.get("set-cookie")!.split(";")[0];
}
