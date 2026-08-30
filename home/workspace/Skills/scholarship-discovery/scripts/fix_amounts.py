#!/usr/bin/env python3
"""
Fix amount outliers in the scholarships database.
Identifies and nulls clearly broken amount values.
"""

import sqlite3
import re

DB_PATH = "/home/workspace/scholarsearch-site/data/processed/scholarships.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def is_bad_amount(row):
    """Heuristic to detect broken scholarship amounts."""
    sid, source, name, amount_min, amount_max, amount_display = row
    
    if amount_min is None and amount_max is None:
        return False
    
    # Convert to ints for comparison
    amin = amount_min if amount_min is not None else 0
    amax = amount_max if amount_max is not None else 0
    
    # 1. Truly absurd values from comma-stripping errors
    if amax > 1_000_000:
        return True
    
    # 2. Year-like values (2020-2030) in either min or max
    if (1900 <= amin <= 2100) or (1900 <= amax <= 2100):
        return True
    
    # 3. Very small min (likely title count) with large max
    #    e.g., "Top 330 STEM Scholarships" -> min=330, max=200000
    if amin < 100 and amax >= 10000:
        return True
    
    # 4. amount_min looks like a count from a title (e.g., 360 from "Top 360")
    #    and amount_max is 200000 (common Scholarships360 pattern)
    if amin < 500 and amax == 200000:
        return True
    
    # 5. Very large min paired with very small max (reversed range)
    if amin > 100000 and amax < 1000 and amax > 0:
        return True
    
    return False

def fix_amounts():
    conn = get_connection()
    cur = conn.cursor()
    
    # Get all records with non-null amounts
    cur.execute("""
        SELECT id, source, scholarship_name, amount_min, amount_max, amount_display
        FROM scholarships
        WHERE amount_min IS NOT NULL OR amount_max IS NOT NULL
    """)
    rows = cur.fetchall()
    
    bad_ids = []
    for row in rows:
        if is_bad_amount(row):
            bad_ids.append(row[0])
    
    print(f"Total records with amounts: {len(rows)}")
    print(f"Bad amount records found: {len(bad_ids)}")
    
    if bad_ids:
        # Update bad records
        placeholders = ",".join("?" * len(bad_ids))
        cur.execute(f"""
            UPDATE scholarships
            SET amount_min = NULL, amount_max = NULL, amount_display = 'Varies'
            WHERE id IN ({placeholders})
        """, bad_ids)
        conn.commit()
        print(f"Updated {cur.rowcount} records")
    else:
        print("No bad records found")
    
    # Show summary by source
    cur.execute("""
        SELECT source, COUNT(*) as cnt
        FROM scholarships
        WHERE amount_min IS NOT NULL OR amount_max IS NOT NULL
        GROUP BY source
        ORDER BY cnt DESC
    """)
    print("\nRemaining records with amounts by source:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")
    
    conn.close()

if __name__ == "__main__":
    fix_amounts()
