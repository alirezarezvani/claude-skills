# Deal Analysis — Sun Belt value-add multifamily syndication
*Produced by the passive-deal-screener skill from the deal in `input.md`. Illustrative example; figures route to the `references/` files, not memory.*

**Verdict: Pursue with conditions.** As underwritten, this is a financing story: the 16% / 2.0x rests on 50bps of exit-cap compression (5.5% in, 5.0% out) and on floating-rate bridge debt that has to be refinanced well before the 5-year exit. It is worth more diligence only if the GP can show the IRR at a flat 5.5% exit cap, the full debt and rate-cap terms, and a realized, net-to-LP restatement of the "30% IRR" track record. **Biggest swing factor: the exit cap.**

*Screening output only, not investment advice.*

Confidence tags: 🟢 stated in the deal or taken from a reference · 🟡 inferred · 🔴 assumed or unverifiable.

---

## 1. Deal Snapshot

| Field | Value |
|---|---|
| Asset class | Multifamily, value-add (280 units) 🟢 |
| Deal type | Equity syndication (single asset) 🟢 |
| Sponsor | **Not stated** |
| Geography | "Sun Belt". **Metro and submarket not stated** |
| Minimum investment | **Not stated** |
| Hold | 5 years 🟢 (bottom of the 5–7 yr category norm, `01`) |
| Raise | $50M equity 🟢 |
| Purchase price / total capitalization / LTV | **Not stated** |
| Debt | Bridge, floating rate 🟢. **Amount, LTV, spread, maturity, extensions, and rate cap not stated** |
| Claimed return | 16% IRR / 2.0x equity multiple 🟢. **Gross vs net-to-LP not stated** |
| Waterfall | 8% pref, 20% promote, American (deal-by-deal) 🟢. **Catch-up, cumulative/compounding, and clawback not stated** |
| Cap rates | Going-in 5.5%, exit 5.0% 🟢 |
| Fees | 2% acquisition, 1.5% annual asset management, 1% disposition 🟢. **Fee bases and all other fees not stated** |
| Track record | "30% IRR across prior deals" (unverified; see §7) 🔴 |

## 2. Return Stress-Test

**Gross or net.** The 16% is not labeled. Retail syndication pitch decks often quote a projected LP figure, but the skill does not compare gross to gross, so both readings are run below. The GP must state which one it is (§8).

**Fee-drag estimate (`fee_drag_calculator.py`)**, 5-yr hold, 8% pref, 20% promote, disclosed fees, undisclosed fees passed as 0:

| Reading of the 16% | Catch-up | Est. net-to-LP IRR | Total drag |
|---|---|---|---|
| Gross deal IRR | 0% (none) | 12.3% | 369 bps/yr |
| Gross deal IRR | 100% | 11.4% | 464 bps/yr |
| Gross deal IRR, fees on a price basis 🔴 (acq ≈6%, disp ≈4% of equity) | 100% | 10.0% | 604 bps/yr |
| Already net-to-LP | — | 16.0% | — |

**Scenarios (net-to-LP, compared with VNQ 4.92% 10yr trailing plus a ~300–400bps hurdle for a 5-yr lock-up, from `05`):**

| Case | Swing assumptions | Est. net-to-LP | vs VNQ | Clears hurdle? |
|---|---|---|---|---|
| **Bull** (the 16% is already net) | Pro forma rent growth hits; 5.0% exit cap; bridge refinances on assumed terms | 16.0% 🟡 | +1,108 bps | Clears comfortably |
| **Base** (the 16% is gross) | Same pro forma, with the fee stack and promote applied | ≈11.4% 🟡 | +644 bps | Clears comfortably |
| **Bear** (exit at the going-in cap) | Exit cap flat at 5.5%; gross falls to ≈10.7% (illustrative 🔴, see §3) | ≈6.8% 🔴 | +158 bps | **Thin / fails** |

The three swing assumptions are: (1) the **exit cap**, (2) **rent growth** from the renovation premium, and (3) the **refinance** out of bridge debt.

Two findings from `05`:
- The **10yr Treasury is 5.18%** (2026-09-24). The bear case is only about 160bps above a risk-free bond. That does not pay for a 5-year illiquid, single-asset, levered position.
- **Beats its own pro forma but trails the comparator plus the premium.** A deal that simply holds cap rates flat and hits its rent plan could still leave the lock-up uncompensated. Dispersion widens the gap further: the median value-add deal realizes 12–15% net (`01`), not the 14–18% marketing range.

