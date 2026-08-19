import { Hono } from "hono";
import { migrate, openDatabase } from "./server/db";
import { createContactsRoutes } from "./server/routes/contacts";
import { createSendingAccountRoutes } from "./server/routes/sending-accounts";
import { createCampaignRoutes } from "./server/routes/campaigns";
import { createEventRoutes } from "./server/routes/events";

const app = new Hono();
export const database = openDatabase();
migrate(database);
database.query("INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)").run("demo-org", "Demo workspace");

const clientScript = await Bun.build({ entrypoints: [new URL("./client/main.tsx", import.meta.url).pathname], target: "browser", minify: false }).then((result) => result.outputs[0].text());

app.get("/api/health", (c) => c.json({ ok: true }));
app.route("/", createContactsRoutes(database));
app.route("/", createSendingAccountRoutes(database));
app.route("/", createCampaignRoutes(database));
app.route("/", createEventRoutes(database));

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
