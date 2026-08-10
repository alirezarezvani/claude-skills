---
description: Interactive wizard to design and validate a chaos engineering experiment
---

# /chaos-experiment

Step through the design of a chaos engineering experiment using the `chaos-engineering` skill. Produces a plan, calculates blast radius, validates abort criteria, and outputs a markdown plan ready for peer review.

## Usage

```
/chaos-experiment
/chaos-experiment --target checkout-svc --attack latency
```

## Implementation

```bash
SKILL=engineering/chaos-engineering/skills/chaos-engineering

# Step 1: gather inputs interactively (target, hypothesis, attack, magnitude, ...)
# Step 2: run experiment_designer.py to produce the plan
python "$SKILL/scripts/experiment_designer.py" \
  --target "$TARGET" --hypothesis "$HYPOTHESIS" \
  --attack "$ATTACK" --magnitude "$MAGNITUDE" \
  --duration-min "$DURATION" \
  --abort-if "$ABORT" --owner "$OWNER" \
  --format json > .chaos-plan.json

# Step 3: calculate blast radius against the team's error budget
python "$SKILL/scripts/blast_radius_calculator.py" \
  --traffic-share "$TRAFFIC_SHARE" \
  --user-pop "$USER_POP" \
  --duration-min "$DURATION" \
  --baseline-availability "$BASELINE_AVAIL" \
  --expected-impact-availability "$IMPACT_AVAIL"

# Step 4: render the markdown plan for peer review
python "$SKILL/scripts/experiment_designer.py" \
  --target "$TARGET" --hypothesis "$HYPOTHESIS" \
  --attack "$ATTACK" --abort-if "$ABORT" --owner "$OWNER"
```

## Output

A markdown plan with:

- Hypothesis, steady-state metric, attack, magnitude, duration
- Blast radius (calculated) with risk score (GREEN/YELLOW/RED)
- Abort criteria parsed from `--abort-if`
- Rollback procedure
- Monitoring dashboard link
- Learning question

## Pre-conditions

- `chaos-engineering` skill installed
- Target identified
- Steady-state metric and dashboard available
- On-call team available
- Error budget known (or use defaults)

## Post-conditions

- `.chaos-plan.json` written for use with `experiment_postmortem.py` later
- Markdown plan streamed for review
- Recommendation printed: PROCEED / REDUCE / ABORT
