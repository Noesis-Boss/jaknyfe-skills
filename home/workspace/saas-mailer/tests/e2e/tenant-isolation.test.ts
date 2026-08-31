import { expect, test } from "bun:test";
import app, { database } from "../../src/server";
import { execute } from "../../src/server/db";
import { authFor } from "../auth-helper";

test("tenant-scoped routes do not expose another organization's accounts or events", async () => {
  execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["iso-a", "Isolation A", "iso-b", "Isolation B"]);
  const cookieA = await authFor("iso-a"); const cookieB = await authFor("iso-b");
  const account = await app.fetch(new Request("http://localhost/api/sending-accounts", { headers: { cookie: cookieA } }));
  expect(account.status).toBe(200); expect(await account.json()).toEqual({ accounts: [] });
  const events = await app.fetch(new Request("http://localhost/api/events", { headers: { cookie: cookieB } }));
  expect(events.status).toBe(200); expect(await events.json()).toEqual({ events: [] });
  const missing = await app.fetch(new Request("http://localhost/api/events"));
  expect(missing.status).toBe(400); expect(await missing.json()).toEqual({ error: "Unable to list events" });
});
