# Fee Stack Library (LP perspective)

The fees an LP pays in a private deal, plus the waterfall mechanics that
determine how promote / carry actually flows. Use this file to spot when a
deal's fee stack is in market-norm territory, when it's aggressive enough to
warrant pushback, and when an essential fee category is suspiciously absent.

## How to read this file

- **What the LP actually pays.** Every fee is net of any operator-borne or
  seller-paid components.
- **"Variable" is a real value.** Where a fee's market norm is genuinely
  unstable — direct GP-sponsored deals with no platform overhead, niche
  asset-class promote structures, definitionally-drifting "servicing" fees in
  private credit — the cell says *variable* with a one-line reason. *Variable*
  tells the analyst the baseline is the deal's own disclosure, not a category
  default.
- **Absent fees flag against this baseline.** A deal that omits a fee
  category most deals of that type carry (e.g. an equity syndication with no
  asset management fee disclosed) is a flag, not a neutral silence — either
  the fee is rolled into another line or it's not been told to you.
- **"Frequency" drives the drag math.** A 1.5% headline lands very differently
  as a one-time fee vs an annual recurring charge. Frequency is in every fee
  row precisely because the same nominal rate can produce 10× different LP
  drag depending on it.

## At a glance

| Category | Common fees | Typical LP-bearing range | Applies to |
|---|---|---|---|
| Acquisition | Acquisition fee | 1–2% of equity raised (or 0.5–1.5% of purchase price) | Equity syndications, Development |
| Asset management | Asset management fee | 1–2% of equity raised, annual | Equity, Preferred equity |
| Financing | Loan placement / refinance fees | 0.5–1.5% of loan amount per event | Equity (when debt is involved) |
| Disposition | Disposition fee | 0.5–1% of sale price | Equity syndications |
| Promote / carry | Promote, sitting above a preferred return | 15–30% above 6–10% pref | Equity, Preferred equity (capped), funds |
| Construction | Construction / development management | 3–5% of hard costs | Development deals |
| Fund-level | Management fee | 1–2% of committed (then invested) capital, annual | Hard money funds, Private credit |
| Servicing | Loan servicing fee | 0.25–0.5% of loan balance, annual | Hard money, Private credit |
| Performance | Performance fee above hurdle | 10–20% above 5–8% hurdle | Hard money, Private credit |
| Misc | Admin, IR, K-1 prep | 0.1–0.5% of equity or fixed $/LP | All deal types |

---

## Equity syndications

The default retail-LP deal structure: a GP sponsor raises equity from LPs to
acquire a single asset (or a small portfolio), operates it for a stated hold
period, and exits. Fee load is moderate but compounded across the hold; the
waterfall is where most of the GP's economics actually live.

### Fee inventory

| Fee | Typical range | Aggressive threshold | Frequency | Applies to | Notes |
|---|---|---|---|---|---|
| Acquisition fee | 1–2% of equity raised, or 0.5–1.5% of purchase price | >2.5% of equity or >2% of purchase price | One-time at close | All equity syndications | Compensates GP for sourcing + closing. Aggressive if GP also takes a separate "sponsor fee" on top. |
| Asset management fee | 1–2% of equity raised, annual | >2.5% annual | Annual recurring | All equity syndications | Compensates ongoing oversight. Some GPs calc on invested capital (lower) instead of equity raised. |
| Disposition fee | 0.5–1% of sale price | >1.5% | One-time at sale | Equity syndications | Compensates GP for sale execution. Stacks with brokerage commission paid by the deal — verify no double-charge. |
| Loan placement fee | 0.5–1.5% of loan amount | >2% | One-time at financing | Equity (debt-financed deals) | If GP also receives a mortgage-broker rebate from the lender, the fee should be reduced or disclosed. |
| Refinance fee | 0.5–1% of new loan | >1.5% | One-time per refi event | Equity (refi-based business plans) | Watch for stacking — some plans refinance twice in a 5-year hold. |
| Promote / carry | 15–30% above 6–10% pref | >30% promote, OR pref <6%, OR no pref | Contingent (sits inside waterfall) | Equity syndications | The economic core of the deal — see Waterfall mechanics below. |
| Construction management | 3–5% of hard costs | >6% | Contingent (development/value-add) | Development and heavy value-add | Larger than a typical asset mgmt fee because GP is overseeing a contractor. See Development variations below. |
| Investor relations / admin | 0.1–0.5% of equity, or $1–3k per LP annually | >$5k/LP or tiered admin fees | Annual recurring | All equity syndications | K-1 prep often bundled here. Tiered admin schemes (more for smaller checks) penalize retail LPs. |

