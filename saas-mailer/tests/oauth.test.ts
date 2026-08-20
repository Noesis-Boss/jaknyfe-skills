import { expect, test } from "bun:test";
import { consumeOAuthState, createOAuthState, oauthAuthorizationUrl } from "../src/server/sending/oauth";

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
