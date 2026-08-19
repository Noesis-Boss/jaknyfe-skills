import { describe, expect, test } from "bun:test";
import { assertOrganizationRecord } from "../src/server/tenancy";
import { execute, migrate, openDatabase, query } from "../src/server/db";

describe("tenant helpers", () => {
  test("allows records belonging to the active organization", () => {
    expect(() => assertOrganizationRecord({ organization_id: "org-123" }, "org-123")).not.toThrow();
  });

  test("rejects records belonging to another organization", () => {
    expect(() => assertOrganizationRecord({ organization_id: "org-999" }, "org-123")).toThrow(
      "Organization access denied",
    );
  });
});

describe("tenant-safe database schema", () => {
  test("creates the required tables and enables foreign keys on each connection", () => {
    const database = openDatabase();
    migrate(database);
    const tables = query<{ name: string }>(
      database,
      "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%' ORDER BY name",
    ).map((row) => row.name);
    expect(tables).toEqual([
      "audit_log",
      "auth_passwords",
      "auth_sessions",
      "campaign_contacts",
      "campaign_steps",
      "campaigns",
      "contacts",
      "events",
      "messages",
      "organization_members",
      "organizations",
      "sending_accounts",
      "suppression_list",
      "users",
    ]);
    expect(query<{ foreign_keys: number }>(database, "PRAGMA foreign_keys")[0]?.foreign_keys).toBe(1);
    for (const table of ["campaign_steps", "campaign_contacts", "messages", "events"]) {
      expect(query(database, `PRAGMA foreign_key_list(${table})`).length).toBeGreaterThan(0);
    }
    database.close();
  });

  test("rejects mismatched organization relationships", () => {
    const database = openDatabase();
    migrate(database);
    execute(database, "INSERT INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["org-a", "A", "org-b", "B"]);
    execute(database, "INSERT INTO contacts (id, organization_id, email) VALUES (?, ?, ?), (?, ?, ?)", ["contact-a", "org-a", "a@example.com", "contact-b", "org-b", "b@example.com"]);
    execute(database, "INSERT INTO campaigns (id, organization_id, name) VALUES (?, ?, ?), (?, ?, ?)", ["campaign-a", "org-a", "A", "campaign-b", "org-b", "B"]);
    execute(database, "INSERT INTO sending_accounts (id, organization_id, provider, email) VALUES (?, ?, ?, ?), (?, ?, ?, ?)", ["account-a", "org-a", "smtp", "a@example.com", "account-b", "org-b", "smtp", "b@example.com"]);
    execute(database, "INSERT INTO messages (id, organization_id, status, idempotency_key) VALUES (?, ?, ?, ?)", ["message-a", "org-a", "queued", "key-a"]);

    expect(() => execute(database, "INSERT INTO campaign_steps (id, organization_id, campaign_id, step_order, subject, body) VALUES (?, ?, ?, ?, ?, ?)", ["step-x", "org-a", "campaign-b", 1, "subject", "body"])).toThrow();
    expect(() => execute(database, "INSERT INTO campaign_contacts (organization_id, campaign_id, contact_id) VALUES (?, ?, ?)", ["org-a", "campaign-a", "contact-b"])).toThrow();
    expect(() => execute(database, "INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, status, idempotency_key) VALUES (?, ?, ?, ?, ?, ?, ?)", ["message-x", "org-a", "campaign-b", "contact-a", "account-a", "queued", "key-x"])).toThrow();
    expect(() => execute(database, "INSERT INTO events (id, organization_id, message_id, contact_id, type) VALUES (?, ?, ?, ?, ?)", ["event-x", "org-a", "message-a", "contact-b", "bounce"])).toThrow();
    database.close();
  });
});
