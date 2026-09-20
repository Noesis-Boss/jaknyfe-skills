#!/usr/bin/env python3
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

RULES = {
    "significance inflation": re.compile(r"\b(?:pivotal|testament|crucial role|setting the stage|indelible mark)\b", re.I),
    "binary contrast": re.compile(r"\b(?:is|was|are|were)\s+not\b[^.?!]*[.!?]\s*\b(?:it|that|this)\s+(?:is|was|are|were)\b", re.I),
    "faux-insight setup": re.compile(r"\b(?:what nobody tells you|the part everyone misses|what most people get wrong)\b", re.I),
    "vague attribution": re.compile(r"\b(?:industry experts|observers|some critics|studies|research)\s+(?:believe|have noted|argue|show|suggest)\b", re.I),
    "fabricated personal authority": re.compile(r"\bI\s+(?:personally\s+)?(?:built|led|managed|tested|used)\b[^.!?]{0,120}\b(?:customers|clients|teams|companies|users)\b", re.I),
    "unsupported credentials or client results": re.compile(r"\b(?:as a|with a|as an)\s+(?:certified|licensed|award-winning|seasoned)\s+[^,.!?]{2,50},?\s+I\s+(?:helped|guided|advised|worked with)\s+\d+\s+(?:clients|customers|companies)\b|\bI\s+(?:helped|guided|advised)\s+\d+\s+(?:clients|customers|companies)\s+[^.!?]{0,80}\b(?:double|doubled|triple|tripled|increase|increased|grew)\b", re.I),
    "invented quote or source link": re.compile(r"(?:https?://(?:example\.invalid|[^\s)]+(?:utm_source=|chatgpt\.com))|\b(?:wrote|said|reported)\s+[^.!?]{0,80}\"[^\"]+\"\s*\([^)]*\b(?:review|report|study)\b)", re.I),
    "AI citation artifact": re.compile(r"(?:contentReference|oaicite|turn\d+search\d+|\[cite:\s*\d+\]|\[span_\d+\]|grok_card|ppl-ai-file-upload|utm_source=chatgpt\.com)", re.I),
    "unsupported date or timeline": re.compile(r"(?:\b(?:in|by|since)\s+20\d{2}\b[^.!?]{0,80}\bI\s+(?:started|launched|built|led|worked|founded)\b|\bI\s+(?:started|launched|built|led|worked|founded)\b[^.!?]{0,80}\b(?:in|by|since)\s+20\d{2}\b)", re.I),
}

class VisibleHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden_roots = []
        self.skip_depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"script", "style", "meta", "title", "head", "template"}:
            self.skip_depth += 1
        elif self.skip_depth == 0 and ("hidden" in attrs or attrs.get("aria-hidden") == "true" or re.search(r"(?:^|\s)(?:hidden|invisible)(?:\s|$)", attrs.get("class", ""), re.I)):
            self.hidden_roots.append(tag)

    def handle_endtag(self, tag):
        if tag in {"script", "style", "meta", "title", "head", "template"} and self.skip_depth:
            self.skip_depth -= 1
        elif self.hidden_roots and tag == self.hidden_roots[-1]:
            self.hidden_roots.pop()

    def handle_data(self, data):
        if self.skip_depth == 0 and not self.hidden_roots and data.strip():
            self.parts.append(data.strip())

def extract_html(text):
    parser = VisibleHTMLParser()
    parser.feed(text)
    return " ".join(parser.parts)

def extract_markdown(text):
    fenced = []
    def keep_fence(match):
        fenced.append(match.group(0))
        return f"\n@@CODEBLOCK{len(fenced) - 1}@@\n"
    text = re.sub(r"```[\s\S]*?```|~~~[\s\S]*?~~~", keep_fence, text)
    text = re.sub(r"^---\n[\s\S]*?\n---\n", "", text, count=1)
    text = re.sub(r"!\[([^]]*)\]\(([^)]+)\)", r"\1 \2", text)
    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 \2", text)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.M)
    text = re.sub(r"^\s{0,3}(?:[-*+] |\d+\. )", "", text, flags=re.M)
    text = re.sub(r"[*_~`]", "", text)
    for index, block in enumerate(fenced):
        text = text.replace(f"@@CODEBLOCK{index}@@", block)
    return re.sub(r"\s+", " ", text).strip()

def extract_visible_text(text, fmt):
    if fmt == "html":
        return extract_html(text)
    if fmt == "markdown":
        return extract_markdown(text)
    return text

def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "--file":
        if len(sys.argv) < 3:
            print("usage: run_fixtures.py [--file PATH [--format plain|html|markdown]]")
            return 2
        path = Path(sys.argv[2])
        fmt = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--format" else path.suffix.removeprefix(".").lower()
        if fmt not in {"plain", "html", "markdown", "md"}:
            print(f"unsupported format: {fmt}")
            return 2
        print(extract_visible_text(path.read_text(), "markdown" if fmt == "md" else fmt))
        return 0
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
    extraction_cases = json.loads(Path(__file__).with_name("extraction_cases.json").read_text())
    for case in extraction_cases:
        actual = extract_visible_text(case["input"], case["format"])
        if actual != case["expected"]:
            failures.append(f'{case["id"]}: expected {case["expected"]!r}, got {actual!r}')
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print(f"PASS: {len(cases)} detector cases, {len(cases) * 2} passages, {len(extraction_cases)} extraction cases")
    return 0

if __name__ == "__main__":
    sys.exit(main())
