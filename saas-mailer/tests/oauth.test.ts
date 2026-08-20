import { expect, test } from "bun:test";
import { consumeOAuthState, createOAuthState, exchangeOAuthCode, fetchProviderIdentity, oauthAuthorizationUrl } from "../src/server/sending/oauth";

process.env.SESSION_SECRET = "test-session-secret";

test("OAuth state is tenant-bound and single-use", () => {
  const state = createOAuthState({ provider: "gmail", organizationId: "org-a", userId: "user-a" }, 1000);
  expect(() => consumeOAuthState(state, { provider: "gmail", organizationId: "org-b", userId: "user-a" }, 1001)).toThrow("Invalid OAuth state");
  expect(consumeOAuthState(state, { provider: "gmail", organizationId: "org-a", userId: "user-a" }, 1001).organizationId).toBe("org-a");
  expect(() => consumeOAuthState(state, { provider: "gmail", organizationId: "org-a", userId: "user-a" }, 1002)).toThrow("already used");
});

test("OAuth state expires and URLs contain no credentials", () => {
  const state = createOAuthState({ provider: "microsoft", organizationId: "org-a", userId: "user-a" }, 1000);
  expect(() => consumeOAuthState(state, { provider: "microsoft", organizationId: "org-a", userId: "user-a" }, 601001)).toThrow("Invalid OAuth state");
  const url = oauthAuthorizationUrl("gmail", "state", { callbackOrigin: "https://mailer.example", googleClientId: "client-id" });
  expect(url).toContain("gmail.send");
  expect(url).not.toContain("client-secret");
});

test("OAuth code exchange normalizes tokens without exposing client secrets", async () => {
  let request: Request | undefined;
  const tokens = await exchangeOAuthCode("gmail", "auth-code", { callbackOrigin: "https://mailer.example", googleClientId: "client-id", googleClientSecret: "client-secret" }, async (url, init) => { request = new Request(url, init); return new Response(JSON.stringify({ access_token: "access", refresh_token: "refresh", expires_in: 3600, token_type: "Bearer" }), { status: 200 }); });
  expect(tokens).toEqual({ accessToken: "access", refreshToken: "refresh", expiresIn: 3600, tokenType: "Bearer" });
  expect(await request?.text()).toContain("code=auth-code");
  expect(request?.url).toContain("oauth2.googleapis.com");
});

test("provider identity comes from the provider API", async () => {
  await expect(fetchProviderIdentity("microsoft", "access", async () => new Response(JSON.stringify({ mail: "Owner@Example.com" }), { status: 200 }))).resolves.toBe("owner@example.com");
});
