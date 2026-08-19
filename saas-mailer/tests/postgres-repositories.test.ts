import { describe, expect, test } from "bun:test";
import { createPostgresDatabase } from "../src/server/postgres";
import { repositories } from "../src/server/repositories";
import { readFileSync } from "node:fs";

const url = process.env.TEST_POSTGRES_URL;

test("PostgreSQL migration defines tenant constraints and queue indexes", () => {
  const sql = readFileSync(new URL("../db/migrations/postgres/001_initial.sql", import.meta.url), "utf8");
  expect(sql).toContain("schema_migrations");
  expect(sql).toContain("FOREIGN KEY (organization_id, campaign_id)");
  expect(sql).toContain("FOREIGN KEY (organization_id, contact_id)");
  expect(sql).toContain("idx_messages_queue");
  expect(sql).toContain("ON CONFLICT DO NOTHING");
});

describe.skipIf(!url)("PostgreSQL repository contract", () => {
  test("isolates tenants and preserves idempotency", async () => {
    const database = createPostgresDatabase(url!);
    await database.migrate();
    await database.sql`TRUNCATE messages, events, campaign_contacts, campaign_steps, campaigns, contacts, sending_accounts, suppression_list, audit_log, auth_sessions, auth_passwords, organization_members, users, organizations CASCADE`;
    await database.sql`INSERT INTO organizations (id, name) VALUES ('repo-a','A'), ('repo-b','B')`;
    const a = repositories({ database, organizationId: "repo-a" });
    const b = repositories({ database, organizationId: "repo-b" });
    const contact = await a.contacts.insert({ email: "person@example.com" });
    expect(contact?.organization_id).toBe("repo-a");
    expect(await b.contacts.list()).toEqual([]);
    const first = await a.messages.insert({ status: "sent", idempotencyKey: "same-key", contactId: contact!.id });
    const duplicate = await a.messages.insert({ status: "sent", idempotencyKey: "same-key", contactId: contact!.id });
    expect(first?.id).toBeDefined();
    expect(duplicate).toBeNull();
    expect(await b.messages.findByIdempotencyKey("same-key")).toBeNull();
    await expect(a.contacts.update(contact!.id, { firstName: "Updated" })).resolves.toMatchObject({ first_name: "Updated" });
    await expect(a.suppressions.add("person@example.com", "bounce")).resolves.toMatchObject({ organization_id: "repo-a" });
    await expect(b.suppressions.findEmail("person@example.com")).resolves.toBeNull();
    await database.close();
  });
});
