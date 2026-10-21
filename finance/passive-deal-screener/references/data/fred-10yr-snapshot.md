# FRED 10-Year Treasury Snapshot

**Series:** `DGS10` (10yr, the headline anchor), plus short points `DGS2` (2yr)
and `DGS3MO` (3-month) for duration-matching debt comparators — all Market Yield
on U.S. Treasury Securities at constant maturity, investment basis (daily).
**Source:** FRED, Federal Reserve Bank of St. Louis —
<https://fred.stlouisfed.org/series/DGS10>, pulled directly from the
`fredgraph.csv` endpoint
**As of:** 2026-09-24 (latest daily close available at capture)
**Captured:** 2026-09-27

## Value — Treasury curve

| Point | Value | As of | Duration-matches | Source |
|---|---|---|---|---|
| 3-month T-bill (DGS3MO) | **4.24%** | 2026-09-24 | very-short hard money (6–18mo loans) | FRED `DGS3MO` |
| 2-year (DGS2) | **4.87%** | 2026-09-24 | short/mid private debt | FRED `DGS2` |
| 10-year (DGS10) | **5.18%** | 2026-09-24 | equity-RE hold (~7yr); general anchor | FRED `DGS10` |

The curve is upward-sloping (4.24% → 4.87% → 5.18%). Rates moved sharply up
through September: the 10yr closed at 4.94% on 2026-09-17 and 5.18% one week
later. Against the prior snapshot (June 2026: 3.71% / 4.15% / ≈4.5%), every point
is roughly 50–70bps higher — a material regime shift, which is the refresh
trigger `README.md` names.

**Read against the comparators:** the 10yr (5.18%) now *exceeds* the trailing
10yr return of VNQ (4.92%) and HYG (4.83%). A risk-free Treasury out-yields what
the REIT and high-yield indices actually delivered over the last decade, so at
this snapshot the duration-matched Treasury, not the trailing comparator, is the
tighter floor.

## Why this file exists

The 10yr Treasury is the **risk-free anchor** for the illiquidity-premium
framework in `05-benchmark-returns.md`. The rule of thumb there — an LP should
demand ≥200bps over the closest *public* comparator, scaled by lock-up — sits on
top of the risk-free rate. When the 10yr moves materially, the entire premium
calculation shifts, which is why this is the file most sensitive to staleness.

The **short points** exist so debt deals get a *duration-matched* floor: a 6–18mo
hard-money fund's honest risk-free comparison is the 3mo/2yr bill, not the 10yr.
`05` reads a debt deal's net yield over the duration-matched Treasury as the
**credit + illiquidity spread** the LP is paid for taking the risk.

## Provenance / refresh note

Pulled directly from FRED's `fredgraph.csv` endpoint
(`?id=DGS10,DGS2,DGS3MO`), which was fetchable on 2026-09-27 (it had returned
HTTP 403 on 2026-06-06). These are daily-volatile market rates: re-pull, don't
assume. `GS10` is the monthly-average sibling of `DGS10` if a smoothed figure is
preferred.
