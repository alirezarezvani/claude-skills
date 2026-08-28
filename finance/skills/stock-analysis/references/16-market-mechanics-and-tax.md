# Market Mechanics, Corporate Actions and Taxation

Use this when: you have a thesis you like and need to know whether it can actually be owned, exited and kept after tax — run the tradeability gate early (before deep fundamental work on any smallcap), and the supply-calendar and tax layers before sizing or writing the recommendation.

Everything upstream in this skill estimates *intrinsic* value. This file governs *realised* return, which differs from intrinsic value by three things the financials never show: whether the market lets you transact at the price on the screen, whether the share count you divided by is the share count you will end up with, and how much of the gain the tax authority and the transaction stack keep. A correct 30% IRR thesis on a stock in a weekly call auction with a 40% lock-in expiry due and a 20% short-term tax rate is not a 30% IRR. The governing rule applies here as everywhere: none of these numbers means anything absolutely — impact cost, delivery percentage, float and dilution are only interpretable against the stock's sector, size bucket and own history, and for banks, REITs/InvITs and PSUs the dilution and distribution logic is structurally different, not just quantitatively different (Section 23).

**Standing warning on tax figures.** Every rate, threshold, holding period and form number in this file is *indicative and dated*. Tax law changes mid-year, differs by jurisdiction, and depends on the holder's residency, entity type and account wrapper. India changed capital-gains rates and buyback taxation within a single recent financial year. Never quote a rate from memory into a report. Verify against the current Finance Act / IRS publication / exchange circular, state the date of the rule you applied, and split any calculation that straddles a rule change by transaction date. Where you could not verify, say "rate to be confirmed" rather than filling in a plausible number.

## Contents

