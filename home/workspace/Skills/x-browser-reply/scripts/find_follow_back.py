#!/usr/bin/env python3
"""Find X/Twitter posts advertising follow-back and extract tweet IDs."""

import argparse
import json
import re
import sys
import urllib.request
import urllib.parse


def search_follow_back(query: str, max_results: int = 10) -> list[dict]:
    """Search X for follow-back posts using web search."""
    
    search_queries = [
        'site:x.com "follow back" -from:jak_nyfe -from:zdsentry',
        'site:x.com "follow for follow" -from:jaknyfe -from:zdsentry',
        'site:x.com "I follow back" -from:jaknyfe -from:zdsentry',
        'site:x.com "f4f" -from:jaknyfe -from:zdsentry',
        'site:x.com "follow me I follow back" -from:jaknyfe -from:zdsentry',
    ]
    
    results = []
    seen_ids = set()
    
    for sq in search_queries:
        if len(results) >= max_results:
            break
            
        encoded = urllib.parse.quote(sq)
        url = f"https://www.google.com/search?q={encoded}&num=10"
        
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            })
            with urllib.request.urlopen(req, timeout=15) as resp:
                html = resp.read().decode("utf-8", errors="replace")
            
            # Extract tweet IDs from URLs like https://x.com/username/status/1234567890
            pattern = r'x\.com/([^/]+)/status/(\d+)'
            matches = re.findall(pattern, html)
            
            for username, tweet_id in matches:
                if tweet_id in seen_ids:
                    continue
                if username.lower() in ('jaknyfe', 'jak_nyfe', 'zdsentry'):
                    continue
                    
                seen_ids.add(tweet_id)
                results.append({
                    "tweet_id": tweet_id,
                    "username": username,
                    "url": f"https://x.com/{username}/status/{tweet_id}"
                })
                
                if len(results) >= max_results:
                    break
                    
        except Exception as e:
            print(f"  Search failed for query: {e}", file=sys.stderr)
            continue
    
    return results[:max_results]


def main():
    parser = argparse.ArgumentParser(description="Find X follow-back posts")
    parser.add_argument("--max", type=int, default=5, help="Max results")
    parser.add_argument("--query", type=str, default=None, help="Custom search query")
    args = parser.parse_args()
    
    print(f"Searching X for follow-back posts (max {args.max})...", file=sys.stderr)
    
    if args.query:
        results = search_follow_back(args.query, args.max)
    else:
        results = search_follow_back("", args.max)
    
    print(f"Found {len(results)} follow-back posts", file=sys.stderr)
    
    # Output as JSON for automation processing
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
