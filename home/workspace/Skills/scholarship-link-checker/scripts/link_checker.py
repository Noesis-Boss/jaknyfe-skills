#!/usr/bin/env python3
import sqlite3, urllib.request, urllib.error, os, json, sys, time

DB_PATH = os.getenv('SCHOLARSHIP_DB', '/home/workspace/scholarsearch-site/data/processed/scholarships.db')
LIMIT = int(os.getenv('LIMIT', '500'))

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Find unchecked or broken links - using correct column names from schema
cursor.execute("SELECT id, application_url, form_url FROM scholarships WHERE url_status = 'unchecked' OR url_status = 'broken' LIMIT ?", (LIMIT,))
rows = cursor.fetchall()

print(f"Found {len(rows)} scholarships to check")

results = {'active': 0, 'broken': 0, 'errors': []}

for row in rows:
    sch_id, app_url, form_url = row
    status = {'id': sch_id, 'app_url': app_url, 'form_url': form_url}
    overall_status = 'active'
    
    for url_field in ['application_url', 'form_url']:
        url = status.get(url_field)
        if not url:
            continue
        try:
            req = urllib.request.Request(url, method='HEAD', headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as resp:
                status_code = resp.getcode()
                if status_code >= 400:
                    overall_status = 'broken'
                    status[f'{url_field}_status'] = status_code
                else:
                    status[f'{url_field}_status'] = status_code
        except Exception as e:
            overall_status = 'broken'
            status[f'{url_field}_status'] = f'error: {str(e)}'
    
    # Update the database
    last_checked = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "UPDATE scholarships SET url_status = ?, last_checked = ? WHERE id = ?",
        (overall_status, last_checked, sch_id)
    )
    conn.commit()
    
    if overall_status == 'active':
        results['active'] += 1
    else:
        results['broken'] += 1
    
    results.setdefault('details', []).append(status)

print(json.dumps(results, indent=2))