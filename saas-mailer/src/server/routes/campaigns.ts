import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { getOrganizationId } from "../tenancy";
import { approveCampaign, createCampaign, enrollContacts } from "../campaigns/service";
export function createCampaignRoutes(database: Database): Hono {
  const routes = new Hono();
  routes.post("/api/campaigns", async c => { try { return c.json(createCampaign(database, getOrganizationId(c.req.raw), await c.req.json()), 201); } catch { return c.json({ error: "Unable to create campaign" }, 400); } });
  routes.post("/api/campaigns/:id/approve", async c => { try { const org = getOrganizationId(c.req.raw); const body = await c.req.json().catch(() => ({})); return c.json(approveCampaign(database, c.req.param("id"), org, body.approved_by || "system")); } catch { return c.json({ error: "Unable to approve campaign" }, 400); } });
  routes.post("/api/campaigns/:id/enroll", async c => { try { return c.json({ enrolled: enrollContacts(database, c.req.param("id"), getOrganizationId(c.req.raw), (await c.req.json()).contact_ids || []) }); } catch { return c.json({ error: "Unable to enroll contacts" }, 400); } });
  return routes;
}
