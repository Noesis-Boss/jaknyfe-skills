import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }
export function createPreferenceRoutes(database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.get("/api/preferences/:contactId", async c => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("contactId");
      const preferences = isPostgres(database) ? await database.query("SELECT topic, status, updated_at FROM subscriber_preferences WHERE organization_id = $1 AND contact_id = $2 ORDER BY topic", [tenant.organizationId, id]) : database.query("SELECT topic, status, updated_at FROM subscriber_preferences WHERE organization_id = ? AND contact_id = ? ORDER BY topic").all(tenant.organizationId, id);
      return c.json({ contact_id: id, preferences });
    } catch { return c.json({ error: "Unable to load preferences" }, 400); }
  });
  routes.put("/api/preferences/:contactId", async c => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("contactId"); const input = await c.req.json(); const topic = String(input.topic || "general"); const status = String(input.status || "subscribed");
      if (!["subscribed", "paused", "unsubscribed"].includes(status)) return c.json({ error: "Invalid preference status" }, 400);
      if (isPostgres(database)) await database.query("INSERT INTO subscriber_preferences (organization_id, contact_id, topic, status, updated_at) VALUES ($1,$2,$3,$4,now()) ON CONFLICT (organization_id,contact_id,topic) DO UPDATE SET status=EXCLUDED.status, updated_at=now()", [tenant.organizationId, id, topic, status]);
      else database.query("INSERT INTO subscriber_preferences (organization_id, contact_id, topic, status, updated_at) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP) ON CONFLICT (organization_id, contact_id, topic) DO UPDATE SET status=excluded.status, updated_at=CURRENT_TIMESTAMP").run(tenant.organizationId, id, topic, status);
      if (status === "unsubscribed") isPostgres(database) ? await database.query("INSERT INTO suppression_list (organization_id,email,reason) SELECT $1,email,'subscriber_unsubscribe' FROM contacts WHERE organization_id=$1 AND id=$2 ON CONFLICT (organization_id,email) DO UPDATE SET reason='subscriber_unsubscribe'", [tenant.organizationId, id]) : database.query("INSERT INTO suppression_list (organization_id,email,reason) SELECT ?,email,'subscriber_unsubscribe' FROM contacts WHERE organization_id=? AND id=? ON CONFLICT (organization_id,email) DO UPDATE SET reason='subscriber_unsubscribe'").run(tenant.organizationId, tenant.organizationId, id);
      return c.json({ ok: true, topic, status });
    } catch { return c.json({ error: "Unable to update preferences" }, 400); }
  });
  return routes;
}
