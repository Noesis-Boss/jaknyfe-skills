import { Hono } from "hono";
import { serveStatic } from "hono/bun";

const ZO_TOKEN = process.env.ZO_CLIENT_IDENTITY_TOKEN ?? "";
const MODEL = "byok:2e03a024-1bd1-4819-b7de-06dbb577e664";
const SYSTEM =
  "You are Concierge (alias Zorro), a friendly trip assistant for 26 travelers flying Phoenix to Houston to Cancun. Keep replies short, warm, practical.";
const MENTION_TRIGGER = "@Zorro";

type Channel = { platform: string; channelId: string; channelName: string; joinedAt: string };

const channels: Channel[] = [];
const channelsFile = "./channels.json";

try {
  const fs = await import("node:fs");
  if (fs.existsSync(channelsFile)) {
    channels.push(...JSON.parse(fs.readFileSync(channelsFile, "utf8")));
  }
} catch {}

function persist() {
  const fs = require("node:fs");
  fs.writeFileSync(channelsFile, JSON.stringify(channels, null, 2));
}

// Shared brain call — every channel routes questions through Zorro here.
async function askZo(question: string): Promise<string> {
  if (!question.trim()) return "Say something helpful.";
  try {
    const res = await fetch("https://api.zo.computer/zo/ask", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${ZO_TOKEN}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        input: `${SYSTEM} Question: ${question}`,
        model_name: MODEL,
      }),
    });
    const data = await res.json();
    return data.output ?? "No answer.";
  } catch {
    return "Concierge is offline right now.";
  }
}

const app = new Hono();

app.use("/*", serveStatic({ root: "./public" }));

// Web UI ask
app.get("/api/ask", async (c) => {
  const q = c.req.query("q") ?? "";
  if (!q.trim()) return c.json({ reply: "" }, 400);
  return c.json({ reply: await askZo(q) });
});

// Channel webhook: bot answers only when text contains "@Zorro"
app.post("/api/incoming", async (c) => {
  let body: any = {};
  try {
    body = await c.req.json();
  } catch {}
  const text: string = body.text ?? body.message?.text ?? body.message ?? "";
  if (!text.includes(MENTION_TRIGGER)) {
    return c.json({ handled: false, reason: "no mention" });
  }
  const q = text.split(MENTION_TRIGGER).join("").trim();
  const reply = await askZo(q);
  const tgToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = body.chat?.id ?? body.message?.chat?.id;
  if (tgToken && chatId) {
    try {
      await fetch(`https://api.telegram.org/bot${tgToken}/sendMessage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text: reply.slice(0, 4096) }),
      });
    } catch {}
  }
  return c.json({ handled: true, reply });
});

// Register a channel the bot has been invited to.
app.post("/api/channels/join", async (c) => {
  const { platform, channelId, channelName } = await c.req.json();
  if (!platform || !channelId) return c.json({ reply: "Missing platform or channelId." }, 400);

  const existing = channels.find((ch) => ch.platform === platform && ch.channelId === channelId);
  if (existing) {
    return c.json({ reply: `Concierge is already in that ${platform} channel.` });
  }

  channels.push({
    platform,
    channelId,
    channelName: channelName ?? channelId,
    joinedAt: new Date().toISOString(),
  });
  persist();

  return c.json({
    reply: `✅ Concierge (Zorro) joined the ${platform} channel "${channelName ?? channelId}". The other travelers can now @Zorro it with questions.`,
  });
});

app.get("/api/channels", (c) => c.json({ channels }));

// ---------- WhatsApp (Meta Cloud API) ----------
// GET: Meta webhook verification handshake
app.get("/api/whatsapp", (c) => {
  const mode = c.req.query("hub.mode");
  const token = c.req.query("hub.verify_token");
  const challenge = c.req.query("hub.challenge");
  if (mode === "subscribe" && token === process.env.WA_VERIFY_TOKEN) {
    return c.text(challenge ?? "");
  }
  return c.text("Forbidden", 403);
});

// POST: inbound WhatsApp message -> answer via Zorro -> reply over WhatsApp
app.post("/api/whatsapp", async (c) => {
  let body: any = {};
  try {
    body = await c.req.json();
  } catch {}
  try {
    const messages: any[] = body?.entry?.[0]?.changes?.[0]?.value?.messages ?? [];
    const phoneNumberId = process.env.WA_PHONE_NUMBER_ID;
    const token = process.env.WA_ACCESS_TOKEN;
    for (const msg of messages) {
      if (msg.type !== "text") continue;
      const from: string = msg.from;
      let text = (msg.text?.body ?? "").replace(/@Zorro/gi, "").trim();
      const answer = await askZo(text);
      if (phoneNumberId && token) {
        await fetch(`https://graph.facebook.com/v21.0/${phoneNumberId}/messages`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            messaging_product: "whatsapp",
            to: from,
            type: "text",
            text: { body: answer.slice(0, 4096) },
          }),
        });
      }
    }
  } catch {}
  return c.text("OK");
});

const port = Number(process.env.PORT ?? 3000);
export default { port, fetch: app.fetch };
