# Balance Sheet Strength, Solvency and Cash Generation

Use this when: you are at Stage 4 and need to establish whether the company can survive what it owes, and whether the profit you validated upstream turns into cash the owners actually keep.

The income statement is an opinion assembled from estimates. The balance sheet tells you who has a prior claim on the business and in what order; the cash flow statement tells you whether the profit was ever real. Almost all permanent capital loss in equities traces to one of two failures — debt that could not be refinanced, or earnings that never became cash — and both are visible in these two statements long before the price reacts. Treat this file as one question in two halves: *what does it owe, and what does it generate to pay with?* As everywhere in this skill, no ratio below means anything until you have placed it against the sector norm and the company's own five-to-ten-year record.

## Contents

- [0. Sector gate — where this toolkit is undefined or inverted](#0-sector-gate--where-this-toolkit-is-undefined-or-inverted)
- [1. Build the economic debt figure before computing any ratio](#1-build-the-economic-debt-figure-before-computing-any-ratio)
- [2. Prove the cash is real](#2-prove-the-cash-is-real)
- [3. Leverage and capital structure](#3-leverage-and-capital-structure)
- [4. Maturity profile and refinancing risk](#4-maturity-profile-and-refinancing-risk)
- [5. Coverage: can it service what it owes](#5-coverage-can-it-service-what-it-owes)
- [6. Covenants and headroom](#6-covenants-and-headroom)
- [7. Liquidity ratios, facilities and runway](#7-liquidity-ratios-facilities-and-runway)
- [8. Working capital and the cash conversion cycle](#8-working-capital-and-the-cash-conversion-cycle)
- [9. Receivables and inventory quality](#9-receivables-and-inventory-quality)
- [10. Off-balance-sheet, contingent and quasi-debt obligations](#10-off-balance-sheet-contingent-and-quasi-debt-obligations)
- [11. Toxic and structured financing, chronic dilution](#11-toxic-and-structured-financing-chronic-dilution)
- [12. Goodwill, tangible book and asset productivity](#12-goodwill-tangible-book-and-asset-productivity)
- [13. Direction of travel, distress scores and credit-market signals](#13-direction-of-travel-distress-scores-and-credit-market-signals)
- [14. Does profit become cash? Accrual quality](#14-does-profit-become-cash-accrual-quality)
- [15. Free cash flow: define it before you use it](#15-free-cash-flow-define-it-before-you-use-it)
- [16. Maintenance versus growth capex](#16-maintenance-versus-growth-capex)
- [17. SBC and the FCF shareholders actually keep](#17-sbc-and-the-fcf-shareholders-actually-keep)
- [18. Sources and uses: who funded the growth, were the payouts earned](#18-sources-and-uses-who-funded-the-growth-were-the-payouts-earned)
- [19. Classification games and off-statement financing](#19-classification-games-and-off-statement-financing)
- [20. Cash taxes versus book taxes](#20-cash-taxes-versus-book-taxes)
- [21. Full-cycle durability and cash return on capital](#21-full-cycle-durability-and-cash-return-on-capital)
- [22. India versus US: conventions that break comparability](#22-india-versus-us-conventions-that-break-comparability)
- [Checklist](#checklist)

**Every range printed below is indicative only.** Bands shift with sector, market, rate cycle, accounting regime and period. Net debt/EBITDA of 3x is prudent for a contracted utility and reckless for a mid-cap capital-goods firm with a 200-day cash cycle. Peer comparison and the company's own history override any absolute band here. When you cite a band in output, cite it as a reference point and immediately state what the peer set actually does.

---

## 0. Sector gate — where this toolkit is undefined or inverted

Run this gate first. For several sectors the standard ratios below are not merely different, they are meaningless, and computing them produces confidently wrong conclusions.

| Sector | What breaks | Use instead |
|---|---|---|
| Banks (NSE/BSE and US) | Debt is raw material, not risk. Debt/equity of 8–12x is normal. Current ratio, CCC, working capital and FCF are undefined — deposits are funding, loans are assets | CET1 / CRAR, GNPA and NNPA, provision coverage, slippage and credit cost, CASA mix, LCR/NSFR, ALM bucket gaps, restructured book |
| NBFCs / HFCs (India) | Same as banks plus acute asset-liability risk; leverage *is* the business model | Tier-1 and CRAR, ALM mismatch in the ≤1-year bucket, borrowing mix (bank lines vs CP vs NCD vs securitisation), incremental cost of funds, Stage-3 assets, liquidity buffer |
| Insurers | No revenue-driven working capital; float is a liability that funds the asset book | Solvency ratio (IRDAI floor 1.5x), VNB and VNB margin, embedded value, persistency, combined ratio (general), reserve adequacy |
| REITs / InvITs / real-estate developers | High leverage is structural; depreciation is non-economic so EPS and FCF mislead; developer inventory is land and WIP, so DIO in the hundreds or thousands of days is by design | LTV against asset value (SEBI caps REIT/InvIT leverage), FFO and AFFO in place of FCF, WALE, interest cover; for developers net debt vs pre-sales collections and collections vs completion |
| Miners, E&P, heavy capex build-outs | FCF is negative by design during a build; net debt/EBITDA measured at a commodity peak understates leverage by a wide margin | Leverage at a mid-cycle price deck, reserve life and replacement, committed vs discretionary capex, cost-curve position, coverage at trough prices |
| Regulated utilities | High leverage is permitted and priced by the regulator | FFO/net debt, regulated asset base and allowed return, tariff and true-up mechanics, ring-fencing at the opco |
| Airlines, shipping, retail chains | Lease-adjusted debt dominates reported debt; negative working capital is a feature, not a warning | Lease-adjusted net debt/EBITDAR, fixed-charge cover, months of liquidity, fleet/vessel age, off-balance commitments |

If the company sits in one of these, stop, open the matching file in `references/sectors/`, and use this file only for the parts that survive: cash quality, contingent liabilities, related-party exposure, promoter pledge, distress signals.

---

## 1. Build the economic debt figure before computing any ratio

Headline "borrowings" understates what the company owes at almost every leveraged company. Compute an **adjusted net debt** first, then feed *that* into every leverage and coverage ratio below. Show the bridge in your output so a reader can disagree with one line rather than with the conclusion.

Start with gross borrowings (short-term + long-term + current maturities of long-term debt) and add:

- **Lease liabilities** (Ind-AS 116 / IFRS 16 / ASC 842). On balance sheet for lessees post-adoption, but confirm they are inside your debt figure and that EBITDA is on the same basis. US GAAP operating leases sit on the balance sheet yet keep rent inside operating expense, so an IFRS/Ind-AS retailer shows structurally higher EBITDA than a US GAAP peer with identical economics. See `14-accounting-comparability.md`.
- **Net pension / post-retirement deficit** (projected benefit obligation minus plan assets, plus OPEB). A senior, non-negotiable claim ranking ahead of equity.
- **India — gratuity and leave encashment (Ind-AS 19).** Frequently *unfunded*, or only partly funded through an LIC group policy. Read the employee-benefits note for the defined-benefit obligation, fair value of plan assets, funded status, discount rate (usually pegged to the G-sec curve), and the salary-escalation and attrition assumptions. An unfunded gratuity obligation in a labour-heavy business is real debt with no offsetting asset, and it grows with the wage bill.
- **Reverse factoring / supply-chain finance / channel financing** balances sitting inside trade payables. This is bank debt wearing a payables costume: reclassify it to debt and reverse the corresponding CFO benefit. US filers must disclose supplier-finance programme obligations and a rollforward (ASU 2022-04); IFRS and Ind-AS filers disclose carrying amounts and terms under the IAS 7 / IFRS 7 amendments. If the programme exists and the disclosure is thin, that is itself a finding.
- **Securitised or factored receivables sold with recourse.** Off the balance sheet, still your credit risk. India: "bills discounted with recourse" is normally disclosed under contingent liabilities rather than debt.
- **Financial guarantees given** — to subsidiaries, JVs, associates, and in India critically to promoter-group entities. Probability-weight them, but never at zero: a guarantee to a weaker group company is a call option written against your equity.
- **Written puts over minority interests (NCI puts).** Common in Indian group structures and in partially acquired subsidiaries — the parent has contracted to buy out a minority at a formula price or on a fixed date. It is a dated cash obligation with debt-like seniority, often disclosed only in the financial-instruments note.
- **Preference shares, perpetual and hybrid instruments, compulsorily convertible instruments, PIK and toggle notes.** Classify by economics, not label: anything with mandatory redemption or a cash coupon that cannot be deferred without consequence is debt. PIK and toggle notes flatter coverage while compounding principal.
- **Customer advances and deferred revenue are *not* debt** — they are interest-free funding and a sign of strength — but note them separately so the reader sees why net debt is low.

Then subtract cash, but only cash genuinely available. Deduct restricted cash, margin money and deposits pledged against letters of credit or guarantees, cash trapped in subsidiaries that cannot upstream it (minority-held or capital-controlled), and cash at consolidated entities the parent cannot reach. **Do not net cash you have not proved (§2).**

Finally, note **structural subordination**: where does the debt sit? A thin listed holdco servicing debt out of dividends from operating subsidiaries that have their own lenders is far riskier than the consolidated ratio implies. This applies to Indian promoter holdcos and US parent/opco structures alike — see `references/sectors/holdco-assetmgr.md`.

---

## 2. Prove the cash is real

Every leverage ratio that nets cash is only as good as the cash. This is the highest-severity test in the file, because fake or encumbered cash is the defining feature of the largest accounting frauds of the last three decades — and the standard ratio toolkit quietly assumes the cash line is true.

Run the **interest-income reconciliation**: implied yield = interest and investment income ÷ average cash and short-term investments. Compare it against prevailing deposit and money-market rates for that currency and period (India: bank FD and liquid-fund yields; US: T-bill and money-market yields). A large cash pile earning implausibly little is cash that is fake, pledged, restricted, parked non-interest-bearing at a related-party bank, or simply not there.

Then ask the structural questions:

- **Why does it carry large gross cash and large gross debt at the same time?** There are legitimate answers — regulatory requirements, working-capital seasonality, prefunding a maturity, jurisdictional trapping. There is also one very common illegitimate answer. Make management's explanation explicit and test it against the arithmetic: if the company pays 9% on debt while earning 3% on cash, the negative carry must appear in the P&L and must be justified by something.
- **Where is it held?** Small, obscure, offshore or related-party banks are a flag; so is concentration in a single unrated institution.
- **Is it pledged?** India: check CARO, the margin-money and "deposits with maturity over 12 months" split in the cash note, and charges filed with the MCA/ROC. US: the debt footnote and the restricted-cash reconciliation required under ASU 2016-18.
- **India-specific corroboration.** CARO 2020 requires the auditor to report on short-term funds applied to long-term purposes, loans and advances to related parties, whether the company is a declared wilful defaulter, and diversion of funds. It is the cheapest forensic evidence available on an Indian filer. Also check rating actions — a CRISIL/ICRA/CARE rating moved to "Issuer Not Cooperating" is a serious signal, as is any SEBI-mandated disclosure of default to the exchanges.
- **US-specific corroboration.** Item 9A internal-control conclusions and any disclosed material weakness in treasury or cash; auditor changes and dismissals (8-K Item 4.01); going-concern language under ASC 205-40.

If the cash cannot be corroborated, run every ratio on **gross** debt as well as net, and lead with the gross figure. State that you did and why.

---

## 3. Leverage and capital structure

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Net debt / EBITDA | Adjusted net debt (§1) ÷ trailing EBITDA; use mid-cycle EBITDA for cyclicals | <2x comfortable; 2–3x manageable; >4–5x stretched outside utilities, REITs and infra | The single most-watched gauge by lenders and rating agencies; it sets refinancing terms |
| Gross debt / EBITDA | Same, without netting cash | Within ~0.5–1x of net for a normally financed firm | Exposes leverage masked by cash that is restricted, trapped or unproven |
| Debt / equity | Adjusted debt ÷ shareholders' funds (India: net worth — watch revaluation reserves) | 0–1x for most non-financials; sector-bound | Shows how much of the asset base creditors funded; the classic Indian screening ratio |
| Debt / total capital | Debt ÷ (debt + equity) | <50% typical for non-financials | Less distorted than D/E when equity is small, negative or buyback-depleted |
| Net debt / (EBITDA − capex) | Uses the cash left after sustaining spend | Materially higher than net debt/EBITDA in capital-heavy names | Capital-intensive firms cannot service debt out of EBITDA they are obliged to reinvest |
| Net debt / FCF (years) | Adjusted net debt ÷ FCF | <4–5 years comfortable for a stable business | Answers "how long to repay out of real cash" without EBITDA's fictions |
| Tangible net worth test | Equity − goodwill − intangibles | Positive | Negative tangible net worth, whether from goodwill or buybacks, can trip net-worth covenants |

**How to read it.** Leverage magnifies both outcomes: a moderately geared firm survives a downturn, an over-geared one is forced into distressed asset sales, dilutive rescue equity or restructuring exactly when conditions are worst. Two refinements change conclusions more often than the level does. First, compute leverage on **mid-cycle** EBITDA for anything cyclical — leverage measured at a commodity, property or freight-rate peak is a trap. Second, ask *why* leverage moved: debt raised to fund capacity that will earn a return is a different signal from debt raised to fund buybacks, dividends or acquisitions, even at an identical ratio.

**Red flags:** net debt/EBITDA rising while EBITDA is flat or falling; D/E far above the peer set with no structural reason; leverage that only looks acceptable after netting unproven cash; management quoting leverage on credit-agreement "adjusted EBITDA" rather than reported EBITDA.

---

## 4. Maturity profile and refinancing risk

A solvent company can still fail if it cannot refinance. This is a *timing* risk independent of profitability, and it is where otherwise healthy businesses die.

Pull the maturity ladder. **US:** the long-term debt footnote and the credit agreements filed as exhibits — the old contractual-obligations table was dropped from Item 7, so do not look for it there. **India:** the borrowings note, the repayment-terms schedule, and the Ind-AS 107 liquidity-risk maturity table in the financial-instruments note.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Near-term maturity cover | (Cash + undrawn committed facilities + 12m projected FCF) ÷ debt due within 12–24 months | >1.5x | Below 1x the company must access markets to survive, on the market's terms |
| Short-term debt share | (Current borrowings + current maturities) ÷ total debt | <25–30% for a non-financial | Short-dated funding of long-dated assets is the classic liability mismatch |
| Weighted-average maturity | Σ(principal × years to maturity) ÷ total principal | >3–4 years for an investment-grade-type profile | Longer tenor buys time through a closed funding window |
| Maturity-wall test | Largest single-year maturity ÷ annual FCF | <2–3x | Identifies the specific year that decides the equity |
| CP / revolver dependence | Commercial paper + revolver drawings ÷ total debt | Low and stable | CP markets shut fastest and with no warning; rollover is not a right |
| Refinancing gap | Weighted-average existing coupon vs current new-issue yield for that rating and tenor | Small | A wide gap is an interest-cost step-up that today's P&L does not show |

**Structure matters as much as size.** Split the book by fixed vs floating (and how much floating is hedged), by currency (is FX debt matched by FX revenue or a natural hedge, or would a currency move be a solvency event?), and by secured vs unsecured/subordinated (how much of the asset base is already pledged — if most assets are encumbered there is no collateral left to raise against, and unsecured creditors and equity are structurally subordinated). India: check the charge register, promoter guarantees on company debt, and short-tenor FX exposure via buyer's credit and packing credit.

**Red flags:** a maturity wall inside 12–24 months exceeding available liquidity; continuous CP rollover funding long-life assets; unhedged floating exposure into a tightening cycle; FX debt at a business with no FX revenue; an average coupon far below current market.

---

## 5. Coverage: can it service what it owes

Leverage sizes the obligation; coverage tells you whether the business generates enough to carry it. Compute both earnings-based and cash-based coverage — the gap between them is itself the finding.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Interest coverage (TIE) | EBIT ÷ interest expense | >4x comfortable; 2–3x fragile; <1.5x distressed | The standard first screen; below ~2x a modest earnings dip breaches covenants |
| EBITDA / interest | EBITDA ÷ interest expense | >4–6x | Useful for capital-heavy firms, but ignores the capex they are obliged to fund |
| (EBITDA − capex) / interest | Strips sustaining investment before testing coverage | >2x | The honest version for asset-heavy businesses |
| Cash interest coverage | CFO before interest ÷ cash interest paid | >3x | Cash pays interest; accounting EBIT does not |
| Fixed-charge coverage | (EBIT + lease expense) ÷ (interest + lease expense + preference dividends) | >1.5–2x | The only fair measure where leases and preferreds are large — retail, airlines, shipping |
| DSCR | (CFO − capex) ÷ (interest + mandatory principal amortisation) | >1.2–1.5x | What project lenders and Indian banks actually test; India: Schedule III requires DSCR in the ratios note |
| FCF / total debt | FCF ÷ adjusted gross debt | >15–20% is strong | The deleveraging speed the equity story is implicitly relying on |

**Always stress-test.** Recompute coverage under (a) a 20–30% fall in CFO and (b) the floating book repricing to current market plus the refinancing gap from §4. Coverage that survives only in a peak year is not coverage. Watch for capitalised interest flattering reported interest expense, and for covenants written on an adjusted EBITDA that bears little relation to cash.

---

## 6. Covenants and headroom

Covenants are the tripwires between distress and default. A company can be paying every bill on time and still lose control of its own restructuring.

Where to read them. **US:** credit agreements and indentures filed as exhibits on EDGAR; amendments and waivers appear as 8-K Item 1.01, acceleration as Item 2.04. EDGAR full-text search for phrases like "Consolidated Leverage Ratio" or "Fixed Charge Coverage Ratio" inside the filer's exhibits works well. **India:** the borrowings note and terms-and-conditions disclosure, the sanction terms summarised in the annual report, any disclosure of breach or waiver, and the mandatory disclosure of payment default to the exchanges.

What to compute and watch:

- **Headroom %** on each maintenance covenant: (limit − current metric) ÷ limit, plus the EBITDA decline that would breach it. Headroom under ~15–20%, or an EBITDA cushion under ~20%, means one weak quarter hands the keys to lenders.
- **Which EBITDA definition the covenant uses.** Credit-agreement EBITDA typically permits add-backs — run-rate synergies, "exceptional" items, pro-forma acquisition contributions — that reported EBITDA does not. Comfortable covenant headroom alongside poor reported cash conversion tells you the covenant is not binding on reality.
- **Springing covenants** that apply only above a revolver-utilisation threshold. They bite precisely when the revolver is being drawn, i.e. in stress.
- **Cross-default and cross-acceleration chains**, change-of-control puts, material-adverse-change clauses, and rating-linked triggers (coupon step-ups, collateral posting).
- **Waiver and amendment history.** Repeated waivers are not a technicality — they are a disclosed loss of negotiating position, and they usually arrive with higher pricing, new security, and restrictions on dividends and capex.
- **Covenant-lite is not safety.** It removes the early warning and defers the reckoning to the maturity wall.

---

## 7. Liquidity ratios, facilities and runway

Ratios are a screen; **absolute accessible liquidity** decides whether a shock is survived.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Current ratio | Current assets ÷ current liabilities | >1.2–1.5 for industrials; retailers and QSR legitimately run below 1 | First-order near-term payment risk; India: Schedule III requires disclosure with an explanation of any >25% YoY change |
| Quick (acid-test) ratio | (Current assets − inventory − prepaids) ÷ current liabilities | ~1 | Strips the least liquid and most over-stated current asset |
| Cash ratio | (Cash + marketable securities) ÷ current liabilities | 0.2–0.5 typical, sector-bound | The worst-case view; immune to receivable and inventory optimism |
| Total available liquidity | Unrestricted cash + undrawn **committed** facilities | ≥12 months of fixed obligations plus committed capex | Absolute rupees or dollars, not ratios, determine survival |
| Revolver utilisation | Drawn ÷ total facility | Low; a fully drawn revolver means the backstop is spent | Heavy drawing is a late-stage distress signal |
| Cash runway (loss-makers) | Unrestricted cash ÷ average quarterly burn | >18–24 months, or a fully funded plan | Runway dictates the timing and price of the next dilution |
| Defensive interval | Liquid assets ÷ daily operating cash expenses | >90 days | Days of survival assuming zero receipts |

Check whether facilities are **committed** (a genuine backstop) or **uncommitted / repayable on demand**. India: most working-capital cash-credit and overdraft limits are repayable on demand and reviewed annually — do not count them as committed liquidity, and watch the drawing power fall when the receivable and inventory base securing them deteriorates. Check facility expiry against the maturity ladder: a revolver expiring before the bond it is meant to backstop is not a backstop.

**Red flags:** current ratio below 1 in a business that does not collect before it pays; liquidity ratios that look adequate only because of slow-moving inventory or doubtful receivables; a large share of "cash" restricted, pledged or trapped; runway under ~12 months with equity markets closed; going-concern emphasis in the audit report.

---

## 8. Working capital and the cash conversion cycle

Working capital is usually the single largest reason profit and cash diverge, and the cheapest place to detect deterioration early.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| DSO | Trade receivables ÷ revenue × 365, on average balances | Sector-bound: FMCG 10–30d, IT services 60–80d, EPC and infra 120d+ | Rising DSO is the earliest sign of channel stuffing, weakening customers or aggressive recognition |
| DIO | Inventory ÷ COGS × 365 | Sector-bound; developers, distillers and jewellery run in years by design | Inventory built ahead of demand precedes write-downs |
| DPO | Trade payables ÷ COGS × 365 | Stable is good; sharply rising is not | Rising DPO flatters CFO by borrowing from suppliers |
| Cash conversion cycle | DSO + DIO − DPO | Negative is a genuine advantage (retail, marketplaces, subscriptions) | How many days of sales must be funded before cash comes back |
| ΔWorking capital / ΔRevenue | Change in net working capital ÷ change in revenue | <15–20% for a capital-light grower | Tells you whether growth consumes or releases cash |
| Working capital / sales | Net working capital ÷ revenue | Flat or falling | The scaling law of the business model |

**Method discipline.** Use average balances, not year-end snapshots, and correct for seasonality — a March-year-end Indian manufacturer and a December-year-end US peer are not measured at the same point in their cycle. Put peers on the same revenue basis (gross vs net of indirect taxes) before comparing days.

**Distinguish a real improvement from a financed one.** A CCC that improves because DPO jumped is supplier financing. A CCC that improves because receivables were factored or securitised is a balance-sheet transaction, not an operating gain. Both reverse, and both strain the counterparty who is funding them. India: Schedule III now mandates **ageing schedules for trade receivables and trade payables** (and for CWIP and intangibles under development) — read them, because a growing over-6-month or over-3-year receivable bucket contradicts a clean-looking headline DSO.

---

## 9. Receivables and inventory quality

These two assets carry the balance sheet's most optimistic estimates, and they inflate the current and quick ratios while doing it.

Checks that change conclusions:

- **Receivables growth vs revenue growth** over 8–12 quarters. Persistent divergence means sales are being recognised faster than they are collected. Cross-reference §14 and `07-forensic-red-flags.md`.
- **Allowance for doubtful accounts ÷ gross receivables, and its trend.** A shrinking allowance into a weakening economy is a quiet earnings source. India: read the Ind-AS 109 expected-credit-loss provision matrix against the ageing buckets. US: the CECL disclosure and the valuation-allowance rollforward.
- **Concentration.** A large receivable from one customer, one government body or a related party is a different asset from a diversified book. In Indian EPC, defence and infrastructure, dues from government and PSU customers are often collectible but with multi-year timing — model the *timing*, not just the loss.
- **Related-party and subsidiary receivables that keep growing and never settle.** A classic tunnelling route; treat a rising, unexplained related-party advance as capital leaving the company.
- **Quarter-end receivable spikes** that reverse in the following quarter — pull-forward of sales into the reporting period.
- **Inventory mix and reserves:** finished goods building faster than sales means sell-through is failing rather than purchasing being early; check the obsolescence-reserve trend and write-down history. For US filers, the LIFO reserve understates carrying value and raises cost of sales relative to FIFO peers — adjust before comparing.
- **Vendor and customer financing.** If the company lends to, guarantees the debt of, or grants unusually long credit to its own customers or distributors to enable purchases, reported growth is partly manufactured credit risk. Track notes receivable, long-dated receivables and customer guarantees against revenue growth. Historically this pattern has ended violently in telecom equipment, solar and EV supply chains — it reads as clean organic growth right up until the receivables sour.

---

## 10. Off-balance-sheet, contingent and quasi-debt obligations

Everything here is a real economic obligation that can convert into cash and lift true leverage well above the reported figure. Go to the notes; the face of the balance sheet will not tell you.

| Item | Where to find it | What it does to your numbers |
|---|---|---|
| Reverse factoring / supply-chain finance / channel financing | US: ASU 2022-04 supplier-finance disclosure and rollforward. IFRS/Ind-AS: IAS 7 and IFRS 7 amendments; also the payables note and concall Q&A | Reclassify to debt and reverse the CFO benefit. Debt disguised as trade payables has preceded sudden collapses in construction and supply-chain-finance-dependent names |
| Receivables securitisation, factoring or bill discounting **with recourse** | Financial-instruments note; India — contingent-liabilities note | Gross up receivables and debt; the credit risk never left the company |
| Financial guarantees (subsidiaries, JVs, associates, promoter entities) | Contingent-liabilities note; related-party schedule | Add probability-weighted. A guarantee to a weaker group entity is equity risk written for free |
| Written puts over NCI / minority buyout obligations | Financial-instruments note; shareholder agreements | A dated cash obligation with debt-like seniority, usually invisible in the headline leverage ratio |
| Take-or-pay, purchase and capex commitments | Commitments note | Fixed future outflows; treat as quasi-debt in any downside scenario |
| Pension and OPEB deficit; India — gratuity and leave encashment | Employee-benefits note (Ind-AS 19 / ASC 715) | Add the net deficit to debt; test sensitivity to a 1% discount-rate move and check the expected-return assumption is not flattering the funded status |
| Litigation, tax, environmental and warranty exposures | Contingent liabilities; US Item 3 and the loss-contingency note | India — "contingent liabilities not provided for" is often dominated by **disputed tax demands** (GST, excise, service tax, income tax). Assess litigation stage and the company's historical win rate rather than adding the gross number |
| VIEs, SPEs and structured entities | Consolidation note | Ask what was moved off balance sheet, and why |
| India — promoter share pledge | Quarterly shareholding pattern; encumbrance disclosures | Not a company liability, but a forced-selling overhang and a tunnelling motive. Pledge above ~25–50% of the promoter stake, or rising into a falling price, is a serious governance-plus-liquidity flag — see `07-forensic-red-flags.md` |

Present the material items as a sensitivity: reported net debt/EBITDA, then the same ratio with quasi-debt included. Where the two tell different stories, that difference *is* your conclusion.

---

## 11. Toxic and structured financing, chronic dilution

Mostly a small- and micro-cap issue, and it deserves a separate check because it can guarantee a falling share price *regardless of operating performance*.

Look for:

- **Variable- or reset-conversion convertibles** ("death-spiral" notes) where the conversion price floats down with the market price. Falling price produces more shares, which produces more selling, which produces a falling price. The instrument is a machine for transferring value away from existing holders.
- **At-the-market (ATM) equity programmes** used continuously to fund operating losses. Quantify the shares issuable under the live shelf at the current price and at a price 50% lower.
- **PIPEs with warrant coverage**, repriceable warrants, and toggle/PIK notes that defer cash cost into principal.
- **India:** preferential allotments and warrants to promoters or related parties priced near the SEBI floor, repeated QIPs whose proceeds fund interest rather than growth, and convertibles issued to group entities. Build the 7–10 year share-count history: chronic dilution while the narrative is "growth" is the tell.

Compute **potential dilution at a stressed price**, not merely today's diluted count, and restate the thesis per share. A company can triple revenue and still halve the value of your claim.

---

## 12. Goodwill, tangible book and asset productivity

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| (Goodwill + intangibles) / total assets | Balance sheet | Low for organic compounders; high for serial acquirers by construction | Sizes how much of the asset base is a price paid rather than a thing owned |
| Goodwill / equity | Above 100% means negative tangible book | <50% preferred outside roll-ups | A single impairment can erase reported net worth and trip net-worth covenants |
| Tangible book value | Equity − goodwill − intangibles (− revaluation reserves) | Positive | The creditor's view of what actually backs the debt |
| Capex / depreciation | Capex ÷ D&A, 5-year average | ~1.0 sustaining; >1 expanding | Sustained below 1 is harvesting the asset base — borrowing FCF from the future |
| Accumulated depreciation / gross PP&E | Fixed-asset schedule | <60–70% | Asset-age proxy; a near-fully-depreciated base means a replacement cycle is coming |
| Asset turnover and fixed-asset turnover | Revenue ÷ total (or net fixed) assets | Stable or rising vs peers | Links the balance sheet to the earnings that repay creditors; feeds DuPont in `05-returns-and-dupont.md` |

Read the impairment-test assumptions — terminal growth rate, discount rate, disclosed headroom. Optimistic assumptions defer inevitable write-downs. A serial acquirer carrying unimpaired goodwill over underperforming acquired segments is running a deferred loss. Impairments are non-cash, but they are an admission, and more usefully a dated record of capital-allocation quality. India: watch **CWIP** and "intangible assets under development" sitting unmoved for years in the Schedule III ageing table — a project that never gets commissioned is an impairment waiting to be taken.

---

## 13. Direction of travel, distress scores and credit-market signals

Trajectory usually matters more than level. Plot five years of adjusted net debt/EBITDA, D/E and interest cover on one view, then *attribute* the change: organic paydown, EBITDA recovery, debt-funded buybacks, debt-funded M&A, working-capital release, or asset sales. Deleveraging by selling the best assets is not deleveraging.

Corroborate with composites and with markets:

- **Altman Z-score** (below ~1.8 is the distress zone for manufacturers; use the Z" variant for non-manufacturers and emerging markets; undefined for financials), **Piotroski F-score** (0–9 fundamental momentum), **Beneish M-score** (manipulation likelihood). These are triage that directs attention, never verdicts — say so when you report them.
- **Credit ratings and outlook** — investment grade vs high yield, negative watch, and especially the crossover to junk, which forces index selling. India: CRISIL, ICRA, CARE and India Ratings rationales are detailed, free, and frequently more candid than the annual report.
- **Bond prices vs par, yield-to-maturity vs the sovereign curve, CDS spreads.** Credit markets aggregate professional lenders' real-time judgement and routinely anticipate equity trouble by quarters. When the bonds trade at distressed levels while the equity is priced for growth, one of the two markets is wrong, and it is rarely the bond market.
- **India-specific stress tells:** rating moved to "Issuer Not Cooperating", disclosure of payment default to the exchanges, insolvency petitions filed at the NCLT by operational creditors, auditor or CFO resignation coinciding with a funding squeeze, and a rising promoter pledge into a falling price.

---

## 14. Does profit become cash? Accrual quality

The highest-yield single test in fundamental analysis. Earnings are an opinion; cash is a fact.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| CFO / net income | Cumulative over 3–5 years, never one year | ~1.0 or above cumulatively | A durable business converts essentially all accounting profit into cash over a cycle |
| CFO / EBITDA | Cash conversion before capex | 70–90%+ for asset-light; structurally lower where working capital is heavy | Isolates working-capital and cash-tax leakage from the capex question |
| Sloan accrual ratio | (Net income − CFO) ÷ average total assets | Low; above ~10% is a flag | High-accrual firms systematically underperform — one of the most robust anomalies in the literature |
| Balance-sheet accruals | Δ(non-cash working capital + net non-current operating assets) ÷ average total assets | Low and stable | Catches accruals that bypass the cash-flow-statement bridge |
| Non-cash add-back share | (D&A + SBC + impairments) ÷ the NI-to-CFO bridge | Understand the mix | A CFO held up entirely by add-backs is not the same as one held up by collections |

**How to run it.** Bridge net income to CFO line by line for each of the last five years and label every line as (a) genuinely non-cash and recurring, (b) non-cash and one-off, or (c) working capital. Then ask the diagnostic question: is the gap explained by depreciation on a real asset base, or by receivables and inventory? A company reporting record earnings while continually borrowing has already answered it.

Never conclude from a single year. Working-capital swings, one-off settlements and acquisition timing distort one year and wash out over three to five.

---

## 15. Free cash flow: define it before you use it

There is no single FCF. State the definition, apply it identically across the peer set, and show the bridge.

| Variant | Definition | Use it for |
|---|---|---|
| Simple FCF | CFO − capex | The default; comparable across most non-financials |
| Levered FCF (FCFE) | CFO − capex − mandatory debt amortisation (interest already inside CFO under US GAAP) | What is genuinely available to equity after the lenders are served |
| Unlevered FCF (FCFF) | NOPAT + D&A − capex − ΔWC | DCF inputs; independent of capital structure |
| FCF after leases | Subtract lease principal repayments, which IFRS 16 / Ind-AS 116 route to financing | Restoring comparability for retailers, airlines and hotels |
| SBC-adjusted FCF | FCF − stock-based compensation | Tech and growth names (§17) |
| Owner earnings | Net income + D&A − maintenance capex − required working-capital investment | The economic version; requires a maintenance-capex estimate (§16) |

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| FCF margin | FCF ÷ revenue | 5–10% solid for industrials; 20%+ for mature software; near zero or negative is normal mid-build for infra and miners | The clearest single measure of how much of a rupee of sales the owner keeps |
| FCF / net income | Cash conversion of earnings | ~0.8–1.0+ over a cycle | Combines accrual quality and capital intensity into one number |
| FCF / EBITDA | Conversion after capex, cash tax, interest and working capital | >50% for asset-light; structurally lower for asset-heavy | Exposes the gap between the EBITDA management guides on and the cash that arrives |
| FCF yield | FCF ÷ market cap (equity) or ÷ enterprise value (unlevered) | Compare to the risk-free rate and to peers | The bridge into valuation — see `06-valuation.md` |

Build the **EBITDA-to-FCF bridge** explicitly — cash interest, cash tax, ΔWC, capex, lease principal — each as a percentage of EBITDA. It tells you *where* the cash leaks and whether the leak is structural or fixable. Two firms with identical EBITDA can produce wildly different FCF, and the bridge is the entire explanation.

**Red flags:** FCF positive only after cutting essential capex; FCF reached with asset sales, tax refunds or insurance proceeds sitting inside the operating section; FCF margin falling while revenue grows (growth that never reaches the owner); positive trailing FCF with negative FCF across the preceding cycle.

---

## 16. Maintenance versus growth capex

Only growth capex is discretionary. Maintenance capex is a permanent claim on cash, and mislabelling it is the easiest way to inflate normalised FCF and return on capital simultaneously.

Estimate maintenance capex independently rather than accepting management's split:

- **D&A-anchored:** take current D&A and adjust upward for inflation since the assets were purchased and for unit growth. Crude, but hard to game.
- **Greenwald method:** compute the historical ratio of gross PP&E to sales, multiply by the current year's *increase* in sales to get growth capex, and treat the remainder of total capex as maintenance.
- **Physical cross-check:** if capex was mostly "growth", capacity or output should have risen. Indian filers routinely disclose installed capacity and utilisation; miners disclose tonnage; utilities disclose MW; telcos disclose sites. Spend that rose without capacity rising was not growth capex.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Capex / revenue | Capex ÷ revenue, 5-year average | 1–3% asset-light; 5–15% manufacturing; 20%+ telecom, utilities, miners | Sets the structural ceiling on FCF margin |
| Capex / D&A | 5-year average | ~1.0 sustaining | Below 1 for several years means the asset base is being harvested |
| Maintenance capex / total capex | From the estimate above | A falling share signals genuine expansion | Determines normalised FCF and owner earnings |
| Incremental capital efficiency | Growth capex ÷ incremental revenue (or incremental EBITDA) | Improving | Tests whether expansion earns its cost of capital before it shows up in ROIC |
| CWIP / gross block (India) | Capital work-in-progress ÷ gross block, read with the ageing schedule | Low and turning over | Large static CWIP is capital deployed but not earning — or an impairment in waiting |

**Red flags:** capex far below D&A for years while margins hold (deferred maintenance flattering today's FCF at tomorrow's expense); capex spiking with no capacity or revenue response; reclassification of maintenance as growth to promote an "adjusted FCF"; recurring operating costs capitalised as software, development, content or cloud migration — see §19 and `03-earnings-quality.md`.

---

## 17. SBC and the FCF shareholders actually keep

Stock-based compensation is a genuine economic cost borne by shareholders through dilution, yet it is added back as non-cash and inflates both CFO and FCF. For a growth-tech name it is frequently the difference between an attractive and an unattractive FCF yield.

Compute and report: SBC ÷ revenue; SBC ÷ CFO; SBC ÷ FCF; **FCF less SBC**; annual diluted share-count growth; and buybacks *net* of issuance. The decisive question is whether repurchases genuinely shrink the share count or merely mop up option and RSU issuance. If the count is flat while the company reports large buybacks, that "capital return" is deferred cash compensation and belongs as a deduction from FCF, not as a shareholder distribution.

India: ESOP pools are generally smaller outside IT services and recently listed new-age companies, but read the ESOP note, the discount to fair value at grant, and pool refreshes. For recent Indian tech listings, SBC and the associated share-count growth can be large enough to invert the FCF conclusion entirely.

**Red flags:** SBC a large and rising share of CFO; share count rising despite buybacks; management promoting an adjusted FCF that treats SBC as free; option repricing or accelerated grants after a price fall.

---

## 18. Sources and uses: who funded the growth, were the payouts earned

Build one cumulative five-year table. Sources: cumulative CFO, debt drawn, equity issued, asset sales. Uses: capex, acquisitions, dividends, buybacks, debt repaid, lease principal. Reconcile to the change in net debt and in share count. This single view answers more questions than any ratio in this file.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Self-funding ratio | Cumulative FCF ÷ cumulative (capex + M&A + distributions) | ≥1.0 | Self-funded growth compounds without dilution or balance-sheet risk |
| FCF payout ratio | (Dividends + gross buybacks) ÷ FCF | <70–80% sustained | Sustained above 100% erodes the balance sheet and ends in a cut |
| Cash dividend cover | FCF ÷ dividends paid | >1.5x | An accounting payout ratio can look safe while the dividend is being borrowed |
| Reinvestment rate | (Capex + M&A + ΔWC) ÷ CFO | Only as high as the return earned justifies | Heavy reinvestment is good only when the incremental return exceeds the cost of capital |
| Net financing flow | Debt drawn − repaid + equity issued − buybacks, over 5 years | Net outflow for a mature franchise | A chronic net *inflow* means the business is capital-markets dependent |
| Share count trend | Diluted shares over 7–10 years | Flat or falling | The per-share claim is the thing you actually own |

Growth funded repeatedly by new debt or equity is fragile: it depends on open capital markets and reverses violently when they shut. That distinction — self-funded compounder versus capital-markets-dependent story — separates two businesses with identical reported growth rates. India: check whether QIPs and preferential allotments funded expansion or funded interest, who subscribed (public versus promoter and related parties), and at what discount.

Buyback quality matters too. Repurchases executed at depressed valuations that permanently reduce the count create value; repurchases at peak multiples funded with debt destroy it while flattering EPS. And a high, "safe-looking" dividend yield is usually the market's warning about coverage rather than a gift.

---

## 19. Classification games and off-statement financing

The section boundaries of the cash-flow statement are a favoured manipulation surface precisely because they attract less scrutiny than the P&L. Moving recurring outflows out of operating, or pulling one-off inflows in, makes cash generation look structurally stronger than it is.

Check for:

- **Receivables factoring or securitisation** inflating CFO in the year the programme starts. The step-up is one-time; the run-rate is not. Compare the change in factored balances year over year from the footnote.
- **Reverse factoring** turning a payables outflow into a financing outflow — or worse, staying inside payables and never appearing as debt at all (§10).
- **Capitalised costs** — software development, development-phase R&D (Ind-AS 38 permits capitalisation; US GAAP is stricter), content, cloud implementation — moving cash from operating to investing. Track capitalised spend as a share of total spend, and its trend.
- **Lease classification.** Under IFRS 16 / Ind-AS 116 the lease principal sits in financing, so CFO is structurally higher than under a US GAAP operating lease. Never compare CFO or CFO/EBITDA across the two regimes unadjusted.
- **Interest and dividend classification.** Under Ind-AS/IFRS, interest paid may be presented in operating *or* financing, and dividends received in operating or investing. Most Indian corporates place interest paid in financing, which makes Indian CFO a **pre-interest** number; US GAAP forces interest paid into operating. Comparing an Indian CFO/EBITDA with a US one without normalising flatters the Indian company, sometimes substantially.
- **One-offs dressed as operating cash:** asset-sale proceeds, litigation and insurance settlements, large tax refunds, government incentive receipts. Compute one-offs as a percentage of CFO.
- **Gross versus net capex** presentation, and disposal proceeds netted against capex to flatter FCF.
- **Opaque "other operating" lines** that are large, volatile and unexplained.
- **Year-end window dressing:** payables settled just after year-end, receivables collected just before, inventory shipped to distributors on quarter-end terms. Where quarterly balance-sheet data exists, compare the year-end balance to the average of the four quarter-ends.

---

## 20. Cash taxes versus book taxes

A low cash tax rate can lift current FCF materially — and most of the drivers expire.

Compute the **cash tax rate** = cash taxes paid ÷ pre-tax income, and set it against the effective book rate and the statutory rate. Explain every gap: accelerated depreciation, loss carryforwards, tax credits, jurisdiction mix, holidays and incentives. Then estimate the **sustainable** rate once timing differences reverse and carryforwards are exhausted, and use that rate in any forward FCF or DCF. Investors who capitalise an artificially low cash tax rate overpay by construction.

India specifics: the concessional 22% regime under s.115BAA (and 15% for qualifying new manufacturing under s.115BAB) versus the older rate; MAT credit utilisation and expiry; SEZ and unit-based deductions winding down; area-based incentives. A company still riding MAT credit or an expiring SEZ benefit has a cash-tax step-up coming that no historical ratio will reveal.

**Red flags:** a large unexplained cash-versus-book gap; FCF flattered by carryforwards about to run out; a growing deferred tax liability that will reverse into cash outflows; guidance that projects today's cash tax rate indefinitely.

---

## 21. Full-cycle durability and cash return on capital

Two companies with identical trailing FCF can carry entirely different risk. Assess durability before you capitalise anything.

- Pull CFO and FCF through the **last downturn** for that sector — 2008–09, 2013 (India: taper and current-account stress), 2015–16 (commodities), 2020, plus any industry-specific bust. If the history does not go back that far, say so and treat durability as unproven rather than assuming it.
- Compute **FCF margin volatility** (standard deviation across the cycle) and the trough-to-peak FCF ratio.
- Establish the **recurring share** of cash flow: contracted, subscription or annuity revenue versus transactional and project-based; customer and end-market concentration; commodity linkage. Recurring cash flow deserves a higher multiple because it is more predictable and more self-funding.
- Set a **mid-cycle normalised FCF** and use that in valuation. Capitalising peak-cycle FCF is the most common valuation error in cyclicals, and it is usually compounded by the fact that leverage also looks fine at the peak.

Then close the loop from cash to value creation:

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| CROIC | FCF ÷ invested capital | Above WACC, consistently | Cash generation creates value only if reinvested above its cost |
| CFROI vs WACC | Inflation-adjusted cash return versus cost of capital | Positive spread | The cash analogue of the ROIC–WACC spread in `05-returns-and-dupont.md` |
| Incremental return on reinvested cash | Δ FCF ÷ cumulative reinvestment, lagged 2–3 years | Above WACC | Averages hide a deteriorating margin on new investment |
| Intrinsic growth rate | Reinvestment rate × cash return on capital | Compare to the growth the market is pricing | The compounding arithmetic a DCF is implicitly asserting |

**Red flags:** heavy reinvestment at cash returns below the cost of capital (busy value destruction); declining cash returns on rising invested capital; acquisitions absorbing all the FCF with no improvement in returns; leverage and dividends both calibrated to peak-cycle cash generation.

---

## 22. India versus US: conventions that break comparability

- **Reporting frequency.** Indian listed companies file quarterly *results* but a balance sheet and cash-flow statement only **half-yearly** under SEBI LODR. You cannot compute a quarterly CCC or CFO for an Indian filer the way you can from a 10-Q. State that limitation rather than interpolating silently.
- **Standalone versus consolidated.** Always analyse **consolidated** statements for leverage, cash and contingent liabilities; standalone hides subsidiary debt and guarantees. Where the listed entity is a holdco, examine both and say where the cash sits versus where the debt sits.
- **Units.** ₹1 crore = 10 million; ₹1 lakh = 100,000. Convert once, label every table, and never mix crore and million within one table.
- **Interest inside CFO.** Ind-AS/IFRS optionality versus US GAAP's mandatory operating classification (§19). Normalise before any cross-border CFO comparison.
- **CARO 2020** (India) has no US analogue and is a free forensic read: short-term funds applied to long-term purposes, loans and advances to related parties, wilful-defaulter status, undisclosed income surrendered in tax proceedings, whistle-blower complaints, and the auditor's view on fund diversion.
- **Schedule III ratio and ageing disclosures** (India): current ratio, debt-equity, DSCR, return ratios, inventory and receivable turnover and more must be disclosed with an explanation for any change above 25% year on year — plus ageing schedules for receivables, payables, CWIP and intangibles under development. Read management's own explanation first, then test it.
- **Contingent liabilities** (India) are typically dominated by disputed tax demands and disclosed gross. Do not add them to debt at face value, but do assess litigation stage, precedent and the company's track record.
- **Concall transcripts** (India) are a primary source and frequently the only place working-capital, collection and covenant questions are answered. US equivalents: Item 7 liquidity and capital resources, the earnings call, and EDGAR full-text search across exhibits.
- **Credit information.** India: rating rationales from CRISIL, ICRA, CARE and India Ratings are detailed, free and often more candid than the annual report. US: agency reports are gated, but bond prices, spreads and 8-K covenant events are public.

---

## Checklist

- [ ] Run the sector gate first — if bank, NBFC, insurer, REIT/InvIT, developer or miner, switch to the sector file before computing any ratio here.
- [ ] Build adjusted net debt: borrowings + leases + pension/gratuity deficit + reverse factoring + recourse securitisation + guarantees + NCI puts + hybrids, less *proven* unrestricted cash.
- [ ] Prove the cash: reconcile interest income to average balances at market rates; explain any large simultaneous gross-cash-and-gross-debt position.
- [ ] Compute leverage on adjusted net debt and on mid-cycle EBITDA; report gross as well as net.
- [ ] Map the maturity ladder against cash + committed undrawn + projected FCF for 24 months; name the maturity-wall year.
- [ ] Split debt by fixed/floating, currency and secured/unsecured; check hedging and how much unencumbered collateral remains.
- [ ] Compute earnings-based and cash-based coverage; stress-test at −25% CFO and at current refinancing rates.
- [ ] Find the covenants; compute headroom %, note the EBITDA definition, springing triggers, cross-defaults and any waiver history.
- [ ] Report absolute available liquidity and months of runway, not just current and quick ratios; verify facilities are committed.
- [ ] Compute DSO, DIO, DPO and CCC on average balances; test whether any improvement came from factoring or stretched payables.
- [ ] Test receivables growth versus revenue, allowance trend, ageing buckets, concentration and related-party receivables; test finished-goods inventory versus sales.
- [ ] Sweep the notes for off-balance-sheet and contingent items; present reported versus quasi-debt-adjusted leverage side by side.
- [ ] Screen for toxic financing and chronic dilution; compute potential dilution at a stressed price.
- [ ] Compute tangible book, goodwill/equity, capex/D&A and asset age; read the impairment assumptions and (India) the CWIP ageing.
- [ ] Plot the five-year leverage trend and attribute it; corroborate with Altman/Piotroski, ratings, bond spreads and India-specific stress tells.
- [ ] Compute cumulative CFO/net income over 3–5 years and the Sloan accrual ratio; bridge net income to CFO line by line.
- [ ] State your FCF definition; compute FCF margin, FCF/NI, FCF/EBITDA and the full EBITDA-to-FCF bridge.
- [ ] Estimate maintenance capex independently; cross-check against disclosed capacity or output growth.
- [ ] Recompute FCF net of SBC; check whether buybacks reduce the share count or only offset issuance.
- [ ] Build the five-year sources-and-uses table; reconcile to change in net debt and share count; test the FCF payout ratio.
- [ ] Check for classification games: factoring, capitalised costs, lease and interest classification, one-offs inside CFO.
- [ ] Compare cash tax to book tax; estimate the sustainable rate and use it forward (India: 115BAA, MAT credit, SEZ expiry).
- [ ] Look at FCF through the last downturn; compute FCF volatility and set a mid-cycle normalised FCF for valuation.
- [ ] Compute CROIC versus WACC and the incremental return on reinvested cash.
- [ ] Normalise India/US conventions (consolidated basis, crore units, interest-in-CFO, half-yearly cash-flow availability) before any cross-market comparison.
- [ ] State every band you cite as indicative, and immediately give the peer-set and own-history figures that override it.
