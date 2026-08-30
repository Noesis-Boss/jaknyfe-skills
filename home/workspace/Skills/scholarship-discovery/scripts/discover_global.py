#!/usr/bin/env python3
"""
Global Scholarship Discovery - Supplemental batch for daily 200 target.
Scrapes additional sources beyond the batch_queue, verifies links, dedups, outputs JSON.
"""
import os, sys, json, re, sqlite3, hashlib, time, random, argparse
from datetime import datetime, timezone
from typing import List, Dict, Optional, Tuple
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
]
OUTPUT_DEFAULT = os.path.join(SCRIPT_DIR, "global_discover_output.json")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ScholarSearch/2.0; +https://jaknyfe.zo.space)"}
REQUEST_TIMEOUT = 20
JITTER = (0.2, 0.5)

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
        return {"ok": True, "status": resp.status_code, "final_url": final_url}
    except requests.RequestException as e:
        return {"ok": False, "reason": str(e)[:120]}

def guess_country(url: str, text: str = "") -> str:
    combined = (url + " " + text).lower()
    if any(t in combined for t in [".gc.ca", "canada.ca", "scholarships.ca", "university of toronto", "mcgill", "ubc"]):
        return "Canada"
    if any(t in combined for t in [".ac.uk", "ucas", "scholarships.org.uk", "oxford", "cambridge", "imperial", "edinburgh"]):
        return "UK"
    if any(t in combined for t in ["edu.au", "studyassist", "scholarships.gov.au", "university of sydney", "university of melbourne"]):
        return "Australia"
    if any(t in combined for t in ["new zealand", "studylink", "nz.govt.nz", "auckland.ac.nz", "otago.ac.nz"]):
        return "New Zealand"
    if any(t in combined for t in ["europa.eu", "erasmus", "daad", "campusfrance", "studynetherlands", "ethz.ch", "ox.ac.uk", "cam.ac.uk"]):
        return "EU"
    if any(t in combined for t in [".edu", ".gov", "university", "college", "scholarships.com", "fastweb", "bold.org", "accessscholarships"]):
        return "USA"
    return "International"

def guess_state(text: str) -> Optional[str]:
    states = {
        "arizona": "AZ", "california": "CA", "texas": "TX", "new york": "NY",
        "florida": "FL", "illinois": "IL", "pennsylvania": "PA", "ohio": "OH",
        "georgia": "GA", "north carolina": "NC", "michigan": "MI", "washington": "WA",
        "virginia": "VA", "colorado": "CO", "oregon": "OR", "massachusetts": "MA",
        "new jersey": "NJ", "maryland": "MD", "minnesota": "MN", "missouri": "MO",
        "wisconsin": "WI", "tennessee": "TN", "indiana": "IN", "alabama": "AL",
        "south carolina": "SC", "oklahoma": "OK", "kansas": "KS", "iowa": "IA",
        "kentucky": "KY", "louisiana": "LA", "connecticut": "CT", "utah": "UT",
        "nevada": "NV", "new mexico": "NM", "idaho": "ID", "montana": "MT",
        "wyoming": "WY", "nebraska": "NE", "north dakota": "ND", "south dakota": "SD",
        "maine": "ME", "vermont": "VT", "new hampshire": "NH", "rhode island": "RI",
        "delaware": "DE", "west virginia": "WV", "arkansas": "AR", "mississippi": "MS",
    }
    lower = text.lower()
    for name, abbr in states.items():
        if name in lower or abbr.lower() in lower:
            return abbr
    return None

