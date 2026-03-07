---
name: tdd
description: Generate tests, analyze coverage, and run TDD workflows. Usage: /tdd <generate|coverage|validate> [options]
---

# /tdd

Generate tests, analyze coverage, and validate test quality using the TDD Guide skill.

## Usage

```
/tdd generate <file-or-dir>     Generate tests for source files
/tdd coverage <test-dir>        Analyze test coverage and gaps
/tdd validate <test-file>       Validate test quality (assertions, edge cases)
```

## Examples

```
/tdd generate src/auth/login.ts
/tdd coverage tests/ --threshold 80
/tdd validate tests/auth.test.ts
```

## Scripts
- `engineering-team/tdd-guide/scripts/test_generator.py` — Generate test cases
- `engineering-team/tdd-guide/scripts/coverage_analyzer.py` — Coverage analysis
- `engineering-team/tdd-guide/scripts/test_quality_checker.py` — Quality validation

## Skill Reference
→ `engineering-team/tdd-guide/SKILL.md`
