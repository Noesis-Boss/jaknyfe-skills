#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080
BG = (10, 18, 32)
WHITE = (240, 245, 250)
MUTED = (155, 174, 196)
CYAN = (47, 211, 190)
GOLD = (255, 190, 74)
RED = (255, 100, 105)

def font(size, bold=False):
    path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)

def wrap(draw, text, f, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        test = f"{line} {word}".strip()
        if draw.textbbox((0, 0), test, font=f)[2] <= max_width:
            line = test
        else:
            lines.append(line); line = word
    if line: lines.append(line)
    return lines

def card(path, title, bullets, accent=CYAN, number=None, chart=False):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 80): d.line((x, 0, x, H), fill=(18, 34, 52), width=1)
    for y in range(0, H, 80): d.line((0, y, W, y), fill=(18, 34, 52), width=1)
    d.rectangle((0, 0, 26, H), fill=accent)
    d.text((110, 90), "NOĒSIS  /  FINANCE BREAKDOWN", font=font(25, True), fill=accent)
    d.text((110, 150), title, font=font(70, True), fill=WHITE)
    y = 300
    for bullet in bullets:
        d.ellipse((115, y + 12, 139, y + 36), fill=accent)
        lines = wrap(d, bullet, font(34), 910)
        for line in lines:
            d.text((165, y), line, font=font(34), fill=WHITE); y += 50
        y += 28
    if number:
        d.rounded_rectangle((1180, 285, 1780, 560), 24, fill=(18, 38, 57), outline=accent, width=4)
        d.text((1250, 340), number[0], font=font(34, True), fill=MUTED)
        d.text((1245, 395), number[1], font=font(86, True), fill=accent)
        d.text((1250, 500), number[2], font=font(26), fill=WHITE)
    if chart:
        pts = [(1190, 850), (1300, 790), (1400, 815), (1500, 675), (1610, 710), (1740, 520)]
        d.line(pts, fill=accent, width=10, joint="curve")
        for x, y2 in pts: d.ellipse((x-12, y2-12, x+12, y2+12), fill=GOLD)
        d.text((1190, 895), "Illustrative direction of borrowing pressure", font=font(24), fill=MUTED)
    d.text((110, 1010), "Educational example — not financial advice", font=font(23), fill=MUTED)
    im.save(path)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", required=True)
    args = ap.parse_args()
    mpath = Path(args.manifest).resolve(); m = json.loads(mpath.read_text())
    root = mpath.parent; visual = root / "visuals"; audio = root / "audio"; visual.mkdir(exist_ok=True)
    total = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(audio / "narration-long.mp3")], text=True))
    specs = [
        ("01-hook.png", "Your loan rate is not set in one place", ["The Fed controls overnight money", "Bond investors influence longer-term borrowing", "That difference reaches ordinary households"], GOLD, ("10-YEAR TREASURY", "4.74%", "reported level in brief"), True),
        ("02-rates.png", "Two rates. Two different jobs.", ["Fed funds rate: short-term policy lever", "10-year Treasury: market pricing benchmark", "Mortgage rates often track the longer end"], CYAN, ("WATCH THE", "10-YEAR", "Treasury yield"), True),
        ("03-mortgage.png", "Small rate changes compound", ["Example: $300,000, 30-year mortgage", "A higher rate means a higher monthly payment", "This is an illustration — not a quote or forecast"], GOLD, ("EXAMPLE LOAN", "$300K", "30-year term"), False),
        ("04-chain.png", "The borrowing-cost relay", ["Bond yield rises", "Lender funding cost changes", "Loan pricing and credit terms can follow"], CYAN, ("THE CHAIN", "YIELD →", "FUNDING → LOAN"), True),
        ("05-pressure.png", "Why investors may demand more yield", ["Inflation uncertainty", "Oil and geopolitical risk", "Government borrowing and supply of debt", "Markets price risk before borrowers feel it"], RED, ("PRESSURE", "RISK", "gets repriced"), True),
        ("06-checklist.png", "What to monitor next", ["10-year Treasury yield", "Your lender’s actual quote", "Inflation data and credit terms", "Never confuse an example with a prediction"], GOLD, ("FOUR", "SIGNALS", "to compare"), False),
    ]
    for spec in specs: card(visual / spec[0], *spec[1:])
    weights = [0.14, 0.17, 0.18, 0.17, 0.18, 0.16]
    durations = [round(total * x, 3) for x in weights]; durations[-1] = round(total - sum(durations[:-1]), 3)
    scenes = []
    start = 0.0
    for i, (spec, duration) in enumerate(zip(specs, durations)):
        out = audio / f"scene-{i+1:02d}.mp3"
        subprocess.run(["ffmpeg", "-y", "-ss", f"{start:.3f}", "-i", str(audio / "narration-long.mp3"), "-t", f"{duration:.3f}", "-c", "copy", str(out)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        scenes.append({"image": str(visual / spec[0]), "audio": str(out), "duration": duration, "motion": "ken-burns"})
        start += duration
    m["scenes"] = scenes; m["visual_style"] = "animated-evidence-cards"; m["motion"] = {"type": "ken-burns", "zoom": "1.00-1.10", "pan": "alternating"}
    mpath.write_text(json.dumps(m, indent=2) + "\n")
    print(mpath)

if __name__ == "__main__": main()
