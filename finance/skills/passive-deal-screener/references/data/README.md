# `references/data/` — versioned source snapshots

The external-source data that `05-benchmark-returns.md` synthesizes. **Every
number in `05` traces to a dated, source-cited snapshot here**, so a refresh
means re-pulling these files, not rewriting `05`'s prose — and a benchmark can't
be invented, only sourced.

## Files

| File | Source | As of | What it holds |
|---|---|---|---|
| `fred-10yr-snapshot.md` | FRED `DGS10` / `DGS2` / `DGS3MO` (St. Louis Fed), direct CSV pull | 2026-09-24 | Treasury curve — 10yr risk-free anchor + 3mo/2yr short points for duration-matching debt deals |
| `etf-comparators-snapshot.md` | Computed from Yahoo Finance dividend-adjusted daily closes | Q2 2026 quarter-end (2026-06-30) | Trailing 5yr/10yr total returns, vol, worst drop, and expense ratios for the 8 public comparators |
| `ncreif-npi-snapshot.md` | NCREIF, via IREI's report of the quarterly release | Q2 2026 | NPI total / income / appreciation returns — the institutional private-RE baseline |
| `preqin-vintage-note.md` | Preqin, via CAIS's public citation | 2001–2017 study window (latest public; re-confirmed 2026-09-27) | Categorical note on private-fund vintage-year net-IRR dispersion |

## Sources — four, one per kind of data

| Data | Source | How |
|---|---|---|
| Treasury curve | **FRED** | Direct CSV: `https://fred.stlouisfed.org/graph/fredgraph.csv?id=DGS10,DGS2,DGS3MO` |
| ETF returns, vol, worst drop | **Yahoo Finance** | Public chart endpoint, dividend-adjusted daily closes; all figures computed from the one price history |
| NCREIF NPI | **IREI** | Its report of each NCREIF quarterly release |
| Private-fund dispersion | **CAIS** | Public citation of Preqin data (Preqin's own tables are subscription-gated) |

Two figures sit outside the quarterly cycle and are confirmed **once a year**:
ETF expense ratios (on each fund company's page) and the NPI full-year and
property-type returns (from the annual recaps). A documented gap is a correct
output; a fabricated number is a defect.

## Refresh procedure

1. **Treasury curve** — download the FRED CSV above; take the latest daily close
   for each of the three series.
2. **ETF figures** — for each of the eight tickers, pull the full daily history
   from Yahoo and compute, as of the latest quarter-end: trailing 5yr and 10yr
   annualized total return, 10yr annualized vol, and full-history worst drop
   (method in `etf-comparators-snapshot.md` → Provenance).
3. **NCREIF NPI** — take the latest quarter's total / income / appreciation and
   the trailing four-quarter total from IREI's report.
4. **Preqin** — re-confirm the CAIS citation; if a Preqin subscription is
   available, replace the categorical note with current quartile boundaries.
5. Update each file's `As of` / `Captured` stamp, then update `05`'s table and
   its own `LAST_UPDATED`.
6. Update the hardcoded copies in `scripts/benchmark_comparator.py`
   (`COMPARATORS`, `TREASURY`, `LAST_UPDATED`) and its `_self_check` anchors,
   then run `python scripts/benchmark_comparator.py --self-check`. Its drift
   guard fails if any constant disagrees with `05`.

Annual refresh is the minimum cadence; refresh sooner if a rate regime shifts
materially (the 10yr anchor moves the whole illiquidity-premium calculation).
