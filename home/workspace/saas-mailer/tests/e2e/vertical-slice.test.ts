import { expect, test } from "bun:test";
import { execute, migrate, openDatabase } from "../../src/server/db";
import { approveCampaign, createCampaign, enrollContacts } from "../../src/server/campaigns/service";
import { processQueuedSend } from "../../src/server/worker/process-send";
import { listEvents } from "../../src/server/events/service";

test("two organizations complete the vertical slice independently", async () => {
  const db = openDatabase(); migrate(db);
  execute(db, "INSERT INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["org-a", "Alpha", "org-b", "Beta"]);
  for (const [org, suffix] of [["org-a", "a"], ["org-b", "b"]]) {
    execute(db, "INSERT INTO contacts (id, organization_id, email) VALUES (?, ?, ?)", [`contact-${suffix}`, org, `${suffix}@example.com`]);
    execute(db, "INSERT INTO sending_accounts (id, organization_id, provider, email) VALUES (?, ?, ?, ?)", [`account-${suffix}`, org, "mock", `${suffix}-sender@example.com`]);
  }
  for (const [org, suffix] of [["org-a", "a"], ["org-b", "b"]]) {
    const campaign = createCampaign(db, org, { name: `${suffix} campaign`, sending_account_id: `account-${suffix}`, steps: [{ subject: "Hello", body: "Welcome" }] });
    approveCampaign(db, campaign.id, org); enrollContacts(db, campaign.id, org, [`contact-${suffix}`]);
    const result = await processQueuedSend(db, { organizationId: org, campaignId: campaign.id, contactId: `contact-${suffix}`, sendingAccountId: `account-${suffix}`, subject: "Hello", body: "Welcome", idempotencyKey: `send-${suffix}` });
    expect(result.status).toBe("sent"); expect(listEvents(db, org)).toHaveLength(1);
  }
  expect(db.query("SELECT COUNT(*) AS count FROM messages").get()).toEqual({ count: 2 });
});
