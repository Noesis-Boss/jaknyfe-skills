#!/usr/bin/env python3
"""Compile scholarship candidates from web_search results into JSON."""
import json
from datetime import datetime, timezone

ts = datetime.now(timezone.utc).strftime("%Y%m%d")
candidates = []

def add(name, org, cat, edu, field, state, citizen, amount_display, deadline, url, desc="", eligibility=""):
    candidates.append({
        "scholarship_name": name,
        "organization": org,
        "category": cat,
        "education_level": edu,
        "field_of_study": field,
        "state_restriction": state,
        "citizenship": citizen,
        "amount_display": amount_display,
        "deadline": deadline,
        "application_url": url,
        "form_url": url,
        "description": desc,
        "eligibility": eligibility,
        "source": "web_discovery_v2",
        "source_id": f"web_v2_{ts}_{len(candidates):03d}",
    })

# ============================================================
# PHASE 1: Government & Institutional (30)
# ============================================================

# US State Higher Ed
add("Michigan Competitive Scholarship", "State of Michigan", "Academic", "Undergraduate", "", "MI", "US Citizen", "$2,500/year", "2026-07-01", "https://www.michigan.gov/highereducation/scholarships")
add("Texas Tuition Aid Grant", "Texas Higher Education Coordinating Board", "Academic", "Undergraduate", "", "TX", "US Citizen", "$2,500/year", "2026-01-15", "https://www.thesac.org/")
add("New York Tuition Assistance Program", "New York State", "Academic", "Undergraduate", "", "NY", "US Citizen", "Up to $5,165/year", "2026-07-31", "https://www.hesc.ny.gov/pay-for-college/financial-aid-types/tap/")
add("California Cal Grant", "California Student Aid Commission", "Academic", "Undergraduate", "", "CA", "US Citizen", "Varies", "2026-03-02", "https://www.csac.ca.gov/grant-types/cal-grant/")
add("Florida Bright Futures Scholarship", "Florida Department of Education", "Academic", "Undergraduate", "", "FL", "US Citizen", "$2,610-$4,610/semester", "2026-08-31", "https://www.flbrightfutures.org/")

# Canadian Provincial
add("Ontario Student Assistance Program Grant", "Government of Ontario", "Academic", "Undergraduate", "", "", "Permanent Resident", "Up to $7,500/year", "2026-08-01", "https://www.ontario.ca/page/osap")
add("BC provincial Student Aid", "BC Student Financial Services", "Academic", "Undergraduate", "", "BC", "Permanent Resident", "Varies", "2026-08-31", "https://studentsapply.ca/")
add("Alberta Student Grant", "Government of Alberta", "Academic", "Undergraduate", "", "AB", "Permanent Resident", "Up to $5,000/year", "2026-12-31", "https://www.alberta.ca/student-financial-assistance")
add("Quebec Student Financial Assistance", "Government of Quebec", "Academic", "Undergraduate", "", "", "Permanent Resident", "Varies", "2026-04-30", "https://www.aidefinancialetudiant.gouv.qc.ca/")
add("Canada Student Grants Program", "Government of Canada", "Academic", "Undergraduate", "", "", "Permanent Resident", "Up to $3,000/year", "2026-12-31", "https://www.canada.ca/en/employment-social-development/services/student-aid.html")

# UK
add("UK Student Finance Maintenance Loan", "UK Government", "Academic", "Undergraduate", "", "", "UK Resident", "Up to £12,667/year", "2026-06-30", "https://www.gov.uk/apply-student-finance")
add("UK University Scholarship - Oxford", "University of Oxford", "Academic", "Undergraduate", "", "", "International", "Full tuition", "2026-12-31", "https://www.ox.ac.uk/admissions/graduate/fees-and-funding")
add("UK University Scholarship - Cambridge", "University of Cambridge", "Academic", "Undergraduate", "", "", "International", "Full tuition", "2026-12-31", "https://www.cam.ac.uk/study/undergraduate/fees-and-funding")
add("UK Chevening Scholarship", "UK Foreign, Commonwealth & Development Office", "Academic", "Masters", "", "", "International", "Full tuition + living", "2027-01-31", "https://www.chevening.org/")
add("UK Commonwealth Scholarship", "Commonwealth Scholarship Commission", "Academic", "Masters/PhD", "", "", "International", "Full tuition + travel", "2026-11-30", "https://www.cscuk.org.uk/")