### Waterfall mechanics

The waterfall is the rule for how cash from the deal splits between LPs and
the GP. It is the highest-impact economic feature of a syndication after the
fee inventory — the same headline *"20% promote over 8% preferred return"*
produces materially different LP outcomes depending on which waterfall
structure carries it.

**Deal-by-deal vs whole-of-fund** *(often called American vs European)*

- **Deal-by-deal waterfall (American)** — the GP earns promote on each
  investment as that investment exits. Fast cash to the GP. The LP can end
  with net IRR below the headline preferred return if early deals win and
  late deals lose, because the GP already took promote on the winners. Most
  retail real estate syndications use this structure.
- **Whole-of-fund waterfall (European)** — the GP earns nothing until the LP
  has received *all* contributed capital back *plus* the preferred return
  across the entire portfolio. Slower cash to the GP, materially better LP
  protection. Standard in institutional PE funds; less common in retail LP
  real estate. *Absence of any disclosure on which structure the deal uses is
  itself a flag* (see `03-red-flag-library.md`).

**Preferred return**

- **Cumulative** — unpaid preferred return in one period carries forward and
  must be paid before the GP earns promote. Standard.
- **Non-cumulative** — unpaid pref in one period is lost. *Variable* in
  practice but rare; non-cumulative pref is an aggressive flag on its own.
- **Compounding vs simple** — compounding pref accrues at the stated rate on
  the growing unpaid balance; simple accrues only on original investment.
  Compounding is more favorable to the LP. Most deals use simple.

**Promote structure**

- **Catch-up phase** — after the LP receives the preferred return, some deals
  give the GP a *catch-up* (often 50%, 80%, or 100% of cash flow until the GP
  reaches its equivalent split of profits to that point). The catch-up rate
  is one of the more aggressive levers in promote design.
- **Split tiers** — past the catch-up, deals typically split residual cash
  flow in tiers (e.g. 80/20 LP/GP up to 12% IRR, 70/30 up to 15%, 60/40 above
  15%). The tier *boundaries* matter as much as the percentages.

**Clawback and GP catch-up**

- **Clawback** — a provision that allows LPs to recover excess promote paid
  to the GP if final fund-level returns underperform. Standard in
  whole-of-fund waterfalls; rare in deal-by-deal. *Absence in a deal-by-deal
  waterfall* is a major flag — without clawback, the GP keeps promote on
  early winners even if late losers wipe out LP capital.

**Worked example** *(8% pref, 80/20 split, 100% GP catch-up to 8% equivalent,
$1M LP invest, 7-year hold)*

At 12% gross deal IRR: LP gets the first 8% pref (≈$80k/yr for 7 years), then
the GP catches up until receiving 20% of cumulative LP profits to that point.
Above the catch-up, residual splits 80/20 LP/GP. **Approximate LP net IRR
≈ 10.5–11%.** Headline gross was 12%; the ~150bps spread is the promote
drag in this structure.

At 15% gross deal IRR: same structure, more residual to split. **LP net IRR
≈ 12.5–13%.** Promote drag widens to ~200bps because the GP's 20% share is
on a larger residual.

(See `scripts/fee_drag_calculator.py` for the executable version with full
fee stack drag added.)

### Development-deal fee variations

Ground-up development and heavy value-add carry fees the typical stabilized
syndication does not:

- **Development fee** — 3–5% of total project cost, one-time. Compensates GP
  for entitlement risk, design oversight, and construction-period management.
  Aggressive: >6% or split across both a development fee *and* construction
  management fee.
- **Entitlement fee** — *variable*, when present. Some deals charge a
  separate fee for securing zoning, permits, and approvals; many roll it
  into the development fee.
