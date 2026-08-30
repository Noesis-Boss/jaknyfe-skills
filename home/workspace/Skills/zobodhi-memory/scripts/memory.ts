#!/usr/bin/env node
import { promises as fs } from 'fs';
import path from 'path';

// Path to JSON storage file
const DB_PATH = path.resolve(process.cwd(), 'memory.json');
const GATES_PATH = path.resolve(process.cwd(), '.gates.json');

const VALID_TYPES = new Set([
  'fact',
  'preference',
  'decision',
  'project',
  'feedback',
  'reference',
  'session',
  'working',
]);
const VALID_STATUS = new Set(['pending', 'verified', 'expired', 'durable', 'superseded']);
const DEFAULT_TYPE = 'fact';
const DEFAULT_STATUS = 'pending';
const STALE_DAYS = 180;

const DEFAULT_GATES = {
  min_confidence: 0.5,
  require_project: true,
  require_type: true,
  blocked_types: ['session'],
  require_source_for: ['decision'],
  max_pending_ratio: 0.3,
  max_stale_days: STALE_DAYS,
};

type Fact = {
  id: number;
  text: string;
  addedAt: string;
  lastSeenAt?: string;
  type?: string;
  status?: string;
  confidence?: number;
  project?: string;
  source?: string;
  tags?: string[];
  supersedes?: number[];
  relations?: { subject: string; predicate: string; object: string }[];
  accessCount?: number;
  expiresAt?: string;
};

type DB = { memories: Fact[] };
type Gates = typeof DEFAULT_GATES;

async function readDB(): Promise<DB> {
  try {
    const raw = await fs.readFile(DB_PATH, 'utf8');
    const parsed = JSON.parse(raw);
    if (!parsed || !Array.isArray(parsed.memories)) return { memories: [] };
    return parsed as DB;
  } catch {
    return { memories: [] };
  }
}

async function writeDB(db: DB) {
  await fs.writeFile(DB_PATH, JSON.stringify(db, null, 2));
}

async function readGates(): Promise<Gates> {
  try {
    const raw = await fs.readFile(GATES_PATH, 'utf8');
    return { ...DEFAULT_GATES, ...JSON.parse(raw) };
  } catch {
    return { ...DEFAULT_GATES };
  }
}

async function writeGates(g: Gates) {
  await fs.writeFile(GATES_PATH, JSON.stringify(g, null, 2));
}

function normalize(text: string): string {
  return text.trim().toLowerCase().replace(/\s+/g, ' ');
}

function fingerprint(text: string): string {
  return normalize(text).slice(0, 200);
}

function parseFlags(args: string[]): Record<string, string | boolean> {
  const out: Record<string, string | boolean> = {};
  for (const a of args) {
    if (!a.startsWith('--')) continue;
    const eq = a.indexOf('=');
    if (eq === -1) out[a.slice(2)] = true;
    else out[a.slice(2, eq)] = a.slice(eq + 1);
  }
  return out;
}

function isLegacyFact(m: any): boolean {
  return m && typeof m.text === 'string' && typeof m.id === 'number';
}

function validateType(type: string): string {
  const t = (type || DEFAULT_TYPE).toLowerCase();
  if (!VALID_TYPES.has(t)) {
    throw new Error(`invalid --type: ${t} (allowed: ${[...VALID_TYPES].join(', ')})`);
  }
  return t;
}

function validateStatus(status: string): string {
  const s = (status || DEFAULT_STATUS).toLowerCase();
  if (!VALID_STATUS.has(s)) {
    throw new Error(`invalid --status: ${s} (allowed: ${[...VALID_STATUS].join(', ')})`);
  }
  return s;
}

function validateConfidence(c: string | undefined): number {
  if (c === undefined) return 1.0;
  const n = Number(c);
  if (Number.isNaN(n) || n < 0 || n > 1) {
    throw new Error(`invalid --confidence: ${c} (expected 0..1)`);
  }
  return n;
}

type GateFailure = { rule: string; detail: string };

