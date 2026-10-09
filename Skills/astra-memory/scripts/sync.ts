#!/usr/bin/env node
/**
 * AstraDB Memory Sync & Query
 *
 * Mirrors zobodhi-memory (JSON) and Clarion (markdown tree) into the
 * AstraDB `memories` collection. Idempotent upserts.
 *
 * Usage:
 *   bun run sync.ts sync [--source=zobodhi|clarion]
 *   bun run sync.ts status
 *   bun run sync.ts query <text> [--source=...]
 *   bun run sync.ts add <fact>
 *   bun run sync.ts tail [n]
 */

import { promises as fs } from "fs";
import { createHash } from "node:crypto";
import path from "path";
import { spawnSync } from "child_process";

const ASTRA_ENDPOINT = process.env.ASTRA_DB_ENDPOINT?.replace(/\/$/, "");
const ASTRA_TOKEN = process.env.ASTRA_DB_APPLICATION_TOKEN;
const ASTRA_KEYSPACE = process.env.ASTRA_DB_KEYSPACE || "default_keyspace";
const COLLECTION = "memories";

const ZOBODHI_JSON = "/home/workspace/Skills/zobodhi-memory/memory.json";
const CLARION_ROOT = "/home/workspace/memory";

// ---------- Astra client ----------

interface AstraResponse {
  data?: { documents?: any[]; nextPageState?: string | null };
  status?: { count?: number; ok?: number };
  errors?: { title: string; message: string }[];
}

