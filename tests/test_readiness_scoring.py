from __future__ import annotations

import unittest

from scripts.generate_report import conclusion, readiness_score


class ReadinessScoringTest(unittest.TestCase):
    def test_all_passed_scores_ready(self) -> None:
        records = [
            {"priority": "P0", "status": "通过", "bug_severity": "", "bug_id": ""},
            {"priority": "P1", "status": "通过", "bug_severity": "", "bug_id": ""},
        ]
        score, risks = readiness_score(records)
        self.assertEqual(score, 100)
        self.assertEqual(risks, [])
        self.assertEqual(conclusion(score, risks), "通过")

    def test_p0_failure_and_fatal_bug_reduce_score(self) -> None:
        records = [
            {"priority": "P0", "status": "失败", "bug_severity": "致命", "bug_id": "BUG-1"},
            {"priority": "P1", "status": "阻塞", "bug_severity": "", "bug_id": ""},
            {"priority": "P2", "status": "失败", "bug_severity": "严重", "bug_id": "BUG-2"},
        ]
        score, risks = readiness_score(records)
        self.assertEqual(score, 82)
        self.assertTrue(any("P0" in risk for _, risk, _ in risks))
        self.assertTrue(any("BUG-1" in risk for _, risk, _ in risks))
        self.assertEqual(conclusion(score, risks), "有条件通过")

    def test_low_score_blocks_release(self) -> None:
        records = [
            {"priority": "P0", "status": "失败", "bug_severity": "致命", "bug_id": f"BUG-{index}"}
            for index in range(4)
        ]
        score, risks = readiness_score(records)
        self.assertEqual(score, 48)
        self.assertEqual(conclusion(score, risks), "不通过")


if __name__ == "__main__":
    unittest.main()
