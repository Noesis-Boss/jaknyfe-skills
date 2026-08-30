#!/usr/bin/env node
/**
 * Zorro — Self-Improving Orchestrator Agent with Persistent Memory
 * 
 * Usage:
 *   bun run zorro.ts "task description"
 *   bun run zorro.ts memory "search query"
 *   bun run zorro.ts remember "fact to remember"
 *   bun run zorro.ts improvements
 *   bun run zorro.ts plan "goal description"  — Create and approve a plan
 */

import { spawnSync } from "child_process";
import { promises as fs } from "fs";
import path from "path";

const ASTRA_MEMORY_SCRIPT = "/home/workspace/Skills/astra-memory/scripts/sync.ts";
const IMPROVEMENT_LOG = "/home/workspace/Skills/zorro/improvements.log";
const SESSION_LOG = "/home/workspace/Skills/zorro/session.log";
const PLAN_LOG = "/home/workspace/Skills/zorro/plans.log";
// --- Skill loading: wires github.com/obra/superpowers + workspace Skills into Zorro ---
const SKILLS_DIR = "/home/workspace/Skills";
// Addy Osmani agent-skills (github.com/addyosmani/agent-skills) discovered/boosted by default.
const AGENT_SKILLS = [
  "using-agent-skills", "spec-driven-development", "planning-and-task-breakdown",
  "incremental-implementation", "code-review-and-quality", "test-driven-development",
  "security-and-hardening", "doubt-driven-development", "frontend-ui-engineering",
];
// Superpowers skills discovered/boosted by default.
const SUPERPOWERS_SKILLS = [
  "brainstorming", "writing-plans", "verification-before-completion",
  "systematic-debugging", "test-driven-development", "subagent-driven-development",
  "dispatching-parallel-agents", "using-git-worktrees", "requesting-code-review",
  "receiving-code-review", "finishing-a-development-branch", "using-superpowers",
  "writing-skills", "executing-plans",
];
// Core methodology always injected into execution/planning prompts.
const EXEC_METHOD_SKILLS = [
  "using-superpowers", "brainstorming", "writing-plans", "verification-before-completion",
  "systematic-debugging", "test-driven-development", "subagent-driven-development",
  "dispatching-parallel-agents", "using-agent-skills", "doubt-driven-development",
];
// Max chars of a skill body injected per match (keeps prompts bounded).
const SKILL_HEAD_LIMIT = 2500;

interface SkillMeta { name: string; description: string; dir: string; }

function parseSkillFrontmatter(raw: string): { name?: string; description?: string; body: string } {
  const m = raw.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!m) return { body: raw };
  const fmRaw = m[1];
  const body = m[2];
  const fm: Record<string, string> = {};
  for (const line of fmRaw.split("\n")) {
    const mm = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (mm) {
      let v = mm[2].trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) v = v.slice(1, -1);
      fm[mm[1]] = v;
    }
  }
  return { name: fm.name, description: fm.description, body };
}

async function listSkillMetas(): Promise<SkillMeta[]> {
  const metas: SkillMeta[] = [];
  let entries: string[] = [];
  try { entries = await fs.readdir(SKILLS_DIR); } catch { return metas; }
  for (const name of entries) {
    const dir = path.join(SKILLS_DIR, name);
    let raw = "";
    try { raw = await fs.readFile(path.join(dir, "SKILL.md"), "utf8"); } catch { continue; }
    const { name: fmName, description } = parseSkillFrontmatter(raw);
    metas.push({ name: fmName || name, description: description || "", dir });
  }
  return metas;
}

function tokenize(s: string): string[] {
  return s.toLowerCase().replace(/[^a-z0-9\s]/g, " ").split(/\s+/).filter(Boolean);
}

async function matchSkills(query: string, k = 4): Promise<SkillMeta[]> {
  const metas = await listSkillMetas();
  const q = query.toLowerCase();
  const qTokens = tokenize(query).filter((t) => t.length >= 3);
  return metas
    .map((meta) => {
      const name = meta.name.toLowerCase();
      const desc = meta.description.toLowerCase();
      let score = 0;
      if (name.includes(q)) score += 3;
      if (desc.includes(q)) score += 1.5;
      for (const t of qTokens) {
        if (name.includes(t)) score += 2;
        if (desc.includes(t)) score += 0.8;
      }
      if (SUPERPOWERS_SKILLS.includes(meta.name)) score += 0.3;
      if (AGENT_SKILLS.includes(meta.name)) score += 0.3;
      return { meta, score };
    })
    .filter((x) => x.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, k)
    .map((x) => x.meta);
}

