import { expect, test } from "bun:test";
import app from "../../src/server";
import { authFor } from "../auth-helper";
import { database } from "../../src/server";
import { execute } from "../../src/server/db";

async function post(path: string, cookie: string, body?: unknown) {
  return app.fetch(new Request(`http://localhost${path}`, { method: "POST", headers: { cookie, "content-type": "application/json" }, body: body ? JSON.stringify(body) : undefined }));
}

test("approved campaigns schedule future sends without enrolling early", async () => {
  const cookie = await authFor("sched-org");
  const contactId = "contact-sched-1";
  execute(database, "INSERT OR IGNORE INTO contacts (id, organization_id, email) VALUES (?, ?, ?)", [contactId, "sched-org", "sched@example.com"]);
  const account = await post("/api/sending-accounts", cookie, { provider: "mock", email: "sched-sender@example.com", credentials: { token: "test" } });
  expect(account.status).toBe(201);
  const accountId = (await account.json()).id;
  const created = await post("/api/campaigns", cookie, { name: "Scheduled newsletter", campaign_type: "newsletter", sending_account_id: accountId, steps: [{ subject: "Later", body: "<p>Soon</p>" }] });
  expect(created.status).toBe(201);
  const campaign = await created.json();

  const gate = await post(`/api/campaigns/${campaign.id}/schedule`, cookie);
  expect(gate.status).toBe(400);

  await post(`/api/campaigns/${campaign.id}/approve`, cookie);
  await post(`/api/campaigns/${campaign.id}/enroll`, cookie, { contact_ids: [contactId] });
  const early = await post(`/api/campaigns/${campaign.id}/schedule`, cookie, { scheduled_at: new Date(Date.now() + 3_600_000).toISOString() });
  expect(early.status).toBe(200);
  expect((await early.json()).queued).toBe(1);

  const again = await post(`/api/campaigns/${campaign.id}/schedule`, cookie, { scheduled_at: new Date(Date.now() + 3_600_000).toISOString() });
  expect(again.status).toBe(400);

  const rows = database.query<any, [string]>("SELECT status, next_attempt_at, subject, body FROM messages WHERE idempotency_key = ?").all(`newsletter:${campaign.id}:${contactId}`);
  expect(rows).toHaveLength(1);
  expect(rows[0].status).toBe("queued");
  expect(rows[0].subject).toBe("Later");
});
