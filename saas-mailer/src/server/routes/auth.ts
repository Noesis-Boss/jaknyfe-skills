import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import { registerUser, verifyPassword } from "../auth/password";
import { createSession, revokeSession } from "../auth/session";
import { requireTenant } from "../auth/middleware";

function cookie(token: string, expiresAt: string): string { const secure = process.env.APP_ENV === "production" ? "; Secure" : ""; return `saas_mailer_session=${encodeURIComponent(token)}; Path=/; HttpOnly; SameSite=Lax${secure}; Expires=${new Date(expiresAt).toUTCString()}`; }

export function createAuthRoutes(database: Database): Hono {
  const routes = new Hono();
  routes.post("/api/auth/register", async c => { try { const body = await c.req.json(); if (!body || typeof body.email !== "string" || typeof body.password !== "string" || typeof body.organization_name !== "string") return c.json({ error: "Invalid registration" }, 400); const user = await registerUser(database, body.email, body.password, body.organization_name); const session = await createSession(database, user.id, user.organizationId!); return c.json({ user: { id: user.id, email: user.email }, organization_id: session.organizationId }, 201, { "Set-Cookie": cookie(session.token, session.expiresAt) }); } catch { return c.json({ error: "Unable to register" }, 400); } });
  routes.post("/api/auth/login", async c => { try { const body = await c.req.json(); if (!body || typeof body.email !== "string" || typeof body.password !== "string") return c.json({ error: "Invalid login" }, 400); const user = await verifyPassword(database, body.email, body.password); if (!user) return c.json({ error: "Invalid email or password" }, 401); const membership = database.query<{ organization_id: string }>("SELECT organization_id FROM organization_members WHERE user_id = ? ORDER BY created_at LIMIT 1").get(user.id); if (!membership) return c.json({ error: "Organization access denied" }, 403); const session = await createSession(database, user.id, membership.organization_id); return c.json({ user, organization_id: session.organizationId }, 200, { "Set-Cookie": cookie(session.token, session.expiresAt) }); } catch { return c.json({ error: "Unable to log in" }, 400); } });
  routes.post("/api/auth/logout", c => { const token = c.req.raw.headers.get("cookie")?.match(/(?:^|;\s*)saas_mailer_session=([^;]+)/)?.[1]; if (token) revokeSession(database, decodeURIComponent(token)); return c.json({ ok: true }, 200, { "Set-Cookie": "saas_mailer_session=; Path=/; HttpOnly; Max-Age=0; SameSite=Lax" }); });
  routes.get("/api/auth/me", c => { try { const tenant = requireTenant(database, c.req.raw); return c.json(tenant); } catch { return c.json({ error: "Authentication required" }, 401); } });
  return routes;
}
