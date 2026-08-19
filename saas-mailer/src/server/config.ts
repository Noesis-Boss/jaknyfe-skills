export type AppEnv = "development" | "test" | "production";

export type AppConfig = {
  appEnv: AppEnv;
  database: "sqlite" | "postgres";
  databaseUrl?: string;
  sessionSecret?: string;
  credentialEncryptionKey?: string;
  oauth: {
    callbackOrigin?: string;
    googleClientId?: string;
    googleClientSecret?: string;
    microsoftClientId?: string;
    microsoftClientSecret?: string;
  };
  sending: {
    adapters: string[];
  };
  worker: {
    pollIntervalMs: number;
    batchSize: number;
    maxSendsPerHour: number;
  };
};

const DEFAULTS = {
  pollIntervalMs: 5_000,
  batchSize: 25,
  maxSendsPerHour: 100,
} as const;

function required(env: NodeJS.ProcessEnv, name: string): string {
  const value = env[name]?.trim();
  if (!value) throw new Error(`Missing required configuration: ${name}`);
  return value;
}

function optional(env: NodeJS.ProcessEnv, name: string): string | undefined {
  const value = env[name]?.trim();
  return value || undefined;
}

function positiveInteger(env: NodeJS.ProcessEnv, name: string, fallback: number): number {
  const raw = optional(env, name);
  if (!raw) return fallback;
  if (!/^\d+$/.test(raw)) throw new Error(`Invalid configuration: ${name} must be a positive integer`);
  const value = Number(raw);
  if (!Number.isSafeInteger(value) || value <= 0) throw new Error(`Invalid configuration: ${name} must be a positive integer`);
  return value;
}

function encryptionKey(env: NodeJS.ProcessEnv, production: boolean): string | undefined {
  const value = optional(env, "CREDENTIAL_ENCRYPTION_KEY");
  if (!value) {
    if (production) throw new Error("Missing required configuration: CREDENTIAL_ENCRYPTION_KEY");
    return undefined;
  }
  const isHex = /^[0-9a-fA-F]{64}$/.test(value);
  let bytes: Uint8Array;
  try {
    bytes = isHex ? Buffer.from(value, "hex") : Buffer.from(value, "base64");
  } catch {
    throw new Error("Invalid configuration: CREDENTIAL_ENCRYPTION_KEY must encode 32 bytes");
  }
  if (bytes.length !== 32) throw new Error("Invalid configuration: CREDENTIAL_ENCRYPTION_KEY must encode 32 bytes");
  return value;
}

export function loadConfig(env: NodeJS.ProcessEnv = process.env): AppConfig {
  const appEnv = (optional(env, "APP_ENV") || "development") as AppEnv;
  if (!["development", "test", "production"].includes(appEnv)) throw new Error("Invalid configuration: APP_ENV");
  const production = appEnv === "production";
  if (production) {
    const missing = ["DATABASE_URL", "SESSION_SECRET", "OAUTH_CALLBACK_ORIGIN"].filter((name) => !optional(env, name));
    if (!optional(env, "CREDENTIAL_ENCRYPTION_KEY")) missing.push("CREDENTIAL_ENCRYPTION_KEY");
    if (missing.length) throw new Error(`Missing required configuration: ${missing.join(", ")}`);
  }
  const databaseUrl = optional(env, "DATABASE_URL");
  const sessionSecret = optional(env, "SESSION_SECRET");
  const credentialEncryptionKey = encryptionKey(env, production);
  const callbackOrigin = production ? required(env, "OAUTH_CALLBACK_ORIGIN") : optional(env, "OAUTH_CALLBACK_ORIGIN");

  return {
    appEnv,
    database: production ? "postgres" : "sqlite",
    databaseUrl,
    sessionSecret,
    credentialEncryptionKey,
    oauth: {
      callbackOrigin,
      googleClientId: optional(env, "GOOGLE_CLIENT_ID"),
      googleClientSecret: optional(env, "GOOGLE_CLIENT_SECRET"),
      microsoftClientId: optional(env, "MICROSOFT_CLIENT_ID"),
      microsoftClientSecret: optional(env, "MICROSOFT_CLIENT_SECRET"),
    },
    sending: { adapters: production ? ["gmail", "microsoft", "smtp"] : ["mock"] },
    worker: {
      pollIntervalMs: positiveInteger(env, "WORKER_POLL_INTERVAL_MS", DEFAULTS.pollIntervalMs),
      batchSize: positiveInteger(env, "WORKER_BATCH_SIZE", DEFAULTS.batchSize),
      maxSendsPerHour: positiveInteger(env, "WORKER_MAX_SENDS_PER_HOUR", DEFAULTS.maxSendsPerHour),
    },
  };
}
