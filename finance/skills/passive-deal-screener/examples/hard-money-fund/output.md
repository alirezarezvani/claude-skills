# Deal Analysis — Hard-money bridge fund (well-disclosed)
*Produced by the passive-deal-screener skill from the deal in `input.md`. Illustrative example; figures route to the `references/` files, not memory.*

**Verdict: Pursue.** This is a well-disclosed senior-secured bridge fund. It answers the questions that sink most hard-money pitches: LTV on as-is value, default and recovery rates through 2020 and 2022–23, geographic mix, and a fee step-down. Its 9% net target is inside the 8–10% category norm and clears HYG plus the illiquidity hurdle for a 3–5 year lock-up. No RED flags fired. The biggest swing factor is **loss severity in the next downturn**: whether the 92% recovery holds if defaults double or triple. The open items (performance fee, servicing fee, fund leverage, GP co-invest, realized net-to-LP history, liquidity terms) are confirmations to close in diligence. None of them is a reason to stop.

*Screening output only, not investment advice.*

---

## 1. Deal Snapshot

| Field | Value | Tag |
|---|---|---|
| Asset class | Hard Money / Bridge Loan | 🟢 |
| Deal type | Debt fund, senior secured bridge loans | 🟢 |
| Sponsor | Not stated | — |
| Geography | 12 states; no single metro >15% | 🟢 |
| Minimum investment | Not stated | — |
| Hold / fund term | Not stated. Category norm is 6–18 months per loan and a 3–5 year fund commitment (`01`). An investment period is mentioned, which implies a closed-end structure. | 🟡 |
| Raise / fund size | Not stated | — |
| Claimed return | 9% net target to LPs | 🟢 |
| Portfolio LTV | 68% as-is / 72% ARV | 🟢 |
| Credit history | 3.1% default rate, 92% realized recovery, including 2020 and 2022–23 | 🟢 |
| Loan grading | A–D, with the grade mix disclosed (the mix itself was not in the pasted text) | 🟢 / 🔴 contents |
| Fees | 1.5% management fee, stepping down to 1.0% after the investment period | 🟢 |

## 2. Return Stress-Test

