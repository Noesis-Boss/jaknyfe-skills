#!/usr/bin/env python3
"""
ScholarSearch Link Verifier
- Checks URLs at 100/hour
- Searches for replacements on failure
- Disables records with no replacement (active=0)
- Excludes disabled records from search
"""
import sqlite3
import urllib.request
import urllib.error
import urllib.parse
import os
import json
import sys
import time
import re
import ssl
from datetime import datetime, timezone

DB_PATH = os.getenv('SCHOLARSHIP_DB', '/home/workspace/scholarsearch-site/data/processed/scholarships.db')
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '100'))
DELAY_BETWEEN = int(os.getenv('DELAY_BETWEEN', '36'))  # 3600/100 = 36s
TIMEOUT = int(os.getenv('TIMEOUT', '15'))
SEARCH_TIMEOUT = int(os.getenv('SEARCH_TIMEOUT', '20'))

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def check_url(url):
    """Returns (status_code, is_valid, error_message)"""
    if not url or not url.startswith('http'):
        return None, False, 'Invalid URL format'
    
    try:
        req = urllib.request.Request(url, method='HEAD', headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as resp:
            return resp.status, True, None
    except urllib.error.HTTPError as e:
        return e.code, False, str(e)
    except urllib.error.URLError as e:
        return None, False, str(e.reason)
    except Exception as e:
        return None, False, str(e)

def search_replacement(scholarship_name, organization):
    """Search DuckDuckGo HTML for a replacement URL."""
    query = f'"{scholarship_name}" "{organization}" scholarship apply application'
    params = urllib.parse.urlencode({'q': query})
    url = f"https://html.duckduckgo.com/html/?{params}"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=SEARCH_TIMEOUT, context=ctx) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
        
        # Extract result links from DuckDuckGo HTML
        # Pattern: result__a href="..."
        matches = re.findall(r'result__a[^>]*href="([^"]+)"', html)
        if not matches:
            # Alternative pattern
            matches = re.findall(r'<a[^>]+class="result__a"[^>]+href="([^"]+)"', html)
        
        for match in matches:
            # DuckDuckGo wraps links; extract actual URL
            if match.startswith('//duckduckgo.com/l/?uddg='):
                parsed = urllib.parse.urlparse(match)
                qs = urllib.parse.parse_qs(parsed.query)
                if 'uddg' in qs:
                    actual_url = urllib.parse.unquote(qs['uddg'][0])
                    if actual_url.startswith('http'):
                        return actual_url
            elif match.startswith('http'):
                return match
        
        return None
    except Exception as e:
        return None

def verify_batch():
    conn = get_db()
    cursor = conn.cursor()
    
    # Get candidates: active records that haven't been checked recently
    # Prioritize broken, then unchecked, then oldest checked
    cursor.execute("""
        SELECT id, scholarship_name, organization, application_url, form_url, website, url_status
        FROM scholarships
        WHERE active = 1
        ORDER BY 
            CASE 
                WHEN url_status = 'broken' THEN 1
                WHEN url_status = 'unchecked' THEN 2
                ELSE 3
            END,
            last_checked IS NULL DESC, 
            last_checked ASC
        LIMIT ?
    """, (BATCH_SIZE,))
    
    rows = cursor.fetchall()
    if not rows:
        print(json.dumps({"status": "complete", "message": "No scholarships to verify"}))
        conn.close()
        return
    
    results = {
        "processed": 0,
        "active": 0,
        "broken": 0,
        "replaced": 0,
        "disabled": 0,
        "details": []
    }
    
    for row in rows:
        sch_id = row['id']
        name = row['scholarship_name']
        org = row['organization']
        urls_to_check = []
        
        # Prioritize application_url, then form_url, then website
        if row['application_url'] and row['application_url'].startswith('http'):
            urls_to_check.append(('application_url', row['application_url']))
        if row['form_url'] and row['form_url'].startswith('http'):
            urls_to_check.append(('form_url', row['form_url']))
        if row['website'] and row['website'].startswith('http'):
            urls_to_check.append(('website', row['website']))
        
        if not urls_to_check:
            # No URLs to check, mark as active but note it
            cursor.execute("""
                UPDATE scholarships SET url_status = 'active', last_checked = ?
                WHERE id = ?
            """, (datetime.now(timezone.utc).isoformat(), sch_id))
            conn.commit()
            results['active'] += 1
            results['processed'] += 1
            continue
        
        overall_valid = False
        replacement_url = None
        checked_url = None
        status_code = None
        error_msg = None
        url_type_used = None
        
        for url_type, url in urls_to_check:
            status_code, is_valid, error_msg = check_url(url)
            checked_url = url
            url_type_used = url_type
            
            if is_valid:
                overall_valid = True
                break
            
            # If this is the primary URL (application_url) and it fails, try to find replacement
            if url_type == 'application_url':
                replacement_url = search_replacement(name, org)
                if replacement_url:
                    status_code, is_valid, error_msg = check_url(replacement_url)
                    if is_valid:
                        overall_valid = True
                        break
        
        now = datetime.now(timezone.utc).isoformat()
        
        if overall_valid:
            # Update with the valid URL (replacement if found)
            final_url = replacement_url if replacement_url else checked_url
            if replacement_url:
                cursor.execute("""
                    UPDATE scholarships 
                    SET application_url = ?, url_status = 'active', last_checked = ?, link_notes = ?
                    WHERE id = ?
                """, (final_url, now, f"Replacement URL found on {now}", sch_id))
                results['replaced'] += 1
            else:
                cursor.execute("""
                    UPDATE scholarships 
                    SET url_status = 'active', last_checked = ?
                    WHERE id = ?
                """, (now, sch_id))
                results['active'] += 1
        else:
            # Mark as disabled - no valid URL and no replacement
            cursor.execute("""
                UPDATE scholarships 
                SET active = 0, url_status = 'broken', last_checked = ?, link_notes = ?
                WHERE id = ?
            """, (now, f"Disabled {now}: no valid URL found. Last checked: {checked_url} - {error_msg}", sch_id))
            results['disabled'] += 1
        
        # Log to history
        cursor.execute("""
            INSERT INTO link_check_history (scholarship_id, url_checked, status_code, is_valid, error_message)
            VALUES (?, ?, ?, ?, ?)
        """, (sch_id, checked_url, status_code, 1 if overall_valid else 0, error_msg))
        
        conn.commit()
        results['processed'] += 1
        results['details'].append({
            "id": sch_id,
            "name": name,
            "status": "active" if overall_valid else "disabled",
            "url": checked_url,
            "replacement": replacement_url,
            "code": status_code
        })
        
        # Rate limit: ~100/hour
        time.sleep(DELAY_BETWEEN)
    
    conn.close()
    
    # Print summary for logs
    print(json.dumps(results, indent=2))
    return results

if __name__ == '__main__':
    verify_batch()