## 3. Where LP Returns Come From

**Exit share 🟡.** 2.0x over 5 years at a 16% IRR implies about 5.4% a year in interim distributions and about a 1.73x terminal distribution, assuming level distributions. A value-add ramp would back-load it further. On those numbers, **about 73% of the LP's profit arrives at exit**. That is above the 60% line, so rule 3 applies (`GEN-08`). The in-place yield is consistent with the 5–8% stabilized cash-on-cash norm (`01`). It is not what drives the IRR.

**Cap compression 🟢.** Exiting at 5.0% instead of 5.5% on the same NOI lifts sale value by 10%. Every other assumption held constant, that is the difference between these two paths:
- With the compression: the pro forma.
- Without it (illustrative 🔴, assuming about 70% leverage and about 30% NOI growth over the hold): sale value roughly 9% lower → about 0.4x of the 1.0x profit disappears → about a 1.6x / 10.7% gross outcome → about 6.8% net.

The leverage and NOI inputs are assumed, so the magnitude is not a basis for a decision. The direction is not in doubt: the cap-rate assumption carries a large part of the headline.

**Leverage 🟢/🟡.** The NCREIF NPI unlevered, in-place baseline is 5.00% (residential 5.3% in 2025), almost all of it income (`05`). A 16% levered IRR leaves about 11 points coming from leverage and assumed appreciation, not operations. The leverage is short-term floating bridge debt.

**Read.** This is an exit- and leverage-driven return: `GEN-07` + `GEN-08` + `EQUITY-06`, the financing-story cluster. The renovation thesis (an asset story) is real but is not what produces the 16%.

## 4. Fee Stack Summary

| Fee | Stated | `02` norm | Read |
|---|---|---|---|
| Acquisition | 2%, basis not stated | 1–2% of equity, or 0.5–1.5% of purchase price. Aggressive above 2% of price | Top of the range on equity. **At the aggressive threshold if charged on purchase price** (≈3x equity → ≈6% of equity 🔴) |
| Asset management | 1.5% annual, basis not stated | 1–2% of equity raised | In range. Confirm equity raised vs invested capital vs revenue |
| Disposition | 1% (of sale price, per `02` norm) | 0.5–1% of sale price | Top of the range. On a levered sale price it is ≈3–4% of equity 🔴. Check for stacking with the broker commission |
| Promote | 20% over 8% pref | 15–30% over 6–10% | In range. Catch-up not stated |
| Loan placement / refinance | **Not stated** | 0.5–1.5% of loan per event | **Likely present.** The bridge plan implies at least one refinance event |
| Construction management | **Not stated** | 3–5% of hard costs | Common on interior-renovation value-add. Absence is a question, not a pass |
| Admin / IR / K-1 | **Not stated** | 0.1–0.5% of equity or $1–3k per LP | Passed as 0. Real drag is likely higher |
| Property management | **Not stated** | — | Affiliate check (`GEN-06`) |

**Gross-to-net drag: ≈370–460 bps/yr** on the disclosed fees (0% vs 100% catch-up). It rises to **≈600 bps/yr** if the acquisition and disposition fees are charged on price. That is **before** the undisclosed loan-placement, refinance, construction-management, and admin fees, which were passed as 0 and are §6 gaps. The drag cannot be computed completely from this disclosure, and that is itself a finding.

## 5. Red Flags

**RED**
- **`EQUITY-06` Exit cap below going-in (5.0% vs 5.5%)** 🟢. The headline IRR assumes 50bps of unproven cap compression. LP exposure: a flat exit cap alone moves net IRR from the pro forma toward the ~7% range (illustrative 🔴, §3).
- **`GEN-07` Financing story** 🟢/🟡. Leverage plus cap compression, not operations, carries the return. About 11 of the 16 points sit above the 5.00% unlevered NPI baseline. LP exposure: the return depends on the rate path and on credit availability.
- **`GEN-08` Exit-dependent IRR (≈73% of profit at exit)** 🟡. The IRR is a bet on the future sale. The GP must decompose it (Q-DS-01).
- *Cluster:* `GEN-07` + `GEN-08` + `EQUITY-06` all fire, so the deal is a **financing story**.
- **`GEN-09` Debt maturity inside the hold** 🟡. Bridge loans run 6–18 months per `01`, far shorter than the 5-year plan. LP exposure: a forced refinance or sale into whatever market exists at maturity.
- **`GEN-05` / `GEN-14` Unverified track record** 🔴. "30% IRR across prior deals" does not say whether it is project-level, GP-level, or net-to-LP, or realized or marked. A 30% figure is about double the 12–15% realized value-add norm (`01`). Treated as **no track record** until restated.

