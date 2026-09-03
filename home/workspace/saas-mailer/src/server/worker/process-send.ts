import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { loadQueueEligibility } from "../campaigns/eligibility";
import { loadQueueEligibilityPostgres } from "../campaigns/eligibility";
import { recordEvent } from "../events/service";
import { recordEventPostgres } from "../events/service";
import { sendWithAccount } from "../sending/service";
import { sendWithAccountPostgres } from "../sending/service";
import { injectTracking } from "../tracking/tokens";
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
    const result = await sendWithAccount(database, job.organizationId, job.sendingAccountId, { to: database.query<{ email: string }, [string, string]>("SELECT email FROM contacts WHERE id = ? AND organization_id = ?").get(job.contactId, job.organizationId)!.email, subject: job.subject, body: injectTracking(job.body, messageId), from: "" });
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

export async function processQueuedSendPostgres(database: PostgresDatabase, job: QueuedSendJob): Promise<SendAttempt> {
  const claim = await database.transaction(async tx => {
    const existing = (await tx.query<{ id: string; status: string }>("SELECT id, status FROM messages WHERE organization_id = $1 AND idempotency_key = $2 FOR UPDATE", [job.organizationId, job.idempotencyKey]))[0];
    if (existing?.status === "retryable_failure") {
      await tx.execute("UPDATE messages SET status = 'queued', attempt_count = attempt_count + 1 WHERE organization_id = $1 AND id = $2", [job.organizationId, existing.id]);
      return { id: existing.id, claimed: true };
    }
    if (existing?.status === "processing") return { id: existing.id, claimed: true };
    if (existing) return { id: existing.id, claimed: false };
    const id = randomUUID();
    await tx.execute("INSERT INTO messages (id, organization_id, campaign_id, contact_id, sending_account_id, status, idempotency_key, subject, body) VALUES ($1,$2,$3,$4,$5,'queued',$6,$7,$8)", [id, job.organizationId, job.campaignId, job.contactId, job.sendingAccountId, job.idempotencyKey, job.subject, job.body]);
    return { id, claimed: true };
  });
  if (!claim.claimed) return { status: "duplicate", messageId: claim.id };

  const eligibility = await loadQueueEligibilityPostgres(database, job.organizationId, job.campaignId, job.contactId);
  if (!eligibility.eligible) return { status: "rejected", reason: eligibility.reason };
  const contact = (await database.query<{ email: string }>("SELECT email FROM contacts WHERE organization_id = $1 AND id = $2", [job.organizationId, job.contactId]))[0];
  if (!contact) return { status: "rejected", reason: "contact_not_found" };
  const messageId = claim.id;

  try {
    const result = await sendWithAccountPostgres(database, job.organizationId, job.sendingAccountId, { to: contact.email, subject: job.subject, body: injectTracking(job.body, messageId), from: "" });
    await database.transaction(async tx => {
      await tx.execute("UPDATE messages SET provider_message_id = $1, status = 'sent', sent_at = $2, error_code = NULL, subject = $3, body = $4 WHERE organization_id = $5 AND id = $6", [result.providerMessageId, result.acceptedAt, job.subject, job.body, job.organizationId, messageId]);
      await tx.execute("UPDATE campaign_contacts SET status = 'sent' WHERE organization_id = $1 AND campaign_id = $2 AND contact_id = $3", [job.organizationId, job.campaignId, job.contactId]);
    });
    const saved = (await database.query<{ id: string }>("SELECT id FROM messages WHERE organization_id = $1 AND idempotency_key = $2", [job.organizationId, job.idempotencyKey]))[0];
    await recordEventPostgres(database, { organizationId: job.organizationId, type: "delivered", messageId: saved.id, contactId: job.contactId, payload: { provider_message_id: result.providerMessageId } });
    return { status: "sent", messageId: saved.id };
  } catch (error) {
    const info = failureInfo(error);
    if (info.code === "auth_failed" || info.code === "quota_exceeded") await database.execute("UPDATE sending_accounts SET status = 'paused' WHERE organization_id = $1 AND id = $2", [job.organizationId, job.sendingAccountId]);
    await database.query("UPDATE messages SET status = $1, error_code = $2 WHERE organization_id = $3 AND id = $4", [info.retryable ? "retryable_failure" : "failed", info.code, job.organizationId, messageId]);
    const saved = (await database.query<{ id: string }>("SELECT id FROM messages WHERE organization_id = $1 AND idempotency_key = $2", [job.organizationId, job.idempotencyKey]))[0];
    await recordEventPostgres(database, { organizationId: job.organizationId, type: "failure", messageId: saved.id, contactId: job.contactId, payload: { code: info.code, message: info.message, retryable: info.retryable } });
    return { status: info.retryable ? "retryable_failure" : "permanent_failure", messageId: saved.id, retryable: info.retryable, reason: info.code };
  }
}
