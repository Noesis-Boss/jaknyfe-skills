import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant } from "../auth/middleware";
import { requireTenantPostgres } from "../auth/middleware";
import { approveCampaign, approveCampaignPostgres, createCampaign, createCampaignPostgres, enrollContacts, enrollContactsPostgres, listCampaigns, listCampaignsPostgres } from "../campaigns/service";
import { loadQueueEligibility, loadQueueEligibilityPostgres } from "../campaigns/eligibility";
import { randomUUID } from "node:crypto";
function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }
export function createCampaignRoutes(database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.post("/api/campaigns", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const input = await c.req.json(); return c.json(isPostgres(database) ? await createCampaignPostgres(database, tenant.organizationId, input) : createCampaign(database, tenant.organizationId, input), 201); } catch { return c.json({ error: "Unable to create campaign" }, 400); } });
  routes.post("/api/campaigns/:id/approve", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); return c.json(isPostgres(database) ? await approveCampaignPostgres(database, c.req.param("id"), tenant.organizationId) : approveCampaign(database, c.req.param("id"), tenant.organizationId)); } catch { return c.json({ error: "Unable to approve campaign" }, 400); } });
  routes.post("/api/campaigns/:id/schedule", async c => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const id = c.req.param("id"); const input = await c.req.json().catch(() => ({})); const scheduledAt = String(input.scheduled_at || new Date().toISOString());
      const when = new Date(scheduledAt); if (Number.isNaN(when.getTime())) return c.json({ error: "Invalid scheduled time" }, 400);
      if (isPostgres(database)) {
        const campaign = (await database.query<any>("SELECT c.*, s.subject, s.body FROM campaigns c JOIN campaign_steps s ON s.organization_id=c.organization_id AND s.campaign_id=c.id AND s.step_order=0 WHERE c.organization_id=$1 AND c.id=$2", [tenant.organizationId, id]))[0];
        if (!campaign || campaign.status !== "approved") return c.json({ error: "Campaign must be approved before scheduling" }, 400);
        const recipients = await database.query<any>("SELECT cc.contact_id, c.email FROM campaign_contacts cc JOIN contacts c ON c.organization_id=cc.organization_id AND c.id=cc.contact_id WHERE cc.organization_id=$1 AND cc.campaign_id=$2 AND cc.status='pending'", [tenant.organizationId, id]);
        let queued = 0; for (const recipient of recipients) { const result = await database.execute("INSERT INTO messages (id,organization_id,campaign_id,contact_id,sending_account_id,status,idempotency_key,next_attempt_at,subject,body) VALUES ($1,$2,$3,$4,$5,'queued',$6,$7,$8,$9) ON CONFLICT (idempotency_key) DO NOTHING", [randomUUID(), tenant.organizationId, id, recipient.contact_id, campaign.sending_account_id, `newsletter:${id}:${recipient.contact_id}`, when, campaign.subject, campaign.body]); queued += result; }
        await database.query("UPDATE campaigns SET scheduled_at=$1, status='scheduled' WHERE organization_id=$2 AND id=$3", [when, tenant.organizationId, id]); return c.json({ scheduled_at: when.toISOString(), queued });
      }
      const campaign = database.query<any>("SELECT c.*, s.subject, s.body FROM campaigns c JOIN campaign_steps s ON s.organization_id=c.organization_id AND s.campaign_id=c.id AND s.step_order=0 WHERE c.organization_id=? AND c.id=?").get(tenant.organizationId, id);
      if (!campaign || campaign.status !== "approved") return c.json({ error: "Campaign must be approved before scheduling" }, 400);
      const recipients = database.query<any>("SELECT cc.contact_id FROM campaign_contacts cc WHERE cc.organization_id=? AND cc.campaign_id=? AND cc.status='pending'").all(tenant.organizationId, id); const insert = database.query("INSERT OR IGNORE INTO messages (id,organization_id,campaign_id,contact_id,sending_account_id,status,idempotency_key,next_attempt_at,subject,body) VALUES (?,?,?,?,?,'queued',?,?,?,?)"); let queued = 0;
      for (const recipient of recipients) queued += insert.run(randomUUID(), tenant.organizationId, id, recipient.contact_id, campaign.sending_account_id, `newsletter:${id}:${recipient.contact_id}`, when.toISOString(), campaign.subject, campaign.body).changes;
      database.query("UPDATE campaigns SET scheduled_at=?, status='scheduled' WHERE organization_id=? AND id=?").run(when.toISOString(), tenant.organizationId, id); return c.json({ scheduled_at: when.toISOString(), queued });
    } catch { return c.json({ error: "Unable to schedule campaign" }, 400); }
  });
  routes.get("/api/campaigns/:id/contacts/:contactId/eligibility", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); return c.json(isPostgres(database) ? await loadQueueEligibilityPostgres(database, tenant.organizationId, c.req.param("id"), c.req.param("contactId")) : loadQueueEligibility(database, tenant.organizationId, c.req.param("id"), c.req.param("contactId"))); } catch { return c.json({ error: "Unable to evaluate campaign eligibility" }, 400); } });
  routes.post("/api/campaigns/:id/enroll", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const ids = (await c.req.json()).contact_ids || []; return c.json({ enrolled: isPostgres(database) ? await enrollContactsPostgres(database, c.req.param("id"), tenant.organizationId, ids) : enrollContacts(database, c.req.param("id"), tenant.organizationId, ids) }); } catch { return c.json({ error: "Unable to enroll contacts" }, 400); } });
  routes.get("/api/campaigns", async c => {
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const campaigns = isPostgres(database) ? await listCampaignsPostgres(database, tenant.organizationId) : listCampaigns(database, tenant.organizationId);
      return c.json({ campaigns });
    } catch { return c.json({ error: "Unable to list campaigns" }, 400); }
  });
  return routes;
}