function checkAddGates(
  candidate: {
    type: string;
    project?: string;
    confidence: number;
    source?: string;
  },
  gates: Gates
): GateFailure[] {
  const fails: GateFailure[] = [];
  if (gates.require_type && !candidate.type) fails.push({ rule: 'require_type', detail: 'type is required' });
  if (gates.require_project && !candidate.project)
    fails.push({ rule: 'require_project', detail: 'project is required' });
  if (candidate.confidence < gates.min_confidence)
    fails.push({
      rule: 'min_confidence',
      detail: `confidence ${candidate.confidence} < ${gates.min_confidence}`,
    });
  if (gates.blocked_types.includes(candidate.type))
    fails.push({ rule: 'blocked_types', detail: `type ${candidate.type} is blocked` });
  if (
    Array.isArray(gates.require_source_for) &&
    gates.require_source_for.includes(candidate.type) &&
    !candidate.source
  )
    fails.push({
      rule: 'require_source_for',
      detail: `type ${candidate.type} requires --source`,
    });
  return fails;
}

async function addFact(text: string, flags: Record<string, string | boolean>) {
  const fact = (text || '').trim();
  if (!fact) throw new Error('fact text is empty');

  const type = validateType(String(flags.type ?? ''));
  const status = validateStatus(String(flags.status ?? ''));
  const confidence = validateConfidence(
    typeof flags.confidence === 'string' ? flags.confidence : undefined
  );
  const project = typeof flags.project === 'string' ? flags.project.toLowerCase() : undefined;
  const sourceProvided = typeof flags.source === 'string' && flags.source.length > 0;
  const source = sourceProvided ? (flags.source as string) : 'manual';
  const tags = typeof flags.tags === 'string'
    ? flags.tags.split(',').map(t => t.trim()).filter(Boolean)
    : [];

  const gates = await readGates();
  const force = flags.force === true;
  if (!force) {
    const fails = checkAddGates(
      { type, project, confidence, source: sourceProvided ? source : undefined },
      gates
    );
    if (fails.length > 0) {
      console.error('🚫 Gate(s) failed:');
      fails.forEach(f => console.error(`   - [${f.rule}] ${f.detail}`));
      console.error('   Re-run with --force to override.');
      process.exit(2);
    }
  } else {
    console.warn('⚠️  --force set; skipping gate checks.');
  }

  const db = await readDB();
  const fp = fingerprint(fact);
  const dup = db.memories.find(m => fingerprint(m.text) === fp);
  if (dup) {
    dup.lastSeenAt = new Date().toISOString();
    await writeDB(db);
    console.log(`♻️  Duplicate of [#${dup.id}]. Updated lastSeenAt.`);
    return;
  }

  const now = new Date().toISOString();
  db.memories.push({
    id: Date.now(),
    text: fact,
    addedAt: now,
    lastSeenAt: now,
    type,
    status,
    confidence,
    project,
    source,
    tags,
    supersedes: [],
    relations: [],
    accessCount: 1,
  });
  await writeDB(db);
  console.log(
    `✅ Added [${type}/${status}${project ? `/${project}` : ''}] ${fact.slice(0, 60)}${fact.length > 60 ? '…' : ''}`
  );
}

async function queryFact(question: string, flags: Record<string, string | boolean>) {
  const db = await readDB();
  const q = normalize(question);
  let results = db.memories.filter(m => normalize(m.text).includes(q));
  const project = typeof flags.project === 'string' ? flags.project.toLowerCase() : undefined;
  if (project) results = results.filter(m => (m.project || '').toLowerCase() === project);
  if (results.length === 0) {
    console.log('🔎 No matching memories found.');
    return;
  }
  console.log(`🔍 ${results.length} match(es):`);
  results.sort((a, b) => {
    const score = (m: Fact) => (m.confidence ?? 1) * 10 + Math.min(m.accessCount ?? 0, 5) + (m.status === 'durable' || m.status === 'verified' ? 2 : 0);
    return score(b) - score(a);
  });
  results.forEach((m, i) => {
    m.accessCount = (m.accessCount ?? 0) + 1;
    const meta = [
      m.type || 'fact',
      m.status || 'pending',
      m.project ? `#${m.project}` : null,
      m.confidence !== undefined ? `c=${m.confidence}` : null,
    ]
      .filter(Boolean)
      .join(' · ');
    console.log(`  ${i + 1}. [#${m.id} ${meta}] ${m.text}`);
  });
  await writeDB(db);
}

