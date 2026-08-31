import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { listEvents, listEventsPostgres } from "../events/service";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }

export function createEventRoutes(database: Database | PostgresDatabase) {
  const routes = new Hono();
  routes.get("/api/events", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const events = isPostgres(database) ? await listEventsPostgres(database, tenant.organizationId) : listEvents(database, tenant.organizationId);
      return c.json({ events });
    }
    catch { return c.json({ error: "Unable to list events" }, 400); }
  });
  return routes;
}
