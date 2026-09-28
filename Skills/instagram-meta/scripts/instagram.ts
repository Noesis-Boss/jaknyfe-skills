#!/usr/bin/env bun
// Instagram Content Publishing CLI — Meta Graph API (Facebook Login for Business).
//
// Required env: INSTAGRAM_ACCESS_TOKEN
// Optional env: INSTAGRAM_USER_ID (IGSID), INSTAGRAM_API_VERSION (default v23.0),
//               INSTAGRAM_GRAPH_HOST (default graph.facebook.com),
//               META_APP_ID / META_APP_SECRET (token refresh only)

type Args = Record<string, string | string[]>;

const VERSION = process.env.INSTAGRAM_API_VERSION || "v23.0";
const HOST = process.env.INSTAGRAM_GRAPH_HOST || "graph.facebook.com";
const BASE = `https://${HOST}/${VERSION}`;

function parseArgs(argv: string[]): Args {
  const out: Args = {};
  const flags: string[] = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith("--")) {
        out[key] = "true";
      } else {
        const existing = out[key];
        if (existing === undefined) out[key] = next;
        else if (Array.isArray(existing)) existing.push(next);
        else out[key] = [existing, next];
        i++;
      }
    } else {
      flags.push(a);
    }
  }
  return { ...out, _: flags };
}

function token(): string {
  const t = process.env.INSTAGRAM_ACCESS_TOKEN;
  if (!t) {
    fail(
      "INSTAGRAM_ACCESS_TOKEN is not set.",
      "Add it in Zo under Settings > Advanced > Secrets, as a Meta long-lived user access token.",
    );
  }
  return t;
}

function first(v: string | string[] | undefined): string | undefined {
  return Array.isArray(v) ? v[0] : v;
}

function list(v: string | string[] | undefined): string[] {
  if (v === undefined) return [];
  return Array.isArray(v) ? v : v.split(",").map((s) => s.trim()).filter(Boolean);
}

function fail(message: string, hint?: string): never {
  console.log(JSON.stringify({ ok: false, error: message, hint: hint || null }, null, 2));
  process.exit(1);
}

async function graph(
  path: string,
  method: "GET" | "POST" = "GET",
  params: Record<string, string> = {},
): Promise<any> {
  const url = new URL(`${BASE}${path.startsWith("/") ? path : `/${path}`}`);
  url.searchParams.set("access_token", token());
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null) url.searchParams.set(k, v);
  }
  if (method === "GET") {
    const res = await fetch(url);
    const json = await res.json();
    if (json.error) throw graphError(json.error);
    return json;
  }
  const res = await fetch(url, { method: "POST" });
  const json = await res.json();
  if (json.error) throw graphError(json.error);
  return json;
}

function graphError(e: any): Error {
  const err = new Error(`Graph API error: ${e.message}`);
  (err as any).details = {
    code: e.code,
    subcode: e.error_subcode,
    type: e.type,
    fbtrace_id: e.fbtrace_id,
  };
  return err;
}

async function igUserId(explicit?: string): Promise<string> {
  if (explicit) return explicit;
  const env = process.env.INSTAGRAM_USER_ID;
  if (env) return env;
  const accounts = await graph("/me/accounts", "GET", {
    fields: "id,name,instagram_business_account{id,username}",
    limit: "50",
  });
  for (const page of accounts.data || []) {
    if (page.instagram_business_account?.id) return page.instagram_business_account.id;
  }
  fail(
    "No Instagram professional account is linked to any Facebook Page you manage.",
    "In Instagram, switch to a Professional (Business or Creator) account and link it to a Facebook Page. Then set INSTAGRAM_USER_ID to the ig user id.",
  );
}

async function waitForContainer(igsid: string, creationId: string, timeoutMs = 300000): Promise<any> {
  const started = Date.now();
  let last = "";
  while (Date.now() - started < timeoutMs) {
    const r = await graph(`/${igsid}/media`, "GET", { fields: "status_code,status", creation_id: creationId });
    last = r.status_code || r.status || "UNKNOWN";
    if (last === "FINISHED") return r;
    if (last === "ERROR" || last === "EXPIRED") {
      fail(`Container ${creationId} finished in state ${last}.`, "Check the media file: size, aspect ratio, codec, and that the URL is publicly reachable over HTTPS.");
    }
    await new Promise((res) => setTimeout(res, 15000));
  }
  fail(`Container ${creationId} still ${last} after ${Math.round(timeoutMs / 1000)}s.`, "Instagram video processing can take several minutes for large files.");
}

