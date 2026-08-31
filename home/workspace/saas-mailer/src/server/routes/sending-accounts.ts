import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { connectSendingAccount, connectSendingAccountPostgres, listSendingAccounts, listSendingAccountsPostgres, sendWithAccount, sendWithAccountPostgres } from "../sending/service";

function logRouteError(operation: string, error: unknown): void {
  console.error(`Sending account ${operation} failed`, error);
}

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }

export function createSendingAccountRoutes(database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.post("/api/sending-accounts", async (c) => {
    try {
      const organizationId = (isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw)).organizationId;
      const body = await c.req.json();
      return c.json(isPostgres(database) ? await connectSendingAccountPostgres(database, organizationId, body) : connectSendingAccount(database, organizationId, body), 201);
    } catch (error) {
      logRouteError("connection", error);
      return c.json({ error: "Unable to connect sending account" }, 400);
    }
  });
  routes.get("/api/sending-accounts", async (c) => {
    try { const organizationId = (isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw)).organizationId; const accounts = isPostgres(database) ? await listSendingAccountsPostgres(database, organizationId) : listSendingAccounts(database, organizationId);
      return c.json({ accounts }); }
    catch (error) {
      logRouteError("listing", error);
      return c.json({ error: "Unable to list sending accounts" }, 400);
    }
  });
  routes.post("/api/sending-accounts/:id/send", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const result = isPostgres(database)
        ? await sendWithAccountPostgres(database, tenant.organizationId, c.req.param("id"), await c.req.json())
        : await sendWithAccount(database, tenant.organizationId, c.req.param("id"), await c.req.json());
      return c.json(result, 200);
    } catch (error) {
      logRouteError("send", error);
      return c.json({ error: "Unable to send message" }, 400);
    }
  });
  return routes;
}
