import crypto from 'crypto';
import Database from 'better-sqlite3';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { migrateDbSchema } from './migrations.js';
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const DB_PATH = path.resolve(__dirname, '../../data/freeapi.db');
let db;
export function getDb() {
    if (!db) {
        throw new Error('Database not initialized. Call initDb() first.');
    }
    return db;
}
export function initDb(dbPath) {
    const resolvedPath = dbPath ?? DB_PATH;
    const isMemory = resolvedPath === ':memory:';
    if (!isMemory) {
        const dataDir = path.dirname(resolvedPath);
        if (!fs.existsSync(dataDir)) {
            fs.mkdirSync(dataDir, { recursive: true });
        }
    }
    db = new Database(resolvedPath);
    if (!isMemory)
        db.pragma('journal_mode = WAL');
    db.pragma('foreign_keys = ON');
    migrateDbSchema(db);
    console.log(`Database initialized at ${resolvedPath}`);
    return db;
}
export function getUnifiedApiKey() {
    const db = getDb();
    const row = db.prepare("SELECT value FROM settings WHERE key = 'unified_api_key'").get();
    return row.value;
}
export function regenerateUnifiedKey() {
    const db = getDb();
    const key = `freellmapi-${crypto.randomBytes(24).toString('hex')}`;
    db.prepare("UPDATE settings SET value = ? WHERE key = 'unified_api_key'").run(key);
    return key;
}
// Generic key/value settings accessors (used by routing strategy, etc.).
export function getSetting(key) {
    const db = getDb();
    const row = db.prepare('SELECT value FROM settings WHERE key = ?').get(key);
    return row?.value;
}
export function setSetting(key, value) {
    const db = getDb();
    db.prepare(`
    INSERT INTO settings (key, value) VALUES (?, ?)
    ON CONFLICT(key) DO UPDATE SET value = excluded.value
  `).run(key, value);
}
//# sourceMappingURL=index.js.map