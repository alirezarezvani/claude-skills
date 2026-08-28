# Management and Corporate Governance

Use this when: you are running the Stage 3 red-flag screen or the governance block of Stage 4, or any time the controlling shareholder, the board or the auditor could be the reason the numbers look the way they do.

Governance is not a soft, optional overlay on the financial analysis — it is the question of whether the financial analysis belongs to you. Every ratio you compute downstream assumes two things: that the reported figures describe reality (the forensic question, `references/07-forensic-red-flags.md`), and that the economics they describe accrue to the security you are considering buying (the governance question, this file). A business can compound beautifully and still deliver nothing to minorities, because the cash was routed to a promoter entity, the earnings were diluted away at a discount, the voting shares are held by someone else, or the listed vehicle only holds contractual claims on assets it does not own. The skill's governing principle applies here too: governance norms are sector- and market-relative. A 60% family stake is a red flag in a US large cap and the default condition in Indian mid-caps; an externally managed REIT has a fee-conflict problem that simply does not exist for an operating company; a bank's "capital allocation" is underwriting, not capex.

## Contents

- [0. How to run this dimension](#0-how-to-run-this-dimension)
- [1. What does the security actually confer? Share class, DVR, ADR/GDR, VIE](#1-what-does-the-security-actually-confer-share-class-dvr-adrgdr-vie)
- [2. Capital allocation: build the deployment ledger](#2-capital-allocation-build-the-deployment-ledger)
- [3. Guidance versus delivery: tabulate it, do not characterise it](#3-guidance-versus-delivery-tabulate-it-do-not-characterise-it)
- [4. Promoter / insider holding: level, trend and mechanism](#4-promoter--insider-holding-level-trend-and-mechanism)
- [5. Share pledging and encumbrance (India-critical)](#5-share-pledging-and-encumbrance-india-critical)
- [6. Insider transactions: read them one trade at a time](#6-insider-transactions-read-them-one-trade-at-a-time)
- [7. Related-party transactions and tunnelling](#7-related-party-transactions-and-tunnelling)
- [8. Group structure complexity and holdco opacity](#8-group-structure-complexity-and-holdco-opacity)
- [9. Capital raising, dilution and financing behaviour](#9-capital-raising-dilution-and-financing-behaviour)
- [10. Executive compensation and alignment](#10-executive-compensation-and-alignment)
- [11. Board independence, composition and functioning](#11-board-independence-composition-and-functioning)
- [12. Auditor: quality, tenure, fees, resignations](#12-auditor-quality-tenure-fees-resignations)
- [13. CFO and finance-team turnover](#13-cfo-and-finance-team-turnover)
- [14. Minority-shareholder rights architecture](#14-minority-shareholder-rights-architecture)
- [15. Succession and key-man risk](#15-succession-and-key-man-risk)
- [16. Integrity, regulatory history and disclosure quality](#16-integrity-regulatory-history-and-disclosure-quality)
- [17. Sector translation: where these checks change or invert](#17-sector-translation-where-these-checks-change-or-invert)
- [18. Scoring, weighting and how to write it up](#18-scoring-weighting-and-how-to-write-it-up)
- [Checklist](#checklist)

---

## 0. How to run this dimension

Three rules before you start.

**Governance is a multiplier and a gate, not an additive score line.** Good governance does not add much to the case for a mediocre business. Bad governance subtracts from everything — it widens the discount rate, caps the multiple you can justify, and in the severe cases it invalidates the analysis entirely rather than costing it a few points. Treat a small number of findings as hard kill criteria (Section 18), and treat the rest as an adjustment to the required margin of safety.

**Separate structure from behaviour.** Structure is what the documents permit: share classes, board composition, RPT approval thresholds, group tree. Behaviour is what the controller has actually done with that latitude over a decade. A concentrated, founder-controlled structure with a decade of clean behaviour is usually a better holding than a textbook-compliant structure run by someone with a record. Score both, and never let a compliance checklist substitute for the track record.

**Everything here is evidence-based or it is not written.** Governance is where an analyst is most tempted to editorialise. Every claim you make must trace to a specific filing, disclosure, vote, transaction or dated statement. "Management seems promoter-friendly" is worthless; "royalty to the parent rose from 1.8% to 3.5% of sales over four years while EBITDA margin fell 200bp, disclosed in Note 41" is a finding.

**Where to look.**

| Item | India (NSE/BSE, Companies Act 2013, SEBI LODR) | US / global (SEC EDGAR) |
|---|---|---|
| Ownership and its trend | Shareholding pattern filed quarterly under LODR Reg 31 (within 21 days of quarter-end); BSE/NSE corporate-announcements pages | DEF 14A beneficial-ownership table; SC 13D/13G and their amendments |
| Insider trades | SEBI PIT Reg 7(2) disclosures (trades above ₹10 lakh in a quarter, filed within 2 trading days); SAST Reg 29 for substantial acquisitions | Forms 3, 4 (within 2 business days) and 5 |
| Pledges | SAST Reg 31 encumbrance disclosures; shareholding-pattern pledge table | Rarely disclosed; look in 13D Item 6, margin-loan disclosures and proxy pledging policy |
| Related parties | Notes to accounts (Ind-AS 24); LODR Reg 23 RPT policy; half-yearly RPT disclosures to exchanges | Notes (ASC 850 / IAS 24); proxy "Certain Relationships and Related Transactions" |
| Board and pay | Corporate Governance Report in the annual report; Reg 27 quarterly CG report; MGT-7 | DEF 14A in full, including CD&A, pay ratio, pay-versus-performance table |
| Auditor | Auditor's report, CARO 2020 annexure, ICFR opinion under s.143(3)(i), Form ADT-3 on resignation, NFRA orders | Audit report, Item 9A (ICFR), 8-K Items 4.01 (auditor change) and 4.02 (non-reliance), PCAOB Form AP and inspection reports |
| Track record | 10 years of annual reports, MD&A, concall transcripts (LODR Reg 46 requires transcripts within 5 working days), analyst-meet decks | 10-K MD&A, earnings-call transcripts, investor-day decks, 8-K guidance releases |
| Integrity record | SEBI orders and adjudications, NCLT/NCLAT, SFIO, income-tax search reports, IiAS / SES / InGovern proxy notes | SEC litigation releases and AAERs, DOJ, class-action dockets, ISS / Glass Lewis reports |

For foreign private issuers filing 20-F, note that the proxy rules do not apply, there is no DEF 14A, compensation may be disclosed only in aggregate, and the company may elect home-country governance practice in place of NYSE/Nasdaq standards (disclosed in Item 16G). The absence of disclosure is not the absence of a problem — say so explicitly rather than scoring the gap as neutral.

---

## 1. What does the security actually confer? Share class, DVR, ADR/GDR, VIE

Do this first, before any other governance work, because it can change the identity of the thing you are analysing. Establish, in one paragraph: which legal entity you would own a claim on, what fraction of votes and of economics that claim carries, and by what legal mechanism the operating profits reach it.

**Dual-class and superior voting rights.** Compute the wedge: voting share minus economic share. A founder holding 12% of economics and 60% of votes has a 48-point wedge, and every minority-protection mechanism downstream (say-on-pay, director elections, majority-of-minority votes) is decorative. Check for a sunset provision — time-based, ownership-based, or transfer/death-triggered — and its date. India: SEBI's 2019 framework permits superior-voting-rights (SR) shares for founders of intensive-technology companies at IPO, with a sunset (5 years, extendable once by shareholder resolution) and coat-tail provisions that collapse SR to ordinary voting on specified resolutions. US: no sunset is required by law, so read the charter.

**DVR (India).** Differential-voting-rights shares in India have historically carried *fewer* votes plus a higher dividend, and they have persistently traded at a large discount to the ordinary share — a discount driven by low liquidity and index exclusion as much as by the voting differential. If you are analysing a DVR line, value it separately: apply the company analysis to the business but the pricing to the specific security, and state the historical discount range and whether any conversion or cancellation scheme is pending. Never quote the ordinary-share multiple as though it applied to the DVR.

**ADR / GDR.** Determine sponsored versus unsponsored; the ratio of ADS to underlying share; the depositary's fees (custody pass-through, typically deducted from dividends); whether the ADR holder can vote and by what instruction mechanism (many depositaries vote uninstructed shares with management); fungibility and whether the ADR can be converted to local shares; and the withholding-tax treatment of the dividend. An ADR premium or discount to the local line, adjusted for the ratio and FX, is a real fact about capital-flow restrictions, not an arbitrage you can assume away.

**VIE and contractual control.** For China-domiciled ADRs and structurally similar EM listings, the listed Cayman holdco frequently does *not* own the operating company. It owns a wholly foreign-owned enterprise (WFOE) that holds a bundle of contracts — exclusive service agreements, equity pledges, powers of attorney — over an onshore entity owned by founders, engineered to satisfy foreign-ownership restrictions in licensed sectors. Establish: whether the operating licences, IP and cash sit inside or outside the consolidated legal perimeter; whether those contracts have ever been tested and enforced in the local courts; the legal route by which onshore cash is upstreamed as dividends and whether capital controls or tax gross-ups impede it; and audit-inspection access (PCAOB inspection status and HFCAA delisting exposure). If the answer is "profitable operating company, contractual claim only, unenforced in court, restricted upstreaming," you are not buying the earnings — you are buying a promise to route the earnings, and that belongs at the top of the risk section, not in a footnote. The same test applies in miniature anywhere the listed entity is a thin holdco whose value resides in entities it does not fully control (Section 8).

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Voting/economic wedge | Insider voting % − insider economic % | 0; any wedge above ~10pts needs explicit justification | Measures how much control has been bought without proportionate capital at risk |
| Sunset horizon | Years until superior votes collapse to one-share-one-vote | Defined and dated | An undated wedge is permanent entrenchment |
| DVR discount (India) | (Ordinary price − DVR price) ÷ ordinary price, vs its own 5-year range | Judge against own history only | Establishes whether the discount is normal or a signal |
| ADR ratio and fees | ADS-to-share ratio; depositary fee per ADS per year | Fees small relative to yield | Silently reduces realised income and distorts naive per-share comparisons |
| Consolidated-perimeter test | % of revenue/profit consolidated via contracts rather than equity | 0% for a straightforward company | Contractual consolidation means legal title to earnings is untested |

Indicative ranges throughout this file vary by market, cycle and period. Peer comparison and the company's own history override every absolute band.

---

## 2. Capital allocation: build the deployment ledger

Over a decade, capital allocation is the largest single driver of per-share value, and it is the most persistent, most predictive management trait you can observe. Do not assess it with adjectives. Build a ledger.

**The method.** For the last 7–10 years, tabulate every source and use of capital, then attach a return to each use.

| Column | What goes in it |
|---|---|
| Year | Fiscal year of commitment |
| Source | Operating cash flow, debt raised, equity raised, asset sale |
| Use | Maintenance capex, growth capex, acquisition, buyback, dividend, debt repayment, cash build |
| Amount | In reporting currency (₹ crore for India; state units) |
| Promised return | What management said at announcement: IRR, payback, capacity, accretion, synergy — quote it with the date and source |
| Realised outcome | Incremental revenue/EBIT actually attributable, capacity actually commissioned, synergies actually visible in the segment numbers |
| Implied incremental ROIC | Incremental NOPAT ÷ capital deployed, once the asset is ramped |
| vs WACC | Spread in basis points |

**Incremental ROIC — compute it properly.** Aggregate ROIC is dominated by legacy assets and hides recent decisions. Use return on incremental invested capital, lagged for ramp:

- RoIIC = (NOPAT_t − NOPAT_{t−n}) ÷ (Invested capital_{t−1} − Invested capital_{t−n−1}), with n = 3 to 5 years, and invested capital lagged by at least a year because capital does not earn on the day it is spent.
- Compute it on a rolling basis and plot it. A business with 25% aggregate ROIC and 6% RoIIC is a good business being converted into a mediocre one; that fact is invisible in the headline ratio and is exactly the sort of single-metric error the skill's governing principle warns against.
- Sanity-check against the growth identity: sustainable growth ≈ reinvestment rate × incremental ROIC. If management guides to growth that this identity cannot produce at their historical incremental returns, either the returns must improve (why?) or the growth requires external capital (dilution — Section 9).
- Cross-check with the definitions and normalisation rules in `references/05-returns-and-dupont.md`; do not re-derive invested capital differently here.

**Acquisitions.** Track cumulative goodwill and acquired intangibles as a share of total assets, and every subsequent impairment. Impairment is the accounting system finally admitting that the price paid exceeded the value received — a recurring impairment pattern is a confession of serial overpayment, and you should read each one as a repayment of a prior year's reported earnings. For serial acquirers, also run the roll-up distortions in `references/07-forensic-red-flags.md`: acquired growth presented as organic, restructuring charges that never end, and purchase accounting that suppresses acquired-entity revenue then flatters subsequent growth.

**Buybacks.** A buyback is a capital allocation decision like any other and must be scored on price, not on existence. Compare the average repurchase price to your own intrinsic-value estimate for that year, or as a proxy to the multiple (P/E, EV/EBIT, P/B) at repurchase against the company's own 10-year range. Buying back stock in the top decile of the historical multiple, while simultaneously issuing cheap equity or options to insiders, is value transfer dressed as shareholder return. India-specific: buybacks may be by tender offer (with the mandated reservation for small shareholders) or open market, and the tax treatment changed materially in October 2024 — proceeds are now taxed in the shareholder's hands as deemed dividend rather than through the company-level buyback tax, which changed the buyback-versus-dividend calculus for Indian issuers. Do not apply pre-2024 payout logic to post-2024 decisions.

**Dividends and debt paydown** are the honest options and should be scored positively when the alternative uses earn below WACC. A company with sub-WACC incremental returns that keeps reinvesting is destroying value more surely than one that pays out.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| RoIIC (3–5y) | Δ NOPAT ÷ Δ invested capital, lagged | Above WACC, and not falling | The only measure of whether *recent* decisions created value |
| ROIC − WACC spread | Aggregate ROIC less WACC, 5-year trend | Positive and stable | Sub-WACC growth destroys value; see `06-valuation.md` for WACC derivation |
| Cumulative FCF vs cumulative capital raised | Σ FCF (10y) ÷ Σ (equity + net debt raised) | >1 for a self-funding business | Distinguishes a compounder from a capital sink |
| Goodwill + acquired intangibles / total assets | From balance sheet | Judge against acquisition strategy | High values make reported ROE flattering and impairment risk structural |
| Cumulative impairments / cumulative acquisition spend | Sum both over 10 years | Near zero | Direct measure of M&A overpayment |
| Buyback multiple percentile | Multiple paid at repurchase vs own 10-year range | Below median | Tests whether buybacks were opportunistic or price-insensitive |
| TSR vs sector over CEO tenure | Total return, CEO start to now, against sector index | Above sector | The bluntest available scorecard; use as a check, never alone |

---

## 3. Guidance versus delivery: tabulate it, do not characterise it

Credibility is measurable. Build a table of every *quantified* forward statement management has made over the last 3–5 years and mark it to actual.

| Date | Source | Statement | Horizon | Target | Actual | Variance |
|---|---|---|---|---|---|---|
| e.g. Q2 concall | Transcript | "capacity commissioned by Q4" | 2 quarters | Commissioning date | Actual date | Slip in quarters |

Include: revenue growth, margin targets, capex budgets, capacity commissioning dates, order-book conversion, debt-reduction targets, acquisition synergies, product launch dates, store/branch openings, and stated payout policy. Then compute a hit rate and a mean *signed* error, because the sign matters: chronic over-promising is a credibility failure that should widen your discount rate; chronic sandbagging is a different behaviour with different implications for how to read current guidance.

**Where guidance lives.** US issuers typically give formal guidance in the earnings release furnished on Form 8-K, repeated in the 10-Q/10-K MD&A. Indian issuers frequently give no formal guidance in filings at all, and the commitments live only in the concall — which is why LODR Reg 46 transcript availability (audio/video within 24 hours, transcript within 5 working days) matters so much for this exercise. Read the transcripts, not the summaries.

**What to do with it.** A management team with a documented history of missing its own targets by wide margins has forfeited the right to have its forward statements used as an input in your model. State that explicitly and haircut the forecast, or model only what the existing asset base can produce. Conversely, a team that has hit dated, specific, falsifiable targets across a downturn has earned some forecast credibility — and note that the willingness to make *falsifiable* statements at all is itself a governance signal. Vague, unfalsifiable strategy language ("we will drive shareholder value") is an evasion, not a target.

---

## 4. Promoter / insider holding: level, trend and mechanism

The trend matters more than the level, and the mechanism matters more than the trend.

**Read the mechanism, not just the delta.** A rising promoter stake means very different things depending on how it rose: open-market purchases with personal cash (strong positive), creeping acquisition within the SAST 5%-per-financial-year limit (positive), a preferential allotment of shares or warrants to the promoter at a formula price during a depressed market (self-dealing dressed as commitment — see Section 9), or a fall in the denominator via buyback (mechanical, no signal). A falling stake can be an ordinary estate-planning sale, a pledge invocation (Section 5), a dilution because the promoter did not participate in a raise, or an inter-se transfer within the promoter group that is not a sale at all.

**India specifics.** Read the LODR Reg 31 shareholding pattern for at least 8–12 quarters, and read the *promoter group* table, not just "promoter" — stakes routinely migrate between family members, family trusts and promoter-group companies. Minimum public shareholding is 25%, so a promoter above 75% has a forced-sale overhang. The SAST open-offer trigger is 25%, and creeping acquisition beyond that is capped at 5% per financial year. Watch for promoter *reclassification* requests, which remove a person from the promoter group and with it certain disclosure and lock-in obligations — always ask why. For recently listed companies, map the IPO lock-in expiry calendar for promoter and pre-IPO investor shares, plus any anchor-investor lock-in; a known supply cliff is a price risk independent of fundamentals.

**US specifics.** The proxy beneficial-ownership table is a point-in-time snapshot with its own record date; use SC 13D/13G (and their amendments) plus Form 4 history to build the trend. 13D signals an activist or control intent, 13G a passive position; a conversion from 13G to 13D is a material event. Note that beneficial ownership includes shares acquirable within 60 days, so option-heavy insiders look larger than their economic exposure.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Promoter / insider holding % | Latest shareholding pattern or proxy table | Sector- and market-relative; stability matters more than level | Skin in the game aligns the controller with minorities |
| 8–12 quarter trend | Absolute change in percentage points | Flat or rising | Persistent decline means the best-informed holders are reducing |
| Mechanism split | % of stake change from open market vs allotment vs dilution vs inter-se transfer | Open-market purchases dominant | Distinguishes conviction from self-allotment |
| Free float and institutional share | 100 − promoter %; DII/FII split and trend | Adequate float for liquidity | Low float distorts price discovery and raises impact cost |
| Beneficial-ownership opacity | % of promoter stake held via trusts, offshore vehicles or layered entities | Low and explained | Opaque holding chains obscure who actually controls and who is pledging |
| Lock-in / lock-up expiry (recent IPOs) | Date and volume of each tranche unlocking | Mapped in advance | Predictable supply shock |

---

## 5. Share pledging and encumbrance (India-critical)

This is the highest-yield India-specific governance check and has no close US equivalent, so run it on every Indian company and do not assume its absence elsewhere means it is irrelevant.

**What it is.** Promoters borrow personally against their shareholding. The pledge sits outside the company's balance sheet, so the company can look conservatively financed while the controlling family is highly levered against the same equity you are buying. Disclosure comes via SAST Reg 31 encumbrance filings and the pledge column of the quarterly shareholding pattern. "Encumbrance" is defined broadly in SEBI's framework and includes non-disposal undertakings and similar arrangements, not just formal pledges — read the encumbrance number, not only the pledge number.

**Why it is dangerous.** The exposure is reflexive. A price fall breaches the lender's loan-to-value threshold, triggering a margin call; if the promoter cannot post collateral, the lender invokes the pledge and sells into a falling market, which lowers the price, which triggers further calls. In the tail, the promoter loses control at the worst possible moment and the company acquires a distressed, motivated seller of its own stock. Before that point, a cash-strapped promoter has an acute incentive to move company cash toward personal obligations — which is why high pledging and rising related-party loans in the same year is one of the most reliable tunnelling signatures available (Section 7).

**How to run it.** Pull the pledge percentage for 8 quarters. Express it two ways — as a share of promoter holding and as a share of total shares outstanding, because the second is the actual float-supply risk. Overlay the share price. Rising pledge percentage into a falling price means either fresh borrowing or an invocation already under way, and both are urgent. Read the disclosed purpose; "for business purposes of the company" is materially different from an undisclosed personal use. Identify the lender: NBFCs and promoter-affiliated lenders extend against collateral that a bank would refuse, and a pledge financed by a related entity may be circular funding rather than a genuine external loan.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Pledged % of promoter holding | Pledged shares ÷ promoter shares | 0 is clean; sustained >25% warrants a discount; >50% is severe | Direct measure of promoter financial stress and forced-sale risk |
| Pledged % of shares outstanding | Pledged shares ÷ total shares | Low relative to average daily volume | Converts pledge risk into the float that could hit the market |
| Trend over 8 quarters | Percentage-point change | Falling | Rising pledges into a falling stock is the pre-invocation pattern |
| Implied LTV | Pledged value at current price ÷ disclosed loan, where available | Comfortable headroom | Estimates how far the price can fall before a call |
| Encumbrance minus pledge | Disclosed encumbrance % less formal pledge % | Zero or explained | Captures non-disposal undertakings and side arrangements |
| Invocation events | Count in last 3 years | Zero | An invocation already occurred means the cascade has started |

---

## 6. Insider transactions: read them one trade at a time

Aggregate net insider buying is a weak signal because it mixes signal with mechanics. Go to the transaction level.

**US — Form 4 transaction codes.** The code determines whether the trade carries any information at all:
- **P** — open-market purchase. The only strongly informative code. Real money, real decision.
- **S** — open-market sale. Informative only after you strip out pre-planned and mechanical sales.
- **A** — grant or award. No signal; it is compensation.
- **M** — option exercise. **F** — shares withheld for tax. A same-day M followed by S or F is a compensation event, not a view on value. Analysts who count these as "insider selling" manufacture false signals constantly.
- **G** — gift. **C** — conversion. Usually estate planning or instrument mechanics.

Check the footnotes for 10b5-1 plan status. Since the 2023 amendments, officer and director plans carry a cooling-off period (the later of 90 days or two business days after the next periodic report, capped at 120 days), overlapping plans are restricted, single-trade plans are limited to one per 12 months, and adoption/termination must be disclosed quarterly (Item 408 of Reg S-K). That gives you two things: a genuine distinction between mechanical and discretionary sales, and a new signal — a plan *adopted or terminated* at a suspicious moment. Also check Item 402(x) disclosure on option-grant timing relative to material non-public information; award dates clustering just before good news or just after bad news is a live governance flag.

**India — PIT and SAST.** SEBI (Prohibition of Insider Trading) Regulations require designated persons, promoters and directors to disclose trades exceeding ₹10 lakh in value in a calendar quarter within two trading days; these appear on the exchange websites. SAST Reg 29 requires disclosure on crossing 5% and on every 2% change thereafter. Additional India-specific checks: the trading-window closure around results (trades near the window edges deserve scrutiny), the contra-trade restriction (a designated person may not take an opposite trade within six months), the maintenance of a structured digital database of unpublished price-sensitive information, and whether the company has ever been the subject of a SEBI insider-trading proceeding.

**What actually carries information.**

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Cluster score | Number of distinct insiders making open-market purchases within a 90-day window | 3+ buyers is a meaningful cluster | Independent decisions by several insiders is far stronger than one large trade |
| Trade size vs holding | Value of purchase ÷ insider's existing holding, and ÷ annual cash compensation | Material (>10–20% of holding, or >1× salary) | A token purchase is a press release; a large one is a decision |
| Discretionary sale share | Sales not under a pre-set plan ÷ total sales | Low | Isolates the informative subset from mechanical liquidation |
| Trade-to-news gap | Days between trade and the next material disclosure | Long | Systematically short gaps suggest information asymmetry or worse |
| Company-buys-insiders-sell | Overlap of buyback windows with insider sales | No overlap | Company capital supporting insider exits is a direct conflict |
| Silence signal | No insider buying despite a large price decline and public management optimism | Buying present | The cheapest possible confirmation of stated conviction, and its absence is informative |

---

## 7. Related-party transactions and tunnelling

RPTs are the primary channel through which controllers extract value from minorities. Read the full RPT schedule in the notes — every year, in full — and build a map of counterparties before you interpret any number.

**What to quantify.** Sales to and purchases from related parties; loans, advances and deposits given; corporate guarantees issued; royalty, brand, trademark and technical-fee payments; management and consultancy fees; rent and property leases; asset purchases and sales; and remuneration to relatives of directors. Express each as a percentage of revenue, of PBT and of net worth, and plot the trend. A single year's RPT table tells you almost nothing; the five-year trajectory tells you whether extraction is intensifying.

**The patterns that matter.**
- **Royalty and brand fees to a parent or promoter entity.** Classic in Indian subsidiaries of multinationals and in family groups. A royalty that rises as a percentage of sales while margins do not improve is a transfer, not a service. India: LODR Reg 23 requires majority-of-minority approval for royalty or brand payments to a related party exceeding 5% of annual consolidated turnover — check whether that threshold was approached, and whether the payment was structured to stay just below it.
- **Loans and advances to promoter entities**, especially interest-free or below-market, unsecured, or repeatedly rolled over. Then check whether they are being written off in "exceptional items."
- **Guarantees for unrelated promoter businesses.** Off-balance-sheet until they crystallise; size them against net worth.
- **Purchases through a single promoter-owned intermediary.** A captive distributor, logistics arm or raw-material supplier is a margin siphon that shows up as unexplained gross-margin underperformance versus peers.
- **Asset transfers near reporting dates** and at valuations supported only by a related valuer.
- **Related-party receivables ageing more slowly than third-party receivables** — the cleanest quantitative tunnelling test available, because it requires no judgement about pricing.

**Approval quality (India).** Under LODR Reg 23 and s.188 of the Companies Act, RPTs require audit-committee approval by disinterested members, and material RPTs — above ₹1,000 crore or 10% of consolidated turnover, whichever is lower — require shareholder approval with related parties abstaining. Verify that this actually happened, and read the dissent. A high against-vote on an RPT resolution that passed only because the promoter group was arithmetically excluded but the institutions still lost is a strong signal about how minorities see the controller.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Total RPT value / revenue | Sum of RPT flows ÷ revenue | Low and stable; high is acceptable only where structurally necessary and priced transparently | Sizes the channel through which value can leave |
| Royalty + brand + management fees / PBT | From RPT note ÷ PBT, 5-year trend | Flat or falling as % of sales | Rising fees against flat margins is a transfer to the controller |
| Loans and advances to related parties / net worth | From RPT note and balance sheet | Near zero for an operating company | Company balance sheet financing the promoter |
| Guarantees to related parties / net worth | Contingent-liability note | Near zero | Off-balance-sheet exposure to entities you cannot analyse |
| RP receivable days vs third-party receivable days | Compute both separately | Similar or shorter for RPs | Divergence is tunnelling that needs no pricing judgement |
| Material RPTs approved by majority of minority | Count and against-vote % | All material RPTs approved; low dissent | Tests whether the approval architecture actually functions |

---

## 8. Group structure complexity and holdco opacity

Map the corporate tree before you interpret consolidated numbers. List subsidiaries, step-down subsidiaries, JVs, associates, trusts and offshore SPVs, with ownership percentages and jurisdictions. For India, the annual report's subsidiary list plus Form AOC-1 gives you the financial summary of each; MCA21 filings give you the group entities that are *not* subsidiaries but sit in the promoter group.

Then answer four questions. **Where does the cash sit** relative to where the debt sits? A cash-rich subsidiary under a debt-laden listed parent means dividends must be upstreamed to service the debt, and minority interests in the subsidiary get paid first. **Are you structurally subordinated?** Debt at the operating company ranks ahead of the holdco's equity claim on that company. **Where is the value you are buying?** If the listed entity is a thin holdco whose assets are minority stakes in operating entities, you are buying a holdco discount that may never close, and you must value it sum-of-the-parts — route to `references/sectors/holdco-assetmgr.md`. **Why is it this complicated?** Complexity has legitimate causes (regulatory ring-fencing, JV partners, tax treaties, project finance at the SPV level). It also has illegitimate ones. Ask management for the rationale and judge whether the answer covers all the entities.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Subsidiary count and consolidation depth | Count entities and layers | Proportionate to the business | Proliferating entities with no disclosed activity is a hiding place |
| Intercompany loans + guarantees / net worth | From notes | Low | Measures how much of group solvency is internal circulation |
| Holdco vs opco debt split | Debt at listed entity vs at operating subsidiaries | Understood and stated | Determines structural subordination and dividend dependency |
| Entities in opaque jurisdictions | Count and % of assets | Zero or fully explained | Secrecy jurisdictions defeat verification |
| Holdco discount | Market cap ÷ sum-of-parts value of stakes | Judge against own history and peer holdcos | Persistent discounts are structural, not a mispricing you can assume closes |

---

## 9. Capital raising, dilution and financing behaviour

Per-share value is what you own. Build a 7–10 year share-count history and identify every event that changed it.

**What to reconstruct.** Rights issues, QIPs and secondary offerings, preferential allotments, convertible bonds, warrants, ESOP/RSU grants and exercises, and buybacks. For each: who subscribed, at what price, and at what discount to the prevailing market. Then compute cumulative equity raised against cumulative FCF generated — a business that has raised more than it has produced across a full cycle is a capital sink regardless of its reported growth.

**India specifics.** Preferential allotment pricing is formula-driven under SEBI ICDR (the higher of the 90-trading-day and 10-trading-day VWAP, with a specified relaxation regime); warrants require 25% upfront with 18 months to convert, which gives the holder a cheap 18-month option struck at a depressed-market price. Warrants issued to promoters during a downturn, converted after a recovery, are a well-worn route to increasing promoter stake at minority expense — always price the option value that was transferred. QIP pricing uses a two-week VWAP with a permitted discount of up to 5%. ESOP schemes fall under the SEBI (SBEB and Sweat Equity) Regulations; check the pool size, the exercise price relative to market, and the performance conditions.

**US specifics.** Watch for at-the-market (ATM) programmes and shelf registrations that permit continuous issuance, convertible notes with reset features, and any structured or "toxic" financing with variable conversion prices — the latter is a near-terminal signal for small caps. Stock-based compensation should be treated as an expense in cash-flow terms and its dilution measured on the diluted count including unvested awards, per `references/03-earnings-quality.md`.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Diluted share-count CAGR | 5–10 year CAGR of fully diluted shares | ≤1–2% for a self-funding business; negative if buying back | The direct measure of how much of the business you keep |
| Cumulative equity raised ÷ cumulative FCF | 10-year sums | <1 | Distinguishes a compounder from a perennial capital consumer |
| Issue discount to market | (Market price − issue price) ÷ market price, per event | Small; large discounts to insiders are a transfer | Prices the wealth moved from minorities to subscribers |
| SBC / ESOP burn rate | Annual grants ÷ shares outstanding | ~1% or less outside early-stage | Compounds silently; large pools with no performance gate are pay, not alignment |
| Warrant option value to insiders (India) | Value of the 18-month option implicitly granted at the formula price | Zero or compensated | The favour is the optionality, not the price |
| Net issuance per share | Shares issued less repurchased, annually | Consistent direction | Issuing cheap to insiders while buying back dear is the classic two-handed transfer |

---

## 10. Executive compensation and alignment

Compensation design predicts behaviour better than any stated strategy. Read the actual plan documents, not the summary table.

**What to extract.** Fixed pay, annual cash bonus, long-term equity (and its vesting horizon and performance conditions), pension, perquisites, severance terms and change-of-control triggers. Then identify the *metrics that gate the bonus*. Metrics that can be bought with capital — revenue growth, absolute EBITDA, adjusted EBITDA, total profit — reward empire building and encourage leverage and acquisitions. Metrics that resist manipulation — ROIC, FCF per share, relative TSR, economic profit — reward the behaviour you want. If a company's bonus plan pays on adjusted EBITDA and the adjustments are management-defined, the plan is paying for the adjustments.

**India specifics.** Managerial remuneration is capped by s.197 of the Companies Act at 11% of net profits computed under s.198 (5% for a single MD/WTD, 10% for all of them together, 1% for non-executive directors where there is an MD, otherwise 3%), with excess requiring a shareholder special resolution — so read the resolution and the dissent when the cap is breached, particularly in a loss year where Schedule V limits apply. Aggregate the remuneration of *all* promoter-family members, including relatives holding office or place of profit, and express it as a percentage of PBT; family payouts are often individually modest and collectively large. The Reg 27 corporate-governance report and the annual report's remuneration section carry the median-employee pay ratio disclosures.

**US specifics.** The DEF 14A CD&A, the Summary Compensation Table, the pay-ratio disclosure and the pay-versus-performance table (Item 402(v), showing Compensation Actually Paid against company TSR, peer TSR, net income and a company-selected measure) let you test alignment directly. Check clawback policy compliance with the Rule 10D-1 listing standards effective end-2023 — recovery of erroneously awarded incentive compensation on restatement is now mandatory, and how a board handled an actual clawback trigger is far more informative than the policy text. Read the say-on-pay result: sustained support below ~70–80% is significant institutional dissent, and a board that receives it and changes nothing has told you where power sits.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| CEO comp / net profit | Total comp ÷ PAT | Small; rising share needs explanation | Scales pay to what the business actually earns |
| Promoter-family aggregate comp / PBT (India) | Sum all related executives ÷ PBT | Low single digits at most | Catches extraction split across family members |
| Pay growth vs EPS/FCF/TSR growth | 3–5 year CAGRs side by side | Pay growth ≤ performance growth | Pay rising while owners lose is board capture |
| Long-term equity share of pay | Performance-linked equity ÷ total comp | Majority for senior executives | Fixed cash rewards tenure; equity rewards outcomes |
| Vesting horizon | Years to full vest, and post-vest holding requirement | 3+ years, with holding requirements | Short vesting rewards a quarter, not a decade |
| Quality of bonus metrics | Classify each KPI as manipulable or durable | Durable metrics dominant | Determines which behaviours get paid for |
| Say-on-pay / remuneration-resolution dissent | Against + abstain % | <10% | Measured institutional judgement, free of charge |
| Repricing and mega-grants | Count of option repricings or outsized grants after price falls | Zero | Repricing removes the downside that made the grant an incentive |

---

## 11. Board independence, composition and functioning

Assess genuine independence, not the label. Directors are classified as independent by the company; you classify them by evidence.

**Adjust the count.** Deduct from the "independent" tally any director with: a prior executive role at the company or a group entity; family ties to the promoter; a professional relationship (law firm, bank, consultancy, audit) with the company; cross-directorships on other promoter-group boards; tenure long enough to have become part of the furniture; or a material commercial relationship disclosed in the RPT note. Report your adjusted independence percentage alongside the company's claimed figure and show the deductions.

**India specifics.** LODR Reg 17 requires at least one-third independent directors where the chair is a non-executive unrelated to the promoter, and at least half where the chair is executive or promoter-related; the top 1,000 listed companies must have at least one woman independent director. Independent-director tenure is capped at two consecutive five-year terms with a cooling-off period (s.149), and since 2022 both appointment and removal of an independent director require a special resolution — which strengthens minorities somewhat, so check how such resolutions have actually been voted. Reg 18 requires an audit committee with a majority of independent members and financial literacy across it. Read the corporate-governance report for attendance, and read every independent-director resignation letter: SEBI requires the detailed reason to be disclosed, and resignations citing "pre-occupation" clustered around a contentious event are a signal regardless of the stated reason.

**US specifics.** Exchange listing standards require a majority-independent board and fully independent audit, compensation and nominating committees, with the audit committee needing a financial expert (disclosed under Item 407(d)(5)). Foreign private issuers may follow home-country practice instead — check Item 16G of the 20-F before assuming any of this applies. Read director-election vote results: a director with 15%+ withheld votes has been formally rebuked. Check ISS/Glass Lewis recommendations and, in India, IiAS/SES/InGovern notes, for the specific reasons given.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Adjusted independence % | Genuinely independent directors ÷ board size, after deductions | Majority; at minimum the statutory floor | The board is the only structural check on a controller |
| Directors with tenure >9–10 years | Count and % | Low, with visible refreshment | Long tenure erodes independence of mind regardless of formal status |
| Chair/CEO separation | Yes/no; lead independent director if combined | Separated, or a genuinely empowered lead independent director | Concentrating both roles removes the agenda-setting check |
| Committee independence | Audit / nomination / remuneration composition | Fully independent; audit chair financially expert | Committees are where governance actually happens |
| Attendance | Board and committee attendance % per director | >75% consistently | Absent directors cannot challenge anything |
| Overboarding | Number of other listed boards per director | ≤4–5, fewer for executives | Capacity constrains scrutiny |
| Independent-director churn | Resignations in 3 years and stated reasons | Low; reasons benign | Resignations citing governance are among the strongest single signals available |
| Against-votes on director elections | Highest against/withheld % in last 3 AGMs | <10% | Independent institutional judgement, already tabulated for you |

---

## 12. Auditor: quality, tenure, fees, resignations

The auditor is the last independent gatekeeper on the numbers everything else depends on.

**Establish the facts.** Who is the auditor; how long have they held the engagement; when was the last rotation; what are audit fees versus non-audit and tax fees paid to the same firm and its network; is the firm's scale and geographic footprint appropriate to the group's size and jurisdictions. India requires rotation under s.139 — a maximum of five consecutive years for an individual auditor and ten for a firm, with a five-year cooling-off — so the presence of the same firm beyond that is itself a question. In the US, tenure is disclosed in the audit report and can run for decades; long tenure is not disqualifying by itself but combines badly with high non-audit fees.

**Read the opinion properly.** Work through: the opinion type (unqualified, qualified, adverse, disclaimer); emphasis-of-matter and material-uncertainty-related-to-going-concern paragraphs; and the Key Audit Matters (India/IFRS) or Critical Audit Matters (US). KAMs/CAMs are the auditor telling you exactly which balances required the most judgement — treat them as a to-do list for your forensic pass, not as boilerplate. In India also read the CARO 2020 annexure in full: it carries specific, checkable statements on undisclosed income, wilful defaulter status, diversion of short-term funds to long-term use, loans to related parties, benami proceedings and whistle-blower complaints. Read the ICFR opinion under s.143(3)(i); in the US read Item 9A and note whether an auditor attestation on internal control was even required — non-accelerated filers and emerging growth companies are exempt from 404(b), so a clean-looking ICFR section may reflect management assertion only.

**Changes and resignations are the high-severity events.** In the US, an auditor change is reported on Form 8-K Item 4.01, including whether there were disagreements and whether the prior auditor's reports contained adverse or qualified opinions; a restatement appears at Item 4.02 (non-reliance). Read the outgoing auditor's exhibit letter, which is the auditor's own account. In India, a resigning auditor files Form ADT-3 and SEBI's framework requires disclosure of detailed reasons, with the auditor expected to complete the limited review or audit for the period before resigning. Any resignation citing lack of information, lack of cooperation, or inability to obtain sufficient appropriate audit evidence is a near-automatic stop: the person with statutory access to the books declined to certify them.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Auditor tenure | Years since appointment; date of last rotation | Within statutory rotation limits (India); disclosed and considered (US) | Familiarity erodes scepticism |
| Non-audit fees / total auditor fees | From proxy fee table (US) or payments-to-auditors note (India) | <25–30% | Consulting revenue is the classic independence solvent |
| Auditor scale vs group complexity | Firm size and network footprint vs group revenue, entities, jurisdictions | Proportionate | A small firm auditing a large multinational group cannot do the work |
| KAM/CAM count and subject | Number and which balances | Few, stable, unsurprising | Names the accounts where judgement is concentrated |
| Modified opinions / going-concern language | Presence and wording | None | The most explicit warning in the document |
| ICFR material weaknesses | Count and nature; whether 404(b) attestation applied | None; attestation present | Weak controls make every other number less reliable |
| Auditor changes in 5 years | Count, with stated reasons | ≤1, routine rotation | Serial changes are auditor shopping |
| Resignation mid-cycle | Yes/no, with the reason given | No | Highest-severity single governance event on this list |

---

## 13. CFO and finance-team turnover

Treat this separately from CEO succession, because it is a different signal with a different mechanism. The numbers are produced by the finance organisation; instability there is one of the most reliable pre-restatement tells available from public filings.

**How to run it.** Build a 5–7 year tenure history for the CFO, the chief accounting officer or controller, the treasurer, the head of internal audit and the audit-committee chair. In the US these departures are disclosed on Form 8-K Item 5.02 with dates; in India they are announced under LODR Reg 30 as material events, and the annual report's KMP list gives you the year-by-year names. Then look for the patterns rather than any single departure:

- Departures announced close to a period end, a filing deadline, an audit completion or an auditor change.
- A resignation with no successor named, or a long interim period covered by a promoted controller.
- More than two CFOs in five years, or a CFO and an auditor changing within the same twelve months — a combination that should raise your forensic priority immediately.
- Boilerplate reasons ("personal reasons", "to pursue other opportunities") attached to a short-tenured, senior finance hire.
- Departure of the audit-committee chair specifically, which removes the board-side counterpart to the auditor.

A single CFO departure with a named successor, an orderly transition period and a plausible destination is ordinary corporate life. A pattern is not. When you find a pattern, do not merely flag it — go back to `references/07-forensic-red-flags.md` and re-run the accruals and cash-existence tests on the periods those individuals signed.

---

## 14. Minority-shareholder rights architecture

This is where minority wealth is preserved or expropriated at inflection points. Assess the machinery *before* an inflection point arrives.

**What to examine.** Voting structure and the wedge (Section 1). Anti-takeover devices: poison pills, staggered boards, supermajority requirements, and — India — the promoter's ability to block special resolutions. The dividend record: consistency through a cycle, and whether payout policy serves all holders or primarily supplies the promoter's cash needs. The company's own history at inflection points: past delisting attempts and the price offered, open offers under SAST and whether the price reflected control value, related-party mergers and the swap ratios used, and the treatment of minorities in prior rights issues (were they able to participate, and on what terms). Responsiveness to dissent: how many resolutions have drawn heavy institutional against-votes, and what the board did afterwards.

**India specifics.** Delisting proceeds by reverse book building, with the framework amended in 2024 to also permit a fixed-price route at a stated premium to the floor price; the historical pattern is that promoters attempt delisting after price weakness, so a delisting proposal arriving at a cyclical trough is a value-capture attempt, not a windfall. Majority-of-minority approval applies to material RPTs and to certain royalty payments. Class-action and derivative remedies exist under s.245 of the Companies Act but are used rarely; assume weak ex-post remedies and price the ex-ante structure accordingly. Read the e-voting results published after each AGM: they give you institution-versus-promoter voting splits resolution by resolution, for free.

**US and global specifics.** Check the charter and bylaws for the wedge, classified board, written-consent and special-meeting rights, exclusive-forum provisions, and the state of incorporation (Delaware's fiduciary case law is a meaningful protection that many other jurisdictions do not replicate). For controlled companies, exchange rules permit exemptions from majority-independent-board and independent-committee requirements — verify whether the company has taken them.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Voting/economic wedge | See Section 1 | Zero | Determines whether any minority vote can ever bind |
| Payout consistency | Dividend paid in each of the last 10 years; payout ratio range | Stable policy through a cycle | Erratic payout alongside strong cash flow suggests cash is being retained for other purposes |
| Past delisting / open-offer pricing | Premium or discount to pre-announcement price and to intrinsic value | Fair premium | The single most direct evidence of how the controller treats minorities in a squeeze |
| Against-management vote share | Highest against % across resolutions in last 3 AGMs | Low | Aggregated professional judgement on the same questions you are asking |
| Board response to dissent | Documented changes following a high against-vote | Visible response | A board that absorbs dissent and changes nothing is not accountable |
| Anti-takeover provisions | Pill, staggered board, supermajority, exclusive forum | Few | Entrenchment removes the market for corporate control as a discipline |

---

## 15. Succession and key-man risk

Underpriced because it is low-probability and high-impact. Assess it explicitly rather than assuming continuity.

Ask: how much of the strategy, the customer relationships, the lender relationships and the regulatory goodwill is personal to one individual? Is there a disclosed succession plan and a named or identifiable successor? What is the tenure and depth of the second line, and what has senior attrition looked like over five years? Is a family transition approaching, and are there signs of intra-family disagreement over control — a dispute among heirs can freeze capital allocation for years and has done so repeatedly in Indian promoter groups. Are there key-man clauses in debt covenants, JV agreements or major customer contracts that would accelerate or terminate on a departure? For founder-led businesses, note age and health disclosure, and whether the founder's stake will pass through a trust or be sold.

An abrupt, unexplained CEO or CFO departure with no successor named is a material event in its own right and should trigger a re-read of Sections 12 and 13, not a routine note.

---

## 16. Integrity, regulatory history and disclosure quality

Past misconduct predicts future misconduct better than almost any other governance variable. Screen the controlling group and the senior team, not just the company.

**The record.** India: SEBI orders and adjudication proceedings against the company, promoters or directors; director disqualifications under s.164; SFIO investigations; income-tax search and survey actions; NCLT/NCLAT proceedings; wilful-defaulter listings; and past appearances on the ASM/GSM surveillance frameworks (see `references/16-market-mechanics-and-tax.md`). US: SEC litigation releases and Accounting and Auditing Enforcement Releases, DOJ actions, FCPA matters, securities class actions and their outcomes, and officer-and-director bars. Search under individual names as well as the corporate name — people move between vehicles.

**Disclosure quality is a live, quarterly signal.** Score it on evidence: does the annual report discuss the segments that did badly with the same specificity as the ones that did well; does management name mistakes; is segment disclosure granular enough to test the story; do defined KPIs stay defined, or do definitions change in the year the metric turns down (a change in KPI definition is a red flag in its own right — see `references/07-forensic-red-flags.md`); are filings timely; how does management handle hostile analyst questions on the call — engagement versus deflection versus refusing to take the question. Run a year-over-year redline of the risk factors and the MD&A: the language management quietly adds or removes is often the earliest disclosure of a deteriorating situation.

**Short-seller and activist reports.** When a credible report exists, read the primary document, then read the company's rebuttal, and grade the rebuttal on specificity. A point-by-point response with documents refutes; a press release about "malicious motives" and a legal threat does not. A refusal to answer the specific quantitative allegations is itself evidence, and should raise your forensic priority sharply.

**Credit and covenant history.** Rating rationales from CRISIL/ICRA/CARE/India Ratings (India) or S&P/Moody's/Fitch (global) contain governance commentary you will not find in the annual report, including agency views on group support, related-party exposure and promoter pledges. A downgrade citing governance or information quality, an "issuer not cooperating" rating status in India, or a covenant waiver history are all direct evidence.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Regulatory actions against insiders | Count and severity, 10 years, by name | Zero | The strongest single predictor of recurrence |
| Filing timeliness | Delayed filings, extensions, restatements in 5 years | Zero | Late filings are usually a symptom, not a process failure |
| Rating trajectory | Direction over 5 years; any "issuer not cooperating" status (India) | Stable or improving | Agencies see covenant and liquidity data you do not |
| Contingent liabilities / net worth | From the contingent-liability note | Low and stable | Sizes the tail of unresolved disputes |
| Rebuttal specificity | Grade any response to credible allegations | Point-by-point with evidence | Distinguishes a wronged company from a cornered one |

---

## 17. Sector translation: where these checks change or invert

The governing principle applies to governance too. Do not carry a generic checklist into a sector where its terms are undefined.

**Banks and NBFCs (India: `references/sectors/banks.md`, `references/sectors/nbfc.md`).** Capital allocation *is* underwriting; there is no meaningful ROIC/WACC test, so assess capital allocation as ROE versus cost of equity, plus credit-cost discipline across a full cycle. The dominant governance risks are connected lending, evergreening of stressed exposures and promoter-group borrowing. India-specific checks: RBI's asset-classification divergence disclosure (required when the regulator's assessment exceeds the bank's by specified thresholds) is the single most valuable governance disclosure in the sector; RBI fit-and-proper norms and MD/CEO tenure caps for private banks; promoter shareholding dilution roadmaps; and mandatory joint statutory auditors with capped tenure for larger banks and NBFCs. Pledging by a bank promoter carries different consequences because of ownership caps and regulatory approval requirements.

**Insurers (`references/sectors/insurance.md`).** Capital allocation is judged on value of new business and embedded-value movement, not ROIC. Governance focus: reserving discipline and the appointed actuary's independence, distribution-related-party arrangements with a bancassurance parent, and IRDAI ownership and fit-and-proper rules.

**REITs, InvITs and externally managed vehicles (`references/sectors/realestate-reit.md`).** The central governance question is the manager's fee structure. Fees on gross assets or on acquisitions reward growing the vehicle regardless of per-unit value; fees on distributable income or total return align better. Every sponsor asset dropped down into the trust is a related-party transaction and must be tested against independent valuation. Check unitholder voting rights, the sponsor's mandated holding and lock-in, related-party approval mechanics excluding the sponsor, and leverage caps. Standard "promoter pledging" and "board independence" tests translate only loosely; ask instead who appoints and can remove the manager.

**Miners, oil and gas, and deep cyclicals (`references/sectors/metals-mining.md`, `references/sectors/oil-gas.md`).** Capital allocation is nearly the entire investment case: the record of committing capex at the top of the cycle versus counter-cyclically is the scorecard. The reserve statement is a second set of accounts, and the competent person's report (JORC, NI 43-101, SEC S-K 1300) is a second auditor — check the qualifications, independence and revision history of reserve estimates the same way you check the financial auditor. Add resource-nationalism, licence-renewal and royalty-regime risk to the integrity screen.

**PSUs and government-controlled companies (India, `references/13-situations.md`).** The promoter is the state, so the tests change rather than disappear: dividend and buyback demands driven by fiscal need, cross-holding bailouts of other state entities, disinvestment overhang, extended vacancies in board and CMD positions, and pricing decisions taken as policy rather than as commerce. Minority interests are structurally subordinate to policy objectives — price that, do not argue with it.

**Holdcos and conglomerates (`references/sectors/holdco-assetmgr.md`).** Section 8 becomes the main event: cross-holdings, the persistence of the discount, and whether cash flows up.

**Early-stage and recently listed companies (`references/13-situations.md`).** Governance maturity lags growth. Expect founder control, thin boards, large option pools and lock-in expiry supply. Weight structure heavily because there is no behavioural track record to weight instead.

---

## 18. Scoring, weighting and how to write it up

**Hard stops.** Treat these as kill criteria under Stage 3 rather than as score deductions. Each one means the analysis cannot be completed with confidence, and the correct output is a documented decline, not a lower target price:

- Auditor resigned or was dismissed citing lack of information, lack of cooperation, or inability to obtain sufficient appropriate audit evidence.
- Adverse opinion, disclaimer of opinion, or unresolved going-concern doubt without a credible, funded remediation plan.
- Regulator has found fraud or securities violations against the current promoter, CEO or CFO and they remain in post.
- Cash balances that fail the existence tests in `references/07-forensic-red-flags.md`.
- Related-party flows large enough that the minority-attributable economics cannot be reliably determined.
- The listed security does not confer legal claim on the operating assets and that claim has never been tested (Section 1), with no compensating structural protection.

**Graduated adjustments.** Everything else feeds the sector-relative score per `references/11-scoring-rubric.md`, and — where you can justify it — an explicit increment to the cost of equity or a cut to the exit multiple in `references/06-valuation.md`. Say which one you applied and by how much. A governance concern that changes no number in the model is a concern you have not actually incorporated.

**How to present it.** Three parts, in this order: what the security confers; the capital-allocation and guidance-delivery evidence, with the ledger and the tabulation; the specific governance findings with their source citations and a severity label. Then state the adjustment you made and where. Distinguish clearly between *structure I dislike* and *behaviour I can evidence* — the second is a finding, the first is a risk factor. And where disclosure simply does not exist (a 20-F filer with aggregate compensation only, an unlisted group entity with no public accounts), say that the check could not be run, rather than scoring the absence as a pass.

---

## Checklist

- [ ] Establish what the security confers: class, votes versus economics, sunset, DVR/ADR/GDR mechanics, VIE or contractual control.
- [ ] Compute the voting/economic wedge and state it in the report.
- [ ] Build the 7–10 year capital deployment ledger: source, use, amount, promised return, realised return.
- [ ] Compute RoIIC (3–5y, lagged) and compare to WACC and to aggregate ROIC.
- [ ] Score every major acquisition against its announcement promises; sum impairments against acquisition spend.
- [ ] Score buybacks on price paid versus the company's own historical multiple range.
- [ ] Tabulate every quantified guidance statement of the last 3–5 years against actuals; compute hit rate and mean signed error.
- [ ] Pull 8–12 quarters of shareholding pattern; identify the *mechanism* of every change in promoter/insider stake.
- [ ] India: pull pledge and total encumbrance as % of promoter holding and of shares outstanding, trend over 8 quarters, lender and purpose.
- [ ] Analyse insider trades transaction by transaction; strip Form 4 codes A/M/F; isolate discretionary trades; look for clusters.
- [ ] Read the full RPT note for 5 years; compute RPT/revenue, fees/PBT, loans and guarantees/net worth, and RP versus third-party receivable days.
- [ ] Verify that material RPTs received disinterested approval, and read the against-vote.
- [ ] Map the group tree: entity count, layers, jurisdictions, intercompany loans and guarantees, where cash sits versus debt.
- [ ] Build the 7–10 year diluted share-count history; price every issuance discount and every insider warrant.
- [ ] Compare cumulative equity raised to cumulative FCF over 10 years.
- [ ] Classify every bonus metric as manipulable or durable; compute pay versus performance and family aggregate pay versus PBT.
- [ ] Recompute board independence after deducting conflicted and long-tenured directors; check attendance, overboarding, committee composition.
- [ ] Read every independent-director resignation reason from the last three years.
- [ ] Record auditor identity, tenure, rotation compliance, non-audit fee share, KAMs/CAMs, CARO exceptions, ICFR findings.
- [ ] Check for any auditor change or resignation and read the outgoing auditor's own statement (8-K Item 4.01 / ADT-3).
- [ ] Build a 5–7 year CFO, controller, treasurer and audit-committee-chair tenure history; flag patterns, not single exits.
- [ ] Review minority-rights machinery: anti-takeover devices, past delisting/open-offer pricing, AGM e-voting splits, board response to dissent.
- [ ] Assess succession, bench strength, key-man covenants and family-transition dynamics.
- [ ] Screen every insider by name against SEBI/SEC/court records; grade disclosure candour and any short-seller rebuttal.
- [ ] Apply the sector translation before scoring: banks, insurers, REITs/InvITs, miners, PSUs and holdcos change the questions.
- [ ] Apply hard stops where they trigger; otherwise state the explicit valuation or scoring adjustment made, and where disclosure was unavailable, say so.
