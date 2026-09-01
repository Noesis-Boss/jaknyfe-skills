import { readFile } from "node:fs/promises";
import { SQL } from "bun";

export type PostgresDatabase = { sql: SQL; query<T = Record<string, unknown>>(text: string, params?: unknown[]): Promise<T[]>; execute(text: string, params?: unknown[]): Promise<number>; close(): Promise<void>; migrate(): Promise<void>; transaction<T>(fn: (tx: PostgresTransaction) => Promise<T>): Promise<T> };
export type PostgresTransaction = { query<T = Record<string, unknown>>(text: string, params?: unknown[]): Promise<T[]>; execute(text: string, params?: unknown[]): Promise<number> };

function interpolate(text: string, params: unknown[] = []): { text: string; params: unknown[] } {
  let index = 0;
  return { text: text.replace(/\?/g, () => `$${++index}`), params };
}

async function queryWith<T>(runner: { unsafe(text: string, params?: unknown[]): Promise<unknown> }, text: string, params: unknown[] = []): Promise<T[]> {
  const converted = interpolate(text, params);
  return await runner.unsafe(converted.text, converted.params) as T[];
}

export function createPostgresDatabase(databaseUrl: string): PostgresDatabase {
  const sql = new SQL(databaseUrl);
  const query = <T>(text: string, params: unknown[] = []) => queryWith<T>(sql, text, params);
  const execute = async (text: string, params: unknown[] = []) => { await queryWith(sql, text, params); return 1; };
  return {
    sql,
    query,
    execute,
    async close() { await sql.close(); },
    async migrate() {
      const migration = await readFile(new URL("../../db/migrations/postgres/001_initial.sql", import.meta.url), "utf8");
      const listsMigration = await readFile(new URL("../../db/migrations/postgres/002_contact_lists.sql", import.meta.url), "utf8");
      await sql.begin(async (tx) => {
        await tx.unsafe("CREATE TABLE IF NOT EXISTS schema_migrations (version TEXT PRIMARY KEY, applied_at TIMESTAMPTZ NOT NULL DEFAULT now())");
        const applied = await tx.unsafe("SELECT 1 FROM schema_migrations WHERE version = $1", ["001_initial"]);
        if (!Array.isArray(applied) || applied.length === 0) await tx.unsafe(migration);
        await tx.unsafe("ALTER TABLE messages ADD COLUMN IF NOT EXISTS next_attempt_at TIMESTAMPTZ NOT NULL DEFAULT now()");
        await tx.unsafe("ALTER TABLE messages ADD COLUMN IF NOT EXISTS lease_owner TEXT");
        await tx.unsafe("ALTER TABLE messages ADD COLUMN IF NOT EXISTS lease_until TIMESTAMPTZ");
        await tx.unsafe("CREATE INDEX IF NOT EXISTS idx_messages_queue ON messages(status, next_attempt_at, lease_until, created_at)");
        await tx.unsafe(listsMigration);
      });
    },
    async transaction<T>(fn) {
      return await sql.begin(async (tx) => fn({ query: <R>(text, params = []) => queryWith<R>(tx, text, params), execute: async (text, params = []) => { await queryWith(tx, text, params); return 1; } }));
    },
  };
}

export async function openProductionDatabase(databaseUrl = process.env.DATABASE_URL): Promise<PostgresDatabase> {
  if (!databaseUrl) throw new Error("Missing required configuration: DATABASE_URL");
  const database = createPostgresDatabase(databaseUrl);
  await database.migrate();
  return database;
}
