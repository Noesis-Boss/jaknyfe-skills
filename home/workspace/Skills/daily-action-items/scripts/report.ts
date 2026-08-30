import { randomUUID } from "node:crypto";
import { existsSync, readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { dirname } from "node:path";

const DATA_FILE = "/home/workspace/memory/action-items-report.json";

type Item = {
  id: string;
  account: string;
  msgId: string;
  threadId: string;
  subject: string;
  from: string;
  date: string;
  action: string;
  priority: "high" | "normal";
  status: "open" | "done";
  addedAt: string;
  doneAt: string | null;
};

type CalEvent = {
  id: string;
  summary: string;
  start: string;
  end: string;
  allDay: boolean;
  location: string;
  account: string;
};

type Store = {
  items: Item[];
  completed: Item[];
  processed: Record<string, string>;
  events: CalEvent[];
  eventsDate: string;
  updatedAt: string;
};

function load(): Store {
  const empty: Store = { items: [], completed: [], processed: {}, events: [], eventsDate: "", updatedAt: new Date().toISOString() };
  if (!existsSync(DATA_FILE)) return empty;
  try {
    const raw = JSON.parse(readFileSync(DATA_FILE, "utf8"));
    return { ...empty, ...raw };
  } catch (e) {
    console.error(`Failed to read ${DATA_FILE}: ${(e as Error).message}`);
    return empty;
  }
}

function save(store: Store) {
  store.updatedAt = new Date().toISOString();
  mkdirSync(dirname(DATA_FILE), { recursive: true });
  writeFileSync(DATA_FILE, JSON.stringify(store, null, 2));
}

function fmtDate(iso: string): string {
  if (!iso) return "";
  const d = new Date(iso);
  return d.toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric", timeZone: "America/Phoenix" });
}

function printTable(items: Item[]) {
  if (items.length === 0) {
    console.log("No items.");
    return;
  }
  for (const it of items) {
    const tag = it.priority === "high" ? " [HIGH]" : "";
    console.log(`${it.id}${tag} | ${it.account.split("@")[0]} | ${fmtDate(it.date)} | ${it.subject}`);
    console.log(`    -> ${it.action}`);
  }
}

function parseArgs(): Record<string, string> {
  const args = process.argv.slice(2);
  const out: Record<string, string> = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith("--") && args[i + 1] !== undefined) {
      out[args[i].slice(2)] = args[i + 1];
      i++;
    }
  }
  return out;
}

const cmd = process.argv[2];

if (cmd === "list") {
  const store = load();
  const mode = process.argv[3] || "open";
  if (mode === "all") {
    printTable([...store.items, ...store.completed]);
  } else if (mode === "done") {
    printTable(store.completed);
  } else {
    printTable(store.items);
  }
  console.log(`\n${store.items.length} open, ${store.completed.length} completed, ${Object.keys(store.processed).length} messages processed`);
} else if (cmd === "stats") {
  const store = load();
  console.log(JSON.stringify({ open: store.items.length, completed: store.completed.length, processed: Object.keys(store.processed).length, updatedAt: store.updatedAt }, null, 2));
} else if (cmd === "check") {
  const id = process.argv[3];
  const store = load();
  const idx = store.items.findIndex((i) => i.id === id);
  if (idx === -1) {
    console.error(`No open item with id ${id}`);
    process.exit(1);
  }
  const [it] = store.items.splice(idx, 1);
  it.status = "done";
  it.doneAt = new Date().toISOString();
  store.completed.unshift(it);
  save(store);
  console.log(`Done: ${it.subject}`);
} else if (cmd === "reopen") {
  const id = process.argv[3];
  const store = load();
  const idx = store.completed.findIndex((i) => i.id === id);
  if (idx === -1) {
    console.error(`No completed item with id ${id}`);
    process.exit(1);
  }
  const [it] = store.completed.splice(idx, 1);
  it.status = "open";
  it.doneAt = null;
  store.items.push(it);
  save(store);
  console.log(`Reopened: ${it.subject}`);
} else if (cmd === "add") {
  const a = parseArgs();
  const action = process.argv[3] || a.action;
  if (!action || !a.msgId) {
    console.error('Usage: report.ts add "<action>" --msgId <id> --threadId <id> --account <email> --subject <s> --from <f> --date <iso> [--priority high]');
    process.exit(1);
  }
  const store = load();
  const existing = store.items.find((i) => i.msgId === a.msgId) || store.items.find((i) => a.threadId && i.threadId === a.threadId);
  if (existing) {
    existing.action = action;
    existing.subject = a.subject || existing.subject;
    existing.from = a.from || existing.from;
    existing.date = a.date || existing.date;
    existing.account = a.account || existing.account;
    existing.priority = (a.priority as Item["priority"]) || existing.priority;
    save(store);
    console.log(`Updated: ${existing.id}`);
  } else if (store.completed.some((i) => i.msgId === a.msgId) || store.completed.some((i) => a.threadId && i.threadId === a.threadId)) {
    console.log("Skipped (already completed).");
  } else {
    const item: Item = {
      id: randomUUID().slice(0, 8),
      account: a.account || "unknown",
      msgId: a.msgId,
      threadId: a.threadId || a.msgId,
      subject: a.subject || "(no subject)",
      from: a.from || "",
      date: a.date || new Date().toISOString(),
      action,
      priority: a.priority === "high" ? "high" : "normal",
      status: "open",
      addedAt: new Date().toISOString(),
      doneAt: null,
    };
    store.items.unshift(item);
    store.processed[a.msgId] = new Date().toISOString();
    save(store);
    console.log(`Added: ${item.id}`);
  }
} else if (cmd === "set-events") {
  const date = process.argv[3];
  const raw = process.argv[4];
  if (!date || !raw) {
    console.error('Usage: report.ts set-events <YYYY-MM-DD> <json-array>');
    process.exit(1);
  }
  const store = load();
  try {
    store.events = JSON.parse(raw);
  } catch (e) {
    console.error(`Bad JSON: ${(e as Error).message}`);
    process.exit(1);
  }
  store.eventsDate = date;
  save(store);
  console.log(`Events set for ${date}: ${store.events.length}`);
} else if (cmd === "clear-events") {
  const store = load();
  store.events = [];
  store.eventsDate = "";
  save(store);
  console.log("Events cleared.");
} else if (cmd === "mark-processed") {
  const msgId = process.argv[3];
  const store = load();
  store.processed[msgId] = new Date().toISOString();
  save(store);
  console.log(`Marked processed: ${msgId}`);
} else if (cmd === "prune-done") {
  const keep = Number(process.argv[3] || "100");
  const store = load();
  if (store.completed.length > keep) {
    store.completed = store.completed.slice(0, keep);
    save(store);
  }
  console.log(`Completed pruned to ${store.completed.length}`);
} else {
  console.log(`Usage:
  report.ts list [open|done|all]
  report.ts stats
  report.ts check <id>
  report.ts reopen <id>
  report.ts add "<action>" --msgId <id> --threadId <id> --account <email> --subject <s> --from <f> --date <iso> [--priority high]
  report.ts mark-processed <msgId>
  report.ts prune-done [keep=100]
  report.ts set-events <YYYY-MM-DD> <json-array>
  report.ts clear-events`);
}
