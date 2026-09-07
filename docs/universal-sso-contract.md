# Noesis Universal SSO Contract

Status: active baseline — 2026-09-02

`https://auth.noesisgroup.com` is the shared identity provider for Noesis applications. Authentik owns identity lifecycle; each application owns only its local authorization and tenant data.

## Provider contract

- Issuer: `https://auth.noesisgroup.com`
- Discovery: `${AUTH_ISSUER}/.well-known/openid-configuration`
- Protocol: OpenID Connect Authorization Code flow with PKCE (`S256`)
- Scopes: `openid profile email`
- Required identity key: normalized, verified `email`; retain the provider `sub` as the durable external subject when available
- Signup destination: `https://auth.noesisgroup.com/if/flow/noesis-self-signup/`

Applications must discover endpoints from the issuer metadata, validate issuer, audience, signature, nonce/state, redirect URI, and token expiry, and use HTTPS in production. Never accept an email or role from an unverified browser request.

## Per-application configuration

Each app receives a separate Authentik OIDC client. Keep these values in the deployment secret store, not source control:

```text
AUTH_ISSUER=https://auth.noesisgroup.com
AUTH_CLIENT_ID=<app-specific client id>
AUTH_CLIENT_SECRET=<app-specific secret>
AUTH_CALLBACK_ORIGIN=https://<app-host>
AUTH_REDIRECT_PATH=/api/auth/oidc/callback
AUTH_POST_LOGOUT_REDIRECT_URI=https://<app-host>/
```

The complete redirect URI is the callback origin plus redirect path. Register exact URIs only; do not use wildcards. Local development may use a separate client and localhost callback.

## Application responsibilities

1. Send unauthenticated users to the provider authorization endpoint.
2. Protect the callback with state and PKCE; use a short-lived, HttpOnly, SameSite=Lax state cookie.
3. Exchange the code server-side and validate the ID token/userinfo response.
4. Create or resume a local session from the verified identity.
5. Map the identity to local membership, roles, or tenant access. Missing membership is an application authorization failure, not a reason to create an account silently.
6. Provide logout that clears the local session and optionally redirects through the provider end-session endpoint.

Existing local accounts should be linked only by an explicit, verified identity-linking flow. Do not merge accounts solely because an unverified email string matches.

## Authentik policy

- One client per application and environment.
- Shared signup, login, recovery, and MFA flows.
- Stable claims: `sub`, `email`, `email_verified`, `name`, `preferred_username`.
- Roles and tenant permissions remain application-owned unless a future group/claim contract is documented and tested.
- Origin/Referer checks can supplement signup protection but do not replace signed, short-lived app-issued signup tokens.

## Onboarding checklist

- [ ] Confirm issuer discovery and TLS.
- [ ] Create a dedicated Authentik provider/application/client.
- [ ] Register exact production and development callback URLs.
- [ ] Add deployment secrets using the names above.
- [ ] Implement authorization-code + PKCE callback and local session creation.
- [ ] Test first login, repeat login, logout, expired state, bad state, bad code, and missing membership.
- [ ] Screenshot the actual login surface and verify the callback in a non-production test account.
- [ ] Record the client name, callback URI, claims, and local role mapping in the app's `AGENTS.md` without recording secrets.

## Current adopters

- Momball: Authentik protects the admin surface; local admin authorization remains app-owned.
- SaaS-Mailer: Authentik login creates/reuses the existing tenant session; organization membership remains app-owned.
