---
name: tdd
description: "Run a red-green-refactor TDD workflow — generate failing tests first, implement to green, then check coverage gaps. Usage: /tdd <generate|coverage|validate> [target]"
argument-hint: <generate|coverage|validate> [file-or-dir]
---

# /tdd

Drive a test-first workflow for `$ARGUMENTS` using the TDD Guide skill. The first word of `$ARGUMENTS` selects the mode (`generate`, `coverage`, or `validate`); the rest is the target file or directory. If `$ARGUMENTS` is empty, ask which mode and target.

> **Note on tooling:** the tdd-guide scripts are **Python library modules, not CLI tools** — import them; do not invoke them as commands. Runnable patterns below.

## Modes

### `/tdd generate <file-or-dir>` — write failing tests FIRST

1. Read `engineering-team/skills/tdd-guide/SKILL.md` and `engineering-team/skills/tdd-guide/references/tdd-best-practices.md` for the red-green-refactor discipline and test-case taxonomy (happy path, edge cases, error cases)
2. Detect the project's test framework — use `engineering-team/skills/tdd-guide/references/framework-guide.md` for Jest/Vitest/pytest/JUnit conventions
3. Write the tests **before** any implementation; run them and confirm they FAIL (red)
4. Implement the minimum code to pass (green), then refactor with tests staying green
5. Optionally use the library for stub scaffolding:

```bash
cd engineering-team/skills/tdd-guide/scripts && python3 -c "
from test_generator import TestGenerator, TestFramework
g = TestGenerator(framework=TestFramework.PYTEST, language='python')
cases = g.generate_from_requirements({'acceptance_criteria': [
    {'id': 'AC1', 'description': 'validates email format'},
    {'id': 'AC2', 'description': 'rejects duplicate emails'}]})
print(g.generate_test_file('registration', cases))
"
```

### `/tdd coverage <coverage-report>` — analyze gaps against a threshold

1. Generate a real coverage report with the project's native runner first (`pytest --cov --cov-report=lcov`, `vitest run --coverage`, `jest --coverage`)
2. Parse it and list prioritized gaps:

```bash
cd engineering-team/skills/tdd-guide/scripts && python3 -c "
from coverage_analyzer import CoverageAnalyzer
a = CoverageAnalyzer()
a.parse_coverage_report(open('<path-to-lcov-or-json>').read(), 'lcov')  # or 'json' / 'xml'
print(a.calculate_summary())
for gap in a.identify_gaps(threshold=80.0): print(gap)
"
```

(Smoke-test input available at `engineering-team/skills/tdd-guide/assets/sample_coverage_report.lcov`.)

3. For each gap, return to `/tdd generate` — coverage gaps are filled with tests, not excuses

### `/tdd validate <test-file>` — review test quality

Read the test file and check it against `engineering-team/skills/tdd-guide/references/tdd-best-practices.md`:

- [ ] Every test has at least one meaningful assertion (no assertion-free tests)
- [ ] Edge cases and error paths covered, not just happy path
- [ ] Tests are independent (no order coupling, no shared mutable state)
- [ ] Test names describe behavior, not implementation
- [ ] No testing of private internals — behavior only

Report failures with concrete rewrite suggestions.

## CI Integration

For wiring coverage thresholds into CI, follow `engineering-team/skills/tdd-guide/references/ci-integration.md`.

## Repo Assets (verified paths)

- Skill: `engineering-team/skills/tdd-guide/SKILL.md` (+ `HOW_TO_USE.md`)
- Best practices: `engineering-team/skills/tdd-guide/references/tdd-best-practices.md`
- Framework conventions: `engineering-team/skills/tdd-guide/references/framework-guide.md`
- CI integration: `engineering-team/skills/tdd-guide/references/ci-integration.md`
- Library modules: `engineering-team/skills/tdd-guide/scripts/` (test_generator, coverage_analyzer, tdd_workflow, fixture_generator, metrics_calculator — import-only)
- Sample inputs: `engineering-team/skills/tdd-guide/assets/`
