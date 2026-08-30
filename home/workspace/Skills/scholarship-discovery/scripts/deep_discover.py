#!/usr/bin/env python3
"""
Deep scholarship discovery: scrape JS-heavy sources with agent-browser,
verify links, and insert into the scholarships DB.
"""
import subprocess, json, sqlite3, re, time, sys, os
from urllib.parse import urlparse
from datetime import datetime

DB_PATH = "/home/workspace/scholarsearch/data/processed/scholarships.db"
DB_PATH2 = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

def run_browser(url, eval_js=None):
    """Open a URL in agent-browser and optionally run JS to extract data."""
    try:
        if eval_js:
            result = subprocess.run(
                ["agent-browser", "open", url, "--auto-connect"],
                capture_output=True, text=True, timeout=30, cwd="/home/.z/workspaces/con_ElTSTCT8Hr8tlAvw"
            )
            time.sleep(2)
            result = subprocess.run(
                ["agent-browser", "eval", eval_js],
                capture_output=True, text=True, timeout=15, cwd="/home/.z/workspaces/con_ElTSTCT8Hr8tlAvw"
            )
            # Parse JSON output
            out = result.stdout.strip()
            if out.startswith('[') or out.startswith('{'):
                return json.loads(out)
            return out
        else:
            result = subprocess.run(
                ["agent-browser", "open", url, "--auto-connect"],
                capture_output=True, text=True, timeout=30, cwd="/home/.z/workspaces/con_ElTSTCT8Hr8tlAvw"
            )
            return result.stdout
    except Exception as e:
        return f"ERROR: {e}"

def get_existing_names(db):
    """Get set of normalized name hashes from DB."""
    names = set()
    for path in [db]:
        try:
            conn = sqlite3.connect(path)
            cur = conn.cursor()
            for row in cur.execute("SELECT name_hash FROM scholarships WHERE name_hash IS NOT NULL"):
                names.add(row[0])
            conn.close()
        except:
            pass
    return names

def normalize_name(name):
    """Normalize name for duplicate detection."""
    if not name:
        return ""
    n = name.lower().strip()
    n = re.sub(r'[^\w\s]', '', n)
    n = re.sub(r'\s+', ' ', n).strip()
    return n

def hash_name(name):
    import hashlib
    return hashlib.md5(normalize_name(name).encode()).hexdigest()

def is_duplicate(scholarship_name, organization, db_paths, existing_hashes):
    """Check if scholarship is a duplicate."""
    h = hash_name(scholarship_name)
    if h in existing_hashes:
        return True
    for db in db_paths:
        try:
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            # Check by exact name match
            cur.execute("SELECT 1 FROM scholarships WHERE scholarship_name = ? AND (organization = ? OR organization IS NULL)", 
                       (scholarship_name, organization))
            if cur.fetchone():
                conn.close()
                return True
            conn.close()
        except:
            pass
    return False

BOLD_EXTRACT_JS = '''
(() => {
  const data = {};
  // Title
  const titleEl = document.querySelector("h1");
  data.title = titleEl ? titleEl.innerText.trim() : "";
  
  // Funded by / organization
  const fundedBy = Array.from(document.querySelectorAll("p")).find(p => p.innerText.includes("Funded by"));
  data.organization = fundedBy ? fundedBy.innerText.replace("Funded by", "").trim() : "";
  
  // Amount
  const amountEl = Array.from(document.querySelectorAll("p")).find(p => p.innerText.includes("$") || p.innerText.match(/\\$[\d,]+/));
  const amountMatch = amountEl ? amountEl.innerText.match(/\\$[\\d,]+(?:,\\d{3})*(?:\\s*\\(?\\d+\\s*winner.*)?|\\$[\d,]+/) : null;
  data.amount_display = amountEl ? amountEl.innerText.trim() : "";
  
  // Parse amount
  const amounts = data.amount_display.match(/\\$([\\d,]+)/g);
  if (amounts) {
    const nums = amounts.map(a => parseInt(a.replace(/[$,]/g,'')));
    data.amount_min = Math.min(...nums);
    data.amount_max = Math.max(...nums);
  }
  
  // Deadline
  const deadlineEl = Array.from(document.querySelectorAll("p")).find(p => p.innerText.includes("DEADLINE") || p.innerText.match(/(Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|October|November|December|January|February|March|April|May|June|July|August|September)\\s\\d{1,2},\\s\\d{4}/i));
  if (deadlineEl) {
    const dlMatch = deadlineEl.innerText.match(/(Oct|Nov|Dec|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|October|November|December|January|February|March|April|May|June|July|August|September)\\s\\d{1,2},\\s\\d{4}/i);
    data.deadline = dlMatch ? dlMatch[0] : "";
  }
  
  // Status
  const statusEl = Array.from(document.querySelectorAll("p")).find(p => ["OPEN","CLOSED","UPCOMING"].includes(p.innerText.trim()));
  data.status = statusEl ? statusEl.innerText.trim() : "";
  
  // Education Level
  const educationEl = Array.from(document.querySelectorAll("p")).find(p => p.innerText.includes("Education Level"));
  if (educationEl) {
    const next = educationEl.nextElementSibling;
    data.education_level = next ? next.innerText.trim() : "";
  }
  
  // Apply link
  const applyLink = Array.from(document.querySelectorAll("a")).find(a => a.textContent.trim().toLowerCase().includes("apply now"));
  data.application_url = applyLink ? applyLink.href : "";
  
  // Description
  const descEl = document.querySelector("p");
  data.description = descEl ? descEl.innerText.substring(0,500) : "";
  
  return JSON.stringify(data);
})()
'''

