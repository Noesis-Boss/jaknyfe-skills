import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { repositories } from "../repositories";

export type EventType = "delivered" | "reply" | "bounce" | "unsubscribe" | "failure" | "opened" | "clicked";
export type RecordEventInput = { organizationId: string; type: EventType; messageId?: string; contactId?: string; payload?: Record<string, unknown> };

export function recordEvent(database: Database, input: RecordEventInput) {
  const eventId = randomUUID();
  database.exec("BEGIN IMMEDIATE");
  try {
    database.query("INSERT INTO events (id, organization_id, message_id, contact_id, type, payload) VALUES (?, ?, ?, ?, ?, ?)").run(eventId, input.organizationId, input.messageId || null, input.contactId || null, input.type, JSON.stringify(input.payload || {}));
    if (input.contactId && ["reply", "bounce", "unsubscribe"].includes(input.type)) {
      database.query("UPDATE campaign_contacts SET status = ? WHERE organization_id = ? AND contact_id = ? AND status NOT IN ('replied', 'bounced', 'unsubscribed')").run(input.type === "reply" ? "replied" : input.type === "bounce" ? "bounced" : "unsubscribed", input.organizationId, input.contactId);
    }
    database.exec("COMMIT");
  } catch (error) { database.exec("ROLLBACK"); throw error; }
  return database.query("SELECT * FROM events WHERE id = ?").get(eventId);
}

export function listEvents(database: Database, organizationId: string) {
  return database.query("SELECT * FROM events WHERE organization_id = ? ORDER BY created_at DESC, id DESC").all(organizationId);
}

export async function recordEventPostgres(database: PostgresDatabase, input: RecordEventInput) {
  return repositories({ database, organizationId: input.organizationId }).transaction(async (tx) => {
    const event = await tx.events.insert(input);
    if (input.contactId && ["reply", "bounce", "unsubscribe"].includes(input.type)) {
      const status = input.type === "reply" ? "replied" : input.type === "bounce" ? "bounced" : "unsubscribed";
      await tx.events.updateContactStatus(input.contactId, status);
    }
    return event;
  });
}

export async function listEventsPostgres(database: PostgresDatabase, organizationId: string) {
  return repositories({ database, organizationId }).events.list();
}
