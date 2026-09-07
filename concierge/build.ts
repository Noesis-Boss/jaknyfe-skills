import { build } from "bun";

await build({
  entrypoints: ["./src/client.tsx"],
  outdir: "./public",
  target: "browser",
  minify: false,
});

console.log("✓ client bundle written to public/");
