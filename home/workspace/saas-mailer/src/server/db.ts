import { Database } from "bun:sqlite";
import { readFileSync } from "node:fs";
import { openProductionDatabase, type PostgresDatabase } from "./postgres";

export type SqlValue = string | number | bigint | boolean | null | Uint8Array;
export type SqlParams = Record<string, SqlValue> | SqlValue[];

export function openDatabase(filename = process.env.DATABASE_PATH || ":memory:"): Database {
  const database = new Database(filename, { create: true, readwrite: true });
  database.exec("PRAGMA foreign_keys = ON");
  return database;
}

export function hostedMode(env: NodeJS.ProcessEnv = process.env): boolean {
  return env.APP_ENV === "production";
}

export async function openConfiguredDatabase(env: NodeJS.ProcessEnv = process.env): Promise<Database | PostgresDatabase> {
  if (hostedMode(env)) return openProductionDatabase(env.DATABASE_URL);
  return openDatabase(env.DATABASE_PATH || ":memory:");
}

export function migrate(database: Database): void {
  database.exec(readFileSync(new URL("../../db/migrations/001_initial.sql", import.meta.url), "utf8"));
  const migration = readFileSync(new URL("../../db/migrations/002_contacts_custom_fields.sql", import.meta.url), "utf8");
  const hasCustomFields = database.query("SELECT 1 FROM pragma_table_info('contacts') WHERE name = 'custom_fields'").get();
  if (!hasCustomFields) database.exec(migration);
  const hasCredentialCiphertext = database.query("SELECT 1 FROM pragma_table_info('sending_accounts') WHERE name = 'credential_ciphertext'").get();
  if (!hasCredentialCiphertext) database.exec(readFileSync(new URL("../../db/migrations/003_sending_account_credentials.sql", import.meta.url), "utf8"));
  const hasApproval = database.query("SELECT 1 FROM pragma_table_info('campaigns') WHERE name = 'approved_at'").get();
  if (!hasApproval) database.exec(readFileSync(new URL("../../db/migrations/004_campaign_approval.sql", import.meta.url), "utf8"));
  const hasAccountSafety = database.query("SELECT 1 FROM pragma_table_info('campaigns') WHERE name = 'timezone'").get();
  if (!hasAccountSafety) database.exec(readFileSync(new URL("../../db/migrations/005_campaign_account_safety.sql", import.meta.url), "utf8"));
  const hasWorkerFields = database.query("SELECT 1 FROM pragma_table_info('messages') WHERE name = 'error_code'").get();
  if (!hasWorkerFields) database.exec(readFileSync(new URL("../../db/migrations/006_worker_events.sql", import.meta.url), "utf8"));
  database.exec(readFileSync(new URL("../../db/migrations/007_auth_sessions.sql", import.meta.url), "utf8"));
  database.exec(readFileSync(new URL("../../db/migrations/008_contact_lists.sql", import.meta.url), "utf8"));
  const hasCampaignType = database.query("SELECT 1 FROM pragma_table_info('campaigns') WHERE name = 'campaign_type'").get();
  if (!hasCampaignType) database.exec(readFileSync(new URL("../../db/migrations/009_ghost_campaigns.sql", import.meta.url), "utf8"));
}

export function query<T extends Record<string, unknown>>(
  database: Database,
  sql: string,
  params: SqlParams = [],
): T[] {
  const statement = database.query<T, SqlParams>(sql);
  return Array.isArray(params) ? statement.all(...params) : statement.all(params);
}

export function execute(database: Database, sql: string, params: SqlParams = []): void {
  const statement = database.query(sql);
  if (Array.isArray(params)) statement.run(...params);
  else statement.run(params);
}
