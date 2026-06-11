# Contributing

Thanks for helping improve `software-test-skill`.

## Good First Contributions

- Add a realistic, sanitized PRD to `examples/`.
- Add execution records that exercise a new risk scenario.
- Improve scripts while keeping the no-network demo path working.
- Add platform adapter notes for another AI coding assistant.
- Tighten schema validation or test coverage.

## Development Workflow

1. Run the validation script:

   ```bash
   python scripts/validate_schema.py --root .
   python scripts/evaluate_quality.py --input examples/sample-test-cases.csv --min-score 75
   ```

2. Run tests:

   ```bash
   python -m unittest discover -s tests -v
   ```

3. Try the demo generation path:

   ```bash
   python scripts/generate_test_cases.py --input examples/prd-login.md --out-dir test-output
   python scripts/generate_report.py --input examples/execution-records.csv --out-dir test-output
   ```

## Contribution Guidelines

- Keep `SKILL.md` focused on essential execution guidance.
- Put detailed frameworks, schemas, and templates under `core/`.
- Keep examples sanitized and runnable without private services.
- Prefer deterministic scripts for outputs that should be reproducible.
- Update `README.md`, `STRUCTURE.md`, and `CHANGELOG.md` when adding visible features.
