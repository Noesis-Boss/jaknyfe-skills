#!/usr/bin/env bun
import { createHash } from "node:crypto";
import { mkdir, readdir, readFile, stat, writeFile } from "node:fs/promises";
import { basename, dirname, extname, join, resolve } from "node:path";
import { $ } from "bun";

type Item = { id: string; topic: string; status: string; createdAt: string; directory?: string; listingId?: number; prompts?: string[]; checks?: string[] };
type State = { items: Item[] };
const root = resolve(import.meta.dir, "../../..");
const defaultState = join(root, "memory/etsy-clipart-workflow.json");
const args = process.argv.slice(2);
const value = (name: string, fallback = "") => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] ?? fallback : fallback; };
const statePath = value("--state", defaultState);
const json = async <T>(path: string, fallback: T): Promise<T> => { try { return JSON.parse(await readFile(path, "utf8")) as T; } catch { return fallback; } };
const save = async (state: State) => { await mkdir(dirname(statePath), { recursive: true }); await writeFile(statePath, JSON.stringify(state, null, 2) + "\n"); };
const usage = () => console.log("Usage: workflow.ts <init|queue|package|etsy-draft|approve|status> [options]\nSecrets: ETSY_API_KEY, ETSY_OAUTH_TOKEN");
const ext = [".png", ".jpg", ".jpeg"];

async function packageCollection(dir: string) {
  const files = (await readdir(dir)).filter(x => ext.includes(extname(x).toLowerCase()));
  if (!files.length) throw new Error("No PNG/JPEG assets found");
  const manifest = [] as object[];
  for (const file of files) { const path = join(dir, file); const info = await stat(path); if (!info.size) throw new Error(`Empty asset: ${file}`); manifest.push({ file, bytes: info.size, sha256: createHash("sha256").update(await readFile(path)).digest("hex") }); }
  await writeFile(join(dir, "manifest.json"), JSON.stringify({ createdAt: new Date().toISOString(), files: manifest }, null, 2) + "\n");
  const zip = join(dir, `${basename(dir)}.zip`); await $`cd ${dir} && zip -q -r ${zip} ${files} manifest.json`;
  console.log(JSON.stringify({ directory: dir, assets: files.length, zip, manifest: join(dir, "manifest.json") }, null, 2));
}

async function etsyDraft(dir: string, shop: string) {
  const apiKey = process.env.ETSY_API_KEY, token = process.env.ETSY_OAUTH_TOKEN;
  if (!apiKey || !token) throw new Error("Set ETSY_API_KEY and ETSY_OAUTH_TOKEN in Zo Settings > Advanced");
  const files = (await readdir(dir)).filter(x => ext.includes(extname(x).toLowerCase()));
  const zip = join(dir, `${basename(dir)}.zip`);
  const body = new URLSearchParams({ quantity: "1", title: value("--title", basename(dir)), description: value("--description", "Original digital clipart collection."), price: value("--price", "4.99"), who_made: "i_did", when_made: "2020_2026", taxonomy_id: value("--taxonomy"), type: "download" });
  if (!body.get("taxonomy_id")) throw new Error("--taxonomy is required for Etsy draft creation");
  const headers = { "x-api-key": apiKey, Authorization: `Bearer ${token}` };
  const created = await fetch(`https://openapi.etsy.com/v3/application/shops/${shop}/listings`, { method: "POST", headers: { ...headers, "content-type": "application/x-www-form-urlencoded" }, body });
  if (!created.ok) throw new Error(`Etsy draft failed ${created.status}: ${await created.text()}`);
  const listing = await created.json() as { listing_id: number };
  for (let i = 0; i < files.length; i++) { const form = new FormData(); form.append("image", new Blob([await readFile(join(dir, files[i]))]), files[i]); form.append("rank", String(i + 1)); const response = await fetch(`https://openapi.etsy.com/v3/application/shops/${shop}/listings/${listing.listing_id}/images`, { method: "POST", headers, body: form }); if (!response.ok) throw new Error(`Image upload failed ${response.status}: ${await response.text()}`); }
  const digital = new FormData(); digital.append("file", new Blob([await readFile(zip)]), basename(zip)); const uploaded = await fetch(`https://openapi.etsy.com/v3/application/shops/${shop}/listings/${listing.listing_id}/files`, { method: "POST", headers, body: digital }); if (!uploaded.ok) throw new Error(`Digital upload failed ${uploaded.status}: ${await uploaded.text()}`);
  const state = await json<State>(statePath, { items: [] }); const item = state.items.find(x => x.directory === dir); if (item) { item.status = "etsy-draft"; item.listingId = listing.listing_id; } await save(state); console.log(JSON.stringify({ listingId: listing.listing_id, state: "draft", files: files.length }, null, 2));
}

const command = args[0];
if (!command || command === "--help") usage();
else if (command === "init") { await save({ items: [] }); console.log(`Initialized ${statePath}`); }
else if (command === "queue") { const state = await json<State>(statePath, { items: [] }); const topic = value("--topic"); if (!topic) throw new Error("--topic is required"); const item: Item = { id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`, topic, status: "queued", createdAt: new Date().toISOString(), prompts: [`Original transparent PNG clipart collection about ${topic}; no text, logos, characters, or copied style.`], checks: ["originality review", "trademark review", "transparent background", "edge and halo inspection"] }; state.items.push(item); await save(state); console.log(JSON.stringify(item, null, 2)); }
else if (command === "package") await packageCollection(resolve(value("--dir")));
else if (command === "etsy-draft") await etsyDraft(resolve(value("--dir")), value("--shop"));
else if (command === "approve") { const state = await json<State>(statePath, { items: [] }); const item = state.items.find(x => x.id === value("--id")); if (!item) throw new Error("Unknown item"); item.status = "approved-for-owner-review"; await save(state); console.log(JSON.stringify(item, null, 2)); }
else if (command === "status") console.log(JSON.stringify(await json<State>(statePath, { items: [] }), null, 2));
else usage();
