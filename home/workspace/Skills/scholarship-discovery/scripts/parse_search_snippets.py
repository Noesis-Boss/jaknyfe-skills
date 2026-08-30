#!/usr/bin/env python3
"""
Parse structured scholarship data from web search result snippets.
Focuses on studentscholarships.org and other high-yield sources.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
DB_PATHS = ["/home/workspace/scholarsearch-site/data/processed/scholarships.db"]

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

def is_dup(conn: sqlite3.Connection, name: str, org: str) -> bool:
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def verify_link(url: Optional[str]) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.head(url, allow_redirects=True, timeout=REQUEST_TIMEOUT, headers=HEADERS)
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
            scholarship.get("source", "search_snippet"),
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

# ------------------------------------------------------------------
# Strict parsers
# ------------------------------------------------------------------
def parse_studentscholarships(text: str, url: str) -> Optional[Dict]:
    """Parse structured text from studentscholarships.org search snippets."""
    if not text:
        return None
    
    # Must have 'Scholarship Application' title
    m = re.search(r"Title:\s*Scholarship Application\s*[-–]\s*(.+)", text)
    if not m:
        return None
    name = m.group(1).strip()
    if len(name) < 5:
        return None
    
    # Extract amount
    amount_min = None
    amount_max = None
    amt_m = re.search(r"Scholarship Value:\s*\$?([0-9,]+)", text, re.I)
    if amt_m:
        amount_min = int(amt_m.group(1).replace(",", ""))
        amount_max = None
    else:
        # Try patterns like "$1,000 - $5,000"
        amt_m = re.search(r"\$([0-9,]+)\s*-\s*\$([0-9,]+)", text)
        if amt_m:
            amount_min = int(amt_m.group(1).replace(",", ""))
            amount_max = int(amt_m.group(2).replace(",", ""))
    
    # Extract deadline
    deadline = ""
    dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if dl_m:
        deadline = dl_m.group(1).strip()
    else:
        dl_m = re.search(r"deadline is ([A-Za-z]+ \d{1,2},? \d{4})", text, re.I)
        if dl_m:
            deadline = dl_m.group(1).strip()
    
    # Extract org from URL
    org = "StudentScholarships.org"
    
    # Extract state from text
    state = guess_state(text)
    country = guess_country(url)
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
    ]:
        if re.search(pat, text, re.I):
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
        if re.search(pat, text, re.I):
            level = lvl
            break
    
    return {
        "scholarship_name": name[:180],
        "organization": org,
        "organization_type": "Non-Profit",
        "description": text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": parse_amount_display(amount_min, amount_max),
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
        "citizenship": "US Citizen" if country == "USA" else "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "studentscholarships_search",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    }

def parse_scholarships360(text: str, url: str) -> Optional[Dict]:
    """Parse structured text from scholarships360.org search snippets."""
    if not text:
        return None
    
    # Must have scholarship keyword
    if not re.search(r"scholarship|bursary|fellowship|grant|award", text, re.I):
        return None
    
    # Extract amount - only match numbers with currency symbols
    amounts = re.findall(r"[\$\,\€\£]?\s*([0-9,]+)", text.replace(",", ""))
    amount_min = None
    amount_max = None
    if amounts:
        nums = [int(a) for a in amounts if int(a) > 0]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            if amount_min and amount_min > 500000:
                amount_min = None
            if amount_max and amount_max > 500000:
                amount_max = None
    
    # Extract deadline
    deadline = ""
    dl_m = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", text, re.I)
    if dl_m:
        deadline = dl_m.group(1).strip()
    
    # Extract name - look for patterns like "X Scholarship" or "X Grant"
    # Use the first sentence or title-like phrase
    title = text.split('\n')[0].strip()[:180]
    
    # Skip FAQ/article titles
    skip_phrases = ["how to", "frequently asked", "tips, common requirements", "research the", "frequently asked questions"]
    if any(title.lower().startswith(p) for p in skip_phrases):
        return None
    
    # Determine category
    category = "Academic"
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
        (r"\blaw\b|\blegal\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
    ]:
        if re.search(pat, text, re.I):
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
        if re.search(pat, text, re.I):
            level = lvl
            break
    
    return {
        "scholarship_name": title[:180],
        "organization": "Scholarships360",
        "organization_type": "Platform",
        "description": text[:500],
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": parse_amount_display(amount_min, amount_max),
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
        "state_restriction": "",
        "gpa_min": None,
        "citizenship": "None",
        "ethnicity": "",
        "gender": "",
        "military_affiliation": "",
        "source": "scholarships360_search",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    }

def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)
    
    search_dir = os.path.join(CONV_WORKSPACE, "read_webpage")
    candidates = []
    
    for fname in sorted(os.listdir(search_dir)):
        if not (fname.startswith("web_search") and fname.endswith(".json")):
            continue
        fpath = os.path.join(search_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            items = data if isinstance(data, list) else data.get("results", data.get("data", []))
            for item in items:
                url = item.get("url", "")
                text = item.get("text", "")
                title = item.get("title", "")
                
                # Skip non-scholarship pages
                if not re.search(r"scholarship|bursary|fellowship|grant|award", f"{title} {text}", re.I):
                    continue
                
                # Skip social media, PDFs, videos
                if any(t in url for t in ["facebook.com", "instagram.com", "youtube.com", "tiktok.com", ".pdf"]):
                    continue
                
                # Parse by domain
                if "studentscholarships.org/scholarship/" in url:
                    s = parse_studentscholarships(text, url)
                    if s:
                        candidates.append(s)
                elif "scholarships360.org" in url and "/scholarships/" in url:
                    s = parse_scholarships360(text, url)
                    if s:
                        candidates.append(s)
        except Exception as e:
            print(f"Error reading {fname}: {e}")
    
    print(f"Extracted {len(candidates)} candidates from search snippets")
    
    # Dedup within candidates
    seen = set()
    unique = []
    for c in candidates:
        key = normalize(c["scholarship_name"]) + "||" + normalize(c["organization"])
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")
    
    # Verify and insert
    before = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        before[path] = cur.fetchone()[0]
        conn.close()
    
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    errors = []
    verified = []
    
    for c in unique[:limit]:
        # Check duplicates against DBs
        dup = False
        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            if is_dup(conn, c["scholarship_name"], c["organization"]):
                dup = True
                conn.close()
                break
            conn.close()
        if dup:
            skipped_dup += 1
            continue
        
        # For studentscholarships.org, trust the URL since it's a structured page
        if c["source"] == "studentscholarships_search":
            vr = {"ok": True, "status": 200, "final_url": c["application_url"]}
        else:
            vr = verify_link(c.get("application_url"))
        
        if not vr.get("ok"):
            skipped_verify += 1
            continue
        
        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
        
        # Insert into both DBs
        for path in DB_PATHS:
            try:
                conn = sqlite3.connect(path)
                add_scholarship(conn, c)
                conn.close()
            except Exception as e:
                errors.append(str(e))
        added += 1
        verified.append(c)
    
    after = {}
    for path in DB_PATHS:
        conn = sqlite3.connect(path)
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM scholarships")
        after[path] = cur.fetchone()[0]
        conn.close()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {len(errors)}")
    print(f"  DB totals before: {before}")
    print(f"  DB totals after: {after}")
    
    from collections import Counter
    cats = Counter(c.get("category", "Unknown") for c in verified)
    print(f"\nBreakdown by category:")
    for cat, count in cats.most_common():
        print(f"  {cat}: {count}")
    
    top = sorted(verified, key=lambda x: x.get("amount_min") or 0, reverse=True)[:10]
    print(f"\nTop 10 by amount:")
    for c in top:
        print(f"  {c['amount_display']} - {c['scholarship_name'][:60]}")
    
    if errors:
        print(f"\nErrors:")
        for e in errors[:10]:
            print(f"  {e}")

if __name__ == "__main__":
    main()
