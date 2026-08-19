export function getOrganizationId(request: Request): string {
  // Provisional tenant context until authentication and membership checks exist.
  const organizationId = request.headers.get("x-organization-id")?.trim();
  if (!organizationId) throw new Error("Missing organization context");
  return organizationId;
}

export function assertOrganizationRecord(
  record: { organization_id?: string | null } | null | undefined,
  organizationId: string,
): void {
  if (!record || record.organization_id !== organizationId) {
    throw new Error("Organization access denied");
  }
}
