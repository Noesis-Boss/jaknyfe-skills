import unittest
from types import SimpleNamespace
from verification import is_application_page, is_search_aggregator, verify_candidate

class VerificationTests(unittest.TestCase):
    def test_aggregator_rejected(self):
        self.assertTrue(is_search_aggregator("https://www.scholarships.com/a"))
        result = verify_candidate({"application_url": "https://bold.org/a"}, lambda _: None)
        self.assertEqual(result["score"], "reject")

    def test_official_application_accepted(self):
        response = SimpleNamespace(url="https://foundation.org/apply/award", status=200, content_type="text/html", title="Award Application", body="Submit your application before the deadline.", links=[])
        result = verify_candidate({"scholarship_name": "Future Award", "application_url": response.url, "deadline": "2027-01-01"}, lambda _: response)
        self.assertEqual(result["status"], "verified")
        self.assertEqual(result["score"], "A")

    def test_generic_homepage_and_installer_do_not_pass(self):
        homepage = SimpleNamespace(url="https://foundation.org/", status=200, content_type="text/html", title="Foundation", body="Welcome to our foundation.", links=[])
        installer = SimpleNamespace(url="https://foundation.org/app.apk", status=200, content_type="application/octet-stream", title="Installer", body="", links=[])
        self.assertEqual(verify_candidate({"scholarship_name": "Award", "application_url": homepage.url}, lambda _: homepage)["score"], "C")
        self.assertEqual(verify_candidate({"scholarship_name": "Award", "application_url": installer.url}, lambda _: installer)["score"], "reject")

if __name__ == "__main__":
    unittest.main()
