#!/usr/bin/env bun

type Args = {
  content?: string;
  slides: number;
  output: string;
};

function parseArgs(argv: string[]): Args {
  const args: Args = { slides: 8, output: "pptx" };
  for (let i = 0; i < argv.length; i += 1) {
    const flag = argv[i];
    if (flag === "--content") args.content = argv[++i];
    else if (flag === "--slides") args.slides = Number(argv[++i]);
    else if (flag === "--output") args.output = argv[++i];
    else if (flag === "--help" || flag === "-h") {
      console.log("Usage: bun run presenton.ts --content FILE [--slides N] [--output pptx|pdf|png]");
      process.exit(0);
    }
  }
  if (!args.content) throw new Error("--content is required");
  if (!Number.isInteger(args.slides) || args.slides < 1 || args.slides > 100) throw new Error("--slides must be 1..100");
  if (!["pptx", "pdf", "png"].includes(args.output)) throw new Error("--output must be pptx, pdf, or png");
  return args;
}

const args = parseArgs(Bun.argv.slice(2));
const baseUrl = process.env.PRESENTON_URL;
if (!baseUrl) throw new Error("PRESENTON_URL is required");
const apiKey = process.env.PRESENTON_API_KEY;

const content = await Bun.file(args.content).text();
if (content.length > 250_000) throw new Error("content exceeds 250,000 characters");

const response = await fetch(`${baseUrl.replace(/\/$/, "")}/api/v1/ppt/presentation/generate`, {
  method: "POST",
  headers: { ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}), "Content-Type": "application/json", Accept: "application/json" },
  body: JSON.stringify({ content, n_slides: args.slides, export_as: args.output }),
});

const body = await response.text();
if (!response.ok) throw new Error(`Presenton returned HTTP ${response.status}: ${body.slice(0, 500)}`);
console.log(body);
