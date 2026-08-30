import sqlite3
import re
from pathlib import Path

DB_PATHS = [
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]

# State name -> code mapping
STATE_MAP = {
    "alabama": "AL", "alaska": "AK", "arizona": "AZ", "arkansas": "AR",
    "california": "CA", "colorado": "CO", "connecticut": "CT", "delaware": "DE",
    "florida": "FL", "georgia": "GA", "hawaii": "HI", "idaho": "ID",
    "illinois": "IL", "indiana": "IN", "iowa": "IA", "kansas": "KS",
    "kentucky": "KY", "louisiana": "LA", "maine": "ME", "maryland": "MD",
    "massachusetts": "MA", "michigan": "MI", "minnesota": "MN", "mississippi": "MS",
    "missouri": "MO", "montana": "MT", "nebraska": "NE", "nevada": "NV",
    "new hampshire": "NH", "new jersey": "NJ", "new mexico": "NM", "new york": "NY",
    "north carolina": "NC", "north dakota": "ND", "ohio": "OH", "oklahoma": "OK",
    "oregon": "OR", "pennsylvania": "PA", "rhode island": "RI", "south carolina": "SC",
    "south dakota": "SD", "tennessee": "TN", "texas": "TX", "utah": "UT",
    "vermont": "VT", "virginia": "VA", "washington": "WA", "west virginia": "WV",
    "wisconsin": "WI", "wyoming": "WY", "district of columbia": "DC",
}

# Direct code mentions in names/orgs
DIRECT_CODES = {
    "AZ": "AZ", "CA": "CA", "WA": "WA", "PA": "PA", "NC": "NC",
    "TX": "TX", "GA": "GA", "MI": "MI", "NY": "NY", "IL": "IL",
    "FL": "FL", "OH": "OH", "VA": "VA", "OR": "OR", "OK": "OK",
    "LA": "LA", "MA": "MA", "NJ": "NJ", "NM": "NM", "DC": "DC",
    "MD": "MD", "CT": "CT", "TN": "TN", "NV": "NV", "NE": "NE",
    "NH": "NH", "RI": "RI", "CO": "CO", "ID": "ID", "D.C.": "DC",
}

# National / multi-jurisdiction orgs that don't map to a single state
NATIONAL_ORGS = {
    "de molay international", "shriners international", "york rite",
    "york rite sovereign college", "rainbow girls - national",
    "job's daughters international", "scottish rite northern masonic jurisdiction",
}


def extract_state(scholarship_name, organization, current_state):
    """Best-effort state extraction from name/org."""
    # If already a valid 2-letter code, keep it
    if current_state and len(current_state) == 2 and current_state.upper() in {v for v in DIRECT_CODES.values()}:
        return current_state.upper()

    text = f"{scholarship_name} {organization}".lower()

    # Check for direct state codes first (e.g. "AZ", "CA") in text
    for code, state_code in DIRECT_CODES.items():
        # Use word-boundary match for 2-letter codes to avoid false positives
        pattern = r'\b' + re.escape(code) + r'\b'
        if code == "D.C.":
            pattern = r'\bD\.C\.\b'
        if re.search(pattern, f"{scholarship_name} {organization}"):
            return state_code

    # Check for full state names
    for name, code in STATE_MAP.items():
        if name in text:
            return code.upper()

    # Check org name prefixes like "Order of the Eastern Star - Colorado"
    if "order of the eastern star" in text:
        for name, code in STATE_MAP.items():
            if name in text:
                return code.upper()

    # If it's a national org, return empty (not state-restricted)
    org_lower = organization.lower().strip()
    for national in NATIONAL_ORGS:
        if national in org_lower:
            return ""

    # If state looks like a dollar amount, clear it
    if current_state and ("$" in current_state or "million" in current_state.lower()):
        return ""

    return current_state if current_state else ""


def is_masonic_category(category):
    return category and category.strip().lower() == "masonic"


def fix_db(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # Find all Masonic-tagged entries
    cur.execute("""
        SELECT id, scholarship_name, organization, state_restriction, category
        FROM scholarships
        WHERE category = 'Masonic'
           OR category = 'masonic'
           OR scholarship_name LIKE '%Masonic%'
           OR scholarship_name LIKE '%Scottish Rite%'
           OR scholarship_name LIKE '%Eastern Star%'
           OR scholarship_name LIKE '%Shrine%'
           OR scholarship_name LIKE '%DeMolay%'
           OR scholarship_name LIKE '%Rainbow%'
           OR scholarship_name LIKE '%York Rite%'
           OR scholarship_name LIKE '%Knights Templar%'
           OR scholarship_name LIKE '%Amaranth%'
           OR organization LIKE '%Masonic%'
           OR organization LIKE '%Freemason%'
           OR organization LIKE '%Grand Lodge%'
           OR organization LIKE '%Scottish Rite%'
           OR organization LIKE '%Eastern Star%'
           OR organization LIKE '%Shrine%'
           OR organization LIKE '%DeMolay%'
           OR organization LIKE '%Rainbow%'
           OR organization LIKE '%York Rite%'
           OR organization LIKE '%Knights Templar%'
    """)
    rows = cur.fetchall()

    updated = 0
    for row in rows:
        rid = row["id"]
        name = row["scholarship_name"] or ""
        org = row["organization"] or ""
        state = row["state_restriction"] or ""
        cat = row["category"] or ""

        new_state = extract_state(name, org, state)
        # Always ensure category is exactly 'Masonic'
        new_cat = "Masonic" if (cat.strip().lower() == "masonic" or
                                name or org) else cat

        needs_state_fix = new_state != state
        needs_cat_fix = new_cat != cat

        if needs_state_fix or needs_cat_fix:
            sets = []
            params = {}
            if needs_state_fix:
                sets.append("state_restriction = :new_state")
                params["new_state"] = new_state
            if needs_cat_fix:
                sets.append("category = :new_cat")
                params["new_cat"] = new_cat
            params["rid"] = rid

            cur.execute(
                f"UPDATE scholarships SET {', '.join(sets)} WHERE id = :rid",
                params,
            )
            updated += 1

    conn.commit()
    conn.close()
    return len(rows), updated


for db in DB_PATHS:
    path = Path(db)
    if not path.exists():
        print(f"MISSING: {db}")
        continue
    total, updated = fix_db(db)
    print(f"{db}: scanned={total}, updated={updated}")
