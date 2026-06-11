from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BenchmarkTest(unittest.TestCase):
    def test_login_benchmark_metadata(self) -> None:
        benchmark = json.loads((ROOT / "benchmarks/login/expected-coverage.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(benchmark["minimum_cases"], 5)
        self.assertIn("安全测试", benchmark["required_test_types"])
        self.assertGreaterEqual(benchmark["minimum_quality_score"], 75)

    def test_generated_login_cases_pass_quality_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            out_dir = Path(temp_dir)
            generate = subprocess.run(
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
            self.assertEqual(generate.returncode, 0, generate.stdout + generate.stderr)

            evaluate = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/evaluate_quality.py"),
                    "--input",
                    str(out_dir / "login-test-cases.csv"),
                    "--min-score",
                    "75",
                ],
                check=False,
                text=True,
                capture_output=True,
            )
            self.assertEqual(evaluate.returncode, 0, evaluate.stdout + evaluate.stderr)
            self.assertIn("quality_score=", evaluate.stdout)


if __name__ == "__main__":
    unittest.main()