- **Construction contingency reserve** — 5–10% of hard costs is typical and
  industry-standard. Aggressive: <5% (under-reserved) or >15% (likely padding
  the budget to inflate the fee base).

---

## Preferred equity

A middle-of-the-capital-stack position: the LP gets a contractual preferred
return ahead of common-equity LPs and sometimes a small equity kicker, in
exchange for capped upside. Fee load is lighter than equity syndications but
the preferred return itself is the headline economic.

### Fee inventory

| Fee | Typical range | Aggressive threshold | Frequency | Applies to | Notes |
|---|---|---|---|---|---|
| Origination / placement fee | 1–2% of investment | >3% | One-time at close | Preferred equity | Sometimes called "structuring fee." |
| Preferred return rate | 8–12% | <7% (under-compensated for risk) or >15% (likely distressed) | Annual recurring (accrued) | Preferred equity | The headline economic of the deal — not strictly a fee, but the rate at which the LP is paid before common LPs see any cash. |
| Servicing fee | 0.5–1% annual | >1.5% | Annual recurring | Preferred equity | Sometimes called "admin fee" or rolled into the origination fee. |
| Equity kicker / participation | 5–20% participation above pref | >25% participation | Contingent | Some preferred equity deals | A second economic layer — the LP gets the pref *and* a share of common upside. Variable across deals. |
| Exit / maturity fee | 0.5–1% of investment | >2% | One-time at maturity | Some preferred equity | Compensates sponsor for refinance / takeout. Stacks with the pref — verify no double-dip. |

### Preferred-return mechanics

Same cumulative-vs-non-cumulative and simple-vs-compounding distinctions as
the equity-syndication waterfall above — see that section for the LP
implications. Cumulative + simple is the typical preferred equity structure;
non-cumulative or simple-only is a flag.

Preferred equity rarely uses a full waterfall with promote tiers — the pref
*is* the structure. If a preferred equity deal also discloses a promote /
catch-up above the pref, it's behaving like equity dressed as preferred, and
the pref-equity risk profile no longer applies.

---

## Hard money / bridge debt

Senior secured short-duration debt against real estate. Fees exist at two
levels: per-loan (borrower pays, flows into fund yield) and fund-level (LP
pays directly). For LP screening, the fund-level fees and the *quality* of
the underlying per-loan pricing both matter.

### Fee inventory

| Fee | Typical range | Aggressive threshold | Frequency | Applies to | Notes |
|---|---|---|---|---|---|
| Origination points (borrower-paid) | 1–3 points (% of loan) | <1 point (yield too low) or >5 points (predatory) | One-time per loan | All hard money / bridge | Borrower pays at funding; flows into fund yield. *Low* origination is a flag — the GP may be giving up yield to win deal flow. |
| Fund management fee | 1–2% of AUM, annual | >2.5% | Annual recurring | Hard money / bridge funds | Sometimes step-downs after the investment period; absence of step-down is a flag in long-dated funds. |
| Servicing fee | 0.25–0.5% of loan balance, annual | >1% | Annual recurring | Per loan, flows into GP economics | Standard for active loan administration. |
| Performance fee / carry | 10–20% above 5–8% hurdle | >25%, OR no hurdle | Contingent | Some hard money funds | Less common than in equity syndications, but increasing in retail-LP HML funds. No-hurdle promotes are aggressive. |
| Late fees / default interest | *Variable* — fund-specific | None — these go to the fund, not the GP | Contingent | All hard money | Late fees and default interest typically benefit the LP (boost fund yield), not the GP. Verify they're not siphoned into a GP "workout fee." |
| Wind-down / liquidation fee | 0.5–1% of remaining AUM | >2% | One-time at fund close | Some hard money funds | Compensates GP for managing the runoff period. Absent in most short-duration funds. |

---

## Private credit funds

Private corporate or specialty lending — debt-only, senior secured, longer-
duration commitments than hard money. Fee structures borrow from both PE
(management + carry) and from hard money (servicing).

### Fee inventory

