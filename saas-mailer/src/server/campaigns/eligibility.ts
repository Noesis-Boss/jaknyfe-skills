export type EligibilityResult = { eligible: true } | { eligible: false; reason: "campaign_not_approved" | "suppressed" | "replied" | "bounced" | "outside_sending_window" | "account_limit_reached" };
export type EligibilityContact = { email: string; suppressed?: boolean; replied?: boolean; bounced?: boolean };
export type EligibilityCampaign = { status?: string; approved_at?: string | null; sending_window_start?: string | null; sending_window_end?: string | null; daily_send_limit?: number; sends_today?: number };

function parseTime(value: string | null | undefined): number | null {
  if (value == null) return null;
  if (!/^([01]\d|2[0-3]):[0-5]\d$/.test(value)) throw new Error("Invalid sending window");
  const [hours, minutes] = value.split(":").map(Number);
  return hours * 60 + minutes;
}

export function isEligibleToSend(contact: EligibilityContact, campaign: EligibilityCampaign, now = new Date()): EligibilityResult {
  if (campaign.status !== "approved" || !campaign.approved_at) return { eligible: false, reason: "campaign_not_approved" };
  if (contact.suppressed) return { eligible: false, reason: "suppressed" };
  if (contact.replied) return { eligible: false, reason: "replied" };
  if (contact.bounced) return { eligible: false, reason: "bounced" };
  const minutes = now.getUTCHours() * 60 + now.getUTCMinutes();
  const start = parseTime(campaign.sending_window_start), end = parseTime(campaign.sending_window_end);
  if (start !== null && end !== null && (start <= end ? minutes < start || minutes > end : minutes < start && minutes > end)) return { eligible: false, reason: "outside_sending_window" };
  if ((campaign.sends_today || 0) >= (campaign.daily_send_limit ?? 100)) return { eligible: false, reason: "account_limit_reached" };
  return { eligible: true };
}

export function loadQueueEligibility(database: any, organizationId: string, campaignId: string, contactId: string, now = new Date()): EligibilityResult {
  const state = database.query<any, [string, string, string, string]>(`SELECT c.status, c.approved_at, c.sending_window_start, c.sending_window_end,
    ct.email, sa.status AS account_status, sa.daily_send_limit AS account_daily_send_limit,
    EXISTS (SELECT 1 FROM suppression_list sl WHERE sl.organization_id = c.organization_id AND lower(sl.email) = lower(ct.email)) AS suppressed,
    EXISTS (SELECT 1 FROM events e WHERE e.organization_id = c.organization_id AND e.contact_id = ct.id AND e.type = 'reply') AS replied,
    EXISTS (SELECT 1 FROM events e WHERE e.organization_id = c.organization_id AND e.contact_id = ct.id AND e.type = 'bounce') AS bounced,
    (SELECT COUNT(*) FROM messages m WHERE m.organization_id = c.organization_id AND m.sending_account_id = c.sending_account_id AND m.status = 'sent' AND date(m.sent_at) = date(?)) AS sends_today
    FROM campaigns c JOIN contacts ct ON ct.organization_id = c.organization_id AND ct.id = ?
    LEFT JOIN sending_accounts sa ON sa.organization_id = c.organization_id AND sa.id = c.sending_account_id
    WHERE c.organization_id = ? AND c.id = ?`).get(now.toISOString(), contactId, organizationId, campaignId);
  if (!state || !state.account_status) return { eligible: false, reason: "campaign_not_approved" };
  if (state.account_status !== "active") return { eligible: false, reason: "account_limit_reached" };
  return isEligibleToSend({ email: state.email, suppressed: Boolean(state.suppressed), replied: Boolean(state.replied), bounced: Boolean(state.bounced) }, { ...state, daily_send_limit: state.account_daily_send_limit, sends_today: state.sends_today });
}
