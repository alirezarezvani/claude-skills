# Return on capital, DuPont decomposition and the arithmetic of compounding

Use this when: you are at Stage 4 with a clean set of financials and need to establish how much the company earns on the money tied up in it, whether that return exceeds its cost of capital, and whether the next rupee invested will earn the same as the last.

This is the intellectual centre of the skill. Margin tells you what a company keeps out of each rupee or dollar of sales; return on capital tells you what it earns on the money required to make that sale, and only the second one compounds. A business earning 35% on capital funds 10% growth out of a quarter of its profit and hands the rest to owners; a business earning 11% must plough back almost everything to grow at the same rate and returns nothing. That difference — not the margin, not the growth rate — separates a compounding machine from a treadmill, and it is invisible on the income statement. Everything below answers three questions in order: **what is the true return on capital, is it above the cost of capital, and will incremental capital earn the same?**

## Contents

- [0. Sector gate — where this arithmetic breaks](#0-sector-gate--where-this-arithmetic-breaks)
- [1. The core argument: why a 20% margin can beat a 30% margin](#1-the-core-argument-why-a-20-margin-can-beat-a-30-margin)
- [2. Which return metric to use, and when](#2-which-return-metric-to-use-and-when)
- [3. Building NOPAT properly](#3-building-nopat-properly)
- [4. Defining invested capital, and the adjustments that decide the answer](#4-defining-invested-capital-and-the-adjustments-that-decide-the-answer)
- [5. ROIC versus WACC: the spread is the whole game](#5-roic-versus-wacc-the-spread-is-the-whole-game)
- [6. DuPont: 3-step and 5-step](#6-dupont-3-step-and-5-step)
- [7. Asset turnover and capital efficiency](#7-asset-turnover-and-capital-efficiency)
- [8. How much of the return is just leverage](#8-how-much-of-the-return-is-just-leverage)
- [9. Return on incremental invested capital (ROIIC)](#9-return-on-incremental-invested-capital-roiic)
- [10. Cash returns: is the ROIC real](#10-cash-returns-is-the-roic-real)
- [11. Tangible versus total capital: the goodwill effect](#11-tangible-versus-total-capital-the-goodwill-effect)
- [12. Consistency and durability across a full cycle](#12-consistency-and-durability-across-a-full-cycle)
- [13. Normalisation: what the mid-cycle return actually is](#13-normalisation-what-the-mid-cycle-return-actually-is)
- [14. Peer and cross-cycle benchmarking](#14-peer-and-cross-cycle-benchmarking)
- [15. Fade rate and the competitive advantage period](#15-fade-rate-and-the-competitive-advantage-period)
- [16. Segment and divisional returns](#16-segment-and-divisional-returns)
- [17. Buybacks, dividends and denominator effects](#17-buybacks-dividends-and-denominator-effects)
- [18. Fourteen ways a reported ROIC lies](#18-fourteen-ways-a-reported-roic-lies)
- [19. India versus US conventions](#19-india-versus-us-conventions)
- [20. What to put in the report](#20-what-to-put-in-the-report)
- [Checklist](#checklist)

**Every range in this file is indicative only.** Return levels are a function of sector, capital intensity, accounting regime, the rate cycle and the local cost of capital. A 12% ROIC is excellent for a regulated utility, roughly value-neutral for an Indian manufacturer facing a 12–13% WACC, and poor for asset-light software. Peer comparison and the company's own 5–10 year record override every absolute band printed here. If you quote a band, quote it as a starting reference and then state what the actual peer set earns.

## 0. Sector gate — where this arithmetic breaks

Run this before computing anything. For several sectors the standard return ratios are not merely less useful — they are undefined, inverted, or measuring the wrong thing.

| Sector | What breaks | Use instead |
|---|---|---|
| **Banks** | Debt is raw material, not financing. Invested capital, NOPAT, EV and ROIC are meaningless; a bank is *supposed* to run 8–15x assets/equity. | ROA (indicatively 1.0–1.8%) and ROE (12–18%) read **together with** CET1/CAR, plus NIM, cost-to-income, credit cost, RoRWA. `references/sectors/banks.md` |
| **NBFCs / HFCs** | Same. Leverage is the product. DuPont still works, but only in the lender form. | ROA decomposed into NIM + fees − opex − credit cost, × equity multiplier; leverage against the regulatory ceiling. `references/sectors/nbfc.md` |
| **Insurers** | New-business strain depresses reported ROE precisely when the company is writing profitable growth. Invested capital is not meaningful against float. | Life: ROEV, VNB margin, operating variances. General: combined ratio, ROE ex-investment gains. `references/sectors/insurance.md` |
| **REITs / InvITs** | Assets are carried at fair value and the asset *is* the business, so ROIC collapses toward the cap rate by construction. | AFFO yield, NOI yield on cost, cap rate vs cost of debt, LTV. `references/sectors/realestate-reit.md` |
| **Miners, commodity producers, refiners** | ROCE at spot prices is procyclical nonsense — highest at the top, negative at the bottom, and neither is the business. | ROCE on **mid-cycle** realised prices; return per tonne; all-in sustaining cost position. `references/sectors/metals-mining.md` |
| **Regulated utilities, transmission** | The return is *set by a regulator*, not earned competitively. India: CERC/SERC norms fix an allowed RoE on approved equity. US: allowed ROE per rate case. | Allowed vs achieved RoE, regulated asset base growth, regulatory assets/under-recoveries. `references/sectors/utilities-power.md` |
| **Holdcos and conglomerates** | Consolidated ROIC blends unrelated businesses into a number no manager can act on. | Segment returns (§16) and sum-of-the-parts. `references/sectors/holdco-assetmgr.md` |
| **Negative-invested-capital businesses** (exchanges, subscription, ticketing, quick commerce, some platforms) | Customer float and payables fund the business, so invested capital approaches zero or goes negative and ROIC becomes infinite or nonsensically negative. | Say so explicitly — it is a *strength*, not a data error. Use ROE, return on tangible capital with a stated floor, and cash generated per unit of fixed capital. |
| **Loss-making / early-stage** | Negative NOPAT makes every return ratio uninterpretable. | Unit economics, contribution margin, cohort payback, path to first positive ROIC. `references/13-situations.md` |
| **Airlines, shipping, retail chains, hotels** | Lease structures shift capital off the denominator and distort EBIT differently under each regime. | Lease-adjusted invested capital, always. ROIC and EV/EBITDAR on the capitalised base. |

## 1. The core argument: why a 20% margin can beat a 30% margin

The identity that governs the entire skill:

```
ROE  =  Net margin   ×  Asset turnover   ×  Equity multiplier
        (NI/Sales)      (Sales/Assets)      (Assets/Equity)

ROIC ≈  NOPAT margin ×  Capital turnover
        (NOPAT/Sales)   (Sales/Invested capital)
```

Margin is **one of three terms**. A company earns a superb return on capital with a thin margin if it turns capital over quickly, and a mediocre return with a fat margin if each unit of sales demands enormous fixed assets and working capital.

**Illustration 1 — same return, opposite margins** (generic and illustrative).

| | Distributor | Branded manufacturer |
|---|---|---|
| NOPAT margin | 4% | 20% |
| Sales / invested capital | 5.0x | 1.0x |
| **ROIC** | **20%** | **20%** |

Identical economics. The 4%-margin business is not worse; it is a different machine reaching the same place by turning capital five times instead of once. Ranking these two on margin teaches you nothing.

**Illustration 2 — the inversion, where the low-margin business is materially better.**

| | Capital-light distributor | Capital-heavy specialty producer |
|---|---|---|
| EBIT margin | 6% | 25% |
| Sales / invested capital | 4.0x | 0.5x |
| Pre-tax return on capital | 24% | 12.5% |
| After 25% tax | **18%** | **9.4%** |
| WACC (illustrative, India) | 12% | 12% |
| **Verdict** | **+6 pts of spread — compounding** | **−2.6 pts — destroying value while growing** |

The 6%-margin business earns roughly double the return of the 25%-margin business and is the only one of the two creating value. This is the OPM error stated as arithmetic: **margin is a ratio to sales, and shareholders do not own sales — they own capital.**

**Illustration 3 — three companies with an identical 18% ROE and three different risk profiles.**

| | Net margin | Asset turnover | Equity multiplier | ROE |
|---|---|---|---|---|
| Quality operator | 12% | 1.2x | 1.25x | 18% |
| Efficiency operator | 3% | 2.4x | 2.5x | 18% |
| Leveraged asset owner | 9% | 0.5x | 4.0x | 18% |

The first is self-funding and survives a downturn. The third needs continuous credit access; a 25% fall in operating profit destroys its interest cover and its ROE mean-reverts violently. **Never compare headline ROEs without decomposing them.**

Two implications to carry through the whole analysis:

1. **Where the margin sits within its sector matters far more than the margin.** A 20% margin in distribution is an outlier; 30% in enterprise software is unremarkable. Establish the sector distribution first (`references/10-peer-set.md`).
2. **Growth is only valuable above the cost of capital.** Revenue growth funded at sub-WACC returns destroys value while making sales, EBITDA and often EPS look better every year. This is the most common way a "growth story" loses money for its shareholders.

## 2. Which return metric to use, and when

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| **ROE** | Net profit attributable to owners ÷ average shareholders' equity (exclude minority interest from both) | India: >15% good, >20% strong, sustained >25% rare without leverage. US: >15% good. Financials have their own bands | The equity holder's return, but contaminated by leverage, buybacks and one-offs. Never quote it without the DuPont split |
| **ROCE (pre-tax)** | EBIT ÷ capital employed, where capital employed = total assets − current liabilities ≈ net worth + total debt + lease liabilities | India: >15% decent, >20% good, >25% strong. Pre-tax, so **not** comparable to after-tax ROIC | The default Indian convention (screener.in, most sell-side notes). Being pre-tax, it is the cleaner metric for cross-period comparison when tax regimes change |
| **ROIC (after-tax)** | NOPAT ÷ average invested capital (§3, §4) | Judge against WACC, not an absolute band. Broadly: US >12%, India >14–15% clears typical hurdles | The correct economic measure and the only return figure directly comparable to the cost of capital |
| **ROA** | Net income ÷ average total assets | Industrials 5–10%; utilities/telecom 2–5%; banks 1.0–1.8% | Leverage-free view of asset productivity. The ROE−ROA gap *is* the leverage contribution |
| **ROTIC / return on tangible capital** | NOPAT ÷ invested capital excluding goodwill and acquired intangibles | Structurally higher than ROIC; the *gap* is the signal | Shows the operating economics stripped of what was paid to acquire them |
| **ROTE** | Net income ÷ average tangible equity | Banks 12–18% | Standard for financials, where goodwill is not loss-absorbing capital |
| **CROIC / CFROI** | FCF (or CFO − maintenance capex) ÷ invested capital | Within roughly 70–100% of ROIC on a 5-year average | Tests whether accounting returns convert into cash owners can actually have |
| **Return on gross invested capital** | NOPAT ÷ invested capital using **gross** (pre-accumulated-depreciation) fixed assets | Materially lower than net-book ROIC for old asset bases | Replacement-cost sanity check. A fully depreciated plant shows a spectacular net-book return and a poor one on what rebuilding costs |
| **ROIIC** | Δ NOPAT ÷ Δ invested capital over 3- and 5-year windows | Should be ≥ current ROIC and comfortably > WACC | The forward-looking number: does continued reinvestment compound or dilute |
| **Economic profit / EVA** | (ROIC − WACC) × invested capital | Positive and growing in absolute currency | Converts a percentage into money. A firm can raise ROIC by shrinking and still create less value |
| **RoRWA** (financials only) | Net profit ÷ average risk-weighted assets | Indian banks: 1.5–2.5% is strong | Risk-adjusted, and the only honest comparison across lenders with different books |

Use **at least three**: ROCE or ROIC for the economics, ROE for the equity holder's view, CROIC for the reality check. Where they diverge is where the analysis lives.

## 3. Building NOPAT properly

NOPAT is the profit the business would earn with no debt — the numerator that matches a denominator financed by debt *and* equity.

```
  EBIT (reported)
+ Operating-lease interest        IFRS 16 / Ind AS 116 already exclude it from EBIT;
                                  for US GAAP filers add back the imputed interest inside lease cost
+ R&D expensed this year          only if you also capitalise R&D in the denominator (§4)
− Amortisation of capitalised R&D
+ Impairments and non-recurring charges;  − non-recurring gains
+ Pension service-cost normalisation where the disclosed charge is distorted
= Adjusted EBIT (NOPBT)
× (1 − normalised cash tax rate)
= NOPAT
```

Rules that decide whether the number is usable:

- **Use a normalised cash tax rate**, not the statutory rate and not one year's effective rate. Take cash taxes paid ÷ pre-tax profit over 3–5 years and sanity-check against statutory. **India:** a company that elected the concessional regime (Section 115BAA, ~25.2% effective including surcharge and cess; ~17.2% for qualifying new manufacturing under 115BAB) is not comparable to its own pre-FY20 history at ~34.9%. **US:** the 2018 cut from 35% to 21% federal breaks a 10-year after-tax series the same way. For cross-cycle work, hold the tax rate constant or use pre-tax ROCE.
- **Do not add back stock-based compensation.** SBC is a real cost that transfers value from existing owners. It also creates no invested capital, which is exactly why heavy-SBC firms show flattered ROIC — note the distortion rather than removing the cost (`references/03-earnings-quality.md`).
- **Match non-operating income to non-operating assets.** Treasury income on surplus cash, rent from non-operating property, and share of profit from associates must either stay with their assets in the denominator or be removed from both sides. Indian companies with large treasury books routinely get this wrong in their own investor decks.
- **Minority interests.** Consolidated EBIT includes 100% of a partly owned subsidiary that owners do not fully own. Either use consolidated NOPAT with capital including minority interest, or strip both. Never mix.

## 4. Defining invested capital, and the adjustments that decide the answer

Two routes to the same number. **Compute both and reconcile** — a gap means something is misclassified.

```
Operating route:    Net working capital (excl. excess cash, excl. debt in current liabilities)
                  + Net PP&E + CWIP / construction in progress
                  + Right-of-use (capitalised lease) assets
                  + Goodwill and acquired intangibles      [total-capital version only]
                  + Capitalised R&D / brand investment      [where applicable]
                  − Non-interest-bearing operating liabilities
                  = Invested capital

Financing route:    Total debt + lease liabilities + shareholders' equity + minority interest
                  − Excess cash and non-operating investments
                  = Invested capital
```

| Adjustment | What to do | Why it changes the conclusion |
|---|---|---|
| **Operating leases** | IFRS 16 and Ind AS 116 (mandatory for Indian listed entities from FY2020) already capitalise them. **US GAAP (ASC 842) capitalises the balance sheet but keeps the entire lease cost in operating expense** — so a US filer's EBIT is depressed relative to an IFRS filer's for identical economics. For pre-FY2020 Indian data and pre-2019 US data, capitalise at ~8x annual rent or the PV of disclosed commitments | Retail, QSR, airlines, hotels, logistics and hospital chains look "asset-light" purely through lease accounting; unadjusted ROIC can be double the true figure. It also silently breaks any 10-year ROCE series at the transition year |
| **Goodwill and acquired intangibles** | Compute ROIC both with and without (§11). Not amortised under Ind AS or US GAAP, so goodwill sits in capital permanently until impaired | Excluding goodwill measures operations; including it measures capital allocation. Both are needed |
| **Cumulative impairments and write-offs** | Add back cumulative goodwill impairments, restructuring write-offs and discontinued-operation losses to the denominator | Otherwise the company is *rewarded* for destroying capital: writing off a bad acquisition shrinks the denominator and lifts ROIC permanently |
| **Excess cash** | Subtract cash above an operating requirement (roughly 2–5% of revenue, sector-dependent) and state the assumption | Net-cash Indian IT services and pharma names show ~25% ROE but 40%+ ROIC once idle cash is removed. That gap is the size of the capital-allocation problem and should be reported as such |
| **Non-operating investments** | Remove associates, listed holdings, group-company loans and surplus real estate — and remove the matching income from NOPAT. **India:** Section 186 loans, guarantees and investments to group entities belong here | Endemic in Indian promoter groups. Leaving them in understates the operating business's true return and hides where capital actually went |
| **CWIP / assets under construction** | Report ROCE both including and excluding CWIP | A cement or capital-goods company mid-expansion earns nothing on CWIP but carries it. Excluding it shows the return on *working* assets; including it shows what shareholders are getting today. **India:** Schedule III requires CWIP ageing plus disclosure of projects overdue or over budget — read it before assuming the CWIP will ever earn |
| **R&D and brand spend** | For intangible-driven businesses (software, pharma, branded consumer), capitalise and amortise over an economic life (3–5 yrs software, 5–10 yrs pharma) and add to capital | Expensing all R&D leaves the firm's principal asset out of the denominator. This is the largest single source of overstated ROIC in US technology and pharma |
| **Revaluation reserves (India)** | If PPE is carried at revalued amounts under Ind AS 16, flag it; consider restating to historic cost for peer comparability | Revaluation inflates equity and capital employed, mechanically depressing ROE and ROCE with no economic change |
| **Average vs point-in-time capital** | Use the **average** of opening and closing capital; for ROIIC and acquisition years use **beginning-of-period** capital | Year-end capital after a December acquisition pairs a full year of old NOPAT with a full year of new capital, understating the return; the reverse flatters it |
| **Gross vs net fixed assets** | Cross-check with a gross-invested-capital ROIC | An old, fully depreciated base produces a return no one could earn building the same plant today — including the company when it must replace it |
| **JVs and associates** | Equity-method income sits in the numerator while the investment sits in the denominator: keep both, strip both, or proportionately consolidate | Common in Indian infrastructure, cement and tower structures, where much of the economics sits outside the consolidated operating lines |

**Apply whatever you choose identically to the peer set and to every year of history, and state the definition in the report.** An ROIC computed on a different basis from its comparison set is worse than no ROIC at all.

## 5. ROIC versus WACC: the spread is the whole game

A business creates value only when ROIC > WACC. Below that line growth destroys value: every additional rupee invested returns less than it cost to raise, while revenue, EBITDA and often EPS keep rising.

```
Economic profit = (ROIC − WACC) × Invested capital
Value creation  = economic profit, sustained and growing, across the competitive advantage period
```

**Estimating WACC without false precision.** Derive it from current market data at the time of analysis — never from memory — and present it as a range.

- **Cost of equity** = risk-free rate + beta × equity risk premium. **India:** current 10-year G-sec yield with an ERP usually taken at 5.5–7%, which has historically put large-cap cost of equity in a low-to-mid-teens range. **US:** current 10-year Treasury with an ERP usually 4.5–5.5%, giving a high-single to low-double-digit cost of equity. These move with the rate cycle — state the inputs and the date.
- **Cost of debt** = the company's actual marginal borrowing rate (interest-rate disclosure or recent issuance), after tax. Not the historical average rate on legacy debt.
- Weight by **market** values of debt and equity, not book.
- **Do not present WACC to two decimals.** Use a range (e.g. "11–13%") and test the conclusion at both ends. If the value-creation verdict flips inside your own WACC range, that *is* the finding — say so.
- **The India/US gap is structural.** A higher risk-free rate means an Indian company needs a materially higher ROIC to create the same economic value as a US peer. A 12% ROIC that clears the bar comfortably in the US can be value-neutral in India. Never compare raw ROIC across markets — compare the spread.

**Report:** ROIC, WACC range, spread in basis points, economic profit in absolute currency, and how many of the last 7–10 years had a positive spread.

**Red flags:** ROIC persistently below WACC while capex or M&A accelerates; a positive spread narrowing year after year; management emphasising adjusted EPS or revenue growth while economic profit stagnates; a spread that was positive only during a demand boom.

## 6. DuPont: 3-step and 5-step

**3-step** — answers *what kind of business is this?*

```
ROE = (Net income / Sales) × (Sales / Total assets) × (Total assets / Equity)
    =    Net margin        ×    Asset turnover      ×    Equity multiplier
```

**5-step** — answers *where is the ROE actually coming from?*

```
ROE = (NI/EBT) × (EBT/EBIT) × (EBIT/Sales) × (Sales/Assets) × (Assets/Equity)
    = Tax burden × Interest burden × Operating margin × Asset turnover × Leverage
```

Worked illustration: 0.75 × 0.85 × 14% × 1.2 × 1.5 = **16.1% ROE**. Now the next year the company reports 18.5%. Rerun the terms: if operating margin and turnover are unchanged and the gain came from the interest burden rising to 0.92 (cheaper refinancing) and leverage to 1.7, the business did not improve at all — the balance sheet and the rate cycle did. That distinction is entirely invisible in the headline number.

**How to run it.**

1. Compute all five terms for each of the last 5–10 years, one row per year.
2. Identify which term moved most, in percentage-point contribution to the change in ROE.
3. Classify the ROE as **operations-driven** (margin × turnover) or **financing-driven** (tax burden, interest burden, leverage).
4. Run the same table for 2–3 peers. Firms with the same ROE and different decompositions are not comparable investments.
5. **Financials:** use the lender form — ROE = ROA × equity multiplier, with ROA broken into NIM + fee income − opex − credit cost, each as a % of average assets.

**What each term tells you.**

| Term | Rising is good when | Rising is a warning when |
|---|---|---|
| Tax burden (NI/EBT) | A permanent regime change (India: 115BAA election) or a genuine structural mix shift | It reflects one-off credits, MAT credit utilisation, an expiring tax holiday about to reverse, or aggressive positions under dispute |
| Interest burden (EBT/EBIT) | Debt has genuinely been repaid | It reflects refinancing at temporarily low rates, or interest capitalised into CWIP instead of expensed |
| Operating margin | Pricing power, mix, or operating leverage that persists | It comes from an input-cost trough, a one-off, capitalised costs, or under-spend on maintenance and marketing |
| Asset turnover | Genuine utilisation gains | It reflects a shrinking asset base from write-offs, or leasing that moved assets off balance sheet |
| Equity multiplier | Almost never good in isolation | Always. Rising leverage is the cheapest way to manufacture ROE and the fastest way to lose the company |

**Red flags:** ROE rising while ROIC is flat or falling (the whole gain is financing); declining turnover masked by added leverage; margin expansion later revealed as non-recurring; ROE improving while book value per share stalls.

## 7. Asset turnover and capital efficiency

Turnover is the forgotten half of ROIC and usually the half that explains why a low-margin business is excellent.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
|---|---|---|---|
| **Total asset turnover** | Sales ÷ average total assets | Distribution/retail 2–4x; manufacturing 0.8–1.5x; utilities/telecom 0.3–0.5x | The efficiency term in DuPont. Judge only against sector |
| **Sales / invested capital** | Sales ÷ average invested capital | Cleaner than asset turnover — excludes idle cash and non-operating assets | The term that multiplies with NOPAT margin to give ROIC |
| **Fixed-asset turnover** | Sales ÷ average net PP&E | Track the trend, not the level | Falling fixed-asset turnover alongside rising capex is the classic signature of building into demand that did not arrive |
| **Working capital turnover** | Sales ÷ average net working capital | Sector-dependent; negative working capital is a feature in retail, QSR and subscription | Usually the largest and most controllable lever on ROIC in Indian manufacturing and trading |
| **Capital intensity** | Capex ÷ sales; total assets ÷ sales | Compare capex/sales with depreciation/sales to separate maintenance from growth | Rising intensity without a margin benefit means returns are heading down regardless of this year's number |
| **Physical productivity** | Revenue per employee, per store, per tonne, per bed, per seat-km, per MW | Sector-specific — take it from the sector playbook | The check that survives accounting choices entirely |

Cross-check against the cash conversion cycle in `references/04-balance-sheet-and-cashflow.md`: an inventory or receivables build simultaneously flatters reported profit and depresses turnover, so it shows up on both sides of the ROIC identity.

**Red flags:** asset base growing faster than sales for more than two consecutive years; turnover far below peers with no structural explanation in the business model; turnover improving only because assets were written off or moved into leases.

## 8. How much of the return is just leverage

```
Leverage contribution ≈ ROE − ROA            (percentage points)
Financial leverage index = ROE / ROA         (>1 means leverage is adding)
```

Leverage adds to ROE only while ROIC exceeds the after-tax cost of debt. When that spread inverts — in a downturn, or after refinancing at higher rates — leverage subtracts at the same multiple. The asymmetry is the entire risk.

- **ROIC minus after-tax cost of debt.** Needs to be wide enough to survive a cyclical decline in ROIC. A company earning 11% ROIC and borrowing at 9% pre-tax has almost no cushion, whatever its ROE says.
- **Stress it against the trough.** Take the worst ROIC year of the last decade (§12), recompute interest cover at today's debt level, and check whether the capital structure survives it.
- **Negative or near-zero tangible equity** makes ROE arithmetically meaningless — it explodes as equity approaches zero from above and inverts below it. Several large US consumer and aerospace names have run negative book equity after years of debt-funded buybacks. For those, drop ROE and use ROIC and ROTIC.
- **India:** promoter share pledging is hidden leverage on the equity itself. High pledging plus high financial leverage compounds in a way no return ratio captures (`references/08-governance.md`).

**Red flags:** ROE far exceeding ROIC with the gap widening; rising leverage as the sole driver of ROE growth; debt-funded buybacks lifting leverage and ROE together while ROIC is flat.

## 9. Return on incremental invested capital (ROIIC)

Average ROIC is history. ROIIC is the forecast.

```
ROIIC (3-yr) = (NOPAT_t − NOPAT_t−3) / (Invested capital_t−1 − Invested capital_t−4)
```

Lag the denominator by a year — capital takes time to earn. Use rolling 3- and 5-year windows; single-year ROIIC is noise.

**Worked illustration.** NOPAT rises from 100 to 130 over three years while invested capital rises from 500 to 900.

- ROIC at the start: 100/500 = **20%**
- ROIC now: 130/900 = **14.4%** — still a respectable-looking headline
- ROIIC: 30/400 = **7.5%** — below an 11–12% WACC

Every rupee of new capital is destroying value. The legacy business is subsidising the expansion, and the blended ROIC will keep drifting toward 7.5% as new capital dominates the base — while management reports record profits throughout. **This is the highest-value calculation in this file, and almost nobody runs it.**

**Pair it with the reinvestment rate:**

```
Reinvestment rate = (capex + acquisitions + Δ working capital − depreciation) / NOPAT
Intrinsic NOPAT growth ≈ Reinvestment rate × ROIIC
```

A firm reinvesting 50% of NOPAT at 20% incremental returns compounds at ~10% with no external funding. A firm reinvesting 90% at 8% compounds at ~7% while consuming all its cash and creating nothing. Use the identity to test management guidance: if the promised growth implies a reinvestment rate above 100% of NOPAT, the plan requires debt or dilution — say so explicitly.

**Red flags:** incremental returns below both the historical average and WACC; large capex or acquisition programmes with flat NOPAT three years later; ROIIC falling steadily as the firm scales (saturation or diseconomies); management declining to give returns on specific projects when asked on the concall.

## 10. Cash returns: is the ROIC real

```
CROIC = FCF ÷ invested capital           (state which capex definition)
      or (CFO − maintenance capex) ÷ invested capital
FCF conversion = FCF ÷ NOPAT
```

Accounting ROIC can be inflated by revenue recognised ahead of cash, capitalised operating costs, understated depreciation, or a working-capital build that never unwinds. Cash returns are the audit.

- Compare **5-year average CROIC with 5-year average ROIC**. A persistent gap of more than a few points needs an explanation, and "we are investing for growth" only qualifies if the growth capex is separately identifiable.
- **CFO ÷ net income above 1.0 on a rolling 3–5 year basis** is the baseline; sustained below 0.8 is a serious signal (`references/03-earnings-quality.md`).
- For genuinely growing companies, FCF conversion is legitimately depressed by growth capex and working capital. Separate maintenance from growth capex — depreciation is a crude floor for maintenance — before drawing any conclusion.
- **Accrual ratio** = (NOPAT − FCF) ÷ average invested capital. Rising across several years means an increasing share of the reported return exists only on paper.

**Red flags:** ROIC persistently and materially above CROIC; conversion deteriorating while reported margins improve; capitalised development costs or capitalised interest growing faster than revenue.

## 11. Tangible versus total capital: the goodwill effect

Compute ROIC both ways for any company that has made acquisitions.

- **Return on tangible invested capital** (goodwill and acquired intangibles excluded) = the economics of the operating business.
- **ROIC on total capital** (goodwill included) = the return on what shareholders actually paid, acquisition premiums and all.

The gap is a direct measure of capital-allocation quality. A serial acquirer can run a 40% return on tangible capital and a 9% return on total capital: the businesses are good, the prices paid were not. Roll-ups habitually headline the tangible figure.

Check: goodwill + acquired intangibles as a % of invested capital; the trend in the gap over 5–10 years (widening means premiums rising or acquired performance falling); the history of goodwill impairments, each of which is documentary evidence of overpayment; and whether the company's own "return on capital" disclosure quietly uses the tangible base.

## 12. Consistency and durability across a full cycle

One year's ROIC tells you almost nothing. Pull **7–10 years minimum**, spanning at least one genuine downturn, and compute:

| Statistic | What it tells you |
|---|---|
| Mean and median ROIC | Central tendency — prefer the median where one year is extreme |
| Standard deviation / coefficient of variation | Volatility of returns is the quantitative fingerprint of cyclicality or a fragile competitive position |
| **Minimum (trough) ROIC** | The honest floor of the business and the best single predictor of downside. A company whose worst year is 14% is a different animal from one whose worst year is −3%, whatever their averages |
| Years with ROIC > WACC out of 10 | Value creation is a habit, not an event |
| Peak-to-trough drawdown in ROIC | How much of the return is cyclical rent rather than franchise |
| Trend line through the series | Structural improvement, stability, or slow erosion |

Durable, high, low-volatility returns are the strongest quantitative evidence that a moat exists. Cross-check against the qualitative moat assessment in `references/02-core-factors.md` — if the narrative claims a widening moat and the ROIC has fallen for six years, the numbers win.

**Red flags:** returns clearing WACC only at the top of the cycle; one exceptional year carrying the whole average; no history through a real downturn (recent IPO, post-restructuring, or a business model younger than the last recession); each cycle peaking lower than the last — structural decline dressed as cyclicality.

## 13. Normalisation: what the mid-cycle return actually is

Reported returns are one point in a cycle plus whatever one-offs landed that year. Capitalise sustainable earning power, not the snapshot.

1. **Strip non-recurring items** from NOPAT: restructuring, litigation settlements, disposal gains and losses, impairments, insurance recoveries, translation effects, one-off incentives. List them; do not silently delete them.
2. **Normalise tax** to a sustainable cash rate (§3).
3. **Mid-cycle the margin.** For cyclicals use a multi-year average realised price or spread rather than the current one — an average GRM for a refiner, mid-cycle spreads for a steel producer, a through-cycle credit cost for a lender. Applying spot economics to a cyclical produces the classic trap: lowest P/E and highest ROCE precisely at the top.
4. **Quantify the gap** between reported and normalised ROIC and explain it in one line.
5. **Audit the company's own adjustments.** If management excludes a charge every year for five years, it is a recurring cost of doing business. Recompute without their adjustments and compare.

**Red flags:** returns dependent on a booming end-market or a commodity price; "one-time" items that recur annually; normalised ROIC materially below reported; company-defined adjusted metrics that only ever exclude unfavourable items; a definition of "adjusted" that changed mid-period (`references/07-forensic-red-flags.md`).

## 14. Peer and cross-cycle benchmarking

Absolute return levels mean nothing. Benchmark twice, always.

**Against peers** (build the set with `references/10-peer-set.md`):

- Use the **same cycle window** and aligned fiscal years for every company.
- **Normalise the accounting before ranking.** Lease presentation (IFRS vs US GAAP), R&D capitalisation policy, revaluation, goodwill history and consolidation scope each move ROIC by several points. Ranking un-normalised figures produces confident nonsense.
- Report the **percentile rank** on ROIC, margin and turnover *separately* — that immediately shows whether the company's advantage is a margin story or a turnover story.
- Watch the **trend in relative rank**, which matters more than the level. A company moving from third quartile to first is a different investment from one drifting the other way at the same absolute ROIC.

**Against its own history:** spread versus its own 5- and 10-year average ROIC, and the same for margin and turnover independently. A company can beat its peers while decaying against itself — a sector in structural decline, which the peer comparison alone would miss entirely.

**Red flags:** a peer set containing differently structured or differently regulated businesses; below-peer returns explained away by management narrative; apparent outperformance that vanishes once leverage and accounting policy are equalised.

## 15. Fade rate and the competitive advantage period

High returns attract capital, and capital compresses returns. Excess returns fade toward the cost of capital across most industries, and the *rate* of that fade is one of the largest drivers of intrinsic value — usually larger than next year's growth rate, which is where almost all attention goes.

Assess:

- **The firm's own persistence.** How many consecutive years has ROIC exceeded WACC, and is the spread widening or narrowing? A long, stable record is real evidence.
- **The industry fade pattern.** Some structures resist fade for decades (network effects, regulated monopolies, entrenched distribution, high-switching-cost software, brands in low-innovation categories). Others fade in three years (commodity manufacturing without a cost advantage, hardware, undifferentiated services).
- **The reinvestment runway.** A 25% ROIC on a capital base that cannot grow is worth far less than a 20% ROIC with a decade of reinvestment ahead. Runway × ROIIC is the compounding engine.
- **What breaks it.** Name the specific entrant, technology, regulation or input shift that would compress the return, and what you would observe first.

Then make the assumption **explicit** in valuation (`references/06-valuation.md`): state the competitive advantage period you are using and fade ROIC toward WACC beyond it. A DCF holding today's ROIC constant into perpetuity assumes the company defeats competition forever — usually the single largest source of overpayment.

**Red flags:** implicit assumption of permanently high returns with no identifiable moat; excess returns already fading while the narrative claims the opposite; well-capitalised entrants arriving; industry-wide return compression visible across the whole peer set.

## 16. Segment and divisional returns

Consolidated ROIC is an average, and averages hide the actual decision.

- Compute **ROCE or ROIC per segment**: segment EBIT ÷ segment capital employed (segment assets − segment operating liabilities). **India:** Ind AS 108 disclosure usually includes segment assets *and* liabilities, so segment capital employed is directly computable — use it. **US:** ASC 280 requires segment assets only where regularly reviewed by the chief operating decision maker, so segment capital is often unavailable; fall back on segment margins plus disclosed capex by segment.
- Identify which segments earn **above and below group WACC**, and where **incremental capital** has gone over five years. A high-return core funding chronic losses elsewhere is the commonest form of value destruction in listed conglomerates and is entirely invisible in the consolidated ratio.
- Compare segment capex with segment returns. Capital flowing consistently to the lowest-return segment is a verdict on management (`references/08-governance.md`).
- Segment work is also where **hidden value** appears — a crown-jewel division dragged down in the consolidated number is the basis of a sum-of-the-parts case, a divestiture thesis or a demerger catalyst.

**Red flags:** heavily aggregated or repeatedly redefined segments; a single segment carrying the entire group's returns; loss-making units retained indefinitely with no credible turnaround plan; segment reporting that changed right after a division started underperforming.

## 17. Buybacks, dividends and denominator effects

Capital return is the other half of this domain, and it moves the denominators directly.

- **Buybacks shrink equity, so ROE rises with zero operating improvement.** Illustration: net income 100 on equity 500 is a 20% ROE. A debt-funded buyback halves equity to 250 and interest cuts net income to 92 — ROE now reads 36.8% while ROIC is unchanged or slightly lower and the balance sheet is materially riskier. **If ROE rises and ROIC does not, the improvement is financial engineering.**
- **Test the price paid.** Buybacks above intrinsic value, or at cyclical peaks, transfer value from continuing holders to sellers. Compare the average buyback price with your own valuation range and with the multiple at the time.
- **Judge payout against reinvestment ROIC, not against a payout norm.** Returning capital is accretive precisely when internal opportunities fall below WACC. A company earning 25% incremental returns should be reinvesting; one earning 6% should be distributing. The comparison is payout ratio versus ROIIC (§9).
- **Track share count and book value per share** alongside ROE. Per-share economic progress is the test that survives every denominator game.
- **India specifics:** buybacks are much less common than in the US and are often tender-offer route — check whether promoters tendered, since that is an exit dressed as capital return. Since October 2024 buyback proceeds are taxed in the shareholder's hands, which has pushed many Indian companies back toward dividends; compare **total shareholder yield** (dividends + net buybacks), never either alone.

**Red flags:** ROE boosted by buybacks that hollow out or eliminate book equity; debt-funded buybacks raising leverage and ROE together; management guiding on EPS while book value per share stalls; dividends funded by borrowing while ROIC sits below WACC.

## 18. Fourteen ways a reported ROIC lies

Run this scan before trusting any return figure, including your own.

1. **Write-offs shrank the denominator** — cumulative impairments not added back, so past destruction now flatters returns.
2. **Buybacks shrank equity** — ROE up, ROIC flat (§17).
3. **Leases off the denominator** — pre-IFRS 16 / pre-ASC 842 history, or a US GAAP filer compared with an IFRS filer on EBIT-based ROCE.
4. **R&D and brand expensed** — the principal asset is missing from capital entirely.
5. **Idle cash left in** — depresses ROIC and hides a capital-allocation problem; or quietly netted out without disclosure.
6. **CWIP carried with no earnings yet** — depresses returns mid-expansion; excluding it without saying so inflates them.
7. **Fully depreciated asset base** — a superb net-book return that could never be earned on replacement cost.
8. **Associates and JVs mismatched** — income in the numerator, investment out of the denominator, or the reverse.
9. **Minority interests mismatched** — 100% of a subsidiary's profit against a partial ownership claim.
10. **One-off gains in the numerator** — disposals, insurance recoveries, tax credits.
11. **Tax-rate breaks** — India's 115BAA election, the US 2018 cut, expiring holidays. After-tax series are not continuous through these.
12. **Year-end rather than average capital** — especially distorting in an acquisition year.
13. **SBC-heavy models** — a real cost that creates no capital, so ROIC is structurally overstated versus a cash-paying competitor.
14. **Off-balance-sheet structures** — securitised receivables, JV-held assets, project SPVs, supplier finance. Earnings consolidated, capital not.

Each of these is a reason to state your definition in the report and apply it identically across the peer set.

## 19. India versus US conventions

| Topic | India (NSE/BSE, Ind AS) | US / global (10-K, GAAP/IFRS) |
|---|---|---|
| **Default return metric** | **ROCE, pre-tax**: EBIT ÷ (total assets − current liabilities). The screener.in and sell-side convention, and *not* comparable to after-tax ROIC — always say which you quote | **ROIC, after-tax**: NOPAT ÷ invested capital. Many filers now disclose their own version in the 10-K or at investor days — read their definition before using their number |
| **ROE denominator** | "Net worth" per Schedule III: equity share capital + other equity, excluding revaluation surplus where identifiable and excluding minority interest | Total stockholders' equity attributable to the parent |
| **Leases** | Ind AS 116 from FY2020 — on balance sheet, rent split into depreciation and interest, so **EBIT stepped up at transition**. Pre-FY2020 years must be adjusted before any 10-year ROCE comparison | ASC 842 from 2019 — right-of-use asset and liability on balance sheet, but **operating-lease cost remains a single operating expense**, so US EBIT is lower than an IFRS filer's for identical economics |
| **Tax** | Section 115BAA (~25.2% effective) vs the older ~34.9%; 115BAB for new manufacturing; MAT credits; SEZ and area-based holidays that expire | 21% federal statutory since 2018 (from 35%), plus state taxes, GILTI/FDII, and large valuation-allowance swings |
| **Goodwill** | Not amortised under Ind AS 103; impairment-tested. Amalgamations under NCLT-approved schemes can adjust goodwill directly against reserves — read the scheme, because capital can leave the denominator without touching the P&L | Not amortised since 2001; impairment-only for filers |
| **Capital work-in-progress** | Schedule III mandates **CWIP ageing** and disclosure of projects overdue or over budget — a direct read on whether carried capital will ever earn | Construction in progress sits inside the PP&E note, generally with less granularity |
| **Related-party capital** | Section 186 loans/guarantees/investments to group entities; CARO 3(iii) on loans granted and 3(ix) on end-use of borrowings — the standard route by which capital leaves the listed entity's operating base | Related-party disclosure under ASC 850; typically far smaller in scale for large filers |
| **Basis of accounts** | **Consolidated vs standalone matters enormously.** For any group with subsidiaries, standalone ROE is meaningless. State which you used | Consolidated by default |
| **Units** | ₹ crore / lakh — state the unit on every figure | Millions / billions |
| **History sources** | Annual report 5-year highlights, BSE/NSE filings, screener.in (check its ROCE definition), CARO annexure, quarterly segment data | 10-K financial statements and MD&A, EDGAR full-text search, segment note (ASC 280), earnings supplements |
| **Management dialogue** | The **concall is the highest-value source**: whether management guides to ROCE, what hurdle rate they apply to new projects, what returns recent capex actually earned. Indian managements frequently state explicit ROCE targets — hold them to it year over year | Investor days and MD&A; some firms publish an explicit ROIC target and hurdle rate. The proxy (DEF 14A) reveals whether incentive pay is tied to ROIC, which is the real hurdle |
| **Governance overlay** | Promoter holding and pledging, promoter-group related-party flows and holdco discounts determine whether the reported return actually accrues to minority shareholders | Dual-class structures, controlled-company exemptions, VIE structures for China-domiciled ADRs where the listed entity may not own the operating assets at all |

## 20. What to put in the report

- A **10-year table**: ROCE/ROIC, ROE, NOPAT margin, capital turnover, CROIC — with the trough year highlighted.
- Your **invested-capital definition** in one sentence, the adjustments made, and their effect in percentage points.
- **ROIC versus a WACC range**, the spread in basis points, and economic profit in absolute currency.
- The **DuPont decomposition** for the company and 2–3 peers, side by side.
- **ROIIC over 3 and 5 years**, beside the historical average ROIC and WACC, with a one-line verdict on whether reinvestment compounds or dilutes.
- **Reported versus normalised** ROIC and what drives the gap.
- The **fade assumption** carried into valuation, stated explicitly.
- **Segment returns** and where incremental capital went, wherever disclosure allows.

## Checklist

- [ ] Run the sector gate first — confirm return-on-capital arithmetic is even defined for this business.
- [ ] Build NOPAT on a normalised cash tax rate; do not add back SBC; match non-operating income to non-operating assets.
- [ ] Build invested capital by both the operating and financing routes and reconcile them.
- [ ] Capitalise leases, state the R&D treatment, add back cumulative impairments, strip excess cash and non-operating investments — and note each adjustment's effect.
- [ ] Use average (or beginning-of-period) capital, never year-end, especially in an acquisition year.
- [ ] Compute ROIC including and excluding goodwill; report the gap for any acquirer.
- [ ] Estimate WACC as a range from current market inputs; report ROIC − WACC in bps and economic profit in currency.
- [ ] Never quote ROE without the 3-step DuPont; run the 5-step where tax or interest burden has moved.
- [ ] Split the return into margin and turnover and say which one drives it versus peers.
- [ ] Compute ROIIC over 3 and 5 years against average ROIC and WACC — the forward-looking signal.
- [ ] Cross-check reinvestment rate × ROIIC against management's growth guidance.
- [ ] Compare CROIC with ROIC over five years and explain any persistent gap.
- [ ] Pull 7–10 years; report mean, volatility, **trough** ROIC, and years above WACC.
- [ ] Normalise for one-offs and cycle position; state reported versus normalised.
- [ ] Benchmark twice — against an accounting-normalised peer set and against the company's own 5–10 year record.
- [ ] State the fade assumption / competitive advantage period explicitly and carry it into valuation.
- [ ] Compute segment returns wherever disclosure allows and check where incremental capital is going.
- [ ] Check whether rising ROE is matched by rising ROIC; if not, name the financing action responsible.
- [ ] Run the fourteen-lies scan (§18) before trusting any return figure, including your own.
- [ ] State metric definition, basis (consolidated/standalone), currency, units and period beside every number.
