#!/usr/bin/env bun
/**
 * Test suite for AI Fallback Proxy
 * Run with: bun run /home/workspace/Skills/ai-fallback-proxy/scripts/test.ts
 */
async function test(name: string, fn: () => Promise<boolean>) {
  try {
    const ok = await fn();
    console.log(`${ok ? "✓" : "✗"} ${name}`);
    if (!ok) process.exitCode = 1;
  } catch (e: any) {
    console.log(`✗ ${name} — ${e.message}`);
    process.exitCode = 1;
  }
}

const BASE = "http://localhost:8787";

async function main() {
  console.log("AI Fallback Proxy Test Suite\n");

  await test("Health endpoint returns provider status", async () => {
    const res = await fetch(`${BASE}/health`);
    const data = await res.json();
    return data.status === "ok" && Array.isArray(data.providers) && data.providers.length >= 1;
  });

  await test("/v1/models returns model list", async () => {
    const res = await fetch(`${BASE}/v1/models`);
    const data = await res.json();
    return Array.isArray(data.data) && data.data.length >= 3;
  });

  await test("Auto bucket returns valid completion", async () => {
    const res = await fetch(`${BASE}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "auto",
        messages: [{ role: "user", content: "Say hello" }],
        max_tokens: 50,
      }),
    });
    const data = await res.json();
    return res.status === 200 && data.choices?.[0]?.message?.content !== undefined;
  });

  await test("Fast bucket returns valid completion", async () => {
    const res = await fetch(`${BASE}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "fast",
        messages: [{ role: "user", content: "Say hi" }],
        max_tokens: 20,
      }),
    });
    const data = await res.json();
    return res.status === 200 && data.choices?.[0]?.message?.content !== undefined;
  });

  await test("Direct OpenAI model (gpt-5-nano)", async () => {
    const res = await fetch(`${BASE}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "openai/gpt-5-nano",
        messages: [{ role: "user", content: "Say hi" }],
        max_tokens: 10,
      }),
    });
    return res.status === 200;
  });

  await test("CORS preflight returns correct headers", async () => {
    const res = await fetch(`${BASE}/v1/chat/completions`, { method: "OPTIONS" });
    return res.headers.get("access-control-allow-origin") === "*";
  });

  await test("Invalid JSON returns 400", async () => {
    const res = await fetch(`${BASE}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: "not json",
    });
    return res.status === 400;
  });

  await test("Unknown endpoint returns 404", async () => {
    const res = await fetch(`${BASE}/unknown`);
    return res.status === 404;
  });

  console.log(`\nDone. ${process.exitCode ? "SOME TESTS FAILED" : "ALL PASSED"}`);
}

main();
