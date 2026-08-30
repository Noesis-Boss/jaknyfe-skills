#!/usr/bin/env bun
/**
 * image-prompt-builder
 * Assembles a structured image-generation prompt from the field-by-field
 * template (FORMAT, BUSINESS, PRODUCT, BUYER, GOAL, SCENE, COMPOSITION,
 * STYLE, TEXT, BRAND INPUTS, IMAGE RULES, OUTPUT).
 *
 * Usage:
 *   bun run image-prompt-builder.ts                          # interactive
 *   bun run image-prompt-builder.ts --file brief.json        # from JSON
 *   bun run image-prompt-builder.ts --stdin                  # from stdin JSON
 *   bun run image-prompt-builder.ts --product "…" --buyer "…"  # flags
 *   bun run image-prompt-builder.ts --output-file out.txt    # save instead of stdout
 *   bun run image-prompt-builder.ts --help
 */

interface TemplateFields {
  format: string;
  business: string;
  product: string;
  buyer: string;
  goal: string;
  scene: string;
  composition: string;
  style: string;
  text: string;
  brandInputs: string;
  imageRules: string;
  output: string;
}

const DEFAULTS: TemplateFields = {
  format: "Where it will be posted + aspect ratio",
  business: "What you actually sell.",
  product: "The specific thing in this image.",
  buyer: "Who you want to stop scrolling.",
  goal: "The ONE job this image does.",
  scene: "Surface, backdrop, props.",
  composition: "Placement, shadow, empty space for text.",
  style: "Aesthetic + hex color palette.",
  text: "The exact words on the image.",
  brandInputs: "Logo, real photos, real product details.",
  imageRules: "What the model may never invent.",
  output: "Resolution + final aspect ratio.",
};

const FLAG_KEYS = ["format", "business", "product", "buyer", "goal", "scene",
  "composition", "style", "text", "brand-inputs", "brandInputs",
  "image-rules", "imageRules", "output"];

function usage(): void {
  console.log(`Image Prompt Builder — assemble structured image prompts.

Usage:
  image-prompt-builder.ts                          # interactive (fills every field)
  image-prompt-builder.ts --file <path>            # load fields from JSON file
  image-prompt-builder.ts --stdin                  # read JSON from stdin
  image-prompt-builder.ts --product "…" --buyer "…"  # fill individual flags
  image-prompt-builder.ts --output-file <path>     # save prompt to file instead of stdout
  image-prompt-builder.ts --help                   # this message

Flags (mirror template fields):
  --format          Where it will be posted + aspect ratio
  --business        What you actually sell
  --product         The specific thing in this image
  --buyer           Who you want to stop scrolling
  --goal            The ONE job this image does
  --scene           Surface, backdrop, props
  --composition     Placement, shadow, empty space for text
  --style           Aesthetic + hex color palette
  --text            The exact words on the image
  --brand-inputs    Logo, real photos, real product details
  --image-rules     What the model may never invent
  --output          Resolution + final aspect ratio`);
}

function normalizeKey(key: string): string {
  const norm = key.replace(/-/g, "");
  if (norm === "brandinputs") return "brandInputs";
  if (norm === "imagerules") return "imageRules";
  return norm;
}

function parseFlags(args: string[]): Partial<TemplateFields> {
  const fields: Partial<TemplateFields> = {};
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith("--") && !["--stdin", "--file", "--output-file"].includes(arg)) {
      const key = arg.slice(2);
      const mappedKey = normalizeKey(key);
      if (FLAG_KEYS.includes(key) || FLAG_KEYS.includes(mappedKey)) {
        const val = args[i + 1];
        if (val !== undefined && !val.startsWith("--")) {
          (fields as any)[mappedKey] = val;
          i++;
        }
      }
    }
  }
  return fields;
}

function buildLabel(field: string): string {
  const labels: Record<string, string> = {
    format: "[FORMAT]", business: "[BUSINESS]", product: "[PRODUCT]",
    buyer: "[BUYER]", goal: "[GOAL]", scene: "[SCENE]",
    composition: "[COMPOSITION]", style: "[STYLE]", text: "[TEXT]",
    brandInputs: "[BRAND INPUTS]", imageRules: "[IMAGE RULES]",
    output: "[OUTPUT]",
  };
  return labels[field] || `[${field.toUpperCase()}]`;
}

