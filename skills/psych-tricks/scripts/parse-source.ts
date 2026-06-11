#!/usr/bin/env bun
/**
 * parse-source.ts
 *
 * Parse /home/workspace/49 Psychological Mind Tricks Breakdown.rtf
 * into scripts/tricks.json. Re-run if the source RTF changes.
 *
 * Usage:  bun scripts/parse-source.ts
 */
import { readFileSync, writeFileSync } from "node:fs";

const SRC = "/home/workspace/49 Psychological Mind Tricks Breakdown.rtf";
const OUT = new URL("./tricks.json", import.meta.url).pathname;

const raw = readFileSync(SRC, "utf8");

let text = raw
  .replace(/\\[a-z]+[-]?[0-9]* ?/g, " ")
  .replace(/[{}]/g, "")
  .replace(/\\[^a-z]/g, " ")
  .replace(/\s+/g, " ")
  .trim();

type Section = { number: number; title: string; start: number; end: number };
const sections: Section[] = [];
const re = /(?<=\s)(\d{1,2})\.\s+/g;
let m: RegExpExecArray | null;
while ((m = re.exec(text)) !== null) {
  const n = parseInt(m[1], 10);
  if (n < 1 || n > 49) continue;
  const after = text.slice(m.index + m[0].length, m.index + m[0].length + 200);
  const endM = /\s+The Concept\b|\s+The Study\b|\s+The Technique\b|\s+Study:|\s+Technique:|\s+Examples:|\s+Application:/.exec(after);
  if (!endM) continue;
  const title = after.slice(0, endM.index).trim().replace(/[.:]+$/, "");
  sections.push({
    number: n,
    title,
    start: m.index + m[0].length + endM.index,
    end: m.index + m[0].length + endM.index,
  });
}

// Re-compute end as the start of the next section
sections.sort((a, b) => a.number - b.number);
for (let i = 0; i < sections.length; i++) {
  const next = sections[i + 1];
  if (!next) {
    sections[i].end = text.length;
    continue;
  }
  const nextStart = text.indexOf(`${next.number}. `, sections[i].start);
  sections[i].end = nextStart > 0 ? nextStart : text.length;
}

const fieldSplitter = /The Concept\s*:|The Study\s*:|The Technique\s*:|Study\s*:|Technique\s*:|Examples\s*:|Application\s*:/gi;

const fieldMarkers = [
  { key: "concept", re: /The Concept\s*:/i },
  { key: "study", re: /(?:The )?Study\s*:/i },
  { key: "technique", re: /(?:The )?Technique\s*:/i },
  { key: "examples", re: /Examples\s*:/i },
  { key: "application", re: /Application\s*:/i },
];

const items = sections.map((s) => {
  const body = text.slice(s.start, s.end).trim();
  const fields: Record<string, string> = {
    concept: "",
    study: "",
    technique: "",
    examples: "",
    application: "",
  };

  // Collect all marker positions
  type Hit = { idx: number; key: string; pos: number };
  const hits: Hit[] = [];
  for (const { key, re } of fieldMarkers) {
    const m = re.exec(body);
    if (m) hits.push({ idx: m.index + m[0].length, key, pos: m.index });
  }
  hits.sort((a, b) => a.pos - b.pos);

  for (let i = 0; i < hits.length; i++) {
    const start = hits[i].idx;
    const end = i + 1 < hits.length ? hits[i + 1].pos : body.length;
    const val = body.slice(start, end).trim();
    fields[hits[i].key] = val;
  }

  return {
    number: s.number,
    title: s.title,
    concept: fields.concept,
    study: fields.study,
    technique: fields.technique,
    examples: fields.examples,
    application: fields.application,
  };
});

writeFileSync(OUT, JSON.stringify(items, null, 2));
console.log(`Wrote ${items.length} items to ${OUT}`);
