import { initDb, getDb } from './dist/db/index.js';
import crypto from 'crypto';

initDb();
const db = getDb();

// Read keys from .env
import { readFileSync } from 'fs';
const envContent = readFileSync(new URL('./.env', import.meta.url), 'utf8');
const env = {};
for (const line of envContent.split('\n')) {
  const [key, ...rest] = line.split('=');
  if (key && rest.length) env[key.trim()] = rest.join('=').trim();
}

const ENCRYPTION_KEY = env.ENCRYPTION_KEY;
if (!ENCRYPTION_KEY) { console.error('No ENCRYPTION_KEY in .env'); process.exit(1); }

function encrypt(text) {
  const iv = crypto.randomBytes(16);
  const key = Buffer.from(ENCRYPTION_KEY, 'hex');
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  let encrypted = cipher.update(text, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  const authTag = cipher.getAuthTag();
  return {
    encrypted_key: encrypted,
    iv: iv.toString('hex'),
    auth_tag: authTag.toString('hex')
  };
}

const providers = [
  { platform: 'openrouter', label: 'OpenRouter', key: env.OPENROUTER_API_KEY, base_url: 'https://openrouter.ai/api/v1' },
  { platform: 'anthropic', label: 'Anthropic', key: env.ANTHROPIC_API_KEY, base_url: 'https://api.anthropic.com' },
  { platform: 'google', label: 'Google', key: env.GOOGLE_GENERATIVE_AI_KEY, base_url: 'https://generativelanguage.googleapis.com/v1beta' },
  { platform: 'nvidia', label: 'NVIDIA', key: env.NVIDIA_INFERENCE_KEY, base_url: 'https://integrate.api.nvidia.com/v1' },
];

let added = 0;
for (const p of providers) {
  if (!p.key) { console.log(`Skipping ${p.platform} - no key`); continue; }
  
  // Check if already exists
  const existing = db.prepare("SELECT id FROM api_keys WHERE platform = ? AND status = 'active'").get(p.platform);
  if (existing) {
    console.log(`${p.platform} already exists (id=${existing.id}), updating...`);
    const enc = encrypt(p.key);
    db.prepare("UPDATE api_keys SET encrypted_key = ?, iv = ?, auth_tag = ?, label = ?, base_url = ?, enabled = 1, status = 'active' WHERE platform = ?")
      .run(enc.encrypted_key, enc.iv, enc.auth_tag, p.label, p.base_url, p.platform);
    added++;
  } else {
    console.log(`Adding ${p.platform}...`);
    const enc = encrypt(p.key);
    db.prepare("INSERT INTO api_keys (platform, label, encrypted_key, iv, auth_tag, status, enabled, base_url) VALUES (?, ?, ?, ?, ?, 'active', 1, ?)")
      .run(p.platform, p.label, enc.encrypted_key, enc.iv, enc.auth_tag, p.base_url);
    added++;
  }
}

console.log(`Done. ${added} keys added/updated.`);
