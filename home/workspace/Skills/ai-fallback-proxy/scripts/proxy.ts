#!/usr/bin/env bun
/**
 * AI Fallback Proxy — OpenAI-compatible reverse proxy with automatic provider failover.
 * Zero external dependencies. Runs on Bun.
 *
 * Provider priority:
 *   1. OpenAI direct
 *   2. Anthropic direct  
 *   3. Google Gemini direct
 *   4. OpenRouter (universal fallback — 338+ models)
 *
 * When a provider fails (401, 429, 5xx, timeout), it auto-cools down and falls through.
 */

// ─── Config ───────────────────────────────────────────────────
const PORT = parseInt(process.env.PROXY_PORT || "8787");
const COOLDOWN_MS = parseInt(process.env.COOLDOWN_MS || "60000");
const TIMEOUT_MS = parseInt(process.env.REQUEST_TIMEOUT_MS || "30000");

// ─── Provider Definitions ─────────────────────────────────────
interface Provider {
  name: string;
  baseUrl: string;
  apiKey: string | undefined;
  isAvailable: boolean;
  cooldownUntil: number; // epoch ms
}

function buildProviders(): Provider[] {
  return [
    {
      name: "openai",
      baseUrl: "https://api.openai.com",
      apiKey: process.env.OPENAI_API_KEY,
      isAvailable: true,
      cooldownUntil: 0,
    },
    {
      name: "anthropic",
      baseUrl: "https://api.anthropic.com",
      apiKey: process.env.ANTHROPIC_API_KEY,
      isAvailable: true,
      cooldownUntil: 0,
    },
    {
      name: "gemini",
      baseUrl: "https://generativelanguage.googleapis.com/v1beta",
      apiKey: process.env.GOOGLE_GENERATIVE_AI_KEY || process.env.GEMINI_API_KEY,
      isAvailable: true,
      cooldownUntil: 0,
    },
    {
      name: "openrouter",
      baseUrl: "https://openrouter.ai/api",
      apiKey: process.env.OPENROUTER_API_KEY,
      isAvailable: true,
      cooldownUntil: 0,
    },
  ].filter(p => p.apiKey); // only include providers with keys
}

// ─── State ────────────────────────────────────────────────────
let providers = buildProviders();
const failureTimeouts = new Map<string, ReturnType<typeof setTimeout>>();

function resetCooldown(name: string) {
  const p = providers.find(x => x.name === name);
  if (p) {
    p.cooldownUntil = 0;
    p.isAvailable = true;
    const existing = failureTimeouts.get(name);
    if (existing) {
      clearTimeout(existing);
      failureTimeouts.delete(name);
    }
  }
}

function coolDown(name: string) {
  const p = providers.find(x => x.name === name);
  if (p) {
    p.cooldownUntil = Date.now() + COOLDOWN_MS;
    p.isAvailable = false;
    // Auto-reset after cooldown
    const timeout = setTimeout(() => resetCooldown(name), COOLDOWN_MS);
    failureTimeouts.set(name, timeout);
  }
}

function isCooledDown(p: Provider): boolean {
  if (p.cooldownUntil === 0) return true;
  if (Date.now() >= p.cooldownUntil) {
    p.cooldownUntil = 0;
    p.isAvailable = true;
    return true;
  }
  return false;
}

function getActiveProviders(): Provider[] {
  return providers
    .filter(p => p.apiKey && isCooledDown(p))
    .sort((a, b) => {
      // OpenRouter always last (it's the catch-all)
      if (a.name === "openrouter") return 1;
      if (b.name === "openrouter") return -1;
      return 0;
    });
}

// ─── Provider-specific request adapters ───────────────────────

/**
 * Each provider has slightly different API shapes.
 * We normalize to OpenAI chat-completions format for the caller,
 * and adapt the request to match each provider's native API.
 */
