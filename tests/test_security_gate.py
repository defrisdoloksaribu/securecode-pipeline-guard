
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.security_gate import evaluate_report


class TestSecurityGate(unittest.TestCase):
    def test_passes_when_no_findings(self):
        self.assertEqual(self.run_report({"findings": []}), 0)

    def test_blocks_high_severity(self):
        report = {
            "findings": [
                {
                    "tool": "Bandit",
                    "severity": "HIGH",
                    "message": "Simulated high severity finding",
                }
            ]
        }
        self.assertEqual(self.run_report(report), 1)

    def test_blocks_critical_severity(self):
        report = {
            "findings": [
                {
                    "tool": "Scanner",
                    "severity": "CRITICAL",
                    "message": "Simulated critical finding",
                }
            ]
        }
        self.assertEqual(self.run_report(report), 1)

    def test_accepts_low_severity(self):
        report = {
            "findings": [
                {
                    "tool": "Bandit",
                    "severity": "LOW",
                    "message": "Simulated low severity finding",
                }
            ]
        }
        self.assertEqual(self.run_report(report), 0)

    def run_report(self, report):
        with TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"
            report_path.write_text(
                json.dumps(report),
                encoding="utf-8",
            )
            return evaluate_report(report_path)


if __name__ == "__main__":
    unittest.main()
