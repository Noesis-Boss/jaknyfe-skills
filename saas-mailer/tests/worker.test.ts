import { describe, expect, test } from "bun:test";
import { execute, migrate, openDatabase } from "../src/server/db";
import { approveCampaign, createCampaign, enrollContacts } from "../src/server/campaigns/service";
import { processQueuedSend } from "../src/server/worker/process-send";
import { registerSendingAdapter } from "../src/server/sending/service";

function fixture() {
  const db = openDatabase(); migrate(db);
  execute(db, "INSERT INTO organizations (id, name) VALUES (?, ?)", ["org-a", "A"]);
  execute(db, "INSERT INTO contacts (id, organization_id, email) VALUES (?, ?, ?)", ["c1", "org-a", "a@example.com"]);
  execute(db, "INSERT INTO sending_accounts (id, organization_id, provider, email) VALUES (?, ?, ?, ?)", ["a1", "org-a", "mock", "sender@example.com"]);
  const campaign = createCampaign(db, "org-a", { name: "Intro", sending_account_id: "a1", steps: [{ subject: "Hi", body: "Hello" }] });
  approveCampaign(db, campaign.id, "org-a"); enrollContacts(db, campaign.id, "org-a", ["c1"]);
  return { db, campaign };
}
const job = (campaignId: string) => ({ organizationId: "org-a", campaignId, contactId: "c1", sendingAccountId: "a1", subject: "Hi", body: "Hello", idempotencyKey: "job-1" });

test("successful send persists message and delivered event", async () => { const { db, campaign } = fixture(); const result = await processQueuedSend(db, job(campaign.id)); expect(result.status).toBe("sent"); expect(db.query("SELECT status FROM messages").get()).toEqual({ status: "sent" }); expect(db.query("SELECT type FROM events").get()).toEqual({ type: "delivered" }); });
test("duplicate job does not send twice", async () => { const { db, campaign } = fixture(); await processQueuedSend(db, job(campaign.id)); expect((await processQueuedSend(db, job(campaign.id))).status).toBe("duplicate"); expect(db.query("SELECT COUNT(*) AS count FROM messages").get()).toEqual({ count: 1 }); });
test("suppressed contact is rejected before adapter", async () => { const { db, campaign } = fixture(); execute(db, "INSERT INTO suppression_list (organization_id, email, reason) VALUES (?, ?, ?)", ["org-a", "a@example.com", "manual"]); expect((await processQueuedSend(db, job(campaign.id))).status).toBe("rejected"); expect(db.query("SELECT COUNT(*) AS count FROM messages").get()).toEqual({ count: 0 }); });
test("permanent adapter failure is recorded", async () => { registerSendingAdapter("fail", { async send() { throw Object.assign(new Error("bad credentials"), { code: "auth_failed" }); } }); const { db, campaign } = fixture(); execute(db, "UPDATE sending_accounts SET provider = 'fail' WHERE id = 'a1'"); const result = await processQueuedSend(db, job(campaign.id)); expect(result.status).toBe("permanent_failure"); expect(db.query("SELECT status, error_code FROM messages").get()).toEqual({ status: "failed", error_code: "auth_failed" }); });
test("retryable failure can be retried and pauses quota accounts", async () => { registerSendingAdapter("quota", { async send() { throw Object.assign(new Error("rate limited"), { code: "quota_exceeded", retryable: true }); } }); const { db, campaign } = fixture(); execute(db, "UPDATE sending_accounts SET provider = 'quota' WHERE id = 'a1'"); const result = await processQueuedSend(db, job(campaign.id)); expect(result.status).toBe("retryable_failure"); expect(db.query("SELECT status FROM sending_accounts WHERE id = 'a1'").get()).toEqual({ status: "paused" }); });