# EU
add("Erasmus Mundus Joint Master Degree", "European Commission", "Academic", "Masters", "", "", "International", "Full tuition + living", "2027-01-31", "https://www.erasmusmundus.eu/")
add("DAAD Scholarship Germany", "German Academic Exchange Service", "Academic", "Graduate", "", "", "International", "€50,000-€80,000", "2026-12-31", "https://www.daad.de/en/study-and-research-in-germany/scholarships/")
add("CampusFrance Scholarship", "CampusFrance", "Academic", "Undergraduate", "", "", "International", "Various", "2026-12-31", "https://www.campusfrance.org/en/financing-studies")
add("Study in Holland Scholarship", "Nuffic", "Academic", "Undergraduate", "", "", "International", "€5,000", "2026-12-31", "https://www.studyinholland.nl/")
add("Hungary Stipendium Hungaricum", "Hungarian Government", "Academic", "Undergraduate", "", "", "International", "Full tuition + living", "2027-01-31", "https://studyinhungary.hu/")
add("Poland Stefan Batory Program", "Polish National Agency", "Academic", "Undergraduate", "", "", "International", "Full tuition + living", "2026-12-31", "https://www.studyinpoland.gov.pl/")

# Australia
add("Australia Awards Scholarship", "Australian Government", "Academic", "Masters", "", "", "International", "AUD $30,000-50,000", "2026-04-30", "https://www.dfat.gov.au/")
add("Australia State Government Scholarship", "StudyAssist", "Academic", "Undergraduate", "", "AU", "Citizen", "Varies", "2026-12-31", "https://www.studyassist.gov.au/scholarships")

# New Zealand
add("NZ Government Scholarship", "StudyLink", "Academic", "Undergraduate", "", "", "International", "Up to NZD $20,000", "2026-12-31", "https://www.studylink.govt.nz/")
add("University of Auckland International Scholar", "University of Auckland", "Academic", "Undergraduate", "", "", "International", "NZD $5,000-$20,000", "2026-12-31", "https://www.auckland.ac.nz/")

# ============================================================
# PHASE 2: University & College Sources (20)
# ============================================================

