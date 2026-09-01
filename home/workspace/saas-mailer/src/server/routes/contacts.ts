import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { countInvalidContacts, parseContactsCsv } from "../contacts/csv";
import { importContacts, importContactsPostgres, listContacts, listContactsPostgres } from "../contacts/service";

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
  routes.get("/api/contacts", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const q = c.req.query("q") || undefined;
      const contacts = isPostgres(database) ? await listContactsPostgres(database, tenant.organizationId, q) : listContacts(database, tenant.organizationId, q);
      return c.json({ contacts });
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Unable to list contacts" }, 400);
    }
  });
  routes.get("/api/contacts/:id", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("id");
      const contact = isPostgres(database)
        ? await (await import("../contacts/service")).contactStore(database, tenant.organizationId).find(id)
        : database.query("SELECT id, email, first_name, last_name, created_at FROM contacts WHERE organization_id = ? AND id = ?").get(tenant.organizationId, id);
      if (!contact) return c.json({ error: "Contact not found" }, 404);
      return c.json(contact);
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Unable to fetch contact" }, 400);
    }
  });
  routes.patch("/api/contacts/:id", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("id");
      const body = await c.req.json();
      const contact = isPostgres(database)
        ? await (await import("../contacts/service")).contactStore(database, tenant.organizationId).update(id, { firstName: body.firstName, lastName: body.lastName })
        : (database.query("UPDATE contacts SET first_name = ?, last_name = ? WHERE organization_id = ? AND id = ?").run(body.firstName || null, body.lastName || null, tenant.organizationId, id).changes
          ? database.query("SELECT id, email, first_name, last_name, created_at FROM contacts WHERE organization_id = ? AND id = ?").get(tenant.organizationId, id)
          : null);
      if (!contact) return c.json({ error: "Contact not found" }, 404);
      return c.json(contact);
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Unable to update contact" }, 400);
    }
  });
  routes.delete("/api/contacts/:id", async (c) => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("id");
      const deleted = isPostgres(database)
        ? await (await import("../contacts/service")).contactStore(database, tenant.organizationId).delete(id)
        : database.query("DELETE FROM contacts WHERE organization_id = ? AND id = ?").run(tenant.organizationId, id).changes > 0;
      if (!deleted) return c.json({ error: "Contact not found" }, 404);
      return c.json({ ok: true });
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Unable to delete contact" }, 400);
    }
  });
  return routes;
}
