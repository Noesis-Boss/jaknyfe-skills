#!/usr/bin/env python3
"""
Read saved scholarship listing pages, extract individual scholarships,
verify links, dedup, and insert into DBs.
"""
import os, sys, json, re, sqlite3, hashlib, time, random
from datetime import datetime, timezone
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/1.0)"}
REQUEST_TIMEOUT = 20

CONV_WORKSPACE = "/home/.z/workspaces/con_3iAHN4wWm8rptujP"
PAGE_DIR = os.path.join(CONV_WORKSPACE, "read_webpage")

# ------------------------------------------------------------------
# Helpers
# ------------------------------------------------------------------
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

def guess_country(url: str, text: str = "") -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".edu/uk", ".ac.uk", "ucas", "scholarships.org.uk", "uk.scholarships"]):
        return "UK"
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "canadian"]):
        return "Canada"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "australia"]):
        return "Australia"
    if any(t in combined for t in [".edu", ".gov", "us", "united states", "american"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "tennessee": "TN", "missouri": "MO", "wisconsin": "WI", "minnesota": "MN",
        "new jersey": "NJ", "maryland": "MD", "indiana": "IN", "ohio": "OH",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

# ------------------------------------------------------------------
# Extraction from listing pages
# ------------------------------------------------------------------
def extract_from_scholarships360(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if not text or len(text) < 8 or "scholarship" not in text.lower():
            continue
        # Find nearby link
        link = None
        parent = tag.find_parent()
        if parent:
            a = parent.find("a", href=True)
            if a:
                link = urljoin(base_url, a["href"])
        if not link:
            nxt = tag.find_next_sibling()
            if nxt:
                a = nxt.find("a", href=True)
                if a:
                    link = urljoin(base_url, a["href"])
        # Get surrounding text for amount/deadline
        parent_text = ""
        if tag.parent:
            parent_text = tag.parent.get_text(" ", strip=True)
        amt_match = re.search(r"\$[\d,]+(?:\s*-\s*\$[\d,]+)?", parent_text)
        amount_display = amt_match.group(0) if amt_match else "Varies"
        deadline = ""
        dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", parent_text, re.I)
        if dl_match:
            deadline = dl_match.group(1)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Scholarships360",
            "description": parent_text[:500],
            "amount_display": amount_display,
            "deadline": deadline,
            "application_url": link or base_url,
            "form_url": link or base_url,
            "website": base_url,
            "category": "Academic",
            "education_level": "Undergraduate",
            "source": "scholarships360",
        })
    return candidates

def extract_from_bold(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if not text or len(text) < 8 or "scholarship" not in text.lower():
            continue
        link = None
        parent = tag.find_parent()
        if parent:
            a = parent.find("a", href=True)
            if a:
                link = urljoin(base_url, a["href"])
        if not link:
            nxt = tag.find_next_sibling()
            if nxt:
                a = nxt.find("a", href=True)
                if a:
                    link = urljoin(base_url, a["href"])
        parent_text = tag.parent.get_text(" ", strip=True) if tag.parent else ""
        amt_match = re.search(r"\$[\d,]+(?:\s*-\s*\$[\d,]+)?", parent_text)
        amount_display = amt_match.group(0) if amt_match else "Varies"
        deadline = ""
        dl_match = re.search(r"(?:deadline|due|closing|apply by)[:\s]+([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})", parent_text, re.I)
        if dl_match:
            deadline = dl_match.group(1)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Bold.org",
            "description": parent_text[:500],
            "amount_display": amount_display,
            "deadline": deadline,
            "application_url": link or base_url,
            "form_url": link or base_url,
            "website": base_url,
            "category": "Academic",
            "education_level": "Undergraduate",
            "source": "bold.org",
        })
    return candidates

