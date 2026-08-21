# Holding companies, conglomerates, AMCs and alternative managers — sector playbook

Use this when: the company's earnings are largely a function of what it *owns* or what it *manages* rather than what it operates — pure investment holdcos, promoter/family holding vehicles, Core Investment Companies, multi-segment conglomerates, listed mutual-fund AMCs, wealth and portfolio managers, and alternative managers (PE, credit, infra, real assets, hedge funds).

The generic checklist assumes one operating business with one P&L. Here the reported financials are an accounting artefact of ownership percentages and consolidation thresholds, not a description of a business. Two holdcos owning economically identical portfolios can report entirely different revenue, margin and leverage purely because one crossed 50% and the other did not. For asset managers the balance sheet is nearly empty and the real assets — AUM, flows, performance, fee yield, accrued carry — sit outside the accounts entirely. Analyse this sector as: **what do I own per share (NAV), what cash actually reaches the parent, and how well is capital allocated** — or for managers, **fee-paying AUM × net revenue yield × operating leverage, minus flow risk**.

All ranges below are **indicative only**. They shift with market level, rate cycle, jurisdiction and regulatory regime. The company's own 5–10 year history and its closest sub-sector peers override every absolute band in this file.

## Contents

- [Why the generic ratio set fails here](#why-the-generic-ratio-set-fails-here)
- [The metrics that actually matter](#the-metrics-that-actually-matter)
- [How to value companies in this sector](#how-to-value-companies-in-this-sector)
- [Peer set construction](#peer-set-construction)
- [Sector-specific red flags](#sector-specific-red-flags)
- [Cycle and structural context](#cycle-and-structural-context)
- [India vs global notes](#india-vs-global-notes)
- [Checklist](#checklist)

## Why the generic ratio set fails here

Before computing anything, establish **which accounting regime each stake sits in**. Under Ind AS / IFRS the same economic ownership produces three incompatible income statements:

| Stake | Treatment | What appears in the P&L |
| --- | --- | --- |
| >50% (control) | Line-by-line consolidation | 100% of the sub's revenue and EBITDA, with the minority (NCI) share stripped out far below, near PAT |
| 20–50% (significant influence) | Equity method | A single "share of profit of associates" line. **Zero revenue.** |
| <20% | FVTPL / FVOCI (Ind AS 109, ASC 321) | Dividends only, plus fair-value marks (in P&L or OCI) |

So consolidated revenue growth can be produced entirely by a stake moving from 49% to 51%, with no change in economics. Every ratio built on revenue or capital employed is therefore non-comparable across holdcos and across time for the same holdco. Discard the following explicitly:

**OPM / EBITDA margin — undefined or meaningless.** A pure holdco's "revenue" is dividends, interest and fair-value gains, so operating margin routinely prints 80–300%, or goes negative in a year with no dividends, and describes nothing. For a conglomerate, blended OPM averages cement (18–22%), an NBFC (where "revenue" is gross interest income and margin is a leverage artefact), IT services (20–25%) and retail (5–7%) into a number that describes no business that exists. For an asset manager there is no COGS, so gross margin is vacuous and EBITDA ≈ EBIT ≈ revenue minus people costs — the only meaningful cost line is compensation.

**ROCE — broken in both directions, never in one.** Indian holdcos carrying decades-old stakes at historical cost show trivial capital employed and absurd ROCE. Holdcos carrying stakes at fair value show inflated capital employed and 2–4% ROCE, because the numerator is dividends received, not the economic earnings of the underlying. Asset managers are near-zero-capital businesses: ROCE of 30–80% is a statement about an empty balance sheet, not about competitive advantage, and it collapses the moment the firm holds seed capital or a principal investment book. Only **segment-level ROCE at the operating subsidiary** is analytically valid.

**D/E and interest cover at the consolidated level — actively misleading, not merely noisy.**
- If any subsidiary is a bank, NBFC or insurer, its 5–9x regulatory leverage swamps the group and consolidated D/E is nonsense.
- The debt that can bankrupt the parent is **holdco standalone debt**, which is structurally subordinated to all opco debt. Consolidated EBITDA/interest cover overstates the parent's capacity, because opco EBITDA is ring-fenced behind opco lenders, minorities, and — for regulated subs — regulator consent to upstream dividends.
- **Double leverage** (parent borrowing to inject equity into subsidiaries) is eliminated on consolidation and is therefore completely invisible in consolidated D/E.

**P/E and EPS — contaminated.** Consolidated PAT includes non-cash fair-value gains, unrealised carry marks, share of associate profits never received in cash, and lumpy stake-sale gains. Holdcos also structurally trade "cheap" on P/E because the market prices a discount to NAV, not a multiple of accounting earnings: a 4x P/E holdco is not cheap, it is a 55% NAV discount expressed badly. For alternative managers GAAP EPS is dominated by carry marks and by consolidation of funds, CLOs and VIEs the firm does not own — which is exactly why the industry reports FRE and DE instead.

**FCF — not the shareholder's cash.** Consolidated OCF-minus-capex includes cash trapped inside partly-owned and regulated subsidiaries. The only cash available for holdco debt service, dividends and buybacks is **upstreamed dividends net of leakage** (minorities, taxation in the recipient's hands, regulator-gated payouts).

**P/B — inconsistent, not wrong in one direction.** Where investments are fair-valued, book ≈ NAV and P/B is a crude discount proxy. Where they sit at cost or are equity-accounted, book value can be understated many times over. Comparing P/B across holdcos without first normalising the carrying basis is meaningless.

**Working capital, current ratio, inventory turns, cash conversion cycle, asset turnover, EV/EBITDA** — undefined for holdcos and asset managers, and mere portfolio averages (hence uninformative) for conglomerates. EV itself is undefined for any group containing a lending or insurance subsidiary, because debt there is raw material, not a claim. Peer-multiple comparison across conglomerates is apples-to-oranges by construction: the answer is determined by segment mix, not by quality.

## The metrics that actually matter

Ranges are indicative and sub-sector specific. Judge within sub-sector and against the company's own history.

| Metric | Definition / how to compute | Indicative healthy range | Why it matters |
| --- | --- | --- | --- |
| **NAV per share and discount / premium to NAV** | Sum-of-the-parts: listed stakes at market price, unlisted at peer multiple or last transaction, treasury and cash at value, **minus holdco standalone net debt**, minus capitalised holdco running costs, minus latent capital-gains tax on unrealised appreciation = tax-adjusted NAV. Discount = 1 − (market cap / NAV). | Developed-market, well-governed, buyback-active holdcos: 5–30% discount (Berkshire has historically traded at a premium to book). European family holdcos: 20–40%. India: 40–75% is the norm. Judge the current discount against the company's own 5–10 year percentile band, never against a universal number. | The actual valuation anchor and the actual return driver: total return = NAV growth + dividend yield ± change in discount. A stock can compound NAV at 15% and deliver 5% if the discount widens. A permanently wide, catalyst-free discount is a value trap, not an opportunity. |
| **Look-through earnings and look-through P/E** | Σ (ownership % × investee PAT) across consolidated subs, associates and minority stakes, regardless of accounting treatment, plus holdco standalone income, minus holdco costs and interest. Look-through P/E = market cap / look-through earnings. | A 40% NAV discount should show up as roughly a 40% lower look-through P/E than the weighted-average P/E of the underlying stakes. Look-through earnings growth of 10–15% p.a. is the bar for a quality holdco. | Neutralises the consolidation accident (full consolidation vs equity method vs FVTPL) and gives one comparable earnings base. It is the only earnings figure that maps to what the shareholder actually owns. |
| **Holdco standalone cash-flow cover (upstreaming ratio)** | Recurring cash received at the parent (dividends from subs and associates, interest, management/brand fees) ÷ parent-level fixed outflows (holdco opex + holdco interest + dividend paid to own shareholders). Read from **standalone**, not consolidated, accounts. | >1.5x comfortable; >2.0x strong; <1.2x is a warning; <1.0x means the parent is funding itself by borrowing or selling assets. | Structural subordination means opco EBITDA is not available to the parent. Upstreaming is gated by minorities, sub-level lender covenants and — for bank, NBFC and insurance subs — regulator approval. This ratio, not consolidated interest cover, tells you whether the holdco can service its own debt. Rating agencies test it explicitly. |
| **Holdco LTV and double leverage** | LTV = holdco standalone net debt ÷ gross market value of the portfolio. Double leverage = (parent's investment in subsidiaries at cost) ÷ parent's standalone net worth. | LTV <10% conservative, 10–25% acceptable, >30–35% is where rating agencies downgrade and forced-selling risk appears (the best-run European holdcos target ~5–10% with a hard ceiling near 25%). Double leverage <1.1x clean, 1.2x tolerable, >1.3x a red flag. | Holdco debt is repaid only from dividends or asset sales. High LTV plus a falling market converts a drawdown into a solvency event and forces sale of the best listed assets at the worst time. Double leverage means the same rupee of equity is counted twice in group capital — and it is invisible in consolidated D/E. | <!-- auditor:ignore-line — false positive: holdco LTV/double-leverage metric definitions; no credential or file access -->
| **Portfolio liquidity and concentration** | % of NAV in freely marketable listed securities (excluding pledged, locked-in, or positions too large to sell without a block discount), plus weight of the top asset and top three assets in NAV. | >60–70% of NAV listed and marketable is healthy. Top single asset <40–50% of NAV; above 60% the holdco is a levered proxy for one stock and deserves a **wider** discount, not a narrower one. | Liquidity determines whether the holdco can ever monetise, buy back stock or repay debt, and it is empirically the biggest single driver of discount width. A vehicle that is 85% one unlisted family asset will never trade near NAV. |
| **Segment ROCE, incremental ROIC, and capital below cost of capital** | Per reported segment: segment EBIT ÷ segment capital employed. Incremental ROIC = Δ segment EBIT ÷ Δ segment capital employed over 3–5 years. Then: % of group capital employed sitting in segments earning below WACC. | India: segment pre-tax ROCE >15–18% against a ~12–14% WACC; developed markets >12–15% against ~8–9%. Keep below-WACC capital under ~15–20% of the group; >30% signals a value-destroying conglomerate. | Company-level ROCE for a conglomerate is a portfolio average that hides cross-subsidy. The entire investment case is whether capital is recycled from cash cows into higher-return uses or into vanity greenfield. Incremental ROIC, not historic ROCE, is where that decision shows up first. |
| **NAV per share total return vs benchmark (capital-allocation scorecard)** | 5- and 10-year CAGR of NAV per share plus dividends vs the relevant total-return index (Nifty 500 TRI in India; MSCI World / STOXX in Europe; S&P 500 TR in the US). Keep a log of buybacks (done below NAV?), acquisition multiples paid and exit multiples achieved. | Beating the index by 200–400 bps p.a. over a full 10-year cycle justifies the structure's existence and a narrow discount. Underperformance over 10 years means the shareholder should own the index. | A holdco or conglomerate is a capital-allocation machine and nothing else. This is the only test of management skill that accounting cannot game, and it is the best predictor of whether the discount narrows. |
| **Holdco running cost ratio** | Parent-level operating expenses (salaries, promoter compensation, advisory, admin, listing costs) ÷ gross portfolio value — the implicit management fee shareholders pay for the structure. | <0.3% of NAV is efficient (the most disciplined global holdcos run near 0.1%). 0.5–1.0% is expensive; >1% and the entity is an expensive closed-end fund. | Capitalised at an 8–10% discount rate, a 1% running cost permanently destroys 10–12% of NAV and mechanically justifies part of the holding discount. It is also the cleanest read on whether the entity exists for shareholders or for the promoter family. |
| **AUM, AUM mix, and organic net flow rate** *(managers)* | Closing **and average** AUM — use average (QAAUM in India) for revenue analysis — split by asset class (equity / hybrid / debt / liquid / passive / alternatives) and by channel. Net flow rate = net client flows ÷ opening AUM, explicitly separated from market appreciation. | Positive net flows through a full cycle is the bar. Traditional managers: +3–6% organic net flow p.a. is good; negative organic flow with rising AUM is a melting ice cube. Alternatives: 10–20% FPAUM growth. India: equity + hybrid at 45–60% of QAAUM. | AUM growth from market beta is not an achievement and it reverses; only net flows are. Mix shift to debt, liquid or passive silently destroys revenue while headline AUM grows — liquid/overnight earns roughly 8–15 bps against 60–70 bps for equity. This is the most common way asset-manager growth is overstated. |
| **Net revenue yield on AUM (bps) and its trend** | Total operating revenue (management fees, net of distributor commissions where reported net) ÷ average AUM, in basis points, tracked quarterly and by asset class. | Indian AMCs: blended 45–55 bps, equity 60–75 bps, capped by SEBI's slab-based TER regime; stable-to-slightly-declining is realistic. Developed-market traditional: 25–45 bps and structurally falling. Alternatives: 100–150 bps on fee-paying AUM and far more stable. | Yield × AUM = revenue, and yield is where competition, TER cuts, direct-plan migration and passive substitution appear first. A manager growing AUM 15% with yield down 10% is a flat business. Yield compression is the defining structural risk of the sector. |
| **Operating profit per unit of AUM (bps) and cost-to-income** | Operating profit (PBT **excluding** other/treasury income) ÷ average AUM in bps — the Indian convention — plus the developed-market equivalent, cost-to-income ratio. | India: 25–40 bps operating profit on AUM is strong; <15 bps is subscale. Cost/income 40–55% for a good traditional manager; >70% is subscale or over-distributed. Alt managers: FRE margin 35–60%, best-in-class ~55–60%. | Isolates operating leverage and scale economics from market movements, and separates the fee franchise from returns on the firm's own investment book. Those two earnings streams deserve completely different multiples and must never be capitalised together. |
| **FRE, DE and permanent-capital share** *(alternative managers)* | FRE = recurring management fees − fee-related expenses, excluding all performance income. DE = FRE + realised performance fees + realised principal investment income, less taxes and interest. Permanent-capital share = % of FPAUM in perpetual or long-dated (>8-year, non-redeemable) vehicles. | FRE at 55–75% of DE indicates earnings are not carry-dependent. Permanent/long-dated capital >50% of FPAUM is a strong structural positive. FRE growth of 10–20% p.a. is the benchmark. | GAAP net income here is noise. FRE is the annuity the market capitalises at 20–30x; carry is capitalised at far less. Because the split determines the multiple, management has every incentive to reclassify items into FRE — so audit the definition, not just the number. |
| **Accrued carry, DPI and realisation rate** *(alternative managers)* | Net accrued performance receivable per share; gross vs net accrued carry after clawback and comp-sharing; DPI (distributions to paid-in) and MOIC / net IRR by vintage; % of funds above their preferred return (typically an 8% hurdle). | Net accrued carry is typically worth 10–25% of market cap and should be haircut 25–40% for realisation and timing risk. >75–80% of FPAUM in funds above hurdle is healthy. DPI >1.0x by year 6–7 of a vintage indicates real cash returns. | Accrued carry is an unrealised, reversible, manager-marked asset that is routinely valued in SOTP as if it were cash. Vintages that never cross the hurdle write it to zero, with clawback on top. DPI is the only honest test that paper marks convert to cash. |
| **Investment performance and asset stickiness** | % of AUM in funds beating benchmark or above peer median over 3 and 5 years; redemption rate; India: monthly SIP inflow, SIP AUM as % of equity AUM, share of equity AUM held >24 months. Institutional: top-5 clients as % of revenue. | >60% of AUM above benchmark/median on 3- and 5-year windows. India: SIP AUM >35–45% of equity AUM with rising monthly flow; individual (vs institutional) AUM >50%. Top-5 client concentration <20% of revenue. | Performance drives flows with a 2–3 year lag, so today's performance table is next year's revenue. Sticky retail SIP money survives drawdowns; institutional and corporate liquid money leaves in a week. Best single operational predictor of flow durability. |
| **Related-party exposure, minority leakage and promoter pledge** | RPTs (sales, purchases, ICDs, loans, guarantees) as % of revenue and net worth; corporate guarantees and contingent liabilities for group companies vs net worth; NCI share of consolidated profit vs NCI share of consolidated equity; promoter shares pledged as % of promoter holding; any circular cross-holdings. | RPTs excluding normal-course operations <5% of revenue; guarantees + contingent liabilities <25–30% of net worth; promoter pledge 0% (>10% is a serious flag in India); no circular cross-holdings. | In group structures value leaks sideways rather than being lost operationally: below-market intra-group pricing, ICDs to promoter vehicles, guarantees for weak affiliates, dilutive rights issues. **NCI profit share materially below NCI equity share** means minorities sit in the good businesses while the parent absorbs the losses. Circular holdings double-count NAV and make SOTP upside illusory. |
| **Free float, buyback record and payout policy** | Promoter/founder holding and free float; buybacks executed and the discount to NAV at which they were done; dividend payout as % of dividends *received* (the pass-through ratio). | Free float >25–30%; a stated policy of passing through received dividends; buybacks executed only at a material discount to NAV. | These are the only mechanisms by which a discount actually narrows. A holdco with cash, a 60% discount and no buyback in a decade is telling you the discount is a governance fact, not a mispricing. |

## How to value companies in this sector

**Default method: sum-of-the-parts NAV. Consolidated multiples are sanity checks only.**

### Holding companies and conglomerates — the SOTP build

1. **Listed stakes at market price.** Apply a block/illiquidity discount (10–20%) where the stake exceeds several months of trading volume or is strategically unsellable.
2. **Unlisted operating subsidiaries at segment-appropriate multiples.** EV/EBITDA for capital-intensive assets (cement, power, telecom infra: roughly 7–12x); EV/EBIT or P/E for asset-light services; **P/B calibrated to ROE** for lending and insurance arms (high-quality Indian NBFCs 2–4x P/B, banks 1.5–3x; insurers on embedded value); EV/Sales or GMV multiples only for genuinely early-stage assets. Never one blended multiple across dissimilar segments.
3. **Real estate, land banks and treasury at appraised or market value**, not book.
4. **Deduct holdco standalone net debt** (never consolidated net debt), pension deficits and group guarantees likely to be called.
5. **Deduct the capitalised PV of holdco running costs** (annual cost ÷ discount rate).
6. **Deduct latent tax on unrealised gains.** In India, LTCG on listed equity plus surcharge, and the full corporate rate on unlisted asset sales. Ignoring this is the single most common overstatement of holdco NAV.
7. **Apply a holding-company discount** to the resulting NAV. Calibrate from the company's own 5–10 year discount band and from peers with similar liquidity, governance and upstreaming — not from a textbook number.

**What widens the discount:** illiquid or unlisted-heavy portfolio, no buyback, thin free float, tax leakage on any monetisation, high running costs, poor NAV compounding, promoter entrenchment, complex multi-layer structures.
**What narrows it:** buybacks below NAV, a generous pass-through dividend policy, a listed and liquid portfolio, demonstrated NAV outperformance, simplification or a stated monetisation path.

**Model the catalyst, not just the gap.** Buyback authorisation, demerger or scheme of arrangement, listing of an unlisted sub, delisting or open offer, change in regulatory status (e.g. RBI CIC classification), promoter succession, or index inclusion. Absent a credible catalyst, assume the discount is permanent and underwrite only the NAV compounding plus dividend yield. This is the discipline that separates a genuine holdco idea from a decade-long value trap.

**Operating conglomerates of the Berkshire type** are better valued two-column: investments per share **plus** a capitalised multiple (roughly 9–12x pre-tax) on operating earnings, or on adjusted P/B (~1.2–1.6x). For diversified conglomerates, build segment EV with segment-specific multiples, allocate net debt to the segments that carry it, then apply a **conglomerate discount of 10–25%** where there is real cross-subsidy or capital misallocation — or a **premium** where the parent demonstrably allocates capital better than the market would.

### Traditional asset managers (AMCs, wealth, PMS)

- **P/E on core earnings** — PAT excluding other/treasury income — cross-checked against **EV/AUM** and **market cap / AUM**.
- Indian AMCs are conventionally quoted as a **percentage of QAAUM**: roughly 3–7% of AUM depending on equity mix and growth, with 25–40x P/E for franchise leaders and 12–20x for subscale players. Developed-market traditional managers trade at 8–15x P/E and 1–3% of AUM, reflecting terminal-decline fears from passives.
- **Always strip net cash and the investment book out of market cap** before computing the operating P/E. Indian AMCs typically carry 15–25% of market cap in liquid investments; including it makes the franchise look more expensive than it is.
- A DCF on fee streams is legitimate but must model **yield compression explicitly** — assume 2–4% annual blended yield decline unless mix is genuinely shifting toward equity and alternatives.

### Alternative asset managers

Strict SOTP:
- **(a) FRE capitalised at 18–30x after tax**, with the multiple set by permanent-capital share, flow durability and FRE margin.
- **(b) Net accrued carried interest at a 25–40% haircut** for realisation, timing and clawback risk.
- **(c) Expected future carry** as a separate low-multiple DCF — never bundled into the FRE multiple.
- **(d) Balance-sheet / principal investments at or below carrying value.**
- Cross-check with **P/DE of 15–25x**. Ignore GAAP P/E entirely, and **de-consolidate funds, CLOs and VIEs** before any leverage analysis.
- For hybrids with insurance balance sheets, value **spread-related earnings separately at a much lower multiple (8–12x)** than fee-related earnings — the market is paying for an annuity book, not a fee franchise.

### What NOT to use

Consolidated EV/EBITDA for any group containing a financial subsidiary; consolidated P/E for holdcos; consolidated ROCE; consolidated net debt in a holdco solvency assessment; GAAP P/E for alternative managers; peer-average multiples across conglomerates with different segment mixes; and P/B compared across holdcos without normalising the carrying basis of investments.

## Peer set construction

Do not put these in one peer table. The sub-sectors below have different value drivers, different multiples and different failure modes.

**1. Pure investment holdcos / promoter vehicles.** Compare only against holdcos with (a) similar portfolio liquidity — listed-heavy vs unlisted-heavy, (b) similar governance and free float, (c) similar tax leakage on monetisation, and (d) similar holdco leverage. An Indian family investment company holding decades-old listed stakes at cost is not comparable to a European family holdco that fair-values, buys back stock and publishes NAV monthly, even if both are "holdcos". The comparable statistic is the **discount band**, not P/E or P/B.

**2. Operating conglomerates.** Comparability requires similar **segment mix and similar capital intensity**. Never compare an industrial-plus-financial-services conglomerate to a pure-industrial one; the financial sub makes consolidated EV, D/E and EBITDA incomparable by construction. Where mix differs, do not compare multiples at all — compare segment-level ROCE and incremental ROIC, and compare the SOTP-implied conglomerate discount.

**3. Traditional AMCs.** Split by (a) equity/hybrid share of AUM — a liquid-heavy AMC is a different business at 8–15 bps than an equity-heavy one at 60–75 bps; (b) distribution model — captive bank/parent channel vs open-architecture vs direct/digital; (c) scale — top-5 by AUM enjoy real operating leverage that mid-table players do not; (d) regulatory regime, since TER caps are jurisdiction-specific. Never mix an Indian AMC (SEBI TER slabs, SIP-driven retail annuity) with a US traditional manager facing structural passive outflows.

**4. Alternative managers.** Split by (a) strategy mix — PE vs credit vs real assets vs infra have different fee rates, hurdle structures and duration; (b) permanent vs finite-life capital; (c) FRE-driven vs carry-driven earnings; (d) whether an insurance/annuity balance sheet is attached. A credit manager with 90% permanent capital and 65% FRE/DE is a different security from an opportunistic PE firm whose earnings are carry.

**5. Wealth managers, brokers and platforms** are a separate set again — they earn on client assets without taking manufacturing risk, have different regulatory capital, and should not be benchmarked on AMC bps.

Cross-cutting rule: never build a peer set on market cap or index membership alone. In this sector the accounting treatment of stakes, the liquidity of the portfolio and the fee-earning mix determine comparability — nothing else does.

## Sector-specific red flags

**Structure and leakage**
- **Circular or cross-holdings** between group entities (A owns B, B owns A) that double-count NAV. Headline SOTP upside is arithmetic fiction until the loop is eliminated.
- **Holdco standalone debt rising while dividends received are flat** — the parent is servicing itself with borrowings or asset sales. Check specifically whether the dividend to shareholders is funded from borrowings; that is a classic late-stage holdco pattern.
- **Double leverage above ~1.3x** — invisible in consolidated D/E, and the first thing that breaks in a downturn.
- **Consolidated net cash claimed while holdco standalone cash is near zero** — the cash is trapped inside partly-owned or regulated subsidiaries and is unavailable for debt service, buybacks or dividends.
- **Minority-interest asymmetry** — NCI's profit share far below its equity share. Also watch subsidiary rights issues priced to dilute minorities or the listed parent.
- **Holdco expenses pushed down to operating subsidiaries**, or brand/royalty/management fees charged by an unlisted promoter entity to listed subsidiaries — legal, but a real transfer of value away from the listed shareholder.
- **Promoter pledges, ICDs to promoter vehicles, guarantees for weak affiliates, non-arm's-length RPTs.** Contingent liabilities plus guarantees exceeding net worth is a solvency-level warning in a group structure.

**Accounting and disclosure**
- **Earnings driven by Level 3 fair-value gains** on unquoted investments marked on internal DCFs or manager marks, with no third-party transaction to corroborate them. Track the cumulative gap between carrying marks and realised exit values.
- **Frequent restructuring** — schemes of arrangement, demergers, mergers of loss-making group entities into profitable listed ones, re-segmentation of reported segments. Each one resets the historical record. A shrinking disclosed segment count or a swelling "Others" segment is deliberate.
- **NAV quoted gross of tax and gross of holdco costs**, with no deduction for capital-gains leakage on latent gains — the most common way holdco "upside" is overstated, typically by 15–25%.
- **Auditor resignation or qualification, especially at unlisted subsidiaries**; group audits where "other auditors" certify >20–30% of consolidated assets; delayed subsidiary filings; unavailable standalone accounts for key subs.
- **Fund / CLO / VIE consolidation** grossing up an alternative manager's balance sheet — apparent leverage and total assets that have nothing to do with the manager's own risk.

**Capital allocation**
- **Conglomerate cross-subsidy** — a mature cash cow funding years of losses in a promoter's new venture (new energy, telecom, retail, EV) with no stated ROIC hurdle, no ring-fencing and no timeline to breakeven. Look for group capex rising while segment incremental ROIC falls.
- **Huge cash and listed investments at a 60%+ discount with no buyback, no special dividend and no monetisation in a decade.** That is a governance signal, not a mispricing. Rising promoter stake toward the 75% ceiling without an open offer, or years of unexplained capital hoarding, means minorities will never see the value.

**Asset-manager specific**
- **AUM growth driven by market appreciation or by low-yield liquid/debt flows** — headline AUM up, blended bps down, revenue flat. Also check for **AUM definition inflation**: including advisory-only, non-fee-paying, uncalled commitments, or double-counted fund-of-fund assets.
- **FRE/DE definition drift** — reclassifying fee-related performance revenues, transaction and monitoring fees, or netting placement costs into FRE; excluding equity-based compensation from DE. These are non-GAAP and company-defined, so **the definition change is the signal**.
- **Accrued carry that grows for years without converting** — rising net accrued carry with flat or falling DPI means paper marks. Vintages that drop below the hurdle write it all off, with clawback exposure on top.
- **Client, mandate or channel concentration** — a single anchor mandate, captive parent/insurance flows, or one distributor bank driving most net sales.
- **Key-man and performance decay** — CIO or star PM exit; top-quartile AUM share falling below 50% on 3-year windows; the flagship underperforming while the firm launches new schemes to disguise net outflows (gross sales strong, net flows negative).
- **India-specific:** SEBI TER slab cuts, migration to direct plans, side-pocketing of stressed debt paper, and credit events in debt schemes — a debt-scheme wind-up can destroy franchise value overnight. A rising share of low-rated credit paper in debt schemes is an unpriced tail risk. Watch B30 incentive-driven flows that reverse when the clawback period ends.

## Cycle and structural context

**Discounts are pro-cyclical, and that is the whole game.** NAV discounts narrow in bull markets (when NAV is also high) and widen violently in drawdowns, so the holdco shareholder takes leveraged exposure to market direction. Buying a holdco at a historically narrow discount near a market peak stacks two mean-reverting variables against you. Conversely, the best risk-reward is a wide discount *plus* a visible catalyst *plus* a portfolio of businesses whose earnings are near a cyclical trough — but at least one of those three must be present or the position is dead money.

**Asset managers are levered beta with a lag.** Revenue = AUM × yield, and AUM moves with markets, so an AMC's earnings fall with the index and its multiple de-rates at the same time — a double hit. But flows lag performance by 2–3 years in both directions, so a good performance record earned during a drawdown pays for the next up-cycle. Model the flow response to a 30% market decline explicitly: how much AUM is sticky SIP/permanent capital, and how much is institutional money that leaves in a week?

**Secular threats.**
- *Fee compression and passive substitution.* Structural and one-directional in developed markets; in India it is regulator-driven (TER slabs that tighten as scheme AUM grows, so scale itself compresses yield) plus direct-plan migration. Passive share is still low in India but rising fast. Any model assuming flat blended bps for a decade is wrong.
- *Private markets consolidation.* Fee-paying AUM is concentrating in a handful of large multi-strategy alternative managers with permanent capital; sub-scale managers face a fundraising cliff as LPs consolidate relationships.
- *The private-credit and insurance-annuity convergence* changes the risk profile of alternative managers materially: spread earnings carry credit and duration risk that fee earnings never did, and deserve a much lower multiple.
- *Conglomerate de-rating.* Global capital markets have structurally penalised diversification since the 1990s; investors can diversify more cheaply than a company can. A conglomerate must now justify itself with demonstrated allocation skill, not with "synergies".

**Regulation is a first-order valuation variable here, not a footnote.**
- India: SEBI's TER caps and slab structure directly set AMC revenue yield; SEBI regulates AIF and PMS structures; RBI regulates **Core Investment Companies** (registration threshold, the double-leverage test, and limits on the number of layers in a group); the Companies Act restricts layers of subsidiaries; IRDAI and RBI gate dividend upstreaming from insurance and lending subs; RPT approval rules under LODR tightened materially.
- Global: SEC registration for advisers, the Investment Company Act 40-Act constraints, Volcker-type limits on bank-affiliated managers, AIFMD and MiFID II (which unbundled research payments and compressed fees) in Europe, and UK/EU value-for-money assessments that ratchet fees down.

**Where holdcos structurally persist.** In India, wide discounts have proved durable for decades because monetisation triggers full capital-gains tax, floats are thin, promoters have no intention of collapsing the structure, and the holdco often exists to hold control rather than to generate shareholder returns. Do not underwrite discount convergence in such names without an identified, dated, mechanically credible catalyst.

## India vs global notes

**Accounting and filings.** India: Ind AS (converged with IFRS), standalone **and** consolidated statements both filed — **always read the standalone for holdco solvency and the consolidated for economics**. Segment disclosure under Ind AS 108 is the raw material for conglomerate analysis; check for re-segmentation year to year. CARO reporting, the auditor's report on subsidiaries ("other auditors"), and the related-party note in the annual report carry most of the governance signal. Concall transcripts and investor presentations often disclose SOTP inputs, QAAUM splits and SIP data that never appear in the financials. Amounts are in crore/lakh — normalise before any cross-border comparison.
US/global: 10-K and 10-Q on EDGAR, US GAAP or IFRS; alternative managers disclose FRE, DE, FPAUM, accrued carry and fund-level performance in a supplemental non-GAAP section — read the reconciliation tables, not the headline. Segment reporting under ASC 280 is generally more granular than Indian practice.

**Holdco discounts.** India 40–75% is normal and durable; Europe 20–40%; well-governed, buyback-active developed-market holdcos 5–30%. The difference is not investor irrationality — it is tax leakage on monetisation, free float, buyback culture and promoter intent.

**Promoter/founder holding.** India-specific and load-bearing: promoter holding %, the 75% maximum public-shareholding ceiling, pledged shares (disclosed quarterly), and inter-se transfers. A promoter creeping toward 75% without an open offer, or persistent pledging, changes the governance read entirely. There is no equivalent disclosure regime in most developed markets, where dual-class share structures play a similar role and must be checked separately.

**Regulatory perimeter.** India's **CIC** regime under RBI is unique: a company whose assets are >90% investments in group companies, with >60% in equity of group companies, must register as a CIC and faces the double-leverage test and layer limits. Check whether the holdco is a registered CIC or an NBFC-ICC — it changes leverage capacity and dividend flexibility. In the US, watch instead for inadvertent Investment Company Act status.

**Dividend taxation and upstreaming.** Post-FY21 India taxes dividends in the shareholder's hands, which mechanically penalises multi-layer holdco structures; Section 80M relief applies only where a domestic company redistributes dividends received. This tax cascade is a genuine economic reason Indian holdco discounts are wide, and it must be modelled, not hand-waved. In the US, the dividends-received deduction and participation exemptions in Europe mitigate the cascade substantially.

**Asset managers.** India: SEBI-mandated slab-based TER falling as scheme AUM rises; monthly AMFI industry AUM and QAAUM data; the SIP book as a structural retail annuity with no direct developed-market equivalent; B30 incentives for smaller-city flows; direct plans mandated since 2013. Disclosure of QAAUM by scheme category is public and monthly — use it, and cross-check the company's claimed market share against AMFI data. US/Europe: fee disclosure through the prospectus and Form ADV; flow data via industry aggregators; heavy passive substitution and continuous fee-war pressure that Indian AMCs have so far felt less acutely.

**Latent capital-gains tax.** India levies LTCG on listed equity plus surcharge and full corporate rate on unlisted asset sales — this must be deducted from NAV. Many developed-market holdco jurisdictions offer participation exemptions on the sale of qualifying stakes, which is a large part of why their discounts are structurally narrower. Never apply an Indian tax haircut to a European holdco or vice versa.

## Checklist

- [ ] Classify every material stake by accounting treatment (consolidated / equity method / FVTPL) before computing any ratio; note which ratios that invalidates.
- [ ] Build a tax-adjusted SOTP NAV per share: listed at market (with block discount), unlisted at segment multiples, minus **holdco standalone** net debt, minus capitalised holdco costs, minus latent capital-gains tax.
- [ ] Plot the current discount against the company's own 5–10 year discount band, not against a textbook number.
- [ ] Name the catalyst that closes the discount, with a date and a mechanism. If there is none, underwrite only NAV compounding plus dividend yield.
- [ ] Compute look-through earnings and look-through P/E; check the implied discount reconciles with the NAV discount.
- [ ] Compute holdco standalone cash-flow cover from the **standalone** accounts; flag anything below 1.2x.
- [ ] Compute holdco LTV and double leverage; flag LTV >30% or double leverage >1.3x.
- [ ] Measure portfolio liquidity (% of NAV listed and freely marketable) and top-asset concentration.
- [ ] Compute 5- and 10-year NAV-per-share total return vs the relevant total-return index; this is the capital-allocation verdict.
- [ ] Compute the holdco running cost ratio and capitalise it — that is a permanent NAV deduction.
- [ ] For conglomerates: segment ROCE, incremental ROIC, and the share of group capital employed earning below WACC.
- [ ] Check for circular cross-holdings and eliminate the loop before quoting SOTP upside.
- [ ] Compare NCI's share of consolidated profit against NCI's share of consolidated equity; asymmetry means minorities own the good assets.
- [ ] Scan RPTs, ICDs, corporate guarantees, contingent liabilities vs net worth, and promoter pledge (India).
- [ ] For managers: split AUM growth into net flows vs market appreciation; never accept headline AUM growth.
- [ ] For managers: track net revenue yield in bps by asset class and its multi-year trend; model yield compression explicitly.
- [ ] For managers: strip treasury/investment income and net cash out before computing an operating P/E or bps-on-AUM.
- [ ] For alternative managers: separate FRE from carry, check the FRE/DE ratio and permanent-capital share, and audit FRE/DE definition changes year to year.
- [ ] For alternative managers: compare accrued carry growth against DPI; de-consolidate funds/CLOs/VIEs before any leverage work.
- [ ] Check performance persistence (% AUM above benchmark on 3- and 5-year windows) and stickiness (India: SIP AUM share; global: institutional concentration).
- [ ] Read the auditor's report for qualifications, resignations, and the share of consolidated assets certified by "other auditors".
- [ ] Check for re-segmentation, demergers and schemes over 5 years; rebuild a like-for-like history before trusting any trend.
- [ ] Confirm the peer set shares accounting treatment, portfolio liquidity and fee/segment mix — not just market cap or index membership.
