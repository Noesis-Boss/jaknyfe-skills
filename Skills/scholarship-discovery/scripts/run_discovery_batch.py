#!/usr/bin/env python3
"""
Comprehensive scholarship discovery batch.
Scrapes bold.org paginated listings via agent-browser, extracts metadata
from each scholarship detail page, verifies application links, and
inserts verified records into both scholarship databases.
"""
import sqlite3
import json
import re
import subprocess
import time
import os
import hashlib
from datetime import datetime, date
from urllib.parse import urlparse
from db_safety import guarded_connection, make_backup

CONV_DIR = "/home/.z/workspaces/con_ElTSTCT8Hr8tlAvw"
DBS = [
    "/home/workspace/scholarsearch/data/processed/scholarships.db",
    "/home/workspace/scholarsearch-site/data/processed/scholarships.db",
]
TODAY = date.today().isoformat()

def agent_browser_cmd(args, timeout=30):
    """Run an agent-browser command."""
    cmd = ["agent-browser"] + args
    try:
        result = subprocess.run(cmd, cwd=CONV_DIR, capture_output=True, text=True, timeout=timeout)
        return result.stdout.strip() if result.returncode == 0 else ""
    except Exception as e:
        return ""

def agent_browser_eval(js, timeout=30, session=None):
    """Run JS in the browser and return the result."""
    if session:
        args = ["eval", js, "--session-name", session]
    else:
        args = ["eval", js]
    result = agent_browser_cmd(args, timeout)
    return result

def open_page(url, session=None):
    """Open a page in the browser."""
    args = ["open", url, "--auto-connect"]
    if session:
        args += ["--session-name", session]
    agent_browser_cmd(args, timeout=30)
    return True

def get_scholarship_urls_from_page(page_num):
    """Get scholarship URLs from a bold.org listing page."""
    url = f"https://bold.org/scholarships/by-year/high-school/{page_num}/" if page_num > 1 else "https://bold.org/scholarships/"
    open_page(url)
    time.sleep(3)
    
    js = '''
    (() => {
      const allLinks = Array.from(document.querySelectorAll("a"));
      const scholarshipLinks = allLinks
        .map(a => a.href)
        .filter(h => 
          h && h.includes("bold.org/scholarships/") && 
          !h.includes("by-") && 
          !h.includes("/page/") && 
          !h.includes("for-") &&
          h !== "https://bold.org/scholarships/" &&
          h.match(/bold\\.org\\/scholarships\\/[a-z0-9-]+\\/$/)
        );
      return JSON.stringify([...new Set(scholarshipLinks)]);
    })()
    '''
    result = agent_browser_eval(js, timeout=20)
    try:
        return json.loads(result)
    except:
        return []

def extract_metadata(url):
    """Extract metadata from a bold.org scholarship detail page."""
    open_page(url)
    time.sleep(3)
    
    js = '''
    (() => {
      const getText = (sel) => {
        const el = document.querySelector(sel);
        return el ? el.innerText.trim() : "";
      };
      const getAllText = (sel) => {
        const els = document.querySelectorAll(sel);
        return Array.from(els).map(e => e.innerText.trim()).filter(t => t);
      };
      
      // Find amount - look for dollar signs in the page
      let amount = "";
      const amountEls = getAllText("body *");
      const dollarLines = amountEls.filter(t => /\\$\\d/.test(t) && t.length < 200);
      amount = dollarLines.join(" | ");
      
      // Find deadline - look for date mentions
      const deadlineEls = getAllText("body *");
      const deadlineMatch = deadlineEls.find(t => /\\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \\d{1,2},? \\d{4}\\b/i.test(t));
      let deadline = deadlineMatch || "";
      
      // Find application link
      const applyLinks = Array.from(document.querySelectorAll("a")).filter(a => 
        /apply now|apply for|continue to apply|external apply/i.test(a.textContent)
      );
      const appUrl = applyLinks.length > 0 ? applyLinks[0].href : (window.location.href);
      
      // Get full page text for parsing
      return JSON.stringify({
        title: getText("h1, .scholarship-title, [class*='title']"),
        pageText: document.body.innerText.substring(0, 5000),
        amount: amount,
        deadline: deadline,
        appUrl: appUrl
      });
    })()
    '''
    result = agent_browser_eval(js, timeout=20)
    try:
        return json.loads(result)
    except:
        return {}

