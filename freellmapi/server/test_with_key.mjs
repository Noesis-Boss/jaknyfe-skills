import Database from '/home/workspace/freellmapi/server/node_modules/better-sqlite3/lib/index.js';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DB_PATH = path.resolve(__dirname, 'data/freeapi.db');
const db = new Database(DB_PATH);
const row = db.prepare("SELECT value FROM settings WHERE key = 'unified_api_key'").get();
const key = row?.value || 'NOT SET';
console.log('Using key:', key.substring(0, 20) + '...');

const res = await fetch('http://localhost:3001/v1/models', {
  headers: { Authorization: `Bearer ${key}` }
});
const data = await res.text();
console.log('Response:', data.substring(0, 100));