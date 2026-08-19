import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { requireTenant } from "../auth/middleware";
import { countInvalidContacts, parseContactsCsv } from "../contacts/csv";
import { importContacts } from "../contacts/service";

export function createContactsRoutes(database: Database): Hono {
  const routes = new Hono();
  routes.post("/api/contacts/import", async (c) => {
    try {
      const organizationId = requireTenant(database, c.req.raw).organizationId;
      const contentType = c.req.header("content-type") || "";
      let csvText = "";
      if (contentType.includes("multipart/form-data")) {
        const form = await c.req.raw.formData();
        const file = form.get("file");
        csvText = file instanceof File ? await file.text() : String(form.get("csv") || "");
      } else csvText = await c.req.text();
      const parsed = parseContactsCsv(csvText);
      const result = importContacts(database, organizationId, parsed);
      result.invalid = countInvalidContacts(csvText);
      return c.json(result, 200);
    } catch (error) {
      return c.json({ error: error instanceof Error ? error.message : "Invalid import" }, 400);
    }
  });
  return routes;
}
