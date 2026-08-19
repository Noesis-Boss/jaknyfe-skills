import { randomUUID } from "node:crypto";
import type { PostgresDatabase, PostgresTransaction } from "../postgres";

export type RepositoryContext = { database: PostgresDatabase; organizationId: string };
type Db = PostgresDatabase | PostgresTransaction;
async function rows<T>(db: Db, text: string, params: unknown[] = []) { return db.query<T>(text, params); }
async function one<T>(db: Db, text: string, params: unknown[] = []) { return (await rows<T>(db, text, params))[0] || null; }

export function repositories(context: RepositoryContext) {
  const { database, organizationId } = context;
  const scoped = <T>(fn: (db: Db) => Promise<T>) => fn(database);
  return {
    contacts: { list: () => scoped(db => rows(db, "SELECT * FROM contacts WHERE organization_id = $1 ORDER BY created_at, id", [organizationId])), insert: (input: { email: string; firstName?: string; lastName?: string; customFields?: object }) => scoped(async db => { const id = randomUUID(); return one(db, "INSERT INTO contacts (id, organization_id, email, first_name, last_name, custom_fields) VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (organization_id,email) DO NOTHING RETURNING *", [id, organizationId, input.email.toLowerCase(), input.firstName || null, input.lastName || null, JSON.stringify(input.customFields || {})]); }) },
    accounts: { list: () => scoped(db => rows(db, "SELECT id, organization_id, provider, email, status, daily_send_limit, timezone, created_at FROM sending_accounts WHERE organization_id = $1 ORDER BY created_at, id", [organizationId])), findActive: (id: string) => scoped(db => one(db, "SELECT * FROM sending_accounts WHERE organization_id = $1 AND id = $2 AND status = 'active'", [organizationId, id])) },
    campaigns: { find: (id: string) => scoped(db => one(db, "SELECT * FROM campaigns WHERE organization_id = $1 AND id = $2", [organizationId, id])), insert: (name: string) => scoped(async db => one(db, "INSERT INTO campaigns (id, organization_id, name) VALUES ($1,$2,$3) RETURNING *", [randomUUID(), organizationId, name])) },
    messages: { findByIdempotencyKey: (key: string, lock = false) => scoped(db => one(db, `SELECT * FROM messages WHERE organization_id = $1 AND idempotency_key = $2${lock ? " FOR UPDATE" : ""}`, [organizationId, key])), insert: (input: Record<string, unknown>) => scoped(db => one(db, "INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, status, idempotency_key, subject, body, error_code) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) ON CONFLICT (idempotency_key) DO NOTHING RETURNING *", [input.id || randomUUID(), organizationId, input.campaignId || null, input.contactId || null, input.sendingAccountId || null, input.status, input.idempotencyKey, input.subject || "", input.body || "", input.errorCode || null])) },
    events: { insert: (input: { type: string; messageId?: string; contactId?: string; payload?: object }) => scoped(db => one(db, "INSERT INTO events (id, organization_id, message_id, contact_id, type, payload) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *", [randomUUID(), organizationId, input.messageId || null, input.contactId || null, input.type, JSON.stringify(input.payload || {})])), list: () => scoped(db => rows(db, "SELECT * FROM events WHERE organization_id = $1 ORDER BY created_at DESC, id DESC", [organizationId])) },
    suppressions: { findEmail: (email: string) => scoped(db => one(db, "SELECT * FROM suppression_list WHERE organization_id = $1 AND email = $2", [organizationId, email.toLowerCase()])) },
    audit: { insert: (input: { action: string; entityType: string; entityId?: string; metadata?: object; userId?: string }) => scoped(db => one(db, "INSERT INTO audit_log (id, organization_id, user_id, action, entity_type, entity_id, metadata) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *", [randomUUID(), organizationId, input.userId || null, input.action, input.entityType, input.entityId || null, JSON.stringify(input.metadata || {})])) },
    transaction: <T>(fn: (tx: ReturnType<typeof repositories>) => Promise<T>) => database.transaction(async tx => fn(repositories({ database: { ...database, transaction: async cb => cb(tx as PostgresTransaction) } as PostgresDatabase, organizationId }))),
  };
}
