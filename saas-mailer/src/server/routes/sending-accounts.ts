import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { getOrganizationId } from "../tenancy";
import { connectSendingAccount, listSendingAccounts, sendWithAccount } from "../sending/service";

export function createSendingAccountRoutes(database: Database): Hono {
  const routes = new Hono();
  routes.post("/api/sending-accounts", async (c) => {
    try {
      const organizationId = getOrganizationId(c.req.raw);
      const body = await c.req.json();
      return c.json(connectSendingAccount(database, organizationId, body), 201);
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Invalid sending account" }, 400);
    }
  });
  routes.get("/api/sending-accounts", (c) => {
    try { return c.json(listSendingAccounts(database, getOrganizationId(c.req.raw))); }
    catch (error) { return c.json({ error: error instanceof Error ? error.message : "Invalid organization" }, 400); }
  });
  routes.post("/api/sending-accounts/:id/send", async (c) => {
    try {
      const result = await sendWithAccount(database, getOrganizationId(c.req.raw), c.req.param("id"), await c.req.json());
      return c.json(result, 200);
    } catch (error) { return c.json({ error: error instanceof Error ? error.message : "Send failed" }, 400); }
  });
  return routes;
}
