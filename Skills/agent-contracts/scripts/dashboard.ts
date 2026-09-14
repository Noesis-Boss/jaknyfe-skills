#!/usr/bin/env bun
import { readdir, readFile, writeFile, mkdir } from "node:fs/promises";
import { join } from "node:path";

const root = "/home/workspace";
const runsDir = join(root, "runs/agent-contracts");
const output = join(root, "runs/agent-contracts/dashboard.html");
const files = (await readdir(runsDir).catch(() => []))
  .filter((file) => file.endsWith(".jsonl"))
  .sort()
  .reverse();
const runs = [];
for (const file of files) {
  const records = (await readFile(join(runsDir, file), "utf8"))
    .trim().split("\n").filter(Boolean).map((line) => JSON.parse(line));
  if (records.length) runs.push(records);
}
const data = JSON.stringify(runs).replace(/</g, "\\u003c");
const html = `<!doctype html><meta charset="utf-8"><title>Agent Contract Audit</title>
<style>body{font:14px system-ui;margin:32px;background:#101114;color:#eee}h1{margin-bottom:8px}input{width:100%;padding:10px;background:#1b1d22;color:#fff;border:1px solid #444;border-radius:6px;margin:12px 0 20px}.run{border:1px solid #363941;border-radius:8px;margin:10px 0;padding:14px;background:#17191e}.meta{color:#aab0bd}.event{margin:6px 0;padding:6px 8px;background:#20232a;border-radius:4px;font-family:ui-monospace,monospace}.ok{color:#7ee787}.error{color:#ff7b72}</style>
<h1>Agent Contract Audit</h1><div class="meta" id="count"></div><input id="q" placeholder="Filter agent, surface, event, tool, or status">
<main id="runs"></main><script>const runs=${data};const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));function render(){const q=document.querySelector('#q').value.toLowerCase();const rows=runs.filter(rs=>JSON.stringify(rs).toLowerCase().includes(q));document.querySelector('#count').textContent=rows.length+' runs';document.querySelector('#runs').innerHTML=rows.map(rs=>{const f=rs[0],l=rs[rs.length-1];return '<section class="run"><b>'+esc(f.agent)+' / '+esc(f.surface)+'</b> <span class="meta">'+esc(f.run_id)+' · '+esc(f.timestamp)+'</span><div class="meta">status: <span class="'+esc(l.status)+'">'+esc(l.status)+'</span> · '+rs.length+' records</div>'+rs.map(e=>'<div class="event"><span class="'+esc(e.status)+'">'+esc(e.type)+'</span> '+esc(e.name||e.artifact||e.path||'')+' <span class="meta">'+esc(e.timestamp)+'</span></div>').join('')+'</section>'}).join('')}document.querySelector('#q').oninput=render;render();</script>`;
await mkdir(join(root, "runs/agent-contracts"), { recursive: true });
await writeFile(output, html);
console.log(output);
