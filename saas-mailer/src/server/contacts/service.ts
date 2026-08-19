import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import { execute, query } from "../db";
import type { ParsedContact } from "./csv";

export type ImportResult = { inserted: number; skipped: number; invalid: number };

export function importContacts(database: Database, organizationId: string, contacts: ParsedContact[]): ImportResult {
  let inserted = 0;
  let skipped = 0;
  const seen = new Set<string>();
  for (const contact of contacts) {
    const email = contact.email.trim().toLowerCase();
    if (seen.has(email) || query(database, "SELECT id FROM contacts WHERE organization_id = ? AND email = ?", [organizationId, email]).length) { skipped += 1; continue; }
    seen.add(email);
    execute(database, "INSERT INTO contacts (id, organization_id, email, first_name, last_name, custom_fields) VALUES (?, ?, ?, ?, ?, ?)", [randomUUID(), organizationId, email, contact.first_name || null, contact.last_name || null, JSON.stringify(contact.custom_fields || {})]);
    inserted += 1;
  }
  return { inserted, skipped, invalid: 0 };
}