**YELLOW–RED**
- **`EQUITY-07` Refi-dependent plan** 🟡. Bridge-to-permanent is the implied capital path. LP exposure: the 2022–24 frozen-refi pattern, which can mean suspended distributions or a capital call.
- **`GEN-10` Rate-cap expiry risk: not confirmed.** Floating debt is stated but the cap is not. This is a must-ask, not a fired flag. If the cap expires before maturity or before the refinance, debt service spikes and erases the ~5% cash yield.
- **`GEN-15` Missing financials** 🟢. No rent roll, T-12, or debt terms.
- **`GEN-16` Partial fee and waterfall disclosure** 🟢. Headline fees only. Catch-up, clawback, and the loan, construction-management, and admin fees are missing.
- **`GEN-06` Affiliate fees: unknown.** Property management and construction management on a 280-unit renovation are common affiliate lines. Probe; not fired.

**YELLOW**
- **`GEN-11` No distribution schedule** 🟢. An IRR with no J-curve disclosure.
- **`GEN-13` No sensitivity or downside case** 🟢. A single-point pro forma.
- **`GEN-17` Category-essential disclosures absent** 🟢. No exit-cap sensitivity and no record of prior multifamily *exits* (`01`).
- **`GEN-18` Rent-growth assumption** 🟡. The plan is "raise rents", but no submarket supply or absorption data is given. Probe.
- **`EQUITY-01` / `EQUITY-02` Deal-by-deal waterfall, clawback not stated.** A 20% promote is mid-range and this is a single asset, so the cross-deal leakage risk is limited. Stays YELLOW unless the promote tiers escalate or a clawback is expressly absent.
- **`EQUITY-03` / `EQUITY-05` Catch-up rate and cumulative status not stated.** The 100% catch-up case costs about 95 bps/yr more than no catch-up (§4).

Not fired: `GEN-01` (co-invest not stated → must-ask), `GEN-02` (background check), `GEN-12` (no T-3/T-6 was offered either; covered by `GEN-15`).

## 6. Missing Disclosures

Measured against `01` (multifamily value-add essentials) and `02` (equity fee inventory):
- Rent roll and **T-12 actuals** (`GEN-15`)
- **Exit-cap sensitivity** and the IRR at a flat or higher exit cap (`GEN-13`, `GEN-17`)
- **Full debt terms:** loan amount/LTV, index and spread, maturity, extension tests, **rate cap strike, term and expiry**, and prepayment (`GEN-09`, `GEN-10`)
- **Refinance assumptions:** rate, proceeds, DSCR, timing (`EQUITY-07`)
- **GP track record on prior multifamily exits**: realized and net-to-LP (`GEN-05`, `GEN-14`)
- Whether the 16% IRR is gross or net-to-LP
- Distribution schedule and J-curve (`GEN-11`)
- Waterfall detail: catch-up, cumulative or compounding pref, clawback, promote tiers (`GEN-16`)
- Fee bases (equity vs price) and the missing fee lines: loan placement, refinance, construction management, admin/IR, property management (`GEN-16`, `GEN-06`)
- Sponsor identity, submarket, purchase price, capex budget per unit, minimum investment, GP co-invest (`GEN-01`)
- Renovation capex budget and funding source. This is flagged only for whether it is funded or needs a capital call; scope and bids are the operator's diligence.

These gaps are material but **do not make the deal un-underwritable**. The core return story (IRR, multiple, caps, waterfall, fees) is disclosed, so this is a merits verdict with conditions, not "Pass as presented".

## 7. GP Alignment

