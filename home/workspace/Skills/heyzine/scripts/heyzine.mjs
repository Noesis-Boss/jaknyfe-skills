#!/usr/bin/env node
/**
 * Heyzine API CLI
 */

const BASE = "https://heyzine.com/api1";
const API_KEY = process.env.HEYZINE_API_KEY;
const CLIENT_ID = process.env.HEYZINE_CLIENT_ID;

if (!API_KEY || !CLIENT_ID) {
  console.error("Missing HEYZINE_API_KEY or HEYZINE_CLIENT_ID in env.");
  process.exit(1);
}

const args = new Map(
  process.argv.slice(3).reduce((acc, a, i, arr) => {
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = arr[i + 1];
      acc.set(key, next && !next.startsWith("--") ? (process.argv.includes("--" + next) ? next : (isNaN(Number(next)) ? next : Number(next))) : true);
    }
    return acc;
  }, new Map())
);

function parseArgs(argv) {
  const out = {};
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (next && !next.startsWith("--")) {
        out[key] = next;
        i++;
      } else {
        out[key] = true;
      }
    }
  }
  return out;
}

async function req(method, path, body) {
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers: {
      Authorization: `Bearer ${API_KEY}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await res.text();
  let data;
  try {
    data = JSON.parse(text);
  } catch {
    data = { raw: text };
  }
  const apiFailed = data && typeof data === "object" && data.success === false;
  if (!res.ok || apiFailed) {
    const msg = data?.msg || text || `HTTP ${res.status}`;
    console.error(`HTTP ${res.status}: ${msg}`);
    process.exit(1);
  }
  return data;
}

async function main() {
  const cmd = process.argv[2];
  const rest = process.argv.slice(3);
  const a = parseArgs(rest);

  switch (cmd) {
    case "convert": {
      const pdf = a["pdf"];
      if (!pdf) {
        console.error("--pdf required");
        process.exit(1);
      }
      const body = { pdf, client_id: CLIENT_ID };
      const boolFields = ["download", "full-screen", "share", "prev-next", "show-info", "rtl"];
      for (const f of boolFields) {
        if (a[f] !== undefined) body[f.replace("-", "_")] = a[f] === "1" || a[f] === "true";
      }
      const strFields = ["title", "subtitle", "description", "background-color", "logo", "page-effect", "template", "tags", "private-notes", "url-path", "url-domain"];
      for (const f of strFields) {
        if (a[f] !== undefined) body[f.replace("-", "_")] = a[f];
      }
      const isAsync = a["async"] === true || a["async"] === "1";
      const path = isAsync ? "/async" : "/rest";
      const data = await req("POST", path, body);
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "flipbook-list": {
      const data = await req("GET", "/flipbook-list");
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "flipbook-details": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const data = await req("POST", "/flipbook-details", { id });
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "update-design": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const body = { id };
      const strFields = ["template", "title", "page-effect", "url-path", "url-domain"];
      for (const f of strFields) {
        if (a[f] !== undefined) body[f.replace("-", "_")] = a[f];
      }
      if (a["rtl"] !== undefined) body["rtl"] = a["rtl"] === "1" || a["rtl"] === "true";
      const data = await req("PATCH", "/flipbook-design", body);
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "flipbook-delete": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const data = await req("POST", "/flipbook-delete", { id });
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "bookshelf-list": {
      const data = await req("GET", "/bookshelf-list");
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "bookshelf-flipbooks": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const data = await req("POST", "/bookshelf-flipbooks", { id });
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "bookshelf-add": {
      const id = a["id"];
      const flipbookId = a["flipbook-id"];
      if (!id || !flipbookId) { console.error("--id and --flipbook-id required"); process.exit(1); }
      const body = { id, flipbook_id: flipbookId };
      if (a["position"] !== undefined) body["position"] = Number(a["position"]);
      const data = await req("POST", "/bookshelf-add", body);
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "bookshelf-remove": {
      const id = a["id"];
      const flipbookId = a["flipbook-id"];
      if (!id || !flipbookId) { console.error("--id and --flipbook-id required"); process.exit(1); }
      const data = await req("POST", "/bookshelf-remove", { id, flipbook_id: flipbookId });
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "flipbook-social": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const body = { id };
      const strFields = ["title", "description", "thumbnail"];
      for (const f of strFields) {
        if (a[f] !== undefined) body[f] = a[f];
      }
      const data = await req("POST", "/flipbook-social", body);
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    case "bookshelf-social": {
      const id = a["id"];
      if (!id) { console.error("--id required"); process.exit(1); }
      const body = { id };
      const strFields = ["title", "description", "thumbnail"];
      for (const f of strFields) {
        if (a[f] !== undefined) body[f] = a[f];
      }
      const data = await req("POST", "/bookshelf-social", body);
      console.log(JSON.stringify(data, null, 2));
      break;
    }
    default:
      console.error("Unknown command:", cmd);
      console.error("Try: convert, flipbook-list, flipbook-details, update-design, flipbook-delete, bookshelf-list, bookshelf-flipbooks, bookshelf-add, bookshelf-remove, flipbook-social, bookshelf-social");
      process.exit(1);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
