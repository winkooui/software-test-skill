from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ValidationNegativeTest(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / "scripts/validate_schema.py"), "--root", str(ROOT), *args],
            check=False,
            text=True,
            capture_output=True,
        )

    def test_rejects_failed_execution_without_bug_id(self) -> None:
        result = self.run_validator(
            "--execution-csv",
            str(ROOT / "examples/bad-inputs/execution-missing-bug.csv"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("failed record must include bug_id", result.stdout)

    def test_rejects_invalid_execution_status(self) -> None:
        result = self.run_validator(
            "--execution-csv",
            str(ROOT / "examples/bad-inputs/execution-invalid-status.csv"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid status", result.stdout)

    def test_rejects_invalid_case_file(self) -> None:
        result = self.run_validator(
            "--case-csv",
            str(ROOT / "examples/bad-inputs/test-cases-invalid.csv"),
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("invalid id", result.stdout)
        self.assertIn("regression case must include proximity_level", result.stdout)


if __name__ == "__main__":
    unittest.main()
