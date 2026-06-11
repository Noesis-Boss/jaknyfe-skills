#!/usr/bin/env node
import { promises as fs } from 'fs';
import path from 'path';

// Path to JSON storage file
const DB_PATH = path.resolve(process.cwd(), 'memory.json');

// Helper to read DB
async function readDB() {
  try {
    const raw = await fs.readFile(DB_PATH, 'utf8');
    return JSON.parse(raw);
  } catch {
    // If file doesn't exist or is invalid, start with empty object
    return { memories: [] };
  }
}

// Helper to write DB
async function writeDB(db: { memories: any[] }) {
  await fs.writeFile(DB_PATH, JSON.stringify(db, null, 2));
}

// Command handlers
async function addFact(fact: string) {
  const db = await readDB();
  db.memories.push({
    id: Date.now(),
    text: fact,
    addedAt: new Date().toISOString(),
    tags: [],
  });
  await writeDB(db);
  console.log('✅ Fact added to memory store.');
}

async function queryFact(question: string) {
  const db = await readDB();
  const results = db.memories.filter(m => m.text.toLowerCase().includes(question.toLowerCase()));
  if (results.length > 0) {
    console.log('🔍 Findings:');
    results.forEach((m, i) => console.log(`  ${i + 1}. ${m.text}`));
  } else {
    console.log('🔎 No matching memories found.');
  }
}

async function listFacts() {
  const db = await readDB();
  console.log('🗂️  All stored memories:');
  db.memories.forEach((m, i) => console.log(`  ${i + 1}. [${m.id}] ${m.text.substring(0, 80)}...`));
}

async function clearFacts() {
  await writeDB({ memories: [] });
  console.log('🧹 Memory store cleared.');
}

// CLI parsing
const args = process.argv.slice(2);
const command = args[0];

if (!command) {
  console.log('Usage: memory.ts <command> [args]\nCommands: add, query, list, clear');
} else {
  switch (command) {
    case '--add':
      addFact(args.slice(1).join(' '));
      break;
    case '--query':
      queryFact(args.slice(1).join(' '));
      break;
    case '--list':
      listFacts();
      break;
    case '--clear':
      clearFacts();
      break;
    default:
      console.log('Unknown command. Use --add, --query, --list, or --clear');
  }
}