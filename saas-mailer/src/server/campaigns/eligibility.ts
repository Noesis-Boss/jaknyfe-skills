export type EligibilityResult = { eligible: true } | { eligible: false; reason: "campaign_not_approved" | "suppressed" | "replied" | "bounced" | "outside_sending_window" | "account_limit_reached" };
export type EligibilityContact = { email: string; suppressed?: boolean; replied?: boolean; bounced?: boolean };
export type EligibilityCampaign = { status?: string; approved_at?: string | null; sending_window_start?: string | null; sending_window_end?: string | null; daily_send_limit?: number; sends_today?: number };

export function isEligibleToSend(contact: EligibilityContact, campaign: EligibilityCampaign, now = new Date()): EligibilityResult {
  if (campaign.status !== "approved" || !campaign.approved_at) return { eligible: false, reason: "campaign_not_approved" };
  if (contact.suppressed) return { eligible: false, reason: "suppressed" };
  if (contact.replied) return { eligible: false, reason: "replied" };
  if (contact.bounced) return { eligible: false, reason: "bounced" };
  const minutes = now.getHours() * 60 + now.getMinutes();
  const parse = (value?: string | null) => value ? Number(value.split(":")[0]) * 60 + Number(value.split(":")[1] || 0) : null;
  const start = parse(campaign.sending_window_start), end = parse(campaign.sending_window_end);
  if (start !== null && end !== null && (start <= end ? minutes < start || minutes > end : minutes < start && minutes > end)) return { eligible: false, reason: "outside_sending_window" };
  if ((campaign.sends_today || 0) >= (campaign.daily_send_limit ?? 100)) return { eligible: false, reason: "account_limit_reached" };
  return { eligible: true };
}
