export type QueuedSendJob = {
  organizationId: string;
  campaignId: string;
  contactId: string;
  sendingAccountId: string;
  stepId?: string;
  subject: string;
  body: string;
  idempotencyKey: string;
};
