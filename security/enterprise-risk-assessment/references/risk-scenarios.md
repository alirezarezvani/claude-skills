# Risk Scenario Library and Board Reporting Format

## Risk Scenario Library

### Scenario 1: Ransomware Attack on Core Systems
- **Threat actor**: Organized cybercriminal
- **Attack vector**: Phishing → credential theft → domain compromise
- **Impact components**:
  - Business interruption: $X/day × estimated downtime
  - Ransom payment: $X (if paid)
  - IR/forensics costs: $X
  - Regulatory fines: $X (if PII/PCI breach)
  - Reputational: Customer churn × LTV
- **ARO estimate**: 15-25% annually for mid-market companies

### Scenario 2: Data Breach (PII Exfiltration)
- **Threat actor**: Nation-state or financially motivated
- **Impact components**:
  - Regulatory fines: GDPR €20M or 4% revenue (max)
  - Breach notification costs: $X per record
  - Legal defense: $X
  - Credit monitoring: $X per affected customer
  - Brand damage: Stock price impact for public companies
- **Industry benchmark**: IBM Cost of Data Breach Report 2024 — $4.88M average

### Scenario 3: Supply Chain Compromise
- **Threat actor**: Nation-state APT targeting software supply chain
- **Impact**: Code signing key compromise → all customers affected
- **Amplification factor**: 10-1000x customer multiplier

---

## Board Reporting Format (Quarterly Risk Dashboard)

```
CYBER RISK POSTURE — Q[N] [YEAR]
================================
Top 3 Risks:
1. [Risk] — ALE: $X-$Y (90% CI) — Trend: ↑/↓/→
2. [Risk] — ALE: $X-$Y — Trend: ↑/↓/→
3. [Risk] — ALE: $X-$Y — Trend: ↑/↓/→

Total Cyber Risk Exposure: $X-$Y (90% CI)
Cyber Insurance Coverage: $X (gap: $Y)
Security Investment: $X (ROI: X% risk reduction)

Key Metrics vs. Last Quarter:
- Critical findings: N (was N)
- Mean Time to Patch (Critical): N days
- Security incidents: N (was N)
```

---

## Output Artifacts

| When operator asks for... | You produce... |
|---|---|
| FAIR risk quantification | Per-scenario JSON: `scenario`, `ale_min`, `ale_likely`, `ale_max`, `aro`, `inherent_risk_tier`, `residual_risk_tier`, `key_controls`, `control_gaps` |
| Board-ready risk summary | Plain-English risk dashboard using the Board Reporting Format — top 3 risks by ALE, total exposure range, insurance gap, investment ROI |
| Risk register extract | Markdown table: Scenario → ALE Range → Risk Tier → Risk Owner → Last Assessed → Trend |
| Risk trend delta | Comparison of current vs. prior assessment: scenarios that moved tiers, new scenarios added, scenarios closed, aggregate ALE change |

---

## Related Skills

- `risk-threat-modeling` — Use before this skill to generate threat scenario inputs from system DFDs. NOT for board-level ALE quantification (that is this skill's function).
- `compliance-mapping` — Use after this skill to map high-ALE scenarios to specific regulatory control gaps. NOT for financial risk quantification.
- `cyber-insurance` — Use in parallel to validate insurance coverage adequacy against the ALEs this skill produces. NOT a substitute for quantified risk assessment.
- `security-posture-score` — Use after this skill to translate risk findings into a cross-domain posture scorecard. NOT for FAIR methodology calculations.
- `cs-ciso-advisor` — The orchestrator agent that includes this skill's output in board-ready briefs. NOT a direct substitute for this skill's quantification analysis.