- **Co-invest:** not stated. Cash amount and pari-passu terms are unknown (`GEN-01` → Q-GP-01). 🔴
- **Track record:** "30% IRR across prior deals" is **unverified**. It does not say whether the figure is project-level, GP-level, or net-to-LP, or whether the deals are realized or marked. A 30% net-to-LP realized record in value-add multifamily would sit roughly twice the category's realized norm, so the burden of proof is on the GP. Until it is restated as **realized, net-to-LP**, treat it as no track record (`GEN-05`, `GEN-14`). 🔴
- **Waterfall alignment:** an 8% pref and 20% promote are market-standard 🟢. Deal-by-deal on a single asset is a modest concern. Catch-up and clawback are unknown.
- **Fee alignment:** about 60 bps/yr of one-time fees (acquisition plus disposition, higher if charged on price) plus 150 bps/yr of asset management are **paid whether or not the LP earns the pref**. The GP earns about 2.1%/yr regardless of outcome before any promote. The acquisition fee in particular rewards closing, not performance.
- **Affiliates:** unknown (`GEN-06`).

## 8. Questions for the GP

**Must-ask**

| # | Question (ID) | Flag | Bad-answer signal |
|---|---|---|---|
| 1 | **Q-EXIT-01** "Why is the exit cap below the going-in cap, and what's the IRR at an exit cap equal to or above going-in?" | `EQUITY-06` | "Cap rates will compress". The IRR breaks at a flat exit cap. No sensitivity offered. |
| 2 | **Q-DS-01** "What share of projected LP IRR comes from in-place cash flow versus the exit, and what's the IRR at a flat exit cap?" | `GEN-08` | Can't or won't decompose the IRR. "Real estate always appreciates". Falls below the pref at a flat cap. |
| 3 | **Q-DS-02** "Strip out leverage and cap-rate compression — what is the unlevered, in-place return?" | `GEN-07` | Levered IRR is the only figure. "Leverage is just how the deal works." |
| 4 | **Q-RISK-01** "When does the debt mature relative to the projected hold, and what's the refinance or extension plan?" | `GEN-09` | Maturity inside the hold. "We'll refinance" with no terms. |
| 5 | **Q-RISK-02** "When does the rate cap expire relative to debt maturity, and what's the cost to extend it at current pricing?" | `GEN-10` | Cap expires before maturity. Extension cost not modeled. "Rates should be lower by then." |
| 6 | **Q-EXIT-02** "Does the business plan depend on a refinance, and what happens to distributions if the refi isn't available on the assumed terms?" | `EQUITY-07` | Capital return requires a refi at lower rates. No fallback. "The refi market will reopen." |
| 7 | **Q-GP-02** "Can you restate your track record as net-to-LP IRR on fully-realized, exited deals only?" | `GEN-05`, `GEN-14` | Only project-level or GP-level IRR. "Most deals are still performing". Can't separate realized from unrealized. |
| 8 | **Q-DS-03** "What is the return under a bear case — flat rents, higher exit cap, no refinance?" | `GEN-13` | No downside case. "We underwrite conservatively" with nothing to show. |
| 9 | **Q-RISK-03** "Can you provide trailing-twelve-month actuals, the rent roll, and complete debt terms?" | `GEN-15` | T-3/T-6 only. "Confidential until you commit." |
| 10 | **Q-FEE-01** "Can you provide the complete fee schedule and the full distribution waterfall?" Also ask: is the 16% gross or net-to-LP, and what are the fee bases? | `GEN-16` | "Standard market fees". "The PPM has it" without producing it. |
| 11 | **Q-FEE-03** "Is the waterfall deal-by-deal or whole-of-fund, and is there a clawback?" | `EQUITY-01`, `EQUITY-02` | Can't explain the catch-up. "You get paid when we get paid." |
| 12 | **Q-FEE-04** "What preferred return do LPs receive before the GP earns promote, and is it cumulative and compounding?" | `EQUITY-05` (and `EQUITY-03` catch-up) | Non-cumulative pref. A 100% catch-up that is not disclosed until asked. |
| 13 | **Q-FEE-02** "Which service providers are GP-affiliated, what do they charge, and are those rates third-party-benchmarked?" | `GEN-06` | "All arm's-length" without naming providers. |
| 14 | **Q-GP-01** "How much of your own capital is in this deal, on the same terms as LPs?" | `GEN-01` | "Our sweat equity is our investment". Co-invest is a fee waiver. |
| 15 | **Q-GP-03** "Have you or your principals faced any regulatory action, enforcement, or investor litigation?" | `GEN-02` | "Nothing material"; a search surfaces something undisclosed. |
| 16 | **Q-MKT-01** "What submarket supply pipeline and absorption data support the rent-growth assumption?" | `GEN-18` | Sun Belt metro optimism standing in for submarket data. No supply pipeline acknowledged. |
| 17 | **Q-DIST-01** "What is the projected distribution schedule, and at what milestones does LP capital start returning?" | `GEN-11` | "We'll distribute when the deal supports it". No milestones. |
| 18 | **Q-LIQ-01** "What are my options if I need to exit before the hold period ends?" | — | "A secondary market may develop". |

