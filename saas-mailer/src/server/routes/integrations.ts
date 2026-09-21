import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { resendAdapter } from "../sending/resend-adapter";

function authorized(request: Request): boolean {
  const configured = process.env.FAMILY_CHORE_PLANNER_MAILER_TOKEN?.trim();
  const supplied = request.headers.get("authorization")?.replace(/^Bearer\s+/i, "").trim();
  return Boolean(configured && supplied && supplied === configured);
}

export function createIntegrationRoutes(_database: Database | PostgresDatabase): Hono {
  const routes = new Hono();
  routes.post("/api/integrations/family-chore-planner/invitations", async c => {
    if (!authorized(c.req.raw)) return c.json({ error: "Unauthorized" }, 401);
    const body = await c.req.json().catch(() => null) as { to?: string; inviteUrl?: string; role?: string } | null;
    const to = body?.to?.trim().toLowerCase();
    const inviteUrl = body?.inviteUrl?.trim();
    const role = body?.role === "Parent" ? "Parent" : "Member";
    if (!to || !inviteUrl || !/^https?:\/\//.test(inviteUrl)) return c.json({ error: "Invalid invitation" }, 400);
    try {
      const from = process.env.FAMILY_CHORE_PLANNER_FROM || "Kinfolk <mailer@noesisgroup.com>";
      const result = await resendAdapter(process.env.RESEND_API_KEY || "").send({
        from,
        to,
        subject: "You’re invited to join a household on Kinfolk",
        body: `<p>You’ve been invited to join a household on Kinfolk as a ${role}.</p><p><a href="${inviteUrl}">Open your household invitation</a></p><p>This invitation expires in 7 days.</p>`,
      });
      return c.json({ ok: true, providerMessageId: result.providerMessageId });
    } catch (error) {
      console.error("Family Chore Planner invitation delivery failed", error);
      return c.json({ error: "Invitation delivery failed" }, 502);
    }
  });
  return routes;
}
