# Test Coverage Analysis

**Date:** 2026-03-30
**Scope:** Full repository analysis of testing infrastructure, coverage gaps, and improvement recommendations.

---

## Current State

### By the Numbers

| Metric | Value |
|--------|-------|
| Total Python scripts | 301 |
| Scripts with any test coverage | 0 |
| Validation/quality scripts | 35 |
| CI quality gate checks | 5 (YAML lint, JSON schema, Python syntax, safety audit, markdown links) |
| Test framework configuration | None (no pytest.ini, tox.ini, etc.) |
| Test dependencies declared | None |

### What Exists Today

The repository has **no unit tests**. Quality assurance relies on:

1. **CI quality gate** (`ci-quality-gate.yml`) - Runs syntax compilation, YAML linting, JSON schema validation, dependency safety audits, and markdown link checks. Most steps use `|| true`, making them non-blocking.
2. **Playwright hooks** - Anti-pattern detection for Playwright test files (not test execution).
3. **Skill validator** (`engineering/skill-tester/`) - Validates skill directory structure, script syntax, and argparse compliance. Designed for users to run on their own skills.
4. **35 validation scripts** - Checkers and linters distributed across skills (SEO, compliance, security, API design). These are *skill products*, not repo infrastructure tests.

### Key Observation

The CLAUDE.md explicitly states "No build system or test frameworks - intentional design choice for portability." However, the repository has grown to 301 Python scripts, many with pure computational logic that is highly testable and would benefit from regression protection.

---

## Coverage Gaps (Prioritized)

### Priority 1: Core Infrastructure Scripts (High Impact, Easy)

**Scripts:** `scripts/generate-docs.py`, `scripts/sync-codex-skills.py`, `scripts/sync-gemini-skills.py`

**Risk:** These scripts power the documentation site build and multi-platform sync. A regression here breaks the entire docs pipeline or causes silent data loss in skill synchronization.

**What to test:**
- `generate-docs.py`: Skill file discovery logic, domain categorization, YAML frontmatter parsing, MkDocs nav generation
- `sync-*-skills.py`: Symlink creation, directory mapping, validation functions

**Effort:** Low. Functions are mostly pure with filesystem inputs that can be mocked or tested against fixture directories.

---

### Priority 2: Calculator/Scoring Scripts (High Value, Trivial)

**Scripts (examples):**
- `product-team/product-manager-toolkit/scripts/rice_prioritizer.py` - RICE formula
- `product-team/product-manager-toolkit/scripts/okr_tracker.py` - OKR scoring
- `finance/financial-analysis/scripts/dcf_calculator.py` - DCF valuation
- `finance/financial-analysis/scripts/ratio_analyzer.py` - Financial ratios
- `marketing-skill/campaign-analytics/scripts/roi_calculator.py` - ROI calculations
- `engineering/skill-tester/scripts/quality_scorer.py` - Quality scoring

**Risk:** Incorrect calculations silently produce wrong results. Users trust these as authoritative tools.

**What to test:**
- Known-input/known-output parameterized tests for all formulas
- Edge cases: zero values, negative inputs, division by zero, boundary scores
- Categorical-to-numeric mappings (e.g., "high" -> 3)

**Effort:** Trivial. These are pure functions with zero external dependencies.

---

### Priority 3: Parser/Analyzer Scripts (Medium Impact, Moderate Effort)

**Scripts (examples):**
- `marketing-skill/seo-audit/scripts/seo_checker.py` - HTML parsing + scoring
- `marketing-skill/schema-markup/scripts/schema_validator.py` - JSON-LD validation
- `engineering/api-design-reviewer/scripts/api_linter.py` - API spec linting
- `engineering/docker-development/scripts/compose_validator.py` - Docker Compose validation
- `engineering/helm-chart-builder/scripts/values_validator.py` - Helm values checking
- `engineering/changelog-generator/scripts/commit_linter.py` - Conventional commit parsing

**Risk:** Parsers are notoriously fragile against edge-case inputs. Malformed HTML, YAML, or JSON can cause silent failures or crashes.

**What to test:**
- Well-formed input produces correct parsed output
- Malformed input is handled gracefully (no crashes, clear error messages)
- Edge cases: empty files, very large files, unicode content, missing required fields

**Effort:** Moderate. Requires crafting fixture files but the parser classes are self-contained.

---

### Priority 4: Compliance Checker Scripts (High Regulatory Risk)

**Scripts:**
- `ra-qm-team/gdpr-dsgvo-expert/scripts/gdpr_compliance_checker.py`
- `ra-qm-team/fda-consultant-specialist/scripts/qsr_compliance_checker.py`
- `ra-qm-team/information-security-manager-iso27001/scripts/compliance_checker.py`
- `ra-qm-team/quality-documentation-manager/scripts/document_validator.py`

