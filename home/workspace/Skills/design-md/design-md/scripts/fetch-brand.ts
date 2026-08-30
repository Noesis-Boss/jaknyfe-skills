/**
 * Fetch a DESIGN.md from the awesome-design-md collection.
 * Usage:
 *   bun run fetch-brand.ts --list                    # List available brands
 *   bun run fetch-brand.ts stripe                    # Fetch Stripe's DESIGN.md
 *   bun run fetch-brand.ts notion > DESIGN.md        # Save to file
 *   bun run fetch-brand.ts --search linear           # Search brands
 */

const REPO_API = "https://api.github.com/repos/VoltAgent/awesome-design-md/contents/design-md";
const RAW_BASE = "https://raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md";

interface GitHubItem {
  name: string;
  path: string;
  type: "dir" | "file";
  download_url: string | null;
}

let brandsCache: string[] | null = null;

async function fetchBrands(): Promise<string[]> {
  if (brandsCache) return brandsCache;
  
  const res = await fetch(REPO_API);
  if (!res.ok) throw new Error(`Failed to fetch brands: ${res.status}`);
  
  const items: GitHubItem[] = await res.json();
  brandsCache = items
    .filter((i) => i.type === "dir")
    .map((i) => i.name)
    .sort();
  
  return brandsCache;
}

async function fetchBrandDESIGN(brand: string): Promise<string> {
  const url = `${RAW_BASE}/${brand}/DESIGN.md`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Brand "${brand}" not found (${res.status}). Run --list to see available brands.`);
  return res.text();
}

async function main() {
  const args = process.argv.slice(2);

  if (args.length === 0 || args.includes("--help") || args.includes("-h")) {
    console.log(`Usage:
  bun run fetch-brand.ts --list              List available brands
  bun run fetch-brand.ts --search <query>    Search brands
  bun run fetch-brand.ts <brand>             Fetch a brand's DESIGN.md
  bun run fetch-brand.ts <brand> > DESIGN.md Save to file`);
    return;
  }

  if (args.includes("--list")) {
    const brands = await fetchBrands();
    for (const b of brands) console.log(b);
    return;
  }

  if (args.includes("--search")) {
    const query = args[args.indexOf("--search") + 1];
    if (!query) { console.error("Missing search query"); process.exit(1); }
    const brands = await fetchBrands();
    const matches = brands.filter((b) => b.toLowerCase().includes(query.toLowerCase()));
    if (matches.length === 0) {
      console.error(`No brands match "${query}"`);
      process.exit(1);
    }
    for (const b of matches) console.log(b);
    return;
  }

  const brand = args[0];
  const content = await fetchBrandDESIGN(brand);
  process.stdout.write(content);
}

main().catch((err) => {
  console.error(err.message);
  process.exit(1);
});
