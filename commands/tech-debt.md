---
name: tech-debt
description: Score, track, and prioritize technical debt. Usage: /tech-debt <scan|score|report> [options]
---

# /tech-debt

Scan codebases for technical debt, score severity, and generate prioritized remediation plans.

## Usage

```
/tech-debt scan <project-dir>           Scan for debt indicators
/tech-debt score <project-dir>          Calculate debt score (0-100)
/tech-debt report <project-dir>         Full report with remediation plan
```

## Examples

```
/tech-debt scan ./src
/tech-debt score . --format json
/tech-debt report . --output debt-report.md
```

## Scripts
- `engineering/tech-debt-tracker/scripts/debt_scanner.py` — Detect debt patterns
- `engineering/tech-debt-tracker/scripts/debt_scorer.py` — Calculate severity scores
- `engineering/tech-debt-tracker/scripts/remediation_planner.py` — Generate fix plans
- `engineering/tech-debt-tracker/scripts/trend_tracker.py` — Track debt over time
- `engineering/tech-debt-tracker/scripts/cost_estimator.py` — Estimate remediation cost

## Skill Reference
→ `engineering/tech-debt-tracker/SKILL.md`
