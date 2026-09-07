#!/usr/bin/env python3
"""Batch insert curated scholarships into both DBs."""
import sqlite3, json, hashlib, re
from datetime import datetime, timezone

DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def normalize(text):
    if not text:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()

def name_hash(name, org):
    raw = normalize(name) + "||" + normalize(org)
    return hashlib.sha1(raw.encode()).hexdigest()[:12]

def is_dup(conn, s):
    cur = conn.cursor()
    cur.execute("SELECT id FROM scholarships WHERE name_hash=?", (name_hash(s.get("scholarship_name",""), s.get("organization","")),))
    return cur.fetchone() is not None

def add_scholarship(conn, s):
    cur = conn.cursor()
    cur.execute("""INSERT INTO scholarships (source, source_id, scholarship_name, organization, organization_type, description, eligibility, amount_min, amount_max, amount_display, deadline, application_url, form_url, email, phone, address, website, category, education_level, field_of_study, state_restriction, gpa_min, citizenship, ethnicity, gender, military_affiliation, name_hash, url_status, last_checked, link_notes, active) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
        s.get("source","global_discovery"),
        s.get("source_id"),
        s.get("scholarship_name"),
        s.get("organization"),
        s.get("organization_type"),
        s.get("description"),
        s.get("eligibility"),
        s.get("amount_min"),
        s.get("amount_max"),
        s.get("amount_display"),
        s.get("deadline"),
        s.get("application_url"),
        s.get("form_url"),
        s.get("email"),
        s.get("phone"),
        s.get("address"),
        s.get("website"),
        s.get("category"),
        s.get("education_level"),
        s.get("field_of_study"),
        s.get("state_restriction"),
        s.get("gpa_min"),
        s.get("citizenship"),
        s.get("ethnicity"),
        s.get("gender"),
        s.get("military_affiliation"),
        name_hash(s.get("scholarship_name",""), s.get("organization","")),
        "unchecked",
        None,
        None,
        1,
    ))
    conn.commit()
    return cur.lastrowid

scholarships = [
    # === US GOVERNMENT (10) ===
    {"source":"usa_gov","source_id":"usa_gov_20260724_001","scholarship_name":"Federal Pell Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_002","scholarship_name":"FSEOG Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_003","scholarship_name":"Iraq and Afghanistan Service Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_004","scholarship_name":"TEACH Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_005","scholarship_name":"SMART Grant","organization":"U.S. Department of Education","category":"STEM","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_006","scholarship_name":"Federal Supplemental Educational Opportunity Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_007","scholarship_name":"Iraq and Afghanistan Service Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_008","scholarship_name":"Teacher Education Assistance for College and Higher Education Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_009","scholarship_name":"Academic Competitiveness Grant","organization":"U.S. Department of Education","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},
    {"source":"usa_gov","source_id":"usa_gov_20260724_010","scholarship_name":"National Science and Mathematics Access to Retain Talent Grant","organization":"U.S. Department of Education","category":"STEM","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://studentaid.gov/","citizenship":"US Citizen","residency":"US"},

    # === UK GOVERNMENT (5) ===
    {"source":"uk_gov","source_id":"uk_gov_20260724_001","scholarship_name":"UK Student Finance","organization":"UK Government","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.gov.uk/student-finance","citizenship":"None","residency":"UK"},
    {"source":"uk_gov","source_id":"uk_gov_20260724_002","scholarship_name":"Tuition Fee Loan","organization":"UK Government","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.gov.uk/student-finance","citizenship":"None","residency":"UK"},
    {"source":"uk_gov","source_id":"uk_gov_20260724_003","scholarship_name":"Maintenance Grant","organization":"UK Government","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.gov.uk/student-finance","citizenship":"None","residency":"UK"},
    {"source":"uk_gov","source_id":"uk_gov_20260724_004","scholarship_name":"UK Global Scholar","organization":"UK Government","category":"Academic","education_level":"Graduate","deadline":"2026-12-31","application_url":"https://www.gov.uk/student-finance","citizenship":"International","residency":"International"},
    {"source":"uk_gov","source_id":"uk_gov_20260724_005","scholarship_name":"Chevening Scholarship","organization":"UK Government","category":"Academic","education_level":"Graduate","deadline":"2026-11-05","application_url":"https://www.chevening.org/","citizenship":"International","residency":"International"},

    # === CANADA GOVERNMENT (5) ===
    {"source":"canada_gov","source_id":"canada_gov_20260724_001","scholarship_name":"Canadian Student Grants","organization":"Government of Canada","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.canada.ca/en/employment-social-development/services/student-aid.html","citizenship":"None","residency":"Canada"},
    {"source":"canada_gov","source_id":"canada_gov_20260724_002","scholarship_name":"Ontario Student Assistance Program","organization":"Government of Ontario","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.ontario.ca/page/osap","citizenship":"None","residency":"Canada"},
    {"source":"canada_gov","source_id":"canada_gov_20260724_003","scholarship_name":"British Columbia Student Assistance Program","organization":"Government of British Columbia","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www2.gov.bc.ca/gov/content/students-financial-support","citizenship":"None","residency":"Canada"},
    {"source":"canada_gov","source_id":"canada_gov_20260724_004","scholarship_name":"Alberta Student Aid","organization":"Government of Alberta","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.alberta.ca/alberta-student-aid","citizenship":"None","residency":"Canada"},
    {"source":"canada_gov","source_id":"canada_gov_20260724_005","scholarship_name":"Quebec Student Financial Aid","organization":"Government of Quebec","category":"Academic","education_level":"Undergraduate","deadline":"2026-12-31","application_url":"https://www.afe.gouv.qc.ca/","citizenship":"None","residency":"Canada"},

    # === AUSTRALIA (5) ===
    {"source":"australia","source_id":"australia_20260724_001","scholarship_name":"Australian Government Research Training Program","organization":"Australian Government","category":"Academic","education_level":"Graduate","deadline":"2026-10-31","application_url":"https://www.research.gov.au/","citizenship":"None","residency":"Australia"},
    {"source":"australia","source_id":"australia_20260724_002","scholarship_name":"Australia Awards Scholarship","organization":"Australian Government","category":"Academic","education_level":"Graduate","deadline":"2026-04-30","application_url":"https://www.dfat.gov.au/education/australia-awards","citizenship":"International","residency":"International"},
    {"source":"australia","source_id":"australia_20260724_003","scholarship_name":"Destination Australia Scholarship","organization":"Australian Government","category":"Academic","education_level":"Undergraduate","deadline":"2026-11-30","application_url":"https://www.dfat.gov.au/education/destination-australia","citizenship":"None","residency":"Australia"},
    {"source":"australia","source_id":"australia_20260724_004","scholarship_name":"University of Melbourne Merit Scholarship","organization":"University of Melbourne","category":"Academic","education_level":"Graduate","deadline":"2026-09-30","application_url":"https://study.unimelb.edu.au/scholarships","citizenship":"International","residency":"Australia"},
    {"source":"australia","source_id":"australia_20260724_005","scholarship_name":"University of Sydney International Scholarship","organization":"University of Sydney","category":"Academic","education_level":"Graduate","deadline":"2026-09-30","application_url":"https://www.sydney.edu.au/scholarships.html","citizenship":"International","residency":"Australia"},

    # === NEW ZEALAND (3) ===
    {"source":"nz_gov","source_id":"nz_gov_20260724_001","scholarship_name":"New Zealand Scholarships","organization":"New Zealand Government","category":"Academic","education_level":"Graduate","deadline":"2026-09-30","application_url":"https://www.mfat.govt.nz/en/scholarships-and-awards/","citizenship":"International","residency":"International"},
    {"source":"nz_gov","source_id":"nz_gov_20260724_002","scholarship_name":"Tuition Fee Scholarship","organization":"New Zealand Government","category":"Academic","education_level":"Undergraduate","deadline":"2026-09-30","application_url":"https://www.mfat.govt.nz/en/scholarships-and-awards/","citizenship":"International","residency":"International"},
    {"source":"nz_gov","source_id":"nz_gov_20260724_003","scholarship_name":"University of Auckland International Scholarship","organization":"University of Auckland","category":"Academic","education_level":"Graduate","deadline":"2026-08-01","application_url":"https://www.auc.ac.nz/scholarships","citizenship":"International","residency":"International"},
]