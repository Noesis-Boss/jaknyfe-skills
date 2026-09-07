// Thin shim: rules reference memory.js; implementation lives in memory.ts.
import { spawn } from "bun";

const args = ["run", new URL("./memory.ts", import.meta.url).pathname, ...process.argv.slice(2)];
const proc = spawn(["bun", ...args], { stdout: "inherit", stderr: "inherit", stdin: "inherit" });
process.exit(await proc.exited);
