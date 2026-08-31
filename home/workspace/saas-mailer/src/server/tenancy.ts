export function assertOrganizationRecord(
  record: { organization_id?: string | null } | null | undefined,
  organizationId: string,
): void {
  if (!record || record.organization_id !== organizationId) {
    throw new Error("Organization access denied");
  }
}