**Nice-to-ask**
- **Q-DIST-02** "When are capital calls expected, and what's the consequence of a missed or late call?" Bad answer: "calls as needed", punitive dilution. *(Escalate to must-ask if the rate-cap or refi answers expose a funding gap.)*
- **Q-GP-04** Team and monitoring capacity vs AUM (`GEN-04`, not fired). Bad answer: "we're lean and efficient" as the whole answer.
- **Q-LIQ-02** K-1 delivery timing. Bad answer: a history of extensions.

## 9. Diligence Checklist

- [ ] **PPM and operating agreement:** confirm the waterfall (catch-up, clawback, cumulative pref), every fee and its basis, and capital-call and dilution terms.
- [ ] **Loan documents / term sheet:** maturity, extension tests, rate cap strike, expiry, and replacement-cost escrow. Confirm independently rather than from the deck.
- [ ] **Sponsor background:** SEC / FINRA / state regulator searches and litigation search on the principals (`GEN-02`).
- [ ] **Track-record verification:** a realized-deal list with LP-level distribution statements or K-1s, or references from prior LPs on exited deals.
- [ ] **Rent roll and T-12:** reconcile against the pro forma's in-place NOI and the 5.5% going-in cap.
- [ ] **Third-party sale and rent comps:** independent support for the 5.0% exit cap and the post-renovation rent premium in the specific submarket.
- [ ] **Appraisal and lender sizing:** confirm the purchase price, the LTV, and the lender's own underwritten exit and refinance assumptions.

## 10. Verdict

**Pursue with conditions.**

**Why not Pass.** The core return story is disclosed: IRR, multiple, both cap rates, waterfall headline, and fees. The fee stack and the 8%/20% structure sit within `02` norms. The benchmark math clears VNQ plus the illiquidity hurdle if the pro forma holds, whether the 16% is gross (≈11.4% net) or net.

**Why not a clean Pursue.** The headline depends on three things the LP cannot yet verify:
1. **The exit cap (biggest swing).** 50bps of assumed compression. At a flat cap, the illustrative net return falls to around 7%. That is thin against VNQ, and only about 160bps over a 5.18% Treasury.
2. **The bridge debt.** It matures inside the hold by construction, so the plan needs a refinance, and a floating rate with an undisclosed cap is the 2022–24 failure pattern.
3. **A track record that cannot be used.** "30% IRR" is unlabeled and about twice the realized category norm.

**Conditions to proceed:**
1. IRR at a flat 5.5% exit cap still clears the 8% pref and roughly 9% net (VNQ plus the hurdle).
2. Debt terms show a rate cap covering at least the loan term through the planned refinance, with extension cost budgeted, and a no-refi fallback that does not require a capital call.
3. The track record is restated as realized, net-to-LP, multifamily exits, with a clear answer on whether the 16% is gross or net.
4. The full fee schedule, including bases and any loan, construction, admin, or affiliate fees, keeps total drag at or under about 500 bps/yr.

**Walk away if** the GP cannot produce the IRR at a flat exit cap, if the rate cap expires before the refinance window with no budgeted extension, or if the track record can only be given as project-level or unrealized.

**Who it suits.** An LP who explicitly wants a leveraged cap-rate and rate-path bet on Sun Belt multifamily, can hold 5+ years with no liquidity, can meet a possible capital call, and sizes this as a satellite position. It does not suit an LP looking for income or downside protection: the in-place yield (about 5%) is roughly the unlevered NPI baseline, and everything above it is financing and exit.
