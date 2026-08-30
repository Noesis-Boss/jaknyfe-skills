#!/usr/bin/env python3
import argparse, hashlib, json, re, sqlite3, time
import base64
from datetime import datetime, timezone
from urllib.parse import parse_qs, unquote, urljoin, urlparse
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

DBS = ['/home/workspace/scholarsearch/data/processed/scholarships.db', '/home/workspace/scholarsearch-site/data/processed/scholarships.db']
UA = 'Mozilla/5.0 (compatible; ScholarSearchDeepResearch/1.0)'
BLOCKED = re.compile(r'(scholarships?\.com|bold\.org|fastweb|scholarships360|accessscholarships|studentscholarships|appily|cappex|scholarshipportal|apps\.apple|play\.google|facebook|instagram|linkedin|twitter|youtube)', re.I)
BAD_PATH = re.compile(r'/(category|categories|search|browse|directory|blog|news|articles|about|faq|success-stories)(/|$)', re.I)
TERM = re.compile(r'scholarship|fellowship|bursary|grant|award', re.I)
APPLY = re.compile(r'apply|application|submit|portal|form|how to apply', re.I)

def get(url):
    req = Request(url, headers={'User-Agent': UA, 'Accept': 'text/html,application/xhtml+xml'})
    with urlopen(req, timeout=15) as r:
        return r.geturl(), r.read(700000).decode('utf-8', 'replace'), r.status

def norm(v): return re.sub(r'[^a-z0-9]+', ' ', (v or '').lower()).strip()
def nh(name, org): return hashlib.sha1((norm(name)+'||'+norm(org)).encode()).hexdigest()[:12]

def search(query, limit):
    from urllib.parse import quote
    for base, selector in [('https://www.google.com/search?q=', 'a'), ('https://www.bing.com/search?q=', 'li.b_algo h2 a')]:
        try: _, html, _ = get(base + quote(query))
        except Exception: continue
        soup = BeautifulSoup(html, 'html.parser'); out=[]
        base_url = base
        for a in soup.select(selector):
            href = urljoin(base_url, a.get('href','')); qs=parse_qs(urlparse(href).query)
            href=unquote(qs.get('uddg',[href])[0])
            href=unquote(qs.get('q',[href])[0])
            if 'bing.com/ck/a' in href and 'u=a1' in href:
                try: href=base64.urlsafe_b64decode(href.split('u=a1',1)[1].split('&',1)[0]+'===').decode()
                except Exception: continue
            if href.startswith('http') and 'google.' not in urlparse(href).netloc and 'bing.' not in urlparse(href).netloc and href not in out: out.append(href)
        if out: return out[:limit]
    return []

def candidate(page_url, html, anchor_text=''):
    soup=BeautifulSoup(html,'html.parser'); title=(soup.find('h1') or soup.find('title'))
    name=' '.join((title.get_text(' ',strip=True) if title else anchor_text).split())[:180]
    text=' '.join(soup.get_text(' ',strip=True).split())[:10000]
    if not TERM.search(name+' '+text) or BAD_PATH.search(urlparse(page_url).path): return None
    links=[]
    for a in soup.select('a[href]'):
        href=urljoin(page_url,a.get('href','')).split('#')[0]; label=a.get_text(' ',strip=True)
        if href.startswith('http') and APPLY.search(label+' '+href) and not BLOCKED.search(href): links.append(href)
    app=links[0] if links else page_url
    if BLOCKED.search(app) or BAD_PATH.search(urlparse(app).path): return None
    org=urlparse(page_url).netloc.lower().removeprefix('www.').split('.')[0].replace('-',' ').title()
    amount=re.search(r'[$€£]\s*([0-9][0-9,]*)',text); deadline=re.search(r'(?:deadline|due|apply by|closing)[^.;]{0,50}',text,re.I)
    return {'scholarship_name':name,'organization':org,'application_url':app,'website':page_url,'description':text[:1000],'amount_min':int(amount.group(1).replace(',','')) if amount else None,'amount_max':None,'amount_display':('$'+amount.group(1)) if amount else 'Varies','deadline':deadline.group(0)[:160] if deadline else '','eligibility':text[:1500],'source':'deep_research','source_provenance':page_url,'link_notes':'Discovered through search mesh; official endpoint checked.'}