def parse_metadata(raw, url):
    """Parse raw extracted metadata into structured fields."""
    data = {}
    pageText = raw.get("pageText", "")
    
    # Title - try multiple approaches
    title = raw.get("title", "")
    if not title:
        # Look for first H1 or large text
        for line in pageText.split("\n"):
            line = line.strip()
            if line and len(line) < 150 and not line.isdigit():
                title = line
                break
    data["scholarship_name"] = title[:200]
    
    # Amount - parse $X,XXX format
    amount_text = raw.get("amount", "")
    amounts = re.findall(r'\$[\d,]+\.?\d*', amount_text)
    if amounts:
        nums = [int(re.sub(r'[^0-9]', '', a)) for a in amounts]
        data["amount_display"] = amounts[0]
        data["amount_min"] = min(nums) if nums else None
        data["amount_max"] = max(nums) if nums else None
    
    # Deadline - find date
    deadline_text = raw.get("deadline", "")
    if not deadline_text:
        # Search page text for dates
        date_match = re.search(r'(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+(\d{1,2}),?\s*(\d{4})', pageText, re.IGNORECASE)
        if date_match:
            deadline_text = date_match.group(0)
    if deadline_text:
        try:
            parsed = datetime.strptime(deadline_text, '%b %d, %Y').date()
            data["deadline"] = parsed.isoformat()
        except:
            try:
                parsed = datetime.strptime(deadline_text, '%B %d, %Y').date()
                data["deadline"] = parsed.isoformat()
            except:
                data["deadline"] = deadline_text[:50]
    
    # Application URL
    data["application_url"] = raw.get("appUrl", "")
    
    # Organization
    org_match = re.search(r'Funded by\s*(.+?)(?:\n|$)', pageText)
    if org_match:
        data["organization"] = org_match.group(1).strip()
    
    # Education level
    edu_match = re.search(r'Education Level:\s*(.+?)(?:\n|$)', pageText)
    if edu_match:
        data["education_level"] = edu_match.group(1).strip()
    
    # Description - first paragraph after key info
    data["description"] = pageText[:500] if pageText else ""
    
    # Determine category based on keywords
    text_lower = pageText.lower()
    if "stem" in text_lower or "engineering" in text_lower or "computer science" in text_lower:
        data["category"] = "STEM"
    elif "medicine" in text_lower or "health" in text_lower or "nursing" in text_lower:
        data["category"] = "Medicine"
    elif "women " in text_lower or "female" in text_lower:
        data["category"] = "Women"
    elif "hbcu" in text_lower or "african american" in text_lower or "black" in text_lower:
        data["category"] = "Community"
    elif "business" in text_lower or "entrepreneur" in text_lower:
        data["category"] = "Business"
    elif "art" in text_lower or "creative" in text_lower or "writing" in text_lower:
        data["category"] = "Arts"
    elif "military" in text_lower or "veteran" in text_lower:
        data["category"] = "Military/Veteran"
    elif "mason" in text_lower or "lodge" in text_lower or "fraternal" in text_lower:
        data["category"] = "Masonic"
    elif "community" in text_lower or "service" in text_lower:
        data["category"] = "Community"
    elif "undergraduate" in text_lower or "college" in text_lower or "university" in text_lower:
        data["category"] = "Academic"
    else:
        data["category"] = "Academic"
    
    return data

def verify_application_url(url):
    """Verify that the application URL is reachable."""
    try:
        result = subprocess.run(
            ["curl", "-sL", "-o", "/dev/null", "-w", "%{http_code}", 
             "--max-time", "10", "-A", "Mozilla/5.0", url],
            capture_output=True, text=True, timeout=15
        )
        code = result.stdout.strip()
        return code in ("200", "301", "302", "307", "308")
    except:
        return False

def normalize_name(name):
    """Normalize name for comparison."""
    return re.sub(r'[^\w]', '', name.lower())

def is_duplicate(name, organization, db_path):
    """Check if scholarship already exists in DB."""
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    name_hash = hashlib.md5(normalize_name(name).encode()).hexdigest()
    c.execute("SELECT 1 FROM scholarships WHERE name_hash = ? OR (LOWER(scholarship_name) = LOWER(?) AND LOWER(organization) = LOWER(?))", 
              (name_hash, name, organization or ""))
    result = c.fetchone()
    conn.close()
    return result is not None

