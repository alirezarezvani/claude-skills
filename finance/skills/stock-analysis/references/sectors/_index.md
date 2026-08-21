# Sector Router — Pick the Right Playbook Before You Compute Anything

Use this when: you have identified the company but have not yet chosen which sector playbook governs the analysis — or when a company straddles several sectors and you need to decide which lens dominates.

Sector is not a decoration on top of the numbers; it decides which numbers exist at all. A bank has no "revenue" in the industrial sense, a REIT's net income is systematically understated by non-cash depreciation, a miner's peak margin is its most dangerous moment, and a pre-profit SaaS company burning cash may be compounding value faster than a profitable one. Routing to the wrong playbook does not make the analysis slightly wrong — it makes it inverted. Spend the two minutes here before you compute a single ratio.

## Contents

- [Step 1 — Classify by profit driver, not by index label](#step-1--classify-by-profit-driver-not-by-index-label)
- [Step 2 — The routing table](#step-2--the-routing-table)
- [Step 2a — DO NOT route on the label](#step-2a--do-not-route-on-the-label)
- [Step 2b — Complete industry mapping](#step-2b--complete-industry-mapping)
- [Step 3 — Multi-segment companies](#step-3--multi-segment-companies)
- [Step 4 — Conglomerates and holding companies](#step-4--conglomerates-and-holding-companies)
- [Step 5 — When nothing fits](#step-5--when-nothing-fits)
- [Sector families — which standard metrics break](#sector-families--which-standard-metrics-break)
- [Fast sanity check before you leave this file](#fast-sanity-check-before-you-leave-this-file)
- [Checklist](#checklist)

---

## Step 1 — Classify by profit driver, not by index label

Index classifications (GICS, NIC, the exchange's own sector tag, "Nifty FMCG", "S&P Consumer Discretionary") are built for portfolio construction, not for analysis. They routinely mislabel companies whose economics have drifted. Ask instead:

**Q1. Where does the operating profit actually come from?** Read the segment note (Ind-AS 108 / ASC 280 segment reporting) and rank segments by EBIT or segment result, not by revenue. Revenue mix and profit mix diverge violently: a trading segment can be 60% of revenue and 5% of profit.

**Q2. What is the balance sheet for?** This single question separates the four families:
- Balance sheet **is** the product (assets are loans/investments/policies, leverage is the business model) → **financials family**.
- Balance sheet is a **physical asset base** earning a spread over its cost, often with regulated or contracted returns → **real-asset/regulated family**.
- Balance sheet is **plant converting a commodity input to a commodity output**, price-taker on both sides → **cyclical-commodity family**.
- Balance sheet is **small relative to earnings**; the value sits in brands, code, licences, people, or distribution → **asset-light family**.

**Q3. Who sets the price?** Regulator (utilities, some telecom, some pharma pricing), exchange/spot market (metals, oil, shipping rates), contract/tender (infra, capital goods, defence), or the company itself with pricing power (branded consumer, software, medical devices). Price-setting mechanism determines whether margin expansion is skill or luck.

**Q4. What is the unit of production?** Loans disbursed, tonnes shipped, seats flown, square feet leased, subscriptions renewed, prescriptions filled, wafers started. If you cannot state the unit, you do not yet understand the business and should not route.

**Q5. What kills this business?** Credit losses, commodity price collapse, regulatory reset, technological obsolescence, refinancing wall, a single customer leaving. The failure mode names the family more reliably than the product does.

Three worked routing decisions of the kind that trip up label-based classification:

- A company that manufactures nothing, owns the brand and design, and outsources all production is **not** an industrial — route to `fmcg-consumer` or `retail-ecommerce` depending on whether it sells through others' shelves or its own channel.
- A "technology" company whose revenue is per-transaction fees on payment volume is **not** `it-saas` — route to `exchanges-payments`, because its driver is volume × take rate and its risk is regulatory interchange caps, not seat expansion.
- A "consumer finance" arm inside a car maker is a lender. If it is a meaningful share of profit, its economics must be analysed with `nbfc` alongside the parent's `auto` analysis, and the consolidated ratios (which mix a manufacturer's and a lender's balance sheets) must be treated as meaningless until separated.

---

## Step 2 — The routing table

Match on business description and profit driver. Where two rows both apply, apply the guidance in Step 3.

| Playbook file | Route here when | Common sub-sectors | Example business models |
|---|---|---|---|
| `banks.md` | Profit is net interest income on a deposit-funded loan book; regulator sets capital adequacy | Public sector banks, private banks, small finance banks, regional/community banks, cooperative banks | Deposit-taking lender; a bank whose fee income (cards, distribution, treasury) is a growing minority of profit |
| `nbfc.md` | Lender **without** a retail deposit franchise, funded by borrowings/securitisation; India-specific NBFC/HFC/MFI regulatory stack | Housing finance, vehicle finance, gold loans, microfinance, SME lending, consumer/BNPL lenders, US specialty finance & consumer credit | Gold-loan lender; captive finance arm of a manufacturer; a lender funded by bank lines and NCDs |
| `insurance.md` | Profit is underwriting result plus float investment income; liabilities are actuarial | Life insurance, general/P&C insurance, health insurance, reinsurance, title insurance, managed care | Life insurer valued on embedded value and VNB; a P&C insurer whose combined ratio decides everything |
| `insurance-brokers-services.md` | The company **places, distributes or administers** insurance and underwrites none of it; revenue is commission and fees on somebody else's premium | Retail and wholesale brokers, reinsurance brokers, MGAs/MGUs/coverholders, employee-benefit consultants, TPAs and claims administrators, PoSP and online distribution platforms | Acquisitive retail broker whose reported growth is organic plus bought; a TPA paid per member per month |
| `mortgage-reit-specialty-finance.md` | A **leveraged portfolio of financial assets or leased hardware** rather than an operating business; borrowings buy the assets that earn the return | Agency and credit mortgage REITs, commercial mREITs, BDCs and listed private credit, CLO vehicles, aircraft/container/railcar lessors, equipment rental and leasing | Agency mREIT running 7x repo leverage on an MBS book; an aircraft lessor earning a funding-to-lease spread plus a residual-value bet |
| `it-saas.md` | Revenue is software licences, subscriptions or people-hours; near-zero physical capital | IT services & outsourcing, product SaaS, ERTS/engineering R&D services, cybersecurity, internet platforms with subscription revenue | Offshore IT services firm billing on time & materials; seat-based SaaS with net revenue retention above 110% |
| `pharma-healthcare.md` | Profit depends on regulatory approval, patent life, or clinical throughput | Generics, CRAMS/CDMO, API makers, innovator biotech, hospitals, diagnostics labs, medical devices | US-generics exporter facing price erosion; a hospital chain earning on occupancy and ARPOB; a diagnostics chain on test volumes |
| `biotech-clinical.md` | **No approved product and no product revenue.** The whole market capitalisation is a probability-weighted claim on an approval that has not happened | Pre-clinical and clinical-stage developers, platform companies monetising only through partnerships, reverse-merged and de-SPAC'd research entities, carved-out innovator R&D arms | Phase 2 oncology developer with 18 months of runway; a platform company whose only revenue is milestone income |
| `people-businesses.md` | The productive asset is **human time, judgement or attention** and goes home every evening; capital employed is trivial, so gross profit is the real top line | Temp and permanent staffing, IT and management consulting, advertising and media agencies, market research, facilities management, security manpower, testing/inspection/certification, contact centres, real-estate brokerage | Staffing firm on gross profit per consultant and conversion ratio; an agency on organic net-revenue growth |
| `fmcg-consumer.md` | Branded, repeat-purchase products sold through distribution; profit is gross margin × velocity | Foods & beverages, home & personal care, alcohol/tobacco, consumer durables & appliances, branded apparel, QSR | Packaged foods company with a 3-tier distributor network; a durables brand with a dealer channel |
| `auto.md` | Profit is units × contribution margin on a fixed cost base; deep cycle, heavy operating leverage | OEMs (2W/PV/CV/tractors), auto ancillaries, tyres, EV makers and charging, dealerships | Commercial vehicle maker at the mercy of the freight cycle; a Tier-1 supplier with single-OEM concentration |
| `metals-mining.md` | Price-taker on an exchange-quoted commodity; profit is spread over cost per tonne | Steel, aluminium, copper, zinc, coal, iron ore, gold miners, ferro-alloys | Integrated steel maker with captive ore; a non-integrated converter buying ore at spot |
| `oil-gas.md` | Crude/gas price, refining crack spread, or regulated marketing margin drives profit | Upstream E&P, refining, marketing, city gas distribution, oilfield services, LNG | Refiner earning on gross refining margin; a city gas distributor on regulated volumes and spreads |
| `utilities-power.md` | Regulated or long-contracted returns on an asset base; volumes are near-inelastic | Thermal/hydro/nuclear generation, transmission, distribution utilities, renewables IPPs, water | Regulated transmission utility earning a fixed RoE on approved capex; a solar IPP on 25-year PPAs |
| `waste-environmental.md` | Route density plus a **permitted disposal asset**; the moat is a permit a competitor cannot obtain at any price, and the offsetting cost outlives the asset by thirty years | Solid, hazardous, medical and industrial waste collection and disposal, landfills, transfer stations, waste-to-energy, material recovery, EPR-mandated recycling, water and wastewater operations, remediation | Landfill-led collector on internalisation rate and remaining airspace; an e-waste recycler on tonnes processed and scrap spread |
| `realestate-reit.md` | Value is property NAV and rental/development cash flow; depreciation is largely non-economic | Residential developers, commercial landlords, REITs & InvITs, warehousing, data-centre landlords, homebuilders | Residential developer recognising revenue on completion; a REIT distributing 90%+ of NDCF |
| `infra-capitalgoods.md` | Order book converts to revenue over multi-year contracts; working capital is the battleground | EPC contractors, roads/HAM & BOT concessions, defence, industrial machinery, electrical equipment, ports as concessions | EPC firm with a 3x order book to revenue; a road concessionaire whose value is an annuity stream |
| `telecom-media.md` | Subscriber base × ARPU on a heavy, spectrum- or content-funded fixed cost base | Wireless & broadband telcos, tower & fibre infracos, broadcasters, print, film/OTT, music | Wireless operator on ARPU and subscriber churn; a tower company earning on tenancy ratio |
| `aviation-hotels.md` | Perishable inventory sold by the seat-night; yield × occupancy × fixed cost | Airlines, airports (if not concession-led), hotels, restaurants, travel operators, cruise, gaming/casinos | Low-cost carrier on RASK/CASK and load factor; a hotel chain on RevPAR |
| `retail-ecommerce.md` | Profit is thin margin on high throughput; store or fulfilment economics decide everything | Supermarkets, apparel & specialty retail, jewellery retail, pharmacy retail, marketplaces, quick commerce, D2C | Grocery chain at low-single-digit EBIT margin living on inventory turns; a marketplace on GMV take rate |
| `chemicals-cement.md` | Process-industry manufacturing where capacity utilisation and input spreads set margin | Commodity & specialty chemicals, agrochemicals, fertilisers, paints, cement, glass, packaging, industrial gases | Speciality chemicals maker with a molecule-level moat; a cement plant priced by regional realisation per tonne |
| `holdco-assetmgr.md` | Earnings are dividends, fees or fair-value gains on assets others operate | Holding companies, conglomerate parents, asset managers/AMCs, PE & alternatives, wealth managers, business trusts | Listed holdco trading at a discount to its stake value; an AMC earning on AUM × yield |
| `shipping-logistics.md` | Freight rates or per-shipment economics drive profit; asset-heavy or asset-light variants differ sharply | Container/dry bulk/tanker shipping, port terminals, 3PL & warehousing, express/courier, trucking, road freight brokerage | Dry bulk owner exposed to spot charter rates; an asset-light freight forwarder on net revenue per shipment |
| `rail-freight.md` | Freight moved over a **rail network** the company owns or runs on — a capital-intensive network utility with duopoly geography, a common carrier obligation and real pricing power | Class I railroads, regional and short lines, national freight carriers, container train operators, private freight terminals and multimodal rail players | Class I railroad managed to an operating ratio; a container train operator on originating volumes and lead distance |
| `exchanges-payments.md` | Profit is take rate on transaction volume, or fees on a network/venue | Stock exchanges, depositories, clearing houses, brokers, card networks, acquirers/PSPs, fintech rails, credit bureaus, rating agencies | Exchange earning per-trade fees on volatility-driven volumes; an acquirer on payment volume × net take rate |
| `semiconductors.md` | Profit driven by node/design cycle, fab utilisation or design-win pipeline; brutal capital intensity or none at all | Fabless designers, foundries, IDMs, memory, semicap equipment, EDA/IP licensing, OSAT | Fabless designer with high gross margin and no fab; a memory maker whose margin swings with a global supply cycle |

---

## Step 2a — DO NOT route on the label

Read this before the mapping table, because the mapping table cannot save you from a label that is actively lying. A handful of industry names describe what the company is *near* rather than what it *is*, and each one has a naive route that computes cleanly, prints plausible numbers and describes a different company. These are the errors that produce confidently wrong analysis rather than merely imprecise analysis — a missing metric announces itself, a wrong metric does not.

The rule underneath all of them: **route on who bears the risk and what the cash flow is a claim on**, never on the noun in the industry name.

| Label | The naive (wrong) route | The correct route | Why the naive route produces meaningless output |
|---|---|---|---|
| **REIT - Mortgage** | `realestate-reit.md`, because of the word REIT | `mortgage-reit-specialty-finance.md` | An mREIT owns no buildings, no tenants and no leases. Occupancy, WALE, same-store NOI, rent reversion, cap-rate spread, NAV per square foot, FFO and AFFO are not "less relevant" — they have no referent, and an AFFO computed for one is a fabricated number. It is a levered agency/non-agency MBS book funded overnight in repo, so the real questions are book value per share, economic return on book, duration gap, hedge ratio, prepayment speed, repo tenor and haircuts. |
| **Insurance Brokers** | `insurance.md`, because of the word insurance | `insurance-brokers-services.md` | A broker takes no underwriting risk and holds no float, so combined ratio, loss ratio, solvency/RBC, reserve development, persistency, embedded value and VNB do not exist for it. It is a commission-and-fee roll-up: organic growth, EBITDAC, compensation ratio, client retention, net debt/EBITDAC. P/B is the exact inverse error — book value *is* the anchor for a carrier and is an accounting residue of deal prices for a broker, frequently negative on a tangible basis. |
| **Rental & Leasing Services** | `infra-capitalgoods.md` or `auto.md` — it owns machines, so it must be an industrial | `mortgage-reit-specialty-finance.md` (lessor section) | A lessor is a financial business wearing industrial clothing: it earns the spread between funding cost and lease yield, plus a residual-value bet. EV/EBITDA is superficially computable and therefore especially dangerous — EBITDA excludes depreciation (the actual consumption of the leased asset) and interest (the actual raw material), which between them are most of the cost base, so an 80–90% "EBITDA margin" is an accounting artefact, not a moat. Use fleet age, time versus dollar utilisation, lease yield, residual realisation on disposal and the maturity ladder against lease inflows. |
| **Healthcare Plans** | `pharma-healthcare.md` because the word is healthcare, or `insurance.md` run with the P&C or life metric set | `insurance.md`, **managed-care metric set only** | A managed-care insurer has no combined ratio in the P&C sense and no embedded value or VNB in the life sense. Its metrics are the medical loss ratio against statutory minimums, membership by line (commercial, Medicare Advantage, Medicaid, exchange), premium per member per month, star ratings, risk-adjustment revenue and the SG&A ratio. Running it through the P&C set makes the largest cost line disappear into an underwriting ratio that nobody in the industry uses; running it through the life set values a one-year renewable contract as a multi-decade book. |
| **Shell Companies** | Any sector playbook, chosen from the industry of the target the shell says it intends to buy | `references/13-situations.md` §15 (SPAC / de-SPAC) — not a sector playbook at all | There is no business yet. Every sector metric would be computed on a trust account. What actually decides the outcome is trust value per share, the sponsor promote, warrants, PIPE and earn-out shares on a fully diluted count, the redemption deadline and the sponsor's incentive to complete *any* deal before it. Route to a sector playbook only once a merger closes and an operating company exists — and then apply §1 and §8 of that file as well, because most de-SPACs are also loss-making and newly listed. |
| **Biotechnology** | `pharma-healthcare.md` for everything with a molecule | `biotech-clinical.md` when pre-revenue; `pharma-healthcare.md` once there are marketed products. **The test: does the company sell an approved product for its own account?** If every rupee or dollar of revenue is collaboration, milestone, grant or licence income and nothing has marketing approval in a commercial market, it is pre-revenue. One approved product generating recurring product sales — or any biosimilar, generic, API, CDMO or CRO business — moves it to `pharma-healthcare.md`. | The pharma playbook computes margins, and a pre-revenue developer's "margin" is a division by a licensing calendar that swings hundreds of percent between quarters with no change in the business. Worse, it inverts the sign on the key metrics: ROE, ROCE, operating cash flow and FCF all *improve* when the company halves its R&D budget, which is the moment it stops building the only asset it owns. The correct frame is runway against catalyst dates, pipeline stage advancement and risk-adjusted value per unit of cash burned. |
| **Railroads** | `shipping-logistics.md`, filed under transport | `rail-freight.md` | A railroad is a network utility with duopoly geography, a common carrier obligation and durable pricing power; the freight-rate cyclicality lens under-rates that pricing power and under-states the capital intensity at the same time. The sector speaks in operating ratio, which is *inverted* against every margin metric in the generic set (lower is better) and moves mechanically with fuel surcharge. And its central question — is reported free cash flow efficiency, or a capex holiday on track, ties, ballast, bridges and locomotives — does not exist anywhere in a shipping framework. |
| **Solar**, **Utilities - Renewable** | Route the whole industry one way, usually to `utilities-power.md` because of the word renewable | **The test: is it selling electrons or selling hardware?** Selling power under a PPA, feed-in tariff or merchant offtake → `utilities-power.md`. Manufacturing cells, wafers, modules, inverters or trackers → `semiconductors.md`. Producing polysilicon, wafers-as-chemistry, glass or encapsulants → `chemicals-cement.md`. | They are opposite businesses on the same technology. A module maker's margin collapses when module prices fall — which is exactly when the IPP's project returns improve. Applying an IPP's contracted-cash-flow DCF to a manufacturer capitalises an ASP that deflates every single year; applying manufacturing utilisation and ASP logic to an IPP ignores the offtake contract and the offtaker's credit quality, which together are the entire asset. |
| **Conglomerates**, **Financial Conglomerates** | One consolidated P/E or EV/EBITDA on the group | `holdco-assetmgr.md` plus sum-of-the-parts, with each material subsidiary run through its own playbook (and for a financial conglomerate, `banks.md` / `insurance.md` / `nbfc.md` on each regulated entity separately) | Consolidation blends balance sheets that cannot be blended — a lender's, a manufacturer's and a landlord's — so a single multiple across them is arithmetic without meaning, and minority interests can leave the parent owning a small share of the profit it reports. Group leverage, group ROE and group asset turnover describe no business that exists. Value listed stakes at market, unlisted ones on their own sector multiples, deduct holdco debt and capitalised holdco costs, and read the holding discount against its own history rather than against zero. |
| **Real Estate Services** | `realestate-reit.md`, because of the words real estate | `people-businesses.md` | Brokerage, agency, valuation and property management own no property. Revenue is commission on transaction volume and fees on managed area, so cap rate, NAV, FFO, occupancy and same-store NOI are undefined for their own balance sheet. The cyclicality is transaction-volume cyclicality against a semi-fixed cost base of producers who can resign, which is why drop-through in a downturn is brutal and P/E is lowest at the peak. Use `realestate-reit.md` only for the portion of the balance sheet that actually holds property. |
| **Medical Distribution**, **Pharmaceutical Retailers** | `pharma-healthcare.md` | `retail-ecommerce.md` | Neither owns a molecule, a patent or an approval. A drug distributor earns fractions of a percent of gross margin on enormous revenue and lives on working capital, buy-side scale and generic procurement economics; a pharmacy chain lives on footfall, store throughput and front-of-store mix. Applying pharma gross margins, R&D productivity, patent cliffs or approval risk to either describes a company that does not exist, and the "low margin" it prints will be read as weakness when it is the business model. |
| **Health Information Services** | `pharma-healthcare.md` | `it-saas.md` | The customer is in healthcare; the economics are software. Recurring revenue, net revenue retention, gross margin, CAC payback, R&D capitalisation policy and switching costs decide it. Patent life, clinical throughput, approval risk, occupancy and ARPOB have no referent. |
| **Advertising Agencies** | `telecom-media.md`, filed under media | `people-businesses.md` | An agency does not earn its billings — client media money passes through it, and the agent-versus-principal determination under Ind-AS 115 / IFRS 15 / ASC 606 changes reported "revenue" by a multiple with zero change in economics. Growth, EV/Sales and market share built on that top line are fiction. Use net revenue / gross profit as the top line, the conversion ratio (EBITA ÷ gross profit) as the margin, and *average* net debt, because year-end cash is media payables in transit and is not available to shareholders. Broadcaster metrics — ad inventory, viewership, content amortisation — belong to the medium, not to the agency. |
| **Pollution & Treatment Controls** | `waste-environmental.md`, because the end use is environmental | `infra-capitalgoods.md` | Scrubbers, ESPs, membranes, filtration skids and ZLD systems are engineered capital goods sold against the customer's capex budget: order book, execution, milestone billing and working capital decide the outcome. Route density, internalisation rate, landfill airspace amortisation and closure/post-closure liabilities have no referent for an equipment maker, and the environmental end market changes nothing about the economics. |
| **Trucking** | `rail-freight.md`, filed under freight | `shipping-logistics.md` | A trucker rents its right-of-way from the taxpayer, has no network moat and no common carrier pricing power, and runs asset turnover several times a railroad's by construction. Operating ratio, maintenance-of-way capex, network fluidity and car-hire economics do not transfer, and reading spot-rate cyclicality as durable pricing power inverts the conclusion at both ends of the cycle. |
| **Communication Equipment** | `telecom-media.md`, because the customers are telcos | `infra-capitalgoods.md` | It sells *to* operators; it is not one. Revenue is the customers' capex budget converted through tenders and a product cycle, so ARPU, subscriber churn, spectrum cost, tenancy ratio and content spend are meaningless here — and the capex cycle of three or four buyers, not subscriber growth, is the actual risk. Cross-read `semiconductors.md` where most of the value sits in silicon, optics or IP. |
| **Insurance - Specialty** (when the entity is an MGA, MGU or coverholder) | `insurance.md` | `insurance-brokers-services.md` | If the entity binds business on somebody else's paper it holds no reserves and no capital against the risk, so combined ratio and solvency describe the carrier rather than the company. The carrier's loss ratio on the delegated book matters only as a binder-renewal risk — lose the capacity and the revenue line disappears in one renewal cycle regardless of client retention. Genuine specialty underwriters (title, mortgage, credit, warranty) do belong in `insurance.md`. |
| **Credit Services** | One playbook for the whole industry | **The test: who carries the receivable?** Issuers and lenders holding the credit exposure → `nbfc.md`. Networks, acquirers, processors and bureaus taking no credit risk → `exchanges-payments.md`. | The two halves have opposite failure modes. A card network dies of regulatory interchange caps and volume loss; a card issuer dies of a credit cycle. Applying loss-rate, provision-coverage and vintage-curve analysis to a network invents a risk it does not run, while applying volume × take-rate analysis to an issuer omits the only thing that can actually destroy it. |
| **Information Technology Services** | `it-saas.md` for everything with the word technology in it | `it-saas.md` where the firm owns the delivery outcome; `people-businesses.md` where it bills a markup on a head. **The test: does the contract transfer delivery responsibility?** | An IT staffing firm supplies headcount and carries no delivery obligation; an IT services firm owns the outcome. Applying offshore mix, backlog conversion and net revenue retention to a staffing book, or EV/gross profit to a services exporter, produces confident nonsense in both directions. For staffing, the metrics are gross profit per consultant, the bill-pay spread and the conversion ratio — margin on gross revenue *falls* when volumes grow, which a generic screen reads as deterioration. |
| **REIT - Specialty** | One property lens and one cap rate across the whole category | `realestate-reit.md` for the REIT wrapper, then route by what the tenant actually pays for | "Specialty REIT" is a residual bucket, not a business: towers and fibre are tenancy-ratio economics from `telecom-media.md`, a data centre selling power-backed capacity on long contracts is closer to `utilities-power.md`, timberland is a land-NAV business, and a net-lease gaming REIT is single-operator rent-coverage credit analysis. Averaging them into one cap rate blends assets with different tenants, contract lengths and obsolescence risk. |
| **REIT - Hotel & Motel** | The lease-based REIT toolkit — WALE, lease expiry schedule, contractual rent coverage | `realestate-reit.md` for the structure, `aviation-hotels.md` for the earnings | A hotel REIT does not collect contractual rent; it takes the hotel's operating result through a taxable subsidiary. Lease-expiry and rent-coverage metrics are undefined, and the distribution is as cyclical as RevPAR. Read ADR, occupancy, RevPAR, hotel EBITDA margin and the terms of the management agreement, then apply the REIT distribution mechanics on top. |
| **Farm & Heavy Construction Machinery**, **Auto Manufacturers** (where a captive finance arm exists) | Consolidated leverage, margin and return figures | `infra-capitalgoods.md` / `auto.md` for the industrial, `nbfc.md` for the finance arm, then sum the parts | Consolidating a captive lender into a manufacturer produces a debt/equity ratio, an asset turnover and a ROCE that describe neither business — the lender's borrowings are raw material, the manufacturer's are leverage. Separate the finance book, its funding and its credit costs before any leverage or return comparison, and value the two on different multiples. |

If a company sits on one of these lines, say so explicitly in the output: name the industry label, name the route you rejected, and name the one you took. A reader who disagrees should be able to attack the routing decision directly rather than having to reverse-engineer it from the metrics.

---

## Step 2b — Complete industry mapping

Every industry in the standard Yahoo Finance / Morningstar taxonomy, mapped to exactly one playbook. Use it as the starting point, not the conclusion: Step 1 overrules this table whenever the profit driver has drifted from the label, and Step 2a lists the labels that are actively misleading. Rows marked **(added)** are standard industries in that taxonomy that are easy to omit from a screener export.

The Note column carries a routing reason only where the mapping is non-obvious, where a common sub-case routes elsewhere, or where the playbook must be applied with a particular metric set. A blank note means the mapping is what it looks like.

| Industry | Playbook | Note |
|---|---|---|
| Advertising Agencies | `people-businesses.md` | Billings are the client's money, not revenue. Work on net revenue / gross profit and the conversion ratio. Not `telecom-media.md`. |
| Aerospace & Defense | `infra-capitalgoods.md` | Multi-year programme order book, milestone recognition, and a single government customer that also sets the price. |
| Agricultural Inputs | `chemicals-cement.md` | Fertilisers and agrochemicals: process manufacturing on a subsidised or regulated realisation with a raw-material spread. |
| Airlines | `aviation-hotels.md` | |
| Airports & Air Services | `aviation-hotels.md` | Where the asset is a fixed-term concession with a regulated tariff on an approved asset base, the value is a defined-life annuity — use `infra-capitalgoods.md`. |
| Aluminum | `metals-mining.md` | Power cost is the swing variable; captive power and bauxite integration decide who survives the trough. |
| Apparel Manufacturing | `fmcg-consumer.md` | Only where a brand sets the price. A private-label or contract garment maker has no pricing power — customer concentration and utilisation govern it, as in `Textile Manufacturing`. |
| Apparel Retail | `retail-ecommerce.md` | |
| Asset Management | `holdco-assetmgr.md` | A fee on other people's money: AUM × yield, flows and mix, with performance fees as the low-quality line. A BDC, listed credit fund or CLO vehicle deploying **its own** balance sheet is not a fee business — use `mortgage-reit-specialty-finance.md`. |
| Auto & Truck Dealerships | `auto.md` | Retail economics, not manufacturing: inventory turns, F&I attach, service absorption. Floorplan debt is inventory finance — strip it before computing leverage. |
| Auto Manufacturers | `auto.md` | Separate any captive finance arm and run it through `nbfc.md`; consolidated leverage and ROCE describe neither business. |
| Auto Parts | `auto.md` | Check OEM concentration and whether content per vehicle is rising — that, not industry volume, is the growth. |
| Banks - Diversified | `banks.md` | |
| Banks - Regional | `banks.md` | Deposit franchise quality and geographic loan concentration decide it; a regional bank is a bet on one local economy. |
| Beverages - Brewers | `fmcg-consumer.md` | |
| Beverages - Non-Alcoholic | `fmcg-consumer.md` | |
| Beverages - Wineries & Distilleries | `fmcg-consumer.md` | Maturing stock is a multi-year asset, so structurally high inventory days are the business model, not a warning. |
| Biotechnology | `biotech-clinical.md` | Pre-revenue only. Once an approved product is selling for the company's own account — or for any biosimilar, generic, API, CDMO or CRO business — use `pharma-healthcare.md`. See Step 2a. |
| Broadcasting | `telecom-media.md` | |
| Building Materials | `chemicals-cement.md` | Cement, lime, aggregates: regional realisation per tonne, freight radius and capacity utilisation. |
| Building Products & Equipment | `chemicals-cement.md` | Process manufacture of a construction input — boards, glass, insulation, pipes, tiles, sanitaryware. Where the product is engineered equipment sold on specification (HVAC, elevators, building automation), use `infra-capitalgoods.md`. |
| Business Equipment & Supplies **(added)** | `fmcg-consumer.md` | Branded product through a B2B dealer channel. Demand is corporate office and print spend, several categories of which are in secular decline — establish that before extrapolating volume. |
| Capital Markets | `exchanges-payments.md` | Brokers, investment banks and wealth platforms. Where the firm runs a large trading book, margin lending or prime brokerage, add `banks.md` for funding, capital adequacy and liquidity. |
| Chemicals | `chemicals-cement.md` | |
| Coking Coal | `metals-mining.md` | A steel input, so the cycle is steel's, not power's. Never pool with thermal coal. |
| Communication Equipment | `infra-capitalgoods.md` | Sells to operators, is not one — the driver is their capex budget and tender wins. Cross-read `semiconductors.md` where the value sits in silicon or optics. |
| Computer Hardware | `semiconductors.md` | The component and product cycle sets margin. For a box assembler reselling others' silicon, gross margin is thin and the real analysis is component pass-through and inventory. |
| Confectioners | `fmcg-consumer.md` | |
| Conglomerates | `holdco-assetmgr.md` | Sum-of-the-parts always, each subsidiary through its own playbook. Never a single consolidated multiple. |
| Consulting Services | `people-businesses.md` | |
| Consumer Electronics | `fmcg-consumer.md` | Branded durables: gross margin × velocity, channel inventory, replacement cycle. They buy silicon, they do not make it. |
| Copper | `metals-mining.md` | |
| Credit Services | `nbfc.md` | Only where the company carries the receivable. Networks, acquirers, processors and bureaus take no credit risk — use `exchanges-payments.md`. |
| Department Stores | `retail-ecommerce.md` | |
| Diagnostics & Research | `pharma-healthcare.md` | Labs and CROs on test and study volume × price; life-science tools on installed base and consumable pull-through. Neither has a patent cliff. |
| Discount Stores | `retail-ecommerce.md` | |
| Drug Manufacturers - General | `pharma-healthcare.md` | |
| Drug Manufacturers - Specialty & Generic | `pharma-healthcare.md` | Price erosion, not volume, is the default assumption; check plant inspection history before anything else. |
| Education & Training Services | `people-businesses.md` | Delivered by teachers: seats filled, fee per student, faculty cost and attrition. A self-serve online platform with no delivery headcount is `it-saas.md`. |
| Electrical Equipment & Parts | `infra-capitalgoods.md` | |
| Electronic Components | `semiconductors.md` | Passives, connectors, PCBs — the lead-time and channel-inventory cycle is the semiconductor cycle. |
| Electronic Gaming & Multimedia | `telecom-media.md` | Hit-driven slates carry content risk and capitalised development amortisation. A live-service or subscription game is recurring revenue — bookings, deferred revenue, DAU/MAU, ARPDAU — use `it-saas.md`. |
| Electronics & Computer Distribution | `retail-ecommerce.md` | Distribution, not technology: thin margin on throughput, inventory turns, vendor rebates and working capital. |
| Engineering & Construction | `infra-capitalgoods.md` | |
| Entertainment | `telecom-media.md` | Content amortisation policy decides reported profit; check it before comparing any margin. |
| Farm & Heavy Construction Machinery | `infra-capitalgoods.md` | Dealer channel inventory leads the cycle. Separate the captive finance arm (`nbfc.md`) before any leverage or return figure. |
| Farm Products | `fmcg-consumer.md` | Only for branded packaged players. Unbranded processors — sugar, edible oil, poultry, aquaculture — are price-takers on both sides; read the spread-and-utilisation logic in `chemicals-cement.md`. |
| Financial Conglomerates | `holdco-assetmgr.md` | Sum-of-the-parts, then `banks.md` / `insurance.md` / `nbfc.md` on each regulated subsidiary. Group leverage and group ROE describe nothing. |
| Financial Data & Stock Exchanges | `exchanges-payments.md` | |
| Food Distribution | `retail-ecommerce.md` | Drop size and route density on a low-single-digit margin; the customer is a restaurant or a retailer, not a consumer. |
| Footwear & Accessories | `fmcg-consumer.md` | Where own-channel DTC dominates the mix, add the store and cohort economics from `retail-ecommerce.md`. |
| Furnishings, Fixtures & Appliances | `fmcg-consumer.md` | Consumer durables: the cycle follows housing transactions and credit availability, not consumption. |
| Gambling | `aviation-hotels.md` | Land-based casinos and integrated resorts. An online-only sportsbook or iGaming operator owns no property and earns a hold rate on handle — use `exchanges-payments.md` for volume × take rate, and treat customer acquisition cost as the real cost line. |
| Gold | `metals-mining.md` | All-in sustaining cost per ounce, reserve grade and mine life. The gold price is a macro input, not a company variable. |
| Grocery Stores | `retail-ecommerce.md` | |
| Health Information Services | `it-saas.md` | Healthcare customer, software economics. Patent life, approval risk and clinical throughput have no referent. |
| Healthcare Plans | `insurance.md` | Managed-care metric set only: medical loss ratio, membership by line, premium per member per month, star ratings, risk adjustment. Not the P&C or life set. See Step 2a. |
| Home Improvement Retail | `retail-ecommerce.md` | |
| Household & Personal Products | `fmcg-consumer.md` | |
| Industrial Distribution | `retail-ecommerce.md` | A distributor, not a manufacturer: branch and DC economics, inventory turns, private-label mix, vendor rebates. |
| Information Technology Services | `it-saas.md` | Where the firm owns the delivery outcome. A resource-augmentation model billing a markup on a head with no delivery obligation is `people-businesses.md`. |
| Infrastructure Operations | `infra-capitalgoods.md` | Toll roads, annuity and BOT/HAM concessions: a defined-life cash-flow stream, so DCF over the concession term, never a perpetuity multiple. |
| Insurance - Diversified | `insurance.md` | Split the life and non-life books before valuing — they use different frameworks (EV and VNB versus combined ratio). |
| Insurance - Life | `insurance.md` | |
| Insurance - Property & Casualty | `insurance.md` | |
| Insurance - Reinsurance | `insurance.md` | Catastrophe exposure and reserve development dominate; one year's combined ratio is not information. |
| Insurance - Specialty | `insurance.md` | Genuine underwriters — title, mortgage, credit, warranty. An MGA, MGU or coverholder binding on someone else's paper holds no risk capital — use `insurance-brokers-services.md`. |
| Insurance Brokers | `insurance-brokers-services.md` | No underwriting risk, no float, no combined ratio, no solvency ratio, no meaningful book value. Never `insurance.md`. See Step 2a. |
| Integrated Freight & Logistics | `shipping-logistics.md` | Separate asset-heavy operations from asset-light forwarding; they carry different margins on different revenue bases and must not be blended. |
| Internet Content & Information | `it-saas.md` | Asset-light platform economics. Where revenue is advertising, the demand cycle is the ad cycle — cross-read `telecom-media.md`. |
| Internet Retail | `retail-ecommerce.md` | Establish first whether it is a first-party retailer (gross revenue, owned inventory) or a marketplace (GMV × take rate). The two are not comparable on any margin. |
| Leisure | `fmcg-consumer.md` | Branded discretionary durables — toys, boats, powersports, fitness equipment. Where the company operates venues, capacity is perishable — use `aviation-hotels.md`. |
| Lodging | `aviation-hotels.md` | Distinguish the owner (property NAV, cross-read `realestate-reit.md`) from the asset-light franchisor or manager, which is a royalty on system-wide RevPAR. |
| Lumber & Wood Production | `chemicals-cement.md` | Commodity conversion at a mill, driven by housing starts. A timberland owner is a land-NAV business — `realestate-reit.md`. |
| Luxury Goods | `fmcg-consumer.md` | Pricing power and brand heat are the whole thesis; volume growth without price growth is dilution of the brand. |
| Marine Shipping | `shipping-logistics.md` | |
| Medical Care Facilities | `pharma-healthcare.md` | Hospitals: occupancy, ARPOB, payer mix, case mix and doctor retention. |
| Medical Devices | `pharma-healthcare.md` | Approval pathway and reimbursement coding decide the market; the razor-and-blade consumable stream carries the margin. |
| Medical Distribution | `retail-ecommerce.md` | Fractions of a percent of gross margin on enormous revenue; the analysis is working capital and buy-side scale. No patent, no approval, no pricing power — not `pharma-healthcare.md`. |
| Medical Instruments & Supplies | `pharma-healthcare.md` | |
| Metal Fabrication | `metals-mining.md` | A converter, not a miner: margin is the conversion spread and the metal-cost pass-through lag, so a price spike temporarily inflates both revenue and margin. Where product is engineered to order against a backlog, add `infra-capitalgoods.md`. |
| Mortgage Finance **(added)** | `nbfc.md` | Originator-servicers: gain-on-sale margin, origination volume against the rate cycle, and mortgage servicing rights whose fair-value marks move opposite to origination. Earnings are hedged marks — anchor on book value, not EPS. |
| Oil & Gas Drilling | `oil-gas.md` | Day rates and rig utilisation, running roughly one cycle behind the crude price. |
| Oil & Gas Equipment & Services | `oil-gas.md` | |
| Oil & Gas Exploration & Production | `oil-gas.md` | Reserve life, finding and development cost and decline rate; production growth funded by outspending cash flow is not growth. |
| Oil & Gas Integrated | `oil-gas.md` | Segment-split before anything else — upstream and downstream move in opposite directions on the same crude move. |
| Oil & Gas Midstream | `oil-gas.md` | Fee-based contracted throughput is closer to a regulated utility than to E&P. Quantify the commodity-exposed share of margin, then read `utilities-power.md` for the contracted part. |
| Oil & Gas Refining & Marketing | `oil-gas.md` | |
| Other Industrial Metals & Mining | `metals-mining.md` | |
| Other Precious Metals & Mining | `metals-mining.md` | |
| Packaged Foods | `fmcg-consumer.md` | |
| Packaging & Containers | `chemicals-cement.md` | Process manufacture with resin or board input pass-through; the contract structure decides who bears the input move and with what lag. |
| Paper & Paper Products | `chemicals-cement.md` | |
| Personal Services | `people-businesses.md` | Labour-delivered services. Where delivery runs through owned outlets, add the unit economics from `retail-ecommerce.md`; where franchised, it is a royalty stream. |
| Pharmaceutical Retailers | `retail-ecommerce.md` | Pharmacy chains live on footfall, store throughput, prescription volume and front-of-store mix. Not `pharma-healthcare.md`. |
| Pollution & Treatment Controls | `infra-capitalgoods.md` | Equipment makers — scrubbers, ESPs, membranes, ZLD systems. Order book and customer capex, not route density. Not `waste-environmental.md`. |
| Publishing | `telecom-media.md` | |
| Railroads | `rail-freight.md` | Operating ratio (lower is better), maintenance-of-way capex and network fluidity. Never `shipping-logistics.md`. See Step 2a. |
| Real Estate - Development | `realestate-reit.md` | Revenue recognition on completion makes reported growth lumpy and largely uninformative; pre-sales, collections and the land bank are the real series. |
| Real Estate - Diversified | `realestate-reit.md` | Split rental (recurring, NOI and cap rate) from development (lumpy, completion-based) before valuing either. |
| Real Estate Services | `people-businesses.md` | Brokers, agency, valuation and property managers own no property — commission on transaction volume and fees on managed area. Cap rate, NAV, FFO and occupancy are undefined for them. See Step 2a. |
| Recreational Vehicles | `auto.md` | Dealer floorplan inventory is the leading indicator; channel stuffing precedes every downturn in this category. |
| REIT - Diversified | `realestate-reit.md` | |
| REIT - Healthcare Facilities | `realestate-reit.md` | Landlord to operators, so the risk is operator rent coverage (EBITDAR to rent), not patient volumes. Under a RIDEA structure the REIT takes the operating result instead — check the structure first. |
| REIT - Hotel & Motel | `realestate-reit.md` | It takes the hotel's operating result, not contractual rent, so WALE and lease-expiry schedules are undefined. Read RevPAR, ADR and hotel EBITDA from `aviation-hotels.md`. |
| REIT - Industrial | `realestate-reit.md` | |
| REIT - Mortgage | `mortgage-reit-specialty-finance.md` | Owns no buildings. Occupancy, WALE, same-store NOI, cap-rate spread, FFO and AFFO are undefined. Never `realestate-reit.md`. See Step 2a. |
| REIT - Office | `realestate-reit.md` | Lease expiry schedule and releasing spreads carry the thesis; mark leases to current market rent before accepting reported NOI as durable. |
| REIT - Residential | `realestate-reit.md` | |
| REIT - Retail | `realestate-reit.md` | |
| REIT - Specialty | `realestate-reit.md` | A wrapper, not a business. Route by what the tenant pays for: towers and fibre to `telecom-media.md`; data centres selling power-backed capacity to `utilities-power.md`; timberland as land NAV; net-lease gaming as single-operator rent coverage. |
| Rental & Leasing Services | `mortgage-reit-specialty-finance.md` | Lessor section. Fleet utilisation, lease yield, residual-value risk and funding ladder — a financial business, not an industrial one. See Step 2a. |
| Residential Construction | `realestate-reit.md` | Homebuilders: inventory is land and unsold units, and the land bank is where the balance-sheet risk lives. |
| Resorts & Casinos | `aviation-hotels.md` | |
| Restaurants | `aviation-hotels.md` | Same-store sales, covers and perishable capacity. An asset-light franchisor earning royalties on system sales is a brand annuity — cross-read `fmcg-consumer.md`. |
| Scientific & Technical Instruments | `infra-capitalgoods.md` | Precision instruments sold into R&D and industrial capex; the service and consumable attach carries the margin. Where the customer is a fab, the driving cycle is semi capex — `semiconductors.md`. |
| Security & Protection Services | `people-businesses.md` | Manned guarding and facilities services are labour arbitrage: wage pass-through, attrition and contract renewals. Electronic-security equipment makers are `infra-capitalgoods.md`. |
| Semiconductor Equipment & Materials | `semiconductors.md` | Demand is customer capex, so it leads the chip cycle on the way in and lags it on the way out. |
| Semiconductors **(added)** | `semiconductors.md` | Establish the model first — fabless, foundry, IDM or memory — because gross margin, capital intensity and cycle exposure differ completely between them. |
| Shell Companies | `references/13-situations.md` §15 | Not a sector playbook. There is no business: trust value per share, sponsor promote, warrants, redemption deadline and the fully diluted count are the analysis. Route to a sector playbook only after a merger closes. See Step 2a. |
| Silver | `metals-mining.md` | Frequently a by-product of base-metal mining — check whether silver is primary revenue or a credit against another metal's cost. |
| Software - Application | `it-saas.md` | |
| Software - Infrastructure | `it-saas.md` | |
| Solar | `semiconductors.md` | Cell, wafer, module, inverter and tracker manufacture: utilisation, ASP deflation, inventory write-downs. Polysilicon, glass and encapsulants go to `chemicals-cement.md`; a developer or IPP selling power under a PPA goes to `utilities-power.md`. See Step 2a. |
| Specialty Business Services | `people-businesses.md` | Facilities management, testing/inspection/certification, contact centres — outsourced labour with a contract book. |
| Specialty Chemicals | `chemicals-cement.md` | Test the "specialty" claim against margin stability and customer stickiness; much of what is labelled specialty is a commodity with a longer contract. |
| Specialty Industrial Machinery | `infra-capitalgoods.md` | |
| Specialty Retail | `retail-ecommerce.md` | |
| Staffing & Employment Services | `people-businesses.md` | Gross profit, not revenue, is the top line, and the margin metric is the conversion ratio, not OPM. |
| Steel | `metals-mining.md` | |
| Telecom Services | `telecom-media.md` | |
| Textile Manufacturing | `chemicals-cement.md` | Spinning, weaving and man-made fibre are commodity conversion — the cotton- or polyester-to-yarn spread at a given utilisation. A branded apparel business is `fmcg-consumer.md`. |
| Thermal Coal | `metals-mining.md` | Demand is power generation, so the cycle is the utility cycle. Check whether output moves under long-term linkage and fuel supply agreements or at spot — the earnings volatility differs entirely. |
| Tobacco | `fmcg-consumer.md` | Volume declines structurally and price carries everything; excise and litigation are the real risk register. |
| Tools & Accessories | `fmcg-consumer.md` | Branded durables through retail and pro distribution; channel inventory leads reported sales. Separate any captive dealer-finance book into `nbfc.md`. |
| Travel Services | `aviation-hotels.md` | Distinguish the principal (owns the inventory and the risk) from the agent. For an OTA the driver is take rate on gross bookings, not reported revenue growth. |
| Trucking | `shipping-logistics.md` | Spot-rate cyclical with no network moat. Never `rail-freight.md`. See Step 2a. |
| Uranium | `metals-mining.md` | Sold to utilities on long-term contracts, so the realised price is the contract book rather than spot. Conversion and enrichment are separate process businesses. |
| Utilities - Diversified | `utilities-power.md` | Split regulated from merchant before anything else — one earns an allowed return on a rate base, the other takes price risk. |
| Utilities - Independent Power Producers | `utilities-power.md` | PPA-contracted and merchant capacity are different businesses. Offtaker credit quality and receivable days decide whether the contracted cash flow is real. |
| Utilities - Regulated Electric | `utilities-power.md` | A utility earning its allowed RoE is performing correctly, not poorly; the analysis is rate-base growth and the regulatory relationship. |
| Utilities - Regulated Gas | `utilities-power.md` | Rate-base utilities only. A city gas distributor earning a spread on sourced gas rather than a return on an approved asset base belongs in `oil-gas.md`. |
| Utilities - Regulated Water | `utilities-power.md` | Rate base and allowed return, same frame as electric. A contract operator of municipal water and wastewater with no rate base is a services business — `waste-environmental.md`. |
| Utilities - Renewable | `utilities-power.md` | Selling power under a PPA or feed-in tariff. Manufacturing cells or modules is not a utility — see `Solar` and Step 2a. |
| Waste Management | `waste-environmental.md` | Landfill airspace, internalisation rate and closure and post-closure liabilities — which are debt, and sit outside reported borrowings. |

---

## Step 3 — Multi-segment companies

Most real companies are not pure. Route as follows:

1. **Rank segments by profit, not revenue.** Use segment EBIT / segment result from the segment note. In India this is the Ind-AS 108 disclosure in the standalone and consolidated statements; in the US it is the ASC 280 note in the 10-K plus the segment discussion in MD&A. Unallocated corporate costs and inter-segment eliminations are noise — note their size but do not let them decide.

2. **The playbook of the dominant profit segment governs.** If one segment is >60% of EBIT, run its playbook as the primary lens and treat the rest as adjustments.

3. **Explicitly name the secondary segments and what they do to the consolidated numbers.** State the distortion in one line each. Typical distortions: a finance arm inflates consolidated debt and destroys the parent's debt/equity comparability; a property segment holds land at historical cost and hides value; a trading segment inflates revenue and deflates blended margin.

4. **Use SOTP when segments belong to different families** — for example a manufacturer with a lending arm, or a consumer company with a large real-estate holding. Value each segment on its own family's multiple (a lender on P/B or P/adjusted book, a brand on EV/EBITDA or P/E, property on NAV), net out holding-company debt and costs, and apply a holding discount if the segments are not separately monetisable. Never apply a single consolidated P/E across a mixed group — the blend is arithmetic without meaning.

5. **When no segment exceeds ~40% of profit**, treat the company as a de facto conglomerate and go to Step 4.

6. **Score it mechanically rather than from memory.** `scripts/score.py` takes a `segments` array and scores each segment against its own sector's benchmarks, then blends by EBIT (falling back to capital employed or revenue automatically when a segment loses money, because a negative EBIT weight would subtract that segment's score from the group). It prints the concentration test in points 2 and 5 above, the mixed-family contamination warning, and the reminder that a blended score is not a substitute for SOTP. Run `python scripts/score.py --example-segments` for a complete runnable three-segment input to copy, and see `references/11-scoring-rubric.md` §10.

7. **Watch for segment drift.** Compare the profit mix to three and five years ago. A company being re-rated as a "specialty chemicals" or "SaaS" story while the profit mix has barely moved is a narrative, not a re-rating. Conversely, a genuine mix shift justifies changing the governing playbook — say so explicitly and date the change.

---

## Step 4 — Conglomerates and holding companies

Route to `holdco-assetmgr.md` when the parent's own operations are small and its earnings are substantially dividends, fees, or the equity-accounted share of subsidiaries and associates. Route to `holdco-assetmgr.md` **in addition to** the operating playbooks when the group has several material, genuinely different businesses.

Rules that apply to every conglomerate:

- **Sum-of-the-parts is the default method**, not a supplementary one. Value listed stakes at market value (state the date and whether you used a discount for illiquidity or lock-in), unlisted subsidiaries on their own sector multiples, and treasury/real-estate assets separately. Deduct net debt at the holding level and capitalise recurring holdco costs.
- **Holding-company discount is real and persistent.** Discounts to underlying NAV are the norm rather than the exception, driven by tax on monetisation, minority stakes that cannot be sold, and the market's doubt about capital allocation. Compare the current discount to the entity's own history — a discount narrowing or widening versus its own five-year range is far more informative than the absolute level.
- **Consolidated financials of a conglomerate are usually the least useful statement.** Consolidation mixes a lender's balance sheet with a manufacturer's, and minority interests can mean the parent owns a small share of the profits it reports. Always check profit attributable to owners versus total profit, and the size of non-controlling interests.
- **Related-party transactions are the central governance risk.** In India, read the related-party note, the CARO report and auditor qualifications, and check promoter pledge levels and any inter-corporate deposits or guarantees to group entities. In the US, read the related-party disclosures and Item 13 of the 10-K/proxy. Cross-subsidy between group companies changes who the minority shareholder is actually financing.
- **Capital allocation is the real asset.** For a conglomerate, the question is not "what does it own" but "where does incremental capital go and at what return". Track incremental capital deployed by segment over five years against incremental EBIT.

---

## Step 5 — When nothing fits

With Step 2b in place, every industry in the standard taxonomy resolves to a playbook, so arriving here should now be **rare**. When it happens the cause is almost never a missing playbook — it is that the company's economics have drifted away from the label a data provider attached to it, or that the entity is a combination of two businesses rather than one. Treat reaching this step as a prompt to re-run Step 1 on the profit mix, not as licence to invent a framework.

Do not force a fit. Do this instead:

1. **Decompose the P&L into the two or three sub-businesses it actually is**, and route each one. Almost every "unclassifiable" company is a combination, not a novelty.
2. **Route by economics rather than product.** A satellite operator resembles a tower company (`telecom-media`). A ship-leasing company resembles an equipment lessor, which is a spread-and-residual-value business (`mortgage-reit-specialty-finance`), not a shipping operator. A data-centre owner is a landlord (`realestate-reit`) if it leases space, a `utilities-power` analogue if it sells power-backed capacity on long contracts, and an `it-saas` analogue if it sells managed compute — the contract structure decides.
3. **Fall back to the family-level lens** in the table below and use the generic metrics that survive: cash conversion, return on invested capital versus cost of capital, and the trajectory of the company's own history.
4. **Check whether the right file is a situation overlay rather than a sector playbook.** A listed shell or SPAC, a de-SPAC, a pre-revenue developer, a company in liquidation or a pure treasury vehicle is a *situation*, not a sector — `references/13-situations.md` governs, and the sector playbook applies only to whatever operating business emerges later.
5. **Say so in the output — this requirement does not relax just because the mapping is complete.** Write one line naming the industry label you were given, the mapping row you rejected, and the route you took: "Classified as X in the source data; routed to Y rather than the mapped Z because profit is driven by W." An explicit, defensible choice beats a silent mis-route, and it lets a reader attack the routing decision directly instead of reverse-engineering it from the metrics.
6. **Never substitute a peer set you do not believe in.** If there are no true comparables, use the company's own history across a full cycle as the benchmark and say that peer comparison was unavailable.

---

## Sector families — which standard metrics break

Fast sanity check. If you are about to compute a metric in the "undefined" or "inverted" column for that family, stop.

| Metric | Financials (banks, NBFC, insurance, some exchanges) | Real-asset / regulated (utilities, REIT/realestate, infra, telecom, shipping) | Cyclical-commodity (metals, oil & gas, chemicals-cement, semis-memory, autos) | Asset-light (IT-SaaS, FMCG, pharma-branded, exchanges, retail) |
|---|---|---|---|---|
| Revenue / "sales" | **Undefined as normally used.** Use net interest income + fee income (banks/NBFC), or gross written premium and net earned premium (insurance) | Usable, but check regulated vs merchant split; for REITs use rental income and NOI | Usable, but it is price × volume — always decompose | Usable and meaningful |
| Debt/equity, net debt/EBITDA | **Undefined/meaningless.** Debt is raw material. Use CAR/CRAR (banks), capital adequacy and gearing (NBFC), solvency ratio (insurance) | Usable but high leverage is normal and often correct; compare to peers and to contracted cash flow cover, not to a generic 1x rule | Usable and critical — leverage at cycle peak is the standard way these companies die | Usable; sustained high leverage is a red flag |
| EBITDA / EV-EBITDA | **Undefined.** Interest is revenue, not a financing cost | Usable and standard, but EBITDA ignores the maintenance capex that keeps the asset alive — always pair with capex | Usable but must be read against mid-cycle, never peak | Usable; closest to economic reality here |
| P/E | Usable but secondary to P/B for lenders; for life insurers use P/EV and VNB multiples | Distorted by depreciation policy and asset revaluation; for REITs use P/FFO or P/AFFO, not P/E | **Inverted at extremes.** Low P/E at peak earnings signals a top; high P/E at trough earnings can signal a bottom | Usable and primary |
| P/B | **Primary metric** for banks and NBFCs — but only against *adjusted* book after netting stressed assets | Meaningful only if the book reflects current asset value; historical-cost land makes book value fiction | Meaningful as a floor valuation near troughs (P/B near or below 1 on replacement-cost assets) | Largely meaningless — book value omits brands, code and IP |
| Net profit margin | Use NIM, cost-to-income and credit cost instead | Depressed by depreciation and interest on the asset base — do not compare to asset-light peers | Swings by tens of percentage points across a cycle; a single-year figure is not information | Meaningful; compare to own history and direct peers |
| ROE | Flattered by leverage — always read alongside ROA and capital adequacy; a lender with high ROE and thin capital is fragile, not excellent | Often capped by regulation (a regulated utility earning its allowed RoE is performing correctly, not poorly) | Peak-cycle ROE is not a run rate; use average-through-cycle ROCE | Meaningful; check it is not manufactured by buybacks shrinking equity |
| ROCE / ROIC | **Undefined** in the standard form — capital employed is the funding base | Use, but compare to the regulated or contracted allowed return, not to a generic hurdle | Use through-cycle averages only | Primary metric; compare to cost of capital |
| Free cash flow | Standard FCF is **not meaningful** — loan growth consumes cash and is a good thing. Use pre-provision operating profit and capital generation | Meaningful, but separate growth capex from maintenance capex or you will call a growing utility cash-destructive | Meaningful; watch that working capital release in a downturn is not read as improvement | Primary metric; should track net profit closely over time |
| Inventory / receivable days | **Undefined** — no inventory in the normal sense | Limited relevance except for developers (inventory = unsold units, and it matters enormously) | Central. Rising inventory into a price fall is the classic warning | Central for retail and FMCG; near-irrelevant for SaaS |
| Dividend payout | Constrained by regulator and capital needs; a high payout from a thinly capitalised lender is a warning | For REITs/InvITs, a high mandated payout is structural, not generosity — India: InvIT/REIT distribution rules; US: REIT distribution requirement | High payout at cycle peak often precedes a cut | Meaningful signal of capital discipline |
| Depreciation | Small and uninformative | **Systematically overstates economic cost** where assets appreciate (property) — this is why FFO exists | Broadly economic; check for impairments hiding a bad capex cycle | Small; watch capitalised software and R&D policy |
| Asset turnover | **Undefined** | Structurally low by design | Cyclical; falls first as demand rolls over | High; a falling trend is an early warning |

Ranges and thresholds anywhere in the sector playbooks are **indicative only**. They vary by market, by point in the cycle, by accounting regime and by period. A peer-set comparison and the company's own multi-year history always override any absolute band printed in these files.

---

## Fast sanity check before you leave this file

Before running any playbook, confirm you can answer these in one line each. If you cannot, you have not classified the company yet.

- Which segment produces most of the **profit** (not revenue)?
- Which of the four families does the balance sheet belong to?
- Who sets the selling price?
- Where is this company in its cycle — and does the sector even have one?
- Which standard metrics are undefined or inverted here, per the table above?
- What is the correct peer set: same sector, similar size, similar business model, same market? Cross-market peers (a US generic vs an Indian generic, a US bank vs an Indian bank) differ in tax, accounting, rate environment and disclosure — note the differences rather than pretending comparability.

India-specific notes that affect routing: check the standalone versus consolidated split before ranking segments (many Indian groups hold operating businesses in subsidiaries, so standalone numbers describe a shell); read the latest earnings concall transcript for management's own segment framing; check promoter holding and pledge; and read CARO qualifications for related-party and asset-verification flags. US/global notes: use the 10-K segment note and MD&A, check for non-GAAP reconciliations that exclude recurring stock-based compensation, and read the risk factors for the company's own statement of what drives its economics.

---

## Checklist

- [ ] Ranked segments by EBIT/segment result, not revenue, before choosing a playbook.
- [ ] Answered the five classification questions: profit source, balance-sheet role, price setter, unit of production, failure mode.
- [ ] Ignored the index/GICS label where it conflicts with the profit driver, and said so.
- [ ] Checked the industry name against the Step 2a trap list **before** accepting any mapping — mortgage REIT, insurance broker, lessor, healthcare plan, shell company, railroad, solar, real-estate services, drug distributor, pharmacy, ad agency, pollution-control equipment.
- [ ] Took the route from the Step 2b mapping row for the stated industry, or overruled it on the profit driver and stated the override in the output.
- [ ] For a conditional row — Biotechnology, Solar, Utilities - Renewable, Credit Services, Information Technology Services, Insurance - Specialty, Gambling, REIT - Specialty — applied the stated test and recorded which side it fell on.
- [ ] Where the mapping sends part of the company elsewhere (captive finance arm, franchisor royalty stream, property held on balance sheet), separated it rather than blending it into the primary lens.
- [ ] Routed to exactly one primary playbook; named any secondary playbooks and the distortion each creates in consolidated numbers.
- [ ] Used SOTP where segments belong to different families; never applied one blended P/E across a mixed group.
- [ ] For conglomerates: valued parts separately, deducted holdco debt and costs, compared the holding discount to its own history, and checked related-party exposure and minority interests.
- [ ] Checked the undefined/inverted table and struck out every metric that does not exist for this family.
- [ ] Confirmed the peer set is genuinely like-for-like (sector, size, model, market); otherwise fell back to the company's own multi-year history and said so.
- [ ] Treated every indicative range as indicative — anchored the conclusion to peers and own history.
- [ ] If nothing fit: decomposed into sub-businesses, routed by economics, and stated the hybrid classification explicitly in the output.
