import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { verifyTrackingToken, verifyUnsubscribeToken, recordPublicEvent, resolveMessageRecipient, resolveTenantBrand, processUnsubscribe } from "../tracking/tokens";

const transparentPixel = Uint8Array.from([71,73,56,57,97,1,0,1,0,128,0,0,0,0,0,255,255,255,33,249,4,1,0,0,0,0,44,0,0,0,0,1,0,1,0,0,2,2,68,1,0,59]);
function pg(db: Database | PostgresDatabase): db is PostgresDatabase { return "sql" in db; }
export function createAnalyticsRoutes(database: Database | PostgresDatabase) {
  const routes = new Hono();
  routes.get("/api/campaigns/:id/analytics", async c => {
    try {
      const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const id = c.req.param("id");
      const rows = pg(database) ? await database.query<{ type: string; count: number }>("SELECT e.type, count(*)::int AS count FROM events e JOIN messages m ON m.organization_id=e.organization_id AND m.id=e.message_id WHERE e.organization_id=$1 AND m.campaign_id=$2 GROUP BY e.type ORDER BY e.type", [tenant.organizationId, id]) : database.query<{ type: string; count: number }>("SELECT e.type, count(*) AS count FROM events e JOIN messages m ON m.organization_id=e.organization_id AND m.id=e.message_id WHERE e.organization_id=? AND m.campaign_id=? GROUP BY e.type ORDER BY e.type").all(tenant.organizationId, id);
      return c.json({ campaign_id: id, analytics: Object.fromEntries(rows.map(row => [row.type, Number(row.count)])) });
    } catch { return c.json({ error: "Unable to load campaign analytics" }, 400); }
  });
  routes.get("/api/tracking/open/:messageId", async c => {
    try {
      const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const id = c.req.param("messageId");
      if (pg(database)) await database.query("INSERT INTO events (id,organization_id,message_id,type,payload) SELECT gen_random_uuid()::text,$1,id,'opened','{}' FROM messages WHERE organization_id=$1 AND id=$2", [tenant.organizationId, id]);
      else database.query("INSERT INTO events (id,organization_id,message_id,type,payload) SELECT lower(hex(randomblob(16))),?,id,'opened','{}' FROM messages WHERE organization_id=? AND id=?").run(tenant.organizationId, tenant.organizationId, id);
    } catch {}
    return new Response(transparentPixel, { headers: { "Content-Type": "image/gif", "Cache-Control": "no-store" } });
  });
  routes.get("/api/tracking/click/:messageId", async c => {
    try {
      const tenant = pg(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); const id = c.req.param("messageId"); const target = c.req.query("url");
      if (pg(database)) await database.query("INSERT INTO events (id,organization_id,message_id,type,payload) SELECT gen_random_uuid()::text,$1,id,'clicked',$3 FROM messages WHERE organization_id=$1 AND id=$2", [tenant.organizationId, id, JSON.stringify({ url: target || "" })]);
      else database.query("INSERT INTO events (id,organization_id,message_id,type,payload) SELECT lower(hex(randomblob(16))),?,id,'clicked',? FROM messages WHERE organization_id=? AND id=?").run(tenant.organizationId, JSON.stringify({ url: target || "" }), tenant.organizationId, id);
      return c.redirect(target || "/");
    } catch { return c.redirect("/"); }
  });
  routes.get("/api/t/o/:token", async c => {
    try { const id = verifyTrackingToken(c.req.param("token")); if (id) await recordPublicEvent(database, id, "opened"); } catch {}
    return new Response(transparentPixel, { headers: { "Content-Type": "image/gif", "Cache-Control": "no-store" } });
  });
  routes.get("/api/t/c/:token", async c => {
    const target = c.req.query("url") || "/";
    try { const id = verifyTrackingToken(c.req.param("token")); if (id) await recordPublicEvent(database, id, "clicked", { url: target }); } catch {}
    return c.redirect(target);
  });
  routes.get("/api/t/u/:token", async c => {
    const brand = await (async () => { try { const id = verifyUnsubscribeToken(c.req.param("token")); if (!id) return null; const recipient = await resolveMessageRecipient(database, id); return recipient ? resolveTenantBrand(database, recipient.organizationId) : null; } catch { return null; } })();
    const who = brand ? ` from ${brand}` : "";
    const confirmed = `<html><body style="font-family:sans-serif;text-align:center;padding:48px"><h1 style="font-size:20px">You're unsubscribed${who}</h1><p style="color:#666">You will not receive further emails from this sender.</p></body></html>`;
    await processUnsubscribe(database, c.req.param("token"));
    return c.html(confirmed);
  });
  routes.post("/api/t/u/:token", async c => {
    await processUnsubscribe(database, c.req.param("token"));
    return c.html(`<html><body style="font-family:sans-serif;text-align:center;padding:48px"><h1 style="font-size:20px">Unsubscribed</h1><p style="color:#666">You will not receive further emails from this sender.</p></body></html>`);
  });
    return routes;
}
