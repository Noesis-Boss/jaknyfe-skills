#!/usr/bin/env python3
"""
Parse saved webpages and extract scholarships.
Reads all files from conversation workspace read_webpage directory,
extracts scholarship data, verifies links, and inserts into DBs.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
from urllib.parse import urljoin

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("BeautifulSoup not available, install it")
    sys.exit(1)

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
SEARCH_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 15

def normalize(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name: str, org: str) -> str:
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def clean_num(val: Optional[str]) -> Optional[int]:
    if not val:
        return None
    m = re.search(r"[\$\,\€\£]?\s*([0-9,]+)", str(val).replace(",", ""))
    return int(m.group(1)) if m else None

def parse_amount_display(amount_min: Optional[int], amount_max: Optional[int]) -> str:
    if amount_min and amount_max:
        if amount_min == amount_max:
            return f"${amount_min:,}"
        return f"${amount_min:,} - ${amount_max:,}"
    if amount_min:
        return f"${amount_min:,}+"
    if amount_max:
        return f"Up to ${amount_max:,}"
    return "Varies"

def guess_country(url: str) -> str:
    if ".edu" in url or ".gov" in url:
        if any(t in url for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk"]):
            return "UK"
        if any(t in url for t in [".gc.ca", "canada.ca", "scholarships.ca"]):
            return "Canada"
        if any(t in url for t in ["edu.au", "studyassist", "scholarships.gov.au"]):
            return "Australia"
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def verify_link(url: Optional[str]) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.get(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

def add_scholarship(conn: sqlite3.Connection, scholarship: Dict) -> int:
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, created_at, updated_at, link_notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (
            scholarship.get("source", "parse_discovery"),
            scholarship.get("source_id"),
            scholarship.get("scholarship_name"),
            scholarship.get("organization"),
            scholarship.get("organization_type"),
            scholarship.get("description"),
            scholarship.get("eligibility"),
            scholarship.get("amount_min"),
            scholarship.get("amount_max"),
            scholarship.get("amount_display"),
            scholarship.get("deadline"),
            scholarship.get("application_url"),
            scholarship.get("form_url"),
            scholarship.get("email"),
            scholarship.get("phone"),
            scholarship.get("address"),
            scholarship.get("website"),
            scholarship.get("category"),
            scholarship.get("education_level"),
            scholarship.get("field_of_study"),
            scholarship.get("state_restriction"),
            scholarship.get("gpa_min"),
            scholarship.get("citizenship"),
            scholarship.get("ethnicity"),
            scholarship.get("gender"),
            scholarship.get("military_affiliation"),
            name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", "")),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
            scholarship.get("link_notes"),
        ),
    )
    conn.commit()
    return cur.lastrowid

def stats():
    out = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        out[path] = cur.fetchone()[0]
        conn.close()
    return out

def extract_from_studentscholarships_md(md_text: str, url: str) -> Optional[Dict]:
    """Extract scholarship data from studentscholarships.org markdown."""
    # Extract scholarship name from title
    title_m = re.search(r"^#\s+Scholarship Application[:\s]+(.+)$", md_text, re.M)
    if not title_m:
        return None
    name = title_m.group(1).strip()[:180]
    if len(name) < 5:
        return None
    
    # Extract value/amount
    amount_display = "Varies"
    amount_min = None
    amount_max = None
    val_m = re.search(r"Scholarship Value[:\s]*\$?([0-9,]+)", md_text, re.I)
    if val_m:
        amount_min = int(val_m.group(1).replace(",", ""))
        amount_max = amount_min
        amount_display = f"${amount_min:,}"
    
    # Extract deadline
    deadline = ""
    dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", md_text, re.I)
    if dl_m:
        deadline = dl_m.group(1)
    
    # Extract organization from page content
    org = "Unknown"
    org_m = re.search(r"(?:provided by|offered by|sponsored by|awarded by|from)\s+([A-Z][A-Za-z\s&]+?)(?:\s+scholarship|\s+program|\s+fund|\s+foundation|\s+trust|\s+society)", md_text, re.I)
    if org_m:
        org = org_m.group(1).strip()[:100]
    
    # Extract state from URL or text
    state = guess_state(md_text)
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bmilitary\b|\bveteran\b", "Military/Veteran"),
        (r"\bhispanic\b|\blatino\b|\blatina\b", "Hispanic/Latino"),
        (r"\bblack\b|\bafrican\b", "Black/African American"),
        (r"\blgbtq\b|\bqueer\b|\btransgender\b", "LGBTQ"),
    ]:
        if re.search(pat, name + " " + md_text[:1000], re.I):
            category = cat
            break
    
    # Determine education level
    level = "Undergraduate"
    for pat, lvl in [
        (r"\bhigh school\b|\bsecondary\b", "High School"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
    ]:
        if re.search(pat, name + " " + md_text[:1000], re.I):
            level = lvl
            break
    
    return {
        "scholarship_name": name,
        "organization": org,
        "organization_type": "Unknown",
        "description": md_text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": url,
        "form_url": url,
        "email": "",
        "phone": "",
        "address": "",
        "website": url,
        "category": category,
        "education_level": level,
        "field_of_study": "",
        "state_restriction": state or "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "parse_discovery",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    }

def extract_from_bold_md(md_text: str, url: str) -> Optional[Dict]:
    """Extract scholarship data from bold.org listing pages."""
    # Bold.org listing pages have structured scholarship cards
    # We need to find actual scholarship names and amounts
    candidates = []
    
    # Look for scholarship names in the page
    # Bold.org pages have scholarship names in headings or specific sections
    lines = md_text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or len(line) < 10:
            continue
        
        # Check if this looks like a scholarship entry
        if re.search(r"scholarship", line, re.I) and not re.search(r"page|website|home|login|sign", line, re.I):
            # Look for amount in nearby lines
            amount_display = "Varies"
            amount_min = None
            amount_max = None
            
            # Check next few lines for amount
            for j in range(i, min(i+5, len(lines))):
                amt_m = re.search(r"\$[\d,]+(?:\.\d+)?", lines[j])
                if amt_m:
                    amount_str = amt_m.group(0).replace('$', '').replace(',', '')
                    try:
                        amount_min = int(amount_str)
                        amount_max = amount_min
                        amount_display = f"${amount_min:,}"
                    except ValueError:
                        pass
                    break
            
            # Look for deadline
            deadline = ""
            for j in range(i, min(i+10, len(lines))):
                dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4})", lines[j], re.I)
                if dl_m:
                    deadline = dl_m.group(1)
                    break
            
            # Only add if it has substantial text
            if len(line) > 10 and len(line) < 200:
                candidates.append({
                    "scholarship_name": line[:180],
                    "organization": "Bold.org",
                    "amount_display": amount_display,
                    "amount_min": amount_min,
                    "amount_max": amount_max,
                    "deadline": deadline,
                    "url": url,
                })
    
    return candidates[0] if candidates else None

def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    # Load all saved webpage files
    files = []
    for f in os.listdir(SEARCH_DIR):
        if f.endswith('.md') or f.endswith('.html'):
            files.append(os.path.join(SEARCH_DIR, f))
    
    print(f"Found {len(files)} webpage files")
    
    candidates = []
    for filepath in files:
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                content = fh.read()
            
            # Determine URL from filename
            filename = os.path.basename(filepath)
            # Convert encoded filename back to URL
            url = filename.replace("~~2f", "/").replace("~~3a", ":")
            if url.endswith('.md'):
                url = url[:-3]
            elif url.endswith('.html'):
                url = url[:-5]
            url = "https://" + url
            
            # Try studentscholarships.org parser first
            if "studentscholarships.org" in url:
                s = extract_from_studentscholarships_md(content, url)
                if s:
                    candidates.append(s)
            # Try bold.org parser
            elif "bold.org" in url:
                s = extract_from_bold_md(content, url)
                if s:
                    candidates.append(s)
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
    
    print(f"Extracted {len(candidates)} candidates from pages")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in candidates:
        key = normalize(c.get("scholarship_name", "")) + "||" + normalize(c.get("organization", ""))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")
    
    # Verify and insert
    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    errors = 0
    verified = []
    
    for c in unique[:limit]:
        # Check duplicates against DBs
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            if is_dup(conn, c):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # Verify link
        vr = verify_link(c.get("application_url"))
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        # Update final URL if redirected
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
        
        # Insert into DBs
        try:
            for path in DB_PATHS:
                conn = sqlite3.connect(path)
                add_scholarship(conn, c)
                conn.close()
            added += 1
            verified.append(c)
        except Exception as e:
            errors += 1
    
    after = stats()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {errors}")
    print(f"  DB totals before: {before}")
    print(f"  DB totals after: {after}")
    
    # Print breakdown by category
    from collections import Counter
    cats = Counter(c.get("category", "Unknown") for c in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
    
    # Print top 10 by amount
    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for c in top:
        print(f"  {c.get('amount_display', 'Varies')} - {c.get('scholarship_name', 'Unknown')[:60]}")

if __name__ == "__main__":
    main()
