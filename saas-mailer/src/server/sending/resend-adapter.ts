import type { SendInput, SendResult, SendingAdapter } from "./types";
import { providerError } from "./provider-error";

export function resendAdapter(apiKey: string, fetcher: typeof fetch = fetch): SendingAdapter {
  return {
    async send(input: SendInput): Promise<SendResult> {
      const response = await fetcher("https://api.resend.com/emails", {
        method: "POST",
        headers: { authorization: `Bearer ${apiKey}`, "content-type": "application/json" },
        body: JSON.stringify({ from: input.from, to: [input.to], subject: input.subject, text: input.body }),
      });
      if (!response.ok) throw providerError(response, await response.text());
      const result = await response.json() as { id?: string };
      if (!result.id) throw new Error("Resend returned no message id");
      return { providerMessageId: result.id, acceptedAt: new Date().toISOString() };
    },
  };
}
