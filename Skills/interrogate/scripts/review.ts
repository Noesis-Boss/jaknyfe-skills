#!/usr/bin/env bun

/**
 * Interrogate reviewer fan-out.
 *
 * Each reviewer is an independent Zo session, so it never sees the parent
 * conversation, the other reviewers' output, or its own earlier attempts.
 * That independence is the whole point: the adversarial signal comes from
 * not sharing a context, not from an assigned persona.
 *
 *   bun run scripts/review.ts <manifest.json>
 *   bun run scripts/review.ts --list
 *
 * Manifest shape:
 *   {
 *     "intent": "one paragraph of stated intent",
 *     "scope": "diff or file contents under review",
 *     "models": ["byok:...", "byok:..."]   // 1-3 entries
 *   }
 */

const API_URL = "https://api.zo.computer/zo/ask";
const TEMPLATE = new URL("../references/reviewer-prompt.md", import.meta.url);
const RUBRIC = new URL("../references/rubric.md", import.meta.url);
const LENS = new URL("../references/code-quality-review.md", import.meta.url);

const MAX_REVIEWERS = 3;
const TIMEOUT_MS = 15 * 60 * 1000;

type Manifest = {
  intent?: string;
  scope?: string;
  models?: string[];
};

function fail(message: string): never {
  console.error(`interrogate: ${message}`);
  process.exit(1);
}

function fillTemplate(
  template: string,
  intent: string,
  scope: string,
  rubric: string,
  lens: string,
): string {
  return template
    .replaceAll("{INTENT}", intent)
    .replaceAll("{DIFF_OR_FILES}", scope)
    .replaceAll("{RUBRIC_CONTENTS}", rubric)
    .replaceAll("{CODE_QUALITY_CONTENTS}", lens);
}

async function readRequired(url: URL): Promise<string> {
  const file = Bun.file(url);
  if (!(await file.exists())) fail(`missing ${url.pathname}`);
  return file.text();
}

const TIMESTAMP_PREFIX = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}(:\d{2})? [A-Z]{2,5}\s*[-—–]\s*/;

function stripTimestamp(text: string): string {
  return text.trimStart().replace(TIMESTAMP_PREFIX, "").trimStart();
}

async function ask(prompt: string, model: string, label: string): Promise<string> {
  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
  if (!token) fail("ZO_CLIENT_IDENTITY_TOKEN is not set in this environment.");

  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);

  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        authorization: token,
        "content-type": "application/json",
      },
      body: JSON.stringify({ input: prompt, model_name: model }),
      signal: controller.signal,
    });

    if (!response.ok) {
      const body = await response.text();
      return `HTTP ${response.status} — ${body.slice(0, 400)}`;
    }

    const payload = (await response.json()) as { output?: string };
    return stripTimestamp(payload.output ?? "") || "empty response";
  } catch (error) {
    return `request failed — ${error instanceof Error ? error.message : String(error)}`;
  } finally {
    clearTimeout(timer);
    void label;
  }
}

async function main(): Promise<void> {
  const argv = process.argv.slice(2);

  if (argv.includes("--list")) {
    console.log(JSON.stringify({ max_reviewers: MAX_REVIEWERS, timeout_ms: TIMEOUT_MS }, null, 2));
    return;
  }

  const path = argv.find((arg) => !arg.startsWith("--"));
  if (!path) fail("usage: bun run scripts/review.ts <manifest.json>");

  const file = Bun.file(path);
  if (!(await file.exists())) fail(`no manifest at ${path}`);

  let manifest: Manifest;
  try {
    manifest = JSON.parse(await file.text());
  } catch (error) {
    fail(`manifest is not valid JSON — ${error instanceof Error ? error.message : String(error)}`);
  }

  if (!manifest.intent?.trim()) fail('manifest is missing "intent"');
  if (!manifest.scope?.trim()) fail('manifest is missing "scope"');

  const configured = (manifest.models ?? []).filter(Boolean);
  if (!configured.length) {
    fail(
      'manifest is missing "models". This skill exists to get independent voices — with no explicit model there is nothing to fan out to. Add a "models" array of 1-3 Zo model names.',
    );
  }
  if (configured.length === 1) {
    console.error(
      "interrogate: 1 model configured — you get one independent pass but no cross-model consensus. Two or more is the point of this skill.",
    );
  }
  if (configured.length > MAX_REVIEWERS) {
    console.error(
      `interrogate: ${configured.length} models configured, running the first ${MAX_REVIEWERS}. Each reviewer is a full billed session.`,
    );
  }

  const models = configured.slice(0, MAX_REVIEWERS);
  const [template, rubric, lens] = await Promise.all([
    readRequired(TEMPLATE),
    readRequired(RUBRIC),
    readRequired(LENS),
  ]);

  const prompt = fillTemplate(template, manifest.intent.trim(), manifest.scope.trim(), rubric, lens);
  const labelFor = (index: number) => `Reviewer ${String.fromCharCode(65 + index)}`;

  const results = await Promise.all(models.map((model, index) => ask(prompt, model, labelFor(index))));

  results.forEach((result, index) => {
    console.log(`## ${labelFor(index)} (${models[index]})`);
    console.log();
    console.log(result);
    console.log();
  });

  const families = new Set(models.map((model) => model.split(/[:/]/).pop()?.split("-")[0] ?? model));
  if (families.size < models.length) {
    console.log(
      `**Model-diversity caveat:** the ${models.length} reviewers do not span ${models.length} distinct model families. Agreement between them is weaker evidence than it looks — treat the Agreement Map as a consistency check, not independent corroboration.`,
    );
  }
}

await main();
