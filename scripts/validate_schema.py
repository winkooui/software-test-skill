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


def load_json(path: Path) -> None:
    with path.open(encoding="utf-8") as file:
        json.load(file)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def validate_case_csv(path: Path) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(read_csv(path), start=2):
        for field in CASE_REQUIRED:
            if not row.get(field):
                errors.append(f"{path}:{index}: missing {field}")
        if row.get("id") and not CASE_ID_PATTERN.match(row["id"]):
            errors.append(f"{path}:{index}: invalid id {row['id']}")
        if row.get("type") == "用户视角测试" and not row.get("user_perspective_tag"):
            errors.append(f"{path}:{index}: user perspective case must include user_perspective_tag")
        if row.get("is_regression") == "true" and not row.get("proximity_level"):
            errors.append(f"{path}:{index}: regression case must include proximity_level")
    return errors


def validate_execution_csv(path: Path) -> list[str]:
    errors: list[str] = []
    for index, row in enumerate(read_csv(path), start=2):
        for field in EXEC_REQUIRED:
            if not row.get(field):
                errors.append(f"{path}:{index}: missing {field}")
        if row.get("case_id") and not CASE_ID_PATTERN.match(row["case_id"]):
            errors.append(f"{path}:{index}: invalid case_id {row['case_id']}")
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
    args = parser.parse_args()
    root = Path(args.root)

    for path in [
        root / "core/schemas/test-case-record.schema.json",
        root / "core/schemas/test-execution-record.schema.json",
        root / "core/templates/excel-schema.json",
        root / "core/templates/chart-specs.json",
    ]:
        load_json(path)

    errors = []
    errors.extend(validate_case_csv(root / "examples/sample-test-cases.csv"))
    errors.extend(validate_execution_csv(root / "examples/execution-records.csv"))

    if errors:
        for error in errors:
            print(error)
        return 1
    print("Schema and example validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