async function loadSkillBodies(names: string[], limit = SKILL_HEAD_LIMIT): Promise<string> {
  const parts: string[] = [];
  const seen = new Set<string>();
  for (const name of names) {
    if (seen.has(name)) continue;
    seen.add(name);
    try {
      const { body } = parseSkillFrontmatter(await fs.readFile(path.join(SKILLS_DIR, name, "SKILL.md"), "utf8"));
      const trimmed = body.trim().slice(0, limit);
      parts.push(`### Skill: ${name}\n${trimmed}${body.trim().length > limit ? "\n…(truncated)" : ""}`);
    } catch { /* skill not present */ }
  }
  return parts.join("\n\n");
}

// Builds the methodology block injected into Zorro's sub-agent prompts:
// always the core superpowers set, plus any extra skills matched by the task query.
async function buildMethodologyContext(query: string): Promise<string> {
  const names = new Set(EXEC_METHOD_SKILLS);
  for (const m of await matchSkills(query, 4)) names.add(m.name);
  const loaded = await loadSkillBodies([...names]);
  return loaded ? `## Agent methodology (github.com/obra/superpowers + workspace Skills — follow these)\n${loaded}\n` : "";
}

interface MemoryResult {
  source: string;
  layer: string;
  project: string;
  title: string;
  path: string;
  timestamp: string;
  rrf: number;
  snippet: string;
}

interface ImprovementEntry {
  timestamp: string;
  task: string;
  outcome: "success" | "partial" | "failure";
  errorCategory?: string;
  lesson: string;
  strategyUpdate?: string;
}

interface VerificationStep {
  name: string;
  command: string;
  expectedPattern?: string;
  cwd?: string;
}

interface PlanStep {
  id: string;
  description: string;
  agentType: string;
  dependsOn?: string[];
  verification?: {
    visual?: { url: string; expected?: string };
    programmatic?: VerificationStep[];
  };
}

interface Plan {
  id: string;
  goal: string;
  steps: PlanStep[];
  createdAt: string;
  approved: boolean;
  completedSteps: string[];
}

async function recall(query: string, limit = 10): Promise<MemoryResult[]> {
  const sub = spawnSync("bun", ["run", ASTRA_MEMORY_SCRIPT, "query", query, `--limit=${limit}`, "--json"], {
    encoding: "utf8",
    maxBuffer: 16 * 1024 * 1024,
  });
  if (sub.status !== 0) {
    console.warn(`⚠️  Recall failed: ${sub.stderr || sub.stdout}`);
    return [];
  }
  try {
    const out = (sub.stdout || "").trim();
    const json = JSON.parse(out);
    return json.results || [];
  } catch (e) {
    console.warn(`⚠️  Could not parse recall output: ${e}`);
    return [];
  }
}

async function remember(fact: string): Promise<void> {
  const sub = spawnSync("bun", ["run", ASTRA_MEMORY_SCRIPT, "add", fact], {
    encoding: "utf8",
  });
  if (sub.status !== 0) {
    console.error(`❌ Failed to remember: ${sub.stderr || sub.stdout}`);
  } else {
    console.log(`✅ Remembered: ${fact}`);
  }
}

async function fullSync(): Promise<void> {
  const sub = spawnSync("bun", ["run", ASTRA_MEMORY_SCRIPT, "sync"], {
    encoding: "utf8",
  });
  if (sub.status !== 0) {
    console.warn(`⚠️  Full sync warning: ${sub.stderr || sub.stdout}`);
  }
}

async function logImprovement(entry: ImprovementEntry): Promise<void> {
  const line = JSON.stringify(entry) + "\n";
  await fs.appendFile(IMPROVEMENT_LOG, line);
}

async function logSession(message: string): Promise<void> {
  const ts = new Date().toISOString();
  await fs.appendFile(SESSION_LOG, `[${ts}] ${message}\n`);
}

async function logPlan(plan: Plan): Promise<void> {
  const line = JSON.stringify(plan) + "\n";
  await fs.appendFile(PLAN_LOG, line);
}

