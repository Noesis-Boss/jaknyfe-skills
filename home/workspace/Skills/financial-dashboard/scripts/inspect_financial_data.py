#!/usr/bin/env python3
import argparse
import csv
import datetime as dt
import json
import re
from pathlib import Path

DATE_RE = re.compile(r"^\d{1,4}[-/]\d{1,2}[-/]\d{1,4}$")
NUMBER_RE = re.compile(r"^[-+]?\$?\s*\d[\d,]*(?:\.\d+)?%?$")

def load_rows(path: Path):
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))
    if path.suffix.lower() == ".json":
        value = json.loads(path.read_text(encoding="utf-8"))
        return value if isinstance(value, list) else value.get("rows", [])
    raise ValueError("Supported inputs are CSV and JSON")

def normalize_number(value):
    if not isinstance(value, str) or not NUMBER_RE.match(value.strip()):
        return value
    cleaned = value.strip().replace("$", "").replace(",", "").replace("%", "")
    number = float(cleaned)
    return number / 100 if value.strip().endswith("%") else number

def inspect(path: Path):
    rows = load_rows(path)
    issues = []
    normalized = []
    seen = set()
    fields = sorted({key for row in rows for key in row})
    for index, row in enumerate(rows, start=2):
        copy = dict(row)
        fingerprint = json.dumps(row, sort_keys=True, default=str)
        if fingerprint in seen:
            issues.append({"row": index, "issue": "duplicate row", "suggested_correction": "Review and retain or remove explicitly", "confidence": "high"})
        seen.add(fingerprint)
        for key in fields:
            value = row.get(key)
            if value is None or (isinstance(value, str) and not value.strip()):
                issues.append({"row": index, "issue": f"blank value in {key}", "suggested_correction": "Supply a value or mark as unknown", "confidence": "high"})
                continue
            text = str(value).strip()
            low = key.lower()
            if "date" in low or low in {"month", "due", "paid"}:
                if DATE_RE.match(text):
                    try:
                        parsed = dt.datetime.strptime(text.replace("/", "-"), "%Y-%m-%d")
                    except ValueError:
                        try:
                            parsed = dt.datetime.strptime(text.replace("/", "-"), "%d-%m-%Y")
                        except ValueError:
                            parsed = None
                    if parsed is None:
                        issues.append({"row": index, "issue": f"invalid date in {key}", "suggested_correction": "Review date and standardize to DD/MM/YYYY", "confidence": "medium"})
                    else:
                        copy[key] = parsed.strftime("%d/%m/%Y")
                else:
                    issues.append({"row": index, "issue": f"inconsistent date format in {key}", "suggested_correction": "Standardize to DD/MM/YYYY", "confidence": "medium"})
            elif any(token in low for token in ("amount", "revenue", "expense", "cost", "cash", "balance", "price", "budget")):
                converted = normalize_number(text)
                if converted == text:
                    issues.append({"row": index, "issue": f"inconsistent number format in {key}", "suggested_correction": "Review and standardize as numeric currency", "confidence": "medium"})
                else:
                    copy[key] = converted
        normalized.append(copy)
    return {"source": str(path), "row_count": len(rows), "fields": fields, "normalized_rows": normalized, "data_issues": issues}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    report = inspect(Path(args.input))
    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"output": str(Path(args.output).resolve()), "rows": report["row_count"], "issues": len(report["data_issues"])}))

if __name__ == "__main__":
    main()
