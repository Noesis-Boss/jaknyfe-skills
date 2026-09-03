import { Hono } from "hono";
import { serveStatic } from "hono/bun";
import campaigns from "./src/data/campaigns.json";
import { verifyMessage } from "ethers";

const app = new Hono();

const campaignDataPath = "./data/campaigns.json";
const campaignFile = Bun.file(campaignDataPath);
const campaignStore = (await campaignFile.exists()
  ? await campaignFile.json()
  : [...campaigns]) as Array<Record<string, unknown>>;
const walletChallenges = new Map<string, { message: string; expiresAt: number }>();

async function saveCampaigns() {
  await Bun.write(campaignDataPath, JSON.stringify(campaignStore, null, 2) + "\n");
}

app.get("/api/campaigns", (c) => c.json(campaignStore));

app.post("/api/wallet/challenge", async (c) => {
  const body = await c.req.json<{ address?: string }>();
  const address = body.address?.trim();
  if (!address || !/^0x[a-fA-F0-9]{40}$/.test(address)) return c.json({ error: "Invalid wallet address" }, 400);
  const message = `CoinBackers wallet verification\nAddress: ${address}\nNonce: ${crypto.randomUUID()}`;
  walletChallenges.set(address.toLowerCase(), { message, expiresAt: Date.now() + 5 * 60 * 1000 });
  return c.json({ message, expiresAt: Date.now() + 5 * 60 * 1000 });
});

app.post("/api/wallet/verify", async (c) => {
  const body = await c.req.json<{ address?: string; message?: string; signature?: string }>();
  const address = body.address?.trim();
  const challenge = address ? walletChallenges.get(address.toLowerCase()) : undefined;
  if (!address || !body.message || !body.signature || !challenge || challenge.expiresAt < Date.now() || challenge.message !== body.message) {
    return c.json({ error: "Challenge expired or invalid" }, 401);
  }
  try {
    const recovered = verifyMessage(body.message, body.signature);
    if (recovered.toLowerCase() !== address.toLowerCase()) return c.json({ error: "Signature does not match wallet" }, 401);
    walletChallenges.delete(address.toLowerCase());
    return c.json({ verified: true, address: recovered });
  } catch {
    return c.json({ error: "Invalid wallet signature" }, 401);
  }
});

app.get("/api/campaigns/:id", (c) => {
  const campaign = campaignStore.find((item) => item.id === c.req.param("id"));
  return campaign ? c.json(campaign) : c.json({ error: "Campaign not found" }, 404);
});

app.post("/api/campaigns", async (c) => {
  const campaign = await c.req.json<Record<string, unknown>>();
  if (!campaign.id || !campaign.title || !campaign.description || !Number.isFinite(Number(campaign.goal))) {
    return c.json({ error: "Invalid campaign" }, 400);
  }
  campaignStore.push(campaign);
  await saveCampaigns();
  return c.json(campaign, 201);
});

app.post("/api/upload", async (c) => {
  const body = await c.req.parseBody();
  const file = body.file;
  if (!(file instanceof File) || !file.type.startsWith("image/") || file.size > 5 * 1024 * 1024) {
    return c.json({ error: "Upload a valid image under 5MB" }, 400);
  }
  const extension = file.type.split("/")[1]?.replace("jpeg", "jpg");
  if (!extension || !["png", "jpg", "webp", "gif"].includes(extension)) {
    return c.json({ error: "Unsupported image format" }, 400);
  }
  const filename = `campaign-${crypto.randomUUID()}.${extension}`;
  await Bun.write(`./dist/uploads/${filename}`, file);
  return c.json({ url: `/uploads/${filename}` }, 201);
});

app.post("/api/campaigns/:id/pledge", async (c) => {
  const campaign = campaignStore.find((item) => item.id === c.req.param("id"));
  if (!campaign) return c.json({ error: "Campaign not found" }, 404);
  const body = await c.req.json<{ amount?: number }>();
  const amount = Number(body.amount);
  if (!Number.isFinite(amount) || amount <= 0) return c.json({ error: "Invalid pledge" }, 400);
  campaign.pledged = Number(campaign.pledged || 0) + amount;
  campaign.backers = Number(campaign.backers || 0) + 1;
  await saveCampaigns();
  return c.json(campaign);
});

app.get("/api/price", (c) => {
  const prices: Record<string, number> = { eth: 3200, btc: 95000, sol: 145, usdc: 1, xrp: 2.4, ada: 0.8, doge: 0.25, matic: 0.35, link: 18, ltc: 100 };
  const symbol = c.req.query("symbol")?.toLowerCase() || "";
  const usdPrice = prices[symbol];
  return usdPrice ? c.json({ symbol, usdPrice }) : c.json({ error: "Unsupported currency" }, 400);
});

app.get("/images/coins/:file", (c) => {
  const file = c.req.param("file");
  if (!/^coin-\d{2}\.png$/.test(file)) return c.notFound();
  return new Response(Bun.file(`./dist/images/coins/${file}`));
});

app.get("/", serveStatic({ path: "./dist/index.html" }));
app.get("/favicon.ico", serveStatic({ path: "./dist/favicon.svg" }));
app.get("*", async (c) => {
  const pathname = new URL(c.req.url).pathname;
  if (pathname.includes("..")) return c.notFound();

  const asset = Bun.file(`./dist${pathname}`);
  if (await asset.exists()) return new Response(asset);
  if (pathname.includes(".")) return c.notFound();

  return new Response(Bun.file("./dist/index.html"), {
    headers: { "Content-Type": "text/html; charset=UTF-8" },
  });
});

const port = Number(process.env.PORT) || 3000;
console.log(`CoinBackers listening on port ${port}`);
export default { port, fetch: app.fetch };
