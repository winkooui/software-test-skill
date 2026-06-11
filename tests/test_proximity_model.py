from __future__ import annotations

import unittest

from scripts.proximity_model import calculate_proximity, classify_score


class ProximityModelTest(unittest.TestCase):
    def test_classifies_boundaries(self) -> None:
        self.assertEqual(classify_score(4.0), ("高", "全量", "100%"))
        self.assertEqual(classify_score(2.0), ("中", "重点", ">=70%"))
        self.assertEqual(classify_score(1.0), ("低", "冒烟", ">=50%"))
        self.assertEqual(classify_score(0.1), ("微", "极简", "采样"))
        self.assertEqual(classify_score(0.0), ("无关", "核心冒烟", "关键路径"))

    def test_weighted_score(self) -> None:
        result = calculate_proximity(code=4, data=4, api=3, business=4, ui=2)
        self.assertEqual(result.score, 3.6)
        self.assertEqual(result.level, "中")
        self.assertEqual(result.regression_depth, "重点")

    def test_calibration_rules_raise_score(self) -> None:
        result = calculate_proximity(
            code=2,
            data=2,
            api=2,
            business=2,
            ui=2,
            historical_hotspot=True,
            payment_or_money=True,
        )
        self.assertEqual(result.score, 4.0)
        self.assertEqual(result.level, "高")

    def test_ddl_change_forces_high(self) -> None:
        result = calculate_proximity(code=0, data=0, api=0, business=0, ui=0, ddl_change=True)
        self.assertEqual(result.score, 4.0)
        self.assertEqual(result.level, "高")

    def test_rejects_invalid_dimension(self) -> None:
        with self.assertRaises(ValueError):
            calculate_proximity(code=6, data=0, api=0, business=0, ui=0)


if __name__ == "__main__":
    unittest.main()
