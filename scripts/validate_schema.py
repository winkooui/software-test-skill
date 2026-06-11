#!/usr/bin/env python3
"""Validate repository JSON files and bundled CSV examples."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


CASE_ID_PATTERN = re.compile(r"^TC-[A-Z]{2,6}-\d{2}-\d{3}-[FIPSCUENR]$")
CASE_REQUIRED = [
    "id",
    "module",
    "function",
    "type",
    "priority",
    "name",
    "precondition",
    "steps",
    "test_data",
    "data_prep_method",
    "expected_result",
]
EXEC_REQUIRED = ["case_id", "status"]
EXEC_STATUSES = {"通过", "失败", "阻塞", "跳过", "未执行"}
CASE_TYPES = {"功能测试", "接口测试", "性能测试", "安全测试", "兼容性测试", "用户体验测试", "用户视角测试", "回归测试"}
PRIORITIES = {"P0", "P1", "P2", "P3"}
PROXIMITY_LEVELS = {"高", "中", "低", "微", "无关"}
REGRESSION_DEPTHS = {"全量", "重点", "冒烟", "极简"}


def load_json(path: Path) -> None:
    with path.open(encoding="utf-8") as file:
        json.load(file)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def validate_case_csv(path: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()
    for index, row in enumerate(read_csv(path), start=2):
        for field in CASE_REQUIRED:
            if not row.get(field):
                errors.append(f"{path}:{index}: missing {field}")
        if row.get("id") and not CASE_ID_PATTERN.match(row["id"]):
            errors.append(f"{path}:{index}: invalid id {row['id']}")
        if row.get("id") in seen_ids:
            errors.append(f"{path}:{index}: duplicate id {row['id']}")
        if row.get("id"):
            seen_ids.add(row["id"])
        if row.get("type") and row["type"] not in CASE_TYPES:
            errors.append(f"{path}:{index}: invalid type {row['type']}")
        if row.get("priority") and row["priority"] not in PRIORITIES:
            errors.append(f"{path}:{index}: invalid priority {row['priority']}")
        if row.get("type") == "用户视角测试" and not row.get("user_perspective_tag"):
            errors.append(f"{path}:{index}: user perspective case must include user_perspective_tag")
        if row.get("type") == "用户视角测试" and not row.get("user_persona"):
            errors.append(f"{path}:{index}: user perspective case must include user_persona")
        if row.get("is_regression") == "true":
            if not row.get("proximity_level"):
                errors.append(f"{path}:{index}: regression case must include proximity_level")
            elif row["proximity_level"] not in PROXIMITY_LEVELS:
                errors.append(f"{path}:{index}: invalid proximity_level {row['proximity_level']}")
            if not row.get("regression_depth"):
                errors.append(f"{path}:{index}: regression case must include regression_depth")
            elif row["regression_depth"] not in REGRESSION_DEPTHS:
                errors.append(f"{path}:{index}: invalid regression_depth {row['regression_depth']}")
    return errors


def validate_execution_csv(path: Path) -> list[str]:
    errors: list[str] = []
    seen_case_ids: set[str] = set()
    for index, row in enumerate(read_csv(path), start=2):
        for field in EXEC_REQUIRED:
            if not row.get(field):
                errors.append(f"{path}:{index}: missing {field}")
        if row.get("case_id") and not CASE_ID_PATTERN.match(row["case_id"]):
            errors.append(f"{path}:{index}: invalid case_id {row['case_id']}")
        if row.get("case_id") in seen_case_ids:
            errors.append(f"{path}:{index}: duplicate case_id {row['case_id']}")
        if row.get("case_id"):
            seen_case_ids.add(row["case_id"])
        if row.get("status") not in EXEC_STATUSES:
            errors.append(f"{path}:{index}: invalid status {row.get('status')}")
        if row.get("status") == "失败" and not row.get("bug_id"):
            errors.append(f"{path}:{index}: failed record must include bug_id")
        if row.get("status") == "阻塞" and not row.get("actual_result_detail"):
            errors.append(f"{path}:{index}: blocked record must include actual_result_detail")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate schema files and examples.")
    parser.add_argument("--root", default=".", help="Repository root.")
    parser.add_argument("--case-csv", action="append", default=[], help="Additional or replacement test case CSV to validate.")
    parser.add_argument("--execution-csv", action="append", default=[], help="Additional or replacement execution CSV to validate.")
    args = parser.parse_args()
    root = Path(args.root)

    for path in [
        root / "core/schemas/test-case-record.schema.json",
        root / "core/schemas/test-execution-record.schema.json",
        root / "core/templates/excel-schema.json",
        root / "core/templates/chart-specs.json",
    ]:
        load_json(path)

    case_csvs = [Path(path) for path in args.case_csv] or [root / "examples/sample-test-cases.csv"]
    execution_csvs = [Path(path) for path in args.execution_csv] or [root / "examples/execution-records.csv"]

    errors = []
    for path in case_csvs:
        errors.extend(validate_case_csv(path))
    for path in execution_csvs:
        errors.extend(validate_execution_csv(path))

    if errors:
        for error in errors:
            print(error)
        return 1
    print("Schema and example validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
