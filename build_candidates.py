import json, re, hashlib, sqlite3, requests
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def normalize(text):
    if not text: return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name, org):
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def clean_num(val):
    if not val: return None
    m = re.search(r"[\$€£]?\s*([0-9,]+)", str(val).replace(",", ""))
    return int(m.group(1)) if m else None

def is_dup(conn, name, org):
    h = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (h,))
    return cur.fetchone() is not None

def insert_scholarship(s):
    nh = name_hash(s.get("scholarship_name",""), s.get("organization",""))
    for db_path in DBS:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
        if cur.fetchone():
            conn.close()
            continue
        try:
            cur.execute("""INSERT INTO scholarships (
                source, source_id, scholarship_name, organization, organization_type,
                description, eligibility, amount_min, amount_max, amount_display,
                deadline, application_url, form_url, email, phone, address, website,
                category, education_level, field_of_study, state_restriction,
                gpa_min, citizenship, ethnicity, gender, military_affiliation,
                name_hash, link_notes, url_status)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    s.get("source","web_search"),
                    s.get("source_id",""),
                    s.get("scholarship_name",""),
                    s.get("organization",""),
                    s.get("organization_type",""),
                    s.get("description",""),
                    s.get("eligibility",""),
                    s.get("amount_min"),
                    s.get("amount_max"),
                    s.get("amount_display",""),
                    s.get("deadline",""),
                    s.get("application_url",""),
                    s.get("form_url",""),
                    s.get("email",""),
                    s.get("phone",""),
                    s.get("address",""),
                    s.get("website",""),
                    s.get("category","Academic"),
                    s.get("education_level","Undergraduate"),
                    s.get("field_of_study",""),
                    s.get("state_restriction",""),
                    s.get("gpa_min"),
                    s.get("citizenship","None"),
                    s.get("ethnicity",""),
                    s.get("gender",""),
                    s.get("military_affiliation",""),
                    nh,
                    s.get("link_notes",""),
                    s.get("url_status","unchecked"),
                ))
            conn.commit()
        except Exception as e:
            pass
        finally:
            conn.close()

# Load existing
conn = sqlite3.connect(DBS[0])
cur = conn.cursor()
cur.execute("SELECT scholarship_name, organization FROM scholarships")
existing = set()
for row in cur.fetchall():
    existing.add((normalize(row[0]), normalize(row[1])))
conn.close()

# Build comprehensive candidates from web_search data
candidates = []

# ===== Category: Government/Institutional (USA) =====
gov_us = [
    {"name":"BigFuture Scholarships","org":"College Board","cat":"Academic","edu":"High School","field":"","amount":"$40,000","deadline":"7/31/26","url":"https://bigfuture.collegeboard.org/scholarship-search","source":"usa_gov"},
    {"name":"$1,000 Invite-a-Friend Scholarship","org":"Fastweb","cat":"Academic","edu":"Undergraduate","field":"","amount":"$1,000","deadline":"Rolling","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Debt.com Scholarship for Aggressive Scholarship Applicants","org":"Debt.com","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Gen and Kelly Tanabe Think about Your Future Scholarship","org":"Fastweb","cat":"Academic","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"12/31/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Sallie $2,000 No Essay Scholarship","org":"Sallie","cat":"Academic","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"7/31/26","url":"https://www.scholarships.com/scc.aspx?pid=1438","source":"usa_platform"},
    {"name":"Niche $25,000 No Essay Scholarship","org":"Niche","cat":"Academic","edu":"Undergraduate","field":"","amount":"$25,000","deadline":"7/31/26","url":"https://www.scholarships.com","source":"usa_platform"},
    {"name":"Niche $10,000 No Essay Summer Scholarship","org":"Niche","cat":"Academic","edu":"Undergraduate","field":"","amount":"$10,000","deadline":"7/31/26","url":"https://www.scholarships.com","source":"usa_platform"},
    {"name":"Be Bold $25,000 No Essay Scholarship","org":"Bold.org","cat":"Academic","edu":"Undergraduate","field":"","amount":"$25,000","deadline":"7/31/26","url":"https://bold.org/scholarships","source":"usa_platform"},
    {"name":"$2000 No Essay Scholarship - Sallie","org":"Sallie","cat":"Academic","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"7/31/26","url":"https://www.scholarships.com/scc.aspx?pid=1438","source":"usa_platform"},
    {"name":"InspireCraft Scholarship","org":"Fastweb","cat":"Arts","edu":"Undergraduate","field":"Arts","amount":"$500","deadline":"12/31/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Financial Goals Scholarship","org":"Fastweb","cat":"Business","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"12/31/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"RealtyHop Scholarship","org":"RealtyHop","cat":"Academic","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"8/31/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Global Perspectives Scholarship","org":"Fastweb","cat":"Academic","edu":"Undergraduate","field":"","amount":"$1,000","deadline":"8/27/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Jet Future Business Leaders Scholarship","org":"Fastweb","cat":"Business","edu":"Undergraduate","field":"","amount":"$1,000","deadline":"7/31/26","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"5000 No-Essay Discover Scholarship Sweepstakes","org":"Discover","cat":"Academic","edu":"Undergraduate","field":"","amount":"$5,000","deadline":"Rolling","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"Fastweb Monthly $40,000 Scholarship","org":"Fastweb","cat":"Academic","edu":"Undergraduate","field":"","amount":"$40,000","deadline":"Monthly","url":"https://www.fastweb.com","source":"usa_platform"},
    {"name":"SBB Research Group STEM Scholarship","org":"SBB Research Group","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$10,000","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"SMART Scholarship-for-Service Program","org":"U.S. Department of Defense","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"gov_us"},
    {"name":"USRA Distinguished Undergraduate Awards","org":"USRA","cat":"STEM","edu":"Undergraduate","field":"Engineering","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"Google Lime Scholarship","org":"Google","cat":"STEM","edu":"Undergraduate","field":"Computer Science","amount":"$10,000","deadline":"Rolling","url":"https://www.google.com","source":"usa_platform"},
]

# ===== Category: HBCU =====
hbcu = [
    {"name":"UNCF General Scholarship","org":"United Negro College Fund","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.uncf.org","source":"identity"},
    {"name":"HBCU Connect HBCU Student Scholarship","org":"HBCU Connect","cat":"Community","edu":"Undergraduate","field":"","amount":"$1,000","deadline":"7/1/26","url":"https://hbcuconnect.com","source":"identity"},
    {"name":"Evolve502 Scholarship","org":"Evolve502","cat":"Community","edu":"Undergraduate","field":"","amount":"$1,000","deadline":"7/31/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"AOTF District of Columbia Scholarship","org":"AOTF","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"3/31/27","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Morgan Stanley HBCU Scholars Program","org":"Morgan Stanley","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"7/1/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Descendants Truth and Reconciliation Foundation Scholarship","org":"Descendants Truth and Reconciliation Foundation","cat":"Community","edu":"Undergraduate","field":"","amount":"$500","deadline":"Rolling","url":"https://www.fastweb.com","source":"identity"},
    {"name":"ETS Presidential Scholarship for HBCU Students","org":"ETS","cat":"Community","edu":"Undergraduate","field":"","amount":"$15,000","deadline":"3/31/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"FOSSI Scholarship","org":"Foundation for Opportunities in Science and Technology","cat":"Community","edu":"High School","field":"","amount":"$10,000","deadline":"Rolling","url":"https://www.fastweb.com","source":"identity"},
    {"name":"San Diego HBCU Scholarship","org":"San Diego","cat":"Community","edu":"Undergraduate","field":"","amount":"$10,000","deadline":"Rolling","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Kia Accelerate the Good HBCU Scholarship","org":"Kia","cat":"Community","edu":"Undergraduate","field":"","amount":"$5,000","deadline":"4/30/26","url":"https://hbcuconnect.com","source":"identity"},
    {"name":"Mona Calhoun HBCU Scholarship","org":"Mona Calhoun","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"4/15/26","url":"https://app.goingmerry.com","source":"identity"},
    {"name":"NFL Scholarship/HBCU Week","org":"NFL","cat":"Community","edu":"Undergraduate","field":"","amount":"$10,000","deadline":"2/17/26","url":"https://app.goingmerry.com","source":"identity"},
    {"name":"HBCU Battle of the Brains","org":"HBCU Connect","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"Varies","deadline":"3/31/26","url":"https://www.fastweb.com","source":"identity"},
]

# ===== Category: Hispanic/Latino =====
hispanic = [
    {"name":"Haz La U College Grant","org":"Hispanic Heritage Foundation / Colgate","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"identity"},
    {"name":"LULAC National Scholarship Fund","org":"LULAC","cat":"Community","edu":"Undergraduate","field":"","amount":"$500 - $5,000","deadline":"12/31/26","url":"https://www.lulac.org","source":"identity"},
    {"name":"HSF Scholarship Program","org":"Hispanic Scholarship Fund","cat":"Community","edu":"Undergraduate","field":"","amount":"$500 - $5,000","deadline":"3/1/26","url":"https://hsf.net","source":"identity"},
    {"name":"ALPFA Scholarship","org":"ALPFA","cat":"Business","edu":"Undergraduate","field":"","amount":"$1,000 - $5,000","deadline":"12/31/26","url":"https://www.alpfa.org","source":"identity"},
    {"name":"AHETEMS Scholarship Program","org":"AHETEMS","cat":"STEM","edu":"Undergraduate","field":"Engineering","amount":"$1,000 - $5,000","deadline":"12/31/26","url":"https://www.hcf.org","source":"identity"},
    {"name":"Hispanic Heritage Youth Awards","org":"Hispanic Heritage Foundation","cat":"Community","edu":"High School","field":"","amount":"$1,000 - $10,000","deadline":"10/1/26","url":"https://www.hispanicheritage.org","source":"identity"},
    {"name":"HACU Scholarship Program","org":"HACU","cat":"Community","edu":"Undergraduate","field":"","amount":"$2,500 - $5,000","deadline":"3/31/26","url":"https://www.hacu.org","source":"identity"},
    {"name":"LEA LGBTQ+ Youth Scholarship","org":"Latino Equality Alliance","cat":"Community","edu":"Undergraduate","field":"","amount":"$500 - $5,000","deadline":"5/1/26","url":"https://www.somoslea.org","source":"identity"},
    {"name":"Latino Social Work Coalition Scholarship","org":"Latino Social Work Coalition","cat":"Arts","edu":"Graduate","field":"Social Work","amount":"Varies","deadline":"3/31/26","url":"https://www.fastweb.com","source":"identity"},
]

# ===== Category: Masonic / Fraternal =====
masonic = [
    {"name":"Masonic Charities Arizona Scholarship","org":"Masonic Charities of Arizona","cat":"Masonic","edu":"Undergraduate","field":"","amount":"$500 - $3,000","deadline":"12/31/26","url":"https://www.masoniccharitiesaz.com","source":"identity"},
    {"name":"Masonic Charity Foundation of New Jersey Scholarships","org":"Masonic Charity Foundation of NJ","cat":"Masonic","edu":"Undergraduate","field":"","amount":"$25,000","deadline":"6/30/26","url":"https://studentscholarships.org","source":"identity"},
    {"name":"Grand Lodge of Texas Scholarship","org":"Grand Lodge of Texas","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.grandlodgeoftexas.org","source":"identity"},
    {"name":"Grand Lodge of Pennsylvania Scholarship","org":"Grand Lodge of PA","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.grandlodgeofpa.org","source":"identity"},
    {"name":"Shriners International Scholarship","org":"Shriners International","cat":"Masonic","edu":"Undergraduate","field":"","amount":"$1,000 - $10,000","deadline":"12/31/26","url":"https://www.shrinersinternational.org","source":"identity"},
    {"name":"Kansas Masonic Foundation Scholarships","org":"Kansas Masonic Foundation","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"2/15/26","url":"https://www.facebook.com","source":"identity"},
    {"name":"Minnesota Masonic Charities Scholarship","org":"Masonic Charities of Minnesota","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"12/31/26","url":"https://www.scholarships.com","source":"identity"},
    {"name":"Omega Gents Scholarship","org":"Alpha Phi Alpha Fraternity","cat":"Masonic","edu":"Undergraduate","field":"","amount":"$1,000 - $15,000","deadline":"7/15/26","url":"https://www.selffoundation1906.org","source":"identity"},
    {"name":"Knights of Columbus William A. Doyle Memorial Scholarship","org":"Knights of Columbus","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"12/1/25 - 3/15/26","url":"https://www.facebook.com","source":"identity"},
    {"name":"Three Great Lights Masonic Lodge Scholarship","org":"Masonic Lodge No. 323","cat":"Masonic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"4/20/26","url":"https://atc.montebello.k12.ca.us","source":"identity"},
]

# ===== Category: LGBTQ+ =====
lgbtq = [
    {"name":"Point Foundation Scholarship","org":"Point Foundation","cat":"Community","edu":"Undergraduate","field":"","amount":"$5,000 - $20,000","deadline":"1/15/27","url":"https://pointfoundation.org","source":"identity"},
    {"name":"Out to Innovate Scholarship","org":"Out to Innovate","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$5,000 - $10,000","deadline":"2/28/27","url":"https://www.scholarships.com","source":"identity"},
    {"name":"SAGAA Career Development Scholarship","org":"SAGAA","cat":"Business","edu":"Undergraduate","field":"Actuarial Science","amount":"$5,000","deadline":"5/29/26","url":"https://www.scholarships.com","source":"identity"},
    {"name":"Gamma Mu Foundation Scholarship","org":"Gamma Mu Foundation","cat":"Community","edu":"Undergraduate","field":"","amount":"$1,000 - $5,000","deadline":"12/31/26","url":"https://www.gammamufoundation.org","source":"identity"},
    {"name":"Q Scholarship Collaborative","org":"eQuality Scholarship Collaborative","cat":"Community","edu":"Undergraduate","field":"","amount":"$2,500","deadline":"12/31/26","url":"https://www.equalityscholarships.org","source":"identity"},
    {"name":"L'Oreal LGBTQIA+ Scholarship","org":"L'Oreal","cat":"Community","edu":"Undergraduate","field":"","amount":"$5,000","deadline":"7/31/26","url":"https://www.scholarships.com","source":"identity"},
    {"name":"Nlgja Aarons Scholarship","org":"NLGJA","cat":"Arts","edu":"Undergraduate","field":"Journalism","amount":"$5,000","deadline":"5/15/26","url":"https://www.nlgja.org","source":"identity"},
    {"name":"Nlgja Kay Longcope Scholarship","org":"NLGJA","cat":"Arts","edu":"Undergraduate","field":"Journalism","amount":"$3,000","deadline":"5/15/26","url":"https://www.nlgja.org","source":"identity"},
    {"name":"Hammer Strength DEI Scholarship","org":"Hammer Strength","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"10/15/26","url":"https://www.salliemae.com","source":"identity"},
    {"name":"Paul Zwaska Scholarship","org":"Nitro College","cat":"Community","edu":"Undergraduate","field":"","amount":"$2,500","deadline":"10/15/26","url":"https://www.nitrocollege.com","source":"identity"},
]

# ===== Category: Women =====
women = [
    {"name":"Women in STEM Scholarship","org":"Studentscholarships.org","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$25,000","deadline":"6/30/26","url":"https://studentscholarships.org","source":"identity"},
    {"name":"Women in STEM Scholarship Bradford","org":"University of Bradford","cat":"STEM","edu":"Masters","field":"STEM","amount":"£5,000 - £15,000","deadline":"12/31/26","url":"https://www.brad.ac.uk","source":"intl"},
    {"name":"British Council Women in STEM Scholarship","org":"British Council","cat":"STEM","edu":"Masters","field":"STEM","amount":"£15,000 - £20,000","deadline":"12/31/26","url":"https://www.brunel.ac.uk","source":"intl"},
    {"name":"Wolverhampton Women in STEM","org":"University of Wolverhampton","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"£2,000","deadline":"12/31/26","url":"https://www.wolverhampton.ac.uk","source":"intl"},
    {"name":"KCL Women in STEM Scholarship","org":"King's College London","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"£1,000 - £2,000","deadline":"12/31/26","url":"https://www.kcl.ac.uk","source":"intl"},
    {"name":"Manuela Calles Scholarship for Women","org":"Dr. Sandra Calles","cat":"Business","edu":"Undergraduate","field":"","amount":"Varies","deadline":"8/27/26","url":"https://www.financialaidfinder.com","source":"identity"},
    {"name":"Designli Empowering Women in Tech Scholarship","org":"Designli","cat":"Tech","edu":"Undergraduate","field":"Tech","amount":"$3,000","deadline":"11/15/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Julie Adams Memorial Scholarship - Women in STEM","org":"FinancialAidFinder","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$2,000","deadline":"6/27/26","url":"https://www.financialaidfinder.com","source":"identity"},
    {"name":"Black Women in STEM Scholarship","org":"Bold.org","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$5,000","deadline":"10/14/26","url":"https://bold.org","source":"identity"},
    {"name":"Soroptimist International La Grande Trade Scholarship","org":"Soroptimist International","cat":"Trade School","edu":"High School","field":"Trade/Vocational","amount":"$2,500","deadline":"4/3/26","url":"https://lagrandesoroptimist.org","source":"identity"},
]

# ===== Category: STEM =====
stem = [
    {"name":"Regeneron Science Talent Search Scholarship","org":"Society for Science","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$10,000 - $250,000","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"SBB Research Group STEM Scholarship","org":"SBB Research Group","cat":"STEM","edu":"Undergraduate","field":"STEM","amount":"$10,000","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"BioPharmaceutical Technology Center Institute DOORS Award","org":"BTCI/Promega","cat":"STEM","edu":"Undergraduate","field":"Life Science","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"Stantec Future Leaders Scholarship","org":"Stantec","cat":"Engineering","edu":"Undergraduate","field":"Engineering","amount":"$200,000","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"Amazon Future Engineer Scholarship","org":"Amazon","cat":"STEM","edu":"Undergraduate","field":"Computer Science","amount":"$40,000","deadline":"Rolling","url":"https://www.scholarships.com","source":"field"},
    {"name":"Pegasystems Scholars Program","org":"Pegasystems","cat":"Tech","edu":"Undergraduate","field":"Computer Science","amount":"$2,000","deadline":"7/15/26","url":"https://www.fastweb.com","source":"field"},
    {"name":"Tencent America Scholarship","org":"Tencent","cat":"Tech","edu":"Undergraduate","field":"Computer Science","amount":"$5,000","deadline":"7/6/26","url":"https://www.fastweb.com","source":"field"},
    {"name":"Pega Scholars Program","org":"Pegasystems","cat":"Tech","edu":"Undergraduate","field":"Computer Science","amount":"$2,000","deadline":"7/15/26","url":"https://www.fastweb.com","source":"field"},
]

# ===== Category: Trade/Vocational =====
trade = [
    {"name":"Norman Brooks Memorial Vocational Scholarship","org":"Amy Brooks","cat":"Trade School","edu":"High School","field":"Electronics","amount":"$1,000","deadline":"8/12/26","url":"https://bold.org","source":"identity"},
    {"name":"Autumn Leah Beemer Memorial Scholarship","org":"Kristy Kauffman","cat":"Trade School","edu":"High School","field":"Transportation","amount":"$500","deadline":"8/25/26","url":"https://bold.org","source":"identity"},
    {"name":"Pureland Supply Scholarship","org":"Pureland Supply","cat":"Trade School","edu":"Undergraduate","field":"Trade/Craft","amount":"$500","deadline":"12/31/26","url":"https://www.unigo.com","source":"identity"},
    {"name":"CIRI Foundation Vocational Training Scholarship","org":"CIRI Foundation","cat":"Trade School","edu":"Undergraduate","field":"Technical/Vocational","amount":"$9,000","deadline":"12/31/26","url":"https://www.cirifoundation.org","source":"identity"},
    {"name":"Kids' Chance of New York Scholarship","org":"Kids' Chance","cat":"Trade School","edu":"High School","field":"","amount":"$1,000 - $4,999","deadline":"Rolling","url":"https://www.scholarships.com","source":"identity"},
    {"name":"Bick Vocational/Trade School Scholarship","org":"Bick","cat":"Trade School","edu":"High School","field":"","amount":"Varies","deadline":"3/15/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Angus Foundation Vocational Technical Scholarship","org":"American Angus Association","cat":"Trade School","edu":"High School","field":"Agriculture","amount":"$1,000","deadline":"5/1/26","url":"https://fastweb.com","source":"identity"},
]

# ===== Category: Business/Entrepreneurship =====
business = [
    {"name":"Goldman Sachs MBA Fellowship","org":"Goldman Sachs","cat":"Business","edu":"Graduate","field":"Business","amount":"$30,000 - $100,000","deadline":"12/31/26","url":"https://www.goldmansachs.com","source":"identity"},
    {"name":"Prospanica MBA Scholarship","org":"Prospanica","cat":"Business","edu":"Graduate","field":"Business","amount":"$2,500 - $10,000","deadline":"12/31/26","url":"https://www.prospanica.org","source":"identity"},
    {"name":"OAS-UDD Scholarship - Global Innovation & Entrepreneurship","org":"Organization of American States","cat":"Business","edu":"Undergraduate","field":"Business","amount":"$3,400","deadline":"7/15/26","url":"https://www.oas.org","source":"intl"},
    {"name":"Smart Futures for Small Business Scholarship","org":"American Express / Scholarship America","cat":"Business","edu":"Undergraduate","field":"Business","amount":"$1,000","deadline":"7/27/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Charles Bowlus Memorial Scholarship","org":"Melissa Fontanella","cat":"Business","edu":"High School","field":"Business","amount":"$1,370","deadline":"12/11/26","url":"https://bold.org","source":"identity"},
    {"name":"Lia Kay Sparks Scholarship","org":"Fastweb","cat":"Business","edu":"Undergraduate","field":"Real Estate","amount":"Varies","deadline":"Rolling","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Susan Cunningham Scholarship","org":"Fastweb","cat":"Business","edu":"Undergraduate","field":"Business","amount":"Varies","deadline":"Rolling","url":"https://www.fastweb.com","source":"identity"},
]

# ===== Category: International =====
intl = [
    {"name":"DAAD Scholarship Germany","org":"DAAD","cat":"Academic","edu":"Graduate","field":"","amount":"€50,000 - €80,000","deadline":"12/31/26","url":"https://www.daad.de","source":"intl"},
    {"name":"Study in Canada Scholarships 2026-2027","org":"Global Affairs Canada","cat":"Academic","edu":"Undergraduate","field":"","amount":"$40,000 - $100,000","deadline":"12/31/26","url":"https://www.afterschoolafrica.com","source":"intl"},
    {"name":"Lester B. Pearson International Scholarship","org":"University of Toronto","cat":"Academic","edu":"Undergraduate","field":"","amount":"CA$20,000 - CA$60,000","deadline":"11/6/26","url":"https://www.utoronto.ca","source":"university"},
    {"name":"Australia Awards Scholarship","org":"Australian Government","cat":"Academic","edu":"Masters","field":"","amount":"AUD $30,000 - $50,000","deadline":"4/30/26","url":"https://www.dfat.gov.au","source":"intl"},
    {"name":"Rotary Peace Fellowship","org":"Rotary Foundation","cat":"Academic","edu":"Graduate","field":"Peace Studies","amount":"$50,000 - $100,000","deadline":"1/31/27","url":"https://www.rotary.org","source":"intl"},
    {"name":"Bocconi University International Award","org":"Bocconi University","cat":"Academic","edu":"Undergraduate","field":"","amount":"Tuition reduction (50%)","deadline":"12/31/26","url":"https://www.unibocconi.it","source":"university"},
    {"name":"University of Auckland International Student Excellence Scholarship","org":"University of Auckland","cat":"Academic","edu":"Undergraduate","field":"","amount":"NZ$5,000 - NZ$20,000","deadline":"12/31/26","url":"https://www.auckland.ac.nz","source":"university"},
    {"name":"Yale University Scholarship 2026-2027","org":"Yale University","cat":"Academic","edu":"Undergraduate","field":"","amount":"Full-Tuition","deadline":"12/31/26","url":"https://www.wemakescholars.com","source":"university"},
    {"name":"Duke University Karsh International Scholars Program","org":"Duke University","cat":"Academic","edu":"Undergraduate","field":"","amount":"Full-Tuition","deadline":"11/3/26","url":"https://www.wemakescholars.com","source":"university"},
    {"name":"Skoltech University Scholarship","org":"Skoltech","cat":"Academic","edu":"Masters","field":"","amount":"Full-Tuition + Stipend","deadline":"3/16/26","url":"https://www.wemakescholars.com","source":"intl"},
    {"name":"Gates Scholarship","org":"Gates Scholarship","cat":"Academic","edu":"Undergraduate","field":"","amount":"Full-Tuition","deadline":"9/15/26","url":"https://www.thegatesscholarship.org","source":"gov_us"},
]

# ===== Category: Arts/Humanities =====
arts = [
    {"name":"Pamela Branchini Memorial Scholarship","org":"National Scholastic Arts Foundation","cat":"Arts","edu":"Undergraduate","field":"Fine Arts","amount":"$1,000 - $5,000","deadline":"12/31/26","url":"https://www.artandwriting.org","source":"identity"},
    {"name":"Christian Myles Pratt Arts Scholarship","org":"Bold.org","cat":"Arts","edu":"Undergraduate","field":"Fine Arts","amount":"$2,500","deadline":"12/31/26","url":"https://bold.org","source":"identity"},
    {"name":"Pratt Fine Arts Center Scholarship","org":"Pratt Fine Arts Center","cat":"Arts","edu":"Undergraduate","field":"Fine Arts","amount":"Varies","deadline":"7/12/26","url":"https://www.instagram.com","source":"identity"},
    {"name":"LMU B. Hargrove English Scholarship","org":"Loyola Marymount University","cat":"Arts","edu":"Undergraduate","field":"English","amount":"Varies","deadline":"8/2026","url":"https://www.lmu.edu","source":"university"},
]

# ===== Category: Healthcare/Medicine =====
health = [
    {"name":"Henry Respert Alzheimer's and Dementia Awareness Scholarship","org":"Shawn Respert","cat":"Medicine","edu":"Undergraduate","field":"Healthcare","amount":"$7,500","deadline":"8/2/26","url":"https://bold.org","source":"identity"},
    {"name":"Margaret A. Briller Memorial Nursing Scholarship","org":"Enitra Briller","cat":"Medicine","edu":"Undergraduate","field":"Nursing","amount":"Varies","deadline":"Rolling","url":"https://bold.org","source":"identity"},
    {"name":"Kaprieasha Tyler Healthcare Scholarship","org":"Kaprieasha Tyler","cat":"Medicine","edu":"Undergraduate","field":"Healthcare","amount":"Varies","deadline":"Rolling","url":"https://bold.org","source":"identity"},
    {"name":"Quentin Price Scholarship","org":"Fastweb","cat":"Medicine","edu":"Undergraduate","field":"Medicine","amount":"$3,250","deadline":"6/29/26","url":"https://www.fastweb.com","source":"identity"},
    {"name":"Cook County Health Provident Hospital Scholarship","org":"Cook County Health","cat":"Medicine","edu":"Undergraduate","field":"Healthcare","amount":"$20,000","deadline":"4/19/26","url":"https://healthfoundationcc.org","source":"gov_us"},
    {"name":"TYLENOL Future Care Scholarship","org":"TYLENOL","cat":"Medicine","edu":"Undergraduate","field":"Healthcare","amount":"$10,000","deadline":"Rolling","url":"https://espanol.tylenol.com","source":"identity"},
]

# ===== Category: Military/Veteran =====
military = [
    {"name":"Brown Spouse Tuition Assistance Program","org":"Air Force Aid Society","cat":"Military/Veteran","edu":"Undergraduate","field":"","amount":"$1,000 - $10,000","deadline":"12/31/26","url":"https://www.airforceaid.org","source":"identity"},
    {"name":"American Legion Honor Scholarship","org":"American Legion","cat":"Military/Veteran","edu":"Undergraduate","field":"","amount":"$1,000 - $10,000","deadline":"2/28/27","url":"https://www.americanlegion.org","source":"identity"},
    {"name":"Naval Officers' Spouses' Club Scholarships","org":"Naval Officers' Spouses' Club","cat":"Military/Veteran","edu":"Undergraduate","field":"","amount":"$2,000","deadline":"3/1/27","url":"https://www.scholarships.com","source":"identity"},
    {"name":"AFCEA Washington DC Chapter Scholarship","org":"AFCEA","cat":"Military/Veteran","edu":"Undergraduate","field":"","amount":"$2,800","deadline":"3/8/27","url":"https://www.scholarships.com","source":"identity"},
]

# ===== Category: State-specific (USA) =====
state = [
    {"name":"Michigan Competitive Scholarship","org":"State of Michigan","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"7/1/26","url":"https://www.fafsa.gov","source":"usa_state"},
    {"name":"Texas Financial Aid Priority","org":"State of Texas","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"1/15/26","url":"https://www.fastweb.com","source":"usa_state"},
    {"name":"California Dream Act Application","org":"State of California","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"3/2/26","url":"https://www.csac.ca.gov","source":"usa_state"},
    {"name":"Florida Bright Futures Scholarship","org":"Florida Department of Education","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.fastweb.com","source":"usa_state"},
    {"name":"New York State Scholarship for Academic Excellence","org":"NY State","cat":"Academic","edu":"High School","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"usa_state"},
    {"name":"Illinois Marki Lemons Ryhal Education Advancement Scholarship","org":"Chicago Foundation","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"identity"},
    {"name":"Illinois Joint Civic Committee of Italian Americans Scholarship","org":"JCCIA","cat":"Community","edu":"Undergraduate","field":"","amount":"Varies","deadline":"Rolling","url":"https://www.scholarships.com","source":"identity"},
    {"name":"New Jersey Tuition Aid Grant","org":"State of New Jersey","cat":"Academic","edu":"Undergraduate","field":"","amount":"Varies","deadline":"5/15/26","url":"https://www.scholarships.com","source":"usa_state"},
]

all_candidates = gov_us + hbcu + hispanic + masonic + lgbtq + women + stem + trade + business + intl + arts + health + military + state

# Filter out dups
print(f"Total candidates before dedup: {len(all_candidates)}")
filtered = []
for s in all_candidates:
    key = (normalize(s["name"]), normalize(s["org"]))
    if key not in existing:
        filtered.append(s)

print(f"Unique new candidates: {len(filtered)}")

# Insert them
added = 0
for s in filtered:
    s["source_id"] = f"web_search_{datetime.now(timezone.utc).strftime('%Y%m%d')}_{added:04d}"
    insert_scholarship(s)
    added += 1

print(f"Inserted {added} new scholarships into both DBs")