**Risk:** Compliance tools that give false positives or false negatives have real regulatory consequences. Users rely on these for audit preparation.

**What to test:**
- Known-compliant inputs return passing results
- Known-noncompliant inputs flag correct violations
- Completeness: all documented requirements are actually checked
- Output format consistency (JSON/human-readable modes)

**Effort:** Moderate. Requires building compliance fixture data.

---

### Priority 5: CI Quality Gate Hardening

**Current problem:** Most CI steps use `|| true`, meaning failures are swallowed silently. The quality gate currently cannot block a broken PR.

**Recommended improvements:**
- Remove `|| true` from Python syntax check (currently only checks 5 of 9+ skill directories)
- Add `engineering/`, `business-growth/`, `finance/`, `project-management/` to the compileall step
- Add a `--help` smoke test for all argparse-based scripts (the repo already validated 237/237 passing)
- Add SKILL.md structure validation (required sections, YAML frontmatter)
- Make at least syntax and import checks blocking (remove `|| true`)

---

### Priority 6: Integration/Smoke Tests for Skill Packages

**What's missing:** No test verifies that a complete skill directory is internally consistent - that SKILL.md references to scripts and references actually exist, that scripts listed in workflows are present, etc.

**What to test:**
- All file paths referenced in SKILL.md exist
- All scripts in `scripts/` directories pass `python script.py --help`
- All referenced `references/*.md` files exist and are non-empty
- YAML frontmatter in SKILL.md is valid

---

## Recommended Implementation Plan

### Phase 1: Foundation (1-2 days)

1. Add `pytest` to a top-level `requirements-dev.txt`
2. Create a `tests/` directory at the repo root
3. Add pytest configuration in `pyproject.toml` (minimal)
4. Write smoke tests: import + `--help` for all 301 scripts
5. Harden CI: remove `|| true` from syntax checks, expand compileall scope

### Phase 2: Unit Tests for Pure Logic (2-3 days)

1. Test all calculator/scoring scripts (Priority 2) - ~15 scripts, parameterized tests
2. Test core infrastructure scripts (Priority 1) - 3 scripts with mocked filesystem
3. Add to CI pipeline as a blocking step

### Phase 3: Parser and Validator Tests (3-5 days)

1. Create fixture files for each parser type (HTML, YAML, JSON, Dockerfile, etc.)
2. Test parser scripts (Priority 3) - ~10 scripts
3. Test compliance checkers (Priority 4) - ~5 scripts with compliance fixtures
4. Add to CI pipeline

### Phase 4: Integration Tests (2-3 days)

1. Skill package consistency validation (Priority 6)
2. Cross-reference validation (SKILL.md -> scripts, references)
3. Documentation build test (generate-docs.py end-to-end)

---

## Quick Win: Starter Test Examples

### Example 1: RICE Calculator Test

```python
# tests/test_rice_prioritizer.py
import pytest
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'product-team', 'product-manager-toolkit', 'scripts'))
from rice_prioritizer import RICECalculator

@pytest.mark.parametrize("reach,impact,confidence,effort,expected_min", [
    (1000, "massive", "high", "medium", 500),
    (0, "high", "high", "low", 0),
    (100, "low", "low", "massive", 0),
])
def test_rice_calculation(reach, impact, confidence, effort, expected_min):
    calc = RICECalculator()
    result = calc.calculate_rice(reach, impact, confidence, effort)
    assert result["score"] >= expected_min
```

### Example 2: Script Smoke Test

```python
# tests/test_script_smoke.py
import subprocess, glob, pytest

scripts = glob.glob("**/scripts/*.py", recursive=True)

@pytest.mark.parametrize("script", scripts)
def test_script_syntax(script):
    result = subprocess.run(["python", "-m", "py_compile", script], capture_output=True)
    assert result.returncode == 0, f"Syntax error in {script}: {result.stderr.decode()}"
```

---

## Summary

The repository has **0% unit test coverage** across 301 Python scripts. The CI quality gate exists but is non-blocking (`|| true`). The highest-impact improvements are:

1. **Harden CI** - Make syntax checks blocking, expand scope to all directories
2. **Test pure calculations** - Trivial effort, high trust value for calculator scripts
3. **Test infrastructure scripts** - Protect the docs build and sync pipelines
4. **Test parsers with fixtures** - Prevent regressions in fragile parsing logic
5. **Test compliance checkers** - Regulatory correctness matters

The recommended phased approach adds meaningful coverage within 1-2 weeks without violating the repository's "minimal dependencies" philosophy - pytest is the only addition needed.
