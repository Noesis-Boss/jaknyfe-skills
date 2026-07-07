import { Hono } from "hono";
import { serveStatic } from "@hono/node-server/serve-static";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import {
  getOrCreateUser,
  createSession,
  getUserBySession,
  deleteSession,
  createMagicToken,
  consumeMagicToken,
  getProfile,
  upsertProfile,
  getEntries,
  upsertEntry,
} from "./db";
import { sendMagicLink, resendConfigured } from "./email";
import { googleAuthUrl, exchangeGoogleCode } from "./auth";

const app = new Hono();
const COOKIE = "wl_session";
const DIST = join(import.meta.dir, "dist");

function sessionCookie(token: string, maxAge = 60 * 60 * 24 * 30) {
  return `${COOKIE}=${token}; HttpOnly; Path=/; SameSite=Lax; Max-Age=${maxAge}`;
}
function clearCookie() {
  return `${COOKIE}=; HttpOnly; Path=/; SameSite=Lax; Max-Age=0`;
}

function baseUrl(req: Request) {
  return process.env.PUBLIC_BASE || new URL(req.url).origin;
}

// ---- Auth ----
app.get("/api/auth/google", (c) => {
  const url = googleAuthUrl(baseUrl(c.req.raw));
  return c.redirect(url);
});

app.get("/api/auth/google/callback", async (c) => {
  const code = c.req.query("code");
  if (!code) return c.redirect("/?error=google");
  try {
    const email = await exchangeGoogleCode(code, baseUrl(c.req.raw));
    const userId = getOrCreateUser(email, null, "google");
    const { token } = createSession(userId);
    return c.redirect("/", 302).header("Set-Cookie", sessionCookie(token));
  } catch {
    return c.redirect("/?error=google");
  }
});

app.post("/api/auth/magic", async (c) => {
  const { email } = await c.req.json<{ email: string }>();
  if (!email || !email.includes("@")) return c.json({ error: "invalid email" }, 400);
  if (!resendConfigured()) return c.json({ error: "email_not_configured" }, 503);
  const token = createMagicToken(email.toLowerCase().trim());
  const link = `${origin(c.req.raw)}/api/auth/magic/verify?token=${token}`;
  try {
    await sendMagicLink(email, link);
    return c.json({ ok: true });
  } catch (e: any) {
    return c.json({ error: e.message || "send_failed" }, 500);
  }
});

app.get("/api/auth/magic/verify", async (c) => {
  const token = c.req.query("token");
  if (!token) return c.redirect("/?error=magic");
  const email = consumeMagicToken(token);
  if (!email) return c.redirect("/?error=magic_expired");
  const userId = getOrCreateUser(email, null, "magic");
  const { token: sess } = createSession(userId);
  return c.redirect("/", 302).header("Set-Cookie", sessionCookie(sess));
});

app.post("/api/auth/logout", (c) => {
  const token = c.req.header("Cookie")?.match(/wl_session=([^;]+)/)?.[1];
  if (token) deleteSession(token);
  return c.json({ ok: true }).header("Set-Cookie", clearCookie());
});

app.get("/api/me", (c) => {
  const token = c.req.header("Cookie")?.match(/wl_session=([^;]+)/)?.[1];
  const user = token ? getUserBySession(token) : undefined;
  if (!user) return c.json({ user: null }, 401);
  const profile = getProfile(user.id);
  return c.json({ user, profile });
});

// ---- Profile ----
app.post("/api/profile", async (c) => {
  const token = c.req.header("Cookie")?.match(/wl_session=([^;]+)/)?.[1];
  const user = token ? getUserBySession(token) : undefined;
  if (!user) return c.json({ error: "unauthorized" }, 401);
  const { start_weight, target_weight, start_date } = await c.req.json();
  upsertProfile(user.id, start_weight ?? null, target_weight ?? null, start_date ?? null);
  return c.json({ ok: true });
});

// ---- Tracker ----
app.get("/api/tracker", (c) => {
  const token = c.req.header("Cookie")?.match(/wl_session=([^;]+)/)?.[1];
  const user = token ? getUserBySession(token) : undefined;
  if (!user) return c.json({ error: "unauthorized" }, 401);
  return c.json({ entries: getEntries(user.id) });
});

app.post("/api/tracker", async (c) => {
  const token = c.req.header("Cookie")?.match(/wl_session=([^;]+)/)?.[1];
  const user = token ? getUserBySession(token) : undefined;
  if (!user) return c.json({ error: "unauthorized" }, 401);
  const { date, weight, steps, calories_in, exercise_burn } = await c.req.json();
  if (!date) return c.json({ error: "date required" }, 400);
  upsertEntry(user.id, date, weight ?? null, steps ?? null, calories_in ?? null, exercise_burn ?? 0);
  return c.json({ ok: true });
});

// ---- Static (built React app) ----
app.use("/*", serveStatic({ root: DIST }));
app.get("*", (c) => {
  try {
    return c.html(readFileSync(join(DIST, "index.html"), "utf8"));
  } catch {
    return c.text("Build not found. Run `bun run build`.", 500);
  }
});

const port = Number(process.env.PORT) || 3000;
console.log(`Weight-loss tracker listening on :${port}`);
export default {
  port,
  fetch: app.fetch,
};
