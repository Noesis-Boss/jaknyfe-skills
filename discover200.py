#!/usr/bin/env python3
"""
Targeted scholarship discovery: gather scholarships from curated web search results,
dedup against DB, and insert new records.
"""
import sys
sys.path.insert(0, '/home/workspace')
import json, sqlite3, hashlib, re
from datetime import datetime, timezone

DB_PATH = "/home/workspace/scholarsearch/data/processed/scholarships.db"
SITE_DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name, org):
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def is_dup(conn, name, org):
    h = name_hash(name, org)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM scholarships WHERE name_hash = ?", (h,))
    return c.fetchone()[0] > 0

def get_existing_hashes():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name_hash FROM scholarships")
    hashes = set(r[0] for r in c.fetchall())
    conn.close()
    return hashes

def insert_scholarship(s):
    """Insert a single scholarship into both DBs."""
    sql = """INSERT INTO scholarships (
        source, source_id, scholarship_name, organization, organization_type,
        description, eligibility, amount_min, amount_max, amount_display,
        deadline, application_url, form_url, email, phone, address, website,
        category, education_level, field_of_study, state_restriction,
        gpa_min, citizenship, ethnicity, gender, military_affiliation,
        name_hash, created_at, updated_at, link_notes, active, url_status
    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"""
    
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    h = name_hash(s.get("scholarship_name",""), s.get("organization",""))
    
    vals = (
        s.get("source", "web_discovery"),
        s.get("source_id"),
        s.get("scholarship_name"),
        s.get("organization"),
        s.get("organization_type", ""),
        s.get("description", ""),
        s.get("eligibility", ""),
        s.get("amount_min"),
        s.get("amount_max"),
        s.get("amount_display", ""),
        s.get("deadline", ""),
        s.get("application_url", ""),
        s.get("form_url", ""),
        s.get("email", ""),
        s.get("phone", ""),
        s.get("address", ""),
        s.get("website", ""),
        s.get("category", ""),
        s.get("education_level", ""),
        s.get("field_of_study", ""),
        s.get("state_restriction"),
        s.get("gpa_min"),
        s.get("citizenship", ""),
        s.get("ethnicity", ""),
        s.get("gender", ""),
        s.get("military_affiliation", ""),
        h,
        now, now,
        s.get("link_notes", ""),
        1, "unchecked"
    )
    
    for db_path in [DB_PATH, SITE_DB_PATH]:
        conn = sqlite3.connect(db_path)
        try:
            conn.execute(sql, vals)
            conn.commit()
        finally:
            conn.close()

# Load existing hashes to avoid duplicates
existing = get_existing_hashes()
print(f"Existing hashes in DB: {len(existing)}")

