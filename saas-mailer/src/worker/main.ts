import { openProductionDatabase } from "../server/postgres";

const database = await openProductionDatabase();
const controller = new AbortController();
process.once("SIGTERM", () => controller.abort());
process.once("SIGINT", () => controller.abort());
console.log(JSON.stringify({ event: "worker_started", pid: process.pid }));

try {
  const { runWorker } = await import("./scheduler");
  await runWorker(database, controller.signal, { onError: error => console.error(JSON.stringify({ event: "worker_error", error: error instanceof Error ? error.message : "unknown" })) });
} finally {
  await database.close();
}
