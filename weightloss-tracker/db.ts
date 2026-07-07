import { Database } from "bun:sqlite";

const DB_PATH = process.env.DB_PATH || "/home/workspace/weightloss-tracker/data/tracker.db";
import { mkdirSync } from "node:fs";
mkdirSync(require("node:path").dirname(DB_PATH), { recursive: true });

export const db = new Database(DB_PATH, { create: true });
db.run("PRAGMA journal_mode = WAL;");

db.run(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    name TEXT,
    provider TEXT NOT NULL DEFAULT 'magic',
    created_at INTEGER NOT NULL
  );
`);

db.run(`
  CREATE TABLE IF NOT EXISTS sessions (
    token TEXT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );
`);

db.run(`
  CREATE TABLE IF NOT EXISTS magic_tokens (
    token TEXT PRIMARY KEY,
    email TEXT NOT NULL,
    expires_at INTEGER NOT NULL
  );
`);

db.run(`
  CREATE TABLE IF NOT EXISTS profiles (
    user_id INTEGER PRIMARY KEY,
    start_weight REAL,
    target_weight REAL,
    start_date TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
  );
`);

db.run(`
  CREATE TABLE IF NOT EXISTS tracker_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    date TEXT NOT NULL,
    weight REAL,
    steps INTEGER,
    calories_in INTEGER,
    exercise_burn INTEGER DEFAULT 0,
    created_at INTEGER NOT NULL,
    UNIQUE(user_id, date),
    FOREIGN KEY (user_id) REFERENCES users(id)
  );
`);

export function getUserByEmail(email: string) {
  return db.query("SELECT * FROM users WHERE email = ?").get(email) as
    | { id: number; email: string; name: string | null; provider: string; created_at: number }
    | undefined;
}

export function createUser(email: string, name: string | null, provider: string) {
  const res = db
    .query("INSERT INTO users (email, name, provider, created_at) VALUES (?, ?, ?, ?) RETURNING id")
    .get(email, name, provider, Date.now()) as { id: number };
  return res.id;
}

export function getOrCreateUser(email: string, name: string | null, provider: string) {
  const existing = getUserByEmail(email);
  if (existing) return existing.id;
  return createUser(email, name, provider);
}

export function createSession(userId: number) {
  const token = crypto.randomUUID().replace(/-/g, "") + crypto.randomUUID().replace(/-/g, "");
  const expires = Date.now() + 1000 * 60 * 60 * 24 * 30; // 30 days
  db.query("INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)").run(token, userId, expires);
  return { token, expires };
}

export function getUserBySession(token: string) {
  const s = db.query("SELECT * FROM sessions WHERE token = ?").get(token) as
    | { token: string; user_id: number; expires_at: number }
    | undefined;
  if (!s || s.expires_at < Date.now()) return undefined;
  const u = db.query("SELECT id, email, name, provider FROM users WHERE id = ?").get(s.user_id) as
    | { id: number; email: string; name: string | null; provider: string }
    | undefined;
  return u;
}

export function deleteSession(token: string) {
  db.query("DELETE FROM sessions WHERE token = ?").run(token);
}

export function createMagicToken(email: string) {
  const token = crypto.randomUUID().replace(/-/g, "") + crypto.randomUUID().replace(/-/g, "");
  const expires = Date.now() + 1000 * 60 * 15; // 15 min
  db.query("INSERT INTO magic_tokens (token, email, expires_at) VALUES (?, ?, ?)").run(token, email, expires);
  return token;
}

export function consumeMagicToken(token: string) {
  const m = db.query("SELECT * FROM magic_tokens WHERE token = ?").get(token) as
    | { token: string; email: string; expires_at: number }
    | undefined;
  if (!m || m.expires_at < Date.now()) return undefined;
  db.query("DELETE FROM magic_tokens WHERE token = ?").run(token);
  return m.email;
}

export function getProfile(userId: number) {
  return db.query("SELECT * FROM profiles WHERE user_id = ?").get(userId) as any;
}

export function upsertProfile(
  userId: number,
  start_weight: number | null,
  target_weight: number | null,
  start_date: string | null
) {
  const now = Date.now();
  const existing = getProfile(userId);
  if (existing) {
    db.query(
      "UPDATE profiles SET start_weight = ?, target_weight = ?, start_date = ?, updated_at = ? WHERE user_id = ?"
    ).run(start_weight, target_weight, start_date, now, userId);
  } else {
    db.query(
      "INSERT INTO profiles (user_id, start_weight, target_weight, start_date, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)"
    ).run(userId, start_weight, target_weight, start_date, now, now);
  }
}

export function getEntries(userId: number) {
  return db
    .query("SELECT * FROM tracker_entries WHERE user_id = ? ORDER BY date ASC")
    .all(userId) as any[];
}

export function upsertEntry(
  userId: number,
  date: string,
  weight: number | null,
  steps: number | null,
  calories_in: number | null,
  exercise_burn: number
) {
  const existing = db.query("SELECT id FROM tracker_entries WHERE user_id = ? AND date = ?").get(userId, date) as
    | { id: number }
    | undefined;
  if (existing) {
    db.query(
      "UPDATE tracker_entries SET weight = ?, steps = ?, calories_in = ?, exercise_burn = ? WHERE id = ?"
    ).run(weight, steps, calories_in, exercise_burn, existing.id);
  } else {
    db.query(
      "INSERT INTO tracker_entries (user_id, date, weight, steps, calories_in, exercise_burn, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)"
    ).run(userId, date, weight, steps, calories_in, exercise_burn, Date.now());
  }
}
