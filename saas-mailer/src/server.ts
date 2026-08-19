import { Hono } from "hono";
import { migrate, openDatabase } from "./server/db";
import { createContactsRoutes } from "./server/routes/contacts";
import { createSendingAccountRoutes } from "./server/routes/sending-accounts";
import { createCampaignRoutes } from "./server/routes/campaigns";

const app = new Hono();
export const database = openDatabase();
migrate(database);

const clientScript = `
const root = document.getElementById("root");
root.innerHTML =
  '<main class="dashboard-shell">' +
    '<header class="topbar"><div><p class="eyebrow">SaaS-Mailer</p><h1>Outbound workspace</h1></div><span class="status-pill">Ready</span></header>' +
    '<section class="welcome-card"><p class="eyebrow">Dashboard</p><h2>Build your first campaign.</h2><p>Import contacts, create a sequence, and review every send from one workspace.</p><button type="button">Import contacts</button></section>' +
  '</main>';
`;

app.get("/api/health", (c) => c.json({ ok: true }));
app.route("/", createContactsRoutes(database));
app.route("/", createSendingAccountRoutes(database));
app.route("/", createCampaignRoutes(database));

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
    <link rel="stylesheet" href="/src/client/styles.css" />
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/client/main.js"></script>
  </body>
</html>`),
);

export default app;

if (import.meta.main) {
  Bun.serve({
    port: Number(process.env.PORT || 3000),
    fetch: app.fetch,
  });
}
