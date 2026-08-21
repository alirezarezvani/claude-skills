# Income Statement Analysis and Earnings Quality

Use this when: you are at Stage 4 and need to establish whether the reported profit is real, repeatable, and earned by the operating business.

The income statement is the most-read and least-trusted of the three statements. It is the one management has the most discretion over, the one that drives headlines and multiples, and the one that can be made to say almost anything within the rules. Your job here is not to admire the profit number — it is to take it apart, find out which parts recur, which parts are cash, and which parts are the accounting equivalent of a loan from next year. Everything downstream (returns on capital, valuation, scoring) inherits the errors you fail to catch here.

## Contents

- [1. The OPM trap — read this before computing any margin](#1-the-opm-trap--read-this-before-computing-any-margin)
- [2. Revenue growth decomposition](#2-revenue-growth-decomposition)
- [3. The margin ladder](#3-the-margin-ladder)
- [4. Operating leverage and the fixed/variable split](#4-operating-leverage-and-the-fixedvariable-split)
- [5. Below-the-line: the EBIT-to-PAT bridge](#5-below-the-line-the-ebit-to-pat-bridge)
- [6. Other income reliance](#6-other-income-reliance)
- [7. One-offs, exceptionals and the adjusted-earnings gap](#7-one-offs-exceptionals-and-the-adjusted-earnings-gap)
- [8. Tax normalcy and sustainability](#8-tax-normalcy-and-sustainability)
- [9. Accruals versus cash — the single highest-yield test](#9-accruals-versus-cash--the-single-highest-yield-test)
- [10. Revenue recognition aggressiveness](#10-revenue-recognition-aggressiveness)
- [11. Vendor and customer financing — demand bought with your own balance sheet](#11-vendor-and-customer-financing--demand-bought-with-your-own-balance-sheet)
- [12. Per-employee productivity cross-check](#12-per-employee-productivity-cross-check)
- [13. Segment profitability and mix](#13-segment-profitability-and-mix)
- [14. Share-based comp, dilution and per-share quality](#14-share-based-comp-dilution-and-per-share-quality)
- [15. Depreciation adequacy and capitalisation policy](#15-depreciation-adequacy-and-capitalisation-policy)
- [16. Where this file does not apply](#16-where-this-file-does-not-apply)
- [17. Writing the earnings-quality verdict](#17-writing-the-earnings-quality-verdict)
- [Checklist](#checklist)

---

## 1. The OPM trap — read this before computing any margin

**Margin level is sector-bound and close to meaningless across sectors. Margin trend, and the reason behind the trend, is where the information lives.**

A distributor at 4% operating margin and a software firm at 30% cannot be ranked against each other. The distributor turns its capital over ten times a year and may earn a 40% return on capital; the software firm may be spending three years of gross profit to acquire each customer and earn less. Margin is one input into return on capital (see `05-returns-and-dupont.md`) — it is never a standalone quality score, and a screen sorted on OPM descending is a list of industries, not a list of good businesses.

What margin *does* tell you, and only in these forms:

| Question | What to compare | What it means |
|---|---|---|
| Does this business have pricing power? | Its own gross margin across a full input-cost cycle | Stable/expanding GM through a raw-material spike is the clearest quantitative footprint of a moat |
| Is it winning or losing its position? | Its margin vs the sector median, tracked over 5–10 years | Converging toward peers = advantage eroding; diverging above = advantage compounding |
| Is management running it well? | GM trend vs OPM trend | GM flat but OPM falling is overhead bloat; GM falling but OPM held is cost-cutting masking a demand problem |
| Is the margin structural or cyclical? | Margin vs capacity utilisation, commodity spreads, currency | Peak-cycle margin extrapolated forever is the most common valuation error in cyclicals |

**Two vocabulary traps that cause real errors:**

- **India:** what Indian screeners and concalls call "OPM" is almost always **EBITDA margin** — operating profit *before* depreciation, and computed *excluding* other income. What a US analyst calls "operating margin" is **EBIT margin**, after depreciation. Comparing an Indian "OPM %" to a US "operating margin %" without adjusting for depreciation is an apples-to-oranges error of several hundred basis points. Always state which you mean.
- **India:** the Schedule III P&L format has **no gross profit line**. Construct it yourself: revenue from operations minus (cost of materials consumed + purchases of stock-in-trade + changes in inventories of FG/WIP/stock-in-trade). Decide explicitly whether to include power & fuel, freight and direct labour, and apply the same definition to every peer — otherwise the peer comparison is noise.
- **Both markets:** Ind-AS 116 / IFRS 16 moved operating-lease rent out of opex into depreciation and interest, inflating EBITDA margin with no economic change. Retailers, airlines, hotels and QSR are affected most. Never compare a post-adoption EBITDA margin to a pre-adoption one, or an IFRS lessee to a US GAAP operating-lease lessee, without adjusting. See `14-accounting-comparability.md`.

---

## 2. Revenue growth decomposition

Headline growth is an aggregate of drivers with completely different durability. Decompose it before you value it.

**Decompose into:** organic volume · price/realisation · product and customer mix · currency translation · acquisitions and divestitures.

Sources for the bridge: MD&A / Item 7 in the 10-K, the "revenue bridge" slide in the investor deck, constant-currency disclosures, and unit disclosures (tonnes, units, subscribers, room-nights, billable headcount, same-store/like-for-like). In India, the concall Q&A is often the only place volume-versus-realisation is split — management will give it if asked, and the transcript is a primary source.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Revenue CAGR (3/5/10y) | (End/Start)^(1/n) − 1, consolidated | Comfortably above nominal GDP + sector inflation | Below nominal GDP is real-terms shrinkage regardless of the reported "growth" |
| Organic growth % | Reported growth − acquired revenue contribution − FX | Should be the majority of total growth | Isolates the actual franchise from deal-making |
| Volume growth vs realisation growth | Units/tonnes/subs YoY vs revenue-per-unit YoY | Volume positive over a cycle | Price-led growth reverses when input costs fall; volume compounds |
| Same-store / like-for-like | Revenue from outlets/contracts open the full comparable period | Positive and above inflation | Strips out the store-opening treadmill in retail, QSR, hotels |
| Book-to-bill; backlog coverage | New orders ÷ revenue; backlog ÷ trailing revenue (months) | >1.0x; coverage stable or rising | Leading indicator for EPC, capital goods, IT services, defence |
| Constant-currency growth | Reported growth ex-translation | — | FX tailwinds are not performance |

*Indicative ranges vary by market, cycle and period; the company's own history and the peer median override any absolute band.*

**Why this matters:** two companies printing 15% growth can be opposite investments. Volume-led growth with stable price is demand. Price-led growth during an inflation spike is a loan from the next deflation. Roll-up growth resets the baseline every year and hides an organic business that may be shrinking — check what happens to the growth rate if M&A pauses, and pair this with the serial-acquirer accounting checks in `07-forensic-red-flags.md`.

**Red flags:** growth entirely from price while volumes decline; growth that vanishes when acquisitions are stripped out; deceleration masked by serial M&A; revenue growing below inflation for years; growth carried by one large contract or one customer; recurring quarter-end revenue surges.

**India note:** Q4 standalone/consolidated results are frequently a *balancing figure* — audited full-year minus the three limited-review quarters. Provisions, true-ups and rev-rec adjustments cluster there. Always compare Q4 margin and other income to the 9M run-rate; a Q4 that looks nothing like the rest of the year is telling you where the discretion was exercised.

---

## 3. The margin ladder

Walk every rung. Each level answers a different question, and the *differences between adjacent rungs* are where the information is.

| Rung | What it isolates | What can be manipulated at this rung |
|---|---|---|
| **Gross margin** | Pricing power and cost position — the purest moat read | Cost reclassification into SG&A; capitalising production costs; inventory absorption games; channel stuffing |
| **EBITDA margin** | Cash-ish operating profitability before capital intensity | The most gamed metric of all: "adjusted" add-backs, lease accounting, SBC added back |
| **EBIT / operating margin** | True core profitability including the cost of the asset base | Understated depreciation; opex capitalised; "other operating income" of dubious nature parked above the line |
| **PBT margin** | After financing and associates | Interest capitalised into assets; associate income; forex reclassification |
| **PAT margin** | After tax and minorities | Tax holidays, deferred-tax reversals, minority-interest structure |
| **EPS** | After dilution and buybacks | Share-count engineering; SBC excluded from adjusted EPS |

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Gross margin % | Gross profit ÷ revenue (construct manually for Ind-AS filers) | Wholly sector-bound: ~15–25% distribution/EPC, ~25–40% auto components, ~50–70% branded consumer/pharma, ~70–90% software | Level says little; *stability through an input-cost cycle* says a lot |
| GM delta (bps YoY, 5y trend) | Change in GM in basis points | Trend flat-to-up | Multi-year erosion = commoditisation working its way down every line |
| Raw material % of sales | Cost of materials ÷ revenue | — | Sizes the input-cost exposure you are underwriting |
| EBITDA margin % | EBITDA ÷ revenue; state whether pre- or post-IFRS 16 | Sector-bound | Drives multiples and covenants — which is exactly why it is manipulated |
| Adjusted-vs-reported EBITDA gap | (Adj EBITDA − reported) ÷ reported | <5%, and shrinking | A persistent double-digit gap means the "clean" number overstates earning power |
| Add-backs as % of EBITDA | Sum of all adjustments ÷ EBITDA | <10% | Add-backs that appear every year are operating costs |
| EBIT margin % | EBIT ÷ revenue | Sector-bound | The cleanest measure of scalable core profitability |
| SG&A / R&D / employee cost as % of sales | Each line ÷ revenue, 5-year trend | Stable or falling with scale | Reveals whether growth is being bought or earned |

*Indicative ranges vary by market, cycle and period; peer and own-history comparison overrides any absolute band.*

**The diagnostic that matters most: compare the GM trend with the OPM trend.**
- GM stable, OPM falling → overhead bloat or negative operating leverage. Ask what SG&A is buying.
- GM falling, OPM stable → costs are being cut to protect the print. Check whether R&D, advertising or maintenance capex is being starved — margin held by mortgaging the future looks identical to margin held by efficiency for about three years.
- Both rising, revenue flat → suspicious. Cost capitalisation and reclassification produce exactly this signature.
- A sudden unexplained GM jump with no mix or input-price explanation is a forensic trigger, not a positive.

**On EBITDA specifically:** it excludes capex, working capital and the real cost of stock compensation. Treat every add-back as a claim requiring evidence. Restructuring charges in five consecutive years are a cost of doing business. Reconcile adjusted EBITDA back to statutory operating profit *and* to operating cash flow; if adjusted EBITDA grows while cash flow does not, the adjustments are the growth. US filers must publish a Reg G / Item 10(e) reconciliation in the 10-K or 8-K Item 2.02 — read it, do not take the press-release headline.

---

## 4. Operating leverage and the fixed/variable split

Estimate the fixed/variable cost split and measure how earnings respond to revenue.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Degree of operating leverage | %Δ EBIT ÷ %Δ revenue, over several periods | 1.5–3x for most industrials; >4x is a cyclical warning | Sizes the downside, not just the upside |
| Incremental margin | Δ EBIT ÷ Δ revenue (YoY) | At or above current EBIT margin | Falling incremental margin means new revenue is worth less than old revenue |
| Decremental margin | Same, on a revenue decline | Below the incremental margin | Tells you what a 20% volume drop actually does to EBIT |
| Contribution margin % | (Revenue − variable costs) ÷ revenue | — | Needed to compute breakeven |
| Breakeven revenue | Fixed costs ÷ contribution margin % | Comfortably below trough-cycle revenue | If breakeven is creeping toward current sales, a mild downturn produces losses |
| Capacity utilisation | Volume ÷ rated capacity | — | Margin expansion at rising utilisation is *not* structural improvement |

**Why it matters:** operating leverage determines earnings volatility and therefore the multiple the business deserves. Margin expansion driven purely by volume flowing over a fixed base will reverse just as fast on the way down. Before crediting management for a 300bps margin gain, decompose it: how much was utilisation, how much was input-cost deflation, how much was price, how much was genuine structural cost-out that survives a downturn. Then stress the EBIT at trough-cycle revenue — that number, not the current one, is what a cyclical should be valued on (`13-situations.md`).

---

## 5. Below-the-line: the EBIT-to-PAT bridge

Build the bridge explicitly and quantify every step: EBIT → finance costs → interest/other income → share of associates and JVs → exceptional items → tax → non-controlling interests → PAT attributable to owners.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| PBT margin % | PBT ÷ revenue | Sector-bound | Where financing structure shows up |
| PAT margin % | PAT attributable to owners ÷ revenue | Sector-bound | The bottom line equity holders actually own |
| PAT growth vs EBIT growth | 3–5 year CAGR of each | Should track within a few points | Persistent divergence means the profit engine is below the operating line |
| Interest coverage | EBIT ÷ finance cost | >4x general; >6x for cyclicals | Detail in `04-balance-sheet-and-cashflow.md` |
| Minority interest as % of PAT | NCI share ÷ consolidated PAT | — | High NCI means headline consolidated PAT overstates what owners get |
| Associate/JV share as % of PAT | Share of profit of associates ÷ PAT | Small, unless it is the business model | Associate income is non-cash until dividended up |

**Why it matters:** net margin can rise for years while the operating business decays, on nothing but falling interest rates, a rising associate contribution, or a tax break. That growth is lower quality — management does not control it, it does not compound, and it should not earn the multiple that operating growth earns.

**Red flags:** net margin rising while operating margin falls; profit growth attributable mainly to deleveraging or a falling tax rate; consolidated PAT flattered by a partly-owned subsidiary (check the "attributable to owners of the parent" line, not the consolidated total); interest capitalised into CWIP suppressing the finance-cost line while a project builds. **India:** always compare standalone and consolidated — where they diverge sharply, the subsidiaries and associates are the story.

---

## 6. Other income reliance

Disaggregate "other income" into recurring (interest on surplus cash, dividends from investments) and non-core/lumpy (asset-sale gains, treasury and mark-to-market gains, forex, government grants and export incentives, insurance recoveries, provision write-backs).

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Other income as % of PBT | Other income ÷ PBT | <10%; investigate above ~15–20% | Above that, a share of the "profit" is not the business |
| Recurring vs non-recurring split | From the other-income note in the accounts | Majority recurring | Disposal gains do not repeat |
| Treasury income vs core EBIT | Investment income ÷ EBIT | — | A large cash pile earning interest is not operating skill |
| Forex gain/loss as % of PBT | Net FX ÷ PBT | Small and two-directional over time | One-directional FX "gains" every year suggests policy, not luck |

**Why it matters:** other income overstates sustainable earning power and is the easiest lever for hitting a target. Its collapse is also mechanical: interest income vanishes the moment the cash pile is deployed into capex or an acquisition, so a company valued on a P/E that includes treasury income gets re-rated downward the year it finally invests.

**India note:** the Schedule III format gives "Other income" its own prominent line, and Indian screeners exclude it from operating profit by design — which is correct. Read the note behind the line; export incentives, PLI grants and forex are often material and are frequently reported as though they were operating.

---

## 7. One-offs, exceptionals and the adjusted-earnings gap

Catalogue every exceptional, special, restructuring, impairment, litigation-provision, write-off and disposal item for the last **5–7 years** in a single table. The table is the analysis — the pattern across years is what a single-year read cannot show.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Exceptional items as % of PBT | Absolute exceptional ÷ PBT, per year | Genuinely rare | Frequency, not size, is the tell |
| Frequency over 5–7 years | Count of years with an exceptional charge | ≤2 of 7 | Charges in 5 of 7 years are operating costs mislabelled |
| Cumulative restructuring/impairment | Sum over the period vs cumulative reported PAT | Small fraction | Shows how much "profit" was written back off |
| Adjusted vs statutory PAT gap | (Adj PAT − statutory) ÷ statutory | <10% and non-directional | A permanent one-way gap means the adjustments are the earnings |

**Why it matters:** classification of an item as exceptional is discretionary, and the discretion runs one way. Only charges get excluded from "underlying" profit; one-off *gains* stay in. Normalised earnings built on that asymmetry are systematically overstated, and every multiple computed on them is systematically too low.

**Red flags:** "non-recurring" charges in most years; asymmetric treatment of gains and losses; a big-bath write-off in the first year of a new CEO (resetting the base so future growth looks better); impairment of goodwill from a recent acquisition (a priced admission of overpayment — see `07-forensic-red-flags.md`); serial restructuring programmes each announced as the last one.

**India note:** Ind-AS 1 discourages the label "extraordinary items", but Indian filers still present an "Exceptional items" line. Cross-check it against the CARO report, the Key Audit Matters, and the contingent-liabilities note — provisions created and later written back to profit are a classic cookie jar.

---

## 8. Tax normalcy and sustainability

Compare the effective tax rate to the statutory rate and read the rate reconciliation in the tax footnote.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Effective tax rate | Total tax expense ÷ PBT | Near statutory: India ~25.17% under the 115BAA concessional regime (22% + surcharge + cess); US ~21% federal + state | A rate far below statutory needs a durable, named reason |
| Statutory-to-effective gap | Reconciliation line items | Explained and stable | Unexplained gaps are the warning |
| Cash tax rate | Taxes actually paid (cash flow statement) ÷ PBT | Close to the book rate over 3–5 years | Book profit with negligible cash tax means the profit is not being recognised by the tax authority either |
| Deferred tax movement | Δ net DTA/DTL | Small relative to PAT | A large DTA recognition can single-handedly create a profitable year |
| Remaining life of incentives | From the tax note / MD&A | Known and modelled | Expiry creates a step-down in EPS with no operational change |

**Why it matters:** an abnormally low tax rate inflates EPS in a way that does not persist. Tax holidays expire on a published date; when they do, PAT drops by the difference with no warning from the operating business. Model the post-expiry EPS before applying a multiple.

**India-specific:** SEZ/Section 10AA benefits taper and sunset; the old 80-IA infrastructure deductions; MAT/AMT credits being drawn down; whether the company has opted into the 115BAA regime (which forfeits most incentives permanently). **US-specific:** GILTI/FDII, R&D credits, the Section 174 capitalisation rules that have widened the book-versus-cash tax gap for R&D-heavy filers since 2022, valuation allowances on deferred tax assets, and uncertain tax positions (FIN 48) disclosed in the footnote.

**Red flag:** net profit growth where the largest single contributor is a falling tax rate. Strip it out and re-read the growth rate.

---

## 9. Accruals versus cash — the single highest-yield test

If you run only one earnings-quality test, run this one. Accrual-heavy earnings reliably revert.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Cash conversion | CFO ÷ net income, averaged over 3–5 years | >0.9x; >1.0x is strong | A single year is noise; a five-year average below 0.8x is a finding |
| FCF conversion | (CFO − capex) ÷ net profit | >0.6x for a maturing business | Profit that never becomes spendable cash is not profit yet |
| OCF ÷ EBITDA | Operating cash flow ÷ EBITDA | >0.7x | Isolates working-capital absorption |
| Sloan accrual ratio | (Net income − CFO) ÷ average total assets | <5%; >10% is a red flag | The classic academic predictor of earnings reversal |
| Balance-sheet accruals | Δ net operating assets ÷ average net operating assets | Low and non-trending | Catches accruals that route through investing, not just working capital |
| Receivables/inventory growth vs revenue growth | Each YoY growth rate | At or below revenue growth | Both growing faster than sales is the standard signature of pulled-forward revenue |

*Indicative ranges vary by market, cycle and period; a growing company legitimately absorbs working capital — compare to its own history and to peers growing at the same rate.*

**Why it matters:** the gap between accounting profit and cash generation is the most reliable early-warning signal available from public filings, and it is early — it typically widens for several periods before the reported numbers break. Note that the direction of the test is asymmetric: cash below profit is a warning; cash *above* profit is usually a good sign (negative working capital, deferred revenue growth) but check it is not just underinvestment or a one-time payables stretch.

Depth on working-capital mechanics and the cash flow statement sits in `04-balance-sheet-and-cashflow.md`; the fraud-detection framing (Beneish-style ratios, channel stuffing) sits in `07-forensic-red-flags.md`.

---

## 10. Revenue recognition aggressiveness

Read the revenue-recognition accounting policy and the critical-estimates note. You are looking for how much judgement sits between a customer's order and a revenue line.

**What to examine:**
- **Timing:** point-in-time vs over-time; percentage-of-completion vs milestone (dominant in EPC, infrastructure, defence, and long-cycle IT contracts, and the single most judgement-laden method in common use).
- **Gross vs net (principal vs agent):** whether a marketplace books GMV or commission. Gross-basis reporting can overstate apparent scale by an order of magnitude and makes every margin ratio incomparable to a net-basis peer.
- **Multi-element arrangements:** how a bundle of hardware, licence and support is allocated across performance obligations, and how much revenue is pulled to day one.
- **Bill-and-hold, channel financing, distributor sell-in vs sell-through:** revenue recognised into a channel is not demand.
- **Returns, rebates, discounts and warranty provisioning:** under-provisioning inflates current revenue and margin.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| DSO | (Receivables ÷ revenue) × 365 | Stable vs own history and peers | Rising DSO with rising revenue is the classic pulled-forward-revenue signature |
| Contract assets / unbilled receivables growth | YoY growth vs revenue growth | At or below revenue growth | Revenue recognised ahead of the right to bill is the softest revenue there is |
| Deferred revenue / contract liabilities | YoY trend vs revenue | Growing with revenue for subscription models | Falling deferred revenue while revenue grows = the backlog is being consumed, not replenished |
| Provision for returns/rebates as % of sales | From the provisions note | Stable | A quietly shrinking provision rate is a margin lever, not an improvement |

**Red flags:** contract assets compounding well ahead of revenue; DSO up several quarters in a row; a rev-rec policy change that happens to lift growth; quarter-end revenue spikes (especially the Indian Q4 balancing quarter); gross-basis presentation adopted without a principal-role justification; revenue growth concentrated in the least-verifiable geography or the newest business line.

**Standards:** Ind-AS 115 and IFRS 15 and ASC 606 are converged in substance, so the five-step model and the disaggregation disclosures are comparable across markets — use the disaggregation table, it is one of the most useful and least-read disclosures in any filing.

---

## 11. Vendor and customer financing — demand bought with your own balance sheet

Determine whether the company is funding its own customers' purchases: captive finance arms, seller notes, unusually long or extended credit to distributors, channel financing arrangements, guarantees of customer or dealer debt, buy-back or residual-value commitments, and vendor loans on equipment sales.

**Where to look:** notes receivable and long-dated/non-current receivables; the related-party and contingent-liability notes; guarantees given; the financing subsidiary's own accounts; and the gap between revenue growth and cash collections. In India, CARO reporting on loans and guarantees, and the Ind-AS 24 related-party note, are the practical route.

**Why it matters:** revenue funded by the seller's own credit is not demand — it is a loan that has been booked as a sale. It reads as clean organic growth until the receivables sour, and then it reverses violently, taking both the revenue and the balance sheet down at once. This mechanism has repeatedly destroyed telecom-equipment, solar, EV and capital-goods names historically; the pattern is always the same and always visible in the receivable maturities before it is visible in the P&L.

**What to compute:** customer financing exposure (on- and off-balance-sheet) as a % of annual revenue; the share of revenue growth attributable to financed sales; and the receivable ageing profile. If a material share of growth is vendor-financed, treat that revenue as lower quality and treat the company as partly a lender — which means the sector playbooks for lenders (`sectors/nbfc.md`) have relevant tests even for an industrial.

---

## 12. Per-employee productivity cross-check

Compute revenue per employee and gross profit per employee versus peers and over 5+ years, alongside headcount growth versus revenue growth.

**Why it matters:** headcount is one of the few operating inputs that is hard to fabricate and is often disclosed independently of the financials (annual report, LinkedIn-scale disclosures, ESG/BRSR reports, regulatory filings). It provides an external sanity check on claimed scale. Deteriorating revenue per employee while a growth story is being told, or a hiring freeze that contradicts guidance, is an early and independent tell.

**Read it sector-appropriately.** In IT services, revenue per employee combined with utilisation and offshore mix is a core margin driver, not merely a check. In manufacturing it tracks automation and mix. In software and platforms it should rise steeply with scale — if it does not, the business is not actually scaling. **India note:** employee benefit expense is a separate Schedule III line and headcount is disclosed in the Board's Report and BRSR, so this cross-check is usually computable for NSE/BSE names.

---

## 13. Segment profitability and mix

Break the consolidated result into reportable segments and geographies: revenue mix, segment EBIT and margin, growth rate, capital employed, and the size of unallocated corporate costs.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Segment revenue mix % | Segment revenue ÷ total | — | Shows where the business actually is |
| Segment EBIT margin and 5y trend | From the segment note | — | The consolidated margin is a weighted average hiding both good and bad |
| % of profit from the top segment | Largest segment EBIT ÷ total segment EBIT | <60% for a diversified claim | Concentration in one segment means you are underwriting one business, not a portfolio |
| Unallocated / corporate cost as % of EBIT | From the reconciliation | Small and stable | Rising unallocated costs is where inconvenient items go |
| Segment ROCE | Segment EBIT ÷ segment capital employed (where disclosed) | — | The only way to see if a segment earns its capital |

**Why it matters:** consolidated numbers blend divergent economics and disguise cross-subsidy. A profitable core funding a chronic loss-maker destroys value even while consolidated profit grows, and mix shift toward lower-return segments lowers the multiple the whole company deserves even when EPS is rising. Segment disclosure is also where you find whether the growth story and the profit source are the same business — frequently they are not.

**Red flags:** frequent redefinition of segments (a common way to bury a deteriorating unit); aggregation into a single "others" bucket; segment results presented without capital employed; rising unallocated costs.

**Conventions:** Ind-AS 108 and ASC 280 both use the management approach, so segments follow internal reporting and are *not* comparable across companies — build the peer comparison at the metric level, not the segment-label level. US filers now disclose significant segment expenses under ASU 2023-07, which materially improves this analysis for 10-K filers. Indian companies disclose segment revenue, results, assets and liabilities quarterly — use the quarterly segment series, it is the highest-frequency view of mix available.

---

## 14. Share-based comp, dilution and per-share quality

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| SBC as % of revenue | SBC expense ÷ revenue | <5%; >10% is severe | A real cost of labour paid in shares |
| SBC as % of operating cash flow | SBC ÷ CFO | <20% | SBC is added back in the cash flow statement — CFO is flattered by exactly this amount |
| Diluted share count growth | YoY change in weighted diluted shares | ≤1–2% p.a. | Steady dilution is a quiet transfer of value away from you |
| Diluted EPS CAGR vs net income CAGR | Both over 5 years | EPS ≥ NI growth | EPS lagging net income means dilution is eating the growth |
| Buyback contribution to EPS growth | EPS growth − net income growth | Should be a minority of EPS growth | Separates operating performance from financial engineering |
| Net buyback vs issuance | Shares retired − shares issued | Genuinely negative | Buybacks that only mop up option issuance are compensation, not capital return |

**Why it matters:** SBC is a real economic cost that is routinely added back to "adjusted" earnings and EBITDA, and it is added back in the cash flow statement by construction — so a company with heavy SBC shows flattering margins *and* flattering operating cash flow simultaneously. Meanwhile EPS can rise for years on debt-funded buybacks while revenue and EBIT go nowhere. Always decompose EPS growth into operating growth, margin, and share count before crediting management with anything.

**Conventions:** dilution must be computed on the diluted count under the treasury-stock method, plus any convertible instruments under the if-converted approach (ASU 2020-06 for US filers). **India:** ESOP charges appear within employee benefit expense; the scheme details, outstanding options and exercise prices sit in the Board's Report / ESOP disclosure under the SEBI SBEB Regulations. Indian SBC is generally far smaller than US tech levels — do not import a US benchmark. Also check warrants issued to promoters and preferential allotments, which dilute outside any ESOP scheme.

---

## 15. Depreciation adequacy and capitalisation policy

Understated depreciation and aggressive capitalisation are the two quietest ways to inflate current profit, because both defer a real cost rather than eliminating it.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| D&A as % of sales | D&A ÷ revenue, 5-year trend | Stable; sector-bound | A falling ratio with a growing asset base needs an explanation |
| D&A ÷ capex | 5-year averages of both | ~0.8–1.2x for a steady-state business | D&A persistently far below capex means depreciation is not reflecting replacement needs |
| Implied depreciation rate | Depreciation ÷ average gross block | Consistent with disclosed useful lives | Falling implied rate = lives lengthened or asset mix shifted |
| Capitalised development/software as % of relevant spend | From the intangibles note and cash flow statement | Low vs peers who expense | If peers expense what this company capitalises, the margins are not comparable |
| Amortisation of acquired intangibles | From the intangibles note | — | Serial acquirers "adjust it out" while continuing to buy the intangibles |

**Why it matters:** capitalising a cost moves it from this year's P&L to the next several years' depreciation line. Profit rises now, and the business looks more asset-light and more profitable than it is. The comparison that exposes it is against peers: within the same sector, if one company capitalises development costs and product engineering while the others expense them, the margin gap is an accounting choice, not a performance gap. Normalise before you compare (`14-accounting-comparability.md`).

**Red flags:** useful lives extended in a year when earnings needed help; a change in depreciation method; capitalised development or software rising faster than revenue; capitalised interest large relative to PBT; a low depreciation charge against a large gross block; subscriber-acquisition or contract-acquisition costs capitalised.

**Conventions:** **India** — Schedule II of the Companies Act 2013 prescribes indicative useful lives; a company using longer lives must disclose technical justification, so a deviation is both visible and meaningful. Also check the componentisation approach and the treatment of CWIP (long-standing CWIP with capitalised interest is a classic profit-deferral and impairment risk). **US/IFRS** — IFRS/Ind-AS requires capitalising development costs meeting the IAS 38 criteria while US GAAP largely expenses R&D (with narrow software exceptions), which is a structural, not discretionary, difference between an IFRS and a US GAAP peer. Adjust for it explicitly rather than treating it as a quality difference.

---

## 16. Where this file does not apply

The governing principle bites hardest here. For several sectors the standard income-statement ladder is undefined or inverted, and applying it produces confident nonsense:

- **Banks and NBFCs** — there is no revenue, COGS or gross margin. The equivalents are net interest income, NIM, fee income, cost-to-income, credit cost and provision coverage. Interest expense is a cost of goods, not a financing item. Go to `sectors/banks.md` / `sectors/nbfc.md`.
- **Insurers** — premium is not revenue in the ordinary sense; the profit signal is the combined ratio (general/health) or VNB margin and embedded-value movement (life). `sectors/insurance.md`.
- **REITs / InvITs** — net income is meaningless because depreciation on appreciating property overwhelms it; use FFO/AFFO and NDCF. `sectors/realestate-reit.md`.
- **Miners and commodity producers** — margin is a price artefact. Use cost-curve position (C1/AISC), reserve life and mid-cycle realisations. `sectors/metals-mining.md`.
- **Loss-making growth companies** — the margin ladder still applies but the level is uninformative; work on gross margin, contribution margin after customer-acquisition cost, cohort economics and the path to breakeven. `13-situations.md`.

---

## 17. Writing the earnings-quality verdict

Do not present this as fifteen paragraphs of findings. Compress to a judgement the reader can act on:

1. **Quality of the growth** — how much of the last three years' revenue growth was volume, price, mix, FX and M&A, in numbers.
2. **Quality of the margin** — direction over 5–10 years, the reason for the direction, and whether it is structural or cyclical. State the peer median so the level is anchored, and say explicitly that the level alone is not the finding.
3. **Quality of the profit** — how much of PAT is operating, and what the multi-year cash conversion is.
4. **The adjustment gap** — statutory PAT versus the company's own adjusted number, and whether the gap is one-directional.
5. **The three things that would change this verdict** — specific, observable, checkable next quarter.

Then carry the *normalised* earnings figure forward into valuation, not the reported one, and state every normalisation you made.

---

## Checklist

- [ ] Stated whether "OPM" here means EBITDA margin (Indian convention) or EBIT margin (US convention).
- [ ] Constructed gross margin manually for Ind-AS filers and used the identical definition for every peer.
- [ ] Decomposed 3-year revenue growth into volume, price/mix, FX and M&A, with a source for each.
- [ ] Compared revenue growth to nominal GDP + sector inflation, and to industry volume growth.
- [ ] Checked same-store/like-for-like and book-to-bill or backlog coverage where the sector has them.
- [ ] Plotted the full margin ladder for 5–10 years; compared the GM trend against the OPM trend and explained any divergence.
- [ ] Checked lease-accounting (IFRS 16 / Ind-AS 116) comparability before comparing EBITDA margins.
- [ ] Listed every add-back to adjusted EBITDA/EPS and tested whether each recurs across 5+ years.
- [ ] Estimated degree of operating leverage and incremental margin; stress-tested EBIT at trough revenue.
- [ ] Built the EBIT→PAT bridge; quantified interest, associates, minorities and tax separately.
- [ ] Split other income into recurring and non-recurring; flagged if it exceeds ~15% of PBT.
- [ ] Tabulated exceptional items for 5–7 years; checked for asymmetric treatment of gains vs losses.
- [ ] Compared ETR to statutory, and cash tax to book tax; noted expiry dates of any tax incentives.
- [ ] Computed 3–5 year average CFO/net income, FCF/PAT and the Sloan accrual ratio.
- [ ] Compared receivables, inventory and contract-asset growth to revenue growth.
- [ ] Read the revenue-recognition policy; checked gross vs net, POC judgement, DSO trend and quarter-end spikes.
- [ ] Checked for vendor/customer financing, guarantees and long-dated receivables funding reported demand.
- [ ] Cross-checked revenue and gross profit per employee against peers and own 5-year history.
- [ ] Analysed segment margins, mix shift, unallocated costs and any segment redefinition.
- [ ] Measured SBC as % of revenue and of CFO; decomposed EPS growth into operating growth vs share count.
- [ ] Tested depreciation adequacy (D&A vs capex, implied rate vs gross block) and capitalisation policy vs peers.
- [ ] Confirmed consolidated vs standalone basis, currency and units on every figure used (India: crore/lakh).
- [ ] Confirmed the sector actually admits these metrics; switched to the sector playbook if it does not.
- [ ] Carried a normalised earnings figure into valuation and disclosed every normalisation made.
