import { describe, expect, test } from "bun:test";
import { retryAt, retryDelayMs } from "../../src/worker/backoff";

describe("durable worker backoff", () => {
  test("grows exponentially and is bounded", () => {
    expect(retryDelayMs(1)).toBe(30_000);
    expect(retryDelayMs(3)).toBe(120_000);
    expect(retryDelayMs(99)).toBe(3_600_000);
  });

  test("computes the next retry time", () => {
    const now = new Date("2026-08-20T00:00:00.000Z");
    expect(retryAt(2, now).toISOString()).toBe("2026-08-20T00:01:00.000Z");
  });
});
