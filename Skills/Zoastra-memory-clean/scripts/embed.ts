#!/usr/bin/env node
/**
 * Local embedding via nomic-embed-text-v1.5 (Transformers.js).
 *
 * - Uses @huggingface/transformers v3 (preferred; matches upstream README)
 * - Falls back to @xenova/transformers v2 (legacy) if v3 isn't loadable
 * - Matryoshka truncation to 512 dims by default (configurable via env)
 * - Required prefixes: "search_query: " for queries, "search_document: " for docs
 * - Output is L2-normalized so cosine similarity == dot product
 *
 * Usage:
 *   bun run embed.ts embed "text to embed"
 *   bun run embed.ts embed-doc "memory body text"
 *   bun run embed.ts embed-query "search text"
 *   bun run embed.ts info
 */

const MODEL_ID = "nomic-ai/nomic-embed-text-v1.5";
const MATRYOSHKA_DIM = parseInt(process.env.MATRYOSHKA_DIM || "768", 10);
const CACHE_DIR = process.env.HF_HOME || ".cache/huggingface";

// Try v3 first, fall back to v2.
let pipeline: any;
let layer_norm: any;
try {
  // @ts-ignore
  const v3 = await import("@huggingface/transformers");
  pipeline = v3.pipeline;
  layer_norm = v3.layer_norm;
  if (!layer_norm) console.warn("⚠️  @huggingface/transformers has no layer_norm export; using fallback L2-norm only");
} catch (e) {
  console.warn("⚠️  v3 import failed, falling back to @xenova/transformers:", (e as Error).message);
  // @ts-ignore
  const v2 = await import("@xenova/transformers");
  pipeline = v2.pipeline;
  layer_norm = v2.layer_norm;
}

// One extractor, reused across calls.
let extractorPromise: Promise<any> | null = null;
async function getExtractor() {
  if (!extractorPromise) {
    // @ts-ignore
    process.env.HF_HOME = CACHE_DIR;
    extractorPromise = pipeline("feature-extraction", MODEL_ID, {
      quantized: true,
      cache_dir: CACHE_DIR,
    });
  }
  return extractorPromise;
}

function l2norm(t: any): any {
  // t is a Tensor [n, dim]; normalize along last dim.
  if (typeof t.normalize === "function") return t.normalize(2, -1);
  // Fallback: manual L2 norm
  const data = t.data as Float32Array;
  const dim = t.dims[t.dims.length - 1];
  const out = new Float32Array(data.length);
  for (let i = 0; i < data.length; i += dim) {
    let s = 0;
    for (let j = 0; j < dim; j++) s += data[i + j] ** 2;
    s = Math.sqrt(s) || 1;
    for (let j = 0; j < dim; j++) out[i + j] = data[i + j] / s;
  }
  // Wrap in same-ish shape so slicing works
  return { ...t, data: out, dims: t.dims };
}

async function embedRaw(text: string): Promise<Float32Array> {
  const extractor = await getExtractor();
  let emb = await extractor(text, { pooling: "mean" });
  // Apply layer norm if available (Nomic v1.5 README requires this before slicing)
  if (layer_norm) {
    try {
      emb = layer_norm(emb, [emb.dims[emb.dims.length - 1]]);
    } catch (e) {
      console.warn("⚠️  layer_norm step skipped:", (e as Error).message);
    }
  }
  // Matryoshka truncate
  const fullDim = emb.dims[emb.dims.length - 1];
  const target = Math.min(MATRYOSHKA_DIM, fullDim);
  if (typeof emb.slice === "function") {
    emb = emb.slice(null, [0, target]);
  }
  // L2 normalize (required for cosine sim == dot product)
  emb = l2norm(emb);
  // Return as plain Float32Array
  return Float32Array.from(emb.data as Float32Array);
}

async function embedDoc(text: string): Promise<Float32Array> {
  return embedRaw(`search_document: ${text}`);
}

async function embedQuery(text: string): Promise<Float32Array> {
  return embedRaw(`search_query: ${text}`);
}

async function main() {
  const [cmd, ...rest] = process.argv.slice(2);
  const arg = rest.join(" ").trim();

  switch (cmd) {
    case "info": {
      console.log(`Model:    ${MODEL_ID}`);
      console.log(`Dim:      ${MATRYOSHKA_DIM} (matryoshka-truncated from 768)`);
      console.log(`Cache:    ${CACHE_DIR}`);
      console.log(`Runtime:  ${layer_norm ? "@huggingface/transformers v3" : "@xenova/transformers v2"}`);
      const t0 = Date.now();
      const e = await embedQuery("warmup");
      console.log(`Warmup:   ${Date.now() - t0}ms (first run downloads model ~270MB)`);
      console.log(`Output:   Float32Array(${e.length})`);
      break;
    }
    case "embed":
    case "embed-doc": {
      const v = await embedDoc(arg);
      console.log(JSON.stringify(Array.from(v)));
      break;
    }
    case "embed-query": {
      const v = await embedQuery(arg);
      console.log(JSON.stringify(Array.from(v)));
      break;
    }
    default:
      console.log("Usage:");
      console.log("  embed.ts info");
      console.log("  embed.ts embed-doc <text>");
      console.log("  embed.ts embed-query <text>");
  }
}

main().catch((e) => {
  console.error("❌", e.message);
  process.exit(1);
});
