import { describe, expect, test } from "bun:test";
import { execute, migrate, openDatabase } from "../src/server/db";
import { getMockSendingAdapter, connectSendingAccount, listSendingAccounts, sendWithAccount } from "../src/server/sending/service";
import app, { database as appDatabase } from "../src/server";
import { authFor } from "./auth-helper";

process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY = "11".repeat(32);

function fixture() {
  const database = openDatabase();
  migrate(database);
  execute(database, "INSERT INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["org-a", "A", "org-b", "B"]);
  return database;
}

describe("sending accounts", () => {
  test("connects an account and never exposes credentials", () => {
    const database = fixture();
    const account = connectSendingAccount(database, "org-a", { provider: "mock", email: "Sender@Example.com", credentials: { token: "secret" } });
    expect(account).toMatchObject({ organization_id: "org-a", provider: "mock", email: "sender@example.com", status: "active" });
    expect(account).not.toHaveProperty("credential_ciphertext");
    const stored = database.query("SELECT credential_ciphertext FROM sending_accounts WHERE id = ?").get(account.id) as { credential_ciphertext: string };
    expect(stored.credential_ciphertext).toMatch(/^encrypted:v1:/);
    expect(stored.credential_ciphertext).not.toContain("secret");
  });

  test("fails closed when credential encryption is not configured", () => {
    const database = fixture();
    const configuredKey = process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY;
    delete process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY;
    try {
      expect(() => connectSendingAccount(database, "org-a", { provider: "mock", email: "x@example.com", credentials: { token: "secret" } })).toThrow("Credential encryption is not configured");
      expect(database.query("SELECT COUNT(*) AS count FROM sending_accounts").get()).toEqual({ count: 0 });
    } finally {
      process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY = configuredKey;
    }
  });

  test("selects only accounts in the active organization", () => {
    const database = fixture();
    connectSendingAccount(database, "org-a", { provider: "mock", email: "a@example.com", credentials: {} });
    connectSendingAccount(database, "org-b", { provider: "mock", email: "b@example.com", credentials: {} });
    expect(listSendingAccounts(database, "org-a")).toHaveLength(1);
    expect(() => connectSendingAccount(database, "org-a", { provider: "unknown", email: "x@example.com", credentials: {} })).toThrow("Unsupported sending provider");
  });

  test("delivers through the deterministic mock adapter", async () => {
    const database = fixture();
    const account = connectSendingAccount(database, "org-a", { provider: "mock", email: "sender@example.com", credentials: {} });
    const result = await sendWithAccount(database, "org-a", account.id, { from: "", to: "to@example.com", subject: "Hello", body: "Body" });
    expect(result.providerMessageId).toMatch(/^mock-/);
    expect(result.acceptedAt).toBeString();
    expect(getMockSendingAdapter().sent.at(-1)).toEqual({ from: "sender@example.com", to: "to@example.com", subject: "Hello", body: "Body" });
  });

  test("exposes tenant-safe account and send routes without credentials", async () => {
    execute(appDatabase, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?)", ["org-route", "Route"]);
    const cookie = await authFor("org-route");
    const response = await app.fetch(new Request("http://localhost/api/sending-accounts", { method: "POST", headers: { cookie, "content-type": "application/json" }, body: JSON.stringify({ provider: "mock", email: "route@example.com", credentials: { token: "secret" } }) }));
    expect(response.status).toBe(201);
    const account = await response.json();
    expect(account.credential_ciphertext).toBeUndefined();
    expect(account.provider).toBe("mock");
    const send = await app.fetch(new Request(`http://localhost/api/sending-accounts/${account.id}/send`, { method: "POST", headers: { cookie, "content-type": "application/json" }, body: JSON.stringify({ to: "to@example.com", subject: "Hi", body: "Body" }) }));
    expect(send.status).toBe(200);
    expect(await send.json()).toMatchObject({ providerMessageId: expect.stringMatching(/^mock-/) });
  });

  test("uses browser-safe errors and rejects cross-tenant route access", async () => {
    execute(appDatabase, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["org-safe-a", "A", "org-safe-b", "B"]);
    const cookieA = await authFor("org-safe-a"); const cookieB = await authFor("org-safe-b");
    const created = await app.fetch(new Request("http://localhost/api/sending-accounts", { method: "POST", headers: { cookie: cookieA, "content-type": "application/json" }, body: JSON.stringify({ provider: "mock", email: "safe@example.com", credentials: {} }) }));
    const account = await created.json();
    const listed = await app.fetch(new Request("http://localhost/api/sending-accounts", { headers: { cookie: cookieB } }));
    expect(await listed.json()).toEqual([]);
    const crossTenantSend = await app.fetch(new Request(`http://localhost/api/sending-accounts/${account.id}/send`, { method: "POST", headers: { cookie: cookieB, "content-type": "application/json" }, body: JSON.stringify({ to: "to@example.com", subject: "Hi", body: "Body" }) }));
    expect(crossTenantSend.status).toBe(400);
    expect(await crossTenantSend.json()).toEqual({ error: "Unable to send message" });
    const unsupported = await app.fetch(new Request("http://localhost/api/sending-accounts", { method: "POST", headers: { cookie: cookieA, "content-type": "application/json" }, body: JSON.stringify({ provider: "unknown", email: "safe@example.com", credentials: {} }) }));
    expect(await unsupported.json()).toEqual({ error: "Unable to connect sending account" });
  });
});