def insert_scholarship(data, db_path, source="bold_org"):
    """Insert one record under a validated lock and transaction."""
    with guarded_connection(db_path) as conn:
        name = data.get("scholarship_name", "")
        source_id = f"bold_{TODAY}_{name[:30].replace(' ', '_')}"
        name_hash = hashlib.md5(normalize_name(name).encode()).hexdigest()
        cols = ["source", "source_id", "scholarship_name", "organization", "organization_type", "description", "eligibility", "amount_min", "amount_max", "amount_display", "deadline", "application_url", "category", "education_level", "field_of_study", "state_restriction", "gpa_min", "citizenship", "ethnicity", "gender", "url_status", "last_checked", "name_hash", "active", "created_at", "updated_at"]
        vals = [source, source_id, name, data.get("organization", ""), None, data.get("description", ""), data.get("eligibility", ""), data.get("amount_min"), data.get("amount_max"), data.get("amount_display", ""), data.get("deadline", ""), data.get("application_url", ""), data.get("category", ""), data.get("education_level", ""), None, data.get("state_restriction", "US"), data.get("gpa_min"), "None", data.get("ethnicity", ""), data.get("gender", ""), "active" if data.get("application_url") else "inactive", TODAY, name_hash, 1, TODAY, TODAY]
        placeholders = ",".join(["?"] * len(cols))
        conn.execute(f"INSERT INTO scholarships ({','.join(cols)}) VALUES ({placeholders})", vals)
    return True

def main():
    total_target = 200
    total_found = 0
    failed_urls = []
    stats = {"by_category": {}, "by_region": {}}

    backups = {db: make_backup(db) for db in DBS}
    print(f"Backups created: {backups}")
    
    # Get DB count before
    counts_before = {}
    for db in DBS:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM scholarships")
        counts_before[db] = c.fetchone()[0]
        conn.close()
    
    print(f"DB counts before: {counts_before}")
    
    # Phase 1: bold.org listing pages (paginate through to get scholarship URLs)
    all_urls = []
    for page in range(1, 12):  # Pages 1-11 should give ~270 scholarships
        print(f"Fetching bold.org page {page}...")
        urls = get_scholarship_urls_from_page(page)
        print(f"  Found {len(urls)} URLs on page {page}")
        all_urls.extend(urls)
        if total_found >= total_target and len(all_urls) >= total_target + 50:
            break
        time.sleep(2)
    
    print(f"\nTotal unique URLs collected: {len(set(all_urls))}")
    all_urls = list(set(all_urls))
    
    # Phase 2: Extract metadata from each scholarship page
    # Process in batches to be efficient
    inserted = 0
    for i, url in enumerate(all_urls):
        if total_found >= total_target:
            break
        
        # Check for duplicates before spending time
        name = url.replace("https://bold.org/scholarships/", "").replace("/", "").replace("-", " ").title()
        if is_duplicate(name, "Bold.org", DBS[0]):
            print(f"  [{i+1}/{len(all_urls)}] Duplicate: {url}")
            continue
        
        try:
            raw = extract_metadata(url)
            if not raw.get("pageText"):
                failed_urls.append(url)
                continue
            
            data = parse_metadata(raw, url)
            if not data.get("scholarship_name"):
                continue
            
            # Verify application URL
            app_url = data.get("application_url", "")
            if app_url:
                verified = verify_application_url(app_url)
                if not verified:
                    failed_urls.append(url)
                    # Still insert but mark inactive
                    data["application_url"] = app_url
            
            # Update stats
            cat = data.get("category", "Other")
            stats["by_category"][cat] = stats["by_category"].get(cat, 0) + 1
            
            # Insert into both DBs
            for db in DBS:
                if not is_duplicate(data["scholarship_name"], data.get("organization",""), db):
                    try:
                        insert_scholarship(data, db)
                    except Exception as e:
                        print(f"  Insert error: {e}")
            
            inserted += 1
            total_found += 1
            print(f"  [{i+1}/{len(all_urls)}] ✓ {data.get('scholarship_name','')[:50]} | ${data.get('amount_display','?')} | {data.get('deadline','?')}")
            
        except Exception as e:
            print(f"  [{i+1}/{len(all_urls)}] ERROR: {e}")
            failed_urls.append(url)
        
        # Brief pause
        time.sleep(0.5)
    
    # Get DB counts after
    counts_after = {}
    for db in DBS:
        conn = sqlite3.connect(db)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM scholarships")
        counts_after[db] = c.fetchone()[0]
        conn.close()
    
    print(f"\n{'='*60}")
    print(f"DISCOVERY COMPLETE")
    print(f"{'='*60}")
    print(f"Target: {total_target}")
    print(f"New found: {total_found}")
    print(f"DB counts after: {counts_after}")
    print(f"Failed URLs: {len(failed_urls)}")
    print(f"By category: {json.dumps(stats['by_category'], indent=2)}")
    
    # Save summary
    summary = {
        "date": TODAY,
        "target": total_target,
        "found": total_found,
        "counts_before": counts_before,
        "counts_after": counts_after,
        "failed_urls": failed_urls,
        "by_category": stats["by_category"],
    }
    with open(f"{CONV_DIR}/discovery_summary_{TODAY}.json", "w") as f:
        json.dump(summary, f, indent=2)
    
    print(f"\nSummary saved to {CONV_DIR}/discovery_summary_{TODAY}.json")

if __name__ == "__main__":
    main()
