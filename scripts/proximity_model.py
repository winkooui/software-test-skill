#!/usr/bin/env python3
"""Deterministic proximity scoring helpers used by docs and tests."""

from __future__ import annotations

from dataclasses import dataclass


WEIGHTS = {
    "code": 0.30,
    "data": 0.25,
    "api": 0.20,
    "business": 0.15,
    "ui": 0.10,
}


@dataclass(frozen=True)
class ProximityResult:
    score: float
    level: str
    regression_depth: str
    coverage: str


def _validate_dimension(name: str, value: float) -> None:
    if value < 0 or value > 5:
        raise ValueError(f"{name} score must be between 0 and 5: {value}")


def classify_score(score: float) -> tuple[str, str, str]:
    if score >= 4.0:
        return "高", "全量", "100%"
    if score >= 2.0:
        return "中", "重点", ">=70%"
    if score >= 1.0:
        return "低", "冒烟", ">=50%"
    if score > 0:
        return "微", "极简", "采样"
    return "无关", "核心冒烟", "关键路径"


def calculate_proximity(
    *,
    code: float,
    data: float,
    api: float,
    business: float,
    ui: float,
    historical_hotspot: bool = False,
    payment_or_money: bool = False,
    middleware_change: bool = False,
    ddl_change: bool = False,
) -> ProximityResult:
    """Calculate weighted proximity and apply calibration rules."""

    dimensions = {
        "code": code,
        "data": data,
        "api": api,
        "business": business,
        "ui": ui,
    }
    for name, value in dimensions.items():
        _validate_dimension(name, value)

    if ddl_change:
        score = 4.0
    else:
        score = sum(dimensions[name] * weight for name, weight in WEIGHTS.items())
        calibration = sum([historical_hotspot, payment_or_money, middleware_change])
        score = min(5.0, score + calibration)

    level, regression_depth, coverage = classify_score(score)
    return ProximityResult(round(score, 2), level, regression_depth, coverage)


if __name__ == "__main__":
    result = calculate_proximity(code=4, data=4, api=3, business=4, ui=2)
    print(f"{result.score},{result.level},{result.regression_depth},{result.coverage}")