async function publish(igsid: string, creationId: string) {
  const r = await graph(`/${igsid}/media_publish`, "POST", { creation_id: creationId });
  console.log(JSON.stringify({ ok: true, action: "published", id: r.id, permalink: permalinkFor(r.id) }, null, 2));
}

function permalinkFor(id: string): string | null {
  if (!id.startsWith("1784")) return null;
  return `https://www.instagram.com/p/${id.split("_")[0]}/`;
}

const COMMANDS: Record<string, (a: Args) => Promise<void>> = {
  async check(a) {
    const me = await graph("/me", "GET", { fields: "id,name" });
    const accounts = await graph("/me/accounts", "GET", {
      fields: "id,name,access_token,instagram_business_account{id,username}",
      limit: "50",
    });
    const linked = (accounts.data || []).filter((p: any) => p.instagram_business_account?.id);
    const igsid = await igUserId(first(a["id"] as string | string[]));
    const profile = await graph(`/${igsid}`, "GET", {
      fields: "id,username,name,media_count,followers_count,following_count,profile_picture_url,website",
    });
    let quota: any = null;
    try {
      quota = await graph(`/${igsid}/content_publishing_limit`, "GET", {
        fields: "quota_usage,config,rate_limit_settings",
      });
    } catch {
      quota = { error: "content_publishing_limit unavailable — instagram_content_publish scope may be missing" };
    }
    console.log(
      JSON.stringify(
        {
          ok: true,
          token_owner: { id: me.id, name: me.name },
          facebook_pages: (accounts.data || []).map((p: any) => ({
            id: p.id,
            name: p.name,
            linked_instagram: p.instagram_business_account?.username || null,
          })),
          linked_page_count: linked.length,
          instagram: profile,
          quota,
          api_version: VERSION,
        },
        null,
        2,
      ),
    );
  },

  async profile(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    console.log(
      JSON.stringify(
        { ok: true, ...(await graph(`/${igsid}`, "GET", { fields: "id,username,name,biography,website,media_count,followers_count,following_count,profile_picture_url" })) },
        null,
        2,
      ),
    );
  },

  async posts(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    const limit = first(a["limit"] as string | string[]) || "10";
    const r = await graph(`/${igsid}/media`, "GET", {
      fields: "id,caption,media_type,media_product_type,permalink,timestamp,like_count,comments_count,media_url,thumbnail_url",
      limit,
    });
    console.log(JSON.stringify({ ok: true, count: (r.data || []).length, media: r.data || [] }, null, 2));
  },

  async quota(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    console.log(
      JSON.stringify({ ok: true, ...(await graph(`/${igsid}/content_publishing_limit`, "GET", { fields: "quota_usage,config,rate_limit_settings" })) }, null, 2),
    );
  },

  async insights(a) {
    const mediaId = a._[0];
    if (!mediaId) fail("Usage: insights <MEDIA_ID>");
    const metric = first(a["metric"] as string | string[]) || "reach,likes,comments,saved,shares,total_interactions";
    const r = await graph(`/${mediaId}/insights`, "GET", { metric });
    console.log(JSON.stringify({ ok: true, media_id: mediaId, data: r.data || [] }, null, 2));
  },

  async post(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    const imageUrl = first(a["url"] as string | string[]);
    const caption = first(a["caption"] as string | string[]) || "";
    if (!imageUrl) fail("Usage: post --url <PUBLIC_IMAGE_URL> --caption <text>");
    const container = await graph(`/${igsid}/media`, "POST", { image_url: imageUrl, caption });
    await publish(igsid, container.id);
  },

  async reel(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    const videoUrl = first(a["url"] as string | string[]);
    const caption = first(a["caption"] as string | string[]) || "";
    if (!videoUrl) fail("Usage: reel --url <PUBLIC_MP4_URL> --caption <text>");
    const container = await graph(`/${igsid}/media`, "POST", {
      video_url: videoUrl,
      caption,
      media_type: "REELS",
      share_to_feed: first(a["share_to_feed"] as string | string[]) || "true",
    });
    await waitForContainer(igsid, container.id);
    await publish(igsid, container.id);
  },

  async carousel(a) {
    const igsid = await igUserId(first(a["id"] as string | string[]));
    const urls = list(a["url"] as string | string[]);
    const caption = first(a["caption"] as string | string[]) || "";
    if (urls.length < 2) fail("Usage: carousel --url <URL1> --url <URL2> [--url <URL3>...] --caption <text>");
    const children = urls.map((u) => JSON.stringify({ media_type: "IMAGE", image_url: u })).join(",");
    const container = await graph(`/${igsid}/media`, "POST", {
      media_type: "CAROUSEL",
      children,
      caption,
    });
    await publish(igsid, container.id);
  },

  async status(a) {
    const id = a._[0];
    if (!id) fail("Usage: status <CREATION_ID>");
    console.log(JSON.stringify({ ok: true, ...(await graph(`/${id}`, "GET", { fields: "id,status,status_code" })) }, null, 2));
  },

  async delete(a) {
    const id = a._[0];
    if (!id) fail("Usage: delete <MEDIA_ID>");
    const r = await graph(`/${id}`, "DELETE");
    console.log(JSON.stringify({ ok: r.success === true, media_id: id, deleted: r.success === true }, null, 2));
  },

  async refresh() {
    const appId = process.env.META_APP_ID;
    const appSecret = process.env.META_APP_SECRET;
    if (!appId || !appSecret) {
      fail("META_APP_ID and META_APP_SECRET are required for token refresh.", "Add both in Zo under Settings > Advanced > Secrets.");
    }
    const url = new URL(`${BASE}/oauth/access_token`);
    url.searchParams.set("grant_type", "fb_exchange_token");
    url.searchParams.set("client_id", appId);
    url.searchParams.set("client_secret", appSecret);
    url.searchParams.set("fb_exchange_token", token());
    const res = await fetch(url);
    const json: any = await res.json();
    if (json.error) throw graphError(json.error);
    console.log(
      JSON.stringify(
        {
          ok: true,
          note: "Paste the new value into Zo Settings > Advanced > Secrets as INSTAGRAM_ACCESS_TOKEN. Never paste it into chat or a repo.",
          access_token: json.access_token,
          expires_in_days: Math.round((json.expires_in || 0) / 86400),
        },
        null,
        2,
      ),
    );
  },
};