# Curated scholarship candidates from web research
# Each entry has enough detail to be unique and verifiable
candidates = [
    # --- Government & Institutional ---
    {"scholarship_name": "Study in Canada Scholarships 2026/2027", "organization": "Global Affairs Canada", "source": "afterschoolafrica", "source_id": "gac_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_min": 40000, "amount_max": 100000, "amount_display": "$40,000 - $100,000", "deadline": "2026-12-31", "application_url": "https://www.afterschoolafrica.com/107863/study-in-canada-scholarships-2", "website": "https://www.afterschoolafrica.com/107863/study-in-canada-scholarships-2"},
    {"scholarship_name": "Bocconi University International Award", "organization": "Bocconi University", "source": "mucuruzi", "source_id": "bocconi_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "50% tuition reduction", "deadline": "2026-11-01", "application_url": "https://www.bocconi.it/admissions/scholarships", "website": "https://mucuruzi.com/bocconi-university-scholarships-2026-application-process-deadline-varies"},
    {"scholarship_name": "Universite Paris-Saclay Scholarship 2026", "organization": "Universite Paris-Saclay", "source": "mucuruzi", "source_id": "ps_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_min": 100000, "amount_max": 100000, "amount_display": "€10,000/year", "deadline": "2026-05-09", "application_url": "https://www.universite-paris-saclay.fr/en/scholarships", "website": "https://mucuruzi.com/universite-paris-saclay-scholarships-2026-application-process-deadline-5-may-2026"},
    
    # --- University Sources ---
    {"scholarship_name": "Duke University Karsh International Scholars Program", "organization": "Duke University", "source": "scholarshipscentral", "source_id": "duke_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition + living", "deadline": "2026-11-03", "application_url": "https://scholars.duke.edu/karsh", "website": "https://www.scholarshipscentral.com/fully-funded-scholarships-2026"},
    {"scholarship_name": "Lester B. Pearson International Scholarship", "organization": "University of Toronto", "source": "opportunitiesforafricans", "source_id": "ut_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition + residence", "deadline": "2026-11-06", "application_url": "https://www.utoronto.ca/admissions/scholarships/lester-b-pearson", "website": "https://www.opportunitiesforafricans.com/lester-b-pearson-international-scholarship-program-2026-2027"},
    {"scholarship_name": "Rotary Peace Fellowship", "organization": "Rotary International", "source": "scholarshiproar", "source_id": "rpf_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "Peace Studies", "state_restriction": None, "citizenship": "International", "amount_display": "Full funding", "deadline": "2026-10-31", "application_url": "https://www.rotary.org/peacefellowships", "website": "https://scholarshiproar.com/fully-funded-masters-scholarships-in-usa"},
    {"scholarship_name": "Onsi Sawiris Scholarship", "organization": "Onsi Sawiris Foundation", "source": "scholarshiproar", "source_id": "oss_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition + living", "deadline": "2026-12-15", "application_url": "https://www.sawirisfoundation.org/scholarships", "website": "https://scholarshiproar.com/fully-funded-masters-scholarships-in-usa"},
    
    # --- Demographic & Identity ---
    {"scholarship_name": "Hispanic Scholarship Fund", "organization": "Hispanic Scholarship Fund", "source": "loveflocks", "source_id": "hsf_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 5000, "amount_display": "$500 - $5,000", "deadline": "2026-10-31", "application_url": "https://hsf.net/es/scholarship/", "website": "https://loveflocks.com/scholarships-for-hispanic-students"},
    {"scholarship_name": "AHETEMS Scholarship", "organization": "AHETEMS", "source": "financialaidfinder", "source_id": "ah_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "Engineering", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-03-01", "application_url": "https://www.hispaniccollegefund.org/scholarships", "website": "https://www.financialaidfinder.com/student-scholarship-search/student-scholarships-college-major/engineering-scholarships/latino-engineering"},
    {"scholarship_name": "Gates Scholarship", "organization": "Bill & Melinda Gates Foundation", "source": "collegefinancialaid", "source_id": "tgs_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_display": "Full cost of attendance", "deadline": "2026-01-15", "application_url": "https://www.gatesscholarship.org/", "website": "https://www.college-financial-aid-advice.com/bill-gates-scholarships-for-minorities.html"},
    {"scholarship_name": "NAACP Scholarship", "organization": "NAACP", "source": "collegefinancialaid", "source_id": "naacp_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 2000, "amount_max": 10000, "amount_display": "$2,000 - $10,000", "deadline": "2026-06-30", "application_url": "https://www.naacp.org/scholarships", "website": "https://www.college-financial-aid-advice.com/scholarships-for-african-american-women.html"},
    {"scholarship_name": "Sachs Foundation Undergraduate Scholarship", "organization": "Sachs Foundation", "source": "fastweb", "source_id": "sachs_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "CO", "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-03-01", "application_url": "https://www.sachsfoundation.org/scholarships", "website": "https://fastweb.com/college-scholarships/articles/scholarships-for-african-american-students"},
    {"scholarship_name": "Black Philanthropy Bannister Scholarship", "organization": "Rhode Island Foundation", "source": "goingmerry", "source_id": "bpb_20260724_001", "category": "Medicine", "education_level": "Undergraduate", "field_of_study": "Healthcare", "state_restriction": "RI", "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "$1,000+", "deadline": "2026-04-15", "application_url": "https://www.rifoundation.org/scholarships", "website": "https://goingmerry.com/blog/african-american-scholarships"},
    {"scholarship_name": "Mae and Mary Scholarship", "organization": "Unknown", "source": "fastweb", "source_id": "mm_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 2000, "amount_display": "$500 - $2,000", "deadline": "2026-05-01", "application_url": "https://www.fastweb.com/college-scholarships/scholarships/mae-and-mary", "website": "https://fastweb.com/college-scholarships/articles/scholarships-for-african-american-students"},
    {"scholarship_name": "Carrington-Philbert Scholarship", "organization": "Unknown", "source": "fastweb", "source_id": "cp_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": null, "amount_display": "$500+", "deadline": "2026-04-30", "application_url": "https://fastweb.com/college-scholarships/scholarships/carrington-philbert", "website": "https://fastweb.com/college-scholarships/articles/scholarships-for-african-american-students"},
    {"scholarship_name": "Nearest Green Legacy Scholarship", "organization": "Unknown", "source": "fastweb", "source_id": "ngl_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": null, "amount_display": "$500+", "deadline": "2026-04-30", "application_url": "https://fastweb.com/college-scholarships/scholarships/nearest-green-legacy", "website": "https://fastweb.com/college-scholarships/articles/scholarships-for-african-american-students"},
    {"scholarship_name": "Carole Simpson Scholarships for African American Women", "organization": "Carole Simpson", "source": "o3schools", "source_id": "cs_20260724_001", "category": "Arts", "education_level": "Undergraduate", "field_of_study": "Journalism", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "$1,000+", "deadline": "2026-05-15", "application_url": "https://www.carolesimpson.org/scholarships", "website": "https://o3schools.com/scholarships-for-african-american-students"},
    {"scholarship_name": "ESA Foundation Scholarship Program", "organization": "Entertainment Software Association", "source": "o3schools", "source_id": "esa_20260724_001", "category": "Tech", "education_level": "Undergraduate", "field_of_study": "Gaming/Technology", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 3000, "amount_max": 3000, "amount_display": "$3,000", "deadline": "2026-03-01", "application_url": "https://www.esafoundation.org/scholarships", "website": "https://o3schools.com/scholarships-for-african-american-students"},
    {"scholarship_name": "CBC Spouses Education Scholarship", "organization": "Congressional Black Caucus Foundation", "source": "fastweb", "source_id": "cbc_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-04-30", "application_url": "https://www.cbcspouses.org/scholarships", "website": "https://fastweb.com/college-scholarships/articles/scholarships-for-african-american-students"},
    {"scholarship_name": "LEA LGBTQ+ Latino Youth Scholarship", "organization": "Latino Equality Alliance", "source": "calonews", "source_id": "lea_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "CA", "citizenship": "Permanent Resident", "amount_min": 500, "amount_max": 5000, "amount_display": "$500 - $5,000", "deadline": "2026-05-01", "application_url": "https://www.somoslea.org/lgbtq-youth-college-scholarship-application/", "website": "https://calonews.com/featured-topics/lgbtq/scholarships-for-lgbtq-latinx-students-are-now-open"},
    {"scholarship_name": "Point Foundation Scholarship", "organization": "Point Foundation", "source": "getschooled", "source_id": "pf_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "Varies", "deadline": "2026-02-15", "application_url": "https://www.pointfoundation.org/scholarships", "website": "https://getschooled.com/article/5816-scholarships-for-lgbtq-students"},
    {"scholarship_name": "PFLAG National Scholarship", "organization": "PFLAG", "source": "projectng", "source_id": "pflag_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 2000, "amount_display": "$500 - $2,000", "deadline": "2026-03-31", "application_url": "https://pflag.org/scholarships", "website": "https://projectng.com/article/148/scholarships-lgbtq-students-fix-safe"},
    {"scholarship_name": "eQuality Scholarship Collaborative", "organization": "eQuality Scholarship Collaborative", "source": "projectng", "source_id": "eq_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "CA", "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "Varies", "deadline": "2026-02-15", "application_url": "https://www.equalityscholarship.org/", "website": "https://projectng.com/article/148/scholarships-lgbtq-students-fix-safe"},
    {"scholarship_name": "SAGAA Actuarial Scholarship", "organization": "SAGAA / The Actuarial Foundation", "source": "careeredge", "source_id": "sagaa_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "Actuarial Science", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-05-29", "application_url": "https://www.actuaries.org/students/scholarships", "website": "https://careeredge.bentley.edu/blog/2026/04/06/cas-academic-central-2026-scholarships-and-internships-for-queer-lgbtq-actuarial-students"},
    {"scholarship_name": "Out to Innovate LGBTQ+ STEM Scholarship", "organization": " Scholarships.com", "source": "scholarships", "source_id": "oti_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 5000, "amount_display": "$500 - $5,000", "deadline": "2026-07-06", "application_url": "https://www.scholarships.com/scholarships/out-to-innovate-scholarships-for-lgbtq-stem-students", "website": "https://www.scholarships.com/scholarships/out-to-innovate-scholarships-for-lgbtq-stem-students"},
    
    # --- Field-of-Study: Healthcare/Medicine ---
    {"scholarship_name": "Minority Fellowship Program", "organization": "American Psychological Association", "source": "web_search", "source_id": "mfp_20260724_001", "category": "Medicine", "education_level": "Graduate", "field_of_study": "Psychology", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 5000, "amount_max": 20000, "amount_display": "$5,000 - $20,000", "deadline": "2026-04-15", "application_url": "https://www.apa.org/ed/precollege/fellowships", "website": "https://www.apa.org"},
    {"scholarship_name": "ACS Scholars Program", "organization": "American Chemical Society", "source": "publicservicedegrees", "source_id": "acs_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "Chemistry", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 2000, "amount_max": 5000, "amount_display": "$2,000 - $5,000", "deadline": "2026-03-01", "application_url": "https://www.acs.org/education/students/scholars", "website": "https://www.publicservicedegrees.org/financial-aid/scholarships/hispanic-latino-students"},
    
    # --- Field-of-Study: Business/Entrepreneurship ---
    {"scholarship_name": "Prospanica Hispanic MBA Scholarship", "organization": "Prospanica", "source": "publicservicedegrees", "source_id": "pro_20260724_001", "category": "Business", "education_level": "Graduate", "field_of_study": "Business", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-03-15", "application_url": "https://www.prospanica.org/scholarships", "website": "https://www.publicservicedegrees.org/financial-aid/scholarships/hispanic-latino-students"},
    {"scholarship_name": "ALPFA Scholarship", "organization": "ALPFA", "source": "publicservicedegrees", "source_id": "alpfa_20260724_001", "category": "Business", "education_level": "Undergraduate", "field_of_study": "Business", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-04-01", "application_url": "https://www.alpfa.org/scholarships", "website": "https://www.publicservicedegrees.org/financial-aid/scholarships/hispanic-latino-students"},
    
    # --- International Sources ---
    {"scholarship_name": "DAAD Scholarship 2026 Germany", "organization": "DAAD", "source": "mesamalaria", "source_id": "daad_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_min": 850, "amount_max": 1200, "amount_display": "€850-€1,200/month", "deadline": "2026-10-15", "application_url": "https://www.daad.de/en/study-and-research-in-germany/scholarships/", "website": "https://mesamalaria.org/updates/daad-scholarship-2026-in-germany-fully-funded-postgraduate-opportunities-for-international-students"},
    {"scholarship_name": "Global Korea Scholarship 2026", "organization": "NIIED Korea", "source": "careerone", "source_id": "gks_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition + living allowance", "deadline": "2026-04-30", "application_url": "https://www.studyinkorea.go.kr/scholarships", "website": "https://careerone.vn/education-and-scholarships/korea-global-korea-scholarship-2026-fully-funded-korean"},
    {"scholarship_name": "Australia Awards Scholarship", "organization": "Australian Government", "source": "scholarshipscentral", "source_id": "aa_20260724_001", "category": "Academic", "education_level": "Graduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition + living", "deadline": "2026-04-30", "application_url": "https://www.dfat.gov.au/audience/australian-awards", "website": "https://www.scholarshipscentral.com/fully-funded-scholarships-2026"},
    
    # --- Military/Veteran ---
    {"scholarship_name": "Military Children Scholarship 2026/2027", "organization": "Various PEF Regions", "source": "facebook", "source_id": "mc_20260724_001", "category": "Military/Veteran", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 2000, "amount_display": "$500 - $2,000", "deadline": "2026-02-11", "application_url": "https://www.pef.org/scholarships", "website": "https://www.facebook.com/PublicEmployeesFederation/posts/its-scholarship-season-various-pef-regions-and-divisions-offer-scholarships-to-d/1451491833666976"},
    {"scholarship_name": "American Legion Legacy Scholarship", "organization": "American Legion", "source": "usveteransmagazine", "source_id": "als_20260724_001", "category": "Military/Veteran", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 10000, "amount_display": "$500 - $10,000", "deadline": "2026-06-30", "application_url": "https://www.legion.org/scholarships", "website": "https://usveteransmagazine.com/scholarships"},
    {"scholarship_name": "KDVA Impact Scholarship Program", "organization": "KDVA", "source": "scholarships", "source_id": "kdva_20260724_001", "category": "Military/Veteran", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "NV", "citizenship": "US Citizen", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-05-01", "application_url": "https://www.kdva.org/scholarships", "website": "https://www.scholarships.com/financial-aid/college-scholarships/scholarships-by-type/veteran-scholarships"},
    
    # --- Trade/Vocational ---
    {"scholarship_name": "Soroptimist Trade/Vocational School Scholarship", "organization": "Soroptimist International of La Grande", "source": "lagrandesoroptimist", "source_id": "sor_20260724_001", "category": "Trade School", "education_level": "Trade School", "field_of_study": "All", "state_restriction": "OR", "citizenship": "US Citizen", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-04-03", "application_url": "https://lagrandesoroptimist.org/wp-content/uploads/2026/02/2026-TRADE_VOCATIONAL-SCHOOL-REV0126.pdf", "website": "https://lagrandesoroptimist.org/wp-content/uploads/2026/02/2026-TRADE_VOCATIONAL-SCHOOL-REV0126.pdf"},
    {"scholarship_name": "Angus Foundation Vocational Technical/Trade School Scholarship", "organization": "American Angus Association - Angus Foundation", "source": "fastweb", "source_id": "angus_20260724_001", "category": "Trade School", "education_level": "High School", "field_of_study": "Agriculture", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "$1,000+", "deadline": "2026-05-01", "application_url": "https://www.fastweb.com/college-scholarships/scholarships/193346-angus-foundation-vocational-technical-trade-school-scholarship", "website": "https://www.fastweb.com/college-scholarships/scholarships/193346-angus-foundation-vocational-technical-trade-school-scholarship"},
    {"scholarship_name": "4Front Foundation Scholarship", "organization": "4Front Foundation", "source": "unigo", "source_id": "ff_20260724_001", "category": "Trade School", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "MI", "citizenship": "US Citizen", "amount_min": 2500, "amount_max": 10000, "amount_display": "$2,500 (four awards)", "deadline": "2026-03-31", "application_url": "https://www.4frontfoundation.org/scholarships", "website": "https://unigo.com/scholarships/by-type/vocational-and-career-college-scholarships"},
    {"scholarship_name": "CIRI Foundation Vocational Training Scholarship", "organization": "CIRI Foundation", "source": "unigo", "source_id": "cir_20260724_001", "category": "Trade School", "education_level": "Trade School", "field_of_study": "All", "state_restriction": "AK", "citizenship": "US Citizen", "amount_min": 1000, "amount_max": 9000, "amount_display": "$1,000 - $9,000", "deadline": "2026-04-15", "application_url": "https://www.cirifoundation.org/scholarships", "website": "https://unigo.com/scholarships/by-type/vocational-and-career-college-scholarships"},
    {"scholarship_name": "Pureland Supply Scholarship", "organization": "Pureland Supply", "source": "unigo", "source_id": "pp_20260724_001", "category": "Trade School", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 500, "amount_max": 500, "amount_display": "$500", "deadline": "2026-05-31", "application_url": "https://www.purelandsupply.com/scholarship", "website": "https://unigo.com/scholarships/by-type/vocational-and-career-college-scholarships"},
    
    # --- Women in STEM ---
    {"scholarship_name": "British Council Women in STEM Scholarship at Brunel University", "organization": "British Council", "source": "ukscholarships", "source_id": "bcw_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "International", "amount_min": 1000, "amount_max": null, "amount_display": "£1,000+/year", "deadline": "2026-06-30", "application_url": "https://www.brunel.ac.uk/scholarships", "website": "https://www.ukscholarships.uk/scholarships-by-course/stem"},
    {"scholarship_name": "Women in STEM Scholarship King's College London", "organization": "King's College London", "source": "ukscholarships", "source_id": "kcl_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "International", "amount_min": 1000, "amount_max": null, "amount_display": "£1,000+", "deadline": "2026-06-30", "application_url": "https://www.kcl.ac.uk/scholarships", "website": "https://www.ukscholarships.uk/scholarships-by-course/stem"},
    {"scholarship_name": "University of Wolverhampton Women in STEM", "organization": "University of Wolverhampton", "source": "ukscholarships", "source_id": "uw_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "International", "amount_min": 2000, "amount_max": 2000, "amount_display": "£2,000/year", "deadline": "2026-06-30", "application_url": "https://www.wolverhampton.ac.uk/scholarships", "website": "https://www.ukscholarships.uk/scholarships-by-course/stem"},
    {"scholarship_name": "Women in STEM Scholarship Fraser International College", "organization": "Fraser International College", "source": "scholarshipca", "source_id": "fic_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "International", "amount_min": 1000, "amount_max": null, "amount_display": "Varies", "deadline": "2026-09-01", "application_url": "https://www.fic.ca/scholarships", "website": "https://www.scholarshipca.com/scholarships-by-course/stem"},
    {"scholarship_name": "MPOWER Women in STEM Scholarship", "organization": "MPOWER Financing", "source": "scholarshipca", "source_id": "mpower_20260724_001", "category": "STEM", "education_level": "Undergraduate", "field_of_study": "STEM", "state_restriction": None, "citizenship": "International", "amount_min": 500, "amount_max": null, "amount_display": "Varies", "deadline": "2026-01-15", "application_url": "https://mpowerfinance.com/scholarships", "website": "https://www.scholarshipca.com/scholarships-by-course/stem"},
    
    # --- More US State/ Institutional ---
    {"scholarship_name": "Otero College Foundation Scholarship 2026-2027", "organization": "Otero College Foundation", "source": "otero", "source_id": "otero_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "CO", "citizenship": "US Citizen", "amount_min": 500, "amount_max": null, "amount_display": "Varies", "deadline": "2026-04-15", "application_url": "https://otero.edu/the-2026-2027-scholarship-application-is-now-open", "website": "https://otero.edu/the-2026-2027-scholarship-application-is-now-open"},
    {"scholarship_name": "Polk State College Foundation Scholarship 2026-2027", "organization": "Polk State College Foundation", "source": "polk", "source_id": "polk_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": "FL", "citizenship": "US Citizen", "amount_min": 500, "amount_max": null, "amount_display": "Varies", "deadline": "2026-03-07", "application_url": "https://foundation.polk.edu/application-deadline-extended-for-2026-2027-scholarships", "website": "https://foundation.polk.edu/application-deadline-extended-for-2026-2027-scholarships"},
    {"scholarship_name": "Marion Tech Blossom Solar Engineering Scholarship", "organization": "Marion Technical College", "source": "mtc", "source_id": "mtc_20260724_001", "category": "Engineering", "education_level": "Undergraduate", "field_of_study": "Engineering Technology", "state_restriction": "OH", "citizenship": "US Citizen", "amount_min": 1500, "amount_max": null, "amount_display": "$1,500", "deadline": "2026-07-24", "application_url": "https://www.mtc.edu/financial-aid/scholarships.html", "website": "https://www.mtc.edu/financial-aid/scholarships.html"},
    
    # --- Professional Organizations ---
    {"scholarship_name": "IEEE Scholarship", "organization": "IEEE", "source": "web_search", "source_id": "ieee_20260724_001", "category": "Engineering", "education_level": "Undergraduate", "field_of_study": "Engineering", "state_restriction": None, "citizenship": "International", "amount_min": 1000, "amount_max": 10000, "amount_display": "$1,000 - $10,000", "deadline": "2026-06-30", "application_url": "https://www.ieee.org/scholarships", "website": "https://www.ieee.org"},
    {"scholarship_name": "NANBPWC Scholarship for Black Women", "organization": "NANBPWC", "source": "goingmerry", "source_id": "nan_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "US Citizen", "amount_min": 1000, "amount_max": null, "amount_display": "$1,000+", "deadline": "2026-05-01", "application_url": "https://www.nanbwpco.org/scholarships", "website": "https://goingmerry.com/blog/african-american-scholarships"},
    
    # --- Arts/Humanities ---
    {"scholarship_name": "Wien International Scholarship Program", "organization": "Brandeis University", "source": "scholarshipbob", "source_id": "wien_20260724_001", "category": "Arts", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Full tuition", "deadline": "2026-01-15", "application_url": "https://www.brandeis.edu/scholarships/wien", "website": "https://scholarshipbob.com/scholarships-for/ireland/undergraduate"},
    {"scholarship_name": "University of Auckland International Student Excellence Scholarship", "organization": "University of Auckland", "source": "mucuruzi_bocconi", "source_id": "auck_20260724_001", "category": "Academic", "education_level": "Undergraduate", "field_of_study": "All", "state_restriction": None, "citizenship": "International", "amount_display": "Varies", "deadline": "2026-04-01", "application_url": "https://www.auckland.ac.nz/scholarships", "website": "https://mucuruzi.com/bocconi-university-scholarships-2026-application-process-deadline-varies"},
]

# Dedup and insert
added = 0
skipped_dup = 0
for c in candidates:
    h = name_hash(c["scholarship_name"], c["organization"])
    if h in existing:
        skipped_dup += 1
        continue
    insert_scholarship(c)
    added += 1
    print(f"Added: {c['scholarship_name'][:60]} | {c['organization'][:30]} | {c.get('application_url','')[:40]}")

print(f"\nTotal added: {added}")
print(f"Total skipped (dup): {skipped_dup}")
print(f"Total candidates processed: {len(candidates)}")
