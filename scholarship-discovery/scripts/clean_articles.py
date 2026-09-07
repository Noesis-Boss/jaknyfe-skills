#!/usr/bin/env python3
"""Clean and deduplicate article URLs from a scholarshipregion category page."""
import re, json, sys, os

path = sys.argv[1]
text = open(path, encoding="utf-8").read()

# Extract markdown links
pattern = re.compile(r'\[([^\]]+)\]\s*\(([^)]+)\)', re.IGNORECASE)
matches = pattern.findall(text)

articles = []
seen = set()
skip_prefixes = ('/', 'https://www.scholarshipregion.com/wp-content', 'https://www.scholarshipregion.com/wp-json', 'http://')
skip_titles = ('Home', 'Find', 'About Us', 'Contact Us', 'Advertise', 'Logo')

for title, url in matches:
    url = url.strip().rstrip('"').strip()
    if any(url.startswith(p) for p in skip_prefixes):
        continue
    if title.strip() in skip_titles:
        continue
    if '/category/' in url:
        continue
    if '/tag/' in url:
        continue
    if '/author/' in url:
        continue
    if 'scholarshipregion.com' not in url:
        continue
    # Normalize URL
    if url.startswith('https://www.scholarshipregion.com/'):
        slug = url.replace('https://www.scholarshipregion.com/', '').rstrip('/')
        if ' ' in slug:
            url = 'https://www.scholarshipregion.com/' + slug.split(' ')[0].rstrip('/')
    if url in seen:
        continue
    seen.add(url)
    articles.append({"title": title.strip(), "url": url})

print(json.dumps(articles, indent=2))
print(f"Found {len(articles)} articles")