async function listFacts(flags: Record<string, string | boolean>) {
  const db = await readDB();
  const project = typeof flags.project === 'string' ? flags.project.toLowerCase() : undefined;
  let rows = db.memories;
  if (project) rows = rows.filter(m => (m.project || '').toLowerCase() === project);
  if (rows.length === 0) {
    console.log('🗂️  No facts.');
    return;
  }
  console.log(`🗂️  ${rows.length} fact(s):`);
  rows.forEach((m, i) => {
    const meta = [
      m.type || 'fact',
      m.status || 'pending',
      m.project ? `#${m.project}` : null,
    ]
      .filter(Boolean)
      .join(' · ');
    console.log(`  ${i + 1}. [#${m.id} ${meta}] ${m.text.slice(0, 80)}${m.text.length > 80 ? '…' : ''}`);
  });
}

async function clearFacts() {
  await writeDB({ memories: [] });
  console.log('🧹 Memory store cleared.');
}

async function doctorFacts() {
  const db = await readDB();
  const issues: string[] = [];
  const seen = new Map<string, number>();

  let legacyCount = 0;
  let untypedCount = 0;
  let unprojectedCount = 0;
  let pendingCount = 0;
  let staleCount = 0;
  const now = Date.now();

  for (const m of db.memories) {
    if (!isLegacyFact(m)) {
      issues.push(`[#${(m as any).id}] invalid fact shape`);
      continue;
    }
    if (!m.type) {
      untypedCount++;
      issues.push(`[#${m.id}] missing type`);
    } else if (!VALID_TYPES.has(m.type)) {
      issues.push(`[#${m.id}] invalid type: ${m.type}`);
    }
    if (!m.status) {
      pendingCount++;
    } else if (!VALID_STATUS.has(m.status)) {
      issues.push(`[#${m.id}] invalid status: ${m.status}`);
    }
    if (!m.project) unprojectedCount++;
    if (m.addedAt) {
      const ageDays = (now - new Date(m.addedAt).getTime()) / (1000 * 60 * 60 * 24);
      if (ageDays > STALE_DAYS && (!m.lastSeenAt || new Date(m.lastSeenAt).getTime() < now - STALE_DAYS * 86400000)) {
        staleCount++;
      }
    }
    if (!Array.isArray(m.tags)) {
      issues.push(`[#${m.id}] tags must be an array`);
    }
    const fp = fingerprint(m.text);
    if (seen.has(fp)) {
      issues.push(`[#${m.id}] duplicate of [#${seen.get(fp)}]`);
    } else {
      seen.set(fp, m.id);
    }
    const fields = Object.keys(m);
    const modernFields = ['type', 'status', 'project'];
    if (!modernFields.some(f => fields.includes(f))) legacyCount++;
  }

  const total = db.memories.length;
  const projected = total - unprojectedCount;
  const coverage = total === 0 ? 100 : Math.round((projected / total) * 100);

  console.log(`🩺 zobodhi doctor — ${total} fact(s)`);
  console.log(`  typed:        ${total - untypedCount}/${total}`);
  console.log(`  projected:    ${projected}/${total} (${coverage}% coverage)`);
  console.log(`  pending:      ${pendingCount}`);
  console.log(`  stale (>${STALE_DAYS}d): ${staleCount}`);
  console.log(`  legacy shape: ${legacyCount}`);
  if (issues.length === 0) {
    console.log('  ✅ no issues');
  } else {
    console.log(`  ⚠️  ${issues.length} issue(s):`);
    issues.slice(0, 20).forEach(i => console.log(`    - ${i}`));
    if (issues.length > 20) console.log(`    …and ${issues.length - 20} more`);
  }
}