const HELP = `instagram.ts — Instagram Content Publishing via Meta Graph API

  check                                  verify token, linked Page, profile, and publish quota
  profile                                profile fields for the connected account
  posts [--limit 10]                     recent posts with captions and engagement
  insights <MEDIA_ID>                    reach / likes / comments / saves / shares
  quota                                  remaining 24h publish quota
  post --url <PUBLIC_IMAGE_URL> --caption <text>          single image / feed post
  reel --url <PUBLIC_MP4_URL> --caption <text>           video reel
  carousel --url <U1> --url <U2> [--url <U3>] --caption <text>   2-10 item carousel
  status <CREATION_ID>                   container processing state
  delete <MEDIA_ID>                      delete a post
  refresh                                exchange for a new ~60 day long-lived token

All flags accept --id <IGSID> to target a specific account.
Media URLs must be publicly reachable over HTTPS — Instagram fetches them itself.

Env: INSTAGRAM_ACCESS_TOKEN (required), INSTAGRAM_USER_ID, INSTAGRAM_API_VERSION,
     INSTAGRAM_GRAPH_HOST, META_APP_ID, META_APP_SECRET`;

async function main() {
  const argv = process.argv.slice(2);
  if (!argv.length || argv[0] === "help" || argv[0] === "--help" || argv[0] === "-h") {
    console.log(HELP);
    return;
  }
  const [cmd, ...rest] = argv;
  const handler = COMMANDS[cmd];
  if (!handler) {
    console.log(HELP);
    console.log(`\nUnknown command: ${cmd}`);
    process.exit(1);
  }
  try {
    await handler(parseArgs(rest));
  } catch (e: any) {
    fail(e.message || String(e), e.details ? JSON.stringify(e.details) : undefined);
  }
}

await main();