def extract_scholarship_detail(url, existing_names_db):
    """Extract scholarship metadata from a bold.org detail page."""
    data_str = run_browser(url, BOLD_EXTRACT_JS)
    if isinstance(data_str, str) and data_str.startswith('{'):
        try:
            data = json.loads(data_str)
        except:
            return None
    elif isinstance(data_str, dict):
        data = data_str
    else:
        return None
    
    title = data.get('title', '').strip()
    if not title:
        return None
    
    if is_duplicate(title, data.get('organization',''), [DB_PATH, DB_PATH2], existing_names_db):
        return None
    
    return {
        'scholarship_name': title,
        'organization': data.get('organization') or "Bold.org",
        'description': data.get('description', ''),
        'amount_min': data.get('amount_min'),
        'amount_max': data.get('amount_max'),
        'amount_display': data.get('amount_display', ''),
        'deadline': data.get('deadline', ''),
        'application_url': data.get('application_url', ''),
        'form_url': data.get('application_url', ''),
        'category': 'Other',
        'education_level': data.get('education_level', ''),
        'citizenship': 'None',
        'state_restriction': 'None',
        'source': 'bold.org',
        'source_id': url.replace('https://bold.org/scholarships/', '').rstrip('/'),
        'url_status': 'unchecked',
        'active': 1,
        'status': data.get('status', '')
    }

def get_bold_listing_urls(page_num):
    """Get scholarship URLs from a bold.org listing page."""
    if page_num == 1:
        url = "https://bold.org/scholarships/"
    else:
        url = f"https://bold.org/scholarships/by-year/high-school/{page_num}/"
    
    js = '''
    (() => {
      const allLinks = Array.from(document.querySelectorAll("a")).map(a => a.href);
      const scholarshipLinks = allLinks.filter(h => 
        h.includes("bold.org/scholarships/") && 
        !h.includes("by-") && 
        !h.includes("/page/") && 
        !h.includes("for-") &&
        h !== "https://bold.org/scholarships/" &&
        h !== "https://bold.org/scholarships/by-year/high-school/" &&
        h.match(/bold\\.org\\/scholarships\\/[a-z0-9-]+\\/$/)
      );
      return [...new Set(scholarshipLinks)];
    })()
    '''
    result = run_browser(url, js)
    if isinstance(result, list) and len(result) > 0:
        return result
    return []

