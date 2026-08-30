import { readFileSync, writeFileSync, mkdirSync, existsSync } from "node:fs";

const API_BASE = "https://styles.refero.design/api/styles";

const HELP = `Usage:
  bun run fetch-styles.ts --list [--limit N]     List styles (default 20)
  bun run fetch-styles.ts --search <query>       Search by site name
  bun run fetch-styles.ts <id> > DESIGN.md       Fetch style as DESIGN.md
  bun run fetch-styles.ts <id>                   Preview style tokens`;

interface ReferoColor { name: string; hex: string; }
interface ReferoStyle {
  id: string; url: string; siteName: string; screenshotUrl: string; thumbnailUrl: string;
  colors: ReferoColor[]; fonts: string[]; northStar: string; managementSignals: string[];
  createdAt?: string;
}
interface ReferoResponse { styles: ReferoStyle[]; nextCursor?: string | null; nextPage?: boolean; }

function parseArgs(): { command: string; args: string[] } {
  const args = process.argv.slice(2);
  if (args.length === 0 || args.includes("--help") || args.includes("-h")) return { command: "help", args: [] };
  if (args[0] === "--list" || args[0] === "-l") return { command: "list", args };
  if (args[0] === "--search" || args[0] === "-s") return { command: "search", args };
  return { command: "fetch", args };
}

function parseLimit(args: string[]): number {
  const idx = args.indexOf("--limit");
  if (idx >= 0 && args[idx + 1]) return parseInt(args[idx + 1], 10) || 20;
  return 20;
}

async function fetchStyles(limit = 20, cursor?: string): Promise<ReferoResponse> {
  const url = new URL(API_BASE);
  url.searchParams.set("limit", String(limit));
  if (cursor) url.searchParams.set("cursor", cursor);
  const resp = await fetch(url.toString());
  if (!resp.ok) throw new Error(`HTTP ${resp.status}: ${resp.statusText}`);
  return resp.json();
}

function escapeMd(s: string): string { return s.replace(/\|/g, "\\|").replace(/\*/g, "\\*"); }

async function cmdList(args: string[]): Promise<void> {
  const limit = parseLimit(args);
  const data = await fetchStyles(limit);
  console.log(`\n# refero.design — ${data.styles.length} styles\n`);
  for (const s of data.styles) {
    console.log(`| ${s.siteName} | ${s.colors.map(c => `**${c.name}** ${c.hex}`).join(", ")} | ${s.fonts.join(", ")} |`);
    console.log(`| ${s.url} | _${escapeMd(s.northStar)}_ | |`);
  }
  if (data.nextPage) console.log(`\n--- more available (cursor: ${data.nextCursor}) ---`);
}

async function cmdSearch(args: string[]): Promise<void> {
  const query = args[1];
  if (!query) { console.error("Error: --search requires a query"); process.exit(1); }
  const all: ReferoStyle[] = [];
  let cursor: string | undefined;
  let page = 0;
  while (page < 10) {
    const data = await fetchStyles(50, cursor);
    all.push(...data.styles);
    if (!data.nextPage) break;
    cursor = data.nextCursor ?? undefined;
    page++;
    if (all.length >= 500) break;
  }
  const lc = query.toLowerCase();
  const hits = all.filter(s => s.siteName.toLowerCase().includes(lc) || (s.managementSignals ?? []).some(m => m.toLowerCase().includes(lc)));
  console.log(`\n# refero.results for "${query}" — ${hits.length} matches\n`);
  for (const s of hits.slice(0, 20)) {
    console.log(`## ${s.siteName} — ${s.url}`);
    console.log(`Colors: ${s.colors.map(c => `[${c.name}](${c.hex})`).join(", ")}`);
    console.log(`Fonts: ${s.fonts.join(", ")}`);
    console.log(`North star: "${s.northStar}"`);
    console.log(`ID: \`${s.id}\``);
    console.log();
  }
}

async function cmdFetch(id: string): Promise<void> {
  let style: ReferoStyle | null = null;
  const data = await fetchStyles(1);
  if (data.styles[0]?.id === id) { style = data.styles[0]; }
  else {
    let cursor: string | undefined;
    let page = 0;
    while (page < 100) {
      const pageData = await fetchStyles(50, cursor);
      const found = pageData.styles.find(s => s.id === id);
      if (found) { style = found; break; }
      if (!pageData.nextPage) break;
      cursor = pageData.nextCursor ?? undefined;
      page++;
    }
  }
  if (!style) { console.error(`Error: style ${id} not found`); process.exit(1); }
  const tokens = style.colors.map(c => `- ${c.name}: ${c.hex}`).join("\n");
  console.log(`# ${style.siteName} — DESIGN.md`);
  console.log(`\n> ${escapeMd(style.northStar)}`);
  console.log(`\n## Palette\n${tokens}`);
  console.log(`\n## Typography\n${style.fonts.map(f => `- ${f}`).join("\n")}`);
  console.log(`\n## Source\n- Site: ${style.url}`);
  console.log(`- Thumbnail: ${style.thumbnailUrl}`);
}

async function main(): Promise<void> {
  const { command, args } = parseArgs();
  switch (command) {
    case "help": console.log(HELP); break;
    case "list": await cmdList(args); break;
    case "search": await cmdSearch(args); break;
    case "fetch": await cmdFetch(args[0]); break;
  }
}
main().catch(e => { console.error(e.message); process.exit(1); });
