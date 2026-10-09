import { expect, test } from "bun:test";
import {
  chunked,
  contentHash,
  dedupeInputDocs,
  dedupeKeyForDoc,
  dedupeRanked,
  findPageRequest,
  mergeDocsById,
  normalizedTextHash,
  stableDocId,
  staleDocsToDeactivate,
  type ClarionDoc,
} from "./sync";

function zobodhiDoc(id: number, text: string, timestamp: string): ClarionDoc {
  return {
    source: "zobodhi",
    source_id: `zobodhi:${id}`,
    dedupe_key: `zobodhi:${normalizedTextHash(text)}`,
    layer: "fact",
    text,
    path: "/home/workspace/Skills/zobodhi-memory/memory.json",
    timestamp,
    tags: [],
    project: "general",
    title: text.slice(0, 80),
  };
}

test("stable document IDs depend on source identity, not content", () => {
  expect(stableDocId("clarion:projects/example.md")).toBe(
    stableDocId("clarion:projects/example.md")
  );
  expect(stableDocId("clarion:projects/example.md")).not.toBe(
    stableDocId("clarion:projects/other.md")
  );
});

test("detailed current hashes win when reconciliation summaries overlap", () => {
  const detailed = { _id: "current", content_hash: "content", text_hash: "text", active: true };
  const summary = { _id: "current", source: "zobodhi", active: true };
  expect(mergeDocsById([detailed], [summary]).get("current")).toBe(detailed);
});
test("Astra find requests use cursor pagination, projections, and no total limit", () => {
  expect(findPageRequest({ active: true }, null)).toEqual({
    find: { filter: { active: true }, options: {} },
  });
  expect(findPageRequest({ active: true }, "next-page", { source: 1 })).toEqual({
    find: {
      filter: { active: true },
      projection: { source: 1 },
      options: { pageState: "next-page" },
    },
  });
});

test("ID lookups respect Astra's 100-value $in limit", () => {
  const groups = chunked(Array.from({ length: 201 }, (_, i) => i), 100);
  expect(groups.map((group) => group.length)).toEqual([100, 100, 1]);
  expect(groups.flat()).toEqual(Array.from({ length: 201 }, (_, i) => i));
});

test("content hashes change with content but ignore embedding vectors", () => {
  const original = zobodhiDoc(1, "Original memory", "2026-10-08T00:00:00Z");
  expect(contentHash(original)).not.toBe(
    contentHash({ ...original, text: "Updated memory" })
  );
  expect(contentHash(original)).toBe(
    contentHash({ ...original, $vector: [0.1, 0.2] })
  );
});

test("ingest collapses repeat source IDs but preserves distinct facts with identical text", () => {
  const older = zobodhiDoc(1, "Same fact", "2026-10-07T00:00:00Z");
  const updated = zobodhiDoc(1, "Same fact revised", "2026-10-08T00:00:00Z");
  const sameTextDifferentId = zobodhiDoc(2, "Same fact revised", "2026-10-09T00:00:00Z");
  const result = dedupeInputDocs([older, updated, sameTextDifferentId]);
  expect(result).toHaveLength(2);
  expect(result.map((doc) => doc.text)).toContain("Same fact revised");
  expect(result.map((doc) => doc.source_id)).toContain("zobodhi:1");
  expect(result.map((doc) => doc.source_id)).toContain("zobodhi:2");
});

test("query ranking collapses legacy and stable copies of one fact", () => {
  const stable = zobodhiDoc(1, "The same memory", "2026-10-08T00:00:00Z");
  const legacy = {
    source: "zobodhi",
    path: stable.path,
    text: "The same   memory",
    title: stable.title,
  };
  expect(dedupeKeyForDoc(legacy)).toBe(stable.dedupe_key);
  const result = dedupeRanked([
    { id: "old", score: 0.02, doc: legacy },
    { id: "new", score: 0.03, doc: stable },
  ]);
  expect(result).toHaveLength(1);
  expect(result[0]?.id).toBe("new");
});

test("retirement is scoped, skips current rows, and never deletes", () => {
  const rows = [
    { _id: "current", source: "zobodhi", active: true },
    { _id: "old", source: "zobodhi", active: true },
    { _id: "already-retired", source: "zobodhi", active: false },
    { _id: "other-source", source: "clarion_daily", active: true },
  ];
  expect(staleDocsToDeactivate(rows, new Set(["current"]), ["zobodhi"]).map((r) => r._id)).toEqual([
    "old",
  ]);
});