function assemblePrompt(fields: Partial<TemplateFields>): string {
  const merged: TemplateFields = { ...DEFAULTS, ...fields };
  const lines: string[] = [];

  lines.push(`You are a world-class creative director crafting images for ${merged.business}.`);

  const order: (keyof TemplateFields)[] = [
    "format", "business", "product", "buyer", "goal",
    "scene", "composition", "style", "text", "brandInputs",
    "imageRules", "output",
  ];

  for (const key of order) {
    lines.push(`${buildLabel(key)} ${merged[key]}`);
  }

  return lines.join("\n") + "\n";
}

async function interactive(): Promise<string> {
  const fieldKeys: (keyof TemplateFields)[] = [
    "format", "business", "product", "buyer", "goal",
    "scene", "composition", "style", "text", "brandInputs",
    "imageRules", "output",
  ];

  const display: Record<string, string> = {
    format: "FORMAT — Where it will be posted + aspect ratio",
    business: "BUSINESS — What you actually sell",
    product: "PRODUCT — The specific thing in this image",
    buyer: "BUYER — Who you want to stop scrolling",
    goal: "GOAL — The ONE job this image does",
    scene: "SCENE — Surface, backdrop, props",
    composition: "COMPOSITION — Placement, shadow, empty space for text",
    style: "STYLE — Aesthetic + hex color palette",
    text: "TEXT — The exact words on the image",
    brandInputs: "BRAND INPUTS — Logo, real photos, real product details",
    imageRules: "IMAGE RULES — What the model may never invent",
    output: "OUTPUT — Resolution + final aspect ratio",
  };

  const answers: Partial<TemplateFields> = {};
  const stdin = process.stdin;
  const stdout = process.stdout;

  for (const key of fieldKeys) {
    stdout.write(`\n${display[key]}\n> `);
    const input = await new Promise<string>((resolve) => {
      let data = "";
      const onData = (chunk: Buffer) => {
        data += chunk.toString();
        if (data.includes("\n")) {
          stdin.off("data", onData);
          resolve(data.replace(/\r?\n/, ""));
        }
      };
      stdin.on("data", onData);
    });
    if (input.trim()) {
      (answers as any)[key] = input.trim();
    }
  }

  return assemblePrompt(answers);
}

function loadFromJson(jsonData: Record<string, string>): Partial<TemplateFields> {
  const fields: Partial<TemplateFields> = {};
  for (const [k, v] of Object.entries(jsonData)) {
    (fields as any)[normalizeKey(k)] = v;
  }
  return fields;
}

async function main(): Promise<void> {
  const args = process.argv.slice(2);

  if (args.includes("--help")) {
    usage();
    process.exit(0);
  }

  let fields: Partial<TemplateFields> = {};
  let outputFile: string | undefined;

  // Parse CLI flags
  fields = { ...fields, ...parseFlags(args) };

  // Handle --file
  const fileIdx = args.indexOf("--file");
  if (fileIdx >= 0) {
    const filePath = args[fileIdx + 1];
    if (!filePath) {
      console.error("Error: --file requires a path");
      process.exit(1);
    }
    const content = await Bun.file(filePath).text();
    const jsonData = JSON.parse(content) as Record<string, string>;
    fields = { ...fields, ...loadFromJson(jsonData) };
  }

  // Handle --stdin
  if (args.includes("--stdin")) {
    const content = await new Response(process.stdin).text();
    const jsonData = JSON.parse(content) as Record<string, string>;
    fields = { ...fields, ...loadFromJson(jsonData) };
  }

  // Handle --output-file
  const ofIdx = args.indexOf("--output-file");
  if (ofIdx >= 0) {
    outputFile = args[ofIdx + 1];
    if (!outputFile) {
      console.error("Error: --output-file requires a path");
      process.exit(1);
    }
  }

  const hasAnyField = Object.values(fields).some(v => v !== undefined);

  let prompt: string;
  if (hasAnyField || args.includes("--file") || args.includes("--stdin")) {
    prompt = assemblePrompt(fields);
  } else {
    prompt = await interactive();
  }

  if (outputFile) {
    await Bun.write(outputFile, prompt);
    console.error(`Saved prompt to ${outputFile}`);
  } else {
    console.log(prompt);
  }
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
