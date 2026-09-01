import { createCipheriv, createDecipheriv, randomBytes, randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { repositories } from "../repositories";
import type { ConnectSendingAccountInput, SendInput, SendResult, SendingAccount, SendingAdapter } from "./types";
import { MockSendingAdapter } from "./mock-adapter";
import { refreshOAuthToken } from "./oauth";

const adapters = new Map<string, SendingAdapter>([["mock", new MockSendingAdapter()]]);

function encryptionKey(): Buffer {
  const configuredKey = process.env.CREDENTIAL_ENCRYPTION_KEY || process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY;
  if (!configuredKey) throw new Error("Credential encryption is not configured");
  const key = /^[0-9a-fA-F]{64}$/.test(configuredKey)
    ? Buffer.from(configuredKey, "hex")
    : Buffer.from(configuredKey, "base64");
  if (key.length !== 32) throw new Error("Credential encryption key is invalid");
  return key;
}

export function encryptCredentials(credentials: Record<string, unknown>): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", encryptionKey(), iv);
  const ciphertext = Buffer.concat([cipher.update(JSON.stringify(credentials), "utf8"), cipher.final()]);
  return `encrypted:v1:${iv.toString("base64url")}:${cipher.getAuthTag().toString("base64url")}:${ciphertext.toString("base64url")}`;
}

export function decryptCredentials(value: string): Record<string, unknown> {
  const [prefix, version, ivText, tagText, ciphertextText] = value.split(":");
  if (prefix !== "encrypted" || version !== "v1" || !ivText || !tagText || !ciphertextText) throw new Error("Invalid encrypted credentials");
  const decipher = createDecipheriv("aes-256-gcm", encryptionKey(), Buffer.from(ivText, "base64url"));
  decipher.setAuthTag(Buffer.from(tagText, "base64url"));
  const plaintext = Buffer.concat([decipher.update(Buffer.from(ciphertextText, "base64url")), decipher.final()]).toString("utf8");
  const parsed = JSON.parse(plaintext);
  if (!parsed || typeof parsed !== "object") throw new Error("Invalid encrypted credentials");
  return parsed as Record<string, unknown>;
}

export async function connectSendingAccountPostgres(database: PostgresDatabase, organizationId: string, input: ConnectSendingAccountInput): Promise<SendingAccount> {
  if (!input.provider || !input.email || !input.credentials) throw new Error("Provider, email, and credentials are required");
  getSendingAdapter(input.provider);
  const store = repositories({ database, organizationId });
  const account = await store.accounts.insert({
    provider: input.provider,
    email: input.email,
    credentialCiphertext: encryptCredentials(input.credentials),
  });
  if (!account) throw new Error("Unable to create sending account");
  return account as SendingAccount;
}

export async function listSendingAccountsPostgres(database: PostgresDatabase, organizationId: string): Promise<SendingAccount[]> {
  return (await repositories({ database, organizationId }).accounts.list()) as SendingAccount[];
}

export async function sendWithAccountPostgres(database: PostgresDatabase, organizationId: string, accountId: string, input: SendInput): Promise<SendResult> {
  const account = await repositories({ database, organizationId }).accounts.findActive(accountId);
  if (!account) throw new Error("Sending account not found");
  let credentials = decryptCredentials(String(account.credential_ciphertext));
  if (typeof credentials.expiresAt === "number" && credentials.expiresAt <= Date.now() + 60_000 && typeof credentials.refreshToken === "string") {
    const refreshed = await refreshOAuthToken(String(account.provider) as "gmail" | "microsoft", credentials.refreshToken, {
      googleClientId: process.env.GOOGLE_CLIENT_ID,
      googleClientSecret: process.env.GOOGLE_CLIENT_SECRET,
      microsoftClientId: process.env.MICROSOFT_CLIENT_ID,
      microsoftClientSecret: process.env.MICROSOFT_CLIENT_SECRET,
    });
    credentials = { ...credentials, ...refreshed, expiresAt: refreshed.expiresIn ? Date.now() + refreshed.expiresIn * 1000 : undefined };
    await repositories({ database, organizationId }).accounts.updateCredentials(String(account.id), encryptCredentials(credentials));
  }
  const accessToken = typeof credentials.accessToken === "string" ? credentials.accessToken : "";
  const adapter = String(account.provider) === "gmail"
    ? (await import("./gmail-adapter")).gmailAdapter(accessToken)
    : String(account.provider) === "microsoft"
      ? (await import("./microsoft-adapter")).microsoftAdapter(accessToken)
      : getSendingAdapter(String(account.provider));
  return adapter.send({ ...input, from: input.from || String(account.email) });
}

export function registerSendingAdapter(provider: string, adapter: SendingAdapter): void {
  adapters.set(provider, adapter);
}

export function getSendingAdapter(provider: string): SendingAdapter {
  const adapter = adapters.get(provider);
  if (adapter) return adapter;
  if (provider === "gmail" || provider === "microsoft") return { send: async () => { throw new Error(`Use provider-specific send path for ${provider}`); } };
  throw new Error(`Unsupported sending provider: ${provider}`);
}

export function isConfiguredProvider(provider: string): boolean {
  return provider === "mock" || provider === "gmail" || provider === "microsoft" || provider === "smtp";
}

export function connectSendingAccount(database: Database, organizationId: string, input: ConnectSendingAccountInput): SendingAccount {
  if (!input.provider || !input.email || !input.credentials) throw new Error("Provider, email, and credentials are required");
  if (!isConfiguredProvider(input.provider)) throw new Error(`Unsupported sending provider: ${input.provider}`);
  const id = randomUUID();
  database.query("INSERT INTO sending_accounts (id, organization_id, provider, email, credential_ciphertext) VALUES (?, ?, ?, ?, ?)").run(id, organizationId, input.provider, input.email.trim().toLowerCase(), encryptCredentials(input.credentials));
  return database.query<SendingAccount, [string]>("SELECT id, organization_id, provider, email, status, created_at FROM sending_accounts WHERE id = ?").get(id) as SendingAccount;
}

export function listSendingAccounts(database: Database, organizationId: string): SendingAccount[] {
  return database.query<SendingAccount, [string]>("SELECT id, organization_id, provider, email, status, created_at FROM sending_accounts WHERE organization_id = ? ORDER BY created_at, id").all(organizationId);
}

export async function sendWithAccount(database: Database, organizationId: string, accountId: string, input: SendInput): Promise<SendResult> {
  const account = database.query<{ provider: string; email: string }, [string, string]>("SELECT provider, email FROM sending_accounts WHERE id = ? AND organization_id = ?").get(accountId, organizationId);
  if (!account) throw new Error("Sending account not found");
  return getSendingAdapter(account.provider).send({ ...input, from: input.from || account.email });
}

export function getMockSendingAdapter(): MockSendingAdapter {
  return getSendingAdapter("mock") as MockSendingAdapter;
}
