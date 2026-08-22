import { describe, expect, test } from "bun:test";
import { execute, migrate, openDatabase, query } from "../src/server/db";
import { InvalidContactsCsvError, parseContactsCsv } from "../src/server/contacts/csv";
import { importContacts } from "../src/server/contacts/service";
import app, { database as appDatabase } from "../src/server";
import { authFor } from "./auth-helper";

describe("contact CSV import", () => {
  test("parses valid rows, normalizes email, and preserves custom fields", () => {
    const contacts = parseContactsCsv('Email,First Name,Company\n Alice@Example.COM ,Ada,Acme');
    expect(contacts).toEqual([{ email: "alice@example.com", first_name: "Ada", last_name: undefined, custom_fields: { company: "Acme" } }]);
  });

  test("maps common CRM headers and splits a full name", () => {
    const contacts = parseContactsCsv("E-mail,Full Name,Company Name\nJANE@EXAMPLE.COM,Jane Q Public,Acme");
    expect(contacts).toEqual([{ email: "jane@example.com", first_name: "Jane", last_name: "Q Public", custom_fields: { company_name: "Acme" } }]);
  });

  test("maps first and last name aliases without treating them as custom fields", () => {
    const contacts = parseContactsCsv("mail,given name,surname,job title\nada@example.com,Ada,Lovelace,Engineer");
    expect(contacts[0]).toEqual({ email: "ada@example.com", first_name: "Ada", last_name: "Lovelace", custom_fields: { job_title: "Engineer" } });
  });

  test("detects semicolon, tab, and pipe-delimited exports", () => {
    expect(parseContactsCsv("email;name\nada@example.com;Ada")).toHaveLength(1);
    expect(parseContactsCsv("email\tname\nada@example.com\tAda")).toHaveLength(1);
    expect(parseContactsCsv("email|name\nada@example.com|Ada")).toHaveLength(1);
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
    const response = await app.fetch(new Request("http://localhost/api/contacts/import", { method: "POST", headers: { cookie: await authFor("org-api"), "content-type": "text/csv" }, body: "email\na@example.com\nmissing\na@example.com" }));
    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ inserted: 1, skipped: 1, invalid: 1 });
  });

  test("rejects malformed CSV and missing email header", () => {
    expect(() => parseContactsCsv('email,name\n"unterminated,Ada')).toThrow(InvalidContactsCsvError);
    expect(() => parseContactsCsv('name\nAda')).toThrow("missing required email header");
    expect(() => parseContactsCsv('email,name\nada"broken,Ada')).toThrow("stray quote");
  });

  test("strips a UTF-8 BOM from the first header", () => {
    expect(parseContactsCsv("\uFEFFemail,name\na@example.com,Ada")).toHaveLength(1);
  });

  test("migrates an existing contacts table with custom_fields", () => {
    const db = openDatabase();
    db.exec("CREATE TABLE contacts (id TEXT PRIMARY KEY, organization_id TEXT NOT NULL, email TEXT NOT NULL, first_name TEXT, last_name TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)");
    migrate(db);
    expect(query(db, "SELECT custom_fields FROM contacts")).toEqual([]);
    db.exec("INSERT INTO contacts (id, organization_id, email) VALUES ('c1', 'org-a', 'old@example.com')");
    expect(query(db, "SELECT custom_fields FROM contacts")[0]?.custom_fields).toBe("{}");
  });

  test("uses deterministic conflict-safe duplicate imports", () => {
    const db = openDatabase(); migrate(db); execute(db, "INSERT INTO organizations (id, name) VALUES (?, ?)", ["org-d", "D"]);
    const contacts = parseContactsCsv("email,first_name\na@example.com,First\nA@EXAMPLE.COM,Second");
    expect(importContacts(db, "org-d", contacts)).toEqual({ inserted: 1, skipped: 1, invalid: 0 });
    expect(query(db, "SELECT first_name FROM contacts WHERE organization_id = ?", ["org-d"])[0]?.first_name).toBe("First");
  });
});
