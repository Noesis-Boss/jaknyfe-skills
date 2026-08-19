import type { SendInput, SendResult, SendingAdapter } from "./types";

export class MockSendingAdapter implements SendingAdapter {
  readonly sent: SendInput[] = [];
  private sequence = 0;

  async send(input: SendInput): Promise<SendResult> {
    this.sent.push({ ...input });
    this.sequence += 1;
    return {
      providerMessageId: `mock-${this.sequence}`,
      acceptedAt: new Date().toISOString(),
    };
  }
}
