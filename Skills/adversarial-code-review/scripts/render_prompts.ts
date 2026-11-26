#!/usr/bin/env bun
// Render one adversarial reviewer prompt per lens from the canonical template.
//
// Usage:
//   bun render_prompts.ts --intent "..." --code-file <path> [--lenses skeptic,architect,minimalist]
//                        [--out <dir>] [--json]
//
//   bun render_prompts.ts --intent "..." --diff [--base main] [--paths a,b]
//
// Exit codes: 0 ok, 1 bad args / missing input, 2 template placeholders unfilled.

import {
  readFileSync,
  writeFileSync,
  mkdirSync,
  existsSync,
  mkdtempSync,
} from "node:fs";
import { parseArgs as parseArgsStrict } from "node:util";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const TEMPLATE = resolve(HERE, "../references/reviewer-prompt-template.md");

const LENSES: Record<string, string> = {
  skeptic: [
    "You are the Skeptic. Your job is to break the change: prove the stated intent is",
    "not actually met, find the paths that crash, the states that go stale, the inputs",
    "that produce wrong output silently. Trace call chains; do not assert possibilities.",
    "You are NOT here to evaluate code style. Correctness and root cause only.",
  ].join(" "),
  architect: [
    "You are the Architect. Judge whether this change belongs where it was put: the",
    "layer, the module, the contract. Look for bolted-on logic, duplicated helpers,",
    "wrong-layer responsibility, legacy dual-paths, and data structures that fight the",
    "access patterns. Also weigh complexity budget: dead code, single-call-site",
    "abstractions, speculative configuration. Do not nitpick naming.",
  ].join(" "),
  minimalist: [
    "You are the Minimalist. Assume a code-judo move exists that deletes whole branches,",
    "helpers, or layers without changing behavior. Name the reframing concretely, and",
    "show which code it deletes. Reject premature abstraction and 'just in case' paths.",
    "Behavior-preserving simplification is the deliverable; commentary without a named",
    "deletion or restructure is not a finding.",
  ].join(" "),
  security: [
    "You are the Security Reviewer. Only security. For each finding, trace the input",
    "path from its origin to the dangerous sink and show it: untrusted input reaching",
    "SQL, shell, eval, innerHTML, filesystem paths, deserializers; authn/authz gaps on",
    "new endpoints; secrets in code, logs, or error messages; TOCTOU in security-",
    "critical paths. A security finding without a traced path is not a finding.",
  ].join(" "),
  verifier: [
    "You are the Verifier. Can you tell this code works from reading it? Audit the",
    "test surface: behavior vs implementation details, whether the specific bug being",
    "fixed has a regression test, whether integration boundaries are covered end to",
    "end, and whether any check reads a proxy (mtime, cached state, self-reported",
    "summary) instead of the real value.",
  ].join(" "),
};

function parseArgsStrictOptions(argv: string[]) {
  // node:util.parseArgs enforces the switch/value distinction at the boundary,
  // so a bare `--intent` is a parse error rather than a boolean leaking into
  // `.trim()`. Unknown options and unknown values both fail here, loudly.
  let values: {
    intent?: string;
    "code-file"?: string;
    lenses?: string;
    out?: string;
    base?: string;
    paths?: string;
    diff?: boolean;
    json?: boolean;
  };
  try {
    ({ values } = parseArgsStrict({
      args: argv,
      options: {
        intent: { type: "string" },
        "code-file": { type: "string" },
        lenses: { type: "string" },
        out: { type: "string" },
        base: { type: "string" },
        paths: { type: "string" },
        diff: { type: "boolean" },
        json: { type: "boolean" },
      },
      allowPositionals: false,
    }));
  } catch (err) {
    // node:util.parseArgs throws with a useful code and a message aimed at
    // library callers. Normalize to the documented one-line exit-1 contract.
    const e = err as { code?: string; message?: string };
    const detail =
      e.code === "ERR_PARSE_ARGS_UNKNOWN_OPTION"
        ? "unknown option"
        : e.code === "ERR_PARSE_ARGS_INVALID_OPTION_VALUE"
          ? "bad option value"
          : "could not parse arguments";
    process.stderr.write(`error: ${detail}; run with --help for usage\n`);
    process.exit(1);
  }
  return values;
}

const DEFAULT_LENSES = "skeptic,architect,minimalist";

