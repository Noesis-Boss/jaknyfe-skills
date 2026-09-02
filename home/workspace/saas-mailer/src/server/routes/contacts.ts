import { Hono } from "hono";
import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { countInvalidContacts, invalidContactRows, parseContactsCsv } from "../contacts/csv";
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
      let importOptions: { listId?: string; newListName?: string; listColumn?: string } = {};
      if (contentType.includes("multipart/form-data")) {
        const form = await c.req.raw.formData();
        const file = form.get("file");
        csvText = file instanceof File ? await file.text() : String(form.get("csv") || "");
        importOptions = { listId: String(form.get("list_id") || "") || undefined, newListName: String(form.get("new_list_name") || "") || undefined, listColumn: String(form.get("list_column") || "") || undefined };
      } else csvText = await c.req.text();
      const parsed = parseContactsCsv(csvText);
      const result = isPostgres(database)
        ? await importContactsPostgres(database, tenant.organizationId, parsed)
        : importContacts(database, tenant.organizationId, parsed);
      result.invalid = countInvalidContacts(csvText);
      if (contentType.includes("multipart/form-data")) {
        const invalidRows = invalidContactRows(csvText);
        let listId = importOptions.listId;
        if (!listId && importOptions.newListName) {
          listId = randomUUID();
          const insert = "INSERT INTO contact_lists (id, organization_id, name) VALUES (?, ?, ? )";
          if (isPostgres(database)) await database.execute(insert, [listId, tenant.organizationId, importOptions.newListName]);
          else database.query(insert).run(listId, tenant.organizationId, importOptions.newListName);
        }
        if (listId) {
          const imported = isPostgres(database)
            ? await database.query<{ id: string; email: string }>("SELECT id,email FROM contacts WHERE organization_id=$1", [tenant.organizationId])
            : database.query<{ id: string; email: string }, [string]>("SELECT id,email FROM contacts WHERE organization_id=?").all(tenant.organizationId);
          const wanted = importOptions.listColumn ? parsed.filter(contact => contact.custom_fields[importOptions.listColumn!]).map(contact => contact.email) : parsed.map(contact => contact.email);
          for (const contact of imported.filter(row => wanted.includes(row.email))) {
            const sql = "INSERT INTO contact_list_members (list_id,contact_id,organization_id) VALUES (?,?,?) ON CONFLICT DO NOTHING";
            if (isPostgres(database)) await database.execute(sql, [listId, contact.id, tenant.organizationId]);
            else database.query(sql.replace("ON CONFLICT DO NOTHING", "ON CONFLICT(list_id,contact_id) DO NOTHING")).run(listId, contact.id, tenant.organizationId);
          }
        }
        return c.json({ ...result, invalid_rows: invalidRows, invalid_csv: invalidRows.length ? `row,email,reason\n${invalidRows.map(row => `${row.row},"${row.email.replaceAll('"', '""')}","${row.reason}"`).join("\n")}` : "" }, 200);
      }
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
