import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { registerUser, verifyPassword } from "../auth/password";
import { createSession, revokeSession } from "../auth/session";
import { requireTenant } from "../auth/middleware";
import { requireTenantPostgres } from "../auth/middleware";
import { createSessionPostgres, firstMembershipPostgres, registerUserPostgres, revokeSessionPostgres, verifyPasswordPostgres } from "../auth/postgres";
import type { AppEnv } from "../config";

const loginFailures = new Map<string, { count: number; resetAt: number }>();
const registrations = new Map<string, { count: number; resetAt: number }>();
const WINDOW_MS = 15 * 60 * 1000;
const MAX_LOGIN_FAILURES = 5;
const MAX_REGISTRATIONS = 10;

function limited(bucket: Map<string, { count: number; resetAt: number }>, key: string, max: number): boolean { const now = Date.now(); const current = bucket.get(key); if (!current || current.resetAt <= now) { bucket.set(key, { count: 1, resetAt: now + WINDOW_MS }); return false; } if (current.count >= max) return true; current.count += 1; return false; }
function cookie(token: string, expiresAt: string, appEnv: AppEnv): string { const secure = appEnv === "production" ? "; Secure" : ""; return `saas_mailer_session=${encodeURIComponent(token)}; Path=/; HttpOnly; SameSite=Lax${secure}; Expires=${new Date(expiresAt).toUTCString()}`; }

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }

export function createAuthRoutes(database: Database | PostgresDatabase, appEnv: AppEnv = "development"): Hono {
  const routes = new Hono();
  routes.post("/api/auth/register", async c => { try { const body = await c.req.json(); if (!body || typeof body.email !== "string" || typeof body.password !== "string" || typeof body.organization_name !== "string") return c.json({ error: "Invalid registration" }, 400); const key = c.req.header("x-forwarded-for") || "unknown"; if (appEnv === "production" && limited(registrations, key, MAX_REGISTRATIONS)) return c.json({ error: "Registration temporarily unavailable" }, 429); const user = isPostgres(database) ? await registerUserPostgres(database, body.email, body.password, body.organization_name) : await registerUser(database, body.email, body.password, body.organization_name); const session = isPostgres(database) ? await createSessionPostgres(database, user.id, user.organizationId!) : await createSession(database, user.id, user.organizationId!); return c.json({ user: { id: user.id, email: user.email }, organization_id: session.organizationId }, 201, { "Set-Cookie": cookie(session.token, session.expiresAt, appEnv) }); } catch { return c.json({ error: "Unable to register" }, 400); } });
  routes.post("/api/auth/login", async c => { try { const body = await c.req.json(); if (!body || typeof body.email !== "string" || typeof body.password !== "string") return c.json({ error: "Invalid login" }, 400); const key = `${c.req.header("x-forwarded-for") || "unknown"}:${body.email.trim().toLowerCase()}`; if (appEnv === "production" && loginFailures.get(key)?.count >= MAX_LOGIN_FAILURES && loginFailures.get(key)!.resetAt > Date.now()) return c.json({ error: "Too many login attempts" }, 429); const user = isPostgres(database) ? await verifyPasswordPostgres(database, body.email, body.password) : await verifyPassword(database, body.email, body.password); if (!user) { if (appEnv === "production") limited(loginFailures, key, MAX_LOGIN_FAILURES); return c.json({ error: "Invalid email or password" }, 401); } loginFailures.delete(key); const membership = isPostgres(database) ? await firstMembershipPostgres(database, user.id) : database.query<{ organization_id: string }>("SELECT organization_id FROM organization_members WHERE user_id = ? ORDER BY created_at LIMIT 1").get(user.id); if (!membership) return c.json({ error: "Organization access denied" }, 403); const session = isPostgres(database) ? await createSessionPostgres(database, user.id, membership.organization_id) : await createSession(database, user.id, membership.organization_id); return c.json({ user, organization_id: session.organizationId }, 200, { "Set-Cookie": cookie(session.token, session.expiresAt, appEnv) }); } catch { return c.json({ error: "Unable to log in" }, 400); } });
  routes.post("/api/auth/logout", async c => { const token = c.req.raw.headers.get("cookie")?.match(/(?:^|;\s*)saas_mailer_session=([^;]+)/)?.[1]; if (token) { if (isPostgres(database)) await revokeSessionPostgres(database, decodeURIComponent(token)); else revokeSession(database, decodeURIComponent(token)); } const secure = appEnv === "production" ? "; Secure" : ""; return c.json({ ok: true }, 200, { "Set-Cookie": `saas_mailer_session=; Path=/; HttpOnly; Max-Age=0; SameSite=Lax${secure}` }); });
  routes.get("/api/auth/me", async c => { try { const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw); return c.json(tenant); } catch { return c.json({ error: "Authentication required" }, 401); } });
  return routes;
}