def extract_from_studentscholarships_search(html: str, base_url: str) -> List[Dict]:
    """Extract individual scholarship pages from search results."""
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all("a", href=True):
        href = a["href"]
        text = a.get_text(strip=True)
        if "/scholarship/" in href and len(text) > 10:
            # This is likely an individual scholarship link
            full_url = urljoin(base_url, href)
            candidates.append({
                "scholarship_name": text[:180],
                "organization": "StudentScholarships.org",
                "description": "",
                "amount_display": "Varies",
                "deadline": "",
                "application_url": full_url,
                "form_url": full_url,
                "website": full_url,
                "category": "Academic",
                "education_level": "Undergraduate",
                "source": "studentscholarships_search",
            })
    return candidates

def extract_from_scholarshipscom(html: str, base_url: str) -> List[Dict]:
    candidates = []
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup.find_all(["h2", "h3", "h4"]):
        text = tag.get_text(strip=True)
        if not text or len(text) < 8 or "scholarship" not in text.lower():
            continue
        link = None
        parent = tag.find_parent()
        if parent:
            a = parent.find("a", href=True)
            if a:
                link = urljoin(base_url, a["href"])
        if not link:
            nxt = tag.find_next_sibling()
            if nxt:
                a = nxt.find("a", href=True)
                if a:
                    link = urljoin(base_url, a["href"])
        parent_text = tag.parent.get_text(" ", strip=True) if tag.parent else ""
        amt_match = re.search(r"\$[\d,]+(?:\s*-\s*\$[\d,]+)?", parent_text)
        amount_display = amt_match.group(0) if amt_match else "Varies"
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Scholarships.com",
            "description": parent_text[:500],
            "amount_display": amount_display,
            "deadline": "",
            "application_url": link or base_url,
            "form_url": link or base_url,
            "website": base_url,
            "category": "Academic",
            "education_level": "Undergraduate",
            "source": "scholarships.com",
        })
    return candidates

