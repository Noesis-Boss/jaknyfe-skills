import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { listEvents } from "../events/service";

export function createEventRoutes(database: Database) {
  const routes = new Hono();
  routes.get("/api/events", (c) => c.json({ events: listEvents(database, c.req.header("x-organization-id") || "") }));
  return routes;
}
