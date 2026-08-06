# Pharma, biotech, CDMO, hospitals and diagnostics — sector playbook

Use this when: the company under analysis makes drugs or drug intermediates (formulations, API, biosimilars), does contract development or manufacturing (CDMO/CRAMS), runs clinical-stage R&D without product revenue, or delivers care (hospitals, single-specialty chains, diagnostics labs, medical devices distribution).

This is not one sector — it is at least five businesses with incompatible economics filed under one GICS heading, and the generic ratio set misreads all of them. The assets that produce the cash are patents, trial data, plant compliance status, prescriber loyalty and consultant relationships, and almost none of them appear on the balance sheet unless somebody bought them. Two consequences dominate everything below: **capital-employed and margin ratios are non-comparable by construction**, and **the single largest source of permanent value destruction in this sector — a regulatory action on a manufacturing site — has zero representation in any financial ratio.** Identify the sub-sector before you compute anything; a metric that is decisive for a hospital chain is noise for a biotech.

## Contents

- [Why the generic ratio set fails here](#why-the-generic-ratio-set-fails-here)
- [The metrics that actually matter](#the-metrics-that-actually-matter)
- [How to value companies in this sector](#how-to-value-companies-in-this-sector)
- [Peer set construction](#peer-set-construction)
- [Sector-specific red flags](#sector-specific-red-flags)
- [Cycle and structural context](#cycle-and-structural-context)
- [India vs global notes](#india-vs-global-notes)
- [Checklist](#checklist)

---

## Why the generic ratio set fails here

**OPM is inverted by R&D accounting.** R&D is expensed as incurred (US GAAP ASC 730 mandates it; IAS 38 / Ind AS 38 permit only narrow development-cost capitalisation after technical feasibility). So the P&L charges the full cost of future revenue today and credits none of the asset. A company cutting R&D from 9% to 4% of sales prints +500bps of OPM and screens as "improving quality" while liquidating its 2030 revenue. Never compare OPM across pharma names without normalising for R&D intensity *and* for business mix — a branded-formulations rupee, a US-generic rupee, an API rupee and a CDMO rupee carry structurally different gross margins.

**ROCE and ROE are non-comparable by construction.** Build a pipeline organically and you expensed everything: capital employed is tiny and ROCE looks spectacular. Buy the identical pipeline and you carry goodwill plus acquired intangibles: ROCE looks poor and reported EPS is crushed by non-cash amortisation. Same economics, opposite scores. Hospitals sit at the far end — structurally low asset turns, and every new unit depresses ROCE for three to five years, so low ROCE during expansion is not evidence of poor quality. Only mature-unit or steady-state ROCE is informative there.

**P/E is undefined or distorted.** For clinical-stage biotech it is permanently undefined — negative EPS is the business model, not a problem. For commercial pharma it is distorted by intangible amortisation, IPR&D impairments, litigation settlements (opioid, talc, antitrust/price-fixing), remediation costs and lumpy upfront/milestone licensing income. Hence the market's use of "core"/"adjusted" EPS — which is itself the sector's primary earnings-management lever, so you must audit the bridge rather than accept the adjusted number.

**D/E and interest cover mislead at both ends.** Biotech is usually net cash; the binding constraint is runway versus burn, not leverage, and a "conservative" balance sheet with 9 months of cash is a distressed one. For hospitals, Ind AS 116 / IFRS 16 converted property rent into a lease liability plus depreciation and interest — inflating EBITDA and gearing overnight with zero economic change. An asset-light lease/O&M operator and an owned-real-estate operator are not comparable on EBITDA margin *or* D/E without an EBITDAR (pre-rent) restatement.

**FCF is a false negative for growth providers and CDMOs.** All the capex is front-loaded growth capex; a hospital chain adding beds, a diagnostics network adding labs, or a CDMO building a block two to three years ahead of revenue shows its worst FCF precisely when it is compounding fastest. Separate maintenance from growth capex before FCF carries any information.

**Reported revenue growth is not a clean signal.** In US generics the base portfolio erodes on price every single year, so flat revenue can conceal strong launches, while a single 180-day first-to-file exclusivity can add hundreds of basis points of margin that disappear on a known calendar date. And US "net revenue" is an estimate, not a fact: gross list price minus a 30–70% gross-to-net accrual for chargebacks, rebates, Medicaid/340B and returns.

**P/B and dividend yield are close to irrelevant.** Book value captures neither the patent estate, the approved-and-inspected plant, the prescriber franchise, nor the clinical talent. Where book value *is* large it usually means acquisitions — i.e. the least organic version of the same business.

**The current ratio tells you almost nothing.** Pharma structurally carries 90–150 days of inventory for legitimate reasons (batch stability testing, regulatory hold, long API lead times), so a "healthy" current ratio may just be slow-moving stock approaching expiry; hospitals and labs run negative working capital, so a low current ratio is normal and healthy.

---

## The metrics that actually matter

All ranges below are **indicative only**. They shift with market, cycle, sub-sector and accounting period. A company's own 5–10 year history and its true peer set override every absolute band here — if a range disagrees with a well-constructed peer median, trust the peers.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| **R&D intensity and productivity** | R&D as % of sales, split by type (innovative NCE/biologic vs ANDA/bioequivalence vs biosimilar); plus approvals and launches per unit of cumulative R&D over rolling 5–10 years, and peak sales or eNPV generated per rupee/dollar spent. Track trend, not level. | India plain-vanilla generics/API 4–7%; India complex generics/specialty 8–12%; global innovator 18–25% (some >30%); CDMO 3–5%; hospitals/diagnostics <1%. A US-facing generic player sustaining <5% is starving its pipeline. | R&D hits the P&L now and pays back in 3–7 years, so cutting it is the fastest way to manufacture margin and EPS that a screen reads as quality. **High OPM plus falling R&D intensity is usually a wind-down, not an edge.** A margin dip caused by a step-up in complex-generic or biosimilar spend is often the best signal in the file. |
| **Regulatory compliance scorecard** (USFDA / EU GMP / WHO-GMP) | Per-site inspection classification (NAI / VAI / OAI), count and *severity* of Form 483 observations, warning letters, import alerts, consent decrees, EIR received or not. Critically: % of consolidated revenue, % of EBITDA and % of pending ANDAs tied to each affected site. | Zero OAI sites, zero open warning letters, zero import alerts. 483s limited to a few procedural observations, closed with an EIR within ~6 months. | The highest-impact operational KPI in Indian pharma and invisible to every financial ratio. An import alert halts that plant's US shipments **and freezes all pending approvals filed from it**, typically 2–4 years — converting a growth asset into a cost centre overnight. History (Ranbaxy, Wockhardt, Sun Halol, Lupin Goa, Divi's, Intas) says remediation takes longer and costs more than guided. Read the FDA inspection classification database and warning-letter list directly; never rely on the press release. Any site under import alert contributing >5% of revenue is a material impairment event. |
| **Data-integrity vs procedural 483 split** | Classify each observation: procedural/documentation vs data integrity (deleted or re-run chromatograms, unofficial "trial" testing, shredded records, shared logins, disabled audit trails). | Zero data-integrity observations. | Procedural findings are a process failure; data-integrity findings are a *culture* failure and imply everything else filed from that site is suspect. They take years, not quarters, to clear and often spread to sister sites. Treat one data-integrity observation as more serious than twenty procedural ones. |
| **ANDA/DMF pipeline with complexity mix** | Cumulative and annual ANDA filings; final vs tentative vs pending approvals; DMF filings; Para IV challenges and first-to-file 180-day exclusivities; share of filings that are complex (injectables, inhalation, ophthalmics, transdermals, peptides, depot/long-acting, 505(b)(2), biosimilars) vs plain oral solids; median filing-to-approval time. | Mid/large-cap Indian US-facing player: 10–20 filings/year, 80–150 cumulative pending, 25%+ in complex categories. Approval-to-launch *conversion* matters more than gross filing count. | Revenue two to four years out is mechanically a function of what is filed today — the only genuine forward indicator for a generics business. But mix decides the economics: a plain oral solid meets 8–12 competitors and double-digit annual erosion; a complex injectable or inhaler may meet 1–3 and hold price for years. A filing count without a complexity breakdown is a vanity metric. |
| **Base price erosion and the revenue bridge** | Decompose reported growth: base price erosion + base volume + new launches + one-off exclusivities + FX + acquisitions. Demand it geography by geography. | US generics: −3% to −7% p.a. is normalised; −8% to −12% signals a commoditised portfolio or consortium pressure; positive base pricing is almost always shortage-driven and non-repeatable. India branded: +3% to +6% price/mix, capped on NLEM products by the annual WPI-linked DPCO revision. | Reported growth nets two large opposing forces. A company can print +10% while its base decays −12% — meaning it must launch harder every year just to stand still, a treadmill a P/E multiple should not capitalise as growth. Only the bridge separates a durable franchise from a launch-dependent one. |
| **Revenue concentration and LOE exposure** | % of revenue *and* of EBITDA from the largest product, top five, and from limited-competition/exclusivity opportunities; % of revenue facing patent expiry, exclusivity loss or a known new entrant within 1, 3 and 5 years. Providers: % revenue from top three units/labs and largest payer. | Top product <10–15% of sales and <20% of EBITDA; 5-year LOE exposure <20–25% of revenue; no single hospital unit >20–25% of chain EBITDA. | Exclusivity profits are a wasting asset with a known expiry date, and at 60–90% incremental margins they can be 200–400bps of consolidated OPM (the gRevlimid windfall across several Indian names is the textbook case). **Applying a normal multiple to peak-exclusivity earnings is the most common single valuation error in this sector.** For innovators, the patent cliff *is* the terminal-value question. |
| **Gross-to-net deductions and accrual adequacy** | Chargebacks, commercial and Medicaid rebates, 340B, returns, shelf-stock adjustments, copay assistance, failure-to-supply penalties, as % of gross sales; balance-sheet accrual as a multiple of one quarter's deductions; size of prior-period true-ups credited to current revenue. | US branded 45–70% of list; US generics ~30–55%. Accrual coverage stable or rising; prior-period true-ups immaterial (<1–2% of net revenue) and netting out over time rather than always favourable. | Reported US net revenue is a management estimate. Under-accruing rebates and chargebacks flatters revenue and gross margin with almost no immediate detectability, then reverses years later as an "exceptional" charge. Disclosure sits in the 10-K/20-F or the US subsidiary accounts — not in Indian standalone results. Go looking for it. |
| **Cash runway vs net operating burn** (clinical-stage biotech) | (cash + equivalents + short-term marketable securities − near-term debt) ÷ average quarterly net cash used in operations, in months; mapped against the next value-inflecting readout and the next financing need. List committed milestone receipts, undrawn facilities and any ATM shelf separately. | >24 months comfortable; 18–24 adequate; <12 means a dilutive raise or distressed partnership is imminent almost regardless of the science. Guidance should fund *past* the next Phase II/III readout, not into it. | P/E, ROCE, D/E and FCF are undefined here; runway versus catalyst timing is the actual solvency model. A company forced to finance before a readout raises on the market's terms and dilutes holders at the worst possible price. Runway also determines management's negotiating leverage in any licensing deal. |
| **Risk-adjusted pipeline and catalyst calendar** | Assets by phase, indication, modality and mechanism novelty, weighted by historical probability of success; dated catalysts (interim analyses, topline readouts, PDUFA/EMA/CDSCO decisions, partnering deadlines); bottom-up peak sales = eligible population × diagnosis rate × treatment rate × realistic net price after GTN × penetration × duration of therapy. | Base rates: Phase I to approval ~7–10% (oncology ~5–6%, rare/haematology 15–25%); Phase II→III ~30% (the real filter); Phase III→filing ~55–60%; filed→approved ~85–90%. Premium for validated mechanisms; discount for first-in-class novel targets. | This *is* the balance sheet for a biotech and none of it is capitalised. Two companies with identical financial statements can differ tenfold in value purely on phase mix, mechanism validation and catalyst proximity. A single-asset, single-mechanism company is a binary instrument, not a compounding business — size and value it as such. |
| **Occupancy, ARPOB and ALOS** (hospitals — read as a triangle) | Occupancy = occupied bed-days / operational bed-days. ARPOB = average revenue per occupied bed per day. ALOS = average length of stay. Split mature units (>3–4 yrs) from ramping units, and by specialty. Diagnostics analogue: test volume growth, revenue per patient and per test, B2C vs B2B mix, same-store growth. | India mature units 65–75% occupancy (sustained >75% = capacity-constrained, capex due); blended chain 55–70%. Metro ARPOB broadly Rs 45,000–80,000/day growing 6–10%. ALOS ~3–4 days and structurally falling. US: occupancy 60–70%, revenue per adjusted admission in place of ARPOB. | Hospital revenue is arithmetically beds × occupancy × ARPOB × 365 — no income-statement ratio explains a hospital; these three do. They also trade off: falling ALOS raises throughput and ARPOB while mechanically depressing occupancy, so a genuinely improving chain can look stagnant on occupancy alone. Rising ARPOB from case-mix upgrade (oncology, cardiac, neuro, transplants) is high quality; rising ARPOB with falling footfalls is price-led and fragile. |
| **Mature-unit margin, capex per bed, new-unit breakeven** | EBITDA margin split mature vs ramping; capex per bed for greenfield vs brownfield vs asset-light O&M/lease; months from commissioning to EBITDA breakeven, to PAT breakeven, to target ROCE. State everything consistently pre- or post-Ind AS 116/IFRS 16. | India mature units 22–30% EBITDA margin, blended chain 18–24%. Greenfield ~Rs 0.8–1.5 crore/bed in metros, Rs 0.4–0.7 crore brownfield; EBITDA breakeven 12–24 months; mature ROCE >15–18% by year 4–5. Asset-light O&M carries lower margin but far higher ROCE — compare on ROCE, not margin. | A chain in expansion always shows depressed consolidated margins, negative FCF and weak ROCE, which tells you nothing either way. Mature-unit economics and the shape of the ramp curve decide whether the capex compounds or destroys capital. **A lengthening breakeven period across successive cohorts is the earliest reliable sign of over-expansion.** |
| **Payer mix and days in AR** | Revenue by cash/self-pay, private insurance/TPA, corporate/PSU, and government schemes (PM-JAY, CGHS, ECHS, state schemes in India; Medicare, Medicaid, commercial in the US); DSO/days in AR; disallowance rate; bad-debt / uncompensated-care provision. | India: DSO 40–70 days healthy; scheme-heavy chains run 90+. Scheme tariffs typically realise 15–35% below cash/insurance rates. US: days in AR 40–55; commercial mix drives margin; watch bad debt and charity care as separate lines. | Two hospitals with identical occupancy can have completely different profitability and cash conversion purely on payer mix. Filling beds with low-tariff scheme volume flatters occupancy and revenue growth while diluting ARPOB, stretching receivables and consuming working capital — a very common way a growing provider quietly stops generating cash. Payer concentration also creates tariff-negotiation risk no leverage ratio captures. |
| **Field-force productivity and therapy mix** (India branded formulations) | Revenue per medical representative (MR) per month; MR headcount growth vs domestic sales growth; chronic vs acute mix; top-10 brand contribution; secondary (IQVIA/AWACS retail offtake) growth vs primary (billing) growth; % of domestic portfolio under DPCO/NLEM. | Rs 5–9 lakh revenue per MR per month for efficient players (top quartile higher); chronic mix >45–50% preferred; NLEM exposure ideally <20% of domestic sales; secondary growth tracking primary within ~200bps over four quarters. | Domestic branded formulations are the highest-quality, highest-multiple, most annuity-like part of an Indian pharma company — prescriber loyalty, not patents, is the moat. Primary persistently outrunning secondary means the channel is being stuffed and a correction quarter is coming. Chronic therapies (cardiac, diabetes, CNS, respiratory) compound with patient longevity; acute is seasonal and switch-prone. NLEM exposure caps pricing power by regulation regardless of competitive position. |
| **CDMO capacity, utilisation and molecule-stage mix** | Installed reaction/fermentation capacity (KL or litres); utilisation %; revenue share from commercial-stage vs clinical-stage molecules; innovator vs generic customers; top-5 customer concentration; disclosed order book or committed capacity; raw-material pass-through terms. | Utilisation 70–85% (sustained >85% means expansion capex is overdue); commercial-molecule share >50% for stability; top customer <20–25% of revenue; order book covering >1x NTM revenue. | CDMO earnings look erratic on a P/E view because one molecule's phase transition, a customer's clinical failure, or a single destocking cycle moves revenue sharply. Margins cannot explain that volatility; stage mix and utilisation can. Capex must lead revenue by 2–3 years, so a weak FCF year is often the setup for the next growth phase. Concentration risk here is far more dangerous than leverage. |
| **Working capital cycle and cash conversion** | Inventory days split RM/WIP/FG; receivable days by geography; payable days; core NWC as % of sales; CFO/EBITDA; FCF after separating maintenance from growth capex. | Pharma inventory 90–150 days is structurally normal. Receivables 60–90 days in emerging markets, 60–100 in the US given buying-consortium terms. Core NWC 25–40% of sales. CFO/EBITDA sustained >70%; providers and diagnostics >85% given negative working capital. | Working capital is where channel stuffing, disputed emerging-market receivables and expiring inventory hide. Inventory risk here is unusually severe: product becomes worthless at expiry or the day a competitor launches, and provisioning policy is discretionary. **A widening EBITDA-to-CFO gap sustained over four to six quarters is the most reliable early warning that reported profits are not real.** |
| **Earnings-quality bridge: reported → core** | Full reconciliation: amortisation of acquired intangibles, IPR&D impairment, litigation/settlement charges, remediation, restructuring, upfront and milestone licensing income, forex and treasury "other income", PLI and export incentives, and any development cost capitalised under Ind AS 38 / IAS 38. | Acquired-intangible amortisation of 5–15% of revenue is normal for acquisitive pharma and legitimately added back if disclosed consistently. Capitalised development cost near zero, or clearly disclosed with amortisation starting at launch. Other income a small single-digit % of PBT. **Any "exceptional" appearing three years running is an operating cost.** | Reported P/E is nearly meaningless for acquisitive pharma, so the market uses core EPS — and that same adjustment mechanism is the sector's primary earnings-management lever. Your job is to decide which add-backs reflect genuine non-cash purchase accounting and which are recurring costs relabelled. A rising "intangibles under development" balance with no launches is a direct quality-of-earnings hit. |

---

## How to value companies in this sector

There is no single method. **The sub-sector dictates the tool**, and using the wrong one produces confident nonsense.

### Clinical-stage biotech (no product revenue)
Risk-adjusted NPV (rNPV/eNPV), built asset by asset. For each programme: bottom-up epidemiology peak sales, net of gross-to-net, × cumulative probability of success from the current phase, discounted at 10–14% (higher for single-asset or first-in-class), with the patent/exclusivity cliff modelled explicitly and revenue collapsing to near zero after LOE — **no perpetuity**. Sum the assets, subtract PV of unallocated G&A and expected future financing dilution, add net cash. Cross-checks used in practice: EV/cash (to find negative-EV situations), EV per programme, price-to-risk-adjusted-peak-sales (0.5–2x), and comparable licensing-deal economics (upfront + milestones + royalty %). **Do not use** P/E, EV/EBITDA, P/B, or a DCF with terminal growth — all are inapplicable.

### Commercial innovator pharma
P/E on core EPS (adding back acquired-intangible amortisation), EV/EBITDA, and a DCF that models the in-line portfolio to LOE *plus* a separately risk-adjusted pipeline — effectively a sum-of-the-parts of a melting ice cube plus an option. Terminal growth must be low (0–2%) because patents expire; this is precisely why large-cap pharma structurally trades at a discount to other high-margin businesses, and mistaking that discount for cheapness is a classic error. Developed-market ranges have historically run ~10–16x core EPS and ~8–13x EV/EBITDA, with the multiple driven almost entirely by 5-year LOE exposure and pipeline depth. US IRA Medicare price negotiation and EU international reference pricing now sit inside the terminal-value assumption, not outside it.

### Generics and Indian pharma
Consolidated P/E remains the headline convention (quality Indian names have historically traded ~22–35x forward core EPS, mid-caps 15–22x), but the real work is a **sum-of-the-parts by segment**, because segments deserve very different multiples. Indicative, historical, and cycle-dependent:

| Segment | Indicative EV/EBITDA | Why |
|---|---|---|
| India branded formulations | 25–35x | Annuity-like, prescriber moat, price/mix pricing power |
| CDMO / CRAMS | 20–35x | Long contracts, high switching costs, innovator stickiness |
| Complex generics / specialty | 15–25x | Limited competition, defensible for years |
| API | 10–15x | Cyclical, China-price exposed, commoditising |
| Emerging markets / RoW | 10–15x | Fragmented, FX-exposed, distributor-dependent |
| US plain generics | 7–12x | Price-erosion treadmill, binary FDA risk, 3-consortium buyer power |

Always strip one-off exclusivity profits out of the base before applying any multiple, and haircut or separately value plants under regulatory action. Prefer EV/EBITDA over P/E where acquisition amortisation is large. P/B and dividend yield are close to useless.

### Hospitals and providers
EV/EBITDA is primary, stated consistently pre- or post-Ind AS 116/IFRS 16. Historically the convention was **EV/EBITDAR** (rent-adjusted) precisely so owned-property and leased operators could be compared — that logic still applies, so restate to a rent-inclusive basis before comparing an asset-light operator to an owner. Because ramping units depress consolidated numbers, the more accurate approach is a unit-level DCF or a two-part valuation: mature units on a full multiple, plus new units carried at or below invested capital until they cross breakeven. Cross-checks: EV per operational bed, EV per *mature* bed, and replacement cost (which also captures the land, licence and clinical-talent barrier to entry). Indian listed chains have traded roughly 18–30x EV/EBITDA (premium names higher); large US for-profit operators far lower, ~7–10x — reflecting payer-mix and reimbursement risk, not lower quality. **P/E is poor here** because heavy depreciation on new units distorts it for years. Diagnostics chains: EV/EBITDA (India historically 25–40x, compressing as competition and online-aggregator pricing intensify), supported by same-store growth and revenue per patient. Healthcare real estate in REIT structures: FFO/AFFO and cap rates, never EBITDA multiples.

### Cross-cutting rules
- Capitalise compliance risk explicitly: a plant under warning letter should be valued at a discount or excluded from the base entirely.
- Treat regulated-price exposure (DPCO/NLEM in India, IRA and reference pricing abroad) as a **permanent margin cap**, not a cyclical headwind.
- Never apply a peak-cycle multiple to peak-exclusivity earnings — that error compounds two mistakes in the same number.
- For a mixed group, valuing on consolidated EBITDA alone will systematically misprice it; the segment mix *is* the valuation.

---

## Peer set construction

A valid comparable shares **business model, end-market regulator, and stage of capex cycle** — not merely the word "pharma".

Splits that must never be mixed in one peer set:
- **Innovator vs generic vs API vs CDMO vs provider.** Different revenue durability, different capital intensity, different multiples. A CDMO compared to a generics maker on EV/EBITDA is meaningless.
- **US-exposed vs India-domestic-only.** FDA binary risk, price erosion and litigation exposure are present in one and absent in the other. A domestic-branded pure play deserves a structurally higher multiple.
- **Clinical-stage vs commercial biotech.** Once there is product revenue, the entire valuation framework changes.
- **Owned-real-estate vs leased vs O&M hospitals.** Compare only on EBITDAR and ROCE, never on EBITDA margin or D/E.
- **Mature-network vs expansion-phase providers.** A chain with 80% mature beds and one with 40% are at different points on the same curve; compare mature-unit metrics, not consolidated ones.
- **B2C vs B2B diagnostics.** B2B/reference-lab revenue carries lower margin and worse receivables; a blended margin comparison is misleading.
- **Acquisitive vs organic pharma.** Any ROCE, ROE or reported-EPS comparison across this line is invalid without normalising for goodwill and acquired-intangible amortisation.

Also normalise for: R&D intensity (or restate margins at a common R&D%), one-off exclusivity contribution in the base year, IFRS 16 treatment, and geographic revenue mix. Peer sets here are usually small — three to six genuine comparables beats fifteen loosely related tickers, and where no clean peer exists, the company's own 5–10 year history becomes the primary benchmark.

---

## Sector-specific red flags

**Regulatory and compliance**
- Any open USFDA warning letter, OAI classification, import alert or consent decree — and specifically 483 observations citing data integrity (deleted or re-run chromatograms, unofficial "trial" testing, shredded records, shared logins). Data-integrity findings signal culture, not process, and take years to clear.
- Management downplaying or delaying disclosure of an inspection outcome, or describing an OAI as "procedural". Cross-check the FDA's own inspection classification database, not the press release.
- Segment or operational disclosure *deteriorating*: geography detail withdrawn, ARPOB or occupancy no longer reported, ANDA filing counts dropped. Reduced disclosure almost always precedes bad numbers in this sector.

**Growth quality**
- Growth built on a one-time exclusivity (a Para IV 180-day window, a competitor's supply failure) presented or modelled as the new base — and the multiple applied to that inflated EBITDA.
- Reported revenue growing while base price erosion accelerates, i.e. an ever-larger share of revenue from launches. A launch treadmill needs a bigger launch every year just to stand still.
- Licensing upfronts and milestones recognised as revenue and left inside the growth narrative, creating a base that cannot repeat.
- Customer concentration in US generics: three buying consortia control roughly 90% of US generic purchasing, so a contract loss is a step-change, not a gradual decline. Similarly a CDMO with one innovator customer above ~25% of revenue.

**Accounting and earnings quality**
- R&D intensity falling for two or more consecutive years while OPM expands, especially at a US-generics-dependent company. That is margin harvested from the future.
- Rising "intangible assets under development" or capitalised development cost under Ind AS 38 / IAS 38 with no corresponding launches — legal, disclosed, and a direct transfer of expense from P&L to balance sheet.
- Inventory days and receivable days rising faster than sales, particularly in the US or in emerging-market distributor businesses — the classic channel-stuffing signature. In India, compare primary billing growth with IQVIA/AWACS secondary offtake.
- CFO/EBITDA persistently below ~60–70%, or a widening EBITDA-to-cash gap sustained four-plus quarters despite clean reported profits.
- Favourable prior-period gross-to-net or rebate accrual reversals boosting current revenue; or a shrinking rebate/chargeback accrual relative to gross sales. Under-accrual is the most detection-resistant revenue inflator in US pharma.
- "Adjusted EBITDA" or "core EPS" excluding the same categories every year — litigation, remediation, restructuring, impairment.
- Heavy dependence on "other income" (forex, treasury, export/PLI incentives) to hit PBT; unhedged or undisclosed forex debt and derivative positions at exporters.

**Governance and legal**
- Large or growing off-balance-sheet contingencies: opioid, talc, antitrust/price-fixing, product liability, DOJ False Claims Act and upcoding investigations, state AG actions. Read the contingencies note *before* the ratios.
- Related-party structures: promoter-owned distribution, marketing or C&F entities; sale-and-leaseback of hospital property into promoter vehicles; low-substance overseas subsidiaries; unexplained loans and advances to related entities.
- Auditor resignation or qualification, delayed filings, restatement, repeated CFO or company-secretary churn, or a change in the group's US subsidiary auditor. In this sector these have repeatedly preceded regulatory and accounting blow-ups.

**Biotech-specific**
- Undisclosed pipeline pruning (assets quietly vanishing from the corporate deck), mid-trial changes to the primary endpoint or statistical analysis plan, claims built on open-label or single-arm data with cross-trial comparisons, subgroup-rescue after a missed primary, and insider selling or a 10b5-1 plan initiated shortly before a readout.
- Financing distress signals: an active ATM programme, going-concern qualification, reverse stock split, royalty-monetisation or revenue-interest financing (economically debt, not always presented as such), and runway ending before the next catalyst.

**Provider-specific**
- Occupancy improving only on low-tariff government-scheme volume, with flat or falling ARPOB and lengthening receivables. Also gross-billing revenue recognition before discounts and disallowances, and under-provisioning for scheme disallowances and bad debt.
- Departure of high-revenue consultants or a whole specialty team — the asset walks out of the building, and it shows up in ARPOB and case mix two to three quarters later. Rising doctor payout as % of revenue signals loss of bargaining power.
- Aggressive capitalisation of pre-operative and pre-commissioning expenses; lengthening breakeven across successive new-unit cohorts; owned, leased and O&M units blended into one margin without disclosure.

---

## Cycle and structural context

**Pharma is not economically cyclical, but it is intensely *policy* and *product* cyclical.** Demand is inelastic — volumes barely move with GDP — so the cycles that matter are: the patent cycle (LOE waves), the US generic pricing cycle (consolidation of buying consortia in the mid-2010s triggered a multi-year erosion shock from which the industry never fully recovered), the API cycle (China supply and pricing, plus the post-2020 destocking and restocking swings), and the CDMO cycle (biotech funding → clinical activity → order books, with a 2–3 year lag).

**Where to check you are in the cycle:** US price erosion running better than −5% is usually a shortage-driven upswing that will normalise; API prices near cycle highs invite Chinese capacity back; CDMO order books track biotech funding two years earlier — a funding winter shows up in CDMO revenue with a delay, so a strong current order book from a weak funding period is worth interrogating.

**Structural threats to underwrite explicitly:**
- **US IRA Medicare price negotiation** and the small-molecule/biologic timing asymmetry — a permanent margin and terminal-value issue for innovators, and a change to the economics of which modalities get funded.
- **Biosimilars** eroding the historically safest innovator revenue, and interchangeability rules accelerating substitution.
- **China+1 and PLI** re-shoring API and key starting material capacity to India — a genuine multi-year tailwind for Indian API and CDMO, but one that also invites capacity oversupply.
- **GLP-1s** reallocating an enormous share of global pharma spend and, over time, plausibly reducing volumes in adjacent chronic categories (cardiac, diabetes complications, some orthopaedics and bariatrics) — model second-order effects, not just direct participation.
- **Payer consolidation and PBM reform** in the US; **PM-JAY expansion and tariff-setting** in India, which raises volume while capping realisation.
- **Diagnostics disruption**: online aggregators and hospital-captive labs compressing pricing in a business that historically enjoyed 25–30% margins.
- **Regulatory tightening**: revised Schedule M and stricter CDSCO enforcement in India raising the compliance-capex floor for smaller manufacturers, which consolidates the industry toward larger players.

**Provider structural context:** the constraint is beds, clinicians and land, not demand. Insurance penetration, medical tourism and case-mix upgrade drive the long-run compounding; the binding risks are tariff regulation (scheme rates, any price capping on procedures, stent and knee-implant style price caps recurring), clinician cost inflation, and over-expansion into low-density micro-markets.

---

## India vs global notes

| Dimension | India (NSE/BSE, Ind-AS) | US / global (10-K, 20-F, GAAP/IFRS) |
|---|---|---|
| Primary filings | Annual report, quarterly results, investor presentation, **earnings concall transcript** (often the only place ARPOB, occupancy, ANDA filings, price erosion and segment splits are disclosed), stock-exchange announcements | 10-K / 10-Q / 8-K / 20-F on **EDGAR**; proxy (DEF 14A); segment and product-level revenue disclosure is mandated and far richer |
| Units | Rs crore / lakh; convert consistently — 1 crore = 10 million | USD millions |
| R&D disclosure | Often a single P&L line; the innovative/ANDA split usually only appears in the concall or presentation. Development-cost capitalisation permitted under Ind AS 38 — always check "intangibles under development" | ASC 730 mandates expensing; disclosure by programme is voluntary but common for innovators |
| Regulator (product) | CDSCO, DCGI; state FDAs for licensing; revised Schedule M for GMP | USFDA (CDER/CBER), EMA, MHRA, PMDA; **the FDA inspection classification database and warning-letter list are public — use them** |
| Price control | **DPCO / NLEM**: ceiling prices on scheduled formulations, annual WPI-linked revision; NPPA enforcement and retrospective demands | IRA Medicare negotiation, 340B, Medicaid rebates, EU international reference pricing |
| Ownership | **Promoter holding** and pledge disclosure are central; check pledge %, promoter entities in the distribution chain, and inter-corporate deposits | Institutional and insider ownership; Form 4 insider transactions and 10b5-1 plans are highly informative pre-catalyst |
| Audit and governance | **CARO** reporting (related-party transactions, loans and advances, statutory dues, inventory verification), auditor's report qualifications, SEBI LODR related-party approvals | SOX 404 internal-control opinion, critical audit matters, audit-committee independence |
| Provider metrics | ARPOB, occupancy, ALOS, bed count, doctor payout %, payer mix including PM-JAY/CGHS/ECHS | Revenue per adjusted admission, adjusted admissions, case mix index, same-facility volumes, bad debt and charity care as separate lines |
| Domestic sales tracking | **IQVIA / AWACS secondary sales data** — independent check on primary billing; no equivalent is normally needed elsewhere | IQVIA scripts (TRx/NRx) for branded products; channel data via distributors |
| Leases | Ind AS 116 (aligned to IFRS 16) since FY20 — pre-FY20 EBITDA is not comparable to post | IFRS 16 / ASC 842; US GAAP retains an operating-lease split, so US EBITDA is *not* directly comparable to IFRS 16 EBITDA for lease-heavy operators |
| Typical multiples | Structurally higher than global peers for domestic-branded and CDMO franchises; whole sector re-rates and de-rates on FDA news flow | Lower headline multiples for both innovators (patent cliff) and providers (payer risk) |

Two India-specific traps worth naming: **standalone vs consolidated** — the US business usually sits in overseas subsidiaries, so standalone numbers can look pristine while consolidated tells the real story (and the GTN accruals only exist in the subsidiary accounts); and **"other income"** from export incentives, PLI and forex, which in some years is a large share of PBT and is not operating profit.

---

## Checklist

- [ ] Classify the sub-sector first (innovator / generic / API / CDMO / clinical-stage biotech / hospital / diagnostics) and pick the metric and valuation frame accordingly.
- [ ] Pull the FDA inspection classification and warning-letter databases yourself for every manufacturing site; map each affected site to % of revenue, % of EBITDA and % of pending ANDAs.
- [ ] Separate data-integrity 483 observations from procedural ones; treat the former as a culture problem measured in years.
- [ ] Compute R&D intensity by type and its 5-year trend before looking at OPM; flag any margin expansion accompanied by falling R&D.
- [ ] Rebuild the revenue bridge: base price erosion + base volume + launches + exclusivities + FX + M&A, by geography.
- [ ] Strip one-off exclusivity and licensing-milestone profits out of the earnings base before applying any multiple.
- [ ] Check top-product and top-5 concentration on **EBITDA**, not just revenue; quantify 1/3/5-year LOE exposure.
- [ ] For US-facing names, find gross-to-net deductions and the accrual trend in the 10-K/20-F or subsidiary accounts; check prior-period true-ups.
- [ ] Reconcile reported EPS to core EPS line by line; reclassify any "exceptional" recurring three years running as an operating cost.
- [ ] Check "intangible assets under development" and capitalised development cost against actual launches.
- [ ] Compare CFO/EBITDA and the EBITDA-to-cash gap over 4–8 quarters; split maintenance from growth capex before judging FCF.
- [ ] India domestic: compare primary billing growth with IQVIA/AWACS secondary offtake; check chronic mix, revenue per MR, NLEM exposure.
- [ ] Biotech: compute months of runway vs the next catalyst date; check for ATM, going-concern language, royalty financing and pipeline assets that quietly disappeared.
- [ ] Biotech: build PoS-weighted eNPV asset by asset with an explicit LOE cliff and no perpetuity; add expected financing dilution.
- [ ] Hospitals: read occupancy, ARPOB and ALOS together; split mature from ramping units; check payer mix, DSO and disallowance provisioning.
- [ ] Hospitals: track new-unit breakeven period across successive cohorts; restate to EBITDAR before comparing owned, leased and O&M operators.
- [ ] CDMO: check utilisation, commercial vs clinical molecule mix, top-5 customer concentration and order-book coverage.
- [ ] Build a sum-of-the-parts by segment rather than valuing consolidated EBITDA on one multiple; discount or exclude plants under regulatory action.
- [ ] Read the contingencies note, CARO observations and related-party disclosures before finalising any view.
- [ ] Verify the peer set shares business model, end-market regulator and capex-cycle stage; where no clean peer exists, benchmark against the company's own 5–10 year history.
