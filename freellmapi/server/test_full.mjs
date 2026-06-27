import { initDb, getUnifiedApiKey } from './dist/db/index.js';
initDb();

const key = getUnifiedApiKey();
console.log('Key:', key?.substr(0, 20) + '...');

const res = await fetch('http://localhost:3001/v1/chat/completions', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${key}` },
  body: JSON.stringify({
    model: 'openrouter/owl-alpha',
    messages: [{ role: 'user', content: 'Say OK' }]
  })
});
console.log('Status:', res.status);
const text = await res.text();
console.log(text.length > 100 ? text.slice(0, 100) + '...' : text);