def tag_category(name: str, org: str, raw_text: str, url: str = "") -> str:
    text = f"{name} {org} {raw_text} {url}".lower()
    for pat, cat in [
        (r"\bmasonic\b", "Masonic"),
        (r"\bstem\b|\bengineering\b|\bcomputer\b|\bmath\b|\bscience\b", "STEM"),
        (r"\bmedicine\b|\bnursing\b|\bhealth\b|\bpharmacy\b", "Medicine"),
        (r"\blaw\b|\blegal\b|\battorney\b", "Law"),
        (r"\bbusiness\b|\bfinance\b|\baccounting\b|\bentrepreneur\b", "Business"),
        (r"\bart\b|\bdesign\b|\bcreative\b|\bfine arts\b", "Arts"),
        (r"\btrade\b|\btechnical\b|\bvocational\b|\bwelding\b|\bautomotive\b", "Trade School"),
        (r"\bwomen\b|\bfemale\b", "Women"),
        (r"\bveteran\b|\bmilitary\b|\barmed forces\b", "Military/Veteran"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b|\bph\.?d\b|\bdoctorate\b", "Graduate"),
        (r"\bcommunity\b|\bvolunteer\b|\bservice\b", "Community"),
        (r"\bsocial science\b|\bpolitical\b|\bsociology\b|\bpsychology\b", "Social Science"),
        (r"\beducation\b|\bteacher\b", "Education"),
        (r"\btech\b|\binformation technology\b|\bit\b", "Tech"),
    ]:
        if re.search(pat, text):
            return cat
    return "Academic"

def tag_level(name: str, raw_text: str) -> str:
    text = f"{name} {raw_text}".lower()
    for pat, lvl in [
        (r"\bph\.?d\b|\bdoctorate\b", "PhD"),
        (r"\bgraduate\b|\bmaster\b|\bmba\b", "Graduate"),
        (r"\btrade\b|\btechnical\b|\bvocational\b", "Trade School"),
        (r"\bassociate\b|\bcommunity college\b", "Associate"),
        (r"\bprofessional\b|\bmedical\b|\blaw\b|\bJD\b", "Professional"),
        (r"\bhigh school\b|\bsecondary\b", "High School"),
    ]:
        if re.search(pat, text):
            return lvl
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
# Site-specific extractors
# ------------------------------------------------------------------
def extract_generic_listing(html: str, base_url: str, org_name: str) -> List[Dict]:
    soup = BeautifulSoup(html, "html.parser")
    candidates = []
    seen = set()
    patterns = [
        re.compile(r"/scholarship/", re.I),
        re.compile(r"/grant/", re.I),
        re.compile(r"/fellowship/", re.I),
        re.compile(r"/award/", re.I),
        re.compile(r"/financial-aid/", re.I),
        re.compile(r"/bursary/", re.I),
    ]
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a.get("href", ""))
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
            "organization": org_name,
            "application_url": href,
            "amount_display": "Varies",
            "deadline": "",
            "raw_text": parent_text,
        })
    return candidates

def extract_from_url(url: str, org_name: str) -> List[Dict]:
    html = fetch(url)
    if not html:
        return []
    return extract_generic_listing(html, url, org_name)

