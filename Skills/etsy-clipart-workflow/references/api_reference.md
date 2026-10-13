# Etsy Open API v3 notes

Use `https://openapi.etsy.com/v3` or `https://api.etsy.com/v3`. Every request needs `x-api-key: <keystring>:<shared_secret>`. Private and write requests also need an OAuth 2 bearer token.

Required secrets:

- `ETSY_API_KEY` — keystring and shared secret joined with `:`.
- `ETSY_OAUTH_TOKEN` — OAuth 2 access token, including Etsy's numeric user prefix.

The draft workflow uses `listings_w` for draft listing creation, listing-image uploads, and digital-file uploads. Create listings with `type=download`; leave them in draft state until the owner reviews them.

Etsy OAuth uses an authorization-code flow with PKCE and a registered HTTPS redirect URI. The skill does not perform interactive authorization or store tokens. Configure the token outside the repository, then place the resulting values in Zo Settings > Advanced.

References:

- https://developers.etsy.com/documentation/essentials/authentication/
- https://developers.etsy.com/documentation/tutorials/listings/