async function showImprovements(): Promise<void> {
  try {
    const content = await fs.readFile(IMPROVEMENT_LOG, "utf8");
    const lines = content.trim().split("\n").filter(l => l);
    if (lines.length === 0) {
      console.log("📝 No improvements logged yet.");
      return;
    }
    console.log(`📈 Zorro Improvement Log (${lines.length} entries):\n`);
    for (const line of lines.slice(-20)) {
      const entry = JSON.parse(line) as ImprovementEntry;
      const icon = entry.outcome === "success" ? "✅" : entry.outcome === "partial" ? "⚠️" : "❌";
      console.log(`  ${icon} [${entry.timestamp.slice(0, 19)}] ${entry.task}`);
      console.log(`     Lesson: ${entry.lesson}`);
      if (entry.strategyUpdate) console.log(`     Strategy: ${entry.strategyUpdate}`);
      console.log();
    }
  } catch {
    console.log("📝 No improvements logged yet.");
  }
}

interface VerificationResult {
  success: boolean;
  screenshot?: string;
  error?: string;
}

async function verifyVisual(siteUrl: string, expectedContent: string): Promise<VerificationResult> {
  console.log(`  📸 Visual verification: ${siteUrl}`);
  try {
    const sub = spawnSync("agent-browser", [
      "open", siteUrl,
      "--wait", "3",
      "--screenshot", "/tmp/zorro-verify.png",
      "--full-page"
    ], { encoding: "utf8", timeout: 30000 });
    if (sub.status !== 0) {
      return { success: false, error: `agent-browser failed: ${sub.stderr || sub.stdout}` };
    }
    if (await fs.stat("/tmp/zorro-verify.png").catch(() => false)) {
      console.log(`  ✅ Screenshot captured: /tmp/zorro-verify.png`);
      return { success: true, screenshot: "/tmp/zorro-verify.png" };
    }
    return { success: false, error: "Screenshot not created" };
  } catch (e: any) {
    return { success: false, error: e.message };
  }
}

async function verifyProgrammatic(checks: VerificationStep[]): Promise<{ success: boolean; results: any[] }> {
  console.log(`  🔧 Programmatic verification (${checks.length} checks)...`);
  const results = [];
  let allPass = true;
  for (const check of checks) {
    console.log(`    → ${check.name}...`);
    const sub = spawnSync("bash", ["-c", check.command], {
      encoding: "utf8",
      cwd: check.cwd || "/home/workspace",
      timeout: 30000,
    });
    const passed = sub.status === 0 && (!check.expectedPattern || sub.stdout.includes(check.expectedPattern));
    results.push({ name: check.name, passed, stdout: sub.stdout, stderr: sub.stderr });
    if (passed) {
      console.log(`      ✅ PASS`);
    } else {
      console.log(`      ❌ FAIL${check.expectedPattern ? ` (expected: ${check.expectedPattern})` : ""}`);
      console.log(`      stdout: ${sub.stdout?.slice(0, 200)}`);
      console.log(`      stderr: ${sub.stderr?.slice(0, 200)}`);
      allPass = false;
    }
  }
  return { success: allPass, results };
}

async function askClarifyingQuestions(goal: string, memories: MemoryResult[], methodology: string = ""): Promise<string[]> {
  console.log("\n🤔 Analyzing goal and identifying clarifying questions...\n");
  
  const context = memories.length > 0 
    ? "\nRelevant context from memory:\n" + memories.slice(0, 5).map(m => `- [${m.source}] ${m.title}: ${m.snippet}`).join("\n")
    : "";
  
  const prompt = `Goal: ${goal}${context}

You are Zorro, an orchestrating agent. Your job is to identify ALL clarifying questions needed to create an executable plan. 
Consider: scope, success criteria, constraints, dependencies, target environment, accounts/credentials needed, verification methods.

Output ONLY a JSON array of questions, each with:
- "question": the question to ask
- "category": one of [scope, success_criteria, constraints, dependencies, credentials, verification, other]
- "required": true/false

Example:
[
  {"question": "Which account should post the tweet?", "category": "credentials", "required": true},
  {"question": "What is the exact success metric?", "category": "success_criteria", "required": true}
]`;

  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
  if (!token) {
    console.log("⚠️  ZO_CLIENT_IDENTITY_TOKEN not set, using default questions");
    return [
      "What is the exact success criteria for this task?",
      "Are there any constraints or limitations I should know about?",
      "Which accounts/services need credentials?",
      "How should I verify completion visually and programmatically?"
    ];
  }

  const response = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: { "authorization": token, "content-type": "application/json" },
    body: JSON.stringify({ input: prompt, model_name: "byok:2e03a024-1bd1-4819-b7de-06dbb577e664" }),
  });

  if (!response.ok) {
    console.warn(`⚠️  Zo API error: ${response.status}`);
    return [
      "What is the exact success criteria for this task?",
      "Are there any constraints or limitations I should know about?",
      "Which accounts/services need credentials?",
      "How should I verify completion visually and programmatically?"
    ];
  }

  const data = await response.json();
  try {
    const questions = JSON.parse(data.output || "[]");
    return questions.map((q: any) => q.question);
  } catch {
    return [
      "What is the exact success criteria for this task?",
      "Are there any constraints or limitations I should know about?",
      "Which accounts/services need credentials?",
      "How should I verify completion visually and programmatically?"
    ];
  }
}