- [0. The method: gate, calendar, net-of-cost](#0-the-method-gate-calendar-net-of-cost)
- [1. Exchange surveillance status (India: ASM / GSM / ESM)](#1-exchange-surveillance-status-india-asm--gsm--esm)
- [2. Circuit limits, price bands and trade-to-trade](#2-circuit-limits-price-bands-and-trade-to-trade)
- [3. Delivery volume vs traded volume (India)](#3-delivery-volume-vs-traded-volume-india)
- [4. Liquidity, impact cost and realistic exit size](#4-liquidity-impact-cost-and-realistic-exit-size)
- [5. Halts, suspensions and market-wide circuit breakers](#5-halts-suspensions-and-market-wide-circuit-breakers)
- [6. Free float and float-adjusted supply](#6-free-float-and-float-adjusted-supply)
- [7. The dilution map: build it once, in shares](#7-the-dilution-map-build-it-once-in-shares)
- [8. QIP, preferential allotment and warrants](#8-qip-preferential-allotment-and-warrants)
- [9. Convertibles and the honest diluted share count](#9-convertibles-and-the-honest-diluted-share-count)
- [10. Rights issues](#10-rights-issues)
- [11. Bonus, splits and consolidations](#11-bonus-splits-and-consolidations)
- [12. Buybacks: tender vs open market](#12-buybacks-tender-vs-open-market)
- [13. Lock-in expiries and pre-IPO supply cliffs](#13-lock-in-expiries-and-pre-ipo-supply-cliffs)
- [14. Index inclusion, exclusion and rebalance flows](#14-index-inclusion-exclusion-and-rebalance-flows)
- [15. Open offers, delisting and schemes of arrangement](#15-open-offers-delisting-and-schemes-of-arrangement)
- [16. Capital gains: holding period is a position decision](#16-capital-gains-holding-period-is-a-position-decision)
- [17. Dividend taxation and withholding](#17-dividend-taxation-and-withholding)
- [18. The transaction cost stack: STT, stamp duty, round trip](#18-the-transaction-cost-stack-stt-stamp-duty-round-trip)
- [19. Cross-border: withholding, treaty relief, PFIC, estate tax](#19-cross-border-withholding-treaty-relief-pfic-estate-tax)
- [20. Loss set-off, carry-forward and harvesting](#20-loss-set-off-carry-forward-and-harvesting)
- [21. Custody, demat and account hygiene](#21-custody-demat-and-account-hygiene)
- [22. Settlement, record dates and response obligations](#22-settlement-record-dates-and-response-obligations)
- [23. Sector translation: where this lens inverts](#23-sector-translation-where-this-lens-inverts)
- [Checklist](#checklist)

---

## 0. The method: gate, calendar, net-of-cost

Three passes, in this order. The first is cheap and kills candidates before you waste analysis on them.

**Pass 1 — Tradeability gate (10 minutes, do it first for any sub-largecap).** Surveillance status, price band, median daily traded value, impact cost, delivery percentage, free float. If the stock is in a punitive surveillance stage, or your intended position exceeds what the tape can absorb in a reasonable number of days, stop. No fundamental edge survives an inability to exit. Record the gate result even when it passes — it sets the maximum position size for everything downstream.

**Pass 2 — Supply calendar.** One table, forward 24 months, in shares and in days of average daily traded value (ADV): every lock-in expiry, warrant exercise window, convertible conversion date, unused enabling resolution, ESOP vesting cliff, promoter/PSU divestment intent and index review date. Dilution and supply are the most *predictable* source of drawdown in the whole analysis and the most routinely ignored.

**Pass 3 — Net-of-cost return.** Take your target return and subtract: round-trip transaction stack × expected turnover, dividend tax at the holder's marginal rate, and capital-gains tax at the rate implied by your stated holding period. Report gross and net. If the thesis only works gross, it does not work.

Write the output of all three into the report as three lines, not three pages: *"Position capped at X on liquidity; Y% of shares released from lock-in in month Z equal to N days of ADV; gross 18% IRR becomes ~14% net at a 3-year hold."*

---

## 1. Exchange surveillance status (India: ASM / GSM / ESM)

**India-specific.** Before anything else on an Indian smallcap or microcap, pull the current NSE/BSE lists: **ASM** (Additional Surveillance Measure — short-term and long-term stages), **GSM** (Graded Surveillance Measure, Stages I–VI), and **ESM** (Enhanced Surveillance Measure, aimed at SME and microcap counters). These are published as exchange files and revised on a fixed review cycle.

Record four things: the stage, the date applied, the consequences, and the next review date on which it can escalate or exit.

Typical consequences by escalation (verify the current framework — stages and their exact effects have been revised repeatedly):

| Escalation | Typical consequence | What it does to you |
|---|---|---|
| ASM short-term | 50–100% margin, sometimes reduced price band | Leverage gone; position cost rises |
| Trade-for-trade (T2T / BE series) | 100% delivery, no intraday netting | Cannot scale in and out; every trade settles |
| Price band cut to 5% or 2% | Daily move capped | A −50% repricing takes many sessions you cannot sell into |
| Periodic call auction | Trading collapses to one price-discovery window (weekly in the worst stages) | Effectively no continuous market; exit at whatever single price clears |
| No pledging, no derivatives | Collateral value zero; no hedge or short route | Cannot hedge the position you are stuck in |

**Why it matters.** Surveillance placement is the single biggest silent liquidity killer, and almost no screener surfaces it — so a "cheap" screen hit can be untradeable. It is also an exchange-generated signal that price and volume behaviour looks abnormal relative to fundamentals, which historically precedes regulatory action or collapse more often than it precedes recovery. A GSM Stage IV name is not a cheap stock; it is a stock you may be unable to sell for months.

**US/global analogue.** There is no direct equivalent, but check: SEC trading suspensions, "caveat emptor" flags on OTC Markets, exchange deficiency notices (Nasdaq/NYSE listing-standard non-compliance letters, minimum bid price and market-value tests), and Reg SHO threshold-list membership. For any OTC/pink-sheet name, treat absence of current information tier as an automatic fail.

---

## 2. Circuit limits, price bands and trade-to-trade

Identify the applicable band and the last 3–6 months of circuit history.

- **India:** daily bands of 20% / 10% / 5% / 2% on cash-segment stocks. Stocks in the F&O segment have no fixed daily band but operate under a dynamic price band (commonly 10%) that flexes in steps after a cooling-off period. T2T/BE-series stocks prohibit intraday.
- **US:** Limit Up–Limit Down (LULD) bands trigger 5-minute trading pauses rather than day-long locks; the Short Sale Restriction (alternative uptick rule) engages after a 10% intraday decline and persists into the next session.

Distinguish two very different events: a circuit **touched with volume** (genuine repricing, exit possible) versus a **locked circuit with no counterparty** (no exit at all). Count locked days separately.

**Why it matters.** Circuit structure, not historical volatility, defines your realistic worst case. A 5% lower circuit with no bids means a −50% move takes roughly fourteen sessions during which you cannot sell a single share — the drawdown is not a paper drawdown, it is a trap. Conversely, repeated *locked upper* circuits on a small float usually indicate operator-driven price movement rather than demand, and should pull the stock toward the surveillance and delivery checks rather than into the portfolio. Size positions against the band, not the beta.

---

## 3. Delivery volume vs traded volume (India)

**India-specific**, and one of the most useful free datasets the Indian market provides. NSE and BSE publish security-wise delivery quantity alongside traded quantity in the daily bhavcopy.

| Metric | Definition / how to compute | Indicative range | Why it matters |
|---|---|---|---|
| Delivery % | Delivery qty ÷ total traded qty, averaged over 30 / 90 / 250 days | Broadly 25–50% for liquid mid/large caps; higher for illiquid quality compounders; <20% signals churn | Separates ownership from speculation |
| Delivery-weighted volume trend | Delivery qty (not turnover) trend over 12 months | Rising with price = accumulation | Confirms whether a rally has real buyers |
| Divergence flag | Traded volume spiking while delivery % collapses | Any sharp fall below the stock's own 250-day norm | Classic churn / operator signature |

Benchmark **against the sector and against the stock's own history**, never against an absolute number: an index-heavyweight with heavy derivative and algorithmic activity will structurally show lower delivery than an illiquid quality smallcap, and neither reading means what the raw figure suggests.

**Why it matters.** A price move on huge volume at 15% delivery is rotation that typically reverses; the same move at 60–70% delivery suggests genuine accumulation that has to be sold before the price falls back. Persistently low delivery plus rising price plus a small free float is the standard fingerprint of price manipulation, and it pairs directly with Sections 1 and 6. **US analogue:** no delivery data exists; substitute short interest and days-to-cover, off-exchange (dark) volume share, and 13F/13D-G ownership changes.

---

## 4. Liquidity, impact cost and realistic exit size

Compute in **value, not shares** — share counts are meaningless across prices.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| Median daily traded value (ADV) | Median (not mean — spikes distort) of daily turnover over 6 months | Depends entirely on your AUM; the ratio below is what matters | Base unit for every supply and sizing calculation |
| Days to exit | Position value ÷ (ADV × 10–20% participation) | ≤5 days for a core position; >20 days is a research-only name | The only honest definition of position capacity |
| Impact cost | Exchange-published cost of a standard order (India: NSE publishes impact cost for a Rs 1 lakh order); or model half-spread + depth | Low single-digit basis points for liquid names; >1% is a red flag | Also the exchange's own gating metric for index and F&O eligibility, so it forecasts inclusion |
| Bid–ask spread | Time-weighted spread ÷ mid | A few bps liquid, tens of bps smallcap | Direct round-trip cost, charged twice |
| Derivatives availability | Is the stock in NSE F&O / has listed US options? | — | Determines whether you have any hedge or short route at all |

**Why it matters.** Position size is set by exit liquidity, not conviction. A stock trading Rs 2 crore a day cannot absorb a Rs 5 crore position without moving the price double digits — the exit cost eats the alpha you did the analysis to find. Liquidity is also reflexive: it evaporates precisely in the drawdown when you want to sell, so stress the calculation at 30–50% of normal ADV before deciding the position is exitable.

---

## 5. Halts, suspensions and market-wide circuit breakers

Check the stock's own history of exchange **suspensions** — non-compliance with listing regulations (India: SEBI LODR; US: exchange listing standards), delayed results, auditor resignation, scheme-of-arrangement freezes — and any compulsory-delisting watchlist entry. A suspension freezes capital for an indefinite period, and compulsory delisting can leave you holding an unlisted security with no realistic market.

Separately understand **market-wide circuit breakers**: index moves of 10 / 15 / 20% trigger halts ranging from 45 minutes to the rest of the session, with the duration depending on the time of day the trigger is hit. Know your market's pre-open, post-close and any block/bulk-deal windows.

**Why it matters.** Stop-losses do not execute during a halt, and the gap on resumption routinely prints through them. Anyone running leverage must size for a scenario in which they cannot act for a full session and then reopen 15% lower. This is a mechanical risk, independent of the company.

---

## 6. Free float and float-adjusted supply

From the quarterly shareholding pattern (India: mandatory under LODR, filed on the exchanges; US: proxy statement, 13F/13D/13G, and the cover page of the 10-K), compute **true free float**:

> Shares outstanding − promoter/insider holding − locked-in shares − strategic, parent and government holdings − pledged/encumbered shares

Track quarter-on-quarter movement in promoter, FII/DII (India), institutional (US), and small-retail buckets, plus the total number of shareholders. **India:** also check FPI sectoral and aggregate ceilings and the resulting "foreign room", because MSCI and FTSE apply a foreign-inclusion factor that can halve an index weight regardless of size.

**Why it matters.** Float is the denominator for every supply event in Sections 7–14. A 12% float means an index inclusion or a 5% promoter sale is an enormous event; a 70% float absorbs the identical flow invisibly. Two composition signals to read directly: a **rising retail shareholder count against falling institutional holding** is usually distribution into weak hands, and a shrinking float with rising price and low delivery is a manipulation signature, not a scarcity story.

---

## 7. The dilution map: build it once, in shares

Before working through Sections 8–13 individually, build one table. Every row is a claim on your per-share economics.

| Instrument | Where to find it | Key parameters to record | Effect on share count |
|---|---|---|---|
| Enabling resolution (unused) | AGM/EGM/postal-ballot notice; board outcome filings | Amount authorised, date passed, validity (typically 1 year) | Contingent — price it as an overhang |
| QIP / follow-on / shelf | Exchange filing; **US:** S-3 shelf, ATM programme in 10-Q | Size, floor formula, discount, allottees | Immediate |
| Preferential allotment | Postal ballot / EGM notice | Allottee identity, relationship, price vs floor, lock-in | Immediate |
| Warrants | Same notice; balance-sheet note | Exercise price, 25% upfront, 18-month window, lapse history | Deferred, holder-optional |
| Convertibles (FCCB/CCD/OCD/CCPS) | Balance-sheet notes, annual report | Conversion price, ratio, reset/ratchet, maturity | Deferred, sometimes automatic |
| ESOPs | ESOP note, cash flow statement | Outstanding, vested, weighted exercise price, annual grant run-rate | Continuous drip |
| Rights issue | Letter of offer | Ratio, price, RE trading window | Immediate, but pro-rata |
| Bonus / split | Corporate action circular | Ratio, record date | None economically |

Then compute two numbers and use them consistently downstream: **fully diluted share count** (assume every in-the-money instrument converts) and **annual dilution rate** over the last 5–7 years (CAGR of diluted shares outstanding). Recompute EPS, P/E and market cap on the diluted base. If your valuation used basic shares while an in-the-money convertible sits in the notes, your valuation is simply wrong.

---

## 8. QIP, preferential allotment and warrants

**QIP (India).** Check for board/shareholder **enabling resolutions** — they frequently sit dormant for a year before use — the size sought, the SEBI floor-price formula (a two-week volume-weighted average of the relevant period), the actual discount to market, the allottee list, the stated use of proceeds, and resulting dilution. Note the 6-month lock-in on QIP shares and the minimum gap rule between successive QIPs.

The real signal is **who was allotted**. Marquee long-only institutions validate the story and price. Allotment to unknown entities, or to parties with a visible relationship to the promoter, at or near the floor price, is a governance flag that belongs in `08-governance.md` as well as here.

**Preferential allotment and warrants (India).** Read the postal-ballot/EGM notice: allottee identity and relationship to promoters, pricing versus the SEBI floor, lock-in (longer for promoter allottees; commonly 18 months for others, and up to three years for promoter minimum-contribution tranches — verify current SEBI ICDR provisions). Warrants carry 25% upfront with 18 months to pay the balance and exercise.

Track the **history of earlier warrants**, which is unusually informative:
- Promoters exercising warrants at a price far below market = a wealth transfer from minority shareholders, plus a known deferred dilution overhang.
- Promoters letting warrants **lapse and forfeiting the 25%** = they judged the stock above fair value with their own money at stake. That is one of the cleanest negative signals available.

**US analogue.** Shelf registrations (S-3) and at-the-market (ATM) programmes are the structural equivalent of an unused enabling resolution — an active ATM on a cash-burning company means continuous supply. PIPEs, and SPAC-era warrant overhangs with redemption triggers, are the equivalents of preferential allotments and warrants; read the warrant terms, not the headline share count.

**Why it matters.** An unused authorisation is not nothing — it is a written option the company holds to sell shares to someone else at a discount, and it caps the stock near the floor price until resolved. Price the overhang; do not wait for the announcement.

---

## 9. Convertibles and the honest diluted share count

Search the balance-sheet notes and annual report for every convertible: FCCBs, compulsorily and optionally convertible debentures, convertible preference shares. Record conversion price, conversion ratio, reset clauses, maturity, coupon, and whether conversion is compulsory or at the holder's option.

Three specific things to hunt for:

1. **Anti-dilution / ratchet clauses** that reprice the conversion downward if the stock falls. These create a death-spiral: a falling price increases shares issued, which increases dilution, which pushes the price lower. Any structure with a floating conversion price tied to a trailing market price should be treated as a solvency issue, not a capital-structure detail.
2. **Unconverted instruments near maturity**, especially FCCBs. Out-of-the-money convertibles do not convert — they become a hard cash redemption liability, often in foreign currency, on a fixed date. That belongs in the debt-maturity ladder in `04-balance-sheet-and-cashflow.md`, not in the equity story.
3. **The EPS gap.** Reported basic EPS can overstate per-share earning power materially when convertibles are outstanding. Always restate.

---

## 10. Rights issues

Record the entitlement ratio, issue price versus market, record date, and — India-specific — the **Rights Entitlement (RE)** window: REs are credited to demat and trade on the exchange for a limited period, then **lapse worthless**.

Compute the theoretical ex-rights price (TERP):

> TERP = (existing shares × cum-price + new shares × issue price) ÷ total shares after issue

**Why it matters.** A rights issue is not dilutive to a participant — it is dilutive only to someone who neither subscribes nor sells their REs. Retail holders let REs lapse routinely, which is a pure, avoidable, 100% loss on the entitlement value. Two analytical reads matter more than the arithmetic: **is the promoter taking up their full entitlement or renouncing** (non-participation is a strong statement about their view of the price, or about their own liquidity), and **what are the proceeds for** — growth capital versus repairing a balance sheet the last raise was also meant to repair. Deeply discounted rights also mechanically reset the price chart, so verify that price history and moving averages used anywhere in the analysis are adjusted.

---

## 11. Bonus, splits and consolidations

Confirm record date, ex-date and adjustment factor, and verify that **price history, moving averages, per-share metrics and any screen output have been adjusted**. Unadjusted data is a silent generator of false signals in every backtest and screener.

Check how a bonus is funded (free reserves versus securities premium) and whether the company has a pattern of announcing bonuses into price strength. For a **reverse split / consolidation**, find the reason — it is very often cosmetic, undertaken to escape a minimum-price rule, a surveillance category or an exchange listing standard, on a business that is genuinely impaired.

**Why it matters.** Bonuses and splits create exactly zero economic value; they change the share count and nothing else. Yet they reliably trigger retail buying, which makes them a convenient distribution window for insiders. Treat the announcement as an event to examine for *who is selling into it*, never as a positive fundamental datapoint.

---

## 12. Buybacks: tender vs open market

Determine the route first — the two are economically different instruments.

| | Tender offer | Open market |
|---|---|---|
| Commitment | Binding for the stated size at the stated price | Non-binding authorisation; a ceiling, not a promise |
| Price | Fixed premium to market | Market price up to a maximum |
| Small-shareholder edge (**India**) | 15% of the buyback reserved for holders with ≤Rs 2 lakh at record date, often producing very high acceptance ratios | None |
| Analytical treatment | Estimate acceptance ratio from the shareholding pattern; a real, computable arbitrage | Assume partial completion; check actual spend versus authorised |

Always check: is the buyback funded by surplus cash or by **debt**, or by cash the operating business actually needed? Are promoters/insiders tendering (participation changes the acceptance ratio and the signal)? And how does the buyback price compare to the company's own historical multiple range — buying back stock at a peak multiple destroys value exactly as reliably as issuing at a trough (see `08-governance.md` on capital allocation scoring).

**Tax, and it inverts the conclusion.** **India:** for buybacks after the October 2024 change, proceeds are taxed **in the shareholder's hands as dividend income** at slab rate, with the cost of the tendered shares treated as a capital loss — this reversed the economics that made buybacks tax-efficient under the earlier company-level buyback-tax regime. **US:** a 1% corporate excise tax applies to net repurchases, and the shareholder's receipt is a capital-gains event, not dividend income. Verify current provisions before modelling any tender arbitrage; the after-tax answer, not the premium, is the answer.

---

## 13. Lock-in expiries and pre-IPO supply cliffs

Build an explicit calendar. **Size every tranche in shares, in percent of float, and in days of ADV** — the third number is the one that predicts the price impact.

Typical Indian tranches (verify against the offer document and current SEBI ICDR rules):

| Tranche | Typical lock-in | Seller behaviour |
|---|---|---|
| IPO anchor investors | 50% released at ~30 days, remainder at ~90 days | Mixed; the 90-day tranche is the larger event |
| Pre-IPO / PE-VC holders | ~6 months | Price-insensitive; 10x cost bases mean any price works |
| Promoter minimum contribution | 18 months to 3 years | Watch the date; often the last cliff |
| QIP shares | 6 months | Institutional, usually orderly |
| Preferential allotment | 6–18 months depending on allottee | Related-party allottees often sell immediately on release |
| ESOP vesting cliffs | Per scheme | Recurring, not a one-off |

**US analogue:** IPO lock-ups (commonly 180 days, with early-release triggers tied to price or earnings dates), Rule 144 volume limits for affiliates, and Form 144 filings.

**Why it matters.** This is the most predictable, calendar-driven source of downside in recently listed companies, and it is routinely ignored by fundamental analysis. A release of 40% of shares into a stock that trades a fraction of a percent of its float daily is an unavoidable supply shock, and the market typically front-runs the date rather than waiting for it. Early PE/VC investors are not valuation-sensitive sellers — they are return-crystallising sellers, and they will accept any price above their cost basis.

---

## 14. Index inclusion, exclusion and rebalance flows

Track eligibility and review calendars, not just current membership.

- **India:** Nifty 50 / Next 50 / Midcap / Smallcap, Sensex, and the **AMFI semi-annual large/mid/small-cap reclassification**, which forces actively managed mid- and small-cap funds to adjust holdings, not just passive funds. Also watch F&O inclusion/exclusion, which changes hedgeability and margin.
- **Global:** MSCI quarterly/semi-annual reviews and FTSE reviews — pay attention to their float factors and **foreign-room adjustments**, which can produce a weight far below what market cap implies. **US:** S&P index committee additions (discretionary, announced with a short lead) and the annual Russell reconstitution (rules-based, heavily front-run).

Estimate passive demand as **(index weight × tracking AUM) expressed in days of ADV**, and note the **announcement date versus the effective date** separately.

**Why it matters.** Passive funds must trade at the close on the effective date regardless of price, so an inclusion creates mechanical buying and an exclusion mechanical selling that can be many multiples of daily volume. But the move mostly happens *between* announcement and effective date and then partially reverses — buying an inclusion after the announcement is usually buying the top. Treat index flow as a timing and execution consideration, never as a thesis. Impact cost (Section 4) is the exchange's own eligibility gate, so improving impact cost is a leading indicator of future inclusion.

---

## 15. Open offers, delisting and schemes of arrangement

These events override your thesis entirely — the exit price becomes a formula, not your valuation.

- **India — SEBI Takeover Code (SAST):** an acquisition crossing the 25% threshold, or creeping acquisition beyond the permitted annual limit above it, mandates an open offer for a further 26%. Check the offer price formula and estimate the acceptance ratio.
- **Voluntary delisting (India):** reverse book building, the discovered price, the 90% threshold, and the limited post-delisting exit window. **US:** going-private transactions under Rule 13e-3 with a SC 13E-3 filing.
- **Demergers, mergers and schemes:** record the swap ratio, record date, when the resulting entity lists (there is often a gap during which you hold an untradeable entitlement), and — critically — the **cost-basis apportionment** between the original and resulting entities for tax.

**Why it matters.** You can be forced to exit at a price you did not choose, or be left holding an unlisted share because you failed to tender by a deadline. Delisting arbitrage and open-offer acceptance ratios materially change expected return and should be modelled explicitly when live. Demerger cost-basis apportionment is a routine source of tax error because brokers frequently show the new entity at zero cost, overstating the gain by the entire sale value.

---

## 16. Capital gains: holding period is a position decision

Confirm the holding-period threshold and rate for the asset class, in the holder's jurisdiction, as of the transaction date.

**India (indicative; verify against current Finance Act).** Listed equity and equity mutual funds: 12 months separates short from long term (24 months for most other assets). Post-23 July 2024, STCG on listed equity under section 111A is **20%**, and LTCG under 112A is **12.5%** with an annual exemption of **Rs 1.25 lakh** and no indexation. Pre-31 January 2018 purchases are grandfathered — cost is stepped up to the higher of actual cost and the 31-Jan-2018 fair market value. Broker tax reports use FIFO matching; reconcile against the AIS / Form 26AS.

**US (indicative; verify).** Long-term treatment requires a holding period exceeding one year; long-term rates are tiered (0/15/20%) with a net investment income tax on top for higher incomes, while short-term gains are taxed as ordinary income. There is no annual capital-gains exemption equivalent to India's.

**Why it matters, in decision terms:**
- A sale one day before the 12-month mark can cost several percentage points of tax **on the entire gain** — money no stock-picking edge recovers. Always check the holding-period clock before recommending an exit.
- Rates changed mid-year in India in 2024, so any multi-period calculation must be **split by transaction date**. Do not apply one rate across a straddling year.
- Deferred capital-gains tax is an interest-free loan from the state that compounds with the position. A strategy that turns over annually pays tax every year on a smaller and smaller base; a 10-year hold pays once. This is a real, quantifiable argument for lower turnover, and it belongs in the recommendation.
- Mismatches between broker P&L and the AIS are a common trigger for tax notices in India.

---

## 17. Dividend taxation and withholding

**India (indicative; verify).** Post-2020 there is no dividend distribution tax at the company level; dividends are taxed in the shareholder's hands at slab rate as income from other sources. TDS applies (commonly 10%) above an annual per-company threshold; Forms 15G/15H may apply for those eligible. Reconcile dividends received against the AIS and claim the TDS credit — unreconciled credits are simply money lost.

**US (indicative; verify).** Qualified dividends receive long-term capital-gains rates but only if a minimum holding period around the ex-date is satisfied; non-qualified dividends are ordinary income. REIT distributions are largely non-qualified.

Two mechanical points that change conclusions:

1. **Compute after-tax yield at the holder's marginal rate before comparing.** A 6% headline yield is roughly 4.2% after tax at a 30% marginal rate — which can invert a ranking against a lower-yielding grower or a buyback-returning company. Comparing pre-tax dividend yield against post-tax total return is exactly the kind of like-for-unlike comparison this skill exists to prevent.
2. **The price drops by approximately the dividend on the ex-date.** "Buying for the dividend" converts capital into taxable income and nothing else. Note ex-date versus record date carefully (Section 22).

---

## 18. The transaction cost stack: STT, stamp duty, round trip

Model the **full stack for the actual strategy**, then express it as a round-trip percentage and multiply by expected annual turnover.

**India components (rates change; verify each):** Securities Transaction Tax — different rates for delivery buy and sell, intraday sell, futures sell, options premium and options exercise; exchange transaction charges; SEBI turnover fee; stamp duty on the buy side; GST on brokerage and on charges; DP charges levied per sell instruction (a flat fee, so brutal on small sells); brokerage itself.

**US components:** SEC Section 31 fee on sales, FINRA TAF, commissions (often zero at retail, but payment-for-order-flow shows up as worse execution), ADR custody/pass-through fees on foreign holdings, and currency conversion spreads on any cross-border trade.

| Cost concept | How to compute | Indicative magnitude | Why it matters |
|---|---|---|---|
| Round-trip explicit cost | Sum of all statutory + broker charges, buy + sell | Tens of bps for Indian delivery equity | Charged on turnover regardless of profit |
| Round-trip implicit cost | Half-spread × 2 + market impact at your size | Often larger than explicit cost in smallcaps | The cost nobody invoices you for |
| Annual friction drag | Round-trip cost × portfolio turnover | A 4x-turnover strategy can lose 1.5–3% a year before tax | Frequently exceeds the alpha being chased |

**Why it matters.** STT is levied on turnover, not profit — it is a guaranteed drag that scales linearly with churn and is paid in losing years too. The derivative structures deserve specific attention: options held to expiry have historically been charged STT on a basis far larger than the premium, which can make a strategy that looks profitable on the P&L unprofitable in reality. Any recommendation implying frequent rebalancing must state the friction cost explicitly.

---

## 19. Cross-border: withholding, treaty relief, PFIC, estate tax

This is where the largest avoidable losses occur, and none of it appears in any financial statement.

**Dividend withholding and treaty relief.** Foreign dividends are withheld at source. Treaty relief is not automatic — it requires the right form filed *in advance* (a W-8BEN for a non-US person receiving US income, for example), and the foreign tax credit requires the right form filed with the home return (India: Form 67, filed within the prescribed deadline). Indian residents holding US equities are typically withheld at the treaty rate under the India–US DTAA rather than the statutory non-resident rate, and can claim credit — but only if the paperwork was done. **Verify current rates and deadlines.** People routinely surrender double-digit percentages of their dividend income to a missing form.

**PFIC (US persons only, and it is punitive).** A non-US pooled investment — a foreign mutual fund, a UCITS ETF, many foreign holding and investment companies — is generally a Passive Foreign Investment Company for a US taxpayer. The default section 1291 regime taxes "excess distributions" at the highest ordinary rate with a compounding interest charge on deferred amounts, and requires annual Form 8621 filing. QEF and mark-to-market elections can mitigate this but require information the fund may not provide. Practical consequence for this skill: **a US-taxable holder should generally not be steered into non-US pooled vehicles**, and even foreign operating companies must be screened for the income and asset tests if they hold large passive/cash balances. Ordinary foreign operating businesses are usually not PFICs — cash-heavy shells and post-IPO companies sitting on large raises can be.

**Situs-based estate tax (frequently overlooked and potentially catastrophic).** Estate tax can be levied by the country where the *asset* is situated, regardless of where the owner lives or whether their home country has an estate tax. US-situs assets — including directly held US shares — expose a non-resident non-citizen's estate to US estate tax above a very low exemption threshold (far below the domestic exemption), at rates rising to 40%, and India has no estate-tax treaty with the US to relieve it. UK-situs assets carry an analogous inheritance-tax exposure. **This is a structural reason a large direct US-stock holding may be better held through a non-US-situs wrapper** — but that is a legal and tax-planning decision for a qualified professional, and this file's job is to flag the exposure and its size, not to design the structure. Never present a large foreign-equity allocation without naming this.

**India-specific outbound and NRI items.** Remittances abroad fall under the LRS annual limit with TCS on outward remittance above a threshold (verify current rate and threshold). Foreign assets and foreign income must be disclosed in **Schedule FA** of the Indian ITR — non-disclosure carries penalties under black-money legislation that can dwarf the investment itself, and applies even to loss-making or nil-income holdings. For NRIs investing in India: TDS is deducted on capital gains at source (often on gross gains, locking up capital until a refund a year later), PIS/non-PIS account rules apply, and NRE versus NRO determines repatriability.

---

## 20. Loss set-off, carry-forward and harvesting

Know the hierarchy before recommending any realisation.

**India (indicative; verify).**
- Short-term capital loss sets off against **both** STCG and LTCG.
- Long-term capital loss sets off **only** against LTCG.
- Unabsorbed losses carry forward eight assessment years — **but only if the return is filed by the due date.**
- Speculative (intraday) losses set off only against speculative gains and carry forward four years.
- There is **no wash-sale rule**, so an immediate repurchase is permitted — but weigh it against GAAR and against the round-trip STT/brokerage cost of the manoeuvre.
- Harvest **gains** as well as losses: realise gains up to the annual LTCG exemption each year to step up cost basis for free.

**US (indicative; verify).** The **wash-sale rule** disallows a loss if a substantially identical security is bought within 30 days before or after the sale — the opposite of India's position, and the single most common cross-jurisdiction mistake. Capital losses carry forward indefinitely, with a limited annual offset against ordinary income.

**Why it matters.** Filing one day late in India permanently forfeits that year's loss carry-forward — a pure paperwork destruction of real value. Getting the set-off order wrong wastes short-term losses (which could have sheltered gains taxed at the higher short-term rate) against long-term gains taxed at the lower one. And harvesting gains up to an annual exemption is free basis step-up that most investors never claim. Plan before the tax-year end (31 March in India, 31 December in the US), not after.

---

## 21. Custody, demat and account hygiene

Custody failures, not stock selection, cause a large share of permanent retail losses. Check:

- **Reconcile the depository, not the broker.** India: pull the Consolidated Account Statement from CDSL/NSDL and match it to the broker ledger. This is the only independent verification that the shares you think you own exist in your name.
- **Nomination** registered on every demat account, trading account and mutual fund folio. Estates regularly cannot claim holdings without it.
- **Account type:** confirm holdings are not in a pooled or margin-funded account where they can be re-pledged.
- **POA versus DDPI (India):** a broad Power of Attorney historically allowed brokers wide latitude over client securities; the Demat Debit and Pledge Instruction narrows it to specific purposes. Know which you signed. Confirm the margin-pledge flow is used rather than title transfer.
- **KYC, bank mandate and contact details current.** Lapsed KYC freezes accounts; a stale address breaks corporate-action notices.
- **IEPF (India):** dividends unclaimed for seven consecutive years — and **the underlying shares with them** — are transferred to the Investor Education and Protection Fund. Recovery is possible but slow. Check for any unclaimed-dividend history on inherited or long-dormant holdings.

---

## 22. Settlement, record dates and response obligations

**Settlement cycle (verify current):** India operates on T+1 with an optional same-day (T+0) segment for a specified set of stocks; the US moved to T+1; several other markets remain T+2 and are migrating. The cycle directly determines corporate-action eligibility.

**Derive the cum-date rather than memorising it.** To receive an entitlement you must be on the register on the record date, which means your purchase must have *settled* by then. Under a T+1 cycle, a trade must therefore be executed no later than one trading day before the record date — so the ex-date falls on the record date itself, whereas under T+2 it fell a day earlier. Confirm against the specific corporate-action circular for every event, because this convention shifted when settlement cycles changed and stale guidance is everywhere.

**The error to prevent:** buying *on* the record date gets you nothing except the ex-date price drop. This is one of the most common and most entirely avoidable retail mistakes, and it is expensive around rights entitlements and buyback record dates where the entitlement value is material.

**Response obligations — corporate actions that require you to act, with deadlines:**

| Event | Required action | Consequence of inaction |
|---|---|---|
| Rights issue | Subscribe, or sell the REs before the window closes | REs lapse worthless — total loss of entitlement value |
| Tender buyback | Submit the tender through the broker before close | Forgo the premium and the small-shareholder acceptance edge |
| Open offer | Tender by the deadline | May be left holding a stub in a controlled or delisting company |
| Voluntary delisting | Tender in reverse book building or in the exit window | Left holding an unlisted, largely unsaleable security |
| Scheme of arrangement | Usually automatic, but track listing of the resulting entity and apportion cost basis | Overstated capital gain when the broker shows zero cost |

**Margin and settlement penalties.** Understand upfront/peak margin requirements, short-delivery auction mechanics and the auction settlement price. Short delivery pushes your sale into an auction where the settlement price can be far worse than your intended exit, and peak-margin shortfalls attract penalties that compound within a single day.

---

## 23. Sector translation: where this lens inverts

Apply this before drawing any conclusion from Sections 7–14. The standard reading of "dilution is bad" and "high payout is good" breaks in specific sectors.

- **Banks and NBFCs.** Equity issuance is not a symptom of weakness — regulatory capital is the raw material of the business, and a growing lender *must* raise. The correct test is **issue price versus book value per share**: raising above 1x P/B is accretive to book value per share and enables growth; raising below book destroys per-share value even when the raise is necessary. Judge a QIP by that arithmetic, not by the dilution percentage. Watch also for regulator-mandated capital raises and promoter-dilution mandates (India: RBI shareholding norms), which are timing-forced, not opportunistic.
- **Insurers.** Similar capital logic on solvency ratio rather than book value; growth in new business consumes capital before it produces earnings.
- **REITs and InvITs (India) / REITs (US).** Distributions are not dividends and are **not taxed as a single stream**. An Indian REIT/InvIT distribution is split into interest, dividend, rental and return-of-capital components with different tax treatment for each, and the return-of-capital portion reduces the unit cost basis rather than being taxed currently. Computing an after-tax yield requires the distribution breakup from the trust, not the headline yield. These vehicles also distribute nearly all cash flow by regulation, so they fund growth by issuing units continuously — routine dilution that must be judged on NAV accretion, not avoided.
- **Miners and commodity producers.** Equity issuance to fund development is structurally normal and pre-production companies dilute relentlessly; model dilution per unit of reserve added, not the raw share-count increase. Commodity ETF and index flows can dominate the tape independently of company news.
- **PSUs (India).** Government shareholding is a standing supply overhang — OFS tranches, strategic disinvestment and buyback-for-treasury decisions are policy events with announced dates, not market events. Divestment intent should sit permanently on the supply calendar.
- **Smallcaps and SME-platform listings (India).** Every mechanic in this file binds hardest here: surveillance categories, tiny float, low delivery, wide bands, and lot-size constraints on the SME platform. The tradeability gate should be a genuine kill criterion at this size, not a caveat.
- **Recently listed companies anywhere.** The lock-in calendar (Section 13) frequently dominates fundamentals for the first 12–18 months. Do not compare a post-IPO chart to a seasoned peer's without it.

---

## Checklist

- [ ] Run the tradeability gate before deep work: surveillance status, band, ADV, impact cost, delivery %, free float.
- [ ] India: check current ASM / GSM / ESM lists, note stage, date applied, consequences and next review date.
- [ ] Identify the applicable price band; count locked-circuit days separately from circuits touched with volume.
- [ ] India: compute delivery % over 30/90/250 days against sector and own history; flag volume spikes with collapsing delivery.
- [ ] Compute median daily traded value and days-to-exit at 10–20% participation; stress it at 30–50% of normal ADV.
- [ ] Check suspension and delisting-watchlist history; know the market-wide circuit-breaker rules if using leverage or stops.
- [ ] Compute true free float (net of promoter, lock-in, strategic, pledged); track institutional vs retail composition shift.
- [ ] Build the dilution map: every enabling resolution, QIP, preferential issue, warrant, convertible and ESOP tranche.
- [ ] Restate EPS, P/E and market cap on the fully diluted share count; compute the 5–7 year dilution CAGR.
- [ ] Judge every QIP and preferential allotment by allottee identity and price versus floor, not by size.
- [ ] Check warrant exercise-versus-lapse history — promoter forfeiture of the 25% upfront is a strong negative signal.
- [ ] Hunt for reset/ratchet clauses and for out-of-the-money convertibles maturing as cash liabilities.
- [ ] For rights issues: compute TERP, note the RE window, and check whether promoters are subscribing or renouncing.
- [ ] Verify all price history and per-share metrics are adjusted for bonuses, splits and consolidations.
- [ ] Classify buybacks as tender or open market; estimate acceptance ratio; check funding source and after-tax treatment.
- [ ] Build the 24-month lock-in and supply calendar, sized in shares, % of float and days of ADV.
- [ ] Estimate index inclusion/exclusion flow in days of ADV; separate announcement date from effective date.
- [ ] Check for live open offers, delisting proposals or schemes; model the formula price, not your valuation.
- [ ] Verify capital-gains holding period, rates and thresholds against current law for the holder's jurisdiction and residency.
- [ ] Check the holding-period clock before recommending any exit; split calculations across mid-year rule changes.
- [ ] Compute after-tax dividend yield at the holder's marginal rate before comparing yield to any total-return alternative.
- [ ] Model the full round-trip cost stack and multiply by expected turnover; report the friction drag explicitly.
- [ ] For foreign holdings: confirm withholding rate, treaty form filed in advance, and foreign tax credit form and deadline.
- [ ] Screen US-taxable holders for PFIC exposure in any non-US pooled vehicle; flag Form 8621 obligations.
- [ ] Flag situs-based estate-tax exposure on large direct US or UK holdings; refer the structuring to a professional.
- [ ] India: confirm Schedule FA disclosure of all foreign assets, LRS limits and TCS on outward remittance.
- [ ] Apply the correct loss set-off order; note India has no wash-sale rule while the US does; file on time to preserve carry-forward.
- [ ] Harvest gains up to any annual exemption as well as losses, before the tax-year end.
- [ ] Reconcile depository statement against broker ledger; verify nomination, KYC, DDPI scope and any unclaimed-dividend/IEPF history.
- [ ] Derive the last cum-date from the current settlement cycle for every corporate action; never buy on the record date for the entitlement.
- [ ] List every corporate action requiring a shareholder response, with its deadline and the cost of inaction.
- [ ] Apply the sector translation: for banks judge raises on price versus book; for REITs/InvITs use the distribution breakup, not headline yield; for PSUs treat divestment as standing supply.
- [ ] State gross and net-of-cost, net-of-tax expected return in the report — and the date of the tax rules applied.
