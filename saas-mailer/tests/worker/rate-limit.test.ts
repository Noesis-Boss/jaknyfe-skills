import { describe, expect, test } from "bun:test";
import { createTenantRateLimiter } from "../../src/worker/rate-limit";

describe("tenant rate limiter", () => {
  test("allows sends up to the per-tenant limit", () => {
    const limiter = createTenantRateLimiter(2);
    expect(limiter.tryAcquire("org-a", 1_000)).toBe(true);
    expect(limiter.tryAcquire("org-a", 1_001)).toBe(true);
    expect(limiter.tryAcquire("org-a", 1_002)).toBe(false);
  });

  test("limits tenants independently", () => {
    const limiter = createTenantRateLimiter(1);
    expect(limiter.tryAcquire("org-a", 1_000)).toBe(true);
    expect(limiter.tryAcquire("org-b", 1_001)).toBe(true);
    expect(limiter.tryAcquire("org-a", 1_002)).toBe(false);
    expect(limiter.tryAcquire("org-b", 1_003)).toBe(false);
  });

  test("frees the window after sixty seconds", () => {
    const limiter = createTenantRateLimiter(1);
    expect(limiter.tryAcquire("org-a", 1_000)).toBe(true);
    expect(limiter.tryAcquire("org-a", 30_000)).toBe(false);
    expect(limiter.tryAcquire("org-a", 61_000)).toBe(true);
  });

  test("visible reports current window usage", () => {
    const limiter = createTenantRateLimiter(5);
    limiter.tryAcquire("org-a", 1_000);
    limiter.tryAcquire("org-a", 1_500);
    limiter.tryAcquire("org-b", 1_600);
    expect(limiter.visible("org-a", 2_000)).toBe(2);
    expect(limiter.visible("org-b", 2_000)).toBe(1);
  });
});
