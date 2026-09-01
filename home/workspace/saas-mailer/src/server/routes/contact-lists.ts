import { Hono } from "hono";
import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";

const pg = (db: Database | PostgresDatabase): db is PostgresDatabase => "sql" in db;
export function createContactListRoutes(database: Database | PostgresDatabase) {
  const routes = new Hono();
  routes.get("/api/contact-lists", async c => {
    const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
    const lists = pg(database) ? await database.query("SELECT l.id,l.name,l.created_at,count(m.contact_id)::int AS contact_count FROM contact_lists l LEFT JOIN contact_list_members m ON m.list_id=l.id WHERE l.organization_id=$1 GROUP BY l.id ORDER BY l.created_at,l.id", [tenant.organizationId]) : database.query("SELECT l.id,l.name,l.created_at,count(m.contact_id) AS contact_count FROM contact_lists l LEFT JOIN contact_list_members m ON m.list_id=l.id WHERE l.organization_id=? GROUP BY l.id ORDER BY l.created_at,l.id").all(tenant.organizationId);
    return c.json({ lists });
  });
  routes.post("/api/contact-lists", async c => {
    const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
    const body = await c.req.json(); const name = String(body.name || "").trim(); if (!name) return c.json({ error: "List name is required" }, 400);
    const id = randomUUID();
    try { if (pg(database)) await database.execute("INSERT INTO contact_lists (id,organization_id,name) VALUES (?,?,?)", [id, tenant.organizationId, name]); else database.query("INSERT INTO contact_lists (id,organization_id,name) VALUES (?,?,?)").run(id, tenant.organizationId, name); return c.json({ id, name, contact_count: 0 }, 201); } catch { return c.json({ error: "A list with that name already exists" }, 409); }
  });
  routes.post("/api/contact-lists/:id/members", async c => {
    const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const listId = c.req.param("id"); const ids = (await c.req.json()).contact_ids || [];
    let added = 0; for (const contactId of ids) { try { const sql = "INSERT INTO contact_list_members (list_id,contact_id,organization_id) VALUES (?,?,?) ON CONFLICT DO NOTHING"; if (pg(database)) added += await database.execute(sql, [listId, contactId, tenant.organizationId]); else added += database.query(sql.replace("ON CONFLICT DO NOTHING", "ON CONFLICT(list_id,contact_id) DO NOTHING")).run(listId, contactId, tenant.organizationId).changes; } catch {} }
    return c.json({ added });
  });
  return routes;
}