# ------------------------------------------------------------------
# DB operations
# ------------------------------------------------------------------
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
        # Check if page looks like an application form
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" in content_type:
            if "application" in resp.text.lower() or "scholarship" in resp.text.lower() or "form" in resp.text.lower():
                return {"ok": True, "status": resp.status_code, "final_url": final_url}
            else:
                return {"ok": False, "reason": "no_application_content", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

def add_scholarship(conn: sqlite3.Connection, scholarship: Dict) -> int:
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO scholarships (
            source, source_id, scholarship_name, organization, organization_type,
            description, eligibility, amount_min, amount_max, amount_display,
            deadline, application_url, form_url, email, phone, address, website,
            category, education_level, field_of_study, state_restriction,
            gpa_min, citizenship, ethnicity, gender, military_affiliation,
            name_hash, created_at, updated_at, link_notes
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    """, (
        scholarship.get("source", "page_discovery"),
        scholarship.get("source_id", hashlib.md5(scholarship.get("scholarship_name", "").encode()).hexdigest()[:12]),
        scholarship.get("scholarship_name"),
        scholarship.get("organization"),
        scholarship.get("organization_type", "Unknown"),
        scholarship.get("description", ""),
        scholarship.get("eligibility", ""),
        scholarship.get("amount_min"),
        scholarship.get("amount_max"),
        scholarship.get("amount_display", "Varies"),
        scholarship.get("deadline", ""),
        scholarship.get("application_url"),
        scholarship.get("form_url"),
        scholarship.get("email", ""),
        scholarship.get("phone", ""),
        scholarship.get("address", ""),
        scholarship.get("website"),
        scholarship.get("category", "Academic"),
        scholarship.get("education_level", "Undergraduate"),
        scholarship.get("field_of_study", ""),
        scholarship.get("state_restriction", ""),
        scholarship.get("gpa_min"),
        scholarship.get("citizenship", "None"),
        scholarship.get("ethnicity", ""),
        scholarship.get("gender", ""),
        scholarship.get("military_affiliation", ""),
        name_hash(scholarship.get("scholarship_name", ""), scholarship.get("organization", "")),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
        scholarship.get("link_notes", ""),
    ))
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

# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    limit = 200
    for arg in sys.argv[1:]:
        if arg.isdigit():
            limit = int(arg)

    # Load saved pages
    page_files = []
    for f in os.listdir(PAGE_DIR):
        if f.endswith(".html") and ("scholarships360" in f or "bold.org" in f or "scholarships.com" in f or "studentscholarships" in f):
            page_files.append(os.path.join(PAGE_DIR, f))
    print(f"Found {len(page_files)} relevant page files")

    all_candidates = []
    for pf in page_files:
        try:
            with open(pf, "r", encoding="utf-8", errors="ignore") as fh:
                html = fh.read()
            base_url = "https://" + pf.split("~~")[-1].replace("~~2f", "/").replace("~~2e", ".")
            if "scholarships360.org" in pf:
                all_candidates.extend(extract_from_scholarships360(html, base_url))
            elif "bold.org" in pf:
                all_candidates.extend(extract_from_bold(html, base_url))
            elif "scholarships.com" in pf:
                all_candidates.extend(extract_from_scholarshipscom(html, base_url))
            elif "studentscholarships" in pf and "scholarships/" in pf:
                all_candidates.extend(extract_from_studentscholarships_search(html, base_url))
        except Exception as e:
            print(f"Error parsing {pf}: {e}")

    print(f"Extracted {len(all_candidates)} candidates from pages")

    # Dedup within candidates
    seen = set()
    unique = []
    for c in all_candidates:
        key = normalize(c["scholarship_name"]) + "||" + normalize(c.get("organization", ""))
        if key not in seen:
            seen.add(key)
            unique.append(c)
    print(f"After internal dedup: {len(unique)} unique candidates")

    before = stats()
    added = 0
    skipped_dup = 0
    skipped_verify = 0
    verified = []
    errors = []

    for c in unique[:limit]:
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

        app_url = c.get("application_url")
        if app_url:
            vr = verify_link(app_url)
            if not vr.get("ok"):
                skipped_verify += 1
                c["link_notes"] = vr.get("reason", "link_failed")
                if vr.get("final_url"):
                    c["application_url"] = vr["final_url"]
                    c["form_url"] = vr["final_url"]
                    c["website"] = vr["final_url"]
                continue

        if vr.get("final_url"):
            c["application_url"] = vr["final_url"]
            c["form_url"] = vr["final_url"]
            c["website"] = vr["final_url"]

        # Parse amount_min/amount_max
        amt_str = c.get("amount_display", "Varies")
        amt_min = amt_max = None
        if amt_str.startswith("$"):
            nums = re.findall(r"[\d,]+", amt_str)
            if nums:
                amt_min = int(nums[0].replace(",", ""))
                if len(nums) > 1:
                    amt_max = int(nums[1].replace(",", ""))
                else:
                    amt_max = amt_min
        c["amount_min"] = amt_min
        c["amount_max"] = amt_max

        # Guess category from name
        for pat, cat in [
            (r"\bmasonic\b", "Masonic"),
            (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
            (r"\bmedicine\b|\bnursing\b|\bhealth\b", "Healthcare"),
            (r"\blaw\b|\blegal\b", "Law"),
            (r"\bbusiness\b|\bfinance\b|\baccounting\b", "Business"),
            (r"\bart\b|\bdesign\b|\bcreative\b", "Arts"),
            (r"\bwomen\b|\bfemale\b", "Women"),
            (r"\bveteran\b|\bmilitary\b", "Military/Veteran"),
            (r"\bhispanic\b|\blatino\b|\blatina\b", "Hispanic"),
            (r"\bblack\b|\bafrican\b", "Black"),
            (r"\blgbtq\b|\bqueer\b|\btrans\b|\bnon-binary\b", "LGBTQ"),
            (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
            (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
            (r"\binternational\b", "International"),
        ]:
            if re.search(pat, c["scholarship_name"] + " " + c.get("description", ""), re.I):
                c["category"] = cat
                break

        for path in DB_PATHS:
            conn = sqlite3.connect(path)
            add_scholarship(conn, c)
            conn.close()
        added += 1
        verified.append(c)

    after = stats()
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

if __name__ == "__main__":
    main()
