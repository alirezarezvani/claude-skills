# SLO Architect

Define SLOs that mean something. Most "SLOs" in the wild are arbitrary numbers nobody believes — 99.9% on every endpoint, no SLI definition, no error budget policy. This skill enforces the Google SRE Workbook discipline.

## What's inside

- **3 stdlib Python tools** — SLO designer, error-budget calculator with multi-window burn-rate alerts, SLO reviewer
- **4 reference docs** — principles, SLI design, error budget, composition
- **2 asset templates** — SLO YAML, error budget policy
- **`/slo-design` slash command**

## Install

```bash
# Via Claude Code marketplace
/plugin install slo-architect

# Or clone the repo
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills/engineering/slo-architect
```

## Quick start

```bash
SKILL=engineering/slo-architect/skills/slo-architect

# 1. Design an SLO
python "$SKILL/scripts/slo_designer.py" \
  --service checkout-svc --sli-type request-success-rate \
  --target 99.9 --window-days 28

# 2. Compute error budget + multi-window burn-rate alerts
python "$SKILL/scripts/error_budget_calculator.py" --target 99.9 --window-days 28

# 3. Review existing SLOs for common bugs
python "$SKILL/scripts/slo_review.py" --slo-doc docs/slos/
```

## Key principles

1. **An SLO is a promise about user experience** — not a CPU graph
2. **Pick the SLI from the user's perspective** — request-success / latency / availability / freshness / correctness
3. **Pick the target from data** — measure 30 days, then floor it
4. **Multi-window burn-rate alerts** — single-window is either too noisy or too slow
5. **Error budget without a policy is theater** — every SLO ships with a policy

## The 5 SLI types

| User experience | SLI type |
|---|---|
| "Did the request succeed?" | request-success-rate |
| "Was the response fast?" | request-latency |
| "Was the service up?" | availability-time |
| "Is the data current?" | data-freshness |
| "Was the answer correct?" | correctness |

## Composition with the rest of the portfolio

| Skill | Composition |
|---|---|
| `feature-flags-architect` | Rollout abort criteria reference SLO burn-rate thresholds |
| `chaos-engineering` | Blast-radius calculator takes monthly error budget as input |
| `kubernetes-operator` | Operator capability L4 requires SLOs + Prometheus rules |

## Skill structure

```
slo-architect/
├── README.md
├── .claude-plugin/plugin.json
└── skills/slo-architect/
    ├── SKILL.md
    ├── scripts/
    │   ├── slo_designer.py
    │   ├── error_budget_calculator.py
    │   └── slo_review.py
    ├── references/
    │   ├── slo_principles.md
    │   ├── sli_design.md
    │   ├── error_budget.md
    │   └── composition.md
    └── assets/
        ├── slo_template.yaml
        └── error_budget_policy.md
```

## Verifiable success

A team using this skill should achieve:

- 100% of SLOs pass `slo_review.py` with 0 FAIL findings
- Every SLO has a documented owner, error budget, burn-rate alerts, and policy
- Burn-rate alerts fire ≤2 times/month per SLO that's hit
- Mean time to detect SLO violation: <30 min
- Quarterly SLO review actually happens

## License

MIT — see repo root LICENSE.
