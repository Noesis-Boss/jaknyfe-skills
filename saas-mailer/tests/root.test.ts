import { describe, expect, test } from "bun:test";
import app from "../src/server";

describe("SaaS-Mailer dashboard entrypoint", () => {
  test("serves a usable root shell and its referenced assets", async () => {
    const root = await app.fetch(new Request("http://localhost/"));
    const html = await root.text();

    expect(root.status).toBe(200);
    expect(html).toContain('<div id="root"></div>');
    expect(html).toContain('href="/src/client/styles.css"');
    expect(html).toContain('src="/src/client/main.js"');

    const script = await app.fetch(new Request("http://localhost/src/client/main.js"));
    const styles = await app.fetch(new Request("http://localhost/src/client/styles.css"));

    expect(script.status).toBe(200);
    expect(await script.text()).toContain("Outbound workspace");
    expect(styles.status).toBe(200);
    expect(await styles.text()).toContain(".dashboard-shell");
  });
});
