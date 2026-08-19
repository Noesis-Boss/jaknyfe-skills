import { readFile } from "node:fs/promises";
import { SQL } from "bun";

export type PostgresDatabase = { sql: SQL; close(): Promise<void>; migrate(): Promise<void>; transaction<T>(fn: (tx: PostgresTransaction) => Promise<T>): Promise<T> };
export type PostgresTransaction = { query<T = Record<string, unknown>>(text: string, params?: unknown[]): Promise<T[]>; execute(text: string, params?: unknown[]): Promise<number> };

function interpolate(text: string, params: unknown[] = []): { text: string; params: unknown[] } {
  let index = 0;
  return { text: text.replace(/\?/g, () => `$${++index}`), params };
}

export function createPostgresDatabase(databaseUrl: string): PostgresDatabase {
  const sql = new SQL(databaseUrl);
  const query = async <T>(text: string, params: unknown[] = []): Promise<T[]> => {
    const converted = interpolate(text, params);
    return await sql.unsafe(converted.text, converted.params) as T[];
  };
  return {
    sql,
    async close() { await sql.close(); },
    async migrate() {
      const migration = await readFile(new URL("../../db/migrations/postgres/001_initial.sql", import.meta.url), "utf8");
      await sql.begin(async (tx) => { await tx.unsafe(migration); });
    },
    async transaction<T>(fn) {
      return await sql.begin(async (tx) => fn({ query: async (text, params = []) => await tx.unsafe(interpolate(text, params).text, params) as T[], execute: async (text, params = []) => { const rows = await tx.unsafe(interpolate(text, params).text, params) as Array<{ count?: number }>; return Number(rows[0]?.count || 0); } }));
    },
  };
}

export async function openProductionDatabase(databaseUrl = process.env.DATABASE_URL): Promise<PostgresDatabase> {
  if (!databaseUrl) throw new Error("Missing required configuration: DATABASE_URL");
  const database = createPostgresDatabase(databaseUrl);
  await database.migrate();
  return database;
}
