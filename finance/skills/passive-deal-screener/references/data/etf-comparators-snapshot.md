# Public ETF Comparators Snapshot

Trailing total returns and expense ratios for the eight public-market
comparators `05-benchmark-returns.md` uses to give each private deal type a
liquid, net-of-fee hurdle. Two of the eight (SPY, VTI) are broad-equity
*anchors* — the universal opportunity cost — rather than risk-matched comparators
for a specific private type.

**As of:** trailing returns to the **Q2 2026 quarter-end (2026-06-30)**, one
uniform date for every fund.
**Captured:** 2026-09-27
**Basis:** total return with dividends reinvested, **post-expense-ratio** (net to
a public investor) — apples-to-apples with net-to-LP private returns. Never
compare these to a private deal's *gross* IRR. Computed from market-price closes,
which track NAV total return within a few bps for funds this liquid.

## At-a-glance

| Ticker | Fund | Trailing 5yr | Trailing 10yr | Expense ratio | Best comparator for |
|---|---|---|---|---|---|
| SPY | SPDR S&P 500 | 13.30% | 15.39% | 0.0945% | Universal equity anchor — the opportunity cost every private deal competes with |
| VTI | Vanguard Total Stock Market | 12.24% | 15.04% | 0.03% | Broad-equity anchor — total-market alternative to SPY (incl. mid/small cap), cheaper |
| VNQ | Vanguard Real Estate (REIT) | 2.80% | 4.92% | 0.13% | Equity RE / REIT — multifamily, industrial, retail equity syndications |
| IYR | iShares U.S. Real Estate | 2.65% | 5.21% | 0.39% | Equity RE alternative to VNQ (Dow Jones U.S. Real Estate Capped) |
| LQD | iShares iBoxx $ IG Corp Bond | −0.30% ‡ | 2.36% | 0.14% | Stabilized core / investment-grade-quality debt; senior preferred-equity proxy |
| HYG | iShares iBoxx $ High Yield Corp | 3.66% | 4.83% | 0.49% | High yield / private credit & hard-money fund proxy |
| PFF | iShares Preferred & Income Securities | 0.75% | 3.00% | 0.45% | Preferred equity |
| PRIV | SPDR SSGA IG Public & Private Credit | n/a ※ | n/a ※ | 0.70% | Public + private credit — the most direct private-credit proxy, but too new for trailing returns |

‡ **LQD negative 5yr:** the 2022 IG-bond drawdown still sits inside the
2021–2026 window. Treat it as directional — IG corporates went roughly nowhere,
slightly backwards, over five years.

※ **PRIV too new:** first trade 2025-02-27; no 5yr/10yr trailing return exists.
Since inception to 2026-06-30 it returned **≈4.57% annualized** (≈6.15%
cumulative over ~16 months). PRIV is the *conceptually* closest public proxy for
a public+private IG-credit sleeve, but it carries no seasoned track record yet —
note this explicitly when `05` uses it; lean on HYG/LQD for credit hurdles until
PRIV seasons.

**What changed since the 2026-06 snapshot (Q1 2026 quarter-end):** the 10yr
window rolled forward and rates rose. REIT and credit comparators fell materially
(VNQ 6.47% → 4.92%, HYG 5.0% → 4.83%, PFF 3.72% → 3.00%, LQD ~3.1% → 2.36%);
the equity anchors barely moved (SPY 15.54% → 15.39%). IYR's earlier aggregator
divergence is gone — every figure now comes from one computation on one date.

## Per-comparator notes

- **SPY (0.0945%)** — the universal anchor. A private deal's net-to-LP return
  must clear SPY *plus* an illiquidity premium to justify the lock-up, since SPY
  is daily-liquid and nearly free. Its 10yr (15.39%) reflects an unusually strong
  equity decade; weight that when using it as the hurdle.
- **VTI (0.03%)** — total U.S. market (large + mid + small); the total-market
  alternative anchor to SPY and even cheaper. Returns track SPY closely
  (15.04% 10yr vs 15.39%), as do vol and drawdown. Use whichever anchor the LP
  thinks in; they are near-substitutes, not distinct exposures.
