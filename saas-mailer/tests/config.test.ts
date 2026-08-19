import { afterEach, describe, expect, test } from "bun:test";
import { loadConfig } from "../src/server/config";

const originalEnv = { ...process.env };

afterEach(() => {
  process.env = { ...originalEnv };
});

function setProductionEnv(): void {
  process.env = {
    ...originalEnv,
    APP_ENV: "production",
    DATABASE_URL: "postgres://mailer:test@localhost/mailer",
    SESSION_SECRET: "session-secret",
    CREDENTIAL_ENCRYPTION_KEY: "11".repeat(32),
    OAUTH_CALLBACK_ORIGIN: "https://mailer.example.com",
    GOOGLE_CLIENT_ID: "google-client-id",
    GOOGLE_CLIENT_SECRET: "google-client-secret",
    MICROSOFT_CLIENT_ID: "microsoft-client-id",
    MICROSOFT_CLIENT_SECRET: "microsoft-client-secret",
  };
}

describe("loadConfig", () => {
  test("permits development with the mock adapter and safe defaults", () => {
    process.env = { ...originalEnv, APP_ENV: "development" };

    const config = loadConfig();

    expect(config.appEnv).toBe("development");
    expect(config.sending.adapters).toEqual(["mock"]);
    expect(config.worker.pollIntervalMs).toBeGreaterThan(0);
  });

  test("rejects production without database URL and session secret", () => {
    process.env = { ...originalEnv, APP_ENV: "production" };

    expect(() => loadConfig()).toThrow(/DATABASE_URL.*SESSION_SECRET/);
  });

  test("rejects malformed encryption keys", () => {
    setProductionEnv();
    process.env.CREDENTIAL_ENCRYPTION_KEY = "not-a-key";

    expect(() => loadConfig()).toThrow(/CREDENTIAL_ENCRYPTION_KEY/);
  });

  test("requires callback origin and OAuth credentials in production", () => {
    setProductionEnv();
    delete process.env.OAUTH_CALLBACK_ORIGIN;

    expect(() => loadConfig()).toThrow(/OAUTH_CALLBACK_ORIGIN/);
  });

  test("parses worker intervals and limits explicitly", () => {
    setProductionEnv();
    process.env.WORKER_POLL_INTERVAL_MS = "2500";
    process.env.WORKER_BATCH_SIZE = "25";
    process.env.WORKER_MAX_SENDS_PER_HOUR = "100";

    const config = loadConfig();

    expect(config.worker).toEqual({ pollIntervalMs: 2500, batchSize: 25, maxSendsPerHour: 100 });
  });
});
