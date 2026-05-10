---
title: "SLO Architect — SLOs That Mean Something"
description: "End-to-end SLO/SLI/error-budget discipline for Claude Code per Google SRE Workbook. SLO designer, error-budget calculator with multi-window burn-rate alerts (PromQL-shaped), SLO reviewer that catches the 7 common bugs. Composes with feature-flags-architect, chaos-engineering, kubernetes-operator."
---

# SLO Architect

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `slo-architect`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/slo-architect">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install slo-architect</code>
</div>

Define SLOs that mean something. Most "SLOs" in the wild are arbitrary numbers nobody believes — 99.9% on every endpoint, no SLI definition, no error budget policy. This skill enforces the Google SRE Workbook discipline: pick the right SLI, set a target users actually care about, calculate the error budget, wire multi-window burn-rate alerts, and have a written policy for when budget runs out.

## When to use

- Defining a new SLO for a service or feature
- Reviewing existing SLOs for common bugs
- Picking the right SLI (event-based vs time-window vs request-based)
- Computing error budgets and burn-rate alert thresholds
- Tying SLOs to existing controls — feature flags abort, chaos blast radius, operator capability levels

## When NOT to use

- General observability strategy → use `observability-designer`
- Customer-facing SLAs with legal teeth → contract drafting, not engineering
- Performance load testing → use `performance-profiler`
- Active incident response → use `incident-response`

## The 3 Python tools

All stdlib-only. Karpathy complexity 95/100.

### `slo_designer.py`

Generates structured SLO definitions and refuses to render if required fields (owner, error-budget policy, SLI numerator/denominator) are missing.

```bash
python scripts/slo_designer.py \
  --service checkout-svc --sli-type request-success-rate \
  --target 99.9 --window-days 28 \
  --owner team-checkout --policy-doc docs/eb-policy.md
```

Supports 5 SLI types: `request-success-rate`, `request-latency`, `availability-time`, `data-freshness`, `correctness`.

### `error_budget_calculator.py`

Computes error budget + canonical multi-window burn-rate alert thresholds (Google SRE Workbook Chapter 5):

| Alert | Long window | Short window | Burn rate | Severity |
|---|---|---|---|---|
| Fast burn | 1h | 5m | 14.4 | page |
| Slow burn | 6h | 30m | 6.0 | page |
| Ticket | 3d | 6h | 1.0 | ticket |

Output is PromQL-shaped, ready to paste into Prometheus rules.

```bash
python scripts/error_budget_calculator.py --target 99.9 --window-days 28
```

### `slo_review.py`

Audits SLO definitions for the 7 common bugs:

- `target_too_high` (≥99.99%)
- `target_too_low` (≤99%)
- `window_too_short` (<7 days)
- `window_too_long` (>90 days)
- `no_sli_definition`
- `no_error_budget_policy`
- `cpu_as_sli` (CPU/memory used as user-experience proxy)

Use as a pre-merge gate before SLOs go live.

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

## Reference docs

- `references/slo_principles.md` — SLI vs SLO vs SLA, Google SRE Workbook canon
- `references/sli_design.md` — picking the right SLI; 5 types with examples
- `references/error_budget.md` — error budget math, burn-rate alerts, budget policy
- `references/composition.md` — how SLOs feed feature flags, chaos, operators

## Asset templates

- `assets/slo_template.yaml` — fillable SLO YAML
- `assets/error_budget_policy.md` — fillable policy template

## Slash command

`/slo-design` — interactive SLO design wizard.

## Verifiable success

- 100% of SLOs pass `slo_review.py` with 0 FAIL findings
- Every SLO has documented owner, error budget, burn-rate alerts, policy
- Burn-rate alerts fire ≤2 times/month per SLO (signal not noise)
- Mean time to detect SLO violation: <30 min
- Quarterly SLO review actually happens
