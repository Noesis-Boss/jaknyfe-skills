import Database from '/home/workspace/bound-by-ash-technical-debt/local-live/node_modules/better-sqlite3/lib/index.js';

const db = new Database('/home/workspace/freellmapi/server/data/freeapi.db');
const rows = db.prepare('SELECT id, platform, status FROM api_keys').all();
console.log(JSON.stringify(rows, null, 2));