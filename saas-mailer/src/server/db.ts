import { Database } from "bun:sqlite";
import { readFileSync } from "node:fs";

export type SqlValue = string | number | bigint | boolean | null | Uint8Array;
export type SqlParams = Record<string, SqlValue> | SqlValue[];

export function openDatabase(filename = process.env.DATABASE_PATH || ":memory:"): Database {
  const database = new Database(filename, { create: true, readwrite: true });
  database.exec("PRAGMA foreign_keys = ON");
  return database;
}

export function migrate(database: Database): void {
  database.exec(readFileSync(new URL("../../db/migrations/001_initial.sql", import.meta.url), "utf8"));
  const migration = readFileSync(new URL("../../db/migrations/002_contacts_custom_fields.sql", import.meta.url), "utf8");
  const hasCustomFields = database.query("SELECT 1 FROM pragma_table_info('contacts') WHERE name = 'custom_fields'").get();
  if (!hasCustomFields) database.exec(migration);
  const hasCredentialCiphertext = database.query("SELECT 1 FROM pragma_table_info('sending_accounts') WHERE name = 'credential_ciphertext'").get();
  if (!hasCredentialCiphertext) database.exec(readFileSync(new URL("../../db/migrations/003_sending_account_credentials.sql", import.meta.url), "utf8"));
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