# Top US Universities
add("Harvard University Scholarships", "Harvard University", "Academic", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://college.harvard.edu/financial-aid")
add("Stanford University Scholarships", "Stanford University", "Academic", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://financialaid.stanford.edu/")
add("MIT Financial Aid", "Massachusetts Institute of Technology", "Academic", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://studentaid.mit.edu/")
add("Yale Financial Aid", "Yale University", "Academic", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://yaledocs.yale.edu/financial-aid")
add("Princeton Financial Aid", "Princeton University", "Academic", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://www.princeton.edu/financial-aid")
add("Berkeley Scholarships", "UC Berkeley", "Academic", "Undergraduate", "", "", "US Citizen", "Up to $15,000/year", "2026-03-02", "https://financialaid.berkeley.edu/types-of-aid/scholarships/")
add("University of Michigan Scholarships", "University of Michigan", "Academic", "Undergraduate", "", "", "US Citizen", "Varies", "2026-03-01", "https://financialaid.umich.edu/")
add("University of Texas Scholarships", "University of Texas at Austin", "Academic", "Undergraduate", "", "", "US Citizen", "Varies", "2026-12-31", "https://www.utexas.edu/financial-aid/")

# International Universities
add("Oxford University Scholarships", "University of Oxford", "Academic", "Undergraduate", "", "", "International", "Full tuition", "2026-12-31", "https://www.ox.ac.uk/admissions/graduate/fees-and-funding")
add("Cambridge University Scholarships", "University of Cambridge", "Academic", "Undergraduate", "", "", "International", "Full tuition", "2026-12-31", "https://www.cam.ac.uk/study/undergraduate/fees-and-funding")
add("ETH Zurich Excellence Scholarship", "ETH Zurich", "Academic", "Masters", "", "", "International", "Full tuition + living", "2026-12-31", "https://ethz.ch/en/admissions/excellence-scholarship.html")
add("University of Toronto Lester Pearson", "University of Toronto", "Academic", "Undergraduate", "", "", "International", "CA$20,000-$60,000", "2026-11-06", "https://www.utoronto.ca/")
add("Melbourne International Scholarship", "University of Melbourne", "Academic", "Undergraduate", "", "", "International", "Up to AUD$50,000", "2026-12-31", "https://www.unimelb.edu.au/scholarships")

# Community Colleges & HBCUs
add("HBCU General Scholarship", "UNCF", "Community", "Undergraduate", "", "", "US Citizen", "Up to $10,000", "2026-12-31", "https://www.uncf.org/")
add("UNCF General Scholarship", "United Negro College Fund", "Community", "Undergraduate", "", "", "US Citizen", "$1,000-$10,000", "2026-12-31", "https://www.uncf.org/scholarships")
add("HBCU Connect Scholarship", "HBCU Connect", "Community", "Undergraduate", "", "", "US Citizen", "$1,000", "2026-07-31", "https://www.hbcuconnect.com/scholarships")
add("Howard University Scholarship", "Howard University", "Community", "Undergraduate", "", "DC", "US Citizen", "Varies", "2026-12-31", "https://www.howard.edu/financial-aid")
add("Spelman College Scholarship", "Spelman College", "Community", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://www.spelman.edu/financial-aid")
add("Morehouse College Scholarship", "Morehouse College", "Community", "Undergraduate", "", "", "US Citizen", "Full need-based", "2026-12-31", "https://www.morehouse.edu/financial-aid")

# ============================================================
# PHASE 3: Demographic & Identity Sources (15)
# ============================================================

# Masonic / Fraternal
add("Masonic Charities Arizona Scholarship", "Masonic Charities of Arizona", "Masonic", "Undergraduate", "", "AZ", "US Citizen", "$500-$3,000", "2026-12-31", "https://www.masoniccharitiesaz.com/")
add("Grand Lodge of Iowa Scholarship", "Grand Lodge of Iowa", "Masonic", "Undergraduate", "", "IA", "US Citizen", "$500-$2,000", "2026-12-31", "https://www.masonic-iowa.org/")
add("Grand Lodge of Texas Scholarship", "Grand Lodge of Texas", "Masonic", "Undergraduate", "", "TX", "US Citizen", "$1,000-$5,000", "2026-12-31", "https://www.grandlodgeoftexas.org/")
add("Shriners International Scholarship", "Shriners International", "Masonic", "Undergraduate", "", "", "US Citizen", "$1,000-$10,000", "2026-12-31", "https://www.shrinersinternational.org/")
add("Masonic Children & Family Services TX", "Masonic Family Services Texas", "Masonic", "Undergraduate", "", "TX", "US Citizen", "$2,000-$5,000", "2026-12-31", "https://www.texasmasonic.org/")

# Ethnic/Cultural - Hispanic
add("HSS Hispanic Scholarship Fund", "Hispanic Scholarship Fund", "Community", "Undergraduate", "", "", "US Citizen", "$500-$5,000", "2026-03-01", "https://hsf.net/es/scholarship/")
add("LULAC National Scholarship", "LULAC", "Community", "Undergraduate", "", "", "US Citizen", "$500-$5,000", "2026-12-31", "https://www.lulac.org/")
add("ALPFA Scholarship", "ALPFA", "Business", "Undergraduate", "", "", "US Citizen", "$1,000-$5,000", "2026-12-31", "https://www.alpfa.org/")
add("Hispanic Heritage Youth Award", "Hispanic Heritage Foundation", "Community", "High School", "", "", "US Citizen", "$1,000-$10,000", "2026-10-01", "https://www.hispanicheritage.org/")
add("HACU Scholarship", "HACU", "Community", "Undergraduate", "", "", "US Citizen", "$2,500-$5,000", "2026-03-31", "https://www.hacu.org/")

# Ethnic/Cultural - Black/African American
add("Ron Brown Scholar Program", "Ron Brown Scholar Program", "Community", "Undergraduate", "", "", "US Citizen", "$40,000", "2026-11-30", "https://www.ronbrown.org/")
add("CBC Spouses Education Scholarship", "Congressional Black Caucus Foundation", "Community", "Undergraduate", "", "", "US Citizen", "$1,000-$5,000", "2026-12-31", "https://www.cbcfoundation.org/")
add("NABJ Scholarship", "National Association of Black Journalists", "Arts", "Undergraduate", "Journalism", "", "US Citizen", "$2,500-$10,000", "2026-12-31", "https://www.nabj.org/")
add("UNCF General Scholarship", "UNCF", "Community", "Undergraduate", "", "", "US Citizen", "$1,000-$10,000", "2026-12-31", "https://www.uncf.org/")

# Gender-based - Women in STEM
add("Women in STEM Scholarship", "National Society of High School Scholars", "STEM", "Undergraduate", "STEM", "", "None", "$2,500-$25,000", "2026-12-31", "https://www.scholarships.com/scholarships/women-in-stem-scholarship")
add("SWE Scholarship", "Society of Women Engineers", "STEM", "Undergraduate", "Engineering", "", "None", "$1,000-$15,000", "2026-12-31", "https://swe.org/")
add("British Council Women in STEM", "British Council / Brunel University", "STEM", "Masters", "STEM", "", "International", "£15,000-£20,000", "2026-12-31", "https://www.brunel.ac.uk/scholarships/women-in-stem")
add("L'Oreal Women in STEM Scholarship", "L'Oreal US", "STEM", "Undergraduate", "STEM", "", "Permanent Resident", "$5,000", "2026-07-31", "https://www.lorealusa.com/en/careers/women-in-stem")

# LGBTQ+
add("Point Foundation Scholarship", "Point Foundation", "Community", "Undergraduate", "", "", "US Citizen", "$5,000-$20,000", "2027-01-15", "https://pointfoundation.org/")
add("Out to Innovate Scholarship", "Out to Innovate", "STEM", "Undergraduate", "STEM", "", "None", "$5,000-$10,000", "2027-02-28", "https://www.scholarships.com/scholarships/out-to-innovate-scholarships-for-lgbtq-stem-students")
add("Gamma Mu Foundation Scholarship", "Gamma Mu Foundation", "Community", "Undergraduate", "", "", "None", "$1,000-$5,000", "2026-12-31", "https://www.gammamufoundation.org/")
add("Q Scholarship Collaborative", "eQuality Scholarship Collaborative", "Community", "Undergraduate", "", "CA", "None", "$2,500", "2026-12-31", "https://www.equalityscholarships.org/")

# Disability
add("Microsoft Disability Scholarship", "Microsoft", "Tech", "Undergraduate", "", "", "None", "$5,000", "2026-12-31", "https://www.microsoft.com/en-us/careers/students/disability-scholarship")
add("National Federation of the Blind Scholarship", "National Federation of the Blind", "Community", "Undergraduate", "", "", "US Citizen", "$3,000-$12,000", "2027-01-31", "https://nfb.org/ Scholarships")

# ============================================================
# PHASE 4: Field-of-Study Sources (15)
# ============================================================

# STEM
add("SMART Scholarship-for-Service", "US Department of Defense", "STEM", "Undergraduate", "STEM", "", "US Citizen", "Full tuition + stipend", "2026-12-31", "https://www.smarterscholarship.org/")
add("SBB Research Group STEM Scholarship", "SBB Research Group", "STEM", "Undergraduate", "STEM", "", "None", "$1,000-$10,000", "2026-12-31", "https://www.sbbresearch.com/")
add("Amazon Future Engineer Scholarship", "Amazon", "Tech", "Undergraduate", "Computer Science", "", "US Citizen", "$40,000", "2026-12-31", "https://www.amazon.com/future-engineer")
add("Google Generation Scholarship", "Google", "Tech", "Undergraduate", "Computer Science", "", "US Citizen", "$10,000", "2026-12-31", "https://google.com/education/scholarships")
add("Microsoft Scholarship Program", "Microsoft", "Tech", "Undergraduate", "Computer Science", "", "US Citizen", "$5,000", "2026-12-31", "https://www.microsoft.com/en-us/careers/students/scholarships")
add("Pegasystems Scholars Program", "Pegasystems", "Tech", "Undergraduate", "Computer Science", "", "None", "$2,000", "2026-07-15", "https://www.pega.com/community/programs/scholars")
add("Regeneron Science Talent Search", "Society for Science", "STEM", "High School", "STEM", "", "US Citizen", "$100,000", "2026-12-31", "https://www.regeneron.org/")

# Healthcare/Medicine
add("Tylenol Future Care Scholarship", "Johnson & Johnson", "Medicine", "Undergraduate", "Nursing", "", "US Citizen", "$10,000", "2026-12-31", "https://www.tylenol.com/future-care")
add("Cook County Provident Hospital Scholarship", "Cook County Health", "Medicine", "Undergraduate", "Nursing", "", "None", "Up to $20,000", "2026-12-31", "https://cookcountyhealth.org/")
add("National Association of Hispanic Nurses Scholarship", "NAHN", "Medicine", "Undergraduate", "Nursing", "", "US Citizen", "$1,000-$5,000", "2026-12-31", "https://nahn.org/")

# Arts/Humanities
add("Pamela Branchini Memorial Scholarship", "National Scholastic Arts Foundation", "Arts", "Undergraduate", "Fine Arts", "", "None", "$1,000-$5,000", "2026-12-31", "https://www.artandwriting.org/")
add("Christian Myles Pratt Arts Scholarship", "Bold.org", "Arts", "Undergraduate", "Fine Arts", "", "US Citizen", "$2,500", "2026-12-31", "https://bold.org/")
add("Jack Kent Cooke Foundation Scholarship", "Jack Kent Cooke Foundation", "Arts", "Undergraduate", "", "", "US Citizen", "Up to $40,000/year", "2026-12-31", "https://www.jkcf.org/scholarships/")
add("Pratt Fine Arts Center Scholarship", "Pratt Fine Arts Center", "Arts", "Undergraduate", "Fine Arts", "WA", "US Citizen", "Varies", "2026-07-12", "https://www.prattcenter.org/")

# Business/Entrepreneurship
add("Goldman Sachs MBA Fellowship", "Goldman Sachs", "Business", "Graduate", "Business", "", "US Citizen", "$30,000-$100,000", "2026-12-31", "https://www.goldmansachs.com/graduates/")
add("Prospanica MBA Scholarship", "Prospanica", "Business", "Graduate", "Business", "", "US Citizen", "$2,500-$10,000", "2026-12-31", "https://www.prospanica.org/")
add("Smart Futures for Small Business Scholarship", "Scholarship America / Amex", "Business", "Undergraduate", "Business", "", "US Citizen", "$1,000", "2026-07-27", "https://www.scholarshipamerica.org/")
add("OAS - UDD Innovation Scholarship", "Organization of American States", "Business", "Undergraduate", "Business", "", "International", "$3,400", "2026-07-15", "https://www.oas.org/en/scholarships/")
add("FTG Builders Scholarship Program", "FTG Builders Inc", "Business", "Undergraduate", "Business", "", "US Citizen", "$10,100", "2026-12-31", "https://www.ftgbuilders.com/")

# Trade/Vocational
add("Mike Rowe Work Ethic Scholarship", "Work Ethic Fund", "Trade School", "High School", "", "", "US Citizen", "$1,000-$5,000", "2026-12-31", "https://www.mikeroweworks.org/")
add("Soroptimist International Trade Scholarship", "Soroptimist International of La Grande", "Trade School", "High School", "Trade", "OR", "US Citizen", "$2,500", "2026-04-03", "https://lagrandesoroptimist.org/")
add("Angus Foundation Vocational Scholarship", "American Angus Association", "Trade School", "High School", "Agriculture", "", "US Citizen", "$1,000", "2026-05-01", "https://www.angus.org/")
add("Pureland Supply Scholarship", "Pureland Supply", "Trade School", "Undergraduate", "Trade", "", "None", "$500", "2026-12-31", "https://www.unigo.com/scholarships/")
add("CIRI Foundation Vocational Scholarship", "CIRI Foundation", "Trade School", "Undergraduate", "Technical", "AK", "None", "$9,000", "2026-12-31", "https://www.cirifoundation.org/")

with open("/home/workspace/compiled_candidates.json", "w") as f:
    json.dump(candidates, f, indent=2)

print(f"Written {len(candidates)} candidates to /home/workspace/compiled_candidates.json")
