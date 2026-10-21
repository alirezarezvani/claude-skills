# Deal Analysis — Diversified BDC-style private credit fund
*Produced by the passive-deal-screener skill from the deal in `input.md`. Illustrative example; figures route to the `references/` files, not memory.*

**Verdict: Pursue with conditions.** This is a well-built fund. Leverage is disclosed and moderate, the loan book is broad, loss history is disclosed through the cycle, and the IRR is shown both levered and unlevered. No RED flag fires. The biggest swing factor is the fee base. A 1.5% fee on *gross assets* at ~1.1x leverage works out to roughly **310 bps per year on your equity**, not 150. Add the incentive fee, whose rate and hurdle aren't given, and the unlevered net IRR is the number that has to clear HYG plus the illiquidity hurdle. The conditions are confirmations, not fixes.

*Screening output only, not investment advice.*

---

## 1. Deal Snapshot

| Field | Value |
|---|---|
| Asset class | Private Credit (fund) 🟢 |
| Deal type | Private credit fund, BDC-style (fund-level leverage) 🟢 |
| Sponsor | Not stated |
| Geography | Not stated |
| Minimum investment | Not stated |
| Hold / lock-up | Not stated. `01` baseline is 3–7 yrs; perpetual vs finite-life structure also not stated |
| Raise / fund size | Not stated ("large") |
| Claimed return | Net IRR stated, levered and unlevered. **The figures themselves were not included in what you sent** |
| Portfolio | 400+ loans, diversified across sectors 🟢 |
| Seniority | Not stated |
| Fund leverage | ~1.1x, disclosed 🟢 (read as debt-to-equity, the BDC convention 🟡) |
| Fees | 1.5% mgmt fee on gross assets, 1.0% on assets below the 200% asset-coverage threshold. Two-part incentive fee with hurdle + high-water mark (rates not stated) |
| Loss history | Through-cycle default and recovery rates disclosed 🟢 (figures not included) |

## 2. Return Stress-Test

