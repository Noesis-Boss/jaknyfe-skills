#!/usr/bin/env python3
"""
Parse studentscholarships.org listing pages and insert individual scholarships.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 20

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
    m = re.search(r"[\\$\,\\u20ac\\u00a3]?\\s*([0-9,]+)", str(val).replace(",", ""))
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

def is_dup(conn: sqlite3.Connection, scholarship: Dict) -> bool:
    cur = conn.cursor()
    nh = name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", ""))
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
            scholarship.get("source", "parse_student_scholarships"),
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

def extract_from_studentscholarships_page(url: str, html: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    
    # Scholarship name from h1
    h1 = soup.find("h1")
    name = ""
    if h1:
        text = h1.get_text(strip=True)
        # Remove "Scholarship Application - " prefix
        name = re.sub(r"^Scholarship Application\\s*[-–—]?\\s*", "", text)
        name = name.strip()
    
    if not name or len(name) < 5:
        return []
    
    # Organization from title or breadcrumbs
    title = soup.find("title")
    org = ""
    if title:
        title_text = title.get_text(strip=True)
        m = re.search(r"([^|]+?)\\s*[-|]", title_text)
        if m:
            org = m.group(1).strip()
    
    # Amount - look for "Scholarship Value:" or dollar amounts
    amount_min = None
    amount_max = None
    amount_display = "Varies"
    
    # Try "Scholarship Value: $X" pattern
    val_match = re.search(r"Scholarship Value[:\s]+\$?([0-9,]+)", html)
    if val_match:
        amount_min = int(val_match.group(1).replace(",", ""))
        amount_max = amount_min
        amount_display = f"${amount_min:,}"
    else:
        # Look for dollar amounts near the name
        amt_matches = re.findall(r"\\$([0-9,]+)", html)
        if amt_matches:
            nums = [int(a.replace(",", "")) for a in amt_matches if int(a.replace(",", "")) > 0]
            if nums:
                # Filter out dates and large numbers
                nums = [n for n in nums if n < 500000]
                if nums:
                    amount_min = min(nums)
                    amount_max = max(nums) if len(nums) > 1 else None
                    amount_display = parse_amount_display(amount_min, amount_max)
    
    # Deadline
    deadline = ""
    dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\\s]+([A-Za-z]+ \\d{1,2},? \\d{4}|\\d{1,2}/\\d{1,2}/\\d{4}|\\d{4}-\\d{2}-\\d{2})", html, re.I)
    if dl_match:
        deadline = dl_match.group(1)
    
    # Application URL - look for "APPLY NOW" or "Apply" buttons
    app_url = url
    a_tag = soup.find("a", string=re.compile(r"APPLY NOW|Apply Now|Apply", re.I))
    if a_tag and a_tag.get("href"):
        app_url = urljoin(url, a_tag["href"])
    
    # Category guess
    category = "Academic"
    text_lower = html.lower()
    for pat, cat in [
        (r"\\bmasonic\\b", "Masonic"),
        (r"\\bstem\\b|\\bengineering\\b|\\bcomputer\\b|\\bmath\\b|\\bscience\\b", "STEM"),
        (r"\\bmedicine\\b|\\bnursing\\b|\\bhealth\\b", "Healthcare"),
        (r"\\blaw\\b|\\blegal\\b", "Law"),
        (r"\\bbusiness\\b|\\bfinance\\b|\\baccounting\\b", "Business"),
        (r"\\bart\\b|\\bdesign\\b|\\bcreative\\b", "Arts"),
        (r"\\btrade\\b|\\btechnical\\b|\\bvocational\\b", "Trade School"),
    ]:
        if re.search(pat, text_lower):
            category = cat
            break
    
    # Education level guess
    level = "Undergraduate"
    for pat, lvl in [
        (r"\\bhigh school\\b|\\bsecondary\\b", "High School"),
        (r"\\bgraduate\\b|\\bmaster\\b|\\bmba\\b", "Graduate"),
        (r"\\bph\\.?d\\b|\\bdoctorate\\b", "PhD"),
        (r"\\btrade\\b|\\btechnical\\b|\\bvocational\\b", "Trade School"),
        (r"\\bassociate\\b|\\bcommunity college\\b", "Associate"),
    ]:
        if re.search(pat, text_lower):
            level = lvl
            break
    
    # Description from meta or first paragraph
    desc = ""
    meta_desc = soup.find("meta", attrs={"name": "description"})
    if meta_desc:
        desc = meta_desc.get("content", "")[:500]
    if not desc:
        p = soup.find("p")
        if p:
            desc = p.get_text(strip=True)[:500]
    
    return [{
        "scholarship_name": name[:180],
        "organization": org[:180] if org else "StudentsScholarships.org",
        "organization_type": "Unknown",
        "description": desc,
        "eligibility": "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": app_url,
        "form_url": app_url,
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
        "source": "parse_student_scholarships",
        "source_id": hashlib.md5(url.encode()).hexdigest()[:12],
        "link_notes": "",
    }]

def main():
    # Read all scholarship links from the listing page
    conv = CONV_WORKSPACE
    html_files = [f for f in os.listdir(f"{conv}/read_webpage") if 'studentscholarships.org' in f and 'all-scholarships' in f and f.endswith('.html')]
    
    if not html_files:
        print("No studentscholarships.org all-scholarships page found")
        return
    
    with open(f"{conv}/read_webpage/{html_files[0]}", "r", encoding="utf-8", errors="ignore") as fh:
        html = fh.read()
    
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if '/scholarship/' in href and href != '/scholarships':
            full_url = urljoin("https://studentscholarships.org", href)
            if full_url not in links:
                links.append(full_url)
    
    print(f"Found {len(links)} scholarship links on listing page")
    
    # Load existing application URLs to skip
    conn = sqlite3.connect(SITE_DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT application_url FROM scholarships WHERE source = 'parse_student_scholarships'")
    existing_urls = {r[0] for r in cur.fetchall()}
    conn.close()
    
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    errors = 0
    
    for url in links:
        if url in existing_urls:
            skipped_dup += 1
            continue
        
        try:
            resp = requests.get(url, timeout=REQUEST_TIMEOUT, headers=HEADERS)
            if resp.status_code >= 400:
                skipped_verify += 1
                continue
            page_html = resp.text
        except Exception as e:
            errors += 1
            continue
        
        candidates = extract_from_studentscholarships_page(url, page_html)
        
        conn = sqlite3.connect(SITE_DB_PATH)
        for c in candidates:
            if is_dup(conn, c):
                skipped_dup += 1
                continue
            
            vr = verify_link(c.get("application_url"))
            if not vr.get("ok"):
                skipped_verify += 1
                continue
            
            if vr.get("final_url"):
                c["application_url"] = vr["final_url"]
                c["form_url"] = vr["final_url"]
            
            add_scholarship(conn, c)
            added += 1
            print(f"Added: {c['scholarship_name'][:60]} ({c['amount_display']})")
        conn.close()
    
    print(f"\nResults:")
    print(f"  Added: {added}")
    print(f"  Skipped (dup): {skipped_dup}")
    print(f"  Skipped (verify): {skipped_verify}")
    print(f"  Errors: {errors}")

if __name__ == "__main__":
    main()
