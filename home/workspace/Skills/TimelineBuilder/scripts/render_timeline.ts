import { readFileSync } from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("Usage: bun render_timeline.ts <timeline.json>");
  process.exit(1);
}

const data = JSON.parse(readFileSync(file, "utf-8"));

let out = `# ${data.title}\n\n${data.topic}\n\n`;
if (data.period) out += `**Period:** ${data.period}\n\n`;

for (const phase of data.phases) {
  out += `## ${phase.title}\n\n`;
  for (const e of phase.events) {
    out += `### ${e.date} — ${e.title}\n\n${e.description}\n\n**Significance:** ${e.significance}\n\n**Sources:** ${e.sources.join("; ")}\n\n`;
  }
}

console.log(out);
