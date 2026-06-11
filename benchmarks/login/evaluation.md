# Login Benchmark Evaluation

## Purpose

This benchmark checks whether the skill can turn a compact login PRD into a
useful QA artifact instead of only producing generic happy-path test cases.

## Pass Criteria

| Dimension | Expected |
|-----------|----------|
| Minimum cases | 5 |
| Required functions | 账号密码登录, 错误次数锁定, 跳转恢复, 移动端体验 |
| Required test types | 功能测试, 安全测试, 回归测试, 用户视角测试 |
| Required gates | At least one Prod gate case |
| Required regression metadata | Regression cases include proximity level and regression depth |
| Minimum quality score | 75 |

## Suggested Commands

```bash
python scripts/generate_test_cases.py --input examples/prd-login.md --out-dir test-output
python scripts/evaluate_quality.py --input test-output/login-test-cases.csv --output test-output/login-quality.md
python scripts/validate_schema.py --root .
```
