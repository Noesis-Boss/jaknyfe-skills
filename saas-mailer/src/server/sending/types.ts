export type SendInput = {
  from: string;
  to: string;
  subject: string;
  body: string;
};

export type SendResult = {
  providerMessageId: string;
  acceptedAt: string;
};

export interface SendingAdapter {
  send(input: SendInput): Promise<SendResult>;
}

export type SendingAccount = {
  id: string;
  organization_id: string;
  provider: string;
  email: string;
  status: string;
  created_at: string;
};

export type ConnectSendingAccountInput = {
  provider: string;
  email: string;
  credentials: Record<string, unknown>;
};
