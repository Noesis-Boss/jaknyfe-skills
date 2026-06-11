#!/usr/bin/env node
import { promises as fs } from 'fs';
import path from 'path';

const DB_PATH = path.resolve(process.cwd(), 'memory.json');

async function loadDB() {
  try {
    const raw = await fs.readFile(DB_PATH, 'utf8');
    return JSON.parse(raw);
  } catch {
    return { memories: [] };
  }
}

async function find(question: string) {
  const db = await loadDB();
  const ql = question.toLowerCase();
  const matches = db.memories.filter(m => m.text.toLowerCase().includes(ql));
  if (!matches.length) return '🔎 No matching memory found.';
  // newest match wins
  const latest = matches.sort((a, b) => (b.addedAt > a.addedAt ? 1 : -1))[0];
  return latest.text;
}

async function autoRecall() {
  const db = await loadDB();
  if (!db.memories.length) return;
  // show last 3 stored facts
  const last3 = db.memories.slice(-3).reverse();
  console.log('🧠 Recent context from memory:');
  last3.forEach((m, i) => console.log(`  ${i + 1}. ${m.text.substring(0, 90)}`));
}

const query = process.argv.slice(2).join(' ');
if (!query) {
  // no args → run auto-recall
  autoRecall();
} else {
  find(query).then(console.log).catch(console.error);
}