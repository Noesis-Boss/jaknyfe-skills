import { createPostgresDatabase } from "../src/server/postgres";
import { sendWithAccountPostgres } from "../src/server/sending/service";

const TO = "don@noesisgroup.com";

async function main() {
  const databaseUrl = process.env.DATABASE_URL;
  if (!databaseUrl) throw new Error("DATABASE_URL is not set");
  if (process.env.LIVE_SEND_TEST !== "1") {
    throw new Error("Refusing to run: set LIVE_SEND_TEST=1 to confirm a real send");
  }

  const database = createPostgresDatabase(databaseUrl);
  try {
    const accounts = await database.query<{ id: string; provider: string; email: string; status: string }>(
      "SELECT id, provider, email, status FROM sending_accounts WHERE provider = 'gmail' AND status = 'active' ORDER BY created_at LIMIT 1",
    );
    if (accounts.length === 0) throw new Error("No active Gmail sending account found");
    const account = accounts[0];
    console.log(`account: ${account.id} (${account.email})`);

    const result = await sendWithAccountPostgres(database, String(account.organization_id ?? (await firstOrg(database))), account.id, {
      from: account.email,
      to: TO,
      subject: `SaaS-Mailer live E2E test ${new Date().toISOString()}`,
      body: "End-to-end live send test from saas-mailer/scripts/live-send-test.ts. Tracking pixel and analytics are exercised separately in tests/tracking.test.ts.",
    });
    console.log(`sent: providerMessageId=${result.providerMessageId} acceptedAt=${result.acceptedAt}`);

    const orgId = await firstOrg(database);
    await database.execute(
      "INSERT INTO events (id, organization_id, message_id, type, payload) VALUES ($1, $2, NULL, 'delivered', $3::jsonb)",
      [crypto.randomUUID(), orgId, JSON.stringify({ providerMessageId: result.providerMessageId, to: TO, source: "live-send-test" })],
    );
    console.log("done");
  } finally {
    await database.close();
  }
}

async function firstOrg(database: ReturnType<typeof createPostgresDatabase>): Promise<string> {
  const rows = await database.query<{ organization_id: string }>(
    "SELECT organization_id FROM sending_accounts WHERE provider = 'gmail' AND status = 'active' ORDER BY created_at LIMIT 1",
  );
  if (rows.length === 0) throw new Error("No organization found for Gmail account");
  return rows[0].organization_id;
}

main().catch((error) => {
  console.error(`FAILED: ${error instanceof Error ? error.message : String(error)}`);
  process.exit(1);
});
