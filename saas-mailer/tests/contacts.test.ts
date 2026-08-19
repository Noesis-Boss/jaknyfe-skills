import { describe, expect, test } from "bun:test";
import { execute, migrate, openDatabase, query } from "../src/server/db";
import { parseContactsCsv } from "../src/server/contacts/csv";
import { importContacts } from "../src/server/contacts/service";
import app, { database as appDatabase } from "../src/server";

describe("contact CSV import", () => {
  test("parses valid rows, normalizes email, and preserves custom fields", () => {
    const contacts = parseContactsCsv('Email,First Name,Company\n Alice@Example.COM ,Ada,Acme');
    expect(contacts).toEqual([{ email: "alice@example.com", first_name: "Ada", last_name: undefined, custom_fields: { company: "Acme" } }]);
  });

  test("skips missing and malformed email rows", () => {
    expect(parseContactsCsv("email,name\n,nope\nnot-an-email,Nope\nok@example.com,Yes")).toHaveLength(1);
  });

  test("deduplicates within an organization but not across organizations", () => {
    const db = openDatabase(); migrate(db); execute(db, "INSERT INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["org-a", "A", "org-b", "B"]);
    const contact = parseContactsCsv("email\na@example.com\nA@EXAMPLE.COM");
    expect(importContacts(db, "org-a", contact)).toEqual({ inserted: 1, skipped: 1, invalid: 0 });
    expect(importContacts(db, "org-b", contact)).toEqual({ inserted: 1, skipped: 1, invalid: 0 });
    expect(query(db, "SELECT COUNT(*) AS count FROM contacts")[0]?.count).toBe(2);
  });

  test("imports CSV through the tenant-scoped API", async () => {
    execute(appDatabase, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)", ["org-api", "API"]);
    const response = await app.fetch(new Request("http://localhost/api/contacts/import", { method: "POST", headers: { "x-organization-id": "org-api", "content-type": "text/csv" }, body: "email\na@example.com\nmissing\na@example.com" }));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ inserted: 1, skipped: 1, invalid: 1 });
  });
});
