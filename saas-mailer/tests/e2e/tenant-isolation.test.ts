import { expect, test } from "bun:test";
import app, { database } from "../../src/server";
import { execute } from "../../src/server/db";

test("tenant-scoped routes do not expose another organization's accounts or events", async () => {
  execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["iso-a", "Isolation A", "iso-b", "Isolation B"]);
  const account = await app.fetch(new Request("http://localhost/api/sending-accounts", { headers: { "x-organization-id": "iso-a" } }));
  expect(account.status).toBe(200); expect(await account.json()).toEqual([]);
  const events = await app.fetch(new Request("http://localhost/api/events", { headers: { "x-organization-id": "iso-b" } }));
  expect(events.status).toBe(200); expect(await events.json()).toEqual({ events: [] });
  const missing = await app.fetch(new Request("http://localhost/api/events"));
  expect(missing.status).toBe(400); expect(await missing.json()).toEqual({ error: "Unable to list events" });
});
