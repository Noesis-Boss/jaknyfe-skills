import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { repositories } from "../repositories";
import type { ParsedContact } from "./csv";

export type ImportResult = { inserted: number; skipped: number; invalid: number };

export function importContacts(database: Database, organizationId: string, contacts: ParsedContact[]): ImportResult {
  let inserted = 0;
  let skipped = 0;
  database.exec("BEGIN IMMEDIATE");
  try {
    const insert = database.query("INSERT OR IGNORE INTO contacts (id, organization_id, email, first_name, last_name, custom_fields) VALUES (?, ?, ?, ?, ?, ?)");
    for (const contact of contacts) {
      const result = insert.run(randomUUID(), organizationId, contact.email.trim().toLowerCase(), contact.first_name || null, contact.last_name || null, JSON.stringify(contact.custom_fields || {}));
      if (result.changes === 1) inserted += 1;
      else skipped += 1;
    }
    database.exec("COMMIT");
  } catch (error) {
    database.exec("ROLLBACK");
    throw error;
  }
  return { inserted, skipped, invalid: 0 };
}

export async function importContactsPostgres(database: PostgresDatabase, organizationId: string, contacts: ParsedContact[]): Promise<ImportResult> {
  let inserted = 0;
  let skipped = 0;
  const store = repositories({ database, organizationId });
  await store.transaction(async tx => {
    for (const contact of contacts) {
      const row = await tx.contacts.insert({
        email: contact.email,
        firstName: contact.first_name,
        lastName: contact.last_name,
        customFields: contact.custom_fields,
      });
      if (row) inserted += 1;
      else skipped += 1;
    }
  });
  return { inserted, skipped, invalid: 0 };
}

export type ContactRow = { id: string; email: string; first_name: string | null; last_name: string | null; created_at: string };

export function listContacts(database: Database, organizationId: string, q?: string): ContactRow[] {
  if (q) {
    const term = `%${q.toLowerCase()}%`;
    return database.query<ContactRow, [string, string, string, string]>(
      "SELECT id, email, first_name, last_name, created_at FROM contacts WHERE organization_id = ? AND (lower(email) LIKE ? OR lower(first_name) LIKE ? OR lower(last_name) LIKE ?) ORDER BY created_at DESC, id"
    ).all(organizationId, term, term, term);
  }
  return database.query<ContactRow, [string]>("SELECT id, email, first_name, last_name, created_at FROM contacts WHERE organization_id = ? ORDER BY created_at DESC, id").all(organizationId);
}

export async function listContactsPostgres(database: PostgresDatabase, organizationId: string, q?: string): Promise<ContactRow[]> {
  const store = repositories({ database, organizationId });
  let rows;
  if (q) {
    const term = `%${q.toLowerCase()}%`;
    rows = await database.query(
      "SELECT id, email, first_name, last_name, created_at FROM contacts WHERE organization_id = $1 AND (lower(email) LIKE $2 OR lower(first_name) LIKE $2 OR lower(last_name) LIKE $2) ORDER BY created_at DESC, id",
      [organizationId, term]
    );
  } else {
    rows = await store.contacts.list();
  }
  return rows.map(row => ({ id: row.id, email: row.email, first_name: row.first_name, last_name: row.last_name, created_at: row.created_at }));
}

export function contactStore(database: PostgresDatabase, organizationId: string) {
  const store = repositories({ database, organizationId });
  return {
    find: (id: string) => store.contacts.find(id),
    update: (id: string, input: { firstName?: string; lastName?: string }) => store.contacts.update(id, input),
    delete: async (id: string) => {
      const existing = await store.contacts.find(id);
      if (!existing) return false;
      await database.execute("DELETE FROM contacts WHERE organization_id = $1 AND id = $2", [organizationId, id]);
      return true;
    },
  };
}
