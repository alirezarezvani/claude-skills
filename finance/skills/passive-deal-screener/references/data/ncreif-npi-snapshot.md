# NCREIF NPI Snapshot

The **NCREIF Property Index (NPI)** — the institutional private commercial
real-estate benchmark — measures unlevered total return on a large pool of
institutional-quality properties held by NCREIF members. It is the closest thing
to an "unlevered, in-place" baseline for private equity real estate, which makes
it the grounding figure for the financing-story flag (`03` → `GEN-07`): a deal
whose levered IRR towers over the NPI is earning its excess from leverage and
cap-rate movement, not operations.

**As of:** Q2 2026 (most recent reported; released late July 2026)
**Captured:** 2026-09-27
**Source:** IREI's report of NCREIF's quarterly release (2026-07-27). NPI detail
beyond the headline is membership-gated.

## Values

| Metric | Value | Period |
|---|---|---|
| NPI total return (quarterly) | 1.29% | Q2 2026 |
| — income return | 1.17% | Q2 2026 |
| — appreciation return | 0.12% | Q2 2026 |
| NPI total return (prior quarter) | 1.24% | Q1 2026 |
| NPI total return (trailing 4-quarter) | 5.00% | Q3 2025 – Q2 2026 |
| NPI total return (full year) | 4.9% (≈ 4.8% income, ≈ 0.2% appreciation) | 2025 † |

The trailing four-quarter income/appreciation split was not publicly reported
for Q2 2026. Read together, the index's ~5% return is still **almost entirely
income**: Q2 2026 appreciation was 0.12% against 1.17% income, the same shape as
2025's ≈0.2% appreciation against ≈4.8% income. Returns rose for four consecutive
quarters (the highest trailing four-quarter figure since Q4 2022), but there is
still no meaningful appreciation at the institutional index level. That is the
empirical anchor for LP skepticism of deals underwriting large appreciation.

Index scope at Q2 2026: 13,160 properties, $943B market value.

## By property type (2025 full year) †

| Property type | 2025 total return |
|---|---|
| Retail | 6.8% |
| Residential | 5.3% |
| Industrial | 4.5% |
| Office | 3.4% |

These pair with `01-asset-class-norms.md`: office lagging is consistent with the
post-2020 *variable* office baseline.

† Full-year figures, carried from the June 2026 snapshot (RCLCO / Capital
Economics annual recaps). Refreshed once a year, when the next full-year results
are published, not every quarter.

## How `05` uses this

NPI is the **unlevered private-RE baseline**. The design-review DoD for `05`
(2026-06-01) requires an unlevered comparator alongside each headline ETF return
so the skill can separate "clears the illiquidity hurdle" from "IRR is driven by
leverage, not alpha." If a syndication's *unlevered* projected return doesn't
beat the NPI for its property type, the LP is being paid for leverage risk, not
operating skill.

## Provenance / gated-source note

Quarterly headline figures come from one outlet, **IREI**, which reports each
NCREIF quarterly release (total, income, appreciation, trailing four quarters,
index size). **Property-level detail, ODCE fund-level returns, and the full
sub-type/region matrices are membership-gated** behind NCREIF and are not
captured. On refresh, pull the next quarter's headline from IREI; if NCREIF
membership becomes available, replace with the primary release.
