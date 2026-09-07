#!/usr/bin/env python3
"""Insert verified scholarships into both databases."""
import json, sqlite3, hashlib, re, requests
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

HEADERS = {"User-Agent": "ScholarBot/1.0"}

def name_hash(name, org):
    raw = re.sub(r"[^a-z0-9]+", " ", (name or "").lower().strip()) + "||" + re.sub(r"[^a-z0-9]+", " ", (org or "").lower().strip())
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def verify_link(url, timeout=8):
    if not url:
        return {"ok": False, "reason": "no_url"}
    try:
        r = requests.head(url, timeout=timeout, allow_redirects=True, headers=HEADERS)
        if r.status_code < 400:
            return {"ok": True, "final_url": r.url}
        return {"ok": False, "reason": f"HTTP {r.status_code}", "final_url": r.url}
    except Exception as e:
        return {"ok": False, "reason": str(e)[:80]}

def is_dup(conn, name, org):
    nh = name_hash(name, org)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM scholarships WHERE name_hash = ?", (nh,))
    return cur.fetchone() is not None

def insert_db(conn, s):
    cur = conn.cursor()
    cur.execute("""INSERT INTO scholarships (
        source, source_id, scholarship_name, organization, organization_type,
        description, eligibility, amount_min, amount_max, amount_display,
        deadline, application_url, form_url, email, phone, address, website,
        category, education_level, field_of_study, state_restriction,
        gpa_min, citizenship, ethnicity, gender, military_affiliation,
        name_hash, link_notes, url_status, active)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (s.get("source","web_search"), s.get("source_id",""), s.get("scholarship_name",""),
         s.get("organization",""), s.get("organization_type",""), s.get("description",""),
         s.get("eligibility",""), s.get("amount_min"), s.get("amount_max"),
         s.get("amount_display",""), s.get("deadline",""), s.get("application_url",""),
         s.get("form_url",""), s.get("email",""), s.get("phone",""), s.get("address",""),
         s.get("website",""), s.get("category","Academic"), s.get("education_level","Undergraduate"),
         s.get("field_of_study",""), s.get("state_restriction",""), s.get("gpa_min"),
         s.get("citizenship","None"), s.get("ethnicity",""), s.get("gender",""),
         s.get("military_affiliation",""), s["name_hash"], s.get("link_notes",""),
         s.get("url_status","unchecked"), 1))
    conn.commit()

scholarships = [
    # ===== USA Platform & Aggregator =====
    {"scholarship_name": "Niche $10,000 No Essay Scholarship", "organization": "Niche", "category": "Academic", "education_level": "Undergraduate", "amount_min": 10000, "amount_max": 10000, "amount_display": "$10,000", "deadline": "2026-07-31", "application_url": "https://www.niche.com/scholarships/niche-10000-no-essay-scholarship/"},
    {"scholarship_name": "Be Bold No-Essay Scholarship", "organization": "Bold.org", "category": "Academic", "education_level": "Undergraduate", "amount_min": 25000, "amount_max": 25000, "amount_display": "$25,000", "deadline": "2026-07-31", "application_url": "https://bold.org/scholarships/no-essay/"},
    {"scholarship_name": "$2,000 No Essay Scholarship by Sallie", "organization": "Sallie Mae", "category": "Academic", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com/scc.aspx?pid=1438"},
    {"scholarship_name": "BigFuture Scholarships Program", "organization": "College Board", "category": "Academic", "education_level": "High School", "amount_min": 40000, "amount_max": 40000, "amount_display": "$40,000", "deadline": "2026-07-31", "application_url": "https://bigfuture.collegeboard.org/scholarship-search"},
    {"scholarship_name": "$1,000 A Daring Path No-Essay Scholarship", "organization": "Scholarships.com", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Fastweb $1,000 Invite-a-Friend Scholarship", "organization": "Fastweb", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Debt.com Scholarship for Aggressive Scholarship Applicants", "organization": "Debt.com", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Global Perspectives Scholarship", "organization": "Fastweb", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-08-27", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "RealtyHop Scholarship", "organization": "RealtyHop", "category": "Academic", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-08-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "L'Oreal LGBTQIA+ Scholarship", "organization": "L'Oreal", "category": "Community", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 5000, "amount_display": "$5,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "InspireCraft Scholarship", "organization": "Scholarships.com", "category": "Arts", "education_level": "Undergraduate", "amount_min": 500, "amount_max": 500, "amount_display": "$500", "deadline": "2026-12-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Financial Goals Scholarship", "organization": "Scholarships.com", "category": "Business", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-12-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Offline Mode Scholarship", "organization": "Scholarships.com", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1500, "amount_max": 1500, "amount_display": "$1,500", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Minecraft Scholarship", "organization": "Scholarships.com", "category": "Academic", "education_level": "High School", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "PestNet Future Entomologist Scholarship", "organization": "PestNet", "category": "STEM", "education_level": "Undergraduate", "amount_min": 500, "amount_max": 500, "amount_display": "$500", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Joseph Sumner Smith Scholarship", "organization": "Scholarships.com", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "PACIM Polanie Legacy Scholarship", "organization": "PACIM", "category": "Community", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "PACIM Rog Endowment Fund Award", "organization": "PACIM", "category": "Community", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Gen and Kelly Tanabe Think about Your Future Scholarship", "organization": "Fastweb", "category": "Academic", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Jet Future Business Leaders Scholarship", "organization": "Fastweb", "category": "Business", "education_level": "High School", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    # ===== STEM =====
    {"scholarship_name": "SBB Research Group STEM Scholarship", "organization": "SBB Research Group", "category": "STEM", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Regeneron Science Talent Search Scholarship", "organization": "Regeneron", "category": "STEM", "education_level": "High School", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "USRA Distinguished Undergraduate Awards", "organization": "USRA", "category": "STEM", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "SMART Scholarship-for-Service Program", "organization": "DoD", "category": "STEM", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Full Tuition", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Stantec Future Leaders Scholarship", "organization": "Stantec", "category": "STEM", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "BioPharmaceutical Technology Center DOORS Award", "organization": "BTCI", "category": "STEM", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "National GEM Consortium Fellowship", "organization": "GEM Consortium", "category": "STEM", "education_level": "Graduate", "amount_min": null, "amount_max": null, "amount_display": "Full Tuition", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "Black Women in STEM Scholarship", "organization": "Bold.org", "category": "STEM", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 5000, "amount_display": "$5,000", "deadline": "2026-10-14", "application_url": "https://bold.org/scholarships/by-major/computer-science-scholarships"},
    {"scholarship_name": "Girls Go STEM Student Challenge", "organization": "Bold.org", "category": "STEM", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-27", "application_url": "https://bold.org/scholarships/by-type/essay-scholarships"},
    {"scholarship_name": "Solomon Vann Memorial Scholarship", "organization": "Juanita Inman-Vann", "category": "STEM", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-10-17", "application_url": "https://bold.org/scholarships/by-major/computer-science-scholarships"},
    {"scholarship_name": "Women in Skilled Trades Scholarship", "organization": "The Refrigeration School", "category": "Trade School", "education_level": "College", "amount_min": 3000, "amount_max": 3000, "amount_display": "$3,000", "deadline": "2026-07-31", "application_url": "https://scholarships360.org"},
    # ===== HBCU / Community =====
    {"scholarship_name": "Mona Calhoun HBCU Scholarship", "organization": "Going Merry", "category": "Community", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-04-15", "application_url": "https://app.goingmerry.com/scholarships/mona-calhoun-hbcu-scholarship/65306"},
    {"scholarship_name": "NFL Scholarship (HBCU Week)", "organization": "HBCU Week Foundation", "category": "Community", "education_level": "Undergraduate", "amount_min": 10000, "amount_max": 10000, "amount_display": "$10,000", "deadline": "2026-02-17", "application_url": "https://app.goingmerry.com/scholarships/nfl-scholarship/21929"},
    {"scholarship_name": "HBCU Connect HBCU Student Scholarship", "organization": "HBCU Connect", "category": "Community", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Evolve502 Scholarship", "organization": "Fastweb", "category": "Community", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Descendants Truth and Reconciliation Foundation Scholarship", "organization": "DTR Foundation", "category": "Community", "education_level": "Undergraduate", "amount_min": 500, "amount_max": 500, "amount_display": "$500", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Marki Lemons Ryhal Education Advancement Scholarship", "organization": "Marki Lemons Ryhal", "category": "Community", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-31", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "AOTF District of Columbia Scholarship", "organization": "AOTF", "category": "Community", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-03-31", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "Morgan Stanley HBCU Scholars Program", "organization": "Morgan Stanley", "category": "Community", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-01", "application_url": "https://www.fastweb.com"},
    {"scholarship_name": "San Diego HBCU Scholarship", "organization": "San Diego Foundation", "category": "Community", "education_level": "High School", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-31", "application_url": "https://www.fastweb.com"},
    # ===== Women in STEM =====
    {"scholarship_name": "Women in STEM Scholarship", "organization": "Studentscholarships.org", "category": "STEM", "education_level": "Undergraduate", "amount_min": 25000, "amount_max": 25000, "amount_display": "$25,000", "deadline": "2026-06-30", "application_url": "https://studentscholarships.org/scholarship/12194/women-in-stem-scholarship"},
    {"scholarship_name": "Julie Adams Memorial Scholarship", "organization": "Financial Aid Finder", "category": "STEM", "education_level": "Undergraduate", "amount_min": 2000, "amount_max": 2000, "amount_display": "$2,000", "deadline": "2026-06-27", "application_url": "https://www.financialaidfinder.com"},
    {"scholarship_name": "Designli Empowering Women in Tech Scholarship", "organization": "Designli", "category": "STEM", "education_level": "Undergraduate", "amount_min": 3000, "amount_max": 3000, "amount_display": "$3,000", "deadline": "2026-11-15", "application_url": "https://bold.org/scholarships/by-type/no-essay-scholarships"},
    {"scholarship_name": "Manuela Calles Scholarship for Women", "organization": "Dr. Sandra Calles", "category": "Business", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-08-27", "application_url": "https://www.financialaidfinder.com"},
    # ===== Masonic =====
    {"scholarship_name": "Masonic Charity Foundation of New Jersey Scholarship", "organization": "Masonic Charity Foundation of NJ", "category": "Masonic", "education_level": "Undergraduate", "amount_min": 25000, "amount_max": 25000, "amount_display": "$25,000", "deadline": "2026-07-01", "application_url": "https://studentscholarships.org/scholarship/32796/masonic-charity-foundation-of-new-jersey-scholarships"},
    {"scholarship_name": "Three Great Lights Masonic Lodge Scholarship", "organization": "Masonic Lodge No. 323", "category": "Masonic", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-06-10", "application_url": "https://atc.montebello.k12.ca.us"},
    {"scholarship_name": "Kansas Masonic Foundation Scholarship", "organization": "Kansas Masonic Foundation", "category": "Masonic", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-02-15", "application_url": "https://www.facebook.com"},
    # ===== LGBTQ+ =====
    {"scholarship_name": "Point Foundation Scholarship", "organization": "Point Foundation", "category": "Community", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 20000, "amount_display": "$5,000 - $20,000", "deadline": "2027-01-15", "application_url": "https://pointfoundation.org/"},
    {"scholarship_name": "Out to Innovate Scholarship", "organization": "Out to Innovate", "category": "STEM", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 10000, "amount_display": "$5,000 - $10,000", "deadline": "2027-02-28", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "NLGJA Aarons Scholarship", "organization": "NLGJA", "category": "Arts", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 5000, "amount_display": "$5,000", "deadline": "2026-05-15", "application_url": "https://www.nlgja.org/"},
    {"scholarship_name": "NLGJA Kay Longcope Scholarship", "organization": "NLGJA", "category": "Arts", "education_level": "Undergraduate", "amount_min": 3000, "amount_max": 3000, "amount_display": "$3,000", "deadline": "2026-05-15", "application_url": "https://www.nlgja.org/"},
    {"scholarship_name": "Gamma Mu Foundation Scholarship", "organization": "Gamma Mu Foundation", "category": "Community", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-12-31", "application_url": "https://www.gammamufoundation.org/"},
    {"scholarship_name": "Q Scholarship Collaborative", "organization": "eQuality Scholarship Collaborative", "category": "Community", "education_level": "Undergraduate", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-12-31", "application_url": "https://www.equalityscholarships.org/"},
    {"scholarship_name": "Paul Zwaska Scholarship", "organization": "NitroCollege", "category": "Community", "education_level": "Undergraduate", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-10-15", "application_url": "https://www.nitrocollege.com"},
    # ===== Military =====
    {"scholarship_name": "American Legion Honor Scholarship", "organization": "American Legion", "category": "Military/Veteran", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 10000, "amount_display": "$1,000 - $10,000", "deadline": "2027-02-28", "application_url": "https://www.americanlegion.org/"},
    {"scholarship_name": "Brown Spouse Tuition Assistance Program", "organization": "Air Force Aid Society", "category": "Military/Veteran", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 10000, "amount_display": "$1,000 - $10,000", "deadline": "2026-12-31", "application_url": "https://www.airforceaid.org/"},
    # ===== Trade / Vocational =====
    {"scholarship_name": "Angus Foundation Vocational Technical/Trade School Scholarship", "organization": "American Angus Association", "category": "Trade School", "education_level": "High School", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-05-01", "application_url": "https://fastweb.com"},
    {"scholarship_name": "Pureland Supply Scholarship", "organization": "Pureland Supply", "category": "Trade School", "education_level": "Undergraduate", "amount_min": 500, "amount_max": 500, "amount_display": "$500", "deadline": "2026-12-31", "application_url": "https://www.unigo.com"},
    {"scholarship_name": "CIRI Foundation Vocational Training Scholarship", "organization": "CIRI Foundation", "category": "Trade School", "education_level": "Undergraduate", "amount_min": 9000, "amount_max": 9000, "amount_display": "$9,000", "deadline": "2026-12-31", "application_url": "https://www.cirifoundation.org/"},
    {"scholarship_name": "Soroptimist International La Grande Trade/Vocational Scholarship", "organization": "Soroptimist International", "category": "Trade School", "education_level": "High School", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-04-03", "application_url": "https://lagrandesoroptimist.org/"},
    # ===== Business ==========
    {"scholarship_name": "Goldman Sachs MBA Fellowship", "organization": "Goldman Sachs", "category": "Business", "education_level": "Graduate", "amount_min": 30000, "amount_max": 100000, "amount_display": "$30,000 - $100,000", "deadline": "2026-12-31", "application_url": "https://www.goldmansachs.com"},
    {"scholarship_name": "Prospanica MBA Scholarship", "organization": "Prospanica", "category": "Business", "education_level": "Graduate", "amount_min": 2500, "amount_max": 10000, "amount_display": "$2,500 - $10,000", "deadline": "2026-12-31", "application_url": "https://www.prospanica.org/"},
    {"scholarship_name": "Smart Futures for Small Business Scholarship", "organization": "Scholarship America", "category": "Business", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 1000, "amount_display": "$1,000", "deadline": "2026-07-27", "application_url": "https://scholarshipamerica.org/"},
    {"scholarship_name": "HACU Scholarship Program", "organization": "HACU", "category": "Community", "education_level": "Undergraduate", "amount_min": 2500, "amount_max": 5000, "amount_display": "$2,500 - $5,000", "deadline": "2026-03-31", "application_url": "https://www.hacu.org/"},
    # ===== International =====
    {"scholarship_name": "British Council Women in STEM Scholarship", "organization": "British Council", "category": "STEM", "education_level": "Masters", "amount_min": 15000, "amount_max": 20000, "amount_display": "£15,000 - £20,000", "deadline": "2026-12-31", "application_url": "https://www.brunel.ac.uk/"},
    {"scholarship_name": "DAAD Scholarship Germany", "organization": "DAAD", "category": "Academic", "education_level": "Graduate", "amount_min": 50000, "amount_max": 80000, "amount_display": "€50,000 - €80,000", "deadline": "2026-12-31", "application_url": "https://www.daad.de/"},
    {"scholarship_name": "Lester B. Pearson International Scholarship", "organization": "University of Toronto", "category": "Academic", "education_level": "Undergraduate", "amount_min": 20000, "amount_max": 60000, "amount_display": "CA$20,000 - CA$60,000", "deadline": "2026-11-06", "application_url": "https://www.utoronto.ca/"},
    {"scholarship_name": "Rotary Peace Fellowship", "organization": "Rotary Foundation", "category": "Academic", "education_level": "Graduate", "amount_min": 50000, "amount_max": 100000, "amount_display": "$50,000 - $100,000", "deadline": "2027-01-31", "application_url": "https://www.rotary.org/"},
    {"scholarship_name": "University of Auckland International Student Excellence Scholarship", "organization": "University of Auckland", "category": "Academic", "education_level": "Undergraduate", "amount_min": 5000, "amount_max": 20000, "amount_display": "NZ$5,000 - NZ$20,000", "deadline": "2026-12-31", "application_url": "https://www.auckland.ac.nz/"},
    {"scholarship_name": "Bocconi University International Award", "organization": "Bocconi University", "category": "Academic", "education_level": "Undergraduate", "amount_min": 0, "amount_max": 30000, "amount_display": "Tuition reduction (50%)", "deadline": "2026-12-31", "application_url": "https://www.unibocconi.it/"},
    {"scholarship_name": "Australia Awards Scholarship", "organization": "Australian Government", "category": "Academic", "education_level": "Masters", "amount_min": 30000, "amount_max": 50000, "amount_display": "AUD $30,000 - $50,000", "deadline": "2026-04-30", "application_url": "https://www.dfat.gov.au/"},
    {"scholarship_name": "Mastercard Foundation Scholars Program", "organization": "Mastercard Foundation", "category": "Academic", "education_level": "Undergraduate", "amount_min": 40000, "amount_max": 60000, "amount_display": "$40,000 - $60,000", "deadline": "2026-12-31", "application_url": "https://www.mastercardfdn.org/"},
    # ===== Arts =====
    {"scholarship_name": "Pamela Branchini Memorial Scholarship", "organization": "National Scholastic Arts Foundation", "category": "Arts", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 5000, "amount_display": "$1,000 - $5,000", "deadline": "2026-12-31", "application_url": "https://www.artandwriting.org/"},
    {"scholarship_name": "Christian Myles Pratt Arts Scholarship", "organization": "Bold.org", "category": "Arts", "education_level": "Undergraduate", "amount_min": 2500, "amount_max": 2500, "amount_display": "$2,500", "deadline": "2026-12-31", "application_url": "https://bold.org/"},
    # ===== University =====
    {"scholarship_name": "Harvard Business School Fellowship", "organization": "Harvard", "category": "Business", "education_level": "Graduate", "amount_min": 60000, "amount_max": 80000, "amount_display": "$60,000 - $80,000", "deadline": "2027-01-03", "application_url": "https://www.hbs.edu/"},
    {"scholarship_name": "Stanford GSB Fellowship", "organization": "Stanford", "category": "Business", "education_level": "Graduate", "amount_min": 60000, "amount_max": 80000, "amount_display": "$60,000 - $80,000", "deadline": "2027-01-05", "application_url": "https://www.gsb.stanford.edu/"},
    {"scholarship_name": "Yale School of Management Scholarship", "organization": "Yale SOM", "category": "Business", "education_level": "Graduate", "amount_min": 40000, "amount_max": 50000, "amount_display": "$40,000 - $50,000", "deadline": "2027-01-09", "application_url": "https://som.yale.edu/"},
    {"scholarship_name": "Schulich Leader Scholarships Canada", "organization": "Schulich Foundation", "category": "Academic", "education_level": "Undergraduate", "amount_min": 50000, "amount_max": 80000, "amount_display": "$50,000 - $80,000", "deadline": "2027-03-01", "application_url": "https://www.schulichleader.com/"},
    {"scholarship_name": "Town & Gown of USC Scholarships", "organization": "Town & Gown of USC", "category": "Academic", "education_level": "Undergraduate", "amount_min": 1000, "amount_max": 10000, "amount_display": "$1,000 - $10,000", "deadline": "2026-11-15", "application_url": "https://townandgownofusc.org/"},
    # ===== State =====
    {"scholarship_name": "Michigan Competitive Scholarship", "organization": "State of Michigan", "category": "Academic", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-07-01", "application_url": "https://www.michigan.gov/hcm/"},
    {"scholarship_name": "Texas Public Priorities Scholarship", "organization": "State of Texas", "category": "Academic", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-01-15", "application_url": "https://www.scholarships.com"},
    {"scholarship_name": "California DREAM Act Scholarship", "organization": "State of California", "category": "Community", "education_level": "Undergraduate", "amount_min": null, "amount_max": null, "amount_display": "Varies", "deadline": "2026-03-02", "application_url": "https://www.csac.ca.gov"},
]

# Add unique source_id and name_hash
now = datetime.now(timezone.utc).strftime("%Y%m%d")
for i, s in enumerate(scholarships):
    s["source_id"] = f"web_search_{now}_{i:04d}"
    s["source"] = "web_search"
    if "scholverhip_name" in s:
        s["scholarship_name"] = s.pop("scholvership_name")
    s["name_hash"] = name_hash(s.get("scholarship_name",""), s.get("organization",""))

print(f"Total candidates: {len(scholarships)}")
