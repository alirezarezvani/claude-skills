# Security Roadmap Planner — Workflow Reference

## Roadmap Construction Methodology

A security program roadmap is a structured commitment to close specific gaps within a defined time horizon. The `security-roadmap-planner` skill operationalizes this definition: every initiative must map to a measured gap or quantified risk, and investment priorities must be ranked by risk-reduction-per-dollar rather than by severity perception alone.

---

## Priority Scoring Model

### Formula

```
priority_score = risk_reduction_score / investment_weight
```

**risk_reduction_score (0–100):** Estimated reduction in overall risk exposure if this initiative succeeds. Derived from:
- For posture gaps: proportional to gap size below threshold (gap × 1.5, capped at 100)
- For risk findings: proportional to ALE excess above risk appetite
- For compliance gaps: fixed estimate of 55 (regulatory exposure reduction)

**investment_weight:** Relative cost multiplier to normalize across initiative sizes:
- S (Small): weight = 1 (< 0.5 FTE or < $50K)
- M (Medium): weight = 2 (0.5–2 FTE or $50K–$250K)
- L (Large): weight = 4 (> 2 FTE or > $250K)

A high `priority_score` indicates the initiative delivers significant risk reduction at low relative cost. This is the primary sort key.

### Why Risk-Reduction-Per-Dollar

Ranking by severity alone produces roadmaps that front-load large, expensive programs while neglecting high-impact quick wins. Ranking by risk-reduction-per-dollar ensures that small initiatives with outsized impact (e.g., patching one critical system) are not displaced by large initiatives with modest per-dollar impact (e.g., rebuilding a security operations center).

---

## Quarterly Bucketing

### Capacity Rules

| Quarter | Capacity | Profile |
|---|---|---|
| Q1 | 3 initiatives | Quick wins (priority_score >= 40, S/M band) and critical gap closures |
| Q2 | 4 initiatives | Medium-effort risk reduction programs; begins strategic programs |
| Q3 | 4 initiatives | Strategic capability building; vendor selection and procurement |
| Q4 | 3 initiatives | Long-lead investments; architecture changes; budget cycle alignment |
| Backlog | Unlimited | Overflow — re-evaluate at next planning cycle |

### Bucketing Algorithm

1. Sort all initiatives by `priority_score` descending
2. Iterate through sorted list; assign to earliest quarter with remaining capacity
3. Initiatives that do not fit into Q1–Q4 are assigned to `backlog` with a re-evaluation note

### Overflow Handling

Backlog items should not be abandoned. Each planning cycle, the top backlog items (highest `priority_score`) are candidates to move into Q1 of the next 12-month roadmap. Backlog growth beyond 5 items indicates capacity constraints that require program-level attention.

---

## Traceability Requirement

Every roadmap initiative must satisfy the traceability constraint:

```
initiative.addresses_gap → must reference a specific finding from:
  - posture_score.domain_scores (domain name + score)
  - enterprise_risk.top_risks (risk ID or name + ALE)
  - compliance_mapping.gaps (framework + control ID)
```

Initiatives that cannot be traced to a specific gap or finding are removed before output. This is enforced programmatically by the tool and is a hard quality gate.

Rationale: Untraced initiatives are decoration. They consume budget and attention without closing measured gaps, and they cannot be tracked to program success metrics.

---

## Success Metric Standards

Each initiative must include a measurable success metric. Acceptable forms:

| Form | Example |
|---|---|
| Score target | "Detection domain score >= 75 by end of Q3" |
| Rate target | "SLA breach rate < 5% by end of Q2" |
| Coverage target | "100% of critical assets covered by EDR by end of Q1" |
| Compliance target | "SOC 2 Type II gap: MFA control implemented by regulatory deadline [date]" |

Unacceptable forms:
- "Improve security posture" (not measurable)
- "Review vulnerability management process" (activity, not outcome)
- "Increase awareness" (no measurement defined)

---

## Investment Band Reference

| Band | FTE Equivalent | Budget Equivalent | Typical Initiative Type |
|---|---|---|---|
| S | < 0.5 FTE | < $50K | Quick wins, policy updates, configuration changes, tooling adjustments |
| M | 0.5–2 FTE | $50K–$250K | Program buildouts, new tooling, training programs, process redesigns |
| L | > 2 FTE | > $250K | Platform replacements, major capability builds, architecture overhauls |

Investment bands are proxies for relative cost. Actual budget figures are provided during the business case stage, not at roadmap construction.

---

## Data Availability and Confidence

| Inputs Available | Output Confidence | Notes |
|---|---|---|
| Posture + Risk + Compliance | 0.90 | Full data — high confidence roadmap |
| Posture + Risk only | 0.80 | No regulatory deadlines; compliance exposure unquantified |
| Posture only | 0.60 | Risk appetite unknown; ALE calculations unavailable |
| No inputs | 0.40 | Minimal output; recommend posture assessment as first initiative |

When confidence is below 0.70, the roadmap output must include explicit data gap notes and a recommendation to re-run with complete inputs before committing investment decisions.

---

## Integration with Program Planning Workflow

The security-roadmap-planner is Step 4 in the Security Program Planning (PL) workflow run by `cs-security-program-manager`. Input data flows:

```
[cs-security-program-manager: PL workflow]
  Step 1: security-posture-score   → posture_data
  Step 2: enterprise-risk-assessment → risk_data
  Step 3: compliance-mapping       → compliance_data
  Step 4: security-roadmap-planner (posture + risk + compliance) → roadmap_items
  Step 5: ciso-brief-generator     → board-ready program plan
```

---

## References

- NIST Cybersecurity Framework (CSF) 2.0 — Program maturity tiers and roadmap guidance
- CIS Controls v8 — Implementation group sequencing as capacity model
- FAIR (Factor Analysis of Information Risk) — ALE and risk appetite concepts
- `governance/security-posture-score/SKILL.md` — posture scoring methodology
- `risk-compliance/enterprise-risk-assessment/SKILL.md` — risk quantification model
- `risk-compliance/compliance-mapping/SKILL.md` — regulatory gap identification
