import { describe, expect, test } from "bun:test";
import { signTrackingToken, verifyTrackingToken, signUnsubscribeToken, verifyUnsubscribeToken, injectTracking, unsubscribeUrl } from "../src/server/tracking/tokens";

describe("tokenized tracking", () => {
  test("signs and verifies a message token", () => {
    const token = signTrackingToken("msg-123");
    expect(verifyTrackingToken(token)).toBe("msg-123");
    expect(verifyTrackingToken("tampered")).toBeNull();
    expect(verifyTrackingToken(token.slice(0, -2) + "xx")).toBeNull();
  });

  test("injects tokenized open and click links into html", () => {
    const html = injectTracking("<p>Hi</p><a href='https://example.com/x'>link</a>", "msg-123");
    expect(html).toContain("/api/t/o/");
    expect(html).toContain("/api/t/c/");
    expect(html).toContain("https%3A%2F%2Fexample.com%2Fx");
    const token = html.match(/api\/t\/c\/([^?']+)/)![1];
    expect(verifyTrackingToken(decodeURIComponent(token))).toBe("msg-123");
  });

  test("signs and verifies unsubscribe tokens separately from click tokens", () => {
    const token = signUnsubscribeToken("msg-123");
    expect(verifyUnsubscribeToken(token)).toBe("msg-123");
    expect(verifyTrackingToken(token)).toBeNull();
    expect(verifyUnsubscribeToken(signTrackingToken("msg-123"))).toBeNull();
  });

  test("injects unsubscribe footer into html", () => {
    const html = injectTracking("<p>Hi</p>", "msg-123");
    expect(html).toContain("/api/t/u/");
    expect(html).toContain("Unsubscribe");
    const token = html.match(/api\/t\/u\/([^"]+)/)![1];
    expect(verifyUnsubscribeToken(token)).toBe("msg-123");
  });
});

  test("builds RFC 8058 unsubscribe URL and headers", () => {
    const url = unsubscribeUrl("msg-123");
    expect(url).toContain("/api/t/u/");
    const token = url.split("/api/t/u/")[1];
    expect(verifyUnsubscribeToken(token)).toBe("msg-123");
    const html = injectTracking("<p>Hi</p>", "msg-123");
    expect(html).toContain(url);
  });
