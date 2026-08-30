import json, sys
from pathlib import Path

TUSK_DIR = Path.home() / ".tuskcentral"
COOKIES_FILE = TUSK_DIR / "cookies.json"
SESSION_FILE = TUSK_DIR / "session.json"

def main():
    if not COOKIES_FILE.exists():
        print("No cookies.json found")
        sys.exit(1)

    cookies_raw = json.loads(COOKIES_FILE.read_text())

    # Convert flat dict to Playwright cookie objects
    cookies = []
    for name, value in cookies_raw.items():
        cookies.append({
            "name": name,
            "value": value,
            "domain": ".tuskcentral.ai",
            "path": "/",
            "httpOnly": name.startswith("__"),
            "secure": True,
            "sameSite": "Lax",
        })

    # Build minimal origins list (localStorage)
    origins = [
        {
            "origin": "https://tuskcentral.ai",
            "localStorage": [
                {"name": "__clerk_environment", "value": '{"value":{"object":"environment","auth_config":{"claimed_at":null,"id":"","object":"auth_config","reverification":true,"single_session_mode":true,"session_minter":true},"display_config":{"object":"display_config","after_create_organization_url":"https://tuskcentral.ai","after_join_waitlist_url":"https://tuskcentral.ai","after_leave_organization_url":"https://tuskcentral.ai","after_sign_in_url":"https://tuskcentral.ai","after_sign_out_all_url":"https://accounts.tuskcentral.ai/sign-in","after_sign_out_one_url":"https://accounts.tuskcentral.ai/sign-in/choose","after_sign_up_url":"https://tuskcentral.ai","application_name":"Tusk Central AI","branded":true,"captcha_heartbeat":false,"captcha_oauth_bypass":[],"captcha_provider":"turnstile","captcha_public_key_invisible":"0x4AAAAAAAFV93qQdS0ycilX","captcha_public_key":"0x4AAAAAAAWXJGBD7bONzLBd","captcha_widget_type":"smart","clerk_js_version":"6","create_organization_url":"https://accounts.tuskcentral.ai/create-organization","favicon_image_url":"https://img.clerk.com/eyJ0eXBlIjoicHJveHkiLCJzcmMiOiJodHRwczovL2ltYWdlcy5jbGVyay5kZXYvdXBsb2FkZWQvaW1nXzNEc3dKQWxPUUdRTzI4TlFqQnQ2SGRJRXdKSiJ9","google_one_tap_client_id":"804316029044-91sf9oefekm138imq7854ut29prqibb6.apps.googleusercontent.com","home_url":"https://tuskcentral.ai","id":"display_config_3DssXpNbGsSlfcPSAtT2sCg7oYK","instance_environment_type":"production","logo_image_url":"https://img.clerk.com/eyJ0eXBlIjoicHJveHkiLCJzcmMiOiJodHRwczovL2ltYWdlcy5jbGVyay5kZXYvdXBsb2FkZWQvaW1nXzNEc3dFc1E5WGxpc0ZKWjVXdXJmeXJ1cGozYSJ9","organization_profile_url":"https://accounts.tuskcentral.ai/organization","preferred_sign_in_strategy":"otp","privacy_policy_url":"https://tuskcentral.ai/privacy-policy","show_devmode_warning":false,"sign_in_url":"https://accounts.tuskcentral.ai/sign-in","sign_up_url":"https://accounts.tuskcentral.ai/sign-up","support_email":"support@tuskcentral.zendesk.com","terms_url":"https://tuskcentral.ai/terms-of-service","theme":{"buttons":{"font_color":"#ffffff","font_family":"\\"Source Sans Pro\\", sans-serif","font_weight":"600"},"general":{"color":"#0072BA","padding":"1em","box_shadow":"0 2px 8px rgba(0, 0, 0, 0.2)","font_color":"#151515","font_family":"\\"Source Sans Pro\\", sans-serif","border_radius":"0.5em","background_color":"#ffffff","label_font_weight":"600"},"accounts":{"background_color":"#ffffff"}},"user_profile_url":"https://accounts.tuskcentral.ai/user","waitlist_url":"https://tuskcentral.ai/waitlist"},"id":"","maintenance_mode":false,"client_debug_mode":false,"partitioned_cookies":false,"organization_settings":{"actions":{"admin_delete":true},"domains":{"enabled":false,"enrollment_modes":[],"default_role":""},"enabled":false,"max_allowed_memberships":20},"user_settings":{"actions":{"delete_self":true,"create_organization":true,"create_organizations_limit":null},"attributes":{"email_address":{"enabled":true,"required":false,"used_for_first_factor":true,"first_factors":["email_code"],"used_for_second_factor":false,"second_factors":[],"verifications":["email_code"],"verify_at_sign_up":true,"immutable":true,"name":"email_address"},"phone_number":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"phone_number"},"username":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"username"},"web3_wallet":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"web3_wallet"},"first_name":{"enabled":true,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"first_name"},"last_name":{"enabled":true,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"last_name"},"password":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"password"},"authenticator_app":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"authenticator_app"},"ticket":{"enabled":true,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"ticket"},"backup_code":{"enabled":false,"required":false,"used_for_first_factor":false,"first_factors":[],"used_for_second_factor":false,"second_factors":[],"verifications":[],"verify_at_sign_up":false,"immutable":false,"name":"backup_code"},"passkey_settings":{"allow_autofill":true,"show_sign_in_button":true,"satisfies_second_factor":false},"password_settings":{"disable_hibp":false,"min_length":8,"max_length":72,"require_special_char":false,"require_numbers":false,"require_uppercase":false,"require_lowercase":false,"show_zxcvbn":true,"min_zxcvbn_strength":2,"enforce_hibp_at_sign_up":true,"allowed_special_characters":"!\\"#$%&'()*+,-./:;<=>?@[]^_`{|}~"},"saml":{"enabled":false},"sign_in":{"second_factor":{"required":false}},"sign_up":{"captcha_enabled":true,"captcha_widget_type":"smart","custom_action_required":false,"progressive":true,"mode":"public","legal_consent_enabled":true,"mfa":{"required":false},"social":{"oauth_apple":{"enabled":true,"required":false,"authenticatable":true,"block_email_subaddresses":false,"strategy":"oauth_apple","not_selectable":false,"deprecated":false,"name":"Apple","logo_url":"https://img.clerk.com/static/apple.png"},"oauth_discord":{"enabled":false,"required":false,"authenticatable":true,"block_email_subaddresses":false,"strategy":"oauth_discord","not_selectable":false,"deprecated":false,"name":"Discord","logo_url":"https://img.clerk.com/static/discord.png"},"oauth_facebook":{"enabled":true,"required":false,"authenticatable":true,"block_email_subaddresses":false,"strategy":"oauth_facebook","not_selectable":false,"deprecated":false,"name":"Facebook","logo_url":"https://img.clerk.com/static/facebook.png"},"oauth_google":{"enabled":true,"required":false,"authenticatable":true,"block_email_subaddresses":false,"strategy":"oauth_google","not_selectable":false,"deprecated":false,"name":"Google","logo_url":"https://img.clerk.com/static/google.png"}}},"protect_config":{"object":"protect_config","id":""}},"exp":1784139743512}'}]
            }
        }
    ]

    state = {"cookies": cookies, "origins": origins}
    SESSION_FILE.write_text(json.dumps(state, indent=2))
    print(f"Wrote Playwright storage state to {SESSION_FILE}")
    print(f"Cookies: {len(cookies)}, Origins: {len(origins)}")

if __name__ == "__main__":
    main()
