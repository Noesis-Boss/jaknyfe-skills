#!/usr/bin/env python3
"""Extract article URLs from a scholarshipregion category markdown."""
import re, json, sys, os

path = sys.argv[1]
text = open(path, encoding="utf-8").read()

# Extract markdown links with scholarship titles
pattern = re.compile(r'\[([^\]]+scholarship[^\]]*)\]\s*\(([^)]+)\)', re.IGNORECASE)
matches = pattern.findall(text)

articles = []
seen = set()
for title, url in matches:
    # Only keep links to article pages on scholarshipregion.com
    if 'scholarshipregion.com' not in url:
        continue
    if url in seen:
        continue
    seen.add(url)
    articles.append({"title": title.strip(), "url": url})

print(json.dumps(articles, indent=2))
print(f"Found {len(articles)} articles")
