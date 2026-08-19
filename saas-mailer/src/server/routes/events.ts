import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { listEvents } from "../events/service";
import { getOrganizationId } from "../tenancy";

export function createEventRoutes(database: Database) {
  const routes = new Hono();
  routes.get("/api/events", (c) => {
    try { return c.json({ events: listEvents(database, getOrganizationId(c.req.raw)) }); }
    catch { return c.json({ error: "Unable to list events" }, 400); }
  });
  return routes;
}