The comparator is **HYG (4.83% 10yr)** plus the duration-matched Treasury (3mo 4.24%, 2yr 4.87%) (`05`). I assumed a 4-year lock-up (the midpoint of `01`'s 3–5 year fund norm) because the term is not stated. 🔴

| Case | Net to LP | Swing assumptions | Over HYG | Over 3mo T-bill | vs ~300–400bps hurdle |
|---|---|---|---|---|---|
| **Base** | 9.0% (stated target) | Defaults ~3.1% at 92% recovery → loss ≈ 25bps/yr if 3.1% is an annual rate 🟡 | **417bps** | 476bps | **Clears comfortably** |
| **Bull** | ~9.5% 🟡 | Default interest and late fees accrue to the fund (`02`); full deployment; no cash drag | ~470bps | ~525bps | Clears |
| **Bear** | ~7.0% 🟡 | Defaults roughly triple to ~9% and recovery falls to ~80% → loss ≈ 180bps/yr; some cash drag during the workout | **217bps** | 276bps | **Thin / fails** the hurdle |

Swing assumptions, named:
1. **Loss severity.** 92% recovery is the anchor number. It is realized, which is good, but it came from a book with a 3.1% default rate. Recovery rates tend to fall at the same time default rates rise.
2. **Default frequency by grade.** The A–D mix sets how quickly defaults can rise. A book weighted toward C/D loans reaches the bear case faster.
3. **Rate and deployment path.** This is short-duration paper, so coupons reprice as loans roll. A falling-rate environment compresses the 9% faster than it compresses HYG. Idle cash between loans also dilutes returns.

Script output (`benchmark_comparator.py`): 9.0% net → 417bps over HYG, 4-year hurdle ~300–400bps, **CLEARS comfortably**. 7.0% net → 217bps, **THIN / FAILS**. The base case earns the lock-up. It takes a real credit event, not a mild one, to break it. The spread over the 2yr Treasury (4.87%) is ≈413bps in the base case and ≈213bps in the bear case.

This is necessary, not sufficient: dispersion means the median fund underperforms the marketed figure (`05`).

## 3. Where LP Returns Come From

- **Cash flow: essentially 100%.** 🟢 The return is loan coupon plus borrower-paid origination points, received as interest over 6–18 month loans. There is no terminal-value or exit-cap bet, so `GEN-08` (exit-dependent IRR) does not apply.
- **Exit: none** in the equity sense. Principal comes back as loans repay.
- **Leverage: unknown at the fund level.** 🔴 The underlying loans are the fund's asset, and the borrower's equity cushion is the 32% as-is gap. What is not stated is whether the fund itself borrows (a credit line or warehouse facility) to lever a ~7–8% loan yield into 9%. If it does, the financing-story concern (`GEN-07`) comes back at the fund level. That is a must-ask (§8), not a fired flag.

**Read:** this is an income story, not a financing story, unless fund leverage turns out to be material.

## 4. Fee Stack Summary

| Fee | Disclosed | `02` norm | Read |
|---|---|---|---|
| Fund management fee | 1.5% → 1.0% after the investment period | 1–2% of AUM; a step-down is expected | 🟢 In range. Step-down present, so `HML-05` does **not** fire. |
| Basis of the management fee | Not stated (committed, invested, or AUM) | — | 🔴 Ask. |
| Performance fee / carry | Not stated | 10–20% above a 5–8% hurdle; aggressive if >25% or no hurdle | 🔴 Gap |
| Servicing fee | Not stated | 0.25–0.5% of loan balance, annual; aggressive >1% | 🔴 Gap |
| Origination points (borrower-paid) | Not stated | 1–3 points; <1 means thin yield, >5 is predatory | 🔴 Who keeps the points: the fund or the GP? |
| Late fees / default interest | Not stated | Should go to the fund, not the GP | 🔴 Check for a GP "workout fee" |
| Admin / wind-down | Not stated | 0.1–0.5% admin; 0.5–1% wind-down | 🔴 |

**Gross-to-net drag: ≈125–150bps/yr from the disclosed stack.** This comes from `fee_drag_calculator.py` using the 1.5% management fee alone (150bps) and a ~1.25% blended rate across the step-down (125bps). All undisclosed fees were passed as 0, and the 4-year hold is ASSUMED.

Backing out the gross: a 9% net with 150bps of drag implies ≈10.5% gross from the loan book. That sits just below the 11–13% gross that `01` calls common. It could mean the book is priced conservatively. It could also mean fees not yet disclosed sit between gross and net. If the true gross is 11–13%, then **50–400bps of drag is unaccounted for**: carry, servicing, or a GP share of points.

**The stated net target is the LP's protection here.** Confirm that the 9% is net of *every* layer, and get the full schedule so the drag can be computed rather than inferred. This fires `GEN-16` at YELLOW for partial disclosure, not the undisclosed case.

## 5. Red Flags

**RED:** none.

**YELLOW**
- **`GEN-16` Partial fee disclosure.** The management fee and step-down are disclosed. Carry, servicing, the split of points, and admin are not. The LP exposure is up to several hundred bps of drag between an 11–13% gross and the 9% net that cannot be attributed yet. → `Q-FEE-01`
- **`GEN-11` No distribution schedule.** A net target with no stated distribution cadence (monthly or quarterly) and no reinvestment election. For a debt fund, the LP's return is the distribution stream, so the cadence matters. → `Q-DIST-01`

**Checked and not fired** (cited so the absence is visible):
- `HML-01`: as-is LTV is disclosed (68%).
- `HML-02`: 12 states, max metro 15%.
- `HML-03` / `HML-04`: default and recovery rates are both disclosed, through both stress periods.
- `HML-05`: the step-down is present.
- `GEN-07`, `GEN-08`: no exit or leverage dependency at the loan level. Fund-level leverage is open (§3).

**Open, not fired** because deciding them would need a 🔴 assumption; each is routed to a must-ask:
- `GEN-01` (co-invest)
- `GEN-05` / `GEN-14` (realized net-to-LP track record)
- `GEN-06` (affiliate servicing / points)
- `CREDIT-01` (fund leverage). This ID is outside the routed `HML-` prefix, but the same mechanism applies to a levered bridge fund.

**No cluster.** The two YELLOWs are disclosure-completeness items, not a structural pattern.

## 6. Missing Disclosures

Against `01` (Hard Money essentials) and `02` (hard-money fee inventory):

| Missing | Why it matters | Routed to |
|---|---|---|
| Performance fee / carry, hurdle, catch-up | Largest possible unattributed drag | `Q-FEE-01` |
| Servicing fee; who retains origination points, late fees, default interest | GP economics outside the headline fee | `Q-FEE-01`, `Q-FEE-02` |
| Fund-level leverage | Tells you whether 9% is a levered or unlevered yield | `Q-RISK-06` |
| Basis of the default rate (annual vs cumulative; by count vs by dollar) and of the recovery rate (principal only or principal plus accrued interest; realized vs pending workouts) | Loss math swings ~4× between readings | `Q-RISK-05` |
| Workout timeline on defaulted loans | Time in foreclosure is cash drag even at 92% recovery | `Q-RISK-05` |
| LTV basis reconciliation: 68% as-is vs 72% ARV | ARV > as-is value, so LTV on ARV should normally be *lower*. The likely reason is different numerators: initial advance over as-is value vs total commitment (including rehab holdback) over ARV. Confirm it. 🟡 | `Q-RISK-04` |
| Grade mix contents (A–D shares) and default rate by grade | Shows how the book behaves in the bear case | `Q-RISK-05` |
| Fund term, redemption / lock-up terms | Lock-up length sets the illiquidity hurdle | `Q-LIQ-01` |
| Sponsor identity, GP co-invest, realized net-to-LP history | Alignment and track record (§7) | `Q-GP-01`, `Q-GP-02`, `Q-GP-03` |
| Minimum, fund size | Snapshot completeness | — |

## 7. GP Alignment

- **Co-invest: not stated.** 🔴 Unverified. It is not a fired `GEN-01`, but it is a must-ask.
- **Track record: partially verified.** 🟢 on credit metrics: a realized recovery rate through 2020 and 2022–23 is exactly the evidence `01` asks for ("sponsor history through a downturn"). That is stronger than most hard-money pitches. **Unverified** on LP outcome: the 9% is a *target*. No realized net-to-LP returns by vintage or year were given. Until those arrive, the LP-return record counts as unverified (`GEN-14`, `GEN-05` open).
- **Fee alignment: favorable where disclosed.** The step-down after the investment period is the LP-friendly structure. The carry design (hurdle, catch-up, high-water mark) is unknown.
- **Affiliate economics: unknown.** Servicing and origination points often flow to a GP affiliate. The test is disclosure and benchmarking (`GEN-06`).

## 8. Questions for the GP

**Must-ask**

| ID | Question (as tailored) | Bad-answer signal |
|---|---|---|
| `Q-FEE-01` (`GEN-16`) | "Provide the complete fee schedule: carry/performance fee and hurdle, servicing, admin, wind-down. Is 9% net of all of it?" | "Standard market fees"; a partial list; "the PPM has it" without producing the PPM. |
| `Q-FEE-02` (`GEN-06`) | "Who services the loans, and who keeps origination points, late fees, and default interest: the fund or a GP affiliate?" | "All arm's-length" without naming the providers; points or default interest flow to the GP undisclosed. |
| `Q-RISK-05` (`HML-03`, `HML-04`) | "Is 3.1% annual or cumulative, by count or by dollar? Is 92% recovery on principal only, realized, and what is the average workout timeline? Break it out for 2020 and 2022–23, by loan grade." | Default rate without recovery (or vice versa); "we've never had a loss"; vague on 2022–23. |
| `Q-RISK-04` (`HML-01`) | "Reconcile 68% as-is vs 72% ARV. What numerator does each use, and what is as-is LTV on the *total* commitment including holdbacks?" | Can't produce as-is LTV on the full commitment; "our borrowers always complete." |
| `Q-RISK-06` (`CREDIT-01`, escalated) | "Does the fund use a credit line or other leverage? What ratio, and is the 9% levered?" | Won't give a number; "leverage is conservative"; presents a levered yield as if unlevered. |
| `Q-GP-02` (`GEN-05`, `GEN-14`) | "Give realized net-to-LP returns by year or vintage, including 2020 and 2022–23." | Only the target, or gross loan yield; can't separate realized from marked. |
| `Q-GP-01` (`GEN-01`) | "How much GP capital is in the fund, on LP terms?" | "Our sweat equity is our investment"; a fee waiver in place of cash. |
| `Q-GP-03` (`GEN-02`) | "Any regulatory action, enforcement, or investor litigation?" | "Nothing material"; a search turns up something they did not disclose. |
| `Q-DIST-01` (`GEN-11`) | "What is the distribution cadence? Is there a reinvestment/DRIP option? When do distributions begin after funding?" | "We'll distribute when the book supports it"; no cadence stated. |
| `Q-LIQ-01` | "What is the fund term, and what are the redemption or early-exit options, gates, and penalties?" | "We'll try to accommodate"; lock-up terms not disclosed. |

**Nice-to-ask**

| ID | Question | Bad-answer signal |
|---|---|---|
| `Q-GP-04` (`GEN-04`) | "How have underwriting and asset-management headcount grown with AUM?" | AUM multiplied while the team stayed flat; no named workout lead. |
| `Q-DIST-02` | "Are there capital calls, and what happens on a missed call?" | "As needed," with no notice period. |
| `Q-LIQ-02` | "When are K-1s delivered?" | A history of extensions. |

Not asked, because the flags do not apply to a debt fund: `Q-DS-01`, `Q-DS-02` (no exit or cap-rate story at the loan level), `Q-EXIT-01`, `Q-EXIT-02`, `Q-RISK-01`, `Q-RISK-02`.

## 9. Diligence Checklist

- [ ] PPM and LPA: confirm the fee schedule, carry mechanics, step-down trigger, leverage limits, redemption terms, and where points and default interest go.
- [ ] Audited fund financials (multi-year): verify the default and recovery figures against the audited loss history, not marketing.
- [ ] Loan tape: grade mix, LTV per loan (as-is and ARV, same numerator), and state/metro exposure, to verify the 15% cap.
- [ ] Sample of defaulted-loan files from 2020 and 2022–23: foreclosure timeline, legal cost, recovery realized vs marked.
- [ ] Valuation process: who sets the as-is and ARV values (independent appraisal vs broker price opinion vs internal).
- [ ] Background check: SEC IAPD / Form ADV, FINRA BrokerCheck, state securities regulators, litigation search on the principals.
- [ ] Fund-level credit facility agreement, if any: covenants, and whether a lender margin call could force loan sales.
- [ ] Reference calls with existing LPs on distribution consistency through 2022–23.

## 10. Verdict

**Pursue.** 🟢 on the core story.

**Reasoning.** The essential hard-money disclosures in `01` are present:
- as-is and ARV LTV
- default rate
- recovery rate
- geographic mix
- history through 2020 and 2022–23

Every hard-money-specific flag (`HML-01` through `HML-05`) checks clean. The return is income, not exit or cap-rate driven. At 9% net it sits mid-range for the category and ≈417bps over HYG, clearing a ~300–400bps hurdle for a 3–5 year lock-up. The 32% as-is equity cushion, combined with a demonstrated 92% realized recovery, is the actual LP protection. It is disclosed rather than asserted. The two YELLOWs (`GEN-16`, `GEN-11`) are gaps in disclosure completeness. They are not structural defects.

**Biggest swing factor.** Loss severity in a true credit event. Defaults tripling with recovery falling to ~80% takes the net to ~7%, which is thin against the hurdle. The grade mix and the default-rate basis (annual vs cumulative) determine how close the book sits to that case.

**What would have to be true to commit:**
1. 9% is net of *all* fees, and total undisclosed GP economics (carry, servicing, points) are within `02` norms.
2. Fund-level leverage is zero or modest, and 9% is not a levered figure.
3. The 3.1% / 92% figures hold up on a dollar-weighted, realized basis in audited financials.
4. GP co-invests real cash, and the background check is clean.

**Suits:** an LP who wants income-oriented, short-duration, senior-secured real-estate credit, can accept a 3–5 year lock-up, and is using this fund as a diversifier against equity-RE holdings. It is not a growth allocation. The return is capped at the coupon, and the downside is credit loss.

**Would flip to Pass if:**
- undisclosed fees sit between a 12–13% gross and the 9% net with a no-hurdle carry;
- fund leverage exceeds a modest line; or
- the 3.1% default rate turns out to be annual by count while dollar-weighted losses run materially higher.
