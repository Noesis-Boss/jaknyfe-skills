import type { SendInput, SendResult, SendingAdapter } from "./types";
import { providerError } from "./provider-error";

function base64Url(value: string): string {
  return Buffer.from(value).toString("base64url");
}

function message(input: SendInput): string {
  return [`From: ${input.from}`, `To: ${input.to}`, `Subject: ${input.subject}`, "MIME-Version: 1.0", "Content-Type: text/plain; charset=utf-8", "", input.body].join("\\r\\n");
}

export function gmailAdapter(accessToken: string, fetcher: typeof fetch = fetch): SendingAdapter {
  return {
    async send(input): Promise<SendResult> {
      const response = await fetcher("https://gmail.googleapis.com/gmail/v1/users/me/messages/send", {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" },
        body: JSON.stringify({ raw: base64Url(message(input)) }),
      });
      if (!response.ok) throw providerError(response, await response.text());
      const result = await response.json() as { id?: string };
      if (!result.id) throw new Error("Gmail returned no message id");
      return { providerMessageId: result.id, acceptedAt: new Date().toISOString() };
    },
  };
}
