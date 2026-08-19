import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
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
