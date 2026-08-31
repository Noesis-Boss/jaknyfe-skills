import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discovery_pipeline import canonical_url, run_discovery


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


def test_canonical_url_removes_tracking_and_duplicate_application_urls():
    assert canonical_url("HTTPS://WWW.Example.org/app/?utm_source=x&b=2&a=1#form") == "https://example.org/app?a=1&b=2"
    first = {"scholarship_name": "One", "organization": "Sponsor A", "application_url": "https://example.org/app/?utm_campaign=x"}
    second = {"scholarship_name": "Different title", "organization": "Sponsor B", "application_url": "https://www.example.org/app/"}
    class Stable(Response):
        def __init__(self, url, body):
            super().__init__(url, body)
            self.title = "One application"
    report = run_discovery([first, second], 10, lambda url: Stable(url, "One scholarship apply deadline"), lambda _: [])
    assert report["verified"] == 1
    assert report["rejected"] == 1
    assert report["rejections"][0]["reason"] == "duplicate canonical application URL"


if __name__ == "__main__":
    test_recovered_url_is_verified_before_counting()
    test_canonical_url_removes_tracking_and_duplicate_application_urls()
    print("pipeline fixture passed")