You didn't include the fund's IRR figures, so I bracket the `01` Private Credit net range (8–12%) against the `05` comparator. The lock-up is **assumed at 5 yrs** 🔴 (mid-range of `01`'s 3–7). Output is from `scripts/benchmark_comparator.py`:

| Case | Net-to-LP IRR | vs HYG (4.83% 10yr) | 5-yr illiquidity hurdle (~300–400 bps) | vs 2yr Treasury (4.87%) |
|---|---|---|---|---|
| Bear | 8% | +317 bps | **Clears, thin** | +313 bps |
| Base | 10% | +517 bps | Clears comfortably | +513 bps |
| Bull | 12% | +717 bps | Clears comfortably | +713 bps |

**Swing assumptions:**
1. **Credit losses vs the disclosed through-cycle default/recovery rates.** Diversified senior lending lives or dies on realized loss. `01` puts historical recoveries at ~60–80% with wide dispersion by vintage.
2. **Base-rate path.** Floating-rate loan books earn less as short rates fall. The fund's own borrowing cost moves the other way on any fixed-rate debt. 🟡
3. **Leverage spread.** At 1.1x, each point of spread between asset yield and cost of fund debt is magnified. If the spread compresses, levered net converges toward unlevered net, or falls below it.

**Which IRR to benchmark.** HYG is an *unlevered* high-yield basket. The honest comparison is the fund's **unlevered** net IRR against HYG plus premium. The levered figure also includes leverage return that HYG doesn't carry. The fund discloses both, which is what `02` asks for. Run the unlevered figure through the table above: if it sits at or below ~8%, the illiquidity premium is being bought with leverage (`05` spread-table note on `CREDIT-01`).

Private-credit marks are smoothed (`05` → PRIV note). Any low volatility shown in fund materials understates true risk. 🟢

## 3. Where LP Returns Come From

- **Cash flow (loan interest income): dominant** 🟡. A BDC-style credit fund earns contractual coupon income. There is no exit-cap or terminal-value bet, so `GEN-08` (exit-dependent IRR) does not apply and does not fire.
- **Leverage: material but bounded** 🟢. At ~1.1x, the gap between the stated levered and unlevered net IRRs *is* the leverage contribution, and you can measure it directly because both are disclosed. That is the `05` unlevered-overlay test done by the GP for you. It is not a financing story (`GEN-07` does not fire): leverage is below the `02` 1.5x threshold, and the return base is contractual income, not cap-rate compression.
- **Exit: minimal.** Capital returns through repayments and distributions, not a sale.

Check once you have the numbers: if the levered-minus-unlevered gap exceeds about a third of the levered figure, most of the premium over HYG comes from leverage rather than credit selection 🟡. Not fired, since it can't be determined from the figures provided.

## 4. Fee Stack Summary

| Fee | Disclosed | `02` norm (Private credit) | LP read |
|---|---|---|---|
| Management fee | 1.5% of **gross assets**; 1.0% on assets below 200% asset coverage | 1–2% of committed, 1–1.5% of invested after the investment period | **Headline in range, base is not.** See below |
| Incentive fee (two-part) | Rate and hurdle **not stated**; high-water mark 🟢 | 10–20% above a 5–7% hurdle; aggressive if >25% or hurdle <5% | High-water mark is LP-favorable (`02`: "no carry on losses recouped"). Rate, hurdle %, and catch-up are unknown |
| Hurdle structure | Hurdle exists; soft vs hard **not stated** | Hard hurdle more LP-favorable; soft with 100% catch-up is aggressive | Can't grade |
| Servicing fee | Not stated | 0.25–0.5% of loan balance | Confirm none, or where it's charged |
| Fund-level leverage costs | Implied by 1.1x leverage | *Variable*; flag >1.5x | Below threshold 🟢 |
| Admin / IR | Not stated | $1–3k/LP or 0.1–0.3% | Confirm |

**The key finding is the fee base.** A fee charged on gross assets includes the assets bought with borrowed money. At ~1.1x debt-to-equity, gross assets ≈ 2.1x your equity 🟡:
- 2.0x equity (assets up to 1.0x leverage, i.e. 200% asset coverage) × 1.5% = 3.0%
- 0.1x equity (assets beyond that) × 1.0% = 0.1%
- **≈ 3.1% of equity per year, or ~310 bps** 🟡

The `02` range is 1–2%, and its aggressive threshold is >2%. That range is quoted on committed or invested capital, so this fee is above it on a like-for-like basis. The reduced rate above the asset-coverage threshold is the structural mitigant. It is standard for BDCs and cuts the manager's fee incentive to lever past 1.0x, but it doesn't remove it.

**Gross-to-net drag** (`scripts/fee_drag_calculator.py`; the 12% gross levered return on equity and 5-yr hold are ASSUMED 🔴):

| Scenario | Drag | Net LP |
|---|---|---|
| Mgmt fee only, read naively as 1.5% of equity | 150 bps | 10.50% |
| **Mgmt fee on gross assets (~3.1% of equity), incentive undisclosed → 0** | **310 bps** | **8.90%** |
| Same + illustrative 15% incentive over 6% hurdle, 100% catch-up (within `02` range) | 459 bps | 7.41% |

**Single figure: ≥310 bps per year of drag from the management fee alone, before incentive fee.** The total can't be computed until the incentive rate, hurdle, and catch-up are disclosed. The missing incentive terms are the finding (§6). If the fund's stated net IRR is truly net of all fees, the drag is already inside it. Confirm that it is (Q-FEE-01).

## 5. Red Flags

**RED:** none.

**YELLOW:**
- **`GEN-17` — Essential category-specific disclosure absent (seniority).** `01` lists seniority position as an essential Private Credit disclosure. "400+ loans" doesn't say whether the book is first-lien, unitranche, second-lien, or junior/equity sleeves. Mix determines recovery severity. → `Q-RISK-05` (recovery by seniority) + GP question below. 🟢
- **`GEN-11` — Distribution schedule not stated.** An IRR is quoted with no distribution cadence or policy (e.g. whether distributions are paid from net investment income or include return of capital). → `Q-DIST-01`. 🟢 Mild for an income vehicle, but it's a stated fact gap.

**Probed, not fired (evidence clears them):**
- `CREDIT-01` (fund leverage stacked on loan leverage): ~1.1x is disclosed, below the `02` 1.5x threshold, and the IRR is shown levered and unlevered. That is `Q-RISK-06`'s good answer, already given. Keep the gross-assets fee in view: it pays the manager more as leverage rises (§4).
- `CREDIT-02` (sector concentration): 400+ loans diversified across sectors. Still ask for the single-largest-sector exposure (`Q-RISK-05` pairing below).
- `HML-03` / `HML-04` (default / recovery not disclosed): both disclosed, through-cycle.
- `GEN-16` (no fee or waterfall disclosure): structure is disclosed. Only the incentive *rates* are missing, which is a §6 gap, not a fired flag.
- `GEN-07` / `GEN-08` (financing story / exit-dependent IRR): not applicable to a coupon-income credit book at 1.1x (§3).

**Not assessable from what was provided (unverified, routed to must-asks):** `GEN-01` (co-invest), `GEN-05` / `GEN-14` (net-to-LP realized track record), `GEN-02` (regulatory history), `GEN-06` (affiliate fees, e.g. an affiliated administrator), `HML-05` (management-fee step-down; relevance depends on whether the fund is finite-life or perpetual). None fires: no sponsor or track-record claim was made that could be tested.

## 6. Missing Disclosures

Against the `01` Private Credit essentials and the `02` private-credit fee inventory:

1. **The net IRR figures themselves** (levered and unlevered). You said they're stated but didn't include them, so §2 is bracketed on the `01` range.
2. **Seniority position** of the loan book (`01` essential) → `GEN-17`.
3. **Average loan size** (`01` essential; "400+ loans" gives count only).
4. **Incentive fee rates**: income-fee %, capital-gains-fee %, hurdle %, soft vs hard hurdle, catch-up rate (`02`).
5. **Sector mix** detail and largest single-sector exposure ("diversified" is a claim; `01` asks for the mix).
6. **Hold / liquidity terms**: finite-life vs perpetual, lock-up, redemption or tender mechanics.
7. **Distribution schedule / policy** → `GEN-11`.
8. **Servicing, admin, and fund-expense** lines (`02`).
9. **Sponsor identity, co-invest, and realized track record.**
10. **Default and recovery figures** — disclosed per the summary, but the numbers weren't in what you sent.

**Assumed inputs used above (each a gap):** 5-yr lock-up, 12% gross levered return on equity, debt-to-equity reading of "1.1x," and the incentive terms in the bracket scenario.

## 7. GP Alignment

- **Co-invest:** not stated → unverified. `Q-GP-01`.
- **Track record:** no net-to-LP, realized figures given → **unverified**, not a negative. For a credit fund, "realized" means loss-adjusted, net-to-LP returns on vintages that have repaid through a stress period (2020, 2022–23). `Q-GP-02`.
- **Fee alignment: mixed.**
  - *Positive* 🟢: high-water mark on the incentive fee; a two-part fee with a hurdle; reduced management fee on leverage above the 200% coverage line; levered and unlevered IRR both shown (transparency on the one lever that most flatters credit returns).
  - *Watch* 🟡: a management fee on gross assets rewards the manager for asset growth and leverage whether or not credit performance holds up. The step-down above 1.0x softens this but doesn't neutralize it.
- **Affiliate fees:** not stated. BDC-style structures often use an affiliated administrator → `Q-FEE-02`.

## 8. Questions for the GP

**Must-ask**

| # | Question | Bad-answer signal | ID |
|---|---|---|---|
| 1 | "Can you provide the complete fee schedule: income-incentive %, capital-gains-incentive %, hurdle rate, whether the hurdle is hard or soft, the catch-up rate, and confirmation that the stated net IRR is after every fee including fund expenses?" | "Standard BDC terms"; partial list; "the prospectus has it" without producing it | `Q-FEE-01` (`GEN-16`) |
| 2 | "What is the fund's leverage ratio, how does it move through a cycle, and what are the stated levered and unlevered net IRRs?" | Already well answered in principle. Bad now: unlevered figure not net of the same fees, or a leverage ceiling stated with no number | `Q-RISK-06` (`CREDIT-01`) |
| 3 | "What is your historical default rate and realized recovery rate, including through 2020 and 2022–23, **broken out by seniority** (first-lien vs second-lien/junior)?" | Default rate without recovery; blended figures only; "we've never had a loss"; silence on 2022–23 | `Q-RISK-05` (`HML-03`, `HML-04`, `GEN-17`) |
| 4 | "What is the projected distribution schedule, and how much of each distribution is net investment income versus return of capital?" | "We distribute when the portfolio supports it"; no cadence; distributions exceeding NII with no explanation | `Q-DIST-01` (`GEN-11`) |
| 5 | "How much of your own capital is in the fund, on the same terms as LPs?" | Fee waiver counted as co-invest; token amount on better terms | `Q-GP-01` (`GEN-01`) |
| 6 | "Can you restate your track record as net-to-LP returns on fully realized (repaid) vintages?" | Only gross portfolio yield or NAV marks; can't separate realized from marked | `Q-GP-02` (`GEN-05`, `GEN-14`) |
| 7 | "Have you or your principals faced any regulatory action, enforcement, or investor litigation?" | "Nothing material"; a search turns up something undisclosed | `Q-GP-03` (`GEN-02`) |
| 8 | "What are my options if I need to exit before the hold ends?" | "A secondary market may develop"; tender or redemption limits not stated. An honest "there's no liquidity" is a *good* answer | `Q-LIQ-01` |

**Nice-to-ask**

| # | Question | Bad-answer signal | ID |
|---|---|---|---|
| 9 | "What is the sector breakdown and your single-largest-sector exposure?" | "Diversified" with no table; one sector dominant | `03` → `CREDIT-02` response |
| 10 | "Which service providers (administrator, servicer) are GP-affiliated, and what do they charge?" | "All arm's-length" without naming providers | `Q-FEE-02` (`GEN-06`) |
| 11 | "Does the management fee step down if the fund enters a harvest / wind-down period?" | Full gross-asset fee charged on a shrinking book with no step-down | `03` → `HML-05` response |
| 12 | "How have headcount and credit-monitoring capacity grown with AUM?" | 400+ loans monitored by a flat team; no named workout function | `Q-GP-04` (`GEN-04`) |
| 13 | "When will tax documents (K-1 or 1099) be delivered each year?" | "As soon as we can"; history of extensions | `Q-LIQ-02` |

## 9. Diligence Checklist

- **Offering document / prospectus or PPM:** incentive-fee mechanics, hurdle and catch-up, fee base definition, expense caps, leverage limits.
- **Audited financials:** confirm leverage, NII vs distributions, non-accrual rate, and the default/recovery figures quoted.
- **Loan-level schedule of investments:** seniority mix, average loan size, sector and top-10 borrower concentration.
- **Valuation policy:** third-party valuation agent? How often are level-3 marks independently tested (smoothed-mark caveat, `05`)?
- **Credit facility terms:** lenders, maturity, covenants, and what happens to the fund if asset coverage approaches the regulatory floor.
- **Background / regulatory:** SEC Form ADV Part 2 for the adviser (`02` provenance), principals' regulatory history.
- **Liquidity terms:** redemption / tender mechanics, gates, or fund term.

## 10. Verdict

**Pursue with conditions.**

**Reasoning.** This is a merits verdict, not "as presented." The fund discloses the essentials that normally sink credit-fund screens: leverage (moderate, ~1.1x), diversification (400+ loans, cross-sector), through-cycle default and recovery, and levered vs unlevered IRR. No RED fires, and the `CREDIT-01` concern is answered in the disclosure itself. On the `01` range (8–12% net), a 5-yr lock-up clears HYG + illiquidity hurdle at the base and bull cases, and is thin at 8% (§2).

**Biggest swing factor.** The **unlevered net IRR after the true fee load**. The gross-assets fee base alone costs about 310 bps a year on equity. Whether the fund still pays you a premium over HYG and the ~4.87% 2yr Treasury *without* leverage depends on that figure and the undisclosed incentive terms.

**Conditions:**
1. Unlevered net IRR (after all fees and expenses) ≥ ~8%, i.e. it clears HYG (4.83%) by at least the 300–400 bps 5-yr illiquidity hurdle on its own, not only with leverage.
2. Incentive fee within `02` norms: ≤20% over a ≥5% hurdle, and not a soft hurdle with 100% catch-up.
3. Loan book predominantly senior secured, confirmed by the schedule of investments. Recovery rates hold at the seniority level (`GEN-17`).
4. Liquidity terms you can live with: stated lock-up or tender mechanics, answered honestly (`Q-LIQ-01`).
5. Realized, net-to-LP track record through at least one stress period (`Q-GP-02`).

**Who it suits.** An LP seeking diversified, income-oriented senior credit exposure who can accept multi-year illiquidity and smoothed-mark volatility reporting. It suits you if you want a premium over liquid high yield rather than equity-like upside. It doesn't suit someone who needs capital back on short notice, or who would compare it gross against HYG.

**What would have to be true.** The unlevered net return, after a ~3%-of-equity management fee and the incentive fee, still earns a real spread over HYG and Treasuries, and the disclosed through-cycle losses reflect a book that is mostly first-lien. If the unlevered net lands near HYG, the premium comes from leverage, and the verdict moves to Pass.
