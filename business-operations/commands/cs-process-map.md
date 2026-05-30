---
description: Map an internal business process (BPMN-style swim lanes), measure cycle time, and detect bottlenecks where work spends most of its time waiting. Direct invocation of the process-mapper skill.
argument-hint: "<process description or path to process JSON>"
---

# /cs:process-map — BPMN-style process mapping + bottleneck detection

Run the `process-mapper` skill on this input:

**$ARGUMENTS**

## Three-tool workflow

1. **`process_documenter.py`** — Document the process as a BPMN-ish ASCII swim lane diagram. Input: stage list (name, owner, type{value-add/wait/rework}, P50 + P90 duration). Output: markdown diagram + normalized JSON.

2. **`bottleneck_detector.py`** — Identify bottlenecks. Triggers: stage P50 > 2× mean of value-add stages, OR wait-state % > 40% of total, OR rework % > 15%. Tunable via `--profile {saas,services,manufacturing,healthcare}`.

3. **`cycle_time_analyzer.py`** — Compute total cycle time (P50, P90), value-add ratio (VA%), Little's Law throughput. Verdict: VA% > 25% HEALTHY / 10-25% TYPICAL / <10% WASTE-HEAVY.

## Output

- Process diagram (markdown)
- Bottleneck list with severity + recommended action
- Cycle-time scorecard with VA% verdict
- Top 3 next actions

## Distinct from

- `engineering/slo-architect` — that's system reliability with SLO/SLI. This is **business process** reliability.
- `engineering/llm-wiki` — that's personal PKM. This is **company process documentation**.
- `c-level-advisor/coo-advisor` — that's strategic COO judgment. This is **tactical process mapping**.
