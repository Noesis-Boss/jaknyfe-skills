#!/usr/bin/env python3
import argparse
import concurrent.futures
import json
import os
import socket
import sqlite3
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter

DB_PATH = os.getenv('SCHOLARSHIP_DB', '/home/workspace/scholarsearch/data/processed/scholarships.db')
MIRROR_DB_PATH = os.getenv('SCHOLARSHIP_MIRROR_DB', '/home/workspace/scholarsearch-site/data/processed/scholarships.db')
TIMEOUT = int(os.getenv('CHECK_TIMEOUT', '6'))
WORKERS = int(os.getenv('CHECK_WORKERS', '8'))
USER_AGENT = 'ScholarSearch-Link-Checker/1.0'


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--limit', type=int, default=int(os.getenv('LIMIT', '500')))
    parser.add_argument('--retry-days', type=int, default=int(os.getenv('CHECK_RETRY_DAYS', '30')))
    args = parser.parse_args()
    if args.limit < 1 or args.retry_days < 1 or TIMEOUT < 1 or WORKERS < 1:
        parser.error('limit, retry-days, CHECK_TIMEOUT, and CHECK_WORKERS must be positive')
    return args


def permanent_dns_failure(error):
    reason = getattr(error, 'reason', error)
    if isinstance(reason, socket.gaierror) and reason.errno == getattr(socket, 'EAI_NONAME', -2):
        return True
    message = str(error).lower()
    return 'name or service not known' in message or 'nxdomain' in message


