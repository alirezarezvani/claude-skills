# security-roadmap-planner

**Domain:** Governance | **Level:** L2 (CISO/Mgmt) | **Intent:** advise

Builds an investment-prioritized 12-month security program roadmap from posture, risk, and compliance data. Every roadmap initiative is traceable to a specific posture gap or quantified risk finding. Initiatives are ranked by risk-reduction-per-dollar and bucketed into quarterly milestones.

## Quick Start

```bash
# Run with no input (generates baseline recommendation)
python scripts/security-roadmap-planner_tool.py --output json

# Run with posture score input
python scripts/security-roadmap-planner_tool.py --input posture.json --output json

# Run with full inputs (posture + risk + compliance)
python scripts/security-roadmap-planner_tool.py \
  --input posture.json \
  --risk-input risk.json \
  --compliance-input compliance.json \
  --output json

# Validate with sample output
python scripts/security-roadmap-planner_tool.py \
  --input expected_outputs/sample_output.json --output json
```

## Priority Scoring

```
priority_score = risk_reduction_score / investment_weight
```

Where `investment_weight`: S=1, M=2, L=4. Higher score = more risk reduction per dollar.

## Quarterly Capacity

| Quarter | Max Initiatives | Profile |
|---|---|---|
| Q1 | 3 | Quick wins and critical gap closures (score >= 40) |
| Q2 | 4 | Medium-effort risk reduction programs |
| Q3 | 4 | Strategic capability building |
| Q4 | 3 | Long-lead investments and architecture changes |

## Confidence Levels

| Input Available | Confidence |
|---|---|
| Posture + Risk + Compliance | 0.90 |
| Posture + Risk only | 0.80 |
| Posture only | 0.60 |
| No inputs | 0.40 |

## Routing

- Always routes to `ciso-brief-generator` for board formatting
- Always routes to `metrics-reporting` to track execution
- L-band initiatives → `cs-ciso-advisor` for budget approval framing

## Files

| File | Purpose |
|---|---|
| `SKILL.md` | Full LLM system prompt and roadmap construction methodology |
| `scripts/security-roadmap-planner_tool.py` | Roadmap builder CLI tool |
| `references/workflow.md` | Prioritization methodology and quarterly bucketing logic |
| `assets/templates/output-template.json` | Output schema template |
| `expected_outputs/sample_output.json` | Representative tool output |

## Related Skills

- `governance/security-posture-score` — primary posture input
- `risk-compliance/enterprise-risk-assessment` — risk quantification input
- `risk-compliance/compliance-mapping` — regulatory gap input
- `governance/ciso-brief-generator` — downstream board formatting
- `governance/metrics-reporting` — downstream execution tracking
