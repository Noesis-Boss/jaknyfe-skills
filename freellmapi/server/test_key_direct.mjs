import Database from '../node_modules/better-sqlite3/index.js';
import { initDb } from '../dist/db/index.js';
initDb();
const db = getDb();
const row = db.prepare('SELECT encrypted_key FROM api_keys WHERE platform = "openrouter"').get();
if (!row) { console.log('No key'); process.exit(1); }
const key = decrypt(row.encrypted_key);
console.log('Decrypted length:', key.length);