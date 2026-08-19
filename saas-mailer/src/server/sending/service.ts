import { createCipheriv, randomBytes, randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { ConnectSendingAccountInput, SendInput, SendResult, SendingAccount, SendingAdapter } from "./types";
import { MockSendingAdapter } from "./mock-adapter";

const adapters = new Map<string, SendingAdapter>([["mock", new MockSendingAdapter()]]);

function encryptionKey(): Buffer {
  const configuredKey = process.env.SENDING_CREDENTIAL_ENCRYPTION_KEY;
  if (!configuredKey) throw new Error("Credential encryption is not configured");
  const key = /^[0-9a-fA-F]{64}$/.test(configuredKey)
    ? Buffer.from(configuredKey, "hex")
    : Buffer.from(configuredKey, "base64");
  if (key.length !== 32) throw new Error("Credential encryption key is invalid");
  return key;
}

function encryptCredentials(credentials: Record<string, unknown>): string {
  const iv = randomBytes(12);
  const cipher = createCipheriv("aes-256-gcm", encryptionKey(), iv);
  const ciphertext = Buffer.concat([cipher.update(JSON.stringify(credentials), "utf8"), cipher.final()]);
  return `encrypted:v1:${iv.toString("base64url")}:${cipher.getAuthTag().toString("base64url")}:${ciphertext.toString("base64url")}`;
}

export function registerSendingAdapter(provider: string, adapter: SendingAdapter): void {
  adapters.set(provider, adapter);
}

export function getSendingAdapter(provider: string): SendingAdapter {
  const adapter = adapters.get(provider);
  if (!adapter) throw new Error(`Unsupported sending provider: ${provider}`);
  return adapter;
}

export function connectSendingAccount(database: Database, organizationId: string, input: ConnectSendingAccountInput): SendingAccount {
  if (!input.provider || !input.email || !input.credentials) throw new Error("Provider, email, and credentials are required");
  getSendingAdapter(input.provider);
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
