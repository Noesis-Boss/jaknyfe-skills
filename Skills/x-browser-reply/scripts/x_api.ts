#!/usr/bin/env bun
// x_api.ts — reply/follow on X via a Zo /zo/ask child invocation that uses use_app_x.
// Rebuilt 2026-09-07. Env: ZO_CLIENT_IDENTITY_TOKEN (Zo-provided).
import { writeFileSync, existsSync, readFileSync } from "node:fs";

const LEDGER = "/home/workspace/Skills/x-browser-reply/processed_tweets.json";
const SELF = new Set(["jak_nyfe", "zdsentry"]);

function parseArgs(): Record<string, string> {
  const args: Record<string, string> = {};
  const a = process.argv.slice(2);
  for (let i = 0; i < a.length; i++) {
    if (a[i].startsWith("--")) args[a[i].slice(2)] = a[i + 1] ?? "";
  }
  return args;
}

function loadLedger(): { processed: Record<string, any> } {
  if (existsSync(LEDGER)) {
    try {
      return JSON.parse(readFileSync(LEDGER, "utf8"));
    } catch {}
  }
  return { processed: {} };
}

function markProcessed(tweetId: string, username: string) {
  const ledger = loadLedger();
  ledger.processed[tweetId] = { date: new Date().toISOString().slice(0, 10), username };
  writeFileSync(LEDGER, JSON.stringify(ledger, null, 2));
}

async function ask(prompt: string): Promise<string> {
  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
  if (!token) {
    console.error("ERROR: ZO_CLIENT_IDENTITY_TOKEN missing in env");
    process.exit(3);
  }
  const res = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: { authorization: token, "content-type": "application/json" },
    body: JSON.stringify({
      input: prompt,
      model_name: "vercel:zai/glm-5.3-flash",
    }),
  });
  const data = await res.json();
  return String(data.output ?? "");
}

const [action] = process.argv.slice(2);
const args = parseArgs();
const account = args.username || "jak_nyfe";

if (!SELF.has(account)) {
  console.error(`ERROR: account must be one of ${[...SELF].join(", ")}`);
  process.exit(2);
}

if (action === "reply") {
  const tweetId = args["tweet-id"];
  const text = args.text;
  if (!tweetId || !text) {
    console.error("usage: x_api.ts reply --tweet-id ID --text \"...\" [--username jak_nyfe]");
    process.exit(2);
  }
  const ledger = loadLedger();
  if (ledger.processed[tweetId]) {
    console.log(JSON.stringify({ status: "skipped", reason: "already processed", tweet_id: tweetId }));
    process.exit(0);
  }
  const out = await ask(
    `Using the use_app_x tool with username "${account}", post a reply to tweet ID ${tweetId} ` +
      `with exactly this text: ${JSON.stringify(text)}\n` +
      `Use x-post-reply if available (check list_app_tools("x") first). Do not post anything else. ` +
      `Respond with exactly POSTED if the reply succeeded, or FAILED: <reason> if it did not.`,
  );
  if (out.includes("POSTED")) {
    markProcessed(tweetId, account);
    console.log(JSON.stringify({ status: "posted", tweet_id: tweetId, account }));
  } else {
    console.error(`REPLY FAILED: ${out.slice(0, 300)}`);
    process.exit(1);
  }
} else if (action === "follow") {
  const target = args.follow || args.target || args["follow-username"];
  if (!target) {
    console.error("usage: x_api.ts follow --follow USERNAME [--username jak_nyfe]");
    process.exit(2);
  }
  if (SELF.has(target.toLowerCase())) {
    console.log(JSON.stringify({ status: "skipped", reason: "self-account", target }));
    process.exit(0);
  }
  const out = await ask(
    `Using the use_app_x tool with username "${account}", follow the X user @${target}. ` +
      `Check list_app_tools("x") for a follow action; if none exists, respond FAILED: no-follow-action. ` +
      `Respond with exactly FOLLOWED on success, or FAILED: <reason>.`,
  );
  if (out.includes("FOLLOWED")) {
    console.log(JSON.stringify({ status: "followed", target, account }));
  } else {
    console.error(`FOLLOW FAILED: ${out.slice(0, 300)}`);
    process.exit(1);
  }
} else {
  console.error("usage: x_api.ts <reply|follow> [args] — see SKILL.md");
  process.exit(2);
}
