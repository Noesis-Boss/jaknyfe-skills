import { beforeEach, describe, expect, test } from "bun:test";
import app, { database } from "../src/server";
import { execute, migrate, openDatabase } from "../src/server/db";
import { createSession, lookupSession } from "../src/server/auth/session";
import { requireTenant } from "../src/server/auth/middleware";

function setup() { const db = openDatabase(); migrate(db); execute(db, "INSERT INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["auth-a", "A", "auth-b", "B"]); return db; }

describe("authenticated organization sessions", () => {
  beforeEach(() => { execute(database, "INSERT OR IGNORE INTO organizations (id, name) VALUES (?, ?), (?, ?)", ["auth-a", "A", "auth-b", "B"]); });
  test("registers and logs in without exposing password hashes or tokens", async () => {
    const db = setup();
    const register = await (await import("../src/server/routes/auth")).createAuthRoutes(db).fetch(new Request("http://localhost/api/auth/register", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "Owner@Example.com", password: "correct horse battery staple", organization_id: "auth-a" }) }));
    expect(register.status).toBe(201); expect(await register.json()).not.toHaveProperty("token");
    expect(db.query("SELECT password_hash FROM auth_passwords").get()).toBeTruthy();
    const login = await (await import("../src/server/routes/auth")).createAuthRoutes(db).fetch(new Request("http://localhost/api/auth/login", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "owner@example.com", password: "correct horse battery staple" }) }));
    expect(login.status).toBe(200); expect(login.headers.get("set-cookie")).toContain("HttpOnly");
  });
  test("rejects bad and missing sessions", async () => {
    expect((await app.fetch(new Request("http://localhost/api/auth/me"))).status).toBe(401);
    expect((await app.fetch(new Request("http://localhost/api/auth/login", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "missing@example.com", password: "wrong password" }) }))).status).toBe(401);
  });
  test("logout revokes the session", async () => {
    const response = await app.fetch(new Request("http://localhost/api/auth/register", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "logout@example.com", password: "correct horse battery staple", organization_id: "auth-a" }) }));
    const cookie = response.headers.get("set-cookie")!.split(";")[0];
    expect((await app.fetch(new Request("http://localhost/api/auth/me", { headers: { cookie } }))).status).toBe(200);
    expect((await app.fetch(new Request("http://localhost/api/auth/logout", { method: "POST", headers: { cookie } }))).status).toBe(200);
    expect((await app.fetch(new Request("http://localhost/api/auth/me", { headers: { cookie } }))).status).toBe(401);
  });
  test("expired sessions and forged organization headers cannot change tenant", async () => {
    const db = setup(); execute(db, "INSERT INTO users (id, email) VALUES (?, ?)", ["u1", "u1@example.com"]); execute(db, "INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)", ["auth-a", "u1", "member"]); const session = await createSession(db, "u1", "auth-a");
    execute(db, "UPDATE auth_sessions SET expires_at = ? WHERE id = ?", ["2000-01-01T00:00:00Z", session.id]); expect(lookupSession(db, session.token)).toBeNull();
    const live = await createSession(db, "u1", "auth-a"); const request = new Request("http://localhost/", { headers: { authorization: `Bearer ${live.token}`, "x-organization-id": "auth-b" } }); expect(requireTenant(db, request)).toMatchObject({ organizationId: "auth-a", userId: "u1", role: "member" });
  });
  test("denies cross-organization membership and forged session construction", async () => {
    const db = setup(); execute(db, "INSERT INTO users (id, email) VALUES (?, ?)", ["u2", "u2@example.com"]); expect(() => createSession(db, "u2", "auth-b")).toThrow("Organization access denied");
  });
  test("does not allow registration into an occupied organization", async () => {
    const db = setup(); execute(db, "INSERT INTO users (id, email) VALUES (?, ?)", ["owner", "owner@example.com"]); execute(db, "INSERT INTO organization_members (organization_id, user_id, role) VALUES (?, ?, ?)", ["auth-a", "owner", "owner"]);
    const response = await (await import("../src/server/routes/auth")).createAuthRoutes(db).fetch(new Request("http://localhost/api/auth/register", { method: "POST", headers: { "content-type": "application/json" }, body: JSON.stringify({ email: "intruder@example.com", password: "correct horse battery staple", organization_id: "auth-a" }) }));
    expect(response.status).toBe(400);
  });
});
