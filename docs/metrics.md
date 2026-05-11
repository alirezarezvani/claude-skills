# Metrics Dictionary

Generated: 2026-05-11T14:29:09Z

## North-star KPIs

### Top200_QualityPassRate
- Formula: `passing_skills / 200`
- Current baseline: `194/200 = 97.0%`
- Day-90 target: `>=95%`
- Passing definition: metadata valid, structure valid, references intact, script-help/security checks passing or explicitly not applicable, and quality score >=75.
- Source files: `ops/top200.csv`, `ops/quality_baseline.json`

### ClaimConsistencyScore
- Formula: `consistent_claims / total_checked_claims`
- Target: `100%`
- Claims to check: skill counts, script counts, supported platforms, star/social-proof claims, marketplace/plugin names.
- Source files: README, docs pages, plugin manifests, generated indexes.

### Monthly_New_External_PR_Authors
- Formula: unique non-owner PR authors in the trailing 30 days minus baseline.
- Day-90 target: `+25% vs baseline`
- Guardrail: merged external PR rate `>=40%`.

### StarGrowth_vs_BaselineTrend
- Formula: `net_new_stars_90d / expected_stars_from_trailing_30d_velocity`
- Day-90 target: `>=2x baseline pace`
- Guardrail: star growth cannot override quality gates.

### MedianFirstMaintainerResponse
- Formula: median time from issue/PR open to first maintainer comment, review, label, or close action.
- Target: `<24h`

### InstallMatrixSuccessRate
- Formula: `successful_install_tests / total_install_tests` across supported tools.
- Day-90 target: `>=98%`

## Operating cadence
- Monday: refresh KPIs and top blockers.
- Tuesday/Wednesday: quality and docs fixes.
- Thursday: contributor/bounty review.
- Friday: public quality report and content distribution.
