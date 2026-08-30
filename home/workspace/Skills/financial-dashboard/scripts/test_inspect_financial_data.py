import json
import tempfile
import unittest
from pathlib import Path
from inspect_financial_data import inspect

class InspectionTests(unittest.TestCase):
    def write(self, text):
        file = tempfile.NamedTemporaryFile(suffix=".csv", delete=False, mode="w", encoding="utf-8")
        file.write(text)
        file.close()
        return Path(file.name)

    def test_normalizes_dates_and_currency(self):
        report = inspect(self.write('date,revenue,category\n2026-01-02,"$1,200",Sales\n'))
        self.assertEqual(report["normalized_rows"][0]["date"], "02/01/2026")

    def test_reports_blank_and_duplicate_rows(self):
        report = inspect(self.write("date,amount,category\n2026-01-02,10,\n2026-01-02,10,\n"))
        issue_text = [item["issue"] for item in report["data_issues"]]
        self.assertIn("blank value in category", issue_text)
        self.assertIn("duplicate row", issue_text)

if __name__ == "__main__":
    unittest.main()
