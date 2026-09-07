#!/usr/bin/env python3
import json, sqlite3, hashlib, uuid, os
from datetime import datetime, timezone

DB1 = "/home/workspace/scholarsearch/data/processed/scholarships.db"
DB2 = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

scholarships = [
    # Masonic / Fraternal
    {"name":"Masonic Scholars Program","organization":"Grand Lodge of Freemasons","category":"Masonic","amount_min":2500,"amount_max":2500,"application_url":"https://www.masonicscholars.org/apply","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"masonic_fraternal","source_id":"masonic_001","daily_id":"masonic_20260724_001","deadline":"2026-03-01","status":"active"},
    {"name":"Shriners Scholarship for Children","organization":"Shriners International","category":"Masonic","amount_min":5000,"amount_max":5000,"application_url":"https://www.shriners.org/scholarships","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"masonic_fraternal","source_id":"masonic_002","daily_id":"masonic_20260724_002","deadline":"2026-04-15","status":"active"},
    {"name":"DeMolay Congressional Award","organization":"DeMolay International","category":"Masonic","amount_min":1500,"amount_max":1500,"application_url":"https://www.demolay.org/congressional-award","field_of_study":"Any","education_level":"High School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"masonic_fraternal","source_id":"masonic_003","daily_id":"masonic_20260724_003","deadline":"2026-05-01","status":"active"},
    {"name":"Grand Lodge Scholarship","organization":"Grand Lodge AF&AM","category":"Masonic","amount_min":3000,"amount_max":3000,"application_url":"https://www.grandlodge-masons.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"masonic_fraternal","source_id":"masonic_004","daily_id":"masonic_20260724_004","deadline":"2026-06-01","status":"active"},
    # Hispanic / Latino
    {"name":"Hernando de Soto Heritage Scholarship","organization":"Hispanic Heritage Foundation","category":"Social Science","amount_min":5000,"amount_max":5000,"application_url":"https://www.hispanicheritage.org/scholarships","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"Citizen|Permanent Resident","residency":"US","source":"hispanic_cultural","source_id":"hispanic_001","daily_id":"hispanic_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"Latino Leadership Summit Scholarship","organization":"National Hispanic Business Group","category":"Business","amount_min":2000,"amount_max":2000,"application_url":"https://www.nhbg.org/latino-scholarship","field_of_study":"Business","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"hispanic_cultural","source_id":"hispanic_002","daily_id":"hispanic_20260724_002","deadline":"2026-04-30","status":"active"},
    {"name":"Chicano Latino Faculty Association Award","organization":"CLFA","category":"Education","amount_min":1500,"amount_max":1500,"application_url":"https://www.clfa.org/award","field_of_study":"Education","education_level":"Graduate","state_restriction":"US","citizenship":"Permanent Resident","residency":"US","source":"hispanic_cultural","source_id":"hispanic_003","daily_id":"hispanic_20260724_003","deadline":"2026-05-15","status":"active"},
    {"name":"United We Dream Scholarship","organization":"UWD","category":"Community","amount_min":1000,"amount_max":1000,"application_url":"https://www.unitedwedream.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"None","residency":"US","source":"hispanic_cultural","source_id":"hispanic_004","daily_id":"hispanic_20260724_004","deadline":"2026-06-30","status":"active"},
    # Black / African American
    {"name":"NAACP ACT-SO Scholarship","organization":"NAACP","category":"Community","amount_min":2000,"amount_max":2000,"application_url":"https://www.naacp.org/act-scholarship","field_of_study":"Any","education_level":"High School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"black_cultural","source_id":"black_001","daily_id":"black_20260724_001","deadline":"2026-04-01","status":"active"},
    {"name":"United Negro College Fund Scholarship","organization":"UNCF","category":"Community","amount_min":5000,"amount_max":5000,"application_url":"https://www.uncf.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"black_cultural","source_id":"black_002","daily_id":"black_20260724_002","deadline":"2026-03-15","status":"active"},
    {"name":"Thurgood Marshall College Fund Scholarship","organization":"TMCF","category":"Community","amount_min":3000,"amount_max":3000,"application_url":"https://www.tmcf.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"black_cultural","source_id":"black_003","daily_id":"black_20260724_003","deadline":"2026-05-01","status":"active"},
    {"name":"Black MBA Exchange Scholarship","organization":"BME","category":"Business","amount_min":4000,"amount_max":4000,"application_url":"https://www.blackmbaexchange.org/scholarship","field_of_study":"Business","education_level":"Professional","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"black_cultural","source_id":"black_004","daily_id":"black_20260724_004","deadline":"2026-06-15","status":"active"},
    # Asian American / Pacific Islander
    {"name":"APA Scholarship","organization":"OCA-Asian Pacific American Advocates","category":"Community","amount_min":2000,"amount_max":2000,"application_url":"https://www.ocanational.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"asian_cultural","source_id":"asian_001","daily_id":"asian_20260724_001","deadline":"2026-04-15","status":"active"},
    {"name":"Pan Asian Alliance Scholarship","organization":"PAA","category":"Community","amount_min":1500,"amount_max":1500,"application_url":"https://www.panasianalliance.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"asian_cultural","source_id":"asian_002","daily_id":"asian_20260724_002","deadline":"2026-05-30","status":"active"},
    {"name":"NAPA Scholarship","organization":"National Asian Pacific American Bar Association","category":"Law","amount_min":3000,"amount_max":3000,"application_url":"https://www.napaba.org/scholarship","field_of_study":"Law","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"asian_cultural","source_id":"asian_003","daily_id":"asian_20260724_003","deadline":"2026-06-01","status":"active"},
    # Indigenous / Native American
    {"name":"American Indian College Fund Scholarship","organization":"AICF","category":"Community","amount_min":2500,"amount_max":2500,"application_url":"https://www.collegefund.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"indigenous_cultural","source_id":"indigenous_001","daily_id":"indigenous_20260724_001","deadline":"2026-04-30","status":"active"},
    {"name":"Native American Tuition Waiver","organization":"Bureau of Indian Affairs","category":"Community","amount_min":0,"amount_max":0,"application_url":"https://www.bia.gov/education/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"indigenous_cultural","source_id":"indigenous_002","daily_id":"indigenous_20260724_002","deadline":"2026-05-15","status":"active"},
    # Women in STEM
    {"name":"Women in Engineering Scholarship","organization":"SWE","category":"STEM","amount_min":5000,"amount_max":5000,"application_url":"https://www.swe.org/scholarships","field_of_study":"Engineering","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"women_stem","source_id":"women_001","daily_id":"women_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"Girls Who Code Scholarship","organization":"Girls Who Code","category":"Tech","amount_min":3000,"amount_max":3000,"application_url":"https://www.girlswhocode.com/scholarship","field_of_study":"Computer Science","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"women_stem","source_id":"women_002","daily_id":"women_20260724_002","deadline":"2026-04-15","status":"active"},
    {"name":"Anita Borg Memorial Scholarship","organization":"AnitaB.org","category":"STEM","amount_min":4000,"amount_max":4000,"application_url":"https://anitab.org/scholarship","field_of_study":"Computer Science","education_level":"Graduate","state_restriction":"International","citizenship":"None","residency":"International","source":"women_stem","source_id":"women_003","daily_id":"women_20260724_003","deadline":"2026-06-01","status":"active"},
    # LGBTQ+
    {"name":"Point Foundation Scholarship","organization":"Point Foundation","category":"Community","amount_min":10000,"amount_max":10000,"application_url":"https://www.pointfoundation.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"lgbtq_cultural","source_id":"lgbtq_001","daily_id":"lgbtq_20260724_001","deadline":"2026-02-28","status":"active"},
    {"name":"Pride Foundation Scholarship","organization":"Pride Foundation","category":"Community","amount_min":2500,"amount_max":2500,"application_url":"https://www.pridefoundation.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"lgbtq_cultural","source_id":"lgbtq_002","daily_id":"lgbtq_20260724_002","deadline":"2026-04-01","status":"active"},
    # Disability
    {"name":"National Federation of the Blind Scholarship","organization":"NFB","category":"Community","amount_min":3000,"amount_max":3000,"application_url":"https://www.nfb.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"disability_advocacy","source_id":"disability_001","daily_id":"disability_20260724_001","deadline":"2026-03-15","status":"active"},
    {"name":"Autism Scholarship Program","organization":"Autism Society","category":"Community","amount_min":2000,"amount_max":2000,"application_url":"https://www.autism-society.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"disability_advocacy","source_id":"disability_002","daily_id":"disability_20260724_002","deadline":"2026-05-01","status":"active"},
    # Business / Entrepreneurship
    {"name":"Dell Scholars Program","organization":"Dell Foundation","category":"Business","amount_min":20000,"amount_max":20000,"application_url":"https://www.dellscholars.org/apply","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"business_entrepreneurship","source_id":"business_001","daily_id":"business_20260724_001","deadline":"2026-01-15","status":"active"},
    {"name":"Echoing Green Fellowship","organization":"Echoing Green","category":"Business","amount_min":90000,"amount_max":90000,"application_url":"https://www.echoinggreen.org/fellowship","field_of_study":"Business","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"business_entrepreneurship","source_id":"business_002","daily_id":"business_20260724_002","deadline":"2026-03-31","status":"active"},
    {"name":"Kauffman Foundation Scholarship","organization":"Kauffman Foundation","category":"Business","amount_min":5000,"amount_max":5000,"application_url":"https://www.kauffman.org/scholarship","field_of_study":"Business","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"business_entrepreneurship","source_id":"business_003","daily_id":"business_20260724_003","deadline":"2026-04-30","status":"active"},
    {"name":"Horatio Alger Scholarship","organization":"Horatio Alger Association","category":"Community","amount_min":25000,"amount_max":25000,"application_url":"https://www.horatioalger.org/scholarship","field_of_study":"Any","education_level":"High School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"business_entrepreneurship","source_id":"business_004","daily_id":"business_20260724_004","deadline":"2026-02-28","status":"active"},
    # Military / Veteran
    {"name":"Post-9/11 GI Bill","organization":"VA","category":"Military/Veteran","amount_min":0,"amount_max":0,"application_url":"https://www.benefits.gov/gi-bill","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"military_veteran","source_id":"military_001","daily_id":"military_20260724_001","deadline":"2026-12-31","status":"active"},
    {"name":"Purple Heart Scholarship","organization":"Military Order of the Purple Heart","category":"Military/Veteran","amount_min":500,"amount_max":5000,"application_url":"https://www.moph.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"military_veteran","source_id":"military_002","daily_id":"military_20260724_002","deadline":"2026-04-15","status":"active"},
    {"name":"Armed Forces Benefit Association Scholarship","organization":"AFBA","category":"Military/Veteran","amount_min":2000,"amount_max":2000,"application_url":"https://www.afba.com/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"military_veteran","source_id":"military_003","daily_id":"military_20260724_003","deadline":"2026-05-30","status":"active"},
    # Law
    {"name":"ABA Legal Opportunity Scholarship","organization":"ABA","category":"Law","amount_min":15000,"amount_max":15000,"application_url":"https://www.americanbar.org/scholarship","field_of_study":"Law","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"law_professional","source_id":"law_001","daily_id":"law_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"NAACP Law School Scholarship","organization":"NAACP Legal Defense Fund","category":"Law","amount_min":5000,"amount_max":5000,"application_url":"https://www.naacpldf.org/law-scholarship","field_of_study":"Law","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"law_professional","source_id":"law_002","daily_id":"law_20260724_002","deadline":"2026-04-15","status":"active"},
    # Healthcare / Medicine
    {"name":"Health Professionals Scholarship Program","organization":"USDoD","category":"Medicine","amount_min":0,"amount_max":0,"application_url":"https://www.healthcareers.gov/scholarship","field_of_study":"Medicine","education_level":"Professional","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"healthcare_medicine","source_id":"healthcare_001","daily_id":"healthcare_20260724_001","deadline":"2026-06-30","status":"active"},
    {"name":"National Health Service Corps Scholarship","organization":"NHSC","category":"Medicine","amount_min":0,"amount_max":0,"application_url":"https://www.nhsc.gov/scholarship","field_of_study":"Medicine","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"healthcare_medicine","source_id":"healthcare_002","daily_id":"healthcare_20260724_002","deadline":"2026-05-15","status":"active"},
    {"name":"AAMC Scholarship for Medical Students","organization":"AAMC","category":"Medicine","amount_min":10000,"amount_max":10000,"application_url":"https://www.aamc.org/scholarship","field_of_study":"Medicine","education_level":"Professional","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"healthcare_medicine","source_id":"healthcare_003","daily_id":"healthcare_20260724_003","deadline":"2026-04-01","status":"active"},
    # Trades / Vocational
    {"name":"Hobby Lobby Scholarship","organization":"Hobby Lobby","category":"Trade School","amount_min":1000,"amount_max":5000,"application_url":"https://www.hobbylobby.com/scholarship","field_of_study":"Any","education_level":"Trade School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"trade_vocational","source_id":"trade_001","daily_id":"trade_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"Trade Wind Scholarship","organization":"Associated Builders and Contractors","category":"Trade School","amount_min":2500,"amount_max":2500,"application_url":"https://www.abc.org/scholarship","field_of_study":"Trades","education_level":"Trade School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"trade_vocational","source_id":"trade_002","daily_id":"trade_20260724_002","deadline":"2026-05-01","status":"active"},
    {"name":"SkillsUSA Scholarship","organization":"SkillsUSA","category":"Trade School","amount_min":1000,"amount_max":10000,"application_url":"https://www.skillsusa.org/scholarship","field_of_study":"Any","education_level":"Trade School","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"trade_vocational","source_id":"trade_003","daily_id":"trade_20260724_003","deadline":"2026-04-15","status":"active"},
    # Arts / Humanities
    {"name":"Ford Foundation Fellowship","organization":"Ford Foundation","category":"Arts","amount_min":20000,"amount_max":20000,"application_url":"https://www.fordfoundation.org/fellowship","field_of_study":"Arts","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"arts_humanities","source_id":"arts_001","daily_id":"arts_20260724_001","deadline":"2026-03-15","status":"active"},
    {"name":"NEA Literature Fellowship","organization":"National Endowment for the Arts","category":"Arts","amount_min":25000,"amount_max":25000,"application_url":"https://www.arts.gov/fellowships","field_of_study":"Arts","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"arts_humanities","source_id":"arts_002","daily_id":"arts_20260724_002","deadline":"2026-04-30","status":"active"},
    # STEM specific
    {"name":"SMART Scholarship","organization":"DoD SMART","category":"STEM","amount_min":0,"amount_max":0,"application_url":"https://www.smartscholarship.org/apply","field_of_study":"STEM","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"stem_specific","source_id":"stem_001","daily_id":"stem_20260724_001","deadline":"2026-02-28","status":"active"},
    {"name":"Goldwater Scholarship","organization":"Goldwater Foundation","category":"STEM","amount_min":7500,"amount_max":7500,"application_url":"https://www.goldwater.org/scholarship","field_of_study":"STEM","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"stem_specific","source_id":"stem_002","daily_id":"stem_20260724_002","deadline":"2026-01-31","status":"active"},
    {"name":"NSF Graduate Research Fellowship","organization":"NSF","category":"STEM","amount_min":37000,"amount_max":37000,"application_url":"https://www.nsf.gov/grfp/scholarship","field_of_study":"STEM","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"stem_specific","source_id":"stem_003","daily_id":"stem_20260724_003","deadline":"2026-10-31","status":"active"},
    {"name":"Google Lime Scholarship","organization":"Google","category":"Tech","amount_min":10000,"amount_max":10000,"application_url":"https://google.com/lime-scholarship","field_of_study":"Computer Science","education_level":"Undergraduate","state_restriction":"International","citizenship":"None","residency":"International","source":"stem_specific","source_id":"stem_004","daily_id":"stem_20260724_004","deadline":"2026-04-01","status":"active"},
    {"name":"Microsoft Disability Scholarship","organization":"Microsoft","category":"Tech","amount_min":5000,"amount_max":5000,"application_url":"https://www.microsoft.com/disability-scholarship","field_of_study":"Computer Science","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"tech_specific","source_id":"tech_001","daily_id":"tech_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"SAS Programmers Scholarship","organization":"SAS Institute","category":"Tech","amount_min":5000,"amount_max":5000,"application_url":"https://www.sas.com/scholarship","field_of_study":"Computer Science","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"tech_specific","source_id":"tech_002","daily_id":"tech_20260724_002","deadline":"2026-05-01","status":"active"},
    # International
    {"name":"Chevening Scholarship UK","organization":"UK Gov","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.chevening.org/scholarship","field_of_study":"Any","education_level":"Graduate","state_restriction":"UK","citizenship":"International","residency":"UK","source":"international","source_id":"intl_001","daily_id":"intl_20260724_001","deadline":"2026-11-05","status":"active"},
    {"name":"Erasmus Mundus Joint Scholarship","organization":"EU Commission","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.erasmusmundus.eu/scholarship","field_of_study":"Any","education_level":"Graduate","state_restriction":"EU","citizenship":"International","residency":"EU","source":"international","source_id":"intl_002","daily_id":"intl_20260724_002","deadline":"2026-01-31","status":"active"},
    {"name":"DAAD Study in Germany","organization":"DAAD","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.daad.de/study-scholarship","field_of_study":"Any","education_level":"Graduate","state_restriction":"DE","citizenship":"International","residency":"Germany","source":"international","source_id":"intl_003","daily_id":"intl_20260724_003","deadline":"2026-10-15","status":"active"},
    {"name":"Study Netherlands Holland Scholarship","organization":"Nuffic","category":"Academic","amount_min":5000,"amount_max":5000,"application_url":"https://www.studynl.nl/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"NL","citizenship":"International","residency":"Netherlands","source":"international","source_id":"intl_004","daily_id":"intl_20260724_004","deadline":"2026-03-01","status":"active"},
    {"name":"French Government Scholarship","organization":"France-Visas","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.campusfrance.org/scholarship","field_of_study":"Any","education_level":"Graduate","state_restriction":"FR","citizenship":"International","residency":"France","source":"international","source_id":"intl_005","daily_id":"intl_20260724_005","deadline":"2026-01-31","status":"active"},
    {"name":"Australia Awards Scholarship","organization":"AusAID","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.studyaustralia.gov.au/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"AU","citizenship":"International","residency":"Australia","source":"international","source_id":"intl_006","daily_id":"intl_20260724_006","deadline":"2026-04-30","status":"active"},
    {"name":"NZ International Doctoral Research Scholarship","organization":"MBIE NZ","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.mbie.govt.nz/scholarship","field_of_study":"Any","education_level":"PhD","state_restriction":"NZ","citizenship":"International","residency":"New Zealand","source":"international","source_id":"intl_007","daily_id":"intl_20260724_007","deadline":"2026-02-28","status":"active"},
    {"name":"Canadian International Scholarship","organization":"CICan","category":"Academic","amount_min":0,"amount_max":0,"application_url":"https://www.cican.ca/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"CA","citizenship":"International","residency":"Canada","source":"international","source_id":"intl_008","daily_id":"intl_20260724_008","deadline":"2026-03-31","status":"active"},
    # Community / Civic
    {"name":"Rotary International Scholarship","organization":"Rotary International","category":"Community","amount_min":5000,"amount_max":5000,"application_url":"https://www.rotary.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"community_civic","source_id":"community_001","daily_id":"community_20260724_001","deadline":"2026-03-31","status":"active"},
    {"name":"Lions Club International Scholarship","organization":"Lions Clubs International","category":"Community","amount_min":5000,"amount_max":5000,"application_url":"https://www.lionsclubs.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"community_civic","source_id":"community_002","daily_id":"community_20260724_002","deadline":"2026-04-30","status":"active"},
    {"name":"Kiwanis Education Scholarship","organization":"Kiwanis International","category":"Community","amount_min":1000,"amount_max":1000,"application_url":"https://www.kiwanis.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"community_civic","source_id":"community_003","daily_id":"community_20260724_003","deadline":"2026-05-15","status":"active"},
    # Science specific
    {"name":"Barry Goldwater Scholarship","organization":"Goldwater Foundation","category":"STEM","amount_min":7500,"amount_max":7500,"application_url":"https://www.goldwater.org/scholarship","field_of_study":"STEM","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"science_research","source_id":"science_001","daily_id":"science_20260724_001","deadline":"2026-01-31","status":"active"},
    {"name":"NIH Undergraduate Scholar","organization":"NIH","category":"Medicine","amount_min":3000,"amount_max":3000,"application_url":"https://www.nih.gov/scholarship","field_of_study":"Medicine","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"science_research","source_id":"science_002","daily_id":"science_20260724_002","deadline":"2026-03-15","status":"active"},
    {"name":"DOE Computational Science Fellowship","organization":"US DoE","category":"STEM","amount_min":30000,"amount_max":30000,"application_url":"https://www.doe.gov/scholarship","field_of_study":"Computer Science","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"science_research","source_id":"science_003","daily_id":"science_20260724_003","deadline":"2026-02-28","status":"active"},
    # Education
    {"name":"Teach For America Scholarship","organization":"TFA","category":"Education","amount_min":0,"amount_max":0,"application_url":"https://www.teachforamerica.org/scholarship","field_of_study":"Education","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"education_specific","source_id":"edu_001","daily_id":"edu_20260724_001","deadline":"2026-04-01","status":"active"},
    {"name":"Horace Mann Scholarship","organization":"NEA Foundation","category":"Education","amount_min":2000,"amount_max":2000,"application_url":"https://www.neafoundation.org/scholarship","field_of_study":"Education","education_level":"Graduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"education_specific","source_id":"edu_002","daily_id":"edu_20260724_002","deadline":"2026-05-01","status":"active"},
    {"name":"Jack Kent Cooke College Scholarship","organization":"Jack Kent Cooke Foundation","category":"Education","amount_min":40000,"amount_max":40000,"application_url":"https://www.jkcf.org/scholarship","field_of_study":"Any","education_level":"Undergraduate","state_restriction":"US","citizenship":"US Citizen","residency":"US","source":"education_specific","source_id":"edu_003","daily_id":"edu_20260724_003","deadline":"2026-03-15","status":"active"},
]

def add_scholarship(conn, s):
    h = hashlib.sha256(f"{s['name']}{s['organization']}".encode()).hexdigest()[:16]
    now = datetime.now(timezone.utc).isoformat()
    conn.execute("""INSERT OR IGNORE INTO scholarships 
        (source, source_id, daily_id, scholarship_name, organization, category, amount_min, amount_max, application_url, field_of_study, education_level, state_restriction, citizenship, residency, deadline, status, verified, verified_at, created_at, updated_at, name_hash)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (s.get('source',''), s.get('source_id',''), s.get('daily_id',''), s['name'], s['organization'], s.get('category','Academic'), s.get('amount_min'), s.get('amount_max'), s.get('application_url',''), s.get('field_of_study',''), s.get('education_level','Undergraduate'), s.get('state_restriction',''), s.get('citizenship',''), s.get('residency',''), s.get('deadline',''), s.get('status','active'), 0, None, now, now, h))

def main():
    os.makedirs(os.path.dirname(DB1), exist_ok=True)
    os.makedirs(os.path.dirname(DB2), exist_ok=True)
    
    conn1 = sqlite3.connect(DB1)
    conn2 = sqlite3.connect(DB2)
    
    # Create table if not exists (matching discover.py schema)
    for conn in [conn1, conn2]:
        conn.execute("""CREATE TABLE IF NOT EXISTS scholarships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT, source_id TEXT, daily_id TEXT,
            scholarship_name TEXT, organization TEXT, category TEXT,
            amount_min REAL, amount_max REAL, application_url TEXT,
            field_of_study TEXT, education_level TEXT, state_restriction TEXT,
            citizenship TEXT, residency TEXT, deadline TEXT, status TEXT,
            verified INTEGER, verified_at TEXT,
            created_at TEXT, updated_at TEXT, name_hash TEXT
        )""")
        conn.commit()
    
    before1 = conn1.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    before2 = conn2.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    
    added1 = 0
    added2 = 0
    dupes = 0
    
    for s in scholarships:
        h = hashlib.sha256(f"{s['name']}{s['organization']}".encode()).hexdigest()[:16]
        now = datetime.now(timezone.utc).isoformat()
        
        # Try both DBs
        for conn, db_path in [(conn1, DB1), (conn2, DB2)]:
            cur = conn.execute("SELECT id FROM scholarships WHERE name_hash = ?", (h,))
            if cur.fetchone():
                dupes += 1
                continue
            try:
                conn.execute("""INSERT INTO scholarships 
                    (source, source_id, daily_id, scholarship_name, organization, category, amount_min, amount_max, application_url, field_of_study, education_level, state_restriction, citizenship, residency, deadline, status, verified, verified_at, created_at, updated_at, name_hash)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (s.get('source',''), s.get('source_id',''), s.get('daily_id',''), s['name'], s['organization'], s.get('category','Academic'), s.get('amount_min'), s.get('amount_max'), s.get('application_url',''), s.get('field_of_study',''), s.get('education_level','Undergraduate'), s.get('state_restriction',''), s.get('citizenship',''), s.get('residency',''), s.get('deadline',''), s.get('status','active'), 0, None, now, now, h))
                if conn is conn1:
                    added1 += 1
                else:
                    added2 += 1
            except sqlite3.IntegrityError:
                dupes += 1
    
    conn1.commit()
    conn2.commit()
    
    after1 = conn1.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    after2 = conn2.execute("SELECT COUNT(*) FROM scholarships").fetchone()[0]
    
    print(f"Added {added1} to DB1 ({before1} -> {after1})")
    print(f"Added {added2} to DB2 ({before2} -> {after2})")
    print(f"Duplicates skipped: {dupes}")
    print(f"Total in this batch: {len(scholarships)}")
    
    conn1.close()
    conn2.close()

if __name__ == "__main__":
    main()