| Fee | Typical range | Aggressive threshold | Frequency | Applies to | Notes |
|---|---|---|---|---|---|
| Management fee | 1–2% of committed capital during investment period; 1–1.5% of invested capital after | >2%, OR no step-down post-investment-period | Annual recurring | All private credit funds | Step-down at end of investment period is industry-standard. Absence is a flag. |
| Performance fee / carry | 10–20% above 5–7% hurdle | >25%, OR hurdle <5% | Contingent | All private credit funds | Usually with a high-water mark (no carry on losses recouped). |
| Hurdle structure | Soft hurdle (with catch-up) or hard hurdle (no catch-up) | Soft hurdle with 100% catch-up is aggressive | Contingent | All private credit funds | Hard hurdle is more LP-favorable. |
| Servicing fee | 0.25–0.5% of loan balance | >1% | Annual recurring | Per loan | Same shape as hard money. |
| Fund-level leverage costs | *Variable* — depends on whether the fund itself uses leverage | If fund leverage >1.5× equity, the LP is taking compounded credit risk | Annual recurring | BDC-style and some private credit funds | Verify whether fund-level leverage is disclosed and whether the LP's IRR is on a levered or unlevered basis. |
| Admin / IR | $1–3k per LP annually, or 0.1–0.3% of capital | >$5k/LP | Annual recurring | All private credit funds | K-1 prep often bundled. |

---

## Total-drag framework

The gap between a deal's *gross* IRR (what the underlying property or
portfolio produces) and the LP's *net* IRR (what the LP actually keeps) is
the **total drag** — the sum of every fee and the promote, compounded over
the hold period. For screening, the drag should be calculable from the fee
stack disclosure alone; if it's not, the disclosure is incomplete.

**The math, schematically:**

```
Net LP IRR ≈ Gross deal IRR
           − (annual asset mgmt %    × hold years × compounding factor)
           − (one-time fees %        ÷ hold years × annualization factor)
           − (promote impact, depending on waterfall structure)
           − (fund-level fees, where applicable)
```

The compounding and annualization factors are why the same headline rate
lands differently. A 2% one-time acquisition fee on a 3-year hold is ~67bps
of annual drag; the same fee on a 10-year hold is ~20bps. A 1.5% annual asset
management fee on a 7-year hold compounds to ~10.5% of equity raised, before
any promote impact.

**Worked example.** Multifamily value-add syndication, $1M LP investment,
7-year hold, 15% claimed gross deal IRR. Fee stack: 2% acquisition, 1.5%
annual asset management, 1% disposition, 0.3% admin annually, 20% promote
over 8% cumulative simple pref with 100% catch-up, 80/20 split above.

- Acquisition: 2% one-time ≈ 30bps/year drag.
- Asset mgmt: 1.5% × 7 years = 10.5% cumulative ≈ 150bps/year drag.
- Disposition: 1% one-time ≈ 15bps/year drag.
- Admin: 0.3% × 7 years ≈ 30bps/year drag.
- Promote: ~200bps/year drag at 15% gross IRR (from the waterfall worked
  example above).

**Approximate net LP IRR ≈ 10.5–11%.** The deal needs to deliver close to its
claimed gross to clear a respectable LP outcome; a 200bps shortfall on the
property's actual performance compresses the LP's net much faster than a
single line item would suggest.

**Fund-of-funds layering.** When a deal is accessed through a feeder fund or
fund-of-funds wrapper, expect an additional 50–150bps of annual drag from the
wrapper's own management fee. The wrapper's fee is rarely disclosed
alongside the underlying deal's fee stack — verify both layers separately.

(See `scripts/fee_drag_calculator.py` for the executable version of this
calculation with configurable parameters.)

---

## Provenance

The shared sources in `01-asset-class-norms.md` → Provenance, read for fees
(ILPA fee templates, Preqin fee benchmarking, NCREIF expense ratios), plus:

- **SEC Form ADV filings.** For RIA-managed funds — fee schedules disclosed
  in Part 2.

*Last reviewed: 2026-05-30. Re-baseline when realized fee drag across
surveyed funds shifts materially or when a new fee category emerges (e.g.
the rise of "GP commitment financing fees" in 2024–25 retail-LP deals is the
kind of new category that should land here in a v1.1 update).*