async function gateFacts(): Promise<number> {
  const db = await readDB();
  const gates = await readGates();
  const fails: GateFailure[] = [];
  const total = db.memories.length;

  let typedCount = 0;
  let projectedCount = 0;
  let pendingCount = 0;
  let staleCount = 0;
  let blockedCount = 0;
  let lowConfCount = 0;
  let missingSourceCount = 0;
  const now = Date.now();

  for (const m of db.memories) {
    if (m.type && VALID_TYPES.has(m.type)) typedCount++;
    if (m.project) projectedCount++;
    if (m.status === 'pending' || !m.status) pendingCount++;
    if (gates.blocked_types.includes(m.type || '')) blockedCount++;
    if (typeof m.confidence === 'number' && m.confidence < gates.min_confidence) lowConfCount++;
    if (
      Array.isArray(gates.require_source_for) &&
      gates.require_source_for.includes(m.type || '') &&
      !m.source
    )
      missingSourceCount++;
    if (m.addedAt) {
      const ageDays = (now - new Date(m.addedAt).getTime()) / (1000 * 60 * 60 * 24);
      const lastSeen = m.lastSeenAt ? new Date(m.lastSeenAt).getTime() : 0;
      if (ageDays > gates.max_stale_days && now - lastSeen > gates.max_stale_days * 86400000) {
        staleCount++;
      }
    }
  }

  if (gates.require_type && typedCount < total)
    fails.push({ rule: 'require_type', detail: `${total - typedCount}/${total} facts missing type` });
  if (gates.require_project && projectedCount < total)
    fails.push({
      rule: 'require_project',
      detail: `${total - projectedCount}/${total} facts missing project`,
    });
  if (total > 0) {
    const ratio = pendingCount / total;
    if (ratio > gates.max_pending_ratio)
      fails.push({
        rule: 'max_pending_ratio',
        detail: `pending ratio ${(ratio * 100).toFixed(1)}% > ${(gates.max_pending_ratio * 100).toFixed(1)}%`,
      });
  }
  if (blockedCount > 0)
    fails.push({ rule: 'blocked_types', detail: `${blockedCount} fact(s) use blocked types` });
  if (lowConfCount > 0)
    fails.push({
      rule: 'min_confidence',
      detail: `${lowConfCount} fact(s) below confidence ${gates.min_confidence}`,
    });
  if (missingSourceCount > 0)
    fails.push({
      rule: 'require_source_for',
      detail: `${missingSourceCount} decision(s) missing source`,
    });
  if (staleCount > 0)
    fails.push({
      rule: 'max_stale_days',
      detail: `${staleCount} fact(s) stale (>${gates.max_stale_days}d, never re-seen)`,
    });

  console.log(`🚧 zobodhi gate — ${total} fact(s) · rules from ${path.relative(process.cwd(), GATES_PATH) || '.gates.json'}`);
  console.log(`  typed: ${typedCount}/${total} · projected: ${projectedCount}/${total} · pending: ${pendingCount}`);
  console.log(`  blocked: ${blockedCount} · low-conf: ${lowConfCount} · missing-source: ${missingSourceCount} · stale: ${staleCount}`);
  if (fails.length === 0) {
    console.log('  ✅ all gates passed');
    return 0;
  }
  console.log(`  ❌ ${fails.length} gate failure(s):`);
  fails.forEach(f => console.log(`    - [${f.rule}] ${f.detail}`));
  return 1;
}

async function initGates(flags: Record<string, string | boolean>) {
  const force = flags.force === true;
  try {
    await fs.access(GATES_PATH);
    if (!force) {
      console.log(`⚠️  ${path.basename(GATES_PATH)} already exists. Use --force to overwrite.`);
      return;
    }
  } catch {
    // missing — proceed
  }
  await writeGates(DEFAULT_GATES);
  console.log(`🛠️  Wrote ${path.basename(GATES_PATH)} with defaults:`);
  console.log(JSON.stringify(DEFAULT_GATES, null, 2));
}

