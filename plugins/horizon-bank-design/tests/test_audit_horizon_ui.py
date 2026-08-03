from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
AUDITOR = PLUGIN / "skills" / "audit-horizon-bank-ui" / "scripts" / "audit_horizon_ui.py"


class HorizonWebAuditTests(unittest.TestCase):
    def test_reports_when_no_web_audit_was_performed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="horizon-web-audit-") as temp:
            source = Path(temp) / "ExampleView.swift"
            source.write_text("import SwiftUI\nstruct ExampleView: View {}\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(AUDITOR), str(source), "--strict", "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["scope"], "web_source")
        self.assertFalse(report["audited"])
        self.assertEqual(report["files_scanned"], 0)
        self.assertIn("no web audit was performed", report["message"].lower())

    def test_reports_a_supported_web_scan(self) -> None:
        with tempfile.TemporaryDirectory(prefix="horizon-web-audit-") as temp:
            source = Path(temp) / "example.css"
            source.write_text(".example { color: #141414; }\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(AUDITOR), str(source), "--strict", "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["audited"])
        self.assertEqual(report["files_scanned"], 1)
        self.assertIsNone(report["message"])


if __name__ == "__main__":
    unittest.main()
