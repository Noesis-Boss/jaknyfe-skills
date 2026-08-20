import type { Database } from "bun:sqlite";
import { lookupSession } from "./session";
import type { PostgresDatabase } from "../postgres";
import { lookupSessionPostgres } from "./postgres";

export type AuthenticatedTenant = { userId: string; organizationId: string; role: string };

export async function requireTenantPostgres(database: PostgresDatabase, request: Request): Promise<AuthenticatedTenant> {
  const cookie = request.headers.get("cookie")?.match(/(?:^|;\s*)saas_mailer_session=([^;]+)/)?.[1];
  const token = cookie || request.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!token) throw new Error("Authentication required");
  const session = await lookupSessionPostgres(database, decodeURIComponent(token));
  if (!session) throw new Error("Authentication required");
  return { userId: session.userId, organizationId: session.organizationId, role: session.role };
}

export function requireTenant(database: Database, request: Request): AuthenticatedTenant {
  const cookie = request.headers.get("cookie")?.match(/(?:^|;\s*)saas_mailer_session=([^;]+)/)?.[1];
  const token = cookie || request.headers.get("authorization")?.replace(/^Bearer\s+/i, "");
  if (!token) throw new Error("Authentication required");
  const session = lookupSession(database, decodeURIComponent(token));
  if (!session) throw new Error("Authentication required");
  return { userId: session.userId, organizationId: session.organizationId, role: session.role };
}