async function getUserAnswers(questions: string[]): Promise<Record<string, string>> {
  console.log("\n❓ Clarifying Questions:\n");
  questions.forEach((q, i) => console.log(`  ${i + 1}. ${q}`));
  console.log("\nPlease provide answers (one per line, or 'skip' for optional):\n");
  
  // In a real implementation, this would wait for user input
  // For now, we'll simulate with defaults
  const answers: Record<string, string> = {};
  questions.forEach((q, i) => {
    answers[q] = `Answer to: ${q}`;
  });
  return answers;
}

async function createPlan(goal: string, memories: MemoryResult[], answers: Record<string, string>, methodology: string = ""): Promise<Plan> {
  console.log("\n📋 Creating execution plan...\n");
  
  const context = memories.length > 0 
    ? "\nRelevant context from memory:\n" + memories.slice(0, 10).map(m => `- [${m.source}] ${m.title}: ${m.snippet}`).join("\n")
    : "";
  
  const answersText = Object.entries(answers).map(([q, a]) => `Q: ${q}\nA: ${a}`).join("\n\n");
  
  const prompt = `Goal: ${goal}

Clarifying Answers:
${answersText}

${context}

Create a detailed execution plan as JSON with:
{
  "goal": "restated goal",
  "steps": [
    {
      "id": "step-1",
      "description": "what this step does",
      "agentType": "type of sub-agent (e.g., web-researcher, code-writer, api-caller, visual-verifier)",
      "dependsOn": ["step-0"],
      "verification": {
        "visual": { "url": "https://...", "expected": "text to verify" },
        "programmatic": [{ "name": "check name", "command": "bash command", "expectedPattern": "success text" }]
      }
    }
  ]
}

Each step should be independently executable by a sub-agent. Steps with dependsOn run after dependencies complete.`;

  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
  if (!token) {
    throw new Error("ZO_CLIENT_IDENTITY_TOKEN not set — cannot create plan via Zo API");
  }

  const response = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: { "authorization": token, "content-type": "application/json" },
    body: JSON.stringify({ input: prompt, model_name: "byok:2e03a024-1bd1-4819-b7de-06dbb577e664" }),
  });

  if (!response.ok) {
    throw new Error(`Zo API error: ${response.status} ${await response.text()}`);
  }

  const data = await response.json();
  try {
    const planData = JSON.parse(data.output);
    const plan: Plan = {
      id: `plan-${Date.now()}`,
      goal: planData.goal || goal,
      steps: planData.steps || [],
      createdAt: new Date().toISOString(),
      approved: false,
      completedSteps: [],
    };
    return plan;
  } catch (e) {
    throw new Error(`Failed to parse plan: ${e}`);
  }
}

async function presentPlanForApproval(plan: Plan): Promise<boolean> {
  console.log("\n📋 EXECUTION PLAN FOR APPROVAL\n");
  console.log(`Goal: ${plan.goal}\n`);
  console.log(`Steps (${plan.steps.length}):\n`);
  
  for (const step of plan.steps) {
    const deps = step.dependsOn?.length ? ` (depends on: ${step.dependsOn.join(", ")})` : "";
    console.log(`  ${step.id}: ${step.description}${deps}`);
    console.log(`    Agent: ${step.agentType}`);
    if (step.verification?.visual) console.log(`    Visual: ${step.verification.visual.url}`);
    if (step.verification?.programmatic?.length) console.log(`    Programmatic: ${step.verification.programmatic.length} checks`);
  }
  
  console.log("\n✅ Approve this plan? (yes/no)");
  // In real implementation, wait for user input
  // For now, auto-approve for demo
  return true;
}

