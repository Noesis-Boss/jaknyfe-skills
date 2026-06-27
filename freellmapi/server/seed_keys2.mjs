import { initDb, getDb } from './dist/db/index.js';
import { encrypt } from './dist/lib/crypto.js';
import { readFileSync } from 'fs';

// Must init DB first (which calls initEncryptionKey internally)
initDb();
const db = getDb();

// Read keys from .env
const envContent = readFileSync(new URL('./.env', import.meta.url), 'utf8');
const env = {};
for (const line of envContent.split('\n')) {
  const eq = line.indexOf('=');
  if (eq > 0) env[line.slice(0, eq).trim()] = line.slice(eq + 1).trim();
}

// Use the server's OWN encrypt() function so key derivation matches!
const providers = [
  { platform: 'openrouter', label: 'OpenRouter', key: env.OPENROUTER_API_KEY, base_url: 'https://openrouter.ai/api/v1' },
  { platform: 'anthropic', label: 'Anthropic', key: env.ANTHROPIC_API_KEY, base_url: 'https://api.anthropic.com' },
  { platform: 'google', label: 'Google', key: env.GOOGLE_GENERATIVE_AI_KEY, base_url: 'https://generativelanguage.googleapis.com/v1beta' },
  { platform: 'nvidia', label: 'NVIDIA', key: env.NVIDIA_INFERENCE_KEY, base_url: 'https://integrate.api.nvidia.com/v1' },
];

db.prepare('DELETE FROM api_keys').run();

let added = 0;
for (const p of providers) {
  if (!p.key) { console.log(`Skipping ${p.platform} - no key`); continue; }
  console.log(`Adding ${p.platform}...`);
  const enc = encrypt(p.key);
  db.prepare("INSERT INTO api_keys (platform, label, encrypted_key, iv, auth_tag, status, enabled, base_url) VALUES (?, ?, ?, ?, ?, 'active', 1, ?)")
    .run(p.platform, p.label, enc.encrypted, enc.iv, enc.authTag, p.base_url);
  added++;
}

console.log(`Done. ${added} keys added.`);
