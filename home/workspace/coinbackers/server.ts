import { Hono } from "hono";
import { serveStatic } from "hono/bun";
import campaigns from "./src/data/campaigns.json";
import { verifyMessage } from "ethers";

const app = new Hono();

const campaignDataPath = "./data/campaigns.json";
const verifiedWalletsPath = "./data/verified-wallets.json";
const campaignFile = Bun.file(campaignDataPath);
const campaignStore = (await campaignFile.exists()
  ? await campaignFile.json()
  : [...campaigns]) as Array<Record<string, unknown>>;
const walletChallenges = new Map<string, { message: string; expiresAt: number }>();
const verifiedWalletFile = Bun.file(verifiedWalletsPath);
const verifiedWallets = new Set<string>(await (await verifiedWalletFile.exists() ? verifiedWalletFile.json() : []));
const walletSessions = new Map<string, { address: string; expiresAt: number }>();
const pledgeChallenges = new Map<string, { message: string; expiresAt: number }>();
const SESSION_TTL_MS = 24 * 60 * 60 * 1000;

async function saveVerifiedWallets() {
  await Bun.write(verifiedWalletsPath, JSON.stringify([...verifiedWallets].sort(), null, 2) + "\n");
}

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
    verifiedWallets.add(recovered.toLowerCase());
    await saveVerifiedWallets();
    const token = crypto.randomUUID();
    walletSessions.set(token, { address: recovered.toLowerCase(), expiresAt: Date.now() + SESSION_TTL_MS });
    return c.json({ verified: true, address: recovered, token, expiresAt: Date.now() + SESSION_TTL_MS });
  } catch {
    return c.json({ error: "Invalid wallet signature" }, 401);
  }
});

app.get("/api/wallet/session", (c) => {
  const token = c.req.header("authorization")?.replace(/^Bearer\s+/i, "");
  const session = token ? walletSessions.get(token) : undefined;
  if (!session || session.expiresAt <= Date.now()) {
    if (token) walletSessions.delete(token);
    return c.json({ verified: false }, 401);
  }
  return c.json({ verified: true, address: session.address, expiresAt: session.expiresAt });
});

app.post("/api/wallet/logout", (c) => {
  const token = c.req.header("authorization")?.replace(/^Bearer\s+/i, "");
  if (token) walletSessions.delete(token);
  return c.json({ loggedOut: true });
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
  const token = c.req.header("authorization")?.replace(/^Bearer\s+/i, "");
  const session = token ? walletSessions.get(token) : undefined;
  const creatorWallet = session && session.expiresAt > Date.now() ? session.address : undefined;
  if (!creatorWallet || !verifiedWallets.has(creatorWallet)) {
    return c.json({ error: "Verify your wallet before creating a campaign" }, 401);
  }
  campaign.creatorWallet = creatorWallet;
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

app.post("/api/campaigns/:id/pledge/challenge", async (c) => {
  const campaign = campaignStore.find((item) => item.id === c.req.param("id"));
  if (!campaign) return c.json({ error: "Campaign not found" }, 404);
  const body = await c.req.json<{ address?: string; amount?: number }>();
  const address = body.address?.trim();
  const amount = Number(body.amount);
  if (!address || !/^0x[a-fA-F0-9]{40}$/.test(address)) return c.json({ error: "Invalid wallet address" }, 400);
  if (!Number.isFinite(amount) || amount <= 0) return c.json({ error: "Invalid pledge amount" }, 400);
  const message = `CoinBackers pledge confirmation\nCampaign: ${campaign.title} (${campaign.id})\nAmount (USD): ${amount.toFixed(2)}\nAddress: ${address}\nNonce: ${crypto.randomUUID()}`;
  pledgeChallenges.set(`${campaign.id}:${address.toLowerCase()}`, { message, expiresAt: Date.now() + 5 * 60 * 1000 });
  return c.json({ message, expiresAt: Date.now() + 5 * 60 * 1000 });
});

app.post("/api/campaigns/:id/pledge", async (c) => {
  const campaign = campaignStore.find((item) => item.id === c.req.param("id"));
  if (!campaign) return c.json({ error: "Campaign not found" }, 404);
  const body = await c.req.json<{ amount?: number; address?: string; message?: string; signature?: string }>();
  const amount = Number(body.amount);
  const address = body.address?.trim();
  const challenge = address ? pledgeChallenges.get(`${campaign.id}:${address.toLowerCase()}`) : undefined;
  if (!Number.isFinite(amount) || amount <= 0) return c.json({ error: "Invalid pledge" }, 400);
  if (!address || !body.message || !body.signature || !challenge || challenge.expiresAt < Date.now() || challenge.message !== body.message) {
    return c.json({ error: "Pledge signature missing, expired, or invalid" }, 401);
  }
  try {
    const recovered = verifyMessage(body.message, body.signature);
    if (recovered.toLowerCase() !== address.toLowerCase()) return c.json({ error: "Signature does not match wallet" }, 401);
    pledgeChallenges.delete(`${campaign.id}:${address.toLowerCase()}`);
    campaign.pledged = Number(campaign.pledged || 0) + amount;
    campaign.backers = Number(campaign.backers || 0) + 1;
    const pledges = Array.isArray(campaign.pledges) ? campaign.pledges : [];
    pledges.push({ amount, backerWallet: recovered.toLowerCase(), at: new Date().toISOString() });
    campaign.pledges = pledges;
    await saveCampaigns();
    return c.json(campaign);
  } catch {
    return c.json({ error: "Invalid pledge signature" }, 401);
  }
});

app.get("/api/price", (c) => {
  const prices: Record<string, number> = { eth: 3200, btc: 95000, sol: 145, usdc: 1, xrp: 2.4, ada: 0.8, doge: 0.25, matic: 0.35, link: 18, ltc: 100 };
  const symbol = c.req.query("symbol")?.toLowerCase() || "";
  const usdPrice = prices[symbol];
  return usdPrice ? c.json({ symbol, usdPrice }) : c.json({ error: "Unsupported currency" }, 400);
});

app.get("/api/moonpay-config", (c) => {
  const publicKey = process.env.MOONPAY_PUBLIC_KEY || "";
  return c.json({ publicKey, enabled: Boolean(publicKey) });
});

const ARTWORK_COLORS = [
  ["#4f46e5", "#7c3aed"],
  ["#0ea5e9", "#6366f1"],
  ["#10b981", "#0ea5e9"],
  ["#f59e0b", "#ef4444"],
  ["#8b5cf6", "#ec4899"],
  ["#14b8a6", "#22c55e"],
  ["#f97316", "#eab308"],
  ["#6366f1", "#0ea5e9"],
];

function hashCode(input: string): number {
  let h = 0;
  for (let i = 0; i < input.length; i++) h = (Math.imul(31, h) + input.charCodeAt(i)) | 0;
  return Math.abs(h);
}

app.get("/api/artwork/:seed", (c) => {
  const seed = c.req.param("seed");
  const h = hashCode(seed);
  const [c1, c2] = ARTWORK_COLORS[h % ARTWORK_COLORS.length];
  const initials = seed
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((w) => w[0]!.toUpperCase())
    .join("") || "CB";
  const circles = Array.from({ length: 6 }, (_, i) => {
    const r = 40 + ((h >> (i * 2)) % 120);
    const cx = (h >> (i * 3)) % 900;
    const cy = (h >> (i * 4)) % 500;
    return `<circle cx="${cx}" cy="${cy}" r="${r}" fill="#ffffff" opacity="${0.04 + ((h >> i) % 5) * 0.02}" />`;
  }).join("");
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="900" height="500" viewBox="0 0 900 500">` +
    `<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">` +
    `<stop offset="0%" stop-color="${c1}"/><stop offset="100%" stop-color="${c2}"/></linearGradient></defs>` +
    `<rect width="900" height="500" fill="url(#g)"/>${circles}` +
    `<circle cx="450" cy="250" r="95" fill="#ffffff" opacity="0.14"/>` +
    `<text x="450" y="285" text-anchor="middle" font-family="system-ui, sans-serif" font-size="88" font-weight="700" fill="#ffffff" opacity="0.9">${initials}</text>` +
    `</svg>`;
  return new Response(svg, {
    headers: { "Content-Type": "image/svg+xml", "Cache-Control": "public, max-age=86400" },
  });
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
