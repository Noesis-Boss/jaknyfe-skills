import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import { loadQueueEligibility } from "../campaigns/eligibility";
import { recordEvent } from "../events/service";
import { sendWithAccount } from "../sending/service";
import type { QueuedSendJob } from "./queue";

export type SendAttempt = { status: "sent" | "duplicate" | "rejected" | "retryable_failure" | "permanent_failure"; messageId?: string; reason?: string; retryable?: boolean };

function failureInfo(error: unknown) {
  const value = error as { retryable?: boolean; code?: string; message?: string };
  return { retryable: value?.retryable === true, code: value?.code || "provider_error", message: value?.message || "Provider send failed" };
}

export async function processQueuedSend(database: Database, job: QueuedSendJob): Promise<SendAttempt> {
  const existing = database.query<{ id: string; status: string }, [string]>("SELECT id, status FROM messages WHERE idempotency_key = ?").get(job.idempotencyKey);
  if (existing && existing.status !== "retryable_failure") return { status: "duplicate", messageId: existing.id };
  if (existing?.status === "retryable_failure") database.query("DELETE FROM messages WHERE id = ? AND idempotency_key = ?").run(existing.id, job.idempotencyKey);
  const eligibility = loadQueueEligibility(database, job.organizationId, job.campaignId, job.contactId);
  if (!eligibility.eligible) return { status: "rejected", reason: eligibility.reason };
  const messageId = randomUUID();
  try {
    const result = await sendWithAccount(database, job.organizationId, job.sendingAccountId, { to: database.query<{ email: string }, [string, string]>("SELECT email FROM contacts WHERE id = ? AND organization_id = ?").get(job.contactId, job.organizationId)!.email, subject: job.subject, body: job.body, from: "" });
    database.query("INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, provider_message_id, status, idempotency_key, sent_at, subject, body) VALUES (?, ?, ?, ?, ?, ?, 'sent', ?, ?, ?, ?)").run(messageId, job.organizationId, job.campaignId, job.contactId, job.sendingAccountId, result.providerMessageId, job.idempotencyKey, result.acceptedAt, job.subject, job.body);
    recordEvent(database, { organizationId: job.organizationId, type: "delivered", messageId, contactId: job.contactId, payload: { provider_message_id: result.providerMessageId } });
    database.query("UPDATE campaign_contacts SET status = 'sent' WHERE organization_id = ? AND campaign_id = ? AND contact_id = ?").run(job.organizationId, job.campaignId, job.contactId);
    return { status: "sent", messageId };
  } catch (error) {
    const info = failureInfo(error);
    if (info.code === "auth_failed" || info.code === "quota_exceeded") database.query("UPDATE sending_accounts SET status = 'paused' WHERE id = ? AND organization_id = ?").run(job.sendingAccountId, job.organizationId);
    database.query("INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, status, idempotency_key, error_code) VALUES (?, ?, ?, ?, ?, ?, ?, ?)").run(messageId, job.organizationId, job.campaignId, job.contactId, job.sendingAccountId, info.retryable ? "retryable_failure" : "failed", job.idempotencyKey, info.code);
    recordEvent(database, { organizationId: job.organizationId, type: "failure", messageId, contactId: job.contactId, payload: { code: info.code, message: info.message, retryable: info.retryable } });
    return { status: info.retryable ? "retryable_failure" : "permanent_failure", messageId, retryable: info.retryable, reason: info.code };
  }
}