function splitList(value: string): string[] {
  return value
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

function git(args: string[]): string {
  const r = Bun.spawnSync(["git", ...args], { stdout: "pipe", stderr: "pipe" });
  if (r.exitCode !== 0) {
    process.stderr.write(`git ${args.join(" ")} failed: ${r.stderr.toString()}\n`);
    process.exit(1);
  }
  return r.stdout.toString();
}

function main(): void {
  const args = parseArgsStrictOptions(process.argv.slice(2));
  const intent = args.intent?.trim() ?? "";
  if (!intent) {
    process.stderr.write("error: --intent is required\n");
    process.exit(1);
  }

  let code: string;
  const codeFile = args["code-file"];
  if (codeFile !== undefined) {
    const p = resolve(codeFile);
    if (!existsSync(p)) {
      process.stderr.write(`error: code file not found: ${p}\n`);
      process.exit(1);
    }
    code = readFileSync(p, "utf8");
  } else if (args.diff) {
    const base = args.base ?? "HEAD";
    const diffArgs = ["diff", base];
    // Each path must be its own argv element. Passing "a,b" as a single
    // pathspec makes git match neither path and silently return an empty diff.
    if (args.paths !== undefined) {
      const paths = splitList(args.paths);
      if (paths.length === 0) {
        process.stderr.write("error: --paths was given but resolved to no paths\n");
        process.exit(1);
      }
      diffArgs.push("--", ...paths);
    }
    const diff = git(diffArgs);
    if (!diff.trim()) {
      const scope = args.paths !== undefined ? ` and paths ${args.paths}` : "";
      process.stderr.write(`error: empty diff for base "${base}"${scope}\n`);
      process.exit(1);
    }
    code = diff;
  } else {
    process.stderr.write("error: pass --code-file <path> or --diff\n");
    process.exit(1);
  }

  const lensNames = splitList(args.lenses ?? DEFAULT_LENSES);
  if (lensNames.length === 0) {
    process.stderr.write(
      `error: --lenses selected no reviewers; known: ${Object.keys(LENSES).join(", ")}\n`,
    );
    process.exit(1);
  }

  for (const name of lensNames) {
    if (!Object.hasOwn(LENSES, name)) {
      process.stderr.write(
        `error: unknown lens "${name}". known: ${Object.keys(LENSES).join(", ")}\n`,
      );
      process.exit(1);
    }
  }

  const template = readFileSync(TEMPLATE, "utf8");

  // Validate the template itself, before substitution. Scanning the rendered
  // prompt for `{{...}}` is wrong: the code under review legitimately contains
  // placeholder-looking strings, and this script is one of them.
  const known = new Set(["{{INTENT}}", "{{LENS}}", "{{CODE}}"]);
  const unresolved = (template.match(/\{\{[A-Z_]+\}\}/g) ?? []).filter(
    (ph) => !known.has(ph),
  );
  if (unresolved.length) {
    process.stderr.write(
      `error: template has unknown placeholder(s): ${[...new Set(unresolved)].join(", ")}\n`,
    );
    process.exit(2);
  }
  for (const ph of known) {
    if (!template.includes(ph)) {
      process.stderr.write(`error: template is missing ${ph}\n`);
      process.exit(2);
    }
  }

  // Each render is a self-contained job directory. Replacing the directory
  // wholesale, rather than writing this run's lenses over the last run's, is
  // what makes the set coherent: a prompt set can never be a mix of two
  // changes. `mkdtempSync` is atomic and refuses an existing path, so a
  // repository cannot pre-place a symlink to redirect the write.
  const outRoot = resolve(args.out ?? ".");
  mkdirSync(outRoot, { recursive: true });
  const outDir = mkdtempSync(join(outRoot, "acr-review-"));

  const written: { lens: string; path: string }[] = [];
  for (const name of lensNames) {
    const values: Record<string, string> = {
      "{{INTENT}}": intent.trim(),
      "{{LENS}}": LENSES[name],
      "{{CODE}}": code.trim(),
    };
    // Single pass so substituted values are never rescanned for placeholders.
    const prompt = template.replace(
      /\{\{(INTENT|LENS|CODE)\}\}/g,
      (m) => values[m],
    );
    const p = resolve(outDir, `${name}.prompt.md`);
    writeFileSync(p, prompt);
    written.push({ lens: name, path: p });
  }

  if (args.json) {
    console.log(JSON.stringify({ outDir, prompts: written }, null, 2));
  } else {
    console.log(outDir);
    for (const w of written) console.log(`${w.lens}\t${w.path}`);
  }
}

main();
