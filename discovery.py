import json, glob, re, time, random
from urllib.parse import urlparse
from datetime import datetime

TODAY = datetime.now().strftime('%Y%m%d')
files = sorted(glob.glob('/home/.z/workspaces/con_Xg1QFfyDCEtjEY8u/read_webpage/web_search*.json'))

# Extract meta from search text
AMT = re.compile(r'[\\$\,\\€\\£]\\s*([0-9,]+)')

def extract_amount(text):
    nums = []
    for m in AMT.finditer(text.replace(',', '')):
        n = int(m.group(1))
        if 100 < n < 50000:
            nums.append(n)
    if not nums:
        return None, None, 'Varies'
    amt_min = min(nums)
    amt_max = max(nums) if len(nums) > 1 else None
    if amt_max is None:
        return amt_min, None, f'${amt_min:,}+'
    if amt_min == amt_max:
        return amt_min, None, f'${amt_min:,}'
    return amt_min, amt_max, f'${amt_min:,} - ${amt_max:,}'

def guess_country(url, text=''):
    combined = (url + ' ' + text).lower()
    if any(t in combined for t in ['.gc.ca', 'canada.ca', 'scholarships.ca', 'algomau.ca', 'ucanwest.ca']):
        return 'Canada'
    if any(t in combined for t in ['.ac.uk', 'ucas', 'durham.ac.uk', 'warwick.ac.uk']):
        return 'UK'
    if any(t in combined for t in ['edu.au', 'studyassist', 'scholarships.gov.au']):
        return 'Australia'
    if any(t in combined for t in ['erasmus', 'daad', 'campusfrance', 'studynetherlands', 'sweden', 'studyinsweden', 'si.se']):
        return 'EU'
    if '.edu' in combined:
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

def guess_category(text, title=''):
    combined = (title + ' ' + text).lower()
    if any(t in combined for t in ['stem', 'engineering', 'computer science', 'technology', 'math']):
        return 'STEM'
    if any(t in combined for t in ['medical', 'nursing', 'health', 'medicine', 'premed']):
        return 'Medicine'
    if any(t in combined for t in ['arts', 'humanities', 'film', 'music', 'creative']):
        return 'Arts'
    if any(t in combined for t in ['business', 'mba', 'entrepreneurship', 'management']):
        return 'Business'
    if any(t in combined for t in ['law', 'legal', 'juris']):
        return 'Law'
    if any(t in combined for t in ['masonic', 'freemason']):
        return 'Masonic'
    if any(t in combined for t in ['women', 'female', 'girls']):
        return 'Women'
    if any(t in combined for t in ['hispanic', 'latino', 'latinx']):
        return 'Academic'
    if any(t in combined for t in ['trade', 'vocational', 'technical']):
        return 'Trade School'
    if any(t in combined for t in ['veteran', 'military']):
        return 'Military/Veteran'
    if any(t in combined for t in ['disability', 'disabled']):
        return 'Academic'
    return 'Academic'

def guess_education(text, title=''):
    combined = (title + ' ' + text).lower()
    if any(t in combined for t in ['phd', 'doctorate', 'doctoral']):
        return 'Graduate'
    if any(t in combined for t in ['masters', 'master\'s', 'mba', 'graduate']):
        return 'Graduate'
    if any(t in combined for t in ['undergraduate', 'bachelor', 'freshman', 'sophomore', 'junior', 'senior', 'high school']):
        return 'Undergraduate'
    if any(t in combined for t in ['community college', 'associate']):
        return 'Associate'
    return 'Undergraduate'

def eligible_citizenship(text):
    combined = text.lower()
    if 'international' in combined:
        return 'International'
    if 'permanent resident' in combined or 'green card' in combined:
        return 'Permanent Resident'
    if 'us citizen' in combined or 'u.s. citizen' in combined:
        return 'US Citizen'
    return 'None'

cands = []
seen = set()
seq = 0

for f in files:
    with open(f) as fh:
        data = json.load(fh)
    for r in data:
        url = r['url']
        title = r['title']
        text = r.get('text', '')
        domain = urlparse(url).netloc.lower()
        if not url or url in seen:
            continue
        seen.add(url)
        
        # Skip listing/homepage URLs
        if any(domain.endswith(x) for x in ['fastweb.com', 'scholarships360.org', 'collegeboard.org', 'study.com', 'scholarships.com']):
            continue
        # Skip non-scholarship pages
        if any(kw in domain for kw in ['youtube.com', 'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com', 'reddit.com']):
            continue
        if title.lower() in ['make uk: the manufacturers\' organisation', 'uk parliament']:
            continue
        if len(title) < 5:
            continue
            
        amt_min, amt_max, amt_display = extract_amount(text)
        deadline = ''
        m = re.search(r'(?:deadline|due date|closing|apply by|due)[:\\s]+([A-Za-z]+ \\d{1,2},? \\d{4}|\\d{1,2}/\\d{1,2}/\\d{4}|\\d{4}-\\d{2}-\\d{2})', text, re.I)
        if not m:
            m = re.search(r'([A-Za-z]+ \\d{1,2},? \\d{4})', text)
        if m:
            deadline = m.group(1)
        
        cands.append({
            'source': f'web_search_{TODAY}',
            'source_id': f'ws_{TODAY}_{seq:04d}',
            'scholarship_name': title,
            'organization': urlparse(url).netloc.replace('www.', '').split('.')[0].title(),
            'description': text[:300],
            'amount_min': amt_min,
            'amount_max': amt_max,
            'amount_display': amt_display,
            'deadline': deadline,
            'application_url': url,
            'category': guess_category(text, title),
            'education_level': guess_education(text, title),
            'field_of_study': '',
            'state_restriction': guess_state(text),
            'citizenship': eligible_citizenship(text),
            'residency': guess_country(url, text),
            'status': 'active'
        })
        seq += 1

with open('/tmp/candidates.json', 'w') as f:
    json.dump(cands, f, indent=2)
print(f'Total candidates: {len(cands)}')
print(json.dumps(cands[0], indent=2))