# ------------------------------------------------------------------
# Global source list
# ------------------------------------------------------------------
SOURCES = [
    # Canada
    ("canada_canada_ca", "https://www.canada.ca/en/services/benefits/student/grants-loans.html", "Government of Canada"),
    ("canada_ontario", "https://www.ontario.ca/page/student-financial-aid", "Ontario Student Aid"),
    ("canada_bc", "https://www2.gov.bc.ca/gov/content/education-training/student-financial-aid", "BC Student Aid"),
    ("canada_alberta", "https://alis.alberta.ca/funding-your-education/student-aid/", "Alberta Student Aid"),
    ("canada_quebec", "https://www.quebec.ca/en/education/student-financial-assistance/", "Quebec Student Aid"),
    # UK
    ("uk_ucas", "https://www.ucas.com/student-finance", "UCAS"),
    ("uk_student_finance_england", "https://www.gov.uk/student-finance", "Student Finance England"),
    ("uk_scholarship_search", "https://www.scholarships.org.uk/", "Scholarships.org.uk"),
    ("uk_findamasters", "https://www.findamasters.com/funding/", "FindAMasters"),
    # EU
    ("eu_erasmus_mundus", "https://www.eacea.ec.europa.eu/scholarships/erasmus-mundus-catalogue", "Erasmus Mundus"),
    ("eu_daad", "https://www2.daad.de/deutschland/stipendium/datenbank/en/", "DAAD"),
    ("eu_campusfrance", "https://www.campusfrance.org/en/scholarships", "CampusFrance"),
    ("eu_studynetherlands", "https://www.studynetherlands.org/scholarships", "StudyNetherlands"),
    # Australia
    ("au_studyassist", "https://www.studyassist.gov.au/scholarships", "StudyAssist"),
    ("au_university_of_melbourne", "https://www.unimelb.edu.au/scholarships", "University of Melbourne"),
    ("au_university_of_sydney", "https://www.sydney.edu.au/scholarships/", "University of Sydney"),
    # New Zealand
    ("nz_studylink", "https://www.studylink.govt.nz/funds/scholarships/", "StudyLink NZ"),
    ("nz_auckland", "https://www.auckland.ac.nz/en/for/future-students/funding-and-scholarships.html", "University of Auckland"),
    # USA Masonic
    ("masonic_az", "https://www.azmasonicfoundation.org/scholarships/", "Arizona Masonic Foundation"),
    ("masonic_ca", "https://www.freemason.org/community/scholarships/", "California Masons"),
    ("masonic_tx", "https://www.grandlodgeoftexas.org/charitable-foundation/scholarships/", "Texas Masonic Foundation"),
    ("masonic_ny", "https://www.nymasonicfoundation.org/scholarships/", "New York Masonic Foundation"),
    ("masonic_fl", "https://www.floridalodges.org/scholarships/", "Florida Masons"),
    ("masonic_il", "https://www.illinoismasons.org/scholarships/", "Illinois Masons"),
    # Demographic
    ("demo_hispanic", "https://www.hsf.net/scholarships", "Hispanic Scholarship Fund"),
    ("demo_black", "https://www.UNCF.org/scholarships", "UNCF"),
    ("demo_asian", "https://www.terrapinn.com/scholarships/asian-american/", "Asian American Scholarships"),
    ("demo_indigenous", "https://www.aigw.org/scholarships", "American Indian Graduate Center"),
    ("demo_women_stem", "https://www.swe.org/scholarships/", "SWE Scholarships"),
    ("demo_lgbtq", "https://www.lgbtqfund.org/scholarships", "LGBTQ+ Scholarships"),
    ("demo_disability", "https://www.heathresourcecenter.org/scholarships", "Disability Scholarships"),
    # Professional orgs
    ("prof_ieee", "https://www.ieee.org/education-careers/education/scholarships.html", "IEEE"),
    ("prof_ama", "https://www.ama-assn.org/education-careers/medical-school-admissions/medical-school-scholarships", "American Medical Association"),
    ("prof_aba", "https://www.americanbar.org/groups/legal_education/resources/scholarships/", "American Bar Association"),
    ("prof_nursing", "https://www.nursingworld.org/foundation/scholarships/", "American Nurses Foundation"),
    ("prof_teachers", "https://www.nea.org/grants-and-scholarships", "NEA Foundation"),
    # Field-specific
    ("field_engineering", "https://www.societyofwomenengineers.org/scholarships/", "SWE Engineering"),
    ("field_computer_science", "https://www.ncwit.org/scholarships", "NCWIT"),
    ("field_medicine", "https://www.aamc.org/financial-aid/medical-school-scholarships", "AAMC"),
    ("field_law", "https://www.lsac.org/financial-aid/scholarships", "LSAC"),
    ("field_business", "https://www.gsb.stanford.edu/scholarships", "Stanford GSB Scholarships"),
    ("field_arts", "https://www.collegeart.org/scholarships", "College Art Association"),
    # Additional platforms
    ("platform_fastweb", "https://www.fastweb.com/college-scholarships", "Fastweb"),
    ("platform_cappex", "https://www.cappex.com/scholarships", "Cappex"),
    ("platform_bold", "https://bold.org/scholarships/", "Bold.org"),
    ("platform_scholarships_com", "https://www.scholarships.com/", "Scholarships.com"),
    ("platform_unigo", "https://www.unigo.com/scholarships", "Unigo"),
    ("platform_college_board", "https://bigfuture.collegeboard.org/scholarship-search", "College Board"),
    ("platform_studyportals", "https://www.studyportals.com/scholarships", "StudyPortals"),
    ("platform_scholarshipportal", "https://www.scholarshipportal.eu/", "ScholarshipPortal.eu"),
    ("platform_profellow", "https://www.profellow.com/", "Profellow"),
    ("platform_international_scholarships", "https://www.internationalscholarships.com/", "InternationalScholarships.com"),
    # More USA state sources
    ("usa_state_pa", "https://www.pheaa.org/access-center/scholarships/", "PHEAA Pennsylvania"),
    ("usa_state_ny", "https://www.hesaid.org/ny-scholarships", "HESaID New York"),
    ("usa_state_tx", "https://www.texascollegehelp.org/scholarships", "Texas College Help"),
    ("usa_state_fl", "https://www.floridastudentfinancialaid.sg/ss/", "Florida Student Aid"),
    ("usa_state_il", "https://www.isac.org/grants-and-scholarships/", "ISAC Illinois"),
    ("usa_state_oh", "https://www.ohiohighered.org/students/scholarships", "Ohio Higher Ed"),
    ("usa_state_mi", "https://www.michigan.gov/mistudentaid/scholarships", "Michigan Student Aid"),
    ("usa_state_ga", "https://www.gafutures.org/hope-scholarship/", "Georgia HOPE"),
    ("usa_state_nc", "https://www.cfnc.org/paying-for-school/financial-aid/scholarships/", "CFNC North Carolina"),
    ("usa_state_va", "https://www.schev.edu/index/students/financing/scholarships", "SCHEV Virginia"),
    ("usa_state_co", "https://www.colorado.gov/pacific/sites/default/files/Students_FinancialAid_Scholarships.pdf", "Colorado Student Aid"),
    ("usa_state_wa", "https://www.wsac.wa.gov/scholarships", "WSAC Washington"),
    ("usa_state_or", "https://oregonstudentaid.gov/scholarships", "Oregon Student Aid"),
    ("usa_state_mn", "https://www.ohe.state.mn.us/scholarships", "Minnesota OHE"),
    ("usa_state_wi", "https://dpi.wi.gov/financial-aid/scholarships", "Wisconsin DPI"),
    # USA Universities
    ("uni_harvard", "https://college.harvard.edu/financial-aid/scholarships", "Harvard"),
    ("uni_stanford", "https://financialaid.stanford.edu/undergrad/scholarships.html", "Stanford"),
    ("uni_mit", "https://sfs.mit.edu/undergraduate-students/types-of-aid/scholarships/", "MIT"),
    ("uni_yale", "https://financialaid.yale.edu/undergraduate-aid/scholarships", "Yale"),
    ("uni_princeton", "https://undergrad.princeton.edu/costs-aid/scholarships", "Princeton"),
    ("uni_berkeley", "https://financialaid.berkeley.edu/types-of-aid/scholarships/", "UC Berkeley"),
    ("uni_michigan", "https://finaid.umich.edu/ scholarships/", "University of Michigan"),
    ("uni_texas", "https://onestop.utexas.edu/managing-costs/scholarships/", "University of Texas"),
    ("uni_ucla", "https://www.financialaid.ucla.edu/undergraduate-students/types-of-aid/scholarships", "UCLA"),
    ("uni_ucsd", "https://fas.ucsd.edu/financial-aid/scholarships.html", "UCSD"),
    ("uni_ucsb", "https://financialaid.ucsb.edu/undergraduate/scholarships", "UCSB"),
    ("uni_ucsc", "https://financialaid.ucsc.edu/undergraduate/types-of-aid/scholarships", "UCSC"),
    ("uni_ucr", "https://financialaid.ucr.edu/scholarships", "UCR"),
    ("uni_uci", "https://financialaid.uci.edu/undergraduate/types-of-aid/scholarships", "UCI"),
    ("uni_ucd", "https://financialaid.ucdavis.edu/undergraduate/scholarships", "UC Davis"),
    ("uni_umich", "https://sfs.umich.edu/scholarships", "University of Michigan"),
    ("uni_uky", "https://financialaid.uky.edu/scholarships", "University of Kentucky"),
    ("uni_ucf", "https://financialaid.ucf.edu/scholarships", "UCF"),
    ("uni_rutgers", "https://financialaid.rutgers.edu/scholarships", "Rutgers"),
    ("uni_tamu", "https://financialaid.tamu.edu/scholarships/", "Texas A&M"),
    ("uni_ku", "https://financialaid.ku.edu/scholarships", "University of Kansas"),
]

