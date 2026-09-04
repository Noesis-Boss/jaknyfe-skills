#!/usr/bin/env python3
import argparse, json, sys
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import deep_research as dr

GENERIC = ('financial aid', 'scholarship office', 'scholarships', 'types of aid', 'contact', 'faq', 'admission', 'overawards', 'outside scholarships', 'search for')

def links(seed, html):
    host=urlparse(seed).netloc
    out=[]; seen=set()
    soup=BeautifulSoup(html, 'html.parser')
    for a in soup.select('a[href]'):
        href=urljoin(seed,a.get('href','')).split('#')[0]
        label=' '.join(a.get_text(' ',strip=True).split())
        if urlparse(href).netloc != host or href in seen: continue
        if not dr.TERM.search(label) or len(label)<10: continue
        if any(x in urlparse(href).path.lower() for x in ('/category','/directory','/search','/news','/blog')): continue
        seen.add(href); out.append((href,label))
    return out

def main():
    p=argparse.ArgumentParser(); p.add_argument('sources', nargs='+'); p.add_argument('--limit',type=int,default=100); a=p.parse_args()
    candidates=[]; seen=set()
    for seed in a.sources:
        try: final,html,_=dr.get(seed)
        except Exception as e: print(f'skip {seed}: {e}'); continue
        for href,label in links(final,html)[:a.limit]:
            if href in seen: continue
            seen.add(href)
            try: detail,body,_=dr.get(href)
            except Exception: continue
            c=dr.candidate(detail,body,label)
            if not c or c['scholarship_name'].lower().strip().startswith(GENERIC): continue
            c['organization']=urlparse(final).netloc.replace('www.','').split('.')[0].replace('-',' ').title()
            c['source']='university_directory'; c['source_provenance']=seed
            candidates.append(c)
            if len(candidates)>=a.limit: break
        if len(candidates)>=a.limit: break
    stamp=__import__('datetime').datetime.now(__import__('datetime').timezone.utc).strftime('%Y%m%d%H%M%S')
    added=sum(dr.insert(c,stamp,i) for i,c in enumerate(candidates,1))
    print(json.dumps({'sources':len(a.sources),'candidates':len(candidates),'added':added,'target':a.limit,'shortfall':max(0,a.limit-added)}))

if __name__=='__main__': main()
