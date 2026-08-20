import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { countInvalidContacts, parseContactsCsv } from "../contacts/csv";
import { importContacts, importContactsPostgres } from "../contacts/service";

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase {
  return "sql" in database;
}

export function createContactsRoutes(database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.post("/api/contacts/import", async (c) => {
    try {
      const tenant = isPostgres(database)
        ? await requireTenantPostgres(database, c.req.raw)
        : requireTenant(database, c.req.raw);
      const contentType = c.req.header("content-type") || "";
      let csvText = "";
      if (contentType.includes("multipart/form-data")) {
        const form = await c.req.raw.formData();
        const file = form.get("file");
        csvText = file instanceof File ? await file.text() : String(form.get("csv") || "");
      } else csvText = await c.req.text();
      const parsed = parseContactsCsv(csvText);
      const result = isPostgres(database)
        ? await importContactsPostgres(database, tenant.organizationId, parsed)
        : importContacts(database, tenant.organizationId, parsed);
      result.invalid = countInvalidContacts(csvText);
      return c.json(result, 200);
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Invalid import" }, 400);
    }
  });
  return routes;
}
