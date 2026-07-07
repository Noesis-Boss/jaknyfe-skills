const GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth";
const GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token";
const GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo";

export function googleAuthUrl(baseUrl: string) {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const params = new URLSearchParams({
    client_id: clientId ?? "",
    redirect_uri: `${baseUrl}/api/auth/google/callback`,
    response_type: "code",
    scope: "openid email profile",
    state: "ok",
    access_type: "offline",
    prompt: "select_account",
  });
  return `${GOOGLE_AUTH_URL}?${params.toString()}`;
}

export async function exchangeGoogleCode(code: string, baseUrl: string) {
  const clientId = process.env.GOOGLE_CLIENT_ID;
  const clientSecret = process.env.GOOGLE_CLIENT_SECRET;
  const res = await fetch(GOOGLE_TOKEN_URL, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      code,
      client_id: clientId ?? "",
      client_secret: clientSecret ?? "",
      redirect_uri: `${baseUrl}/api/auth/google/callback`,
      grant_type: "authorization_code",
    }),
  });
  if (!res.ok) throw new Error(`google token error ${res.status}`);
  const tok = await res.json<{ access_token: string }>();
  const u = await fetch(GOOGLE_USERINFO_URL, {
    headers: { Authorization: `Bearer ${tok.access_token}` },
  });
  if (!u.ok) throw new Error("google userinfo error");
  const info = await u.json<{ email?: string }>();
  return info.email ?? "";
}
