// Sends the magic-link email via Resend REST API.
// Requires RESEND_API_KEY secret in Settings > Advanced.
const RESEND_API_KEY = process.env.RESEND_API_KEY;
const FROM = process.env.RESEND_FROM || "The Walk + Protein Method <onboarding@resend.dev>";

export function resendConfigured() {
  return !!RESEND_API_KEY;
}

export async function sendMagicLink(email: string, link: string) {
  if (!RESEND_API_KEY) {
    throw new Error("RESEND_API_KEY not set");
  }
  const res = await fetch("https://api.resend.com/emails", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${RESEND_API_KEY}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      from: FROM,
      to: email,
      subject: "Your sign-in link — The Walk + Protein Method",
      html: `
        <div style="font-family: system-ui, sans-serif; max-width: 480px; margin: 0 auto;">
          <h2 style="color:#16a34a;">Your magic sign-in link</h2>
          <p>Click the button below to sign in to your weight-loss tracker. This link expires in 15 minutes.</p>
          <p style="margin: 28px 0;">
            <a href="${link}" style="background:#16a34a; color:#fff; padding:12px 22px; border-radius:8px; text-decoration:none; font-weight:600;">Sign in</a>
          </p>
          <p style="color:#666; font-size:13px;">If you didn't request this, you can ignore this email.</p>
        </div>
      `,
    }),
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Resend failed: ${res.status} ${body}`);
  }
  return res.json();
}
