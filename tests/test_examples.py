from __future__ import annotations

import csv
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ExampleArtifactsTest(unittest.TestCase):
    def test_sample_test_cases_have_required_fields(self) -> None:
        path = ROOT / "examples/sample-test-cases.csv"
        with path.open(encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        self.assertGreaterEqual(len(rows), 5)
        for row in rows:
            self.assertTrue(row["id"].startswith("TC-"))
            self.assertTrue(row["name"])
            self.assertIn(row["priority"], {"P0", "P1", "P2", "P3"})

    def test_execution_records_include_failure_bug_ids(self) -> None:
        path = ROOT / "examples/execution-records.csv"
        with path.open(encoding="utf-8") as file:
            rows = list(csv.DictReader(file))
        failed = [row for row in rows if row["status"] == "失败"]
        self.assertGreaterEqual(len(failed), 1)
        for row in failed:
            self.assertTrue(row["bug_id"])

    def test_validate_schema_script(self) -> None:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_schema.py"), "--root", str(ROOT)],
            check=False,
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_demo_generation_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            case_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/generate_test_cases.py"),
                    "--input",
                    str(ROOT / "examples/prd-login.md"),
                    "--out-dir",
                    str(out_dir),
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(case_result.returncode, 0, case_result.stdout + case_result.stderr)
            self.assertTrue((out_dir / "login-test-cases.csv").exists())
            self.assertTrue((out_dir / "login-test-cases.md").exists())

            report_result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/generate_report.py"),
                    "--input",
                    str(ROOT / "examples/execution-records.csv"),
                    "--out-dir",
                    str(out_dir),
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(report_result.returncode, 0, report_result.stdout + report_result.stderr)
            self.assertTrue((out_dir / "login-test-report.md").exists())
            self.assertTrue((out_dir / "login-report-summary.csv").exists())


if __name__ == "__main__":
    unittest.main()
