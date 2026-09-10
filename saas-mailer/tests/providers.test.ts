import { expect, test } from "bun:test";
import { gmailAdapter } from "../src/server/sending/gmail-adapter";
import { microsoftAdapter } from "../src/server/sending/microsoft-adapter";
import { resendAdapter } from "../src/server/sending/resend-adapter";

const input = { from: "sender@example.com", to: "lead@example.com", subject: "Hello", body: "Message" };

test("Gmail adapter sends RFC message and normalizes id", async () => {
  let request: Request | undefined;
  const adapter = gmailAdapter("token", async (url, init) => { request = new Request(url, init); return new Response(JSON.stringify({ id: "gmail-1" }), { status: 200 }); });
  await expect(adapter.send(input)).resolves.toMatchObject({ providerMessageId: "gmail-1" });
  expect(request?.url).toContain("gmail.googleapis.com");
  expect(request?.headers.get("authorization")).toBe("Bearer token");
});

test("Microsoft adapter maps quota failures as retryable", async () => {
  const adapter = microsoftAdapter("token", async () => new Response("slow down", { status: 429 }));
  await expect(adapter.send(input)).rejects.toMatchObject({ code: "quota_exceeded", retryable: true });
});

test("Resend adapter sends from the configured domain and normalizes id", async () => {
  let request: Request | undefined;
  const adapter = resendAdapter("re_test", async (url, init) => { request = new Request(url, init); return new Response(JSON.stringify({ id: "resend-1" }), { status: 200 }); });
  await expect(adapter.send(input)).resolves.toMatchObject({ providerMessageId: "resend-1" });
  expect(request?.url).toBe("https://api.resend.com/emails");
  expect(request?.headers.get("authorization")).toBe("Bearer re_test");
  expect(await request?.json()).toMatchObject({ from: "sender@example.com", to: ["lead@example.com"] });
});
