import type { PostgresDatabase } from "../server/postgres";
import type { QueuedSendJob } from "../server/worker/queue";

export async function claimQueuedSends(database: PostgresDatabase, workerId: string, now = new Date(), batchSize = 10, leaseMs = 120_000): Promise<QueuedSendJob[]> {
  return database.transaction(async tx => {
    const rows = await tx.query<QueuedSendJob & { id: string }>(
      `UPDATE messages SET lease_owner = $1, lease_until = $2, status = 'processing'
       WHERE id IN (SELECT id FROM messages WHERE status IN ('queued', 'retryable_failure', 'processing')
       AND next_attempt_at <= $3 AND (lease_until IS NULL OR lease_until <= $3)
       ORDER BY next_attempt_at, created_at FOR UPDATE SKIP LOCKED LIMIT $4)
       RETURNING id, organization_id AS "organizationId", campaign_id AS "campaignId", contact_id AS "contactId",
       sending_account_id AS "sendingAccountId", subject, body, idempotency_key AS "idempotencyKey"`,
      [workerId, new Date(now.getTime() + leaseMs), now, batchSize],
    );
    return rows;
  });
}

export async function releaseLease(database: PostgresDatabase, workerId: string, messageId: string, nextAttemptAt?: Date): Promise<void> {
  await database.execute(
    `UPDATE messages SET lease_owner = NULL, lease_until = NULL, status = CASE WHEN $4::timestamptz IS NULL THEN status ELSE 'queued' END,
     next_attempt_at = COALESCE($4::timestamptz, next_attempt_at) WHERE id = $1 AND lease_owner = $2`,
    [messageId, workerId, new Date(), nextAttemptAt ?? null],
  );
}
