import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { requireTenant } from "../auth/middleware";
import { connectSendingAccount, listSendingAccounts, sendWithAccount } from "../sending/service";

function logRouteError(operation: string, error: unknown): void {
  console.error(`Sending account ${operation} failed`, error);
}

export function createSendingAccountRoutes(database: Database): Hono {
  const routes = new Hono();
  routes.post("/api/sending-accounts", async (c) => {
    try {
      const organizationId = requireTenant(database, c.req.raw).organizationId;
      const body = await c.req.json();
      return c.json(connectSendingAccount(database, organizationId, body), 201);
    } catch (error) {
      logRouteError("connection", error);
      return c.json({ error: "Unable to connect sending account" }, 400);
    }
  });
  routes.get("/api/sending-accounts", (c) => {
    try { return c.json(listSendingAccounts(database, requireTenant(database, c.req.raw).organizationId)); }
    catch (error) {
      logRouteError("listing", error);
      return c.json({ error: "Unable to list sending accounts" }, 400);
    }
  });
  routes.post("/api/sending-accounts/:id/send", async (c) => {
    try {
      const result = await sendWithAccount(database, requireTenant(database, c.req.raw).organizationId, c.req.param("id"), await c.req.json());
      return c.json(result, 200);
    } catch (error) {
      logRouteError("send", error);
      return c.json({ error: "Unable to send message" }, 400);
    }
  });
  return routes;
}
