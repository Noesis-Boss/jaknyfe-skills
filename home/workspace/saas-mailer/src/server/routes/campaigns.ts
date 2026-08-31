import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant } from "../auth/middleware";
import { requireTenantPostgres } from "../auth/middleware";
import { approveCampaign, approveCampaignPostgres, createCampaign, createCampaignPostgres, enrollContacts, enrollContactsPostgres, listCampaigns, listCampaignsPostgres } from "../campaigns/service";
import { loadQueueEligibility, loadQueueEligibilityPostgres } from "../campaigns/eligibility";
function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }
export function createCampaignRoutes(database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.post("/api/campaigns", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const input = await c.req.json(); return c.json(isPostgres(database) ? await createCampaignPostgres(database, tenant.organizationId, input) : createCampaign(database, tenant.organizationId, input), 201); } catch { return c.json({ error: "Unable to create campaign" }, 400); } });
  routes.post("/api/campaigns/:id/approve", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); return c.json(isPostgres(database) ? await approveCampaignPostgres(database, c.req.param("id"), tenant.organizationId) : approveCampaign(database, c.req.param("id"), tenant.organizationId)); } catch { return c.json({ error: "Unable to approve campaign" }, 400); } });
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
