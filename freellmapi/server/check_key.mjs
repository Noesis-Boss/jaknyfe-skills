import Database from '/home/workspace/freellmapi/server/node_modules/better-sqlite3/lib/index.js';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DB_PATH = path.resolve(__dirname, 'data/freeapi.db');
const db = new Database(DB_PATH);
const row = db.prepare("SELECT value FROM settings WHERE key = 'unified_api_key'").get();
console.log('unified_api_key:', row?.value || 'NOT SET');