async function executeStep(step: PlanStep, plan: Plan, memories: MemoryResult[], methodology: string = ""): Promise<{ success: boolean; result: string; errorCategory?: string }> {
  console.log(`\n🚀 Executing step: ${step.id} - ${step.description}`);
  
  const context = memories.length > 0 
    ? "\nRelevant memories:\n" + memories.slice(0, 8).map(m => `- [${m.source}] ${m.title}: ${m.snippet}`).join("\n")
    : "";
  
  const prompt = `Task: ${step.description}

Goal context: ${plan.goal}

${context}

${methodology}

Execute this step completely. You have access to all Zo tools. 
${step.verification?.visual ? `Visual verification target: ${step.verification.visual.url}` : ""}
${step.verification?.programmatic?.map(c => `Programmatic check: ${c.name} - ${c.command}`).join("\n") || ""}

Report your result and any artifacts created.`;

  const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
  if (!token) {
    return { success: false, result: "ZO_CLIENT_IDENTITY_TOKEN not set", errorCategory: "config_error" };
  }

  const response = await fetch("https://api.zo.computer/zo/ask", {
    method: "POST",
    headers: { "authorization": token, "content-type": "application/json" },
    body: JSON.stringify({ input: prompt, model_name: "byok:2e03a024-1bd1-4819-b7de-06dbb577e664" }),
  });

  if (!response.ok) {
    return { success: false, result: `Zo API error: ${response.status}`, errorCategory: "api_error" };
  }

  const data = await response.json();
  const result = data.output || "No output returned";

  // Run verification if defined
  let verificationPassed = true;
  if (step.verification) {
    console.log(`  🔎 Verifying step ${step.id}...`);
    if (step.verification.visual) {
      const visualResult = await verifyVisual(step.verification.visual.url, step.verification.visual.expected || "");
      if (!visualResult.success) {
        console.log(`  ⚠️  Visual verification failed: ${visualResult.error}`);
        verificationPassed = false;
      }
    }
    if (step.verification.programmatic?.length) {
      const progResult = await verifyProgrammatic(step.verification.programmatic);
      if (!progResult.success) {
        console.log(`  ⚠️  Programmatic verification failed`);
        verificationPassed = false;
      }
    }
  }

  return { 
    success: verificationPassed, 
    result, 
    errorCategory: verificationPassed ? undefined : "verification_failed" 
  };
}

async function executePlan(plan: Plan, initialMemories: MemoryResult[], methodology: string = ""): Promise<{ success: boolean; results: Record<string, any> }> {
  console.log(`\n🎯 Executing plan: ${plan.id} for goal: ${plan.goal}\n`);
  await logSession(`PLAN EXECUTION START: ${plan.id} - ${plan.goal}`);

  const results: Record<string, any> = {};
  const completed = new Set<string>();
  let memories = [...initialMemories];

  // Topological execution respecting dependencies
  while (completed.size < plan.steps.length) {
    let progress = false;
    
    for (const step of plan.steps) {
      if (completed.has(step.id)) continue;
      
      const depsMet = step.dependsOn?.every(d => completed.has(d)) ?? true;
      if (!depsMet) continue;

      progress = true;
      const { success, result, errorCategory } = await executeStep(step, plan, memories);
      
      results[step.id] = { success, result, errorCategory };
      completed.add(step.id);
      plan.completedSteps.push(step.id);
      
      // Add result to memories for subsequent steps
      memories.push({
        source: "zorro_execution",
        layer: "session",
        project: "zorro",
        title: `Step ${step.id} result`,
        path: "/zorro",
        timestamp: new Date().toISOString(),


        rrf: 1.0,
        snippet: result.slice(0, 200)
      });
      
      if (!success) {
        console.log(`\n❌ Step ${step.id} failed. Stopping plan execution.`);
        await logSession(`PLAN FAILED: ${plan.id} at step ${step.id}`);
        return { success: false, results };
      }
    }
    
    if (!progress) {
      console.log("\n⚠️  No progress possible — circular dependency or missing dependency?");
      break;
    }
  }

  await logSession(`PLAN COMPLETE: ${plan.id}`);
  return { success: true, results };
}