- **VNQ (0.13%)** — broad U.S. REITs; the cleanest liquid proxy for equity real
  estate. Lower-cost and more diversified than IYR. Primary RE comparator.
- **IYR (0.39%)** — narrower, pricier REIT index; useful only as a cross-check on
  VNQ. The higher expense ratio is itself an LP-lens point: same exposure, more
  drag.
- **LQD (0.14%)** — investment-grade corporates; the liquid analog for stabilized
  "core" cash-flow risk and the senior end of preferred equity. Its rate
  sensitivity is the cautionary tale for any private deal selling "bond-like"
  stability.
- **HYG (0.49%)** — high-yield corporates; the closest liquid proxy for
  hard-money / bridge funds and private credit. The 4.83% 10yr is the number a
  private credit fund's net-to-LP yield should be measured against, with a
  premium for illiquidity and single-borrower concentration.
- **PFF (0.45%)** — preferred securities; the direct liquid comparator for
  preferred-equity positions. Its modest trailing returns (0.75% 5yr / 3.00%
  10yr) set a sober bar for preferred-equity deals claiming equity-like returns.
- **PRIV (0.70%)** — public+private IG credit; conceptually the most direct
  private-credit comparator, but unseasoned. Highest expense ratio of the set.

## Volatility and worst drop

Computed from the same daily price history as the returns, so every fund is
measured on one basis. **Vol** = annualized standard deviation of daily log
returns over the 10yr window (2016-06-30 → 2026-06-30), × √252. **Worst drop** =
largest peak-to-trough fall in dividend-adjusted price over the fund's full
trading history, with the date of the trough.

| Ticker | Vol (10yr) | Worst drop | Trough | History from |
|---|---|---|---|---|
| SPY | 18.0% | −55.2% | 2009-03-09 | 1993-01-29 |
| VTI | 18.3% | −55.5% | 2009-03-09 | 2001-06-15 |
| VNQ | 20.9% | −73.1% | 2009-03-06 | 2004-09-29 |
| IYR | 20.5% | −74.1% | 2009-03-06 | 2000-06-19 |
| LQD | 8.7% | −25.0% | 2022-10-20 | 2002-07-30 |
| HYG | 8.2% | −34.2% | 2008-11-20 | 2007-04-11 |
| PFF | 12.9% | −65.5% | 2009-03-06 | 2007-03-30 |
| PRIV | n/a | n/a | — | 2025-02-27 (too short; and smoothed private marks **understate** true vol) |

Two LP reads:
- **REITs (VNQ/IYR) run higher vol than the equity anchor with a far deeper worst
  drop (−73% vs −55%) while delivering lower trailing returns** — less reward for
  more tail risk.
- **"Income" is not "safe."** PFF's day-to-day vol is modest (12.9%), but it fell
  65% in 2008–09, nearly as far as equities. A preferred-equity deal selling
  "bond-like stability" should be read against that.

These replace the June 2026 relative-only read ("≈ SPY", "below SPY"), which was
used because no single public source measured every fund the same way. The
earlier SPY and VNQ figures (−55%, −73%) are confirmed.

## Provenance

One source for every figure except the expense ratios: **Yahoo Finance's
dividend-adjusted daily closes** (total return, dividends reinvested, net of
expense ratio), pulled 2026-09-27 through the public chart endpoint. Returns are
annualized as (end ÷ start)^(1 ÷ years) − 1 between the last close on or before
2026-06-30 and the last close on or before the same date 5 and 10 years earlier.

**Method validated once, 2026-09-27** (not a per-refresh step): each fund's 10yr
was also computed to 2026-09-25 and compared with averageannualreturn.com's
independently published figure for the same end date. All seven agreed within
0.08 points (VNQ 4.35 vs 4.42, SPY 15.37 vs 15.41, VTI 14.85 vs 14.88, IYR 4.66
vs 4.74, LQD 1.82 vs 1.75, HYG 4.31 vs 4.32, PFF 2.79 vs 2.77).

**Expense ratios** change rarely and are carried from the June 2026 snapshot;
confirm them once a year on each fund company's page.
