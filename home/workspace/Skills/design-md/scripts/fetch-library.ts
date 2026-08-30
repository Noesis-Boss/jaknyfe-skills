/**
 * Fetch DESIGN.md files from designmd.app — the largest open DESIGN.md library (461+ systems).
 *
 * Sources:
 *   - Library:  ~433 community-contributed design systems with YAML front matter
 *   - Brands:    29 real company design systems (markdown format, no YAML front matter)
 *
 * Usage:
 *   bun run fetch-library.ts --list                               List all library designs
 *   bun run fetch-library.ts --list --type "Futurista & Tech"     Filter by type
 *   bun run fetch-library.ts --brands                             List all real brands
 *   bun run fetch-library.ts --search "gradient"                    Search by keyword
 *   bun run fetch-library.ts aurora-ui                           Fetch a library design
 *   bun run fetch-library.ts --brand resend                        Fetch a real brand DESIGN.md
 *   bun run fetch-library.ts --search "gradient" aurora-ui         Search then fetch
 */

import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { exit } from "node:process";

const CATALOG_PATH = resolve(import.meta.dirname, "../references/designmd-library.json");
const BRANDS_PATH = resolve(import.meta.dirname, "../references/designmd-brands.json");

interface DesignItem {
  slug: string;
  title: string;
  type: string;
  description: string;
  use_case: string;
  era: string;
  style_type: string;
  keywords: string[];
  id: number;
  source_url: string;
}

interface Catalog {
  source: string;
  library_count: number;
  last_updated: string;
  items: DesignItem[];
}

interface BrandItem {
  slug: string;
  title: string;
  source_url: string;
}

interface BrandsCatalog {
  source: string;
  brand_count: number;
  last_updated: string;
  brands: BrandItem[];
}

interface ParsedArgs {
  list: boolean;
  brands: boolean;
  search?: string;
  type?: string;
  brand?: string;
  slug?: string;
  help: boolean;
}

function parseArgs(): ParsedArgs {
  const args = process.argv.slice(2);
  const opts: ParsedArgs = { list: false, brands: false, help: false };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg === "--help" || arg === "-h") opts.help = true;
    else if (arg === "--list" || arg === "-l") opts.list = true;
    else if (arg === "--brands") opts.brands = true;
    else if (arg === "--search" || arg === "-s") { opts.search = args[++i]; }
    else if (arg === "--type" || arg === "-t") { opts.type = args[++i]; }
    else if (arg === "--brand" || arg === "-b") { opts.brand = args[++i]; }
    else if (!arg.startsWith("-")) { opts.slug = arg; }
  }

  return opts;
}

function loadCatalog(): Catalog {
  try {
    return JSON.parse(readFileSync(CATALOG_PATH, "utf-8"));
  } catch {
    throw new Error("Catalog file not found. Run this script from the design-md skill directory.");
  }
}

function loadBrandsCatalog(): BrandsCatalog {
  try {
    return JSON.parse(readFileSync(BRANDS_PATH, "utf-8"));
  } catch {
    throw new Error("Brands catalog not found.");
  }
}

function printHelp() {
  console.log(`Fetch DESIGN.md files from designmd.app (461+ design systems)

USAGE:
  bun run fetch-library.ts --list                          List all library designs
  bun run fetch-library.ts --list --type "Futurista & Tech" Filter by category type
  bun run fetch-library.ts --brands                        List all real brand design systems
  bun run fetch-library.ts --search "gradient"             Search by keyword/title
  bun run fetch-library.ts aurora-ui                       Fetch a library design's DESIGN.md
  bun run fetch-library.ts --brand resend                  Fetch a real brand's DESIGN.md
  bun run fetch-library.ts --search "grunge" > DESIGN.md   Search, then save first result

The library has 433 AI-ready design systems with YAML front matter (proper DESIGN.md format).
The brands section has 29 real company design systems (human-readable markdown).

Types: Arte & Ilustracao, Brasil, Brutalismo, Dados & Infografico,
       Design System Themes, Editorial & Tipografia, Flat & Soft UI,
       Futurista & Tech, Minimalismo & Swiss, Retro & Pop, Temas & Verticais`);
}

function listDesigns(opts: ParsedArgs) {
  const catalog = loadCatalog();
  let items = catalog.items;

  if (opts.type) {
    items = items.filter((i) => i.type === opts.type);
  }

  console.log(`${catalog.library_count} design systems from designmd.app`);
  if (opts.type) {
    console.log(`Filtered by type: "${opts.type}"`);
  }
  console.log("---");
  for (const item of items) {
    console.log(`${item.slug}\t${item.title}\t[${item.type}] ${item.era}`);
  }
}

function listBrands() {
  const catalog = loadBrandsCatalog();
  console.log(`${catalog.brand_count} real brand design systems from designmd.app`);
  console.log("---");
  for (const brand of catalog.brands) {
    console.log(`${brand.slug}\t${brand.title}`);
  }
}

function searchDesigns(query: string) {
  const catalog = loadCatalog();
  const q = query.toLowerCase();
  const matches = catalog.items.filter(
    (i) =>
      i.title.toLowerCase().includes(q) ||
      i.slug.toLowerCase().includes(q) ||
      i.keywords.some((k) => k.toLowerCase().includes(q)) ||
      i.type.toLowerCase().includes(q) ||
      i.era.toLowerCase().includes(q)
  );

  console.log(`${matches.length} matches for "${query}"`);
  console.log("---");
  for (const item of matches) {
    console.log(`${item.slug}\t${item.title}\t[${item.type}] ${item.era}`);
  }
}

async function fetchDesign(slug: string) {
  const catalog = loadCatalog();
  const item = catalog.items.find((i) => i.slug === slug);

  if (!item) {
    console.error(`"${slug}" not found in designmd.app library.`);
    console.error(`Run --list to see all available slugs.`);
    exit(1);
  }

  const res = await fetch(`https://designmd.app/library/${slug}/design.md`);
  if (!res.ok) {
    throw new Error(`Failed to fetch: ${res.status} ${res.statusText}`);
  }
  process.stdout.write(await res.text());
}

async function fetchBrand(slug: string) {
  const catalog = loadBrandsCatalog();
  const brand = catalog.brands.find((b) => b.slug === slug);

  if (!brand) {
    console.error(`"${slug}" not found in designmd.app brands.`);
    console.error(`Run --brands to see all available brand slugs.`);
    exit(1);
  }

  const res = await fetch(`https://designmd.app/brands/${slug}/design.md`);
  if (!res.ok) {
    throw new Error(`Failed to fetch brand: ${res.status} ${res.statusText}`);
  }
  process.stdout.write(await res.text());
}

async function main() {
  const opts = parseArgs();

  if (opts.help) {
    printHelp();
    return;
  }

  if (opts.brands) {
    listBrands();
    return;
  }

  if (opts.list) {
    listDesigns(opts);
    return;
  }

  if (opts.search) {
    searchDesigns(opts.search);
    return;
  }

  if (opts.brand) {
    await fetchBrand(opts.brand);
    return;
  }

  if (opts.slug) {
    await fetchDesign(opts.slug);
    return;
  }

  printHelp();
}

main().catch((err) => {
  console.error(err.message);
  exit(1);
});
