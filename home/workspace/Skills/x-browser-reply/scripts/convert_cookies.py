#!/usr/bin/env python3
"""Convert Netscape cookies to Playwright JSON format."""

import json
import sys
from datetime import datetime


def parse_cookies_from_text(text):
    """Parse cookies from tab-separated text."""
    cookies = []
    for line in text.strip().split('\n'):
        if not line.strip():
            continue
        parts = line.split('\t')
        if len(parts) < 7:
            continue
        name, value, domain, path, expires, size, http_only = parts[0], parts[1], parts[2], parts[3], parts[4], parts[5], parts[6]
        # Convert expires to timestamp
        try:
            expires_dt = datetime.fromisoformat(expires.replace('Z', '+00:00'))
            expires_ts = expires_dt.timestamp()
        except:
            expires_ts = -1  # Session cookie

        cookie = {
            "name": name,
            "value": value,
            "domain": domain,
            "path": path,
            "expires": expires_ts,
            "httpOnly": "✓" in http_only,
            "secure": False,
            "sameSite": "Lax"
        }
        cookies.append(cookie)
    return cookies


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python convert_cookies.py < input.txt > output.json")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else input_file.replace('.txt', '.json')

    with open(input_file) as f:
        text = f.read()

    cookies = parse_cookies_from_text(text)

    with open(output_file, 'w') as f:
        json.dump({"cookies": cookies}, f, indent=2)

    print(f"Converted {len(cookies)} cookies to {output_file}")
