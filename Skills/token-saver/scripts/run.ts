const cmd = Bun.argv.slice(2).join(" ");
if (!cmd) {
  console.error("usage: run.ts <command...>");
  process.exit(2);
}
const proc = Bun.spawn(["python3", "/root/.token-saver/scripts/wrap.py", cmd], {
  stdout: "inherit",
  stderr: "inherit",
  stdin: "inherit",
});
process.exit(await proc.exited);
