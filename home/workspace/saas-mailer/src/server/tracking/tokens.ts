import { createHmac } from "node:crypto";
import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";

const secret = () => process.env.TRACKING_SECRET || process.env.SESSION_SECRET || "tracking-dev-secret";

export function signTrackingToken(messageId: string): string {
  const mac = createHmac("sha256", secret()).update(messageId).digest("base64url").slice(0, 22);
  return Buffer.from(`${messageId}.${mac}`).toString("base64url");
}

export function verifyTrackingToken(token: string): string | null {
  try {
    const decoded = Buffer.from(token, "base64url").toString("utf8");
    const index = decoded.lastIndexOf(".");
    if (index <= 0) return null;
    const messageId = decoded.slice(0, index);
    const mac = decoded.slice(index + 1);
    const expected = createHmac("sha256", secret()).update(messageId).digest("base64url").slice(0, 22);
    return mac === expected ? messageId : null;
  } catch {
    return null;
  }
}

export function publicBaseUrl(): string {
  return (process.env.PUBLIC_BASE_URL || process.env.OAUTH_CALLBACK_ORIGIN || "http://localhost:3000").replace(/\/$/, "");
}

export function injectTracking(body: string, messageId: string): string {
  const base = publicBaseUrl();
  const token = signTrackingToken(messageId);
  const rewritten = body.replace(/(https?:\/\/[^\s"'<>]+)/g, url => `${base}/api/t/c/${token}?url=${encodeURIComponent(url)}`);
  return `${rewritten}<img src="${base}/api/t/o/${token}" width="1" height="1" alt="" style="display:none" />`;
}

function pg(db: Database | PostgresDatabase): db is PostgresDatabase {
  return "sql" in db;
}

export async function recordPublicEvent(database: Database | PostgresDatabase, messageId: string, type: "opened" | "clicked", payload: Record<string, unknown> = {}) {
  const json = JSON.stringify(payload);
  if (pg(database)) {
    await database.query("INSERT INTO events (id, organization_id, message_id, type, payload) SELECT gen_random_uuid()::text, organization_id, id, $3, $4::jsonb FROM messages WHERE id = $1 AND organization_id IS NOT NULL AND id IN (SELECT id FROM messages WHERE id = $1) AND EXISTS (SELECT 1 FROM messages WHERE id = $1)", [messageId, messageId, type, json]);
  } else {
    database.query("INSERT INTO events (id, organization_id, message_id, type, payload) SELECT lower(hex(randomblob(16))), organization_id, id, ?, ? FROM messages WHERE id = ?").run(type, json, messageId);
  }
}
