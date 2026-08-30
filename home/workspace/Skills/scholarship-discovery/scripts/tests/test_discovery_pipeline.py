import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discovery_pipeline import run_discovery


class Response:
    def __init__(self, url, body):
        self.url, self.status, self.content_type, self.body, self.title, self.links = url, 200, "text/html", body, "Cancer Pathways Teen Writing Contest", []


def test_recovered_url_is_verified_before_counting():
    candidate = {"scholarship_name": "Cancer Pathways Teen Writing Contest", "organization": "Cancer Pathways", "application_url": "https://cancerpathways.org/old", "sponsor_url": "https://cancerpathways.org", "deadline": "2026-12-01"}
    def fetcher(url):
        if url.endswith("/old"):
            raise RuntimeError("gone")
        return Response(url, "Cancer Pathways Teen Writing Contest Apply application deadline")
    report = run_discovery([candidate], 10, fetcher, lambda _: ["https://cancerpathways.org/programs/teen-writing-contest/"])
    assert report["verified"] == 1
    assert report["recovered"] == 1


if __name__ == "__main__":
    test_recovered_url_is_verified_before_counting()
    print("pipeline fixture passed")