def verify(url):
    if BLOCKED.search(url): return None
    try:
        final, html, status=get(url)
        if status >= 400 or BLOCKED.search(final): return None
        text=' '.join(BeautifulSoup(html,'html.parser').get_text(' ',strip=True).split())
        if not APPLY.search(text) and not re.search(r'apply|application|submit|portal|form',final,re.I): return None
        return final
    except Exception: return None

def insert(c, stamp, idx):
    c=dict(c); c['application_url']=verify(c['application_url'])
    if not c['application_url']: return False
    c['name_hash']=nh(c['scholarship_name'],c['organization']); c['url_status']='verified'; c['verification_score']='B'; c['verification_method']='deep_research'; c['last_checked']=stamp; c['active']=1
    added=False
    for db in DBS:
        con=sqlite3.connect(db); cur=con.cursor()
        cur.execute('select 1 from scholarships where name_hash=? or application_url=?',(c['name_hash'],c['application_url']))
        if cur.fetchone(): con.close(); continue
        cols=['source','source_id','scholarship_name','organization','description','eligibility','amount_min','amount_max','amount_display','deadline','application_url','website','url_status','last_checked','link_notes','name_hash','active','verification_score','verification_method','source_provenance']
        vals=[c.get(x) or '' for x in cols]; vals[1]='deep-'+stamp.replace(' ','T')+'-'+str(idx)
        cur.execute('insert into scholarships ('+','.join(cols)+') values ('+','.join('?' for _ in cols)+')',vals); con.commit(); con.close(); added=True
    return added

def main():
    p=argparse.ArgumentParser(); p.add_argument('--limit',type=int,default=100); p.add_argument('--queries',type=int,default=40); p.add_argument('--results',type=int,default=8); p.add_argument('--seed',action='append',default=[]); a=p.parse_args()
    templates=['site:.edu "scholarship" "apply"','site:.org "scholarship application" students','site:.gov scholarship application students','"2026 scholarship" "apply now" foundation','"2026 scholarship application" university','"scholarship portal" students 2026']
    found=[]; seen=set()
    seed_urls=list(a.seed)
    for u in seed_urls:
        try: final,html,_=get(u)
        except Exception: continue
        c=candidate(final,html)
        if c: found.append(c); seen.add(u)
    for i in range(a.queries):
        urls=search(templates[i%len(templates)],a.results)
        for u in urls:
            if u in seen: continue
            seen.add(u)
            try: final,html,_=get(u)
            except Exception: continue
            c=candidate(final,html)
            if c: found.append(c)
            soup=BeautifulSoup(html,'html.parser')
            for anchor in soup.select('a[href]'):
                label=' '.join(anchor.get_text(' ',strip=True).split())
                link=urljoin(final,anchor.get('href','')).split('#')[0]
                if len(label)>=10 and TERM.search(label) and link.startswith('http') and link not in seen and urlparse(link).netloc==urlparse(final).netloc:
                    seen.add(link)
                    try: detail,body,_=get(link)
                    except Exception: continue
                    item=candidate(detail,body,label)
                    if item: found.append(item)
                    if len(found)>=a.limit*3: break
            if len(found)>=a.limit*3: break
        if len(found)>=a.limit*3: break
    stamp=datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S'); added=0
    for i,c in enumerate(found[:a.limit*2],1):
        if insert(c,stamp,i): added+=1
    print(json.dumps({'queries':a.queries,'candidates':len(found),'added':added,'target':a.limit,'shortfall':max(0,a.limit-added)}))
if __name__=='__main__': main()
