#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path

RULES = {
    "significance inflation": re.compile(r"\b(?:pivotal|testament|crucial role|setting the stage|indelible mark)\b", re.I),
    "binary contrast": re.compile(r"\b(?:is|was|are|were)\s+not\b[^.?!]*[.!?]\s*\b(?:it|that|this)\s+(?:is|was|are|were)\b", re.I),
    "faux-insight setup": re.compile(r"\b(?:what nobody tells you|the part everyone misses|what most people get wrong)\b", re.I),
    "vague attribution": re.compile(r"\b(?:industry experts|observers|some critics|studies|research)\s+(?:believe|have noted|argue|show|suggest)\b", re.I),
}

def main() -> int:
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    failures = []
    for case in cases:
        pattern = RULES.get(case["rule"])
        if pattern is None:
            failures.append(f'{case["id"]}: no detector rule')
            continue
        for label in ("failure", "human"):
            actual = "flag" if pattern.search(case[label]) else "clean"
            expected = case["expected"][label]
            if actual != expected:
                failures.append(f'{case["id"]}/{label}: expected {expected}, got {actual}')
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print(f"PASS: {len(cases)} cases, {len(cases) * 2} passages")
    return 0

if __name__ == "__main__":
    sys.exit(main())