async function writeState() {
  const db = await readDB();
  const gates = await readGates();
  const total = db.memories.length;
  const byType: Record<string, number> = {};
  const byProject: Record<string, number> = {};
  const byStatus: Record<string, number> = {};
  let untyped = 0, unprojected = 0, stale = 0;
  const now = Date.now();
  for (const m of db.memories) {
    const t = m.type || 'unknown';
    byType[t] = (byType[t] || 0) + 1;
    if (!m.type) untyped++;
    const p = m.project || 'unknown';
    byProject[p] = (byProject[p] || 0) + 1;
    if (!m.project) unprojected++;
    const s = m.status || 'pending';
    byStatus[s] = (byStatus[s] || 0) + 1;
    if (m.addedAt) {
      const ageDays = (now - new Date(m.addedAt).getTime()) / 86400000;
      if (ageDays > gates.max_stale_days && (!m.lastSeenAt || new Date(m.lastSeenAt).getTime() < now - gates.max_stale_days * 86400000)) stale++;
    }
  }
  const recent = [...db.memories]
    .sort((a, b) => (b.addedAt || '').localeCompare(a.addedAt || ''))
    .slice(0, 5);

  const lines: string[] = [];
  lines.push('# zobodhi STATE');
  lines.push('');
  lines.push(`_Generated: ${new Date().toISOString()}_`);
  lines.push('');
  lines.push('## Counts');
  lines.push(`- total: **${total}**`);
  lines.push(`- typed: ${total - untyped}/${total} · projected: ${total - unprojected}/${total} · stale: ${stale}`);
  lines.push('');
  lines.push('## By type');
  for (const [k, v] of Object.entries(byType).sort((a, b) => b[1] - a[1])) lines.push(`- ${k}: ${v}`);
  lines.push('');
  lines.push('## By project');
  for (const [k, v] of Object.entries(byProject).sort((a, b) => b[1] - a[1])) lines.push(`- ${k}: ${v}`);
  lines.push('');
  lines.push('## By status');
  for (const [k, v] of Object.entries(byStatus).sort((a, b) => b[1] - a[1])) lines.push(`- ${k}: ${v}`);
  lines.push('');
  lines.push('## Recent (last 5)');
  for (const m of recent) lines.push(`- [#${m.id}] ${m.type || '?'}/${m.status || '?'}/${m.project || '?'} — ${m.text.slice(0, 80)}…`);
  lines.push('');
  lines.push('## Gates');
  lines.push('```json');
  lines.push(JSON.stringify(gates, null, 2));
  lines.push('```');

  const out = path.resolve(process.cwd(), 'STATE.md');
  await fs.writeFile(out, lines.join('\n') + '\n');
  console.log(`📝 Wrote ${out} (${total} facts).`);
}

function printUsage() {
  console.log(`Usage: memory.ts <command> [args] [flags]

Commands:
  --add "<text>"       Add a fact. Flags: --type= --status= --project= --tags=a,b --confidence=0..1 --source= --force
  --query "<text>"     Search facts. Flags: --project=
  --list               List facts. Flags: --project=
  --doctor             Run health checks (duplicates, stale, missing types/projects)
  --gate               Run project gates against the whole store. Exit 1 on failure.
  --init-gates         Write .gates.json with defaults (--force to overwrite)
  --state              Write STATE.md snapshot (counts, recent facts, top projects, gate status)
  --clear              Reset the store

Types:    ${[...VALID_TYPES].join(', ')}
Statuses: ${[...VALID_STATUS].join(', ')}

Gates (.gates.json):
  min_confidence        reject facts below this confidence (default 0.5)
  require_project       require --project on every add (default true)
  require_type          require --type on every add (default true)
  blocked_types         list of types that fail the gate (default ["session"])
  require_source_for    types that must include --source (default ["decision"])
  max_pending_ratio     fail if pending/total exceeds this (default 0.3)
  max_stale_days        fail if fact older & not re-seen (default 180)`);
}

const args = process.argv.slice(2);
const command = args[0];
const rest = args.slice(1);
const flags = parseFlags(rest);

if (!command) {
  printUsage();
} else {
  switch (command) {
    case '--add':
      addFact(rest.filter(a => !a.startsWith('--')).join(' '), flags).catch(e => {
        console.error(`❌ ${e.message}`);
        process.exit(1);
      });
      break;
    case '--query':
      queryFact(rest.filter(a => !a.startsWith('--')).join(' '), flags);
      break;
    case '--list':
      listFacts(flags);
      break;
    case '--doctor':
      doctorFacts().catch(e => {
        console.error(`❌ ${e.message}`);
        process.exit(1);
      });
      break;
    case '--gate': {
      const code = await gateFacts();
      process.exit(code);
      break;
    }
    case '--init-gates':
      initGates(flags).catch(e => {
        console.error(`❌ ${e.message}`);
        process.exit(1);
      });
      break;
    case '--state':
      writeState().catch(e => {
        console.error(`❌ ${e.message}`);
        process.exit(1);
      });
      break;
    case '--clear':
      clearFacts();
      break;
    case '--help':
    case '-h':
      printUsage();
      break;
    default:
      console.log('Unknown command. Use --add, --query, --list, --doctor, --gate, --init-gates, --state, or --clear');
  }
}
