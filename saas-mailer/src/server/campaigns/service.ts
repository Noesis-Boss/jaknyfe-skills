import { randomUUID } from "node:crypto";
import type { Database } from "bun:sqlite";

export type Campaign = { id: string; organization_id: string; name: string; status: string; approved_at: string | null; approved_by: string | null; sending_account_id: string | null; sending_window_start: string | null; sending_window_end: string | null; daily_send_limit: number; created_at: string };
export type CampaignStep = { id: string; organization_id: string; campaign_id: string; step_order: number; subject: string; body: string; delay_minutes: number };
export type CampaignInput = { name: string; sending_account_id?: string; sending_window_start?: string; sending_window_end?: string; daily_send_limit?: number; steps?: Array<{ subject: string; body: string; delay_minutes?: number }> };
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
    database.query("INSERT INTO campaigns (id, organization_id, name, sending_account_id, sending_window_start, sending_window_end, daily_send_limit) VALUES (?, ?, ?, ?, ?, ?, ?)").run(id, organizationId, input.name.trim(), input.sending_account_id || null, input.sending_window_start || null, input.sending_window_end || null, input.daily_send_limit ?? 100);
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