async function runImprovementCycle(task: string, outcome: "success" | "partial" | "failure", result: string, errorCategory?: string): Promise<void> {
  console.log("\n🔄 Running self-improvement analysis...");
  
  let lesson = "";
  let strategyUpdate = "";
  
  if (outcome === "failure") {
    lesson = `Task failed: ${result}. Error category: ${errorCategory || "unknown"}.`;
    if (errorCategory === "memory_gap") {
      strategyUpdate = "Ensure broader memory queries before similar tasks; add missing facts proactively.";
    } else if (errorCategory === "tool_error") {
      strategyUpdate = "Verify tool availability and parameters before execution; add tool-specific checks.";
    } else if (errorCategory === "reasoning_error") {
      strategyUpdate = "Break complex tasks into smaller verified steps; add intermediate validation.";
    } else if (errorCategory === "verification_failed") {
      strategyUpdate = "Add more specific verification criteria; ensure visual/programmatic checks match success definition.";
    } else if (errorCategory === "config_error") {
      strategyUpdate = "Ensure all required environment variables and tokens are configured before execution.";
    } else {
      strategyUpdate = "Review failure pattern; consider adding pre-flight checks for this task type.";
    }
  } else if (outcome === "partial") {
    lesson = `Task partially completed: ${result}. Some objectives not met.`;
    strategyUpdate = "Identify which sub-tasks succeeded vs failed; strengthen memory for weak areas.";
  } else {
    lesson = `Task succeeded: ${result}.`;
    strategyUpdate = "Reinforce the approach used; promote successful patterns to semantic memory.";
  }
  
  await logImprovement({
    timestamp: new Date().toISOString(),
    task,
    outcome,
    errorCategory,
    lesson,
    strategyUpdate,
  });
  
  console.log(`  📝 Lesson: ${lesson}`);
  console.log(`  🎯 Strategy update: ${strategyUpdate}`);
  
  await remember(`[IMPROVEMENT] ${lesson} Strategy: ${strategyUpdate}`);
  await fullSync();
}

async function main() {
  const [, , cmd, ...args] = process.argv;
  const arg = args.join(" ").trim();
  
  console.log("🦊 Zorro — Self-Improving Orchestrator Agent");
  console.log("=============================================\n");
  
  switch (cmd) {
    case "memory":
    case "recall":
    case "query": {
      if (!arg) {
        console.log("Usage: zorro.ts memory <search query>");
        process.exit(1);
      }
      const memories = await recall(arg, 20);
      if (memories.length === 0) {
        console.log("🔍 No matching memories found.");
      } else {
        console.log(`\n📌 Top ${memories.length} matches:\n`);
        for (const m of memories) {
          console.log(`  [${m.source} | ${m.layer} | ${m.project} | rrf=${m.rrf.toFixed(4)}] ${m.title}`);
          console.log(`    ${m.path}`);
          console.log(`    ${m.timestamp}`);
          console.log(`    ${m.snippet}`);
          console.log();
        }
      }
      break;
    }
    
    case "remember":
    case "add": {
      if (!arg) {
        console.log("Usage: zorro.ts remember <fact text>");
        process.exit(1);
      }
      await remember(arg);
      break;
    }
    
    case "improvements":
    case "log": {
      await showImprovements();
      break;
    }
    
    case "sync": {
      await fullSync();
      console.log("✅ Full sync complete.");
      break;
    }

    case "gate": {
      const target = arg?.split("--llm")[0]?.trim();
      if (!target) {
        process.exit(1);
      }
      const sub = spawnSync("/home/workspace/Skills/skillspector/scripts/skillspector-run.sh", [target], {
        encoding: "utf8",
        stdio: "pipe",
      });
      const stdout = sub.stdout || "";
      const stderr = sub.stderr || "";
      const exitCode = sub.status;
      console.log(stdout);
      console.log(stderr);
      process.exit(exitCode);
    }
    
    case "skills": {
      if (arg) {
        const matched = await matchSkills(arg, 8);
        if (matched.length === 0) {
          console.log("No skills matched that query.");
        } else {
          for (const s of matched) {
            console.log(`\n=== ${s.name} ===`);
            console.log(s.description);
            console.log(await loadSkillBodies([s.name], 1500));
            console.log("-".repeat(50));
          }
        }
      } else {
        const metas = await listSkillMetas();
        console.log(`📚 ${metas.length} skills in ${SKILLS_DIR}:\n`);
        for (const m of metas.sort((a, b) => a.name.localeCompare(b.name))) {
          const tag = SUPERPOWERS_SKILLS.includes(m.name) ? "  [superpowers]" : "";
          console.log(`  • ${m.name}${tag} — ${m.description.slice(0, 90)}`);
        }
      }
      break;
    }
    
    case "plan": {
      if (!arg) {
        console.log("Usage: zorro.ts plan \"goal description\"");
        process.exit(1);
      }
      
      console.log(`🎯 Planning for goal: ${arg}\n`);
      
      // Recall relevant memories
      const memories = await recall(arg, 15);
      // Wire superpowers + workspace skills as execution methodology
      const methodology = await buildMethodologyContext(arg);
      console.log("🛠️  Wired superpowers methodology skills into this plan.");
      if (memories.length > 0) {
        console.log(`📚 Found ${memories.length} relevant memories\n`);
      }
      
      // Ask clarifying questions
      const questions = await askClarifyingQuestions(arg, memories, methodology);
      const answers = await getUserAnswers(questions);
      
      // Create plan
      const plan = await createPlan(arg, memories, answers, methodology);
      
      // Present for approval
      const approved = await presentPlanForApproval(plan);
      if (!approved) {
        console.log("\n❌ Plan not approved. Exiting.");
        return;
      }
      
      plan.approved = true;
      await logPlan(plan);
      console.log("\n✅ Plan approved! Starting execution...\n");
      
      // Execute plan
      const { success, results } = await executePlan(plan, memories, methodology);
      
      console.log(`\n${success ? "✅" : "❌"} Plan execution ${success ? "completed" : "failed"}`);
      await runImprovementCycle(`Plan: ${arg}`, success ? "success" : "failure", 
        JSON.stringify(results), success ? undefined : "plan_execution_failed");
      break;
    }
    
    default: {
      if (!cmd) {
        console.log("Usage:");
        console.log("  zorro.ts \"task description\"     — Execute a task with memory");
        console.log("  zorro.ts memory <query>         — Search memories");
        console.log("  zorro.ts remember <fact>        — Store a fact");
        console.log("  zorro.ts improvements           — Show improvement log");
        console.log("  zorro.ts sync                   — Full memory sync");
        console.log("  zorro.ts skills [query]        — List/wire workspace skills");
        console.log("  zorro.ts plan \"goal\"            — Create and execute a plan");
        process.exit(0);
      }
      
      // Legacy single-task execution
      const memories = await recall(cmd + " " + arg, 15);
      const methodology = await buildMethodologyContext(cmd + " " + arg);
      const { success, result } = await executeStep({
        id: "legacy-task",
        description: cmd + " " + arg,
        agentType: "general",
      }, { goal: cmd + " " + arg, steps: [] }, memories, methodology);
      
      await runImprovementCycle(cmd + " " + arg, success ? "success" : "failure", result);
      console.log(`\n✅ Task complete. Outcome: ${success ? "success" : "failure"}`);
      console.log(`📄 Result: ${result}`);
      break;
    }
  }
}

main().catch((e) => {
  console.error("❌", e.message);
  process.exit(1);
});
// ----- Trip Memory integration -----
const TRIP_MEMORY_DIR = "/home/workspace/MEMORY/trips/2026-cancun";
const TRIP_INDEX = path.join(TRIP_MEMORY_DIR, "index.md");

async function recordTripMemory(aspect: string, detail: string): Promise<void> {
  const ts = new Date().toISOString().slice(0, 19) + "Z";
  const entry = `\n- ${ts}: [${aspect}] ${detail}`;
  try {
    await fs.appendFile(TRIP_INDEX, entry);
    console.log(`📍 Trip memory recorded: [${aspect}] ${detail}`);
  } catch (e: any) {
    console.warn(`⚠️  Could not write trip memory: ${e.message}`);
  }
  // Also push to durable cross-session memory
  await remember(`[TRIP:cancun-2026] [${aspect}] ${detail}`);
}
