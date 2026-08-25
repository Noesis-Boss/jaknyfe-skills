import unittest
from types import SimpleNamespace

from link_recovery import recover_application_url


class RecoveryTests(unittest.TestCase):
    def candidate(self):
        return {"scholarship_name": "Future Award", "application_url": "https://foundation.org/old", "sponsor_url": "https://foundation.org"}

    def test_redirect_cleanup_and_recovery(self):
        responses = {
            "https://foundation.org/old": SimpleNamespace(url="https://foundation.org/", status=200, title="Foundation", body="See our award", links=["/apply/future"]),
            "https://foundation.org/apply/future": SimpleNamespace(url="https://foundation.org/apply/future", status=200, title="Future Award Application", body="Submit your application before the deadline.", links=[]),
        }
        result = recover_application_url(self.candidate(), responses.__getitem__, lambda _: [])
        self.assertEqual(result["status"], "recovered")
        self.assertEqual(result["recovered_url"], "https://foundation.org/apply/future")

    def test_page_cap(self):
        seen = []
        def fetch(url):
            seen.append(url)
            return SimpleNamespace(url=url, status=200, title="Foundation", body="Directory", links=[f"/p{len(seen)+1}"])
        result = recover_application_url(self.candidate(), fetch, lambda _: [], max_pages=3)
        self.assertEqual(len(result["attempts"]), 3)

    def test_query_cap(self):
        queries = []
        result = recover_application_url({"scholarship_name": "Award", "application_url": "https://foundation.org/missing", "sponsor_url": "https://foundation.org"}, lambda _: (_ for _ in ()).throw(RuntimeError("offline")), lambda query: queries.append(query) or [], max_pages=1, max_queries=2)
        self.assertEqual(len(queries), 2)
        self.assertEqual(result["status"], "not_recovered")

    def test_timeout(self):
        ticks = iter([0, 61, 61, 61])
        result = recover_application_url(self.candidate(), lambda _: None, lambda _: [], clock=lambda: next(ticks), budget_seconds=60)
        self.assertEqual(result["status"], "timeout")


if __name__ == "__main__":
    unittest.main()