async function astra(
  method: "POST" | "GET" | "DELETE",
  body?: any
): Promise<any> {
  if (!ASTRA_ENDPOINT || !ASTRA_TOKEN) {
    throw new Error(
      "Missing ASTRA_DB_ENDPOINT or ASTRA_DB_APPLICATION_TOKEN env vars. Set them in Settings > Advanced."
    );
  }
  const url = `${ASTRA_ENDPOINT}/api/json/v1/${ASTRA_KEYSPACE}/${COLLECTION}`;
  const res = await fetch(url, {
    method,
    headers: {
      Token: ASTRA_TOKEN,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const json = (await res.json()) as AstraResponse;
  if (json.errors && json.errors.length > 0) {
    const msg = json.errors.map((e) => `${e.title}: ${e.message}`).join("; ");
    throw new Error(`Astra error — ${msg}`);
  }
  if (!res.ok) throw new Error(`Astra HTTP ${res.status}`);
  return json;
}

export function findPageRequest(
  filter: Record<string, any>,
  pageState: string | null,
  projection?: Record<string, number>
) {
  return {
    find: {
      filter,
      ...(projection ? { projection } : {}),
      options: pageState ? { pageState } : {},
    },
  };
}

export function chunked<T>(values: T[], size: number): T[][] {
  if (!Number.isInteger(size) || size < 1) throw new Error("Chunk size must be a positive integer");
  const chunks: T[][] = [];
  for (let i = 0; i < values.length; i += size) chunks.push(values.slice(i, i + size));
  return chunks;
}

async function findAll(
  filter: Record<string, any> = {},
  projection?: Record<string, number>
): Promise<any[]> {
  const all: any[] = [];
  let pageState: string | null = null;
  for (let i = 0; i < 200; i++) {
    const body = findPageRequest(filter, pageState, projection);
    const r = await astra("POST", body);
    const docs = r.data?.documents ?? [];
    all.push(...docs);
    pageState = r.data?.nextPageState ?? null;
    if (!pageState || docs.length === 0) break;
  }
  if (pageState) throw new Error("Astra scan exceeded 200 pages; refusing incomplete sync reconciliation");
  return all;
}

// ---------- Source readers ----------

interface ZobodhiFact {
  id: number;
  text: string;
  addedAt: string;
  tags: string[];
}

async function readZobodhi(): Promise<ZobodhiFact[]> {
  const raw = await fs.readFile(ZOBODHI_JSON, "utf8");
  const db = JSON.parse(raw);
  if (!Array.isArray(db.memories)) {
    throw new Error("zobodhi memory.json has no memories array");
  }
  return db.memories;
}

function frontmatter(text: string): Record<string, string> {
  const m = text.match(/^---\n([\s\S]+?)\n---\n/);
  if (!m?.[1]) return {};
  const fm: Record<string, string> = {};
  for (const line of m[1].split("\n")) {
    const kv = line.match(/^(\w[\w_-]*):\s*(.+?)\s*$/);
    const key = kv?.[1];
    const value = kv?.[2];
    if (key && value) fm[key] = value.replace(/^['"]|['"]$/g, "");
  }
  return fm;
}

function firstHeading(text: string): string {
  const m = text.match(/^#\s+(.+)$/m);
  if (m?.[1]) return m[1].trim();
  return text.replace(/\s+/g, " ").slice(0, 80).trim();
}

function inferProject(filePath: string, fm: Record<string, string>): string {
  if (fm.project) return fm.project.toLowerCase();
  if (filePath.includes("/projects/")) {
    const m = filePath.match(/\/projects\/([^/]+)\.md/);
    if (m?.[1]) return m[1].toLowerCase();
  }
  if (filePath.includes("/daily/")) return "daily";
  if (filePath.includes("/feedback/")) return "feedback";
  return "system";
}

function inferLayer(filePath: string, fm: Record<string, string>): string {
  if (fm.type) {
    const t = fm.type.toLowerCase();
    if (t.includes("project")) return "semantic";
    if (t.includes("feedback")) return "fact";
    if (t.includes("reference")) return "semantic";
  }
  if (filePath.includes("/daily/")) return "session";
  if (filePath.includes("/projects/") || filePath.includes("/reference/"))
    return "semantic";
  if (filePath.includes("/feedback/")) return "fact";
  return "fact";
}

async function walkMarkdown(root: string): Promise<string[]> {
  const out: string[] = [];
  async function walk(dir: string) {
    const entries = await fs.readdir(dir, { withFileTypes: true });
    for (const e of entries) {
      const p = path.join(dir, e.name);
      if (e.isDirectory()) await walk(p);
      else if (e.isFile() && e.name.endsWith(".md") && !e.name.startsWith("_"))
        out.push(p);
    }
  }
  await walk(root);
  return out;
}

export interface ClarionDoc {
  source: string;
  source_id: string;
  dedupe_key: string;
  layer: string;
  text: string;
  path: string;
  timestamp: string;
  tags: string[];
  project: string;
  title: string;
  $vector?: number[];
}

// ---------- Embeddings (delegate to embed.ts subprocess) ----------

function embed(kind: "query" | "doc", text: string): number[] {
  const sub = spawnSync("bun", ["run", new URL("./embed.ts", import.meta.url).pathname, `embed-${kind}`, text], {
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024,
  });
  if (sub.status !== 0) {
    throw new Error(`embed failed: ${sub.stderr || sub.stdout}`);
  }
  const out = (sub.stdout || "").trim();
  const lines = out.split("\n").filter((l) => l.startsWith("["));
  const vectorLine = lines[0];
  if (!vectorLine) throw new Error(`embed: no vector in output — ${out.slice(0, 200)}`);
  return JSON.parse(vectorLine) as number[];
}

function embedDoc(text: string): number[] {
  return embed("doc", text);
}

async function readClarion(): Promise<ClarionDoc[]> {
  const files = await walkMarkdown(CLARION_ROOT);
  const out: ClarionDoc[] = [];
  for (const f of files) {
    const rel = f.replace("/home/workspace/memory/", "");
    const source = rel.startsWith("daily/")
      ? "clarion_daily"
      : rel.startsWith("projects/")
        ? "clarion_project"
        : rel.startsWith("feedback/")
          ? "clarion_feedback"
          : rel.startsWith("reference/")
            ? "clarion_reference"
            : rel.startsWith("projects/") || rel.endsWith("-topics.md")
              ? "clarion_topics"
              : "clarion_bootstrap";
    const sourceId = `clarion:${rel.split(path.sep).join("/")}`;

    try {
      const text = await fs.readFile(f, "utf8");
      const fm = frontmatter(text);
      const stat = await fs.stat(f);
      out.push({
        source,
        source_id: sourceId,
        dedupe_key: sourceId,
        layer: inferLayer(f, fm),
        text: text.trim().slice(0, 7800),
        path: f,
        timestamp:
          fm.date || stat.mtime.toISOString().slice(0, 19) + "Z",
        tags: fm.tags
          ? fm.tags
              .replace(/^\[|\]$/g, "")
              .split(",")
              .map((t) => t.trim())
          : [],
        project: inferProject(f, fm),
        title: fm.name || firstHeading(text),
      });
    } catch (e) {
      throw new Error(`Could not read ${f}: ${e}`);
    }
  }
  return out;
}

// ---------- Sync logic ----------

export function normalizedTextHash(text: string): string {
  const normalized = text.normalize("NFKC").toLowerCase().replace(/\s+/g, " ").trim();
  return createHash("sha256").update(normalized).digest("hex");
}

export function stableDocId(sourceId: string): string {
  return `memory-${createHash("sha256").update(sourceId).digest("hex")}`;
}

export function dedupeKeyForDoc(doc: Record<string, any>): string {
  if (typeof doc.dedupe_key === "string" && doc.dedupe_key) return doc.dedupe_key;
  const source = typeof doc.source === "string" ? doc.source : "unknown";
  const text = typeof doc.text === "string" ? doc.text : "";
  const sourcePath = typeof doc.path === "string" ? doc.path : "";
  if (source === "zobodhi") return `zobodhi:${normalizedTextHash(text)}`;
  if (source.startsWith("clarion_") && sourcePath.startsWith(`${CLARION_ROOT}/`)) {
    return `clarion:${path.relative(CLARION_ROOT, sourcePath).split(path.sep).join("/")}`;
  }
  return `${source}:${sourcePath}:${normalizedTextHash(text)}`;
}

export function contentHash(doc: ClarionDoc): string {
  return createHash("sha256").update(JSON.stringify({
    source: doc.source,
    source_id: doc.source_id,
    dedupe_key: doc.dedupe_key,
    layer: doc.layer,
    text: doc.text,
    path: doc.path,
    timestamp: doc.timestamp,
    tags: doc.tags,
    project: doc.project,
    title: doc.title,
  })).digest("hex");
}

export function dedupeInputDocs(docs: ClarionDoc[]): ClarionDoc[] {
  const bySourceId = new Map<string, ClarionDoc>();
  for (const doc of docs) {
    if (!doc.source_id?.trim()) throw new Error(`Missing stable source_id for ${doc.source}`);
    const previous = bySourceId.get(doc.source_id);
    if (!previous || (doc.timestamp || "").localeCompare(previous.timestamp || "") >= 0) {
      bySourceId.set(doc.source_id, doc);
    }
  }
  return [...bySourceId.values()];
}

export function dedupeRanked<T extends { doc: Record<string, any>; score: number }>(items: T[]): T[] {
  const bestByKey = new Map<string, T>();
  for (const item of items) {
    const key = dedupeKeyForDoc(item.doc);
    const previous = bestByKey.get(key);
    if (!previous || item.score > previous.score) bestByKey.set(key, item);
  }
  return [...bestByKey.values()].sort((a, b) => b.score - a.score);
}

export function staleDocsToDeactivate(
  existing: Record<string, any>[],
  currentIds: Set<string>,
  reconcileSources: string[]
): Record<string, any>[] {
  return existing.filter((doc) =>
    typeof doc._id === "string" &&
    reconcileSources.includes(doc.source) &&
    !currentIds.has(doc._id) &&
    doc.active !== false
  );
}

export function mergeDocsById(...groups: Record<string, any>[][]): Map<string, any> {
  const byId = new Map<string, any>();
  for (const group of groups) {
    for (const doc of group) {
      if (typeof doc._id === "string" && !byId.has(doc._id)) byId.set(doc._id, doc);
    }
  }
  return byId;
}

function buildZobodhiDocs(facts: ZobodhiFact[]): ClarionDoc[] {
  return facts.map((f) => {
    const sourceId = `zobodhi:${f.id}`;
    return {
      source: "zobodhi",
      source_id: sourceId,
      dedupe_key: `zobodhi:${normalizedTextHash(f.text)}`,
      layer: "fact",
      text: f.text,
      path: ZOBODHI_JSON,
      timestamp: f.addedAt,
      tags: f.tags || [],
      project: "general",
      title: f.text.replace(/\s+/g, " ").slice(0, 80),
    };
  });
}

interface SyncCounts {
  inserted: number;
  updated: number;
  skipped: number;
  deactivated: number;
}

async function upsertAll(docs: ClarionDoc[], reconcileSources: string[] = []): Promise<SyncCounts> {
  const prepared = dedupeInputDocs(docs);
  const currentIds = new Set(prepared.map((doc) => stableDocId(doc.source_id)));
  const existingCurrent = (
    await Promise.all(
      chunked([...currentIds], 100).map((ids) =>
        findAll({ _id: { $in: ids } }, { _id: 1, content_hash: 1, text_hash: 1, active: 1 })
      )
    )
  ).flat();
  const existingForReconciliation = reconcileSources.length
    ? await findAll(
        { source: { $in: reconcileSources }, source_id: { $exists: true }, active: true },
        { _id: 1, source: 1, source_id: 1, active: 1 }
      )
    : [];
  const existingById = mergeDocsById(existingCurrent, existingForReconciliation);
  let inserted = 0;
  let updated = 0;
  let skipped = docs.length - prepared.length;

  for (const doc of prepared) {
    const id = stableDocId(doc.source_id);
    const previous = existingById.get(id);
    const nextContentHash = contentHash(doc);
    const nextTextHash = createHash("sha256").update(doc.text).digest("hex");
    if (previous?.content_hash === nextContentHash && previous.active !== false) {
      skipped++;
      continue;
    }

    const fields: Record<string, any> = {
      ...doc,
      content_hash: nextContentHash,
      text_hash: nextTextHash,
      active: true,
    };
    if (!previous || previous.text_hash !== nextTextHash) fields.$vector = embedDoc(doc.text);

    await astra("POST", {
      updateOne: {
        filter: { _id: id },
        update: { $set: fields, $unset: { retired_at: "" } },
        options: { upsert: true },
      },
    });
    if (previous) updated++;
    else inserted++;
  }

  let deactivated = 0;
  const retiredAt = new Date().toISOString();
  for (const doc of staleDocsToDeactivate(existingForReconciliation, currentIds, reconcileSources)) {
    await astra("POST", {
      updateOne: {
        filter: { _id: doc._id },
        update: { $set: { active: false, retired_at: retiredAt } },
      },
    });
    deactivated++;
  }

  return { inserted, updated, skipped, deactivated };
}

async function cmdSync(args: string[]) {
  const sourceArg = args
    .find((a) => a.startsWith("--source="))
    ?.split("=")[1];
  if (sourceArg && !["zobodhi", "clarion"].includes(sourceArg)) {
    throw new Error(`Unsupported source: ${sourceArg}`);
  }

  console.log("📥 Reading sources...");
  const docs: ClarionDoc[] = [];
  const reconcileSources: string[] = [];
  if (!sourceArg || sourceArg === "zobodhi") {
    const facts = await readZobodhi();
    console.log(`  zobodhi:  ${facts.length} facts`);
    docs.push(...buildZobodhiDocs(facts));
    reconcileSources.push("zobodhi");
  }
  if (!sourceArg || sourceArg === "clarion") {
    const clarion = await readClarion();
    console.log(`  clarion:  ${clarion.length} markdown docs`);
    docs.push(...clarion);
    reconcileSources.push(
      "clarion_daily",
      "clarion_project",
      "clarion_feedback",
      "clarion_reference",
      "clarion_topics",
      "clarion_bootstrap"
    );
  }

  console.log(`☁️  Syncing ${docs.length} source records into Astra...`);
  const counts = await upsertAll(docs, reconcileSources);
  console.log(`✅ Done. inserted=${counts.inserted}, updated=${counts.updated}, skipped=${counts.skipped}, deactivated=${counts.deactivated}`);
  const tsFile = path.join(path.dirname(new URL(import.meta.url).pathname), "last-sync.json");
  await fs.writeFile(
    tsFile,
    JSON.stringify({ lastSync: new Date().toISOString(), ...counts })
  );
}

async function cmdStatus() {
  const all = await findAll({ active: true }, { _id: 1, source: 1, layer: 1 });
  const bySource: Record<string, number> = {};
  const byLayer: Record<string, number> = {};
  for (const d of all) {
    bySource[d.source] = (bySource[d.source] || 0) + 1;
    byLayer[d.layer] = (byLayer[d.layer] || 0) + 1;
  }
  console.log(`📊 Total memories in Astra: ${all.length}`);
  console.log("\nBy source:");
  for (const [k, v] of Object.entries(bySource).sort((a, b) => b[1] - a[1]))
    console.log(`  ${k.padEnd(25)} ${v}`);
  console.log("\nBy layer:");
  for (const [k, v] of Object.entries(byLayer).sort((a, b) => b[1] - a[1]))
    console.log(`  ${k.padEnd(25)} ${v}`);
  try {
    const tsFile = path.join(
      path.dirname(new URL(import.meta.url).pathname),
      "last-sync.json"
    );
    const ts = JSON.parse(await fs.readFile(tsFile, "utf8"));
    console.log(`\nLast sync: ${ts.lastSync}`);
    console.log(`  inserted=${ts.inserted}, updated=${ts.updated || 0}, skipped=${ts.skipped}, deactivated=${ts.deactivated || 0}`);
  } catch {}
}

async function cmdQuery(args: string[]) {
  const sourceArg = args
    .find((a) => a.startsWith("--source="))
    ?.split("=")[1];
  const text = args.filter((a) => !a.startsWith("--")).join(" ").trim();
  if (!text) {
    console.log("Usage: query <text> [--source=zobodhi|clarion] [--limit=10]");
    return;
  }
  const limit = parseInt(
    args.find((a) => a.startsWith("--limit="))?.split("=")[1] || "10",
    10
  );

  console.log(`🔎 Hybrid search (semantic + lexical) for: "${text}"`);
  const queryVec = embed("query", text);

  // Vector ANN
  const vectorFind = await astra("POST", {
    find: {
      filter: { active: true },
      projection: { _id: 1, source_id: 1, dedupe_key: 1, source: 1, layer: 1, project: 1, title: 1, path: 1, timestamp: 1, text: 1, active: 1 },
      sort: { $vector: queryVec },
      options: { limit: limit * 3 },
    },
  });
  const vectorDocs: any[] = vectorFind.data?.documents ?? [];

  // Lexical (substring fallback against full corpus)
  const all = await findAll(
    { active: true },
    { _id: 1, source_id: 1, dedupe_key: 1, source: 1, layer: 1, project: 1, title: 1, path: 1, timestamp: 1, text: 1, active: 1 }
  );
  const q = text.toLowerCase();
  const lexical: { id: string; doc: any; score: number }[] = [];
  for (const d of all) {
    const t = (d.text || "").toLowerCase();
    const title = (d.title || "").toLowerCase();
    let score = 0;
    if (title.includes(q)) score += 10;
    let idx = 0;
    while ((idx = t.indexOf(q, idx)) !== -1) {
      score += 1;
      idx += q.length;
    }
    if (score > 0) lexical.push({ id: d._id, doc: d, score });
  }
  lexical.sort((a, b) => b.score - a.score);

  // RRF fusion
  const rrf = new Map<string, number>();
  const docs = new Map<string, any>();
  const k = 60;
  vectorDocs.forEach((d, i) => {
    rrf.set(d._id, (rrf.get(d._id) ?? 0) + 1 / (k + i + 1));
    docs.set(d._id, d);
  });
  lexical.slice(0, limit * 3).forEach((r, i) => {
    rrf.set(r.id, (rrf.get(r.id) ?? 0) + 1 / (k + i + 1));
    if (!docs.has(r.id)) docs.set(r.id, r.doc);
  });

  // Source filter
  let ranked = [...rrf.entries()]
    .map(([id, score]) => ({ id, score, doc: docs.get(id) }))
    .sort((a, b) => b.score - a.score);
  if (sourceArg) {
    const map: Record<string, string> = {
      zobodhi: "zobodhi",
      daily: "clarion_daily",
      project: "clarion_project",
      feedback: "clarion_feedback",
      reference: "clarion_reference",
      topics: "clarion_topics",
      bootstrap: "clarion_bootstrap",
    };
    const want = map[sourceArg] || sourceArg;
    ranked = ranked.filter((r) => r.doc?.source === want);
  }

  ranked = dedupeRanked(ranked.filter((r) => r.doc?.active === true));
  const top = ranked.slice(0, limit);
  if (top.length === 0) {
    console.log("🔍 No matching memories found.");
    return;
  }

  const jsonMode = args.includes("--json");
  if (jsonMode) {
    const out = {
      query: text,
      embedding: { model: "nomic-embed-text-v1.5", dim: queryVec.length },
      hybrid: { semantic: vectorDocs.length, lexical: lexical.length, k: 60 },
      results: top.map(({ doc: d, score }) => {
        const idx = (d.text || "").toLowerCase().indexOf(q);
        const snippet =
          idx >= 0
            ? d.text
                .slice(Math.max(0, idx - 60), Math.min(d.text.length, idx + 160))
                .replace(/\n+/g, " ")
            : (d.text || "").replace(/\n+/g, " ").slice(0, 160);
        return {
          source: d.source,
          layer: d.layer,
          project: d.project,
          title: d.title,
          path: d.path,
          timestamp: d.timestamp,
          rrf: +score.toFixed(6),
          snippet,
        };
      }),
    };
    console.log(JSON.stringify(out, null, 2));
    return;
  }

  console.log(`\n📌 Top ${top.length} matches (RRF fusion):\n`);
  for (const { doc: d, score } of top) {
    console.log(`  [${d.source} | ${d.layer} | rrf=${score.toFixed(4)}] ${d.title}`);
    console.log(`    ${d.path}`);
    console.log(`    ${d.timestamp}`);
    const idx = (d.text || "").toLowerCase().indexOf(q);
    if (idx >= 0) {
      const start = Math.max(0, idx - 60);
      const end = Math.min(d.text.length, idx + 160);
      console.log(`    …${d.text.slice(start, end).replace(/\n+/g, " ")}…`);
    }
    console.log();
  }
}

async function cmdAdd(args: string[]) {
  const text = args.join(" ").trim();
  if (!text) {
    console.log("Usage: add <fact text>");
    return;
  }
  const fact: ZobodhiFact = {
    id: Date.now(),
    text,
    addedAt: new Date().toISOString(),
    tags: [],
  };
  const db = JSON.parse(await fs.readFile(ZOBODHI_JSON, "utf8"));
  if (!Array.isArray(db.memories)) throw new Error("zobodhi memory.json has no memories array");
  db.memories.push(fact);
  await fs.writeFile(ZOBODHI_JSON, JSON.stringify(db, null, 2));
  console.log("✅ Wrote to zobodhi memory.json");

  const doc = buildZobodhiDocs([fact])[0];
  if (!doc) throw new Error("Could not create Astra document for the new fact");
  const counts = await upsertAll([doc]);
  console.log(`☁️  Astra mirror: inserted=${counts.inserted}, updated=${counts.updated}, skipped=${counts.skipped}`);
}

async function cmdTail(args: string[]) {
  const n = Math.max(1, parseInt(args[0] || "10", 10));
  const all = await findAll({ active: true }, { _id: 1, source: 1, title: 1, timestamp: 1, text: 1 });
  const sorted = all
    .sort((a, b) => (b.timestamp || "").localeCompare(a.timestamp || ""))
    .slice(0, n);
  console.log(`🕓 Most recent ${sorted.length}:\n`);
  for (const d of sorted) {
    console.log(`  [${d.timestamp?.slice(0, 19) || "?"}] ${d.source} / ${d.title}`);
    console.log(`    ${(d.text || "").replace(/\n+/g, " ").slice(0, 140)}…`);
    console.log();
  }
}

// ---------- Main ----------

if (import.meta.main) {
  const [, , cmd, ...rest] = process.argv;
  void (async () => {
    try {
      switch (cmd) {
        case "sync":
          await cmdSync(rest);
          break;
        case "status":
          await cmdStatus();
          break;
        case "query":
          await cmdQuery(rest);
          break;
        case "add":
          await cmdAdd(rest);
          break;
        case "tail":
          await cmdTail(rest);
          break;
        default:
          console.log("Usage: sync | status | query <text> | add <fact> | tail [n]");
      }
    } catch (e: any) {
      console.error(`❌ ${e.message}`);
      process.exit(1);
    }
  })();
}
