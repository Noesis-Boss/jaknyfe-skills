import { createHmac } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";

const secret = () => process.env.TRACKING_SECRET || process.env.SESSION_SECRET || "tracking-dev-secret";

type TokenPurpose = "click" | "unsubscribe";

function hmacFor(messageId: string, purpose: TokenPurpose): string {
  return createHmac("sha256", secret()).update(`${purpose}:${messageId}`).digest("base64url").slice(0, 22);
}

function signToken(messageId: string, purpose: TokenPurpose): string {
  return Buffer.from(`${messageId}.${hmacFor(messageId, purpose)}`).toString("base64url");
}

function verifyToken(token: string, purpose: TokenPurpose): string | null {
  try {
    const decoded = Buffer.from(token, "base64url").toString("utf8");
    const index = decoded.lastIndexOf(".");
    if (index <= 0) return null;
    const messageId = decoded.slice(0, index);
    return hmacFor(messageId, purpose) === decoded.slice(index + 1) ? messageId : null;
  } catch {
    return null;
  }
}

export function signTrackingToken(messageId: string): string {
  return signToken(messageId, "click");
}

export function signUnsubscribeToken(messageId: string): string {
  return signToken(messageId, "unsubscribe");
}

export function verifyTrackingToken(token: string): string | null {
  return verifyToken(token, "click");
}

export function verifyUnsubscribeToken(token: string): string | null {
  return verifyToken(token, "unsubscribe");
}

export function publicBaseUrl(): string {
  return (process.env.PUBLIC_BASE_URL || process.env.OAUTH_CALLBACK_ORIGIN || "http://localhost:3000").replace(/\/$/, "");
}

export function unsubscribeUrl(messageId: string): string {
  return `${publicBaseUrl()}/api/t/u/${signUnsubscribeToken(messageId)}`;
}

export async function resolveTenantBrand(database: Database | PostgresDatabase, organizationId: string): Promise<string | null> {
  if (pg(database)) {
    const rows = await database.query<{ name: string }>("SELECT name FROM organizations WHERE id = $1", [organizationId]);
    return rows[0]?.name || null;
  }
  const row = database.query<{ name: string }, [string]>("SELECT name FROM organizations WHERE id = ?").get(organizationId);
  return row?.name || null;
}

export function injectTracking(body: string, messageId: string): string {
  const base = publicBaseUrl();
  const token = signTrackingToken(messageId);
  const rewritten = body.replace(/(https?:\/\/[^\s"'<>]+)/g, url => `${base}/api/t/c/${token}?url=${encodeURIComponent(url)}`);
  const footer = `<div style="margin-top:24px;padding-top:12px;border-top:1px solid #e5e5e5;font-family:sans-serif;font-size:12px;color:#888"><a href="${unsubscribeUrl(messageId)}" style="color:#888">Unsubscribe</a></div>`;
  return `${rewritten}${footer}<img src="${base}/api/t/o/${token}" width="1" height="1" alt="" style="display:none" />`;
}

function pg(db: Database | PostgresDatabase): db is PostgresDatabase {
  return "sql" in db;
}

export async function recordPublicEvent(database: Database | PostgresDatabase, messageId: string, type: "opened" | "clicked" | "unsubscribed", payload: Record<string, unknown> = {}) {
  const json = JSON.stringify(payload);
  if (pg(database)) {
    await database.query("INSERT INTO events (id, organization_id, message_id, type, payload) SELECT gen_random_uuid()::text, organization_id, id, $3, $4::jsonb FROM messages WHERE id = $1", [messageId, messageId, type, json]);
  } else {
    database.query("INSERT INTO events (id, organization_id, message_id, type, payload) SELECT lower(hex(randomblob(16))), organization_id, id, ?, ? FROM messages WHERE id = ?").run(type, json, messageId);
  }
}

export type MessageRecipient = { organizationId: string; email: string; contactId: string | null };

export async function resolveMessageRecipient(database: Database | PostgresDatabase, messageId: string): Promise<MessageRecipient | null> {
  if (pg(database)) {
    const rows = await database.query<{ organization_id: string; contact_id: string | null; email: string }>(
      "SELECT m.organization_id, m.contact_id, c.email FROM messages m JOIN contacts c ON c.organization_id = m.organization_id AND c.id = m.contact_id WHERE m.id = $1",
      [messageId],
    );
    const row = rows[0];
    return row ? { organizationId: row.organization_id, email: row.email, contactId: row.contact_id } : null;
  }
  const row = database.query<{ organization_id: string; contact_id: string | null; email: string }, [string]>(
    "SELECT m.organization_id, m.contact_id, c.email FROM messages m JOIN contacts c ON c.organization_id = m.organization_id AND c.id = m.contact_id WHERE m.id = ?",
  ).get(messageId);
  return row ? { organizationId: row.organization_id, email: row.email, contactId: row.contact_id } : null;
}

export async function suppressEmail(database: Database | PostgresDatabase, organizationId: string, email: string, reason: string): Promise<void> {
  if (pg(database)) {
    await database.query(
      "INSERT INTO suppression_list (organization_id, email, reason) VALUES ($1, $2, $3) ON CONFLICT (organization_id, email) DO UPDATE SET reason = EXCLUDED.reason",
      [organizationId, email, reason],
    );
  } else {
    database.query(
      "INSERT INTO suppression_list (organization_id, email, reason) VALUES (?, ?, ?) ON CONFLICT (organization_id, email) DO UPDATE SET reason = excluded.reason",
    ).run(organizationId, email, reason);
  }
}

export async function processUnsubscribe(database: Database | PostgresDatabase, token: string): Promise<void> {
  const messageId = verifyUnsubscribeToken(token);
  if (!messageId) return;
  const recipient = await resolveMessageRecipient(database, messageId);
  if (!recipient) return;
  await suppressEmail(database, recipient.organizationId, recipient.email, "one_click_unsubscribe");
  await recordPublicEvent(database, messageId, "unsubscribed");
}
