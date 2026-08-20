import { expect, test } from "bun:test";
import { createProviderCallbackRoutes } from "../src/server/routes/provider-callbacks";
import { openDatabase, migrate } from "../src/server/db";
import { registerUser } from "../src/server/auth/password";
import { createSession } from "../src/server/auth/session";
import { loadConfig } from "../src/server/config";

process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY = "00".repeat(32);
process.env.SESSION_SECRET = "callback-test-secret";

test("provider start requires an authenticated tenant", async () => {
  const db = openDatabase(); migrate(db);
  const app = createProviderCallbackRoutes(db, loadConfig({ APP_ENV: "test", OAUTH_CALLBACK_ORIGIN: "https://mailer.example", GOOGLE_CLIENT_ID: "google-client" }));
  const response = await app.fetch(new Request("http://localhost/api/oauth/gmail/start"));
  expect(response.status).toBe(401);
});

test("provider callback rejects missing provider identity", async () => {
  const db = openDatabase(); migrate(db);
  const user = await registerUser(db, "owner@example.com", "correct horse battery", "Workspace");
  const session = await createSession(db, user.id, user.organizationId!);
  const app = createProviderCallbackRoutes(db, loadConfig({ APP_ENV: "test", OAUTH_CALLBACK_ORIGIN: "https://mailer.example", GOOGLE_CLIENT_ID: "google-client", GOOGLE_CLIENT_SECRET: "google-secret" }));
  const response = await app.fetch(new Request("http://localhost/api/oauth/gmail/callback?state=bad&code=code", { headers: { cookie: `saas_mailer_session=${session.token}` } }));
  expect(response.status).toBe(400);
});
