import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";

function zoAskProxy(): Plugin {
  return { name: "zo-ask-proxy", configureServer(server) { server.middlewares.use("/api/ask", async (request, response) => {
    if (request.method !== "POST") { response.statusCode = 405; response.end(JSON.stringify({ error: "Method not allowed" })); return; }
    const chunks: Buffer[] = []; for await (const chunk of request) chunks.push(Buffer.from(chunk));
    try {
      const body = JSON.parse(Buffer.concat(chunks).toString("utf8"));
      const token = process.env.ZO_CLIENT_IDENTITY_TOKEN;
      if (!token) throw new Error("ZO_CLIENT_IDENTITY_TOKEN is unavailable on this server.");
      const upstream = await fetch("https://api.zo.computer/zo/ask", { method: "POST", headers: { authorization: token, "content-type": "application/json" }, body: JSON.stringify({ input: body.prompt, model_name: "byok:66b916e9-a61f-4184-badb-22020c0b2fd9" }) });
      const text = await upstream.text(); response.statusCode = upstream.status; response.setHeader("Content-Type", "application/json"); response.end(text);
    } catch (error) { response.statusCode = 500; response.setHeader("Content-Type", "application/json"); response.end(JSON.stringify({ error: error instanceof Error ? error.message : "Proxy request failed" })); }
  }); } };
}

export default defineConfig({ server: { allowedHosts: ["zoltan"] }, plugins: [react(), zoAskProxy()] });
