import { randomUUID } from "node:crypto";
import type { PostgresDatabase, PostgresTransaction } from "../postgres";

export type RepositoryContext = { database: PostgresDatabase; organizationId: string };
type Db = PostgresDatabase | PostgresTransaction;

async function rows<T>(db: Db, text: string, params: unknown[] = []) { return db.query<T>(text, params); }
async function one<T>(db: Db, text: string, params: unknown[] = []) { return (await rows<T>(db, text, params))[0] || null; }

export function repositories(context: RepositoryContext) {
  const { database, organizationId } = context;
  const scoped = <T>(fn: (db: Db) => Promise<T>) => fn(database);
  const create = (db: Db) => repositories({ database: { ...database, query: <T>(text: string, params?: unknown[]) => db.query<T>(text, params), execute: (text: string, params?: unknown[]) => db.execute(text, params) } as PostgresDatabase, organizationId });

  return {
    contacts: {
      list: () => scoped(db => rows(db, "SELECT * FROM contacts WHERE organization_id = $1 ORDER BY created_at, id", [organizationId])),
      find: (id: string) => scoped(db => one(db, "SELECT * FROM contacts WHERE organization_id = $1 AND id = $2", [organizationId, id])),
      insert: (input: { email: string; firstName?: string; lastName?: string; customFields?: object }) => scoped(db => one(db, "INSERT INTO contacts (id, organization_id, email, first_name, last_name, custom_fields) VALUES ($1,$2,$3,$4,$5,$6) ON CONFLICT (organization_id,email) DO NOTHING RETURNING *", [randomUUID(), organizationId, input.email.trim().toLowerCase(), input.firstName || null, input.lastName || null, JSON.stringify(input.customFields || {})])),
      update: (id: string, input: { firstName?: string; lastName?: string; customFields?: object }) => scoped(db => one(db, "UPDATE contacts SET first_name = $1, last_name = $2, custom_fields = $3 WHERE organization_id = $4 AND id = $5 RETURNING *", [input.firstName || null, input.lastName || null, JSON.stringify(input.customFields || {}), organizationId, id])),
    },
    accounts: {
      list: () => scoped(db => rows(db, "SELECT id, organization_id, provider, email, status, daily_send_limit, timezone, created_at FROM sending_accounts WHERE organization_id = $1 ORDER BY created_at, id", [organizationId])),
      insert: (input: { provider: string; email: string; credentialCiphertext: string }) => scoped(db => one(db, "INSERT INTO sending_accounts (id, organization_id, provider, email, credential_ciphertext) VALUES ($1,$2,$3,$4,$5) RETURNING id, organization_id, provider, email, status, created_at", [randomUUID(), organizationId, input.provider, input.email.trim().toLowerCase(), input.credentialCiphertext])),
      updateCredentials: (id: string, credentialCiphertext: string) => scoped(db => one(db, "UPDATE sending_accounts SET credential_ciphertext = $1 WHERE organization_id = $2 AND id = $3 RETURNING *", [credentialCiphertext, organizationId, id])),
      findActive: (id: string) => scoped(db => one(db, "SELECT * FROM sending_accounts WHERE organization_id = $1 AND id = $2 AND status = 'active'", [organizationId, id])),
      pause: (id: string) => scoped(db => db.execute("UPDATE sending_accounts SET status = 'paused' WHERE organization_id = $1 AND id = $2", [organizationId, id])),
    },
    campaigns: {
      list: () => scoped(db => rows(db, "SELECT * FROM campaigns WHERE organization_id = $1 ORDER BY created_at, id", [organizationId])),
      find: (id: string, lock = false) => scoped(db => one(db, `SELECT * FROM campaigns WHERE organization_id = $1 AND id = $2${lock ? " FOR UPDATE" : ""}`, [organizationId, id])),
      insert: (name: string) => scoped(db => one(db, "INSERT INTO campaigns (id, organization_id, name) VALUES ($1,$2,$3) RETURNING *", [randomUUID(), organizationId, name])),
      updateSettings: (id: string, accountId: string | null, windowStart: string | null, windowEnd: string | null, dailyLimit: number) => scoped(db => one(db, "UPDATE campaigns SET sending_account_id = $1, sending_window_start = $2, sending_window_end = $3, daily_send_limit = $4 WHERE organization_id = $5 AND id = $6 RETURNING *", [accountId, windowStart, windowEnd, dailyLimit, organizationId, id])),
      insertStep: (campaignId: string, order: number, subject: string, body: string, delayMinutes: number) => scoped(db => one(db, "INSERT INTO campaign_steps (id, organization_id, campaign_id, step_order, subject, body, delay_minutes) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *", [randomUUID(), organizationId, campaignId, order, subject, body, delayMinutes])),
      approve: (id: string, approvedAt: string, approvedBy: string) => scoped(db => one(db, "UPDATE campaigns SET status = 'approved', approved_at = $1, approved_by = $2 WHERE organization_id = $3 AND id = $4 RETURNING *", [approvedAt, approvedBy, organizationId, id])),
      enroll: (campaignId: string, contactId: string) => scoped(async db => (await db.execute("INSERT INTO campaign_contacts (campaign_id, contact_id, organization_id) VALUES ($1,$2,$3) ON CONFLICT (campaign_id, contact_id) DO NOTHING", [campaignId, contactId, organizationId])) > 0),
      updateStatus: (id: string, status: string) => scoped(db => one(db, "UPDATE campaigns SET status = $1 WHERE organization_id = $2 AND id = $3 RETURNING *", [status, organizationId, id])),
    },
    messages: {
      findByIdempotencyKey: (key: string, lock = false) => scoped(db => one(db, `SELECT * FROM messages WHERE organization_id = $1 AND idempotency_key = $2${lock ? " FOR UPDATE" : ""}`, [organizationId, key])),
      insert: (input: Record<string, unknown>) => scoped(db => one(db, "INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, status, idempotency_key, subject, body, error_code) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10) ON CONFLICT (idempotency_key) DO NOTHING RETURNING *", [input.id || randomUUID(), organizationId, input.campaignId || null, input.contactId || null, input.sendingAccountId || null, input.status, input.idempotencyKey, input.subject || "", input.body || "", input.errorCode || null])),
      markSent: (id: string, providerMessageId: string, sentAt: string) => scoped(db => one(db, "UPDATE messages SET status = 'sent', provider_message_id = $1, sent_at = $2 WHERE organization_id = $3 AND id = $4 RETURNING *", [providerMessageId, sentAt, organizationId, id])),
    },
    events: {
      insert: (input: { type: string; messageId?: string; contactId?: string; payload?: object }) => scoped(db => one(db, "INSERT INTO events (id, organization_id, message_id, contact_id, type, payload) VALUES ($1,$2,$3,$4,$5,$6) RETURNING *", [randomUUID(), organizationId, input.messageId || null, input.contactId || null, input.type, JSON.stringify(input.payload || {})])),
      list: () => scoped(db => rows(db, "SELECT * FROM events WHERE organization_id = $1 ORDER BY created_at DESC, id DESC", [organizationId])),
      updateContactStatus: (contactId: string, status: string) => scoped(db => db.execute("UPDATE campaign_contacts SET status = $1 WHERE organization_id = $2 AND contact_id = $3 AND status NOT IN ('replied', 'bounced', 'unsubscribed')", [status, organizationId, contactId])),
    },
    suppressions: {
      findEmail: (email: string) => scoped(db => one(db, "SELECT * FROM suppression_list WHERE organization_id = $1 AND email = $2", [organizationId, email.trim().toLowerCase()])),
      add: (email: string, reason: string) => scoped(db => one(db, "INSERT INTO suppression_list (organization_id, email, reason) VALUES ($1,$2,$3) ON CONFLICT (organization_id,email) DO UPDATE SET reason = EXCLUDED.reason RETURNING *", [organizationId, email.trim().toLowerCase(), reason])),
    },
    audit: {
      insert: (input: { action: string; entityType: string; entityId?: string; metadata?: object; userId?: string }) => scoped(db => one(db, "INSERT INTO audit_log (id, organization_id, user_id, action, entity_type, entity_id, metadata) VALUES ($1,$2,$3,$4,$5,$6,$7) RETURNING *", [randomUUID(), organizationId, input.userId || null, input.action, input.entityType, input.entityId || null, JSON.stringify(input.metadata || {})])),
      list: () => scoped(db => rows(db, "SELECT * FROM audit_log WHERE organization_id = $1 ORDER BY created_at DESC, id DESC", [organizationId])),
    },
    transaction: <T>(fn: (tx: ReturnType<typeof repositories>) => Promise<T>) => database.transaction(async tx => fn(create(tx))),
  };
}
