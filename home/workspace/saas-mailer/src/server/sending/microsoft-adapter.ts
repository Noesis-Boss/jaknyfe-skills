import type { SendInput, SendResult, SendingAdapter } from "./types";
import { providerError } from "./provider-error";

export function microsoftAdapter(accessToken: string, fetcher: typeof fetch = fetch): SendingAdapter {
  return {
    async send(input): Promise<SendResult> {
      const response = await fetcher("https://graph.microsoft.com/v1.0/me/sendMail", {
        method: "POST",
        headers: { Authorization: `Bearer ${accessToken}`, "Content-Type": "application/json" },
        body: JSON.stringify({ message: { subject: input.subject, body: { contentType: "Text", content: input.body }, toRecipients: [{ emailAddress: { address: input.to } }], from: { emailAddress: { address: input.from } }, internetMessageHeaders: Object.entries(input.headers || {}).map(([name, value]) => ({ name, value })) } }),
      });
      if (!response.ok) throw providerError(response, await response.text());
      return { providerMessageId: response.headers.get("request-id") || `microsoft-${Date.now()}`, acceptedAt: new Date().toISOString() };
    },
  };
}
