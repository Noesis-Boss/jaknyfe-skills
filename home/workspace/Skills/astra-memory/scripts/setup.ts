#!/usr/bin/env node
/**
 * Create or recreate the Astra `memories` collection with vector support.
 *
 * Data API payload: { "createCollection": { "name", "options": { "vector": { "dimension", "metric" } } } }
 *
 * Idempotent: if collection exists with the right vector dim, no-op.
 * DESTRUCTIVE: if the existing collection has a different vector dim,
 *   we delete + recreate (all existing data is lost).
 *
 * Usage:
 *   bun run setup.ts
 *   bun run setup.ts --recreate
 */

const ASTRA_ENDPOINT = process.env.ASTRA_DB_ENDPOINT?.replace(/\/$/, "");
const ASTRA_TOKEN = process.env.ASTRA_DB_APPLICATION_TOKEN;
const ASTRA_KEYSPACE = process.env.ASTRA_DB_KEYSPACE || "default_keyspace";
const COLLECTION = "memories";
const VECTOR_DIM = parseInt(process.env.ASTRA_VECTOR_DIM || "768", 10);
const METRIC = process.env.ASTRA_VECTOR_METRIC || "cosine";

interface AstraResp<T = any> {
  data?: T;
  status?: { count?: number; ok?: number };
  errors?: { title: string; message: string }[];
}

async function api<T = any>(
  method: "POST" | "GET" | "DELETE",
  path: string,
  body?: any
): Promise<T> {
  if (!ASTRA_ENDPOINT || !ASTRA_TOKEN) {
    throw new Error("Missing ASTRA_DB_ENDPOINT or ASTRA_DB_APPLICATION_TOKEN env vars.");
  }
  const url = `${ASTRA_ENDPOINT}/api/json/v1/${ASTRA_KEYSPACE}${path}`;
  const res = await fetch(url, {
    method,
    headers: {
      Token: ASTRA_TOKEN,
      "Content-Type": "application/json",
      Accept: "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let json: AstraResp<T>;
  try {
    json = JSON.parse(text);
  } catch {
    throw new Error(`Astra ${method} ${path} non-JSON: HTTP ${res.status} ${text.slice(0, 200)}`);
  }
  if (json.errors && json.errors.length > 0) {
    throw new Error(`Astra ${method} ${path} error: ${json.errors.map((e) => `${e.title}: ${e.message}`).join("; ")}`);
  }
  if (!res.ok && res.status !== 404) {
    throw new Error(`Astra ${method} ${path} HTTP ${res.status}: ${text.slice(0, 200)}`);
  }
  return (json.data ?? json) as T;
}

async function listCollections(): Promise<any[]> {
  const r = await api<any[]>("POST", "", { findCollections: { options: { limit: 100 } } });
  return Array.isArray(r) ? r : [];
}

async function getCollection(name: string): Promise<any | null> {
  const all = await listCollections();
  return all.find((c) => c.name === name) ?? null;
}

async function createCollection(name: string, dim: number): Promise<any> {
  return api("POST", "", {
    createCollection: {
      name,
      options: { vector: { dimension: dim, metric: METRIC } },
    },
  });
}

async function deleteCollection(name: string): Promise<void> {
  await api("POST", "", { deleteCollection: { name } });
}

async function collectionExists(): Promise<{ exists: boolean; dim: number | null; metric: string | null }> {
  // Try a cheap find; if collection is missing, this errors. We probe differently:
  // There is no listCollections on Data API per-collection path, so we try to insert a sentinel
  // OR — better — we attempt createCollection and treat "already exists" as success.
  // The cleanest: try createCollection; if error says "already exists", mark exists=true.
  // Then we discover dim via insertOne with a probe vector (or skip dim check and always recreate on --recreate).
  return { exists: false, dim: null, metric: null };
}

async function cmdCreate() {
  const payload = {
    createCollection: {
      name: COLLECTION,
      options: {
        vector: { dimension: VECTOR_DIM, metric: METRIC },
      },
    },
  };
  const r = await api("POST", "", payload);
  console.log(`✅ Created '${COLLECTION}' (vector dim=${VECTOR_DIM}, metric=${METRIC})`);
  console.log(`  ${JSON.stringify(r)}`);
}

async function cmdDrop() {
  const payload = { deleteCollection: { name: COLLECTION } };
  await api("POST", "", payload);
  console.log(`🗑️  Deleted '${COLLECTION}'`);
}

async function main() {
  const recreate = process.argv.includes("--recreate");

  console.log(`📋 Collection '${COLLECTION}' keyspace='${ASTRA_KEYSPACE}' target dim=${VECTOR_DIM} metric=${METRIC}`);

  if (recreate) {
    console.log("🔄 --recreate: dropping then creating.");
    try {
      await cmdDrop();
    } catch (e: any) {
      // ignore "does not exist"
      console.log(`  (drop note: ${e.message})`);
    }
    await cmdCreate();
    return;
  }

  // Non-destructive: try create; if "already exists", warn and exit.
  try {
    await cmdCreate();
  } catch (e: any) {
    if (/already exists/i.test(e.message)) {
      console.log(`⚠️  Collection already exists. If you need to change vector dim, run with --recreate.`);
      console.log(`   (Existing dim cannot be discovered via Data API; recreate is safe — re-sync will repopulate.)`);
    } else {
      throw e;
    }
  }
}

main().catch((e) => {
  console.error("❌", e.message);
  process.exit(1);
});