#!/usr/bin/env python3
"""Evaluate generated test cases against a lightweight quality rubric."""

from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from pathlib import Path


CORE_TYPES = {"功能测试", "接口测试", "安全测试", "异常边界测试", "回归测试"}


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def evaluate_cases(rows: list[dict[str, str]]) -> tuple[int, list[str]]:
    score = 100
    findings: list[str] = []
    total = len(rows)
    if total == 0:
        return 0, ["no test cases found"]

    by_function: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        by_function[row.get("function", "未分类")].append(row)

    p0_count = sum(1 for row in rows if row.get("priority") == "P0")
    user_cases = [row for row in rows if row.get("type") == "用户视角测试"]
    regression_cases = [row for row in rows if row.get("is_regression") == "true"]
    prod_gate_cases = [row for row in rows if row.get("prod_gate") == "true"]
    type_counter = Counter(row.get("type", "") for row in rows)

    if p0_count == 0:
        score -= 15
        findings.append("missing P0 cases")
    if not user_cases:
        score -= 10
        findings.append("missing user perspective cases")
    if not regression_cases:
        score -= 10
        findings.append("missing regression cases")
    if not prod_gate_cases:
        score -= 10
        findings.append("missing production gate cases")
    if len(set(type_counter) & CORE_TYPES) < 3:
        score -= 10
        findings.append("less than three core test types covered")

    for function, function_rows in sorted(by_function.items()):
        type_count = len({row.get("type") for row in function_rows if row.get("type")})
        if type_count < 1:
            score -= 5
            findings.append(f"{function}: no test type coverage")
        if any(not row.get("test_data") for row in function_rows):
            score -= 5
            findings.append(f"{function}: missing test data")
        if any(not row.get("expected_result") for row in function_rows):
            score -= 5
            findings.append(f"{function}: missing expected result")

    return max(0, score), findings


def write_report(path: Path, score: int, findings: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        file.write("# 测试用例质量评估\n\n")
        file.write(f"- 评分: {score}/100\n")
        if findings:
            file.write("- 结论: 需要补充\n\n")
            file.write("## Findings\n\n")
            for finding in findings:
                file.write(f"- {finding}\n")
        else:
            file.write("- 结论: 通过\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate generated test cases against a quality rubric.")
    parser.add_argument("--input", default="examples/sample-test-cases.csv", help="Path to test case CSV.")
    parser.add_argument("--output", default="", help="Optional markdown report path.")
    parser.add_argument("--min-score", type=int, default=75, help="Minimum accepted score.")
    args = parser.parse_args()

    score, findings = evaluate_cases(read_rows(Path(args.input)))
    if args.output:
        write_report(Path(args.output), score, findings)
    print(f"quality_score={score}")
    for finding in findings:
        print(f"- {finding}")
    return 0 if score >= args.min_score else 1


if __name__ == "__main__":
    raise SystemExit(main())
