import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { listEvents } from "../events/service";
import { requireTenant } from "../auth/middleware";

export function createEventRoutes(database: Database) {
  const routes = new Hono();
  routes.get("/api/events", (c) => {
    try { return c.json({ events: listEvents(database, requireTenant(database, c.req.raw).organizationId) }); }
    catch { return c.json({ error: "Unable to list events" }, 400); }
  });
  return routes;
}