def verify_link(url):
    """Verify application link is reachable."""
    if not url or not url.startswith('http'):
        return 'inactive', ''
    try:
        result = subprocess.run(
            ['curl', '-sL', '-o', '/dev/null', '-w', '%{http_code}', '--max-time', '10', url],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()
        if code in ('200', '301', '302', '307', '308'):
            return 'active', code
        elif code in ('403', '401'):
            return 'active', f'{code}_auth_required'
        else:
            return 'inactive', code
    except:
        return 'inactive', 'timeout'

def insert_scholarship(s, db):
    """Insert scholarship into database."""
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    status, link_code = verify_link(s.get('application_url',''))
    s['url_status'] = status
    s['last_checked'] = datetime.now().isoformat()
    
    cols = [k for k in s.keys()]
    placeholders = ','.join(['?' for _ in cols])
    col_str = ','.join(cols)
    vals = [s[k] for k in cols]
    s['name_hash'] = hash_name(s['scholarship_name'])
    cur.execute(f"INSERT INTO scholarships ({col_str}, name_hash) VALUES ({placeholders}, ?)", vals + [s['name_hash']])
    conn.commit()
    conn.close()
    return s['name_hash']

def main():
    target = 200
    print(f"=== Deep Discovery: target {target} scholarships ===")
    
    # Load existing names for deduplication
    existing_names_db = get_existing_names(DB_PATH)
    print(f"Existing name hashes in DB: {len(existing_names_db)}")
    
    found = []
    
    # === PHASE 1: bold.org paginated scraping ===
    print("\n--- PHASE 1: Scraping bold.org ---")
    for page in range(1, 10):
        if len(found) >= target:
            break
        urls = get_bold_listing_urls(page)
        print(f"  Page {page}: found {len(urls)} scholarship URLs")
        for url in urls[:30]:
            if len(found) >= target:
                break
            s = extract_scholarship_detail(url, existing_names_db)
            if s:
                found.append(s)
                # Add to existing_names to prevent duplicates within this run
                existing_names_db.add(hash_name(s['scholarship_name']))
                print(f"  + {s['scholarship_name'][:50]}... ${s.get('amount_max','?')} dl={s.get('deadline','?')}")
        
    # === PHASE 2: Check existing candidates2.json ===
    print("\n--- PHASE 2: Checking existing candidates ---")
    try:
        candidates = json.load(open('/home/workspace/Skills/scholarship-discovery/scripts/candidates2.json'))
        for c in candidates:
            if len(found) >= target:
                break
            name = c.get('scholarship_name', '')
            if not name:
                continue
            if is_duplicate(name, c.get('organization',''), [DB_PATH, DB_PATH2], existing_names_db):
                continue
            s = {
                'scholarship_name': name,
                'organization': c.get('organization', ''),
                'description': c.get('description', ''),
                'amount_min': c.get('amount_min'),
                'amount_max': c.get('amount_max'),
                'amount_display': c.get('amount_display', ''),
                'deadline': c.get('deadline', ''),
                'application_url': c.get('application_url', ''),
                'form_url': c.get('application_url', ''),
                'category': c.get('category', 'Other'),
                'education_level': c.get('education_level', ''),
                'citizenship': c.get('citizenship', 'None'),
                'state_restriction': c.get('state_restriction', 'None'),
                'source': 'candidates2.json',
                'source_id': name,
                'url_status': 'unchecked',
                'active': 1,
            }
            found.append(s)
            existing_names_db.add(hash_name(s['scholarship_name']))
    except Exception as e:
        print(f"  candidates2.json check: {e}")
    
    # === PHASE 3: Scrape other JS-heavy sources ===
    print("\n--- PHASE 3: Scraping other sources ---")
    # Fastweb (uses JS - need browser)
    # scholarships.com - might be server-rendered
    
    # Try student.com / educationusa state department pages with curl
    # These are often server-rendered
    
    # Try scraping additional bold.org scholarship pages if we still need more
    # Try different category pages
    alt_pages = [
        "https://bold.org/scholarships/by-subject/stem/",
        "https://bold.org/scholarships/by-subject/business/",
        "https://bold.org/scholarships/by-subject/arts-humanities/",
        "https://bold.org/scholarships/by-subject/health-medicine/",
        "https://bold.org/scholarships/by-demographic/ethnic/",
        "https://bold.org/scholarships/by-demographic/women/",
    ]
    for alt_url in alt_pages:
        if len(found) >= target:
            break
        urls = get_bold_listing_urls_alt(alt_url)
        print(f"  {alt_url}: found {len(urls)} scholarship URLs")
        for url in urls[:30]:
            if len(found) >= target:
                break
            s = extract_scholarship_detail(url, existing_names_db)
            if s:
                found.append(s)
                existing_names_db.add(hash_name(s['scholarship_name']))
                print(f"  + {s['scholarship_name'][:50]}... ${s.get('amount_max','?')}")
    
    # === Insert into databases ===
    print(f"\n=== Inserting {len(found)} scholarships ===")
    for i, s in enumerate(found[:target]):
        for db in [DB_PATH, DB_PATH2]:
            try:
                insert_scholarship(dict(s), db)
            except Exception as e:
                print(f"  Insert error for {s['scholarship_name'][:40]}: {e}")
                continue
        if (i+1) % 10 == 0:
            print(f"  Inserted {i+1}/{len(found[:target])}")
    
    # Summary
    for db in [DB_PATH, DB_PATH2]:
        conn = sqlite3.connect(db)
        total = conn.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
        conn.close()
        print(f"  {db}: total scholarships = {total}")
    
    # Save found candidates to JSON
    output_path = "/home/workspace/Skills/scholarship-discovery/scripts/deep_found.json"
    with open(output_path, 'w') as f:
        json.dump(found[:target], f, indent=2)
    print(f"\nSaved candidates to {output_path}")
    print(f"Total found and inserted: {min(len(found), target)}")

def get_bold_listing_urls_alt(url):
    """Get scholarship URLs from any bold.org listing URL."""
    js = '''
    (() => {
      const allLinks = Array.from(document.querySelectorAll("a")).map(a => a.href);
      const scholarshipLinks = allLinks.filter(h => 
        h.includes("bold.org/scholarships/") && 
        h.match(/bold\\.org\\/scholarships\\/[a-z0-9-]+\\/$/) &&
        !h.includes("by-") && 
        !h.includes("/page/") && 
        !h.includes("for-") &&
        h !== "https://bold.org/scholarships/"
      );
      return [...new Set(scholarshipLinks)];
    })()
    '''
    result = run_browser(url, js)
    if isinstance(result, list):
        return result
    return []

if __name__ == "__main__":
    main()
