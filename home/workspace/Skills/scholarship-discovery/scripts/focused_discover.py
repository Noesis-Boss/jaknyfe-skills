#!/usr/bin/env python3
"""
Focused scholarship discovery for underrepresented regions and categories.
Targets: Canada, UK, EU, Australia, NZ, Graduate, PhD, Trade School, Professional.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, urllib.parse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup

DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]
OUTPUT_PATH = "/home/workspace/Skills/scholarship-discovery/scripts/new_scholarships.json"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0; +https://jaknyfe.zo.space)"}
REQUEST_TIMEOUT = 20
JITTER = (0.3, 0.8)


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
    m = re.search(r"[\$\,\€\£]\s*([0-9,]+)", str(val).replace(",", ""))
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


def get_db_connection(path: str):
    return sqlite3.connect(path)


def is_dup(conn: sqlite3.Connection, name: str, org: str) -> bool:
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None


def verify_link(url: Optional[str], timeout: int = REQUEST_TIMEOUT) -> Dict:
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        resp = requests.get(url, allow_redirects=True, timeout=timeout, headers=HEADERS)
        final_url = resp.url
        if resp.status_code >= 400:
            return {"ok": False, "reason": f"http_{resp.status_code}", "final_url": final_url}
        text = resp.text.lower()
        has_scholarship = any(k in text for k in ["scholarship", "bursary", "fellowship", "grant", "award", "financial aid"])
        if not has_scholarship:
            return {"ok": False, "reason": "not_scholarship_page", "final_url": final_url}
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}


def guess_country(url: str, text: str = "") -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "mcgill", "ubc", "university of toronto"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge", "imperial", "edinburgh"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in combined for t in ["studylink", "nz gov", "university of auckland"]):
        return "New Zealand"
    if any(t in combined for t in ["erasmus", "daad", "campusfrance", "studynetherlands", "ethz", "europa.eu"]):
        return "EU"
    return "USA"


def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "new jersey": "NJ", "maryland": "MD", "minnesota": "MN", "missouri": "MO",
        "wisconsin": "WI", "tennessee": "TN", "indiana": "IN", "alabama": "AL",
        "south carolina": "SC", "kentucky": "KY", "louisiana": "LA", "oklahoma": "OK",
        "connecticut": "CT", "iowa": "IA", "kansas": "KS", "arkansas": "AR",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None


def categorize(name: str, org: str, raw_text: str, url: str = "") -> str:
    text = f"{name} {org} {raw_text} {url}".lower()
    if re.search(r"\bmasonic\b", text):
        return "Masonic"
    if re.search(r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", text):
        return "STEM"
    if re.search(r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", text):
        return "Medicine"
    if re.search(r"\blaw\b|\blegal\b|\battorney\b", text):
        return "Law"
    if re.search(r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", text):
        return "Business"
    if re.search(r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", text):
        return "Arts"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", text):
        return "Trade School"
    if re.search(r"\bwomen\b|\bfemale\b", text):
        return "Women"
    if re.search(r"\bveteran\b|\bmilitary\b|\barmed forces\b", text):
        return "Military/Veteran"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", text):
        return "Graduate"
    if re.search(r"\bcommunity\b|\bvolunteer\b|\bservice\b", text):
        return "Community"
    if re.search(r"\bsocial science\b|\bpolitical\b|\bsociology\b|\bpsychology\b", text):
        return "Social Science"
    return "Academic"


def tag_level(name: str, raw_text: str) -> str:
    text = f"{name} {raw_text}".lower()
    if re.search(r"\bph\.?d\b|\bdoctorate\b", text):
        return "PhD"
    if re.search(r"\bgraduate\b|\bmaster\b|\bmba\b", text):
        return "Graduate"
    if re.search(r"\btrade\b|\btechnical\b|\bvocational\b", text):
        return "Trade School"
    if re.search(r"\bassociate\b|\bcommunity college\b", text):
        return "Associate"
    if re.search(r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", text):
        return "Professional"
    if re.search(r"\bhigh school\b|\bsecondary\b", text):
        return "High School"
    return "Undergraduate"


def fetch(url: str, timeout: int = REQUEST_TIMEOUT) -> Optional[str]:
    for attempt in range(2):
        try:
            r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
            if r.status_code == 200:
                return r.text
            if r.status_code in (403, 404, 410):
                return None
        except requests.RequestException:
            pass
        time.sleep(1)
    return None


def extract_detail_from_page(html: str, url: str) -> Dict:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(" ", strip=True)
    title = soup.title.string.strip() if soup.title else ""
    combined = f"{title} {text}"

    amount_min, amount_max, amount_display = None, None, "Varies"
    amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", combined.replace(",", ""))
    if amounts:
        nums = [int(a) for a in amounts if 10 < int(a) < 500000]
        if nums:
            amount_min = min(nums)
            amount_max = max(nums) if len(nums) > 1 else None
            amount_display = parse_amount_display(amount_min, amount_max)

    deadline = ""
    dl_match = re.search(
        r"(?:deadline|due date|closing date|apply by|applications due)[:\s]+"
        r"([A-Za-z]+ \d{1,2},? \d{4}|\d{1,2}/\d{1,2}/\d{4}|\d{4}-\d{2}-\d{2})",
        combined, re.I,
    )
    if dl_match:
        deadline = dl_match.group(1)

    org = ""
    org_m = re.search(r"(?:offered by|provided by|sponsored by|from)\s+([A-Z][A-Za-z\s&]+?)(?:\s*[.,]|$)", combined)
    if org_m:
        org = org_m.group(1).strip()[:100]
    if not org:
        domain = re.search(r"https?://(?:www\.)?([^/]+)", url)
        if domain:
            org = domain.group(1).split(".")[0].replace("-", " ").title()

    return {
        "scholarship_name": title[:180] if title else "",
        "organization": org[:100] if org else "",
        "amount_min": amount_min,
        "amount_max": amount_max,
        "amount_display": amount_display,
        "deadline": deadline,
        "raw_text": combined[:2000],
    }


# ------------------------------------------------------------------
# Source-specific extractors
# ------------------------------------------------------------------
def extract_bold_scholarships(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarships/[a-z0-9-]+/?$")):
        href = urllib.parse.urljoin(base_url, a.get("href", ""))
        if re.match(r"/scholarships/(by-|high-school|undergraduate|graduate|demographics|other|type|major|year|state)", href):
            continue
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "Bold.org",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates


def extract_studentscholarships(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    for a in soup.find_all("a", href=re.compile(r"/scholarship/\d+/")):
        href = urllib.parse.urljoin(base_url, a.get("href", ""))
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "tr", "article"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": "StudentScholarships.org",
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates


def extract_scholarships360(html: str, base_url: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\n", strip=True)
    candidates = []
    pattern = re.compile(r"\$([0-9,]+).*?(?:Scholarship|Grant|Award)", re.I)
    for m in pattern.finditer(text):
        context_start = max(0, m.start() - 100)
        context_end = min(len(text), m.end() + 100)
        context = text[context_start:context_end]
        amounts = re.findall(r"[\$\,\€\£]\s*([0-9,]+)", context.replace(",", ""))
        amount_min = None
        amount_max = None
        if amounts:
            nums = [int(a) for a in amounts if 10 < int(a) < 500000]
            if nums:
                amount_min = min(nums)
                amount_max = max(nums) if len(nums) > 1 else None
        name_m = re.search(r"([A-Za-z][A-Za-z0-9 &'\-\.]{10,}?)\s*\$", context)
        name = name_m.group(1).strip() if name_m else "Scholarship"
        if len(name) > 180:
            name = name[:180]
        candidates.append({
            "scholarship_name": name,
            "organization": "Scholarships360",
            "application_url": base_url,
            "amount_display": parse_amount_display(amount_min, amount_max),
            "deadline": "",
            "raw_text": context,
        })
    return candidates


def extract_generic(html: str, base_url: str, domain: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    patterns = [
        re.compile(r"/scholarship/", re.I),
        re.compile(r"/grant/", re.I),
        re.compile(r"/fellowship/", re.I),
        re.compile(r"/award/", re.I),
        re.compile(r"/financial-aid/", re.I),
    ]
    for a in soup.find_all("a", href=True):
        href = urllib.parse.urljoin(base_url, a.get("href", ""))
        if not any(p.search(href) for p in patterns):
            continue
        text = a.get_text(" ", strip=True)
        key = normalize(text)
        if not key or key in seen or len(key) < 10:
            continue
        if not re.search(r"scholarship|bursary|fellowship|grant|award|financial aid", text, re.I):
            continue
        seen.add(key)
        parent = a.find_parent(["div", "li", "article", "tr"]) or a
        parent_text = parent.get_text(" ", strip=True)
        candidates.append({
            "scholarship_name": text[:180],
            "organization": domain,
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates


# ------------------------------------------------------------------
# Deep verification: visit individual scholarship pages
# ------------------------------------------------------------------
def enrich_scholarship(url: str) -> Optional[Dict]:
    html = fetch(url)
    if not html:
        return None
    detail = extract_detail_from_page(html, url)
    if not detail.get("scholarship_name"):
        return None

    # Find application link on the page
    soup = BeautifulSoup(html, "html.parser")
    app_link = None
    for a in soup.find_all("a", href=True):
        text = a.get_text(" ", strip=True).lower()
        href = a.get("href", "")
        if any(k in text for k in ["apply now", "apply", "application", "submit", "start application"]):
            if href.startswith("http"):
                app_link = href
            else:
                app_link = urllib.parse.urljoin(url, href)
            break

    detail["application_url"] = app_link or url
    detail["website"] = url
    return detail


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------
def main():
    sources = [
        # Bold.org category pages
        ("bold_org_hs", "https://bold.org/scholarships/high-school/", extract_bold_scholarships),
        ("bold_org_undergrad", "https://bold.org/scholarships/undergraduate-scholarships/", extract_bold_scholarships),
        ("bold_org_grad", "https://bold.org/scholarships/scholarships-for-graduate-students-list/", extract_bold_scholarships),
        ("bold_org_demo", "https://bold.org/scholarships/by-demographics/", extract_bold_scholarships),
        ("bold_org_type", "https://bold.org/scholarships/by-type/", extract_bold_scholarships),
        ("bold_org_major", "https://bold.org/scholarships/by-major/", extract_bold_scholarships),
        # StudentScholarships
        ("studentscholarships_org", "https://studentscholarships.org/scholarships/", extract_studentscholarships),
        # Scholarships360
        ("scholarships360_org", "https://scholarships360.org", extract_scholarships360),
        # AccessScholarships
        ("accessscholarships_com", "https://accessscholarships.com", lambda h, b: extract_generic(h, b, "AccessScholarships.com")),
        # Fastweb
        ("fastweb_com", "https://www.fastweb.com/college-scholarships", lambda h, b: extract_generic(h, b, "Fastweb")),
        # US Government
        ("studentaid_gov", "https://studentaid.gov/understand-aid/types/scholarships", lambda h, b: extract_generic(h, b, "StudentAid.gov")),
        ("benefits_gov", "https://www.benefits.gov/", lambda h, b: extract_generic(h, b, "Benefits.gov")),
        # International
        ("erasmus_mundus", "https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue", lambda h, b: extract_generic(h, b, "Erasmus Mundus")),
        ("daad", "https://www.daad.de/en/study-and-research-in-germany/scholarships/", lambda h, b: extract_generic(h, b, "DAAD")),
        ("campusfrance", "https://www.campusfrance.org/en/ scholarships", lambda h, b: extract_generic(h, b, "CampusFrance")),
        ("studyassist_au", "https://www.studyassist.gov.au/scholarships", lambda h, b: extract_generic(h, b, "StudyAssist")),
        ("studylink_nz", "https://www.studylink.govt.nz/", lambda h, b: extract_generic(h, b, "StudyLink")),
    ]

    all_candidates = []
    seen_urls = set()

    for src_id, url, extractor in sources:
        print(f"\n=== Fetching {src_id}: {url}")
        html = fetch(url)
        if not html:
            print(f"  -> failed to fetch")
            continue
        print(f"  -> fetched {len(html)} bytes")
        start = time.time()
        try:
            candidates = extractor(html, url)
        except Exception as e:
            print(f"  -> extract error: {e}")
            continue
        parse_time = time.time() - start
        print(f"  -> parsed {len(candidates)} candidates in {parse_time:.1f}s")

        # Dedup by URL at candidate level
        for c in candidates:
            app_url = c.get("application_url", "")
            if app_url and app_url not in seen_urls:
                seen_urls.add(app_url)
                all_candidates.append(c)
        time.sleep(random.uniform(*JITTER))

    print(f"\nTotal unique candidates from listings: {len(all_candidates)}")

    # Enrich individual scholarship pages and verify links
    enriched = []
    seen_name_org = set()
    for c in all_candidates:
        app_url = c.get("application_url")
        if not app_url:
            continue

        # Try to enrich by visiting the page
        detail = enrich_scholarship(app_url)
        if detail:
            name = detail.get("scholarship_name", "")
            org = detail.get("organization", "")
            key = normalize(name) + "||" + normalize(org)
            if key in seen_name_org:
                continue
            seen_name_org.add(key)

            # Verify the application link
            vr = verify_link(detail.get("application_url"))
            if not vr.get("ok"):
                detail["link_notes"] = vr.get("reason", "link_failed")
                detail["status"] = "inactive"
            else:
                if vr.get("final_url"):
                    detail["application_url"] = vr["final_url"]
                    detail["form_url"] = vr["final_url"]
                detail["status"] = "active"

            # Metadata
            raw_text = detail.get("raw_text", "")
            country = guess_country(app_url, raw_text)
            state = guess_state(raw_text)

            record = {
                "source": f"focused_{src_id}",
                "source_id": f"focused_{src_id}_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{len(enriched)+1:03d}",
                "scholarship_name": name,
                "organization": org,
                "organization_type": "",
                "description": detail.get("description", ""),
                "eligibility": "",
                "amount_min": detail.get("amount_min"),
                "amount_max": detail.get("amount_max"),
                "amount_display": detail.get("amount_display", "Varies"),
                "deadline": detail.get("deadline", ""),
                "application_url": detail.get("application_url"),
                "form_url": detail.get("form_url"),
                "email": None,
                "phone": None,
                "address": "",
                "website": detail.get("website"),
                "category": categorize(name, org, raw_text, app_url),
                "education_level": tag_level(name, raw_text),
                "field_of_study": None,
                "state_restriction": state or "",
                "gpa_min": None,
                "citizenship": "US Citizen" if country == "USA" else ("None" if country == "International" else country),
                "ethnicity": None,
                "gender": None,
                "military_affiliation": None,
                "link_notes": detail.get("link_notes", ""),
                "status": detail.get("status", "active"),
            }
            enriched.append(record)
            if len(enriched) % 20 == 0:
                print(f"  ... enriched {len(enriched)}")
        else:
            pass

    print(f"\nEnriched and verified: {len(enriched)}")

    # Global dedup against DB
    final = []
    for r in enriched:
        dup = False
        for path in DB_PATHS:
            conn = get_db_connection(path)
            if is_dup(conn, r["scholarship_name"], r["organization"]):
                dup = True
                conn.close()
                break
            conn.close()
        if not dup:
            final.append(r)

    print(f"After global dedup: {len(final)} new scholarships")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2)
    print(f"Wrote {len(final)} records to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
