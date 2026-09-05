import { randomUUID } from "node:crypto";
import type { PostgresDatabase } from "../server/postgres";
import { processQueuedSendPostgres } from "../server/worker/process-send";
import { claimQueuedSends, releaseLease } from "./lease";
import { retryAt } from "./backoff";
import { createTenantRateLimiter } from "./rate-limit";

export type WorkerOptions = { pollMs?: number; batchSize?: number; tenantSendsPerMinute?: number; workerId?: string; onError?: (error: unknown) => void };

export async function runWorker(database: PostgresDatabase, signal: AbortSignal, options: WorkerOptions = {}): Promise<void> {
  const pollMs = options.pollMs ?? 5_000;
  const workerId = options.workerId ?? `worker-${randomUUID()}`;
  const limiter = createTenantRateLimiter(options.tenantSendsPerMinute ?? 30);
  while (!signal.aborted) {
    const jobs = await claimQueuedSends(database, workerId, new Date(), options.batchSize ?? 10);
    for (const job of jobs) {
      if (!limiter.tryAcquire(job.organizationId)) {
        await releaseLease(database, workerId, (job as typeof job & { id?: string }).id ?? job.idempotencyKey, undefined);
        continue;
      }
      try {
        const result = await processQueuedSendPostgres(database, job);
        const next = result.status === "retryable_failure" ? retryAt(1) : undefined;
        await releaseLease(database, workerId, (job as typeof job & { id?: string }).id ?? job.idempotencyKey, next);
      } catch (error) {
        options.onError?.(error);
        await releaseLease(database, workerId, (job as typeof job & { id?: string }).id ?? job.idempotencyKey, retryAt(1));
      }
    }
    if (!signal.aborted) await new Promise(resolve => setTimeout(resolve, pollMs));
  }
}
