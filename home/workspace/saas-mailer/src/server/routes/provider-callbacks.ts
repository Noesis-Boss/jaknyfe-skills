import { Hono } from "hono";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import type { AppConfig } from "../config";
import { requireTenant, requireTenantPostgres } from "../auth/middleware";
import { connectSendingAccount, connectSendingAccountPostgres } from "../sending/service";
import { consumeOAuthState, createOAuthState, exchangeOAuthCode, fetchProviderIdentity, oauthAuthorizationUrl } from "../sending/oauth";

const providers = ["gmail", "microsoft"] as const;
type Provider = typeof providers[number];
function isProvider(value: string): value is Provider { return providers.includes(value as Provider); }

function isPostgres(database: Database | PostgresDatabase): database is PostgresDatabase { return "sql" in database; }

export function createProviderCallbackRoutes(database: Database | PostgresDatabase, config: AppConfig): Hono {
  const routes = new Hono();
  routes.get("/api/oauth/:provider/start", async c => {
    const provider = c.req.param("provider");
    if (!isProvider(provider) || !config.oauth.callbackOrigin) return c.json({ error: "OAuth provider is not configured" }, 400);
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const state = createOAuthState({ provider, organizationId: tenant.organizationId, userId: tenant.userId });
      return c.redirect(oauthAuthorizationUrl(provider, state, { callbackOrigin: config.oauth.callbackOrigin, googleClientId: config.oauth.googleClientId, microsoftClientId: config.oauth.microsoftClientId }));
    } catch { return c.json({ error: "Unable to start provider connection" }, 401); }
  });
  routes.get("/api/oauth/:provider/callback", async c => {
    const provider = c.req.param("provider");
    if (!isProvider(provider)) return c.json({ error: "Unsupported OAuth provider" }, 400);
    try {
      const tenant = isPostgres(database) ? await requireTenantPostgres(database, c.req.raw) : requireTenant(database, c.req.raw);
      const state = consumeOAuthState(c.req.query("state") || "", { provider, organizationId: tenant.organizationId, userId: tenant.userId });
      const code = c.req.query("code");
      if (!code) return c.json({ error: "OAuth authorization was denied" }, 400);
      const tokens = await exchangeOAuthCode(provider, code, config.oauth);
      const email = await fetchProviderIdentity(provider, tokens.accessToken);
      const credentials = { ...tokens, expiresAt: tokens.expiresIn ? Date.now() + tokens.expiresIn * 1000 : undefined };
      if (isPostgres(database)) await connectSendingAccountPostgres(database, tenant.organizationId, { provider, email, credentials });
      else connectSendingAccount(database, tenant.organizationId, { provider, email, credentials });
      return c.redirect("/?connected=" + provider);
    } catch { return c.json({ error: "Unable to complete provider connection" }, 400); }
  });
  return routes;
}
