#!/usr/bin/env python3
"""Generate working university financial aid scholarship URLs and append to batch_queue.json."""
import json, os, re, requests
from concurrent.futures import ThreadPoolExecutor, as_completed

QUEUE_PATH = "/home/workspace/Skills/scholarship-discovery/scripts/batch_queue.json"

# A broad list of US university short names / domains
UNIS = [
    "harvard","stanford","mit","yale","princeton","columbia","brown","dartmouth","cornell","upenn",
    "duke","northwestern","johnshopkins","rice","vanderbilt","notredame","cmu","emory"," Georgetown","nyu",
    "usc","ucsd","ucsb","ucsc","ucr","uci","ucdavis","ucmerced","ucsf","ucla",
    "berkeley","wisc","umich","uiuc","uw","umn","psu","rutgers","indiana","osu",
    "miami","purdue","iowa","umn","msu","uky","ufl","gatech","ut Austin","tamu",
    "ucsb","ucsd","ucsf","ucr","uci","ucdavis","ucmerced","ucsc","ucsb","ucsd",
    "colorado","arizona","asu","ualberta","ubc","toronto","mcgill","waterloo","ottawa","calgary",
    "oxford","cambridge","imperial","ucl","edinburgh","manchester","kcl","bristol","warwick","durham",
    "eth","epfl","munich","heidelberg","humboldt","copenhagen","stockholm","oslo","helsinki","leiden",
    "sydney","melbourne","anu","auckland","otago","canterbury","mcgill","toronto","ubc","waterloo",
    "buffalo","stonybrook","albany","binghamton","hofstra","fordham","syracuse","bostoncollege","brandeis","tufts",
    "georgetown","american","gwu","jhu","george washington","rice","tulane","vanderbilt","wakeforest","davidson",
    "colgate","hamilton","middlebury","bowdoin","bates","colby","conncoll","trinity","wesleyan","amherst",
    "williams","swarthmore","haverford","brynmawr","gettysburg","lafayette","lehigh","bucknell","dickinson","fandm",
    "oberlin","denison","kenyon","wooster","wittenberg","marietta","ohiou","cincy","miamioh","wright",
    "ku","kstate","wsu","umn","msu","iowastate","ndsu","sdsu","unl","ou",
    "arizona","arizonastate","newmexico","unm","byu","usu","usu","montana","wyoming","coloradostate",
    "utah","usu","idaho","boisestate","portlandstate","oregonstate","uoregon","uw","wsu","wwu",
    "msstate","olemiss","alabama","auburn","georgia","uga","clemson","usouthcarolina","unc","duke",
    "vcu","virginiatech","williamandmary","jmu","odu","richmond","wfu","elon","appstate","uncw",
    "fiu","fsu","umiami","ucf","usf","unf","fgcu","fau","ncu","ecu",
    "tulane","lsu","southern","baylor","tamu","rice","houston","utsa","unt","tcu",
    "okstate","ou","tulsa","ucoklahoma","wvu","kentucky","uk","tennessee","utk","vanderbilt",
    "indiana","purdue","notredame","iowa","iowastate","umn","wisc","msu","umich","osu",
    "psu","rutgers","nyu","columbia","cornell","brown","dartmouth","yale","harvard","princeton",
    "stanford","berkeley","ucla","ucsd","ucsb","ucsc","ucr","uci","ucdavis","ucmerced",
    "seattleu","gonzaga","portland","pacific","loyola","pepperdine","santa clara","usf","stmarys","jhu",
    "georgetown","howard","spelman","hampton","fisk","morehouse","xavier","dillard","clark"," tuskegee",
    "alcorn","jacksonstate","msvcu","ncatsu","scstate","uapb","uicc","vsu","wssu","morgan",
    "calpoly","sjsu","csun","cpp","fullerton","longbeach","dominguez","eastbay","maritime","monterey",
    "sonoma","humboldt","sacramento","sfstate","stanislaus","channel islands","pomona","whittier","claremont","scripps",
    "oxy","redlands","chapman","loyolamarymount","pepperdine","saddleback","irvine","cerritos","cypress","fullerton",
    "grossmont","miramar","palomar","riverside","sanjacinto","santiago","shasta","solano","ventura","westhil"
]

PATTERNS = [
    "https://financialaid.{uni}.edu/scholarships",
    "https://www.{uni}.edu/financial-aid/scholarships",
    "https://studentaid.{uni}.edu/scholarships",
    "https://onestop.{uni}.edu/scholarships",
    "https://sfs.{uni}.edu/scholarships",
    "https://scholarships.{uni}.edu/",
]

def check_url(url):
    try:
        r = requests.get(url, timeout=8, allow_redirects=True, headers={"User-Agent":"Mozilla/5.0"})
        if r.status_code == 200:
            return url
    except Exception:
        pass
    return None

def main():
    with open(QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)
    existing = {src.get("url") for src in queue if src.get("url")}
    new_sources = []
    seen = set()
    urls = []
    for uni in UNIS:
        uni = uni.strip().replace(" ", "").lower()
        if uni in seen:
            continue
        seen.add(uni)
        for pat in PATTERNS:
            url = pat.format(uni=uni)
            if url in existing or url in [u for u in urls]:
                continue
            urls.append(url)

    print(f"Testing {len(urls)} candidate URLs...")
    with ThreadPoolExecutor(max_workers=20) as pool:
        futures = {pool.submit(check_url, u): u for u in urls}
        for fut in as_completed(futures):
            url = futures[fut]
            result = fut.result()
            if result:
                new_sources.append({
                    "id": f"src-uni-{len(new_sources)+1:04d}",
                    "group": "usa_edu",
                    "url": result,
                    "pri": 10,
                    "last_scraped": None,
                    "last_batch_count": 0,
                    "age_score": 999999
                })
                if len(new_sources) >= 120:
                    break

    print(f"Found {len(new_sources)} working new URLs")
    queue.extend(new_sources)
    with open(QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)
    print(f"Queue updated to {len(queue)} sources")

if __name__ == "__main__":
    main()
