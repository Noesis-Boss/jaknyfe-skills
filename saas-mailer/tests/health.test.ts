import { describe, expect, test } from "bun:test";
import app from "../src/server";

describe("SaaS-Mailer health endpoint", () => {
  test("returns a healthy JSON response", async () => {
    const response = await app.fetch(new Request("http://localhost/api/health"));

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ ok: true });
  });
});