def check_url(raw_url):
    try:
        parsed = urllib.parse.urlsplit(raw_url.strip())
        if parsed.scheme.lower() not in ('http', 'https') or not parsed.hostname:
            return None, 'broken', 'Invalid HTTP(S) URL'
    except ValueError as error:
        return None, 'broken', str(error)

    url = raw_url.strip()
    last_error = None
    for method in ('HEAD', 'GET'):
        request = urllib.request.Request(url, method=method, headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,application/pdf,*/*'})
        try:
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                code = response.getcode()
                if code < 400:
                    return code, 'active', None
                last_error = f'HTTP {code}: {response.reason}'
                return code, 'broken' if code in (404, 410) else 'unreachable', last_error
        except urllib.error.HTTPError as error:
            last_error = f'HTTP {error.code}: {error.reason}'
            if method == 'HEAD' and error.code in (403, 405, 429):
                continue
            return error.code, 'broken' if error.code in (404, 410) else 'unreachable', last_error
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as error:
            if permanent_dns_failure(error):
                return None, 'broken', str(error)
            return None, 'unreachable', str(error)
    return None, 'unreachable', last_error or 'No usable HTTP response'


def process_row(row, url_results):
    scholarship_id, application_url, form_url, previous_status = row
    statuses = []
    history = []
    errors = []
    for url in (application_url, form_url):
        if not url:
            continue
        url_key = url.strip()
        code, status, error = url_results[url_key]
        statuses.append(status)
        history.append([scholarship_id, url, code, 1 if status == 'active' else 0 if status == 'broken' else None, error])
        if error:
            errors.append(error)

    if not statuses:
        overall = 'no_url'
        history.append([scholarship_id, '', None, None, 'No application_url or form_url was provided'])
    elif 'broken' in statuses:
        overall = 'broken'
    elif 'unreachable' in statuses:
        overall = 'unreachable'
    else:
        overall = 'active'

    changed = previous_status != overall
    return scholarship_id, overall, changed, history, errors, previous_status


def check_rows(rows):
    unique_urls = list(dict.fromkeys(
        url.strip() for row in rows for url in row[1:3] if url and url.strip()
    ))
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as executor:
        url_results = dict(zip(unique_urls, executor.map(check_url, unique_urls)))
    return [process_row(row, url_results) for row in rows], url_results


def transition_history(history, old_status, new_status):
    if old_status == new_status:
        return history
    transition = f'Status changed from {old_status or "unset"} to {new_status}'
    return [
        [scholarship_id, url, code, is_valid, f'{transition}; {error}' if error else transition]
        for scholarship_id, url, code, is_valid, error in history
    ]


def main():
    args = parse_args()
    mirror_enabled = os.path.abspath(DB_PATH) != os.path.abspath(MIRROR_DB_PATH)
    if not os.path.isfile(DB_PATH):
        raise FileNotFoundError(f'Scholarship database not found: {DB_PATH}')
    if mirror_enabled and not os.path.isfile(MIRROR_DB_PATH):
        raise FileNotFoundError(f'Scholarship mirror database not found: {MIRROR_DB_PATH}')
    connection = sqlite3.connect(DB_PATH, timeout=30)
    connection.execute('PRAGMA busy_timeout=30000')
    if mirror_enabled:
        connection.execute('ATTACH DATABASE ? AS mirror', (MIRROR_DB_PATH,))
    cursor = connection.cursor()
    where_clause = (
        "(COALESCE(s.url_status, 'unchecked') = 'unchecked' OR "
        "(s.url_status IN ('broken', 'unreachable') AND "
        "(s.last_checked IS NULL OR s.last_checked <= datetime('now', ?))))"
    )
    params = [f'-{args.retry_days} days']
    mirror_unchecked_order = ''
    if mirror_enabled:
        mirror_pending = (
            "m.id = s.id AND COALESCE(m.application_url, '') = COALESCE(s.application_url, '') "
            "AND COALESCE(m.form_url, '') = COALESCE(s.form_url, '') AND ("
            "COALESCE(m.url_status, 'unchecked') = 'unchecked' OR "
            "(m.url_status IN ('broken', 'unreachable') AND "
            "(m.last_checked IS NULL OR m.last_checked <= datetime('now', ?))))"
        )
        where_clause += f' OR EXISTS (SELECT 1 FROM mirror.scholarships m WHERE {mirror_pending})'
        params.append(f'-{args.retry_days} days')
        mirror_unchecked_order = (
            " OR EXISTS (SELECT 1 FROM mirror.scholarships m WHERE m.id = s.id "
            "AND COALESCE(m.application_url, '') = COALESCE(s.application_url, '') "
            "AND COALESCE(m.form_url, '') = COALESCE(s.form_url, '') "
            "AND COALESCE(m.url_status, 'unchecked') = 'unchecked')"
        )
    params.append(args.limit)
    cursor.execute(
        "SELECT s.id, s.application_url, s.form_url, s.url_status "
        "FROM main.scholarships s WHERE " + where_clause +
        " ORDER BY CASE WHEN (COALESCE(s.url_status, 'unchecked') = 'unchecked' " +
        mirror_unchecked_order + ") THEN 0 ELSE 1 END, "
        "COALESCE(s.last_checked, '1970-01-01'), s.id LIMIT ?",
        params,
    )
    rows = cursor.fetchall()
    row_urls = {row[0]: (row[1], row[2]) for row in rows}
    checked, url_results = check_rows(rows)

    url_mismatches = 0
    mirror_updates = 0
    status_updates = sum(1 for item in checked if item[2])
    checked_at = time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        connection.execute('BEGIN IMMEDIATE')
        for scholarship_id, status, _, history, _, old_status in checked:
            cursor.executemany(
                "INSERT INTO main.link_check_history (scholarship_id, url_checked, status_code, is_valid, error_message) VALUES (?, ?, ?, ?, ?)",
                transition_history(history, old_status, status),
            )
            cursor.execute(
                "UPDATE main.scholarships SET url_status = ?, last_checked = ?, active = CASE WHEN ? = 'broken' THEN 0 ELSE active END WHERE id = ?",
                (status, checked_at, status, scholarship_id),
            )
            if not mirror_enabled:
                continue
            mirror_row = cursor.execute(
                'SELECT application_url, form_url, url_status FROM mirror.scholarships WHERE id = ?',
                (scholarship_id,),
            ).fetchone()
            if not mirror_row or mirror_row[:2] != row_urls[scholarship_id]:
                url_mismatches += 1
                continue
            mirror_old_status = mirror_row[2]
            mirror_status = status
            if mirror_old_status in ('verified', 'unverified') and status in ('active', 'unreachable'):
                mirror_status = mirror_old_status
            cursor.executemany(
                "INSERT INTO mirror.link_check_history (scholarship_id, url_checked, status_code, is_valid, error_message) VALUES (?, ?, ?, ?, ?)",
                transition_history(history, mirror_old_status, mirror_status),
            )
            cursor.execute(
                "UPDATE mirror.scholarships SET url_status = ?, last_checked = ?, active = CASE WHEN ? = 'broken' THEN 0 ELSE active END WHERE id = ?",
                (mirror_status, checked_at, mirror_status, scholarship_id),
            )
            mirror_updates += int(mirror_old_status != mirror_status)
        connection.commit()
    except BaseException:
        connection.rollback()
        connection.close()
        raise

    counts = Counter(item[1] for item in checked)
    errors = Counter(error for _, _, error in url_results.values() if error)
    cursor.execute('SELECT COUNT(*) FROM main.scholarships WHERE active = 1')
    active_records = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM main.scholarships WHERE COALESCE(url_status, 'unchecked') = 'unchecked'")
    unchecked_remaining = cursor.fetchone()[0]
    mirror_active_records = None
    mirror_unchecked_remaining = None
    if mirror_enabled:
        cursor.execute('SELECT COUNT(*) FROM mirror.scholarships WHERE active = 1')
        mirror_active_records = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM mirror.scholarships WHERE COALESCE(url_status, 'unchecked') = 'unchecked'")
        mirror_unchecked_remaining = cursor.fetchone()[0]
    summary = {
        'checked': len(checked),
        'url_fields_checked': sum(1 for item in checked for record in item[3] if record[1]),
        'unique_urls_checked': len(url_results),
        'reachable': counts['active'],
        'broken': counts['broken'],
        'unreachable': counts['unreachable'],
        'no_url': counts['no_url'],
        'status_updates': status_updates,
        'mirror_status_updates': mirror_updates,
        'mirror_url_mismatches': url_mismatches,
        'active_records': active_records,
        'mirror_active_records': mirror_active_records,
        'unchecked_remaining': unchecked_remaining,
        'mirror_unchecked_remaining': mirror_unchecked_remaining,
        'errors': dict(errors),
    }
    connection.close()
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
