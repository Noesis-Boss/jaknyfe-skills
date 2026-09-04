#!/usr/bin/env python3
import argparse, json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin
from urllib.request import Request, urlopen

UA = 'Mozilla/5.0 (compatible; ScholarSearchUniversityRegistry/1.0)'
PATHS = ('/financial-aid/scholarships', '/financial-aid/types-of-aid/scholarships', '/scholarships', '/financialaid/scholarships', '/admissions/financial-aid/scholarships')

def check(item):
    base = item.get('web_pages', [''])[0].rstrip('/') + '/'
    urls = [base] + [urljoin(base, p.lstrip('/')) for p in PATHS]
    for url in urls:
        try:
            req = Request(url, headers={'User-Agent': UA, 'Accept': 'text/html'})
            with urlopen(req, timeout=8) as r:
                if 200 <= r.status < 400 and 'text/html' in r.headers.get('content-type', ''):
                    return {'name': item['name'], 'url': r.geturl(), 'domain': item.get('domains', [''])[0]}
        except Exception:
            pass
    return None

def main():
    p = argparse.ArgumentParser(); p.add_argument('--input', required=True); p.add_argument('--output', required=True); p.add_argument('--workers', type=int, default=32); p.add_argument('--limit', type=int, default=0); a = p.parse_args()
    data = json.load(open(a.input)); items = [x for x in data if x.get('country') == 'United States' and x.get('web_pages') and x.get('domains')]
    if a.limit: items = items[:a.limit]
    out = []
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        futures = [pool.submit(check, x) for x in items]
        for f in as_completed(futures):
            v = f.result()
            if v: out.append(v)
    out.sort(key=lambda x: x['name'].lower())
    json.dump(out, open(a.output, 'w'), indent=2)
    print(json.dumps({'institutions': len(items), 'reachable_sources': len(out), 'output': a.output}))

if __name__ == '__main__': main()
