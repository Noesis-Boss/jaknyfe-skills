import json, glob, re
from urllib.parse import urlparse

files = sorted(glob.glob('/home/.z/workspaces/con_Xg1QFfyDCEtjEY8u/read_webpage/web_search*.json'))
items = []
for f in files:
    with open(f) as fh:
        items.extend(json.load(fh))

BLOCKED_DOMAINS = {
    'fastweb.com', 'scholarships360.org', 'collegeboard.org', 'study.com',
    'scholarships.com', 'cappex.com', 'unigo.com', 'instagram.com',
    'facebook.com', 'twitter.com', 'x.com', 'linkedin.com', 'youtube.com',
    'reddit.com', 'accessscholarships.com', 'bold.org', 'studyabroad.com',
    'townandgownofusc.org'
}

BLOCKED_TITLE_PREFIXES = [
    'when to apply', 'top 1645', 'top 283', 'make uk:',
    'how to', 'tips', 'checklist', 'blog', 'article'
]

SEQ = 0

def extract(text):
    global SEQ
    # Amount
    amt_min = amt_max = None
    amt_display = 'Varies'
    nums = []
    for m in re.finditer(r'[\\$\,\\€\\£]\\s*([0-9,]+)', text.replace(',', '')):
        n = int(m.group(1))
        if 100 < n < 500000:
            nums.append(n)
    if nums:
        amt_min = min(nums)
        amt_max = max(nums) if len(nums) > 1 else None
        if amt_min == amt_max:
            amt_display = f'${amt_min:,}'
        elif amt_max is not None:
            amt_display = f'${amt_min:,} - ${amt_max:,}'
        else:
            amt_display = f'${amt_min:,}+'
    
    # Deadline
    dl = ''
    m = re.search(r'(?:deadline|due date|closing|due)[:\\s]+([A-Za-z]+ \\d{1,2},? \\d{4}|\\d{4}-\\d{2}-\\d{2})', text, re.I)
    if m:
        dl = m.group(1)
    
    return amt_min, amt_max, amt_display, dl

def guess_education(text):
    c = text.lower()
    if any(t in c for t in ['phd', 'doctorate', 'doctoral']):
        return 'Graduate'
    if any(t in c for t in ['masters', 'master\'s', 'mba', 'graduate']):
        return 'Graduate'
    if any(t in c for t in ['community college', 'associate']):
        return 'Associate'
    if any(t in c for t in ['high school', 'freshman', 'sophomore', 'junior', 'senior', 'undergraduate', 'bachelor']):
        return 'Undergraduate'
    return 'Undergraduate'

def guess_country(url):
    domain = urlparse(url).netloc.lower()
    if '.gc.ca' in domain or 'canada.ca' in domain:
        return 'Canada'
    if '.ac.uk' in domain or 'ucas' in domain:
        return 'UK'
    if 'edu.au' in domain:
        return 'Australia'
    if any(t in domain for t in ['daad', 'erasmus']):
        return 'EU'
    if '.edu' in domain:
        return 'USA'
    return 'International'

def guess_state(text):
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "tennessee": "TN", "missouri": "MO", "maryland": "MD", "minnesota": "MN",
        "wisconsin": "WI", "alabama": "AL", "kansas": "KS", "new jersey": "NJ",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

results = []
for it in items:
    url = it['url']
    title = it['title']
    text = it.get('text', '')
    domain = urlparse(url).netloc.lower()
    
    # Skip blocked domains
    if any(domain.endswith(b) for b in BLOCKED_DOMAINS):
        continue
    # Skip listing/homepage-like titles
    tl = title.lower()
    if any(tl.startswith(p) for p in BLOCKED_TITLE_PREFIXES):
        continue
    if tl in ['uk parliament', 'make uk: the manufacturers\' organisation']:
        continue
    if len(tl) < 8:
        continue
    # Skip non-scholarship pages
    if not re.search(r'scholarship|bursary|fellowship|grant|award', title.lower() + ' ' + text.lower(), re.I):
        continue
    
    amt_min, amt_max, amt_display, dl = extract(text)
    residency = guess_country(url)
    state = guess_state(text)
    # Only set state if URL itself suggests it (avoid false positives from unrelated text)
    if state and not any(s in url for s in [state.lower(), state.title()] + [k.replace('_', ' ').title()[:-2] for k,v in {'alabama':'al','alaska':'ak','arizona':'az','arkansas':'ar','california':'ca','colorado':'co','connecticut':'ct','delaware':'de','florida':'fl','georgia':'ga','hawaii':'hi','idaho':'id','illinois':'il','indiana':'in','iowa':'ia','kansas':'ks','kentucky':'ky','louisiana':'la','maine':'me','maryland':'md','massachusetts':'ma','michigan':'mi','minnesota':'mn','mississippi':'ms','missouri':'mo','montana':'mt','nebraska':'ne','nevada':'nv','new hampshire':'nh','new jersey':'nj','new mexico':'nm','new york':'ny','north carolina':'nc','north dakota':'nd','ohio':'oh','oklahoma':'ok','oregon':'or','pennsylvania':'pa','rhode island':'ri','south carolina':'sc','south dakota':'sd','tennessee':'tn','texas':'tx','utah':'ut','vermont':'vt','virginia':'va','washington':'wa','west virginia':'wv','wisconsin':'wi','wyoming':'wy'}.items()]):
        state = None
    
    org = urlparse(url).netloc.replace('www.', '').split('.')[0].title()
    
    results.append({
        'source': f'web_search_20260722',
        'source_id': f'ws_{SEQ:04d}',
        'scholarship_name': title,
        'organization': org,
        'description': text[:400],
        'amount_min': amt_min,
        'amount_max': amt_max,
        'amount_display': amt_display,
        'deadline': dl,
        'application_url': url,
        'category': 'Academic',
        'education_level': guess_education(text + ' ' + title),
        'residency': residency,
        'state_restriction': state,
        'citizenship': 'International' if residency != 'USA' else 'US Citizen',
        'status': 'active'
    })
    SEQ += 1

with open('/tmp/candidates_clean.json', 'w') as f:
    json.dump(results, f, indent=2)
print(f'Wrote {len(results)} candidates')
