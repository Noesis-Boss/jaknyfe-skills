#!/usr/bin/env bun

const args = process.argv.slice(2);
const value = (name: string) => {
  const i = args.indexOf(name);
  return i >= 0 ? args[i + 1] : undefined;
};
if (args.includes("--help") || (!value("--text") && !value("--file"))) {
  console.log("Usage: kokoro-voice.ts (--text TEXT | --file PATH) --output PATH [--voice af_heart] [--model model_q8f16] [--speed 1]");
  process.exit(args.includes("--help") ? 0 : 1);
}

const output = value("--output");
if (!output) throw new Error("--output is required");
const text = value("--text") ?? await Bun.file(value("--file")!).text();
const format = output.toLowerCase().endsWith(".mp3") ? "mp3" : "wav";
const response = await fetch(`${process.env.KOKORO_BASE_URL ?? "http://127.0.0.1:3010"}/api/v1/audio/speech`, {
  method: "POST",
  headers: { "Content-Type": "application/json", ...(process.env.KOKORO_API_KEY ? { Authorization: `Bearer ${process.env.KOKORO_API_KEY}` } : {}) },
  body: JSON.stringify({ model: value("--model") ?? "model_q8f16", voice: value("--voice") ?? "af_heart", input: text, speed: Number(value("--speed") ?? "1"), response_format: format }),
});
if (!response.ok) throw new Error(`Kokoro request failed: ${response.status} ${await response.text()}`);
await Bun.write(output, await response.arrayBuffer());
console.log(output);
