#!/usr/bin/env node
/**
 * Zorro Self-Improvement Analysis
 * 
 * Analyzes patterns in the improvement log and suggests systemic fixes.
 */

import {object Object}
 */

import { promises as fs } from "fs";

const IMPROVEMENT_LOG = "/home/workspace/Skills/zorro/improvements.log";

interface ImprovementEntry {
  timestamp: string;
  task: string;
  outcome: "success" | "partial" | "failure";
  errorCategory?: string;
  lesson: string;
  strategyUpdate?: string;
}

async function analyze(): Promise<void> {
  try {
    const content = await fs.readFile(IMPROVEMENT_LOG, "utf8");
    const lines = content.trim().split("\n").filter(l => l);
    const entries = lines.map(l => JSON.parse(l) as ImprovementEntry);
    
    if (entries.length === 0) {
      console.log("📝 No improvement data yet.");
      return;
    }
    
    console.log(`📊 Analyzing ${entries.length} improvement entries...\n`);
    
    // Outcome distribution
    const outcomes = { success: 0, partial: 0, failure: 0 };
    for (const e of entries) outcomes[e.outcome]++;
    console.log("Outcome distribution:");
    console.log(`  ✅ Success:   ${outcomes.success}`);
    console.log(`  ⚠️  Partial:  ${outcomes.partial}`);
    console.log(`  ❌ Failure:   ${outcomes.failure}`);
    
    // Error categories
    const errorCats: Record<string, number> = {};
    for (const e of entries) {
      if (e.errorCategory) errorCats[e.errorCategory] = (errorCats[e.errorCategory] || 0) + 1;
    }
    if (Object.keys(errorCats).length > 0) {
      console.log("\nError categories:");
      for (const [cat, count] of Object.entries(errorCats).sort((a, b) => b[1] - a[1])) {
        console.log(`  ${cat}: ${count}`);
      }
    }
    
    // Recurring lessons
    const lessons: Record<string, number> = {};
    for (const e of entries) {
      const key = e.lesson.slice(0, 60);
      lessons[key] = (lessons[key] || 0) + 1;
    }
    console.log("\nRecurring lessons (≥2 occurrences):");
    for (const [lesson, count] of Object.entries(lessons).sort((a, b) => b[1] - a[1])) {
      if (count >= 2) console.log(`  [${count}x] ${lesson}...`);
    }
    
    // Strategy updates frequency
    const strategies: Record<string, number> = {};
    for (const e of entries) {
      if (e.strategyUpdate) {
        const key = e.strategyUpdate.slice(0, 60);
        strategies[key] = (strategies[key] || 0) + 1;
      }
    }
    console.log("\nRecurring strategy updates (≥2 occurrences):");
    for (const [strat, count] of Object.entries(strategies).sort((a, b) => b[1] - a[1])) {
      if (count >= 2) console.log(`  [${count}x] ${strat}...`);
    }
    
    // Recommendations
    console.log("\n🎯 Systemic recommendations:");
    if (errorCats.memory_gap && errorCats.memory_gap >= 3) {
      console.log("  • Frequent memory gaps — consider broader pre-task recall or automated fact extraction");
    }
    if (errorCats.tool_error && errorCats.tool_error >= 3) {
      console.log("  • Frequent tool errors — add tool health checks and parameter validation wrappers");
    }
    if (errorCats.reasoning_error && errorCats.reasoning_error >= 3) {
      console.log("  • Frequent reasoning errors — implement step-by-step verification checkpoints");
    }
    if (outcomes.failure / entries.length > 0.3) {
      console.log("  • High failure rate — review task decomposition and add more pre-flight validation");
    }
    
  } catch (e) {
    console.error("❌ Analysis failed:", (e as Error).message);
  }
}

analyze();