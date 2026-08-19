import { describe, expect, test } from "bun:test";
import { assertOrganizationRecord, getOrganizationId } from "../src/server/tenancy";

describe("tenant helpers", () => {
  test("reads the organization ID from the request", () => {
    const request = new Request("http://localhost/", {
      headers: { "x-organization-id": "org-123" },
    });

    expect(getOrganizationId(request)).toBe("org-123");
  });

  test("rejects a request without organization context", () => {
    expect(() => getOrganizationId(new Request("http://localhost/"))).toThrow(
      "Missing organization context",
    );
  });

  test("allows records belonging to the active organization", () => {
    expect(() => assertOrganizationRecord({ organization_id: "org-123" }, "org-123")).not.toThrow();
  });

  test("rejects records belonging to another organization", () => {
    expect(() => assertOrganizationRecord({ organization_id: "org-999" }, "org-123")).toThrow(
      "Organization access denied",
    );
  });
});