def main():
    parser = argparse.ArgumentParser(description="Global scholarship discovery")
    parser.add_argument("--limit", type=int, default=200, help="Target new scholarships")
    parser.add_argument("--output", default=OUTPUT_DEFAULT, help="Output JSON path")
    args = parser.parse_args()

    before = {}
    for db_path in DB_PATHS:
        if os.path.exists(db_path):
            conn = get_db_connection(db_path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM scholarships")
            before[db_path] = cur.fetchone()[0]
            conn.close()
        else:
            before[db_path] = 0

    all_candidates: List[Dict] = []
    seen_urls = set()
    source_report = []

    for src_id, url, org_name in SOURCES:
        print(f"\n=== Fetching {src_id}: {url}")
        html = fetch(url)
        if not html:
            print(f"  -> failed to fetch")
            source_report.append({"id": src_id, "group": org_name, "count": 0, "status": "fetch_failed"})
            continue
        print(f"  -> fetched {len(html)} bytes")
        start = time.time()
        candidates = extract_generic_listing(html, url, org_name)
        parse_time = time.time() - start
        print(f"  -> parsed {len(candidates)} candidates in {parse_time:.1f}s")

        # Dedup by URL within this run
        new_candidates = []
        for c in candidates:
            app_url = c.get("application_url", "")
            if app_url and app_url not in seen_urls:
                seen_urls.add(app_url)
                new_candidates.append(c)
        print(f"  -> {len(new_candidates)} new unique candidates")

        all_candidates.extend(new_candidates)
        source_report.append({"id": src_id, "group": org_name, "count": len(new_candidates), "status": "ok"})
        time.sleep(random.uniform(*JITTER))

    print(f"\nTotal unique candidates: {len(all_candidates)}")

    # Verify links and build final records
    verified = []
    added_count = 0
    skipped_dup = 0
    skipped_link = 0
    errors = []

    today = datetime.now(timezone.utc).strftime("%Y%m%d")

    for idx, c in enumerate(all_candidates[: args.limit * 3], start=1):
        app_url = c.get("application_url", "")
        raw_text = c.get("raw_text", "")

        # Check duplicates across DBs
        dup = False
        for db_path in DB_PATHS:
            if os.path.exists(db_path):
                conn = get_db_connection(db_path)
                if is_dup(conn, c.get("scholarship_name", ""), c.get("organization", "")):
                    dup = True
                    conn.close()
                    break
                conn.close()
        if dup:
            skipped_dup += 1
            continue

        # Verify link
        link_notes = ""
        status = "active"
        if app_url:
            v = verify_link(app_url)
            if not v.get("ok"):
                skipped_link += 1
                link_notes = v.get("reason", "link_failed")
                status = "inactive"
                if v.get("final_url"):
                    app_url = v["final_url"]
            else:
                app_url = v.get("final_url", app_url)

        # Build record
        detail = extract_detail_from_page(raw_text, app_url) if raw_text else {}
        record = {
            "source": f"global_{src_id}",
            "source_id": f"global_{src_id}_{today}_{idx:03d}",
            "scholarship_name": c.get("scholarship_name") or detail.get("scholarship_name", ""),
            "organization": c.get("organization") or detail.get("organization", ""),
            "organization_type": "",
            "description": "",
            "eligibility": "",
            "amount_min": detail.get("amount_min"),
            "amount_max": detail.get("amount_max"),
            "amount_display": detail.get("amount_display", c.get("amount_display", "Varies")),
            "deadline": c.get("deadline") or detail.get("deadline", ""),
            "application_url": app_url,
            "form_url": None,
            "email": None,
            "phone": None,
            "address": "",
            "website": app_url,
            "category": tag_category(c.get("scholarship_name", ""), c.get("organization", ""), raw_text, app_url),
            "education_level": tag_level(c.get("scholarship_name", ""), raw_text),
            "field_of_study": None,
            "state_restriction": guess_state(raw_text),
            "gpa_min": None,
            "citizenship": None,
            "ethnicity": None,
            "gender": None,
            "military_affiliation": None,
            "link_notes": link_notes,
            "status": status,
        }
        verified.append(record)
        added_count += 1

        if added_count >= args.limit:
            break

    print(f"\nAdded: {added_count}, Skipped dup: {skipped_dup}, Skipped link: {skipped_link}, Errors: {len(errors)}")

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(verified, f, indent=2)
    print(f"Wrote {len(verified)} records to {args.output}")

    after = {}
    for db_path in DB_PATHS:
        if os.path.exists(db_path):
            conn = get_db_connection(db_path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM scholarships")
            after[db_path] = cur.fetchone()[0]
            conn.close()
        else:
            after[db_path] = 0

    print(f"Before: {before}")
    print(f"After: {after}")
    print(f"Source report: {json.dumps(source_report[:10], indent=2)}")

if __name__ == "__main__":
    main()
