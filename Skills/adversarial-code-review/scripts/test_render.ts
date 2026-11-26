#!/usr/bin/env bun
// Regression tests for render_prompts.ts. Every case below is a bug that was
// actually found by an adversarial reviewer run, so a regression means a real
// defect is back, not a stylistic drift.
//
// Usage: bun scripts/test_render.ts   (exit 0 pass, 1 fail)

import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const RENDER = join(HERE, "render_prompts.ts");
const SKILL_MD = resolve(HERE, "..", "SKILL.md");

let pass = 0;
const failures: string[] = [];

function run(args: string[]) {
  const r = Bun.spawnSync(["bun", RENDER, ...args], { stdout: "pipe", stderr: "pipe" });
  return {
    code: r.exitCode,
    out: r.stdout.toString(),
    err: r.stderr.toString(),
  };
}

function check(name: string, cond: boolean, detail = "") {
  if (cond) {
    pass++;
    return;
  }
  failures.push(`${name}${detail ? ` — ${detail}` : ""}`);
}

function expectFail(name: string, args: string[], wantExit: number) {
  const { code, err, out } = run(args);
  const all = out + err;
  check(name, code === wantExit, `exit=${code} want=${wantExit}`);
  check(`${name}: no stack trace`, !/at \w+ \(/.test(all), all.slice(0, 200));
  check(`${name}: one-line error`, all.trim().split("\n").length <= 2, all.slice(0, 200));
}

// --- arg validation: exit 1, clean message, no stack trace ------------------
expectFail("bare value option", ["--intent", "--code-file", SKILL_MD], 1);
expectFail("flag given a value", ["--intent", "x", "--diff=yes", "--code-file", SKILL_MD], 1);
expectFail("unknown option", ["--intent", "x", "--code-file", SKILL_MD, "--bogus", "y"], 1);
expectFail("stray positional", ["stray", "--intent", "x", "--code-file", SKILL_MD], 1);
expectFail("missing intent", ["--code-file", SKILL_MD], 1);
expectFail("missing code file", ["--intent", "x", "--code-file", "/nope.ts"], 1);

// --- empty lens list must not report success --------------------------------
expectFail("empty lens list", ["--intent", "x", "--code-file", SKILL_MD, "--lenses", ","], 1);
expectFail("blank lens list", ["--intent", "x", "--code-file", SKILL_MD, "--lenses", " , ,"], 1);

// --- happy path -------------------------------------------------------------
{
  const out = mkdtempSync(join(tmpdir(), "acr-t-"));
  const { code } = run([
    "--intent", "smoke test",
    "--code-file", SKILL_MD,
    "--lenses", "skeptic,security,minimalist",
    "--out", out,
  ]);
  check("render exit 0", code === 0, `exit=${code}`);
  const files = readdirSync(out).sort();
  check(
    "one prompt per lens",
    files.join(",") === "minimalist.prompt.md,security.prompt.md,skeptic.prompt.md",
    files.join(","),
  );
  for (const f of files) {
    const body = readFileSync(join(out, f), "utf8");
    check(`${f}: intent filled`, body.includes("smoke test"));
    check(`${f}: no template placeholders`, !/\{\{(INTENT|LENS|CODE)\}\}/.test(body));
  }
  rmSync(out, { recursive: true, force: true });
}

// --- every lens injects its own focus text ----------------------------------
{
  const out = mkdtempSync(join(tmpdir(), "acr-t-"));
  run([
    "--intent", "x", "--code-file", SKILL_MD,
    "--lenses", "skeptic,architect,minimalist,security,verifier",
    "--out", out,
  ]);
  const bodies = readdirSync(out).map((f) => readFileSync(join(out, f), "utf8"));
  check("lenses are distinct", new Set(bodies).size === bodies.length, "duplicate prompts");
  const all = bodies.join("\n");
  for (const role of ["You are the Skeptic", "You are the Architect", "You are the Minimalist",
                      "You are the Security Reviewer", "You are the Verifier"]) {
    check(`lens role present: ${role}`, all.includes(role));
  }
  rmSync(out, { recursive: true, force: true });
}

// --- reviewed code may itself contain {{...}} -------------------------------
// Regression: a post-substitution scan for `{{...}}` rejected the renderer's own
// source as a review target, because that source contains the placeholder tokens.
{
  const out = mkdtempSync(join(tmpdir(), "acr-t-"));
  const self = join(HERE, "render_prompts.ts");
  const { code, err } = run(["--intent", "x", "--code-file", self, "--lenses", "skeptic", "--out", out]);
  check("self-referential code renders", code === 0, err.slice(0, 200));
  rmSync(out, { recursive: true, force: true });
}

// --- --paths must be split into separate argv entries -----------------------
// Regression: "a,b" passed as one pathspec matched neither path, so git diff
// succeeded with empty output and the prompt contained none of the change.
{
  const out = mkdtempSync(join(tmpdir(), "acr-t-"));
  const { code } = run([
    "--intent", "x",
    "--diff", "--base", "HEAD",
    "--paths", `${SKILL_MD},${join(HERE, "render_prompts.ts")}`,
    "--lenses", "skeptic",
    "--out", out,
  ]);
  check("comma-joined --paths renders", code === 0, `exit=${code}`);
  rmSync(out, { recursive: true, force: true });
}
expectFail("--paths with no real paths", ["--intent", "x", "--diff", "--base", "HEAD", "--paths", ","], 1);

if (failures.length) {
  process.stderr.write(`FAIL ${failures.length} check(s), ${pass} passed\n`);
  for (const f of failures) process.stderr.write(`  - ${f}\n`);
  process.exit(1);
}
process.stdout.write(`ok: ${pass} checks passed\n`);
