import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";
import type { PostgresDatabase } from "../postgres";
import { repositories } from "../repositories";

export type Campaign = { id: string; organization_id: string; name: string; status: string; campaign_type: 'newsletter' | 'sequence'; preview_text: string; template: string; scheduled_at: string | null; approved_at: string | null; approved_by: string | null; sending_account_id: string | null; sending_window_start: string | null; sending_window_end: string | null; daily_send_limit: number; created_at: string };
export type CampaignStep = { id: string; organization_id: string; campaign_id: string; step_order: number; subject: string; body: string; delay_minutes: number };
export type CampaignInput = { name: string; campaign_type?: 'newsletter' | 'sequence'; preview_text?: string; template?: string; scheduled_at?: string; sending_account_id?: string; sending_window_start?: string; sending_window_end?: string; daily_send_limit?: number; steps?: Array<{ subject: string; body: string; delay_minutes?: number }> };
function validateWindow(value?: string): void { if (value != null && !/^([01]\d|2[0-3]):[0-5]\d$/.test(value)) throw new Error("Invalid sending window"); }

export function createCampaign(database: Database, organizationId: string, input: CampaignInput): Campaign {
  if (!input.name?.trim()) throw new Error("Campaign name is required");
  validateWindow(input.sending_window_start); validateWindow(input.sending_window_end);
  if ((input.sending_window_start == null) !== (input.sending_window_end == null)) throw new Error("Sending window requires start and end");
  if (input.daily_send_limit != null && input.daily_send_limit < 0) throw new Error("Invalid daily send limit");
  if (input.sending_account_id && !database.query("SELECT 1 FROM sending_accounts WHERE id = ? AND organization_id = ? AND status = 'active'").get(input.sending_account_id, organizationId)) throw new Error("Sending account not found or inactive");
  const id = randomUUID();
  database.exec("BEGIN IMMEDIATE");
  try {
    database.query("INSERT INTO campaigns (id, organization_id, name, campaign_type, preview_text, template, scheduled_at, sending_account_id, sending_window_start, sending_window_end, daily_send_limit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)").run(id, organizationId, input.name.trim(), input.campaign_type || 'sequence', input.preview_text || '', input.template || 'plain', input.scheduled_at || null, input.sending_account_id || null, input.sending_window_start || null, input.sending_window_end || null, input.daily_send_limit ?? 100);
    for (const [index, step] of (input.steps || []).entries()) database.query("INSERT INTO campaign_steps (id, organization_id, campaign_id, step_order, subject, body, delay_minutes) VALUES (?, ?, ?, ?, ?, ?, ?)").run(randomUUID(), organizationId, id, index, step.subject, step.body, step.delay_minutes || 0);
    database.exec("COMMIT");
  } catch (error) { database.exec("ROLLBACK"); throw error; }
  return database.query<Campaign, [string]>("SELECT * FROM campaigns WHERE id = ?").get(id) as Campaign;
}

export function approveCampaign(database: Database, campaignId: string, organizationId: string): Campaign {
  const campaign = database.query<Campaign, [string, string]>("SELECT * FROM campaigns WHERE id = ? AND organization_id = ?").get(campaignId, organizationId);
  if (!campaign) throw new Error("Campaign not found");
  const approvedAt = new Date().toISOString();
  const approvedBy = "system:provisional";
  database.query("UPDATE campaigns SET status = 'approved', approved_at = ?, approved_by = ? WHERE id = ? AND organization_id = ?").run(approvedAt, approvedBy, campaignId, organizationId);
  database.query("INSERT INTO audit_log (id, organization_id, action, entity_type, entity_id, metadata) VALUES (?, ?, ?, ?, ?, ?)").run(randomUUID(), organizationId, "campaign.approved", "campaign", campaignId, JSON.stringify({ approved_at: approvedAt, approved_by: approvedBy }));
  return database.query<Campaign, [string]>("SELECT * FROM campaigns WHERE id = ?").get(campaignId) as Campaign;
}

export function enrollContacts(database: Database, campaignId: string, organizationId: string, contactIds: string[]): number {
  const insert = database.query("INSERT OR IGNORE INTO campaign_contacts (campaign_id, contact_id, organization_id) VALUES (?, ?, ?)"); let count = 0;
  for (const contactId of contactIds) if (insert.run(campaignId, contactId, organizationId).changes) count++;
  return count;
}

export async function createCampaignPostgres(database: PostgresDatabase, organizationId: string, input: CampaignInput): Promise<Campaign> {
  if (!input.name?.trim()) throw new Error("Campaign name is required");
  validateWindow(input.sending_window_start); validateWindow(input.sending_window_end);
  if ((input.sending_window_start == null) !== (input.sending_window_end == null)) throw new Error("Sending window requires start and end");
  if (input.daily_send_limit != null && input.daily_send_limit < 0) throw new Error("Invalid daily send limit");
  const repo = repositories({ database, organizationId });
  return repo.transaction(async tx => {
    if (input.sending_account_id && !(await tx.accounts.findActive(input.sending_account_id))) throw new Error("Sending account not found or inactive");
    const campaign = await tx.campaigns.insert(input.name.trim());
    if (!campaign) throw new Error("Unable to create campaign");
    const updated = await tx.campaigns.updateSettings(campaign.id, input.sending_account_id || null, input.sending_window_start || null, input.sending_window_end || null, input.daily_send_limit ?? 100);
    for (const [index, step] of (input.steps || []).entries()) await tx.campaigns.insertStep(campaign.id, index, step.subject, step.body, step.delay_minutes || 0);
    return updated as Campaign;
  });
}

export async function approveCampaignPostgres(database: PostgresDatabase, campaignId: string, organizationId: string): Promise<Campaign> {
  const repo = repositories({ database, organizationId });
  return repo.transaction(async tx => {
    const campaign = await tx.campaigns.find(campaignId);
    if (!campaign) throw new Error("Campaign not found");
    const approvedAt = new Date().toISOString();
    const approved = await tx.campaigns.approve(campaignId, approvedAt, "system:provisional");
    await tx.audit.insert({ action: "campaign.approved", entityType: "campaign", entityId: campaignId, metadata: { approved_at: approvedAt, approved_by: "system:provisional" } });
    return approved as Campaign;
  });
}

export async function enrollContactsPostgres(database: PostgresDatabase, campaignId: string, organizationId: string, contactIds: string[]): Promise<number> {
  const repo = repositories({ database, organizationId });
  return repo.transaction(async tx => {
    let count = 0;
    for (const contactId of contactIds) if (await tx.campaigns.enroll(campaignId, contactId)) count++;
    return count;
  });
}

export function listCampaigns(database: Database, organizationId: string): (Campaign & { step_count: number })[] {
  return database.query<Campaign & { step_count: number }, [string]>("SELECT c.*, (SELECT COUNT(*) FROM campaign_steps s WHERE s.campaign_id = c.id) AS step_count FROM campaigns c WHERE c.organization_id = ? ORDER BY c.created_at DESC, c.id").all(organizationId);
}

export async function listCampaignsPostgres(database: PostgresDatabase, organizationId: string): Promise<(Campaign & { step_count: number })[]> {
  return database.query<Campaign & { step_count: number }>("SELECT c.*, (SELECT COUNT(*)::int FROM campaign_steps s WHERE s.campaign_id = c.id) AS step_count FROM campaigns c WHERE c.organization_id = $1 ORDER BY c.created_at DESC, c.id", [organizationId]);
}
