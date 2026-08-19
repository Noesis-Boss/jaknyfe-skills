import { Hono } from "hono";

const app = new Hono();

app.get("/api/health", (c) => c.json({ ok: true }));

app.get("/", (c) =>
  c.html(`<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>SaaS-Mailer</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/client/main.tsx"></script>
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