function adaptRequest(provider: Provider, model: string, body: any): { url: string; headers: Record<string,string>; adaptedBody: any } {
  if (provider.name === "openai") {
    // Newer OpenAI models use max_completion_tokens instead of max_tokens
    const adaptedBody = { ...body };
    if (adaptedBody.max_tokens !== undefined) {
      adaptedBody.max_completion_tokens = adaptedBody.max_tokens;
      delete adaptedBody.max_tokens;
    }
    // Strip provider prefix (e.g. "openai/gpt-5-nano" → "gpt-5-nano")
    if (adaptedBody.model) {
      adaptedBody.model = adaptedBody.model.replace(/^[^\/]+\//, "");
    }
    return {
      url: `${provider.baseUrl}/v1/chat/completions`,
      headers: {
        "Authorization": `Bearer ${provider.apiKey}`,
        "Content-Type": "application/json",
      },
      adaptedBody,
    };
  }

  if (provider.name === "anthropic") {
    // Convert OpenAI format to Anthropic format
    const messages = body.messages || [];
    const systemMsg = messages.find((m: any) => m.role === "system");
    const userMessages = messages.filter((m: any) => m.role !== "system");

    // Anthropic requires alternating user/assistant; merge consecutive same-role
    const anthropicMessages: any[] = [];
    for (const msg of userMessages) {
      if (msg.role === "user") {
        anthropicMessages.push({ role: "user", content: msg.content });
      } else if (msg.role === "assistant") {
        anthropicMessages.push({ role: "assistant", content: msg.content });
      }
    }

    // If no user message exists and there was no system message, handle edge case
    if (anthropicMessages.length === 0 && messages.length > 0) {
      anthropicMessages.push({ role: "user", content: messages[0].content });
    }

    // Remove consecutive same-role messages
    const merged: any[] = [];
    for (const m of anthropicMessages) {
      if (merged.length > 0 && merged[merged.length - 1].role === m.role) {
        merged[merged.length - 1].content += "\n\n" + m.content;
      } else {
        merged.push(m);
      }
    }

    return {
      url: `${provider.baseUrl}/v1/messages`,
      headers: {
        "x-api-key": provider.apiKey!,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json",
      },
      adaptedBody: {
        model: model?.replace(/^anthropic\//, "").replace(/^~/, "") || "claude-sonnet-4-20250514",
        max_tokens: body.max_tokens || 1024,
        ...(systemMsg ? { system: systemMsg.content } : {}),
        messages: merged.length > 0 ? merged : [{ role: "user", content: "Hi" }],
        stream: body.stream || false,
        ...(body.temperature !== undefined ? { temperature: body.temperature } : {}),
      },
    };
  }

  if (provider.name === "gemini") {
    // Convert OpenAI format to Gemini format
    const messages = body.messages || [];
    const systemMsg = messages.find((m: any) => m.role === "system");
    const contents: any[] = [];
    for (const msg of messages) {
      if (msg.role === "system") continue;
      contents.push({
        role: msg.role === "assistant" ? "model" : "user",
        parts: [{ text: typeof msg.content === "string" ? msg.content : JSON.stringify(msg.content) }],
      });
    }

    const modelId = model?.replace(/^google\//, "").replace(/\//g, "") || "gemini-3.1-flash-lite";

    return {
      url: `${provider.baseUrl}/models/${modelId}:generateContent?key=${provider.apiKey}`,
      headers: {
        "Content-Type": "application/json",
      },
      adaptedBody: {
        contents: contents.length > 0 ? contents : [{ role: "user", parts: [{ text: "Hi" }] }],
        ...(systemMsg ? { systemInstruction: { parts: [{ text: systemMsg.content }] } } : {}),
        generationConfig: {
          ...(body.temperature !== undefined ? { temperature: body.temperature } : {}),
          maxOutputTokens: body.max_tokens || 1024,
        },
      },
    };
  }

  if (provider.name === "openrouter") {
    return {
      url: `${provider.baseUrl}/v1/chat/completions`,
      headers: {
        "Authorization": `Bearer ${provider.apiKey}`,
        "Content-Type": "application/json",
        "HTTP-Referer": "https://jaknyfe.zo.computer",
        "X-Title": "Zo AI Fallback Proxy",
      },
      adaptedBody: { ...body, model: model || "qwen/qwen3.6-flash" },
    };
  }

  throw new Error(`Unknown provider: ${provider.name}`);
}

/**
 * Normalize provider responses back to OpenAI chat-completions format.
 */
function adaptResponse(provider: Provider, raw: any): any {
  if (provider.name === "openai" || provider.name === "openrouter") {
    return raw;
  }

  if (provider.name === "anthropic") {
    const content = raw.content?.map((c: any) => c.text).join("") || "";
    return {
      id: raw.id,
      object: "chat.completion",
      created: Math.floor(Date.now() / 1000),
      model: raw.model,
      choices: [{
        index: 0,
        message: { role: "assistant", content },
        finish_reason: raw.stop_reason === "end_turn" ? "stop" : raw.stop_reason,
      }],
      usage: raw.usage ? {
        prompt_tokens: raw.usage.input_tokens || 0,
        completion_tokens: raw.usage.output_tokens || 0,
        total_tokens: (raw.usage.input_tokens || 0) + (raw.usage.output_tokens || 0),
      } : undefined,
    };
  }

  if (provider.name === "gemini") {
    const candidate = raw.candidates?.[0];
    const text = candidate?.content?.parts?.map((p: any) => p.text).join("") || "";
    return {
      id: raw.responseId || `gemini-${Date.now()}`,
      object: "chat.completion",
      created: Math.floor(Date.now() / 1000),
      model: raw.modelVersion || "gemini",
      choices: [{
        index: 0,
        message: { role: "assistant", content: text },
        finish_reason: candidate?.finishReason?.toLowerCase() === "stop" ? "stop" : (candidate?.finishReason || "stop"),
      }],
      usage: raw.usageMetadata ? {
        prompt_tokens: raw.usageMetadata.promptTokenCount || 0,
        completion_tokens: raw.usageMetadata.candidatesTokenCount || 0,
        total_tokens: raw.usageMetadata.totalTokenCount || 0,
      } : undefined,
    };
  }

  return raw;
}

// ─── Error classification ────────────────────────────────────
function shouldFailover(status: number, body: any): boolean {
  if (status === 401 || status === 403) return true; // Key invalid/expired
  if (status === 429) return true; // Rate limited
  if (status === 402) return true; // Out of credits/billing
  if (status >= 500) return true; // Provider error
  // Check error messages for common "out of tokens" signals
  if (body?.error?.message) {
    const msg = body.error.message.toLowerCase();
    if (msg.includes("credit balance") || msg.includes("insufficient credits") ||
        msg.includes("quota") || msg.includes("rate limit") || msg.includes("overloaded") ||
        msg.includes("invalid model") || msg.includes("does not exist") || msg.includes("not found")) {
      return true;
    }
  }
  return false;
}

// ─── Model resolution ────────────────────────────────────────
function resolveModel(requested: string): string {
  if (!requested || requested === "auto" || requested === "fast" || requested === "smart") {
    return "";
  }
  // Strip Zo BYOK prefixes (e.g., "byok:cde6895a-7a9d-49d9-9828-ca42381fcbb6:gpt-5-nano")
  const stripped = requested.replace(/^byok:[a-f0-9-]+:/, "").replace(/^proxy:/, "");
  return stripped || requested;
}

function selectModelForBucket(bucket: string): string {
  switch (bucket) {
    case "fast": return "meta-llama/llama-3.1-8b-instruct";
    case "smart": return "google/gemini-3.1-flash-lite";
    case "auto": return "qwen/qwen3.6-flash";
    default: return "qwen/qwen3.6-flash";
  }
}

// ─── Core proxy logic ────────────────────────────────────────
async function proxyChatCompletions(req: Request): Promise<Response> {
  const body = await req.json().catch(() => null);
  if (!body) {
    return Response.json({ error: { message: "Invalid JSON body", type: "invalid_request" } }, { status: 400 });
  }

  const requestedModel = resolveModel(body.model);
  const isSpecialBucket = ["auto", "fast", "smart"].includes(body.model);
  const effectiveModel = isSpecialBucket ? selectModelForBucket(body.model) : requestedModel;

  const active = getActiveProviders();
  if (active.length === 0) {
    return Response.json({ error: { message: "All providers exceeded cooldown. Try again later.", type: "all_providers_down" } }, { status: 503 });
  }

  let lastError: { status: number; body: any } | null = null;

  for (const provider of active) {
    // Bucket models (auto/fast/smart) are only meaningful for OpenRouter
    if (isSpecialBucket && provider.name !== "openrouter") continue;

    try {
      const { url, headers, adaptedBody } = adaptRequest(
        provider,
        provider.name === "openrouter" ? effectiveModel : requestedModel,
        isSpecialBucket ? { ...body, model: effectiveModel } : body,
      );

      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);

      const res = await fetch(url, {
        method: "POST",
        headers,
        body: JSON.stringify(adaptedBody),
        signal: controller.signal,
      });
      clearTimeout(timeout);

      const responseText = await res.text();
      let responseBody: any;
      try { responseBody = JSON.parse(responseText); } catch { responseBody = { raw: responseText }; }
      
      if (!res.ok && shouldFailover(res.status, responseBody)) {
        lastError = { status: res.status, body: responseBody };
        coolDown(provider.name);
        continue;
      }

      if (!res.ok) {
        // For bucket models (auto/fast/smart), skip providers that don't have the resolved model
        if (isSpecialBucket && provider.name !== "openrouter") {
          continue;
        }
        // Non-failover error (e.g., 400 bad request) — return as-is
        return Response.json(responseBody, { status: res.status });
      }

      // Success!
      const normalized = adaptResponse(provider, responseBody);
      const response = Response.json(normalized, { status: 200 });
      response.headers.set("X-Proxy-Provider", provider.name);
      return response;

    } catch (err: any) {
      if (err.name === "AbortError") {
        coolDown(provider.name);
        lastError = { status: 408, body: { error: { message: "Provider timeout", type: "provider_timeout" } } };
        continue;
      }
      // Network error — cool down and continue
      coolDown(provider.name);
      lastError = { status: 502, body: { error: { message: `Network error: ${err.message}`, type: "network_error" } } };
      continue;
    }
  }

  // All providers failed
  return Response.json(
    lastError?.body || { error: { message: "All providers failed", type: "all_providers_failed" } },
    { status: lastError?.status || 502 }
  );
}

// ─── Server ───────────────────────────────────────────────────
const server = Bun.serve({
  port: PORT,
  hostname: "0.0.0.0",
  async fetch(req) {
    const url = new URL(req.url);

    // CORS preflight
    if (req.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
      });
    }

    // Health check — provider status
    if (url.pathname === "/health") {
      return Response.json({
        status: "ok",
        providers: providers.map(p => ({
          name: p.name,
          configured: !!p.apiKey,
          available: isCooledDown(p) && !!p.apiKey,
          cooldownUntil: p.cooldownUntil > 0 ? new Date(p.cooldownUntil).toISOString() : null,
        })),
      });
    }

    // Model listing — return wildcard so Zo accepts any model ID
    if (url.pathname === "/v1/models") {
      const reqUrl = new URL(req.url);
      const modelParam = reqUrl.searchParams.get("model");
      // If Zo's verifier asks about a specific model, claim we support it
      if (modelParam) {
        return Response.json({
          object: "list",
          data: [{ id: modelParam, object: "model", created: 0, owned_by: "proxy" }],
        });
      }
      return Response.json({
        object: "list",
        data: [
          { id: "auto", object: "model", created: 0, owned_by: "proxy" },
          { id: "fast", object: "model", created: 0, owned_by: "proxy" },
          { id: "smart", object: "model", created: 0, owned_by: "proxy" },
          { id: "openai/gpt-5-nano", object: "model", created: 0, owned_by: "openai" },
          { id: "openai/gpt-4.1", object: "model", created: 0, owned_by: "openai" },
          { id: "openai/o4-mini", object: "model", created: 0, owned_by: "openai" },
          { id: "anthropic/claude-sonnet-4-20250514", object: "model", created: 0, owned_by: "anthropic" },
          { id: "anthropic/claude-opus-4-20250514", object: "model", created: 0, owned_by: "anthropic" },
          { id: "google/gemini-2.5-pro", object: "model", created: 0, owned_by: "gemini" },
          { id: "google/gemini-2.5-flash", object: "model", created: 0, owned_by: "gemini" },
          { id: "google/gemini-3.1-flash-lite", object: "model", created: 0, owned_by: "gemini" },
          { id: "google/gemini-3.5-flash", object: "model", created: 0, owned_by: "gemini" },
        ],
      });
    }

    // Main endpoint
    if (url.pathname === "/v1/chat/completions" && req.method === "POST") {
      return proxyChatCompletions(req);
    }

    return Response.json({ error: { message: "Not found. Use /v1/chat/completions" } }, { status: 404 });
  },
});

// Graceful shutdown
process.on("SIGTERM", () => {
  for (const t of failureTimeouts.values()) clearTimeout(t);
  server.stop();
  process.exit(0);
});

console.log(`[ai-fallback-proxy] Running on port ${PORT}`);
console.log(`[ai-fallback-proxy] Providers configured: ${providers.map(p => p.name).join(", ")}`);
console.log(`[ai-fallback-proxy] Cooldown: ${COOLDOWN_MS}ms | Timeout: ${TIMEOUT_MS}ms`);