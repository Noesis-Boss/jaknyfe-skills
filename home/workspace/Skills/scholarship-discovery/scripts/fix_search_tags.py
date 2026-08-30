#!/usr/bin/env python3
import sqlite3

DBS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

def normalize_category(val):
    if not val:
        return val
    v = val.strip()
    title_map = {
        "Academic": "Academic",
        "Community": "Community",
        "Extracurricular": "Extracurricular",
        "High School": "High School",
        "International": "International",
        "Local/Regional": "Local/Regional",
        "Masonic": "Masonic",
        "Military/Veteran": "Military/Veteran",
        "Need-Based": "Need-Based",
        "PhD": "PhD",
        "STEM": "STEM",
        "Trade School": "Trade School",
        "Undergraduate": "Undergraduate",
        "Women": "Women",
    }
    if v in title_map:
        return title_map[v]
    snake_map = {
        "academic": "Academic",
        "agriculture": "Agriculture",
        "agriculture_environment": "Agriculture/Environment",
        "arts": "Arts",
        "business": "Business",
        "communications": "Communications",
        "design": "Design",
        "education": "Education",
        "engineering": "Engineering",
        "environment": "Environment",
        "graduate": "Graduate",
        "healthcare": "Healthcare",
        "high_school": "High School",
        "international": "International",
        "law": "Law",
        "localregional": "Local/Regional",
        "medicine": "Medicine",
        "military_veteran": "Military/Veteran",
        "need_based": "Need-Based",
        "phd": "PhD",
        "professional": "Professional",
        "science": "Science",
        "social_science": "Social Science",
        "stem": "STEM",
        "tech": "Tech",
        "trade_school": "Trade School",
        "undergraduate": "Undergraduate",
        "women": "Women",
    }
    return snake_map.get(v.lower(), v)

def normalize_education_level(val):
    if not val:
        return val
    v = val.strip()
    if v.lower() == "high school senior":
        return "High School"
    return v

def normalize_citizenship(val):
    if not val:
        return val
    v = val.strip()
    if v.lower() in ("us", "us citizen"):
        return "US Citizen"
    return v

def clean_db(db_path):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    updates = 0

    # Clean category
    cur.execute("SELECT id, category FROM scholarships WHERE category IS NOT NULL")
    for row_id, cat in cur.fetchall():
        cleaned = normalize_category(cat)
        if cleaned != cat:
            cur.execute(
                "UPDATE scholarships SET category=?, updated_at=datetime('now') WHERE id=?",
                (cleaned, row_id),
            )
            updates += 1

    # Clean education_level
    cur.execute("SELECT id, education_level FROM scholarships WHERE education_level IS NOT NULL")
    for row_id, lvl in cur.fetchall():
        cleaned = normalize_education_level(lvl)
        if cleaned != lvl:
            cur.execute(
                "UPDATE scholarships SET education_level=?, updated_at=datetime('now') WHERE id=?",
                (cleaned, row_id),
            )
            updates += 1

    # Clean citizenship
    cur.execute("SELECT id, citizenship FROM scholarships WHERE citizenship IS NOT NULL")
    for row_id, cit in cur.fetchall():
        cleaned = normalize_citizenship(cit)
        if cleaned != cit:
            cur.execute(
                "UPDATE scholarships SET citizenship=?, updated_at=datetime('now') WHERE id=?",
                (cleaned, row_id),
            )
            updates += 1

    # Clean state_restriction
    for bad in ("Varies", "Varies by jurisdiction", "$3,000", "$500-$1,000"):
        cur.execute(
            "UPDATE scholarships SET state_restriction=NULL, updated_at=datetime('now') WHERE state_restriction=?",
            (bad,),
        )
        updates += cur.rowcount

    conn.commit()

    cur.execute("SELECT COUNT(*) FROM scholarships")
    total = cur.fetchone()[0]
    cur.execute("SELECT category, COUNT(*) FROM scholarships GROUP BY category ORDER BY category")
    cats = cur.fetchall()
    cur.execute("SELECT education_level, COUNT(*) FROM scholarships GROUP BY education_level ORDER BY education_level")
    edus = cur.fetchall()
    cur.execute("SELECT citizenship, COUNT(*) FROM scholarships GROUP BY citizenship ORDER BY citizenship")
    cits = cur.fetchall()
    conn.close()
    return updates, total, cats, edus, cits


for db in DBS:
    print(f"\n=== {db} ===")
    try:
        updates, total, cats, edus, cits = clean_db(db)
        print(f"Updated: {updates} | Total: {total}\n")
        print("Categories:")
        for c, n in cats:
            print(f"  {c}: {n}")
        print("\nEducation Levels:")
        for e, n in edus:
            print(f"  {e}: {n}")
        print("\nCitizenship:")
        for c, n in cits:
            print(f"  {c}: {n}")
    except Exception as e:
        print(f"ERROR: {e}")
