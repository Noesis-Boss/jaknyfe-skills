import { Hono } from "hono";
import { loadConfig } from "./server/config";
import { migrate, openDatabase } from "./server/db";
import { openProductionDatabase } from "./server/postgres";
import { createContactsRoutes } from "./server/routes/contacts";
import { createSendingAccountRoutes } from "./server/routes/sending-accounts";
import { createCampaignRoutes } from "./server/routes/campaigns";
import { createEventRoutes } from "./server/routes/events";
import { createAuthRoutes } from "./server/routes/auth";
import { createProviderCallbackRoutes } from "./server/routes/provider-callbacks";
import { createContactListRoutes } from "./server/routes/contact-lists";
import { createPreferenceRoutes } from "./server/routes/preferences";
import { createAnalyticsRoutes } from "./server/routes/analytics";
import { requireTenant, requireTenantPostgres } from "./server/auth/middleware";

const app = new Hono();
export const config = loadConfig();
export const database = config.database === "postgres" ? await openProductionDatabase(config.databaseUrl) : openDatabase();
if (config.database === "sqlite") {
  migrate(database);
  database.query("INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)").run("demo-org", "Demo workspace");
}

const clientScript = await Bun.build({ entrypoints: [new URL("./client/main.tsx", import.meta.url).pathname], target: "browser", minify: false }).then((result) => result.outputs[0].text());

app.get("/api/health", (c) => c.json({ ok: true }));
app.get("/api/worker/health", async (c) => {
  try {
    const tenant = config.database === "postgres" ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
    const rows = config.database === "postgres"
      ? await (database as import("./server/postgres").PostgresDatabase).query<{ status: string; due: number }>("SELECT status, COUNT(*)::int AS due FROM messages WHERE organization_id = $1 GROUP BY status", [tenant.organizationId])
      : (database as import("bun:sqlite").Database).query<{ status: string; due: number }, [string]>("SELECT status, COUNT(*) AS due FROM messages WHERE organization_id = ? GROUP BY status").all(tenant.organizationId);
    const counts = Object.fromEntries(rows.map(row => [row.status, Number(row.due)]));
    return c.json({ ok: true, state: counts.processing ? "sending" : counts.queued ? "ready" : "idle", counts });
  } catch (error) {
    return c.json({ ok: false, state: "unknown", error: error instanceof Error ? error.message : "unavailable" }, 401);
  }
});
app.route("/", createAuthRoutes(database, config.appEnv));
app.route("/", createProviderCallbackRoutes(database, config));
app.route("/", createContactsRoutes(database));
app.route("/", createSendingAccountRoutes(database));
app.route("/", createCampaignRoutes(database));
app.route("/", createEventRoutes(database));
app.route("/", createContactListRoutes(database));
app.route("/", createPreferenceRoutes(database));
app.route("/", createAnalyticsRoutes(database));

app.get("/src/client/main.js", (c) => c.text(clientScript, 200, { "Content-Type": "application/javascript; charset=UTF-8" }));

app.get("/src/client/styles.css", async (c) =>
  c.text(await Bun.file(new URL("./client/styles.css", import.meta.url)).text(), 200, { "Content-Type": "text/css; charset=UTF-8" }),
);

app.get("/", (c) =>
  c.html(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SaaS-Mailer</title>
    <link rel="stylesheet" href="/src/client/styles.css?v=20260902-2" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/client/main.js?v=20260902-3"></script>
  </body>
</html>`),
);

export default app;
