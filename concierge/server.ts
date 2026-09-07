import { Hono } from "hono";
import { serveStatic } from "hono/bun";

const MENTION_TRIGGER = "@Zorro";

const app = new Hono();
app.use("/*", serveStatic({ root: "./public" }));

// Web UI ask
app.get("/api/ask", async (c) => {
  const q = c.req.query("q") ?? "";
  if (!q.trim()) return c.json({ reply: "" }, 400);
  try {
    const res = await fetch("https://api.zo.computer/zo/ask", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.ZO_CLIENT_IDENTITY_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: `You are Concierge (alias Zorro), a friendly trip assistant for 26 travelers flying Phoenix to Houston to Cancun. Keep replies short, warm, practical. Question: ${q}`,
        model_name: "byok:2e03a024-1bd1-4819-b7de-06dbb577e664",
      }),
    });
    const data = await res.json();
    return c.json({ reply: data.output ?? "No answer." });
  } catch {
    return c.json({ reply: "Concierge is offline right now." }, 500);
  }
});

// Channel webhook: bot answers only when text contains "@Zorro"
app.post("/api/incoming", async (c) => {
  let body: any = {};
  try { body = await c.req.json(); } catch {}
  const text: string = body.text ?? body.message ?? "";
  if (!text.includes(MENTION_TRIGGER)) {
    return c.json({ handled: false, reason: "no mention" });
  }
  const q = text.split(MENTION_TRIGGER).join("").trim() || "Say something helpful.";
  try {
    const res = await fetch("https://api.zo.computer/zo/ask", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.ZO_CLIENT_IDENTITY_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: `You are Concierge (alias Zorro), a friendly trip assistant for 26 travelers flying Phoenix to Houston to Cancun. Keep replies short, warm, practical. Question: ${q}`,
        model_name: "byok:2e03a024-1bd1-4819-b7de-06dbb577e664",
      }),
    });
    const data = await res.json();
    return c.json({ handled: true, reply: data.output ?? "No answer." });
  } catch {
    return c.json({ handled: true, reply: "Concierge is offline right now." });
  }
});

const port = Number(process.env.PORT ?? 3000);
export default { port, fetch: app.fetch };
