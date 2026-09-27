# Red Flag Library (LP perspective)

Categorized warning signs an LP should catch when screening a passive deal,
each with the **mechanism** (why it's a flag) and a one-line **response** (what
to ask the GP). Use this file to convert a vague unease about a deal into a
specific, severity-ranked list of exposures and questions.

## How to read this file

- **Severity is RED or YELLOW, from the LP's recovery perspective.**
  - **RED** — a structural or financial feature that can impair LP capital or
    materially break the return story. A RED flag is a pass-or-resolve before
    committing.
  - **YELLOW** — a feature that warrants a specific question and a satisfactory
    answer; not disqualifying on its own, but a cluster of YELLOWs is a RED.
  - **YELLOW–RED** — boundary flags whose severity depends on the answer
    (e.g. how aggressive, how undisclosed). Treat as RED until the answer
    moves it down.
- **Flag IDs encode scope of applicability.** The prefix tells you which deals
  a flag applies to; the number is stable so `04-question-bank.md` can cite it.
  - **`GEN-`** — applies across all/most deal types (GP behavior, most
    structural / financial / disclosure / market-cycle flags).
  - **`EQUITY-`** — equity-syndication-specific.
  - **`PREF-`** — preferred-equity-specific.
  - **`HML-`** — hard money / bridge-debt-fund-specific.
  - **`CREDIT-`** — private-credit-fund-specific.
- **Absent disclosure is itself a flag.** Most flags fire on what a deal *says*;
  the Disclosure category fires on what it *doesn't*. A missing essential
  disclosure (per `01-asset-class-norms.md`) is scored, not passed over.
- **Thresholds are screening heuristics, not underwriting.** Where a numeric
  trigger is well-established (promote >30%, pref <6%, fund leverage >1.5×) it
  comes from `02-fee-stack-library.md`; where a pattern is real but the
  threshold is cycle-sensitive, the flag describes the pattern qualitatively
  and the deal's own underwriting is the baseline.

## Contents

1. [GP behavior](#gp-behavior) — `GEN-01`–`GEN-05`
2. [Structural](#structural) — `EQUITY-01`–`EQUITY-05`, `PREF-01`, `GEN-06`
3. [Financial](#financial) — `GEN-07`–`GEN-13`, `EQUITY-06`–`EQUITY-07`
4. [Disclosure](#disclosure) — `GEN-14`–`GEN-17`
5. [Market-cycle](#market-cycle) — `GEN-18`–`GEN-19`
6. [Hard money / private credit](#hard-money--private-credit) — `HML-01`–`HML-05`, `CREDIT-01`–`CREDIT-02`

Severity counts: 14 RED, 12 YELLOW, 8 YELLOW–RED across 34 flags.

---

## GP behavior

Flags on the sponsor's alignment, conduct, and the honesty of how the track
record is presented. These apply to every deal type — a GP-behavior flag on a
debt fund matters as much as on an equity syndication.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| GEN-01 | Zero GP co-investment | RED | GP has no capital at risk; it earns fees and promote regardless of LP outcome — alignment is asserted, not structural. | "How much of your own capital is in this deal, on the same terms as LPs?" |
| GEN-02 | Prior regulatory action or investor litigation | RED | A history of SEC / FINRA / state action or LP lawsuits signals a pattern of investor harm or compliance failure. | "Have you or your principals faced any regulatory action, enforcement, or investor litigation?" |
| GEN-03 | Marketing-heavy, substance-light materials | YELLOW | Glossy projections, testimonials, and "limited spots" urgency stand in for underwriting detail and actuals. | "Can you provide the full underwriting model and the historical actuals behind these projections?" |
| GEN-04 | Rapid AUM growth without team scale-up | YELLOW | Capital raised faster than the team can underwrite and monitor dilutes diligence on each successive deal. | "How have your headcount and deal-monitoring capacity grown alongside AUM?" |
| GEN-05 | GP-IRR vs LP-IRR divergence | RED | Track record cites project-level or GP-level IRR rather than net-to-LP IRR; promote and fees mean the LP's realized return is materially lower than the headline. | "Can you restate your track record as net-to-LP IRR on realized deals only?" |

**Notes.** *GEN-05* is the most common way a mediocre record is made to look
strong: project-level IRR ignores the fee stack and the waterfall entirely, and
GP-level IRR can be flattered by the timing of the GP's own capital. Always
force the number back to net-to-LP on **realized** deals — which connects to
*GEN-14* (unrealized track record). A GP that can produce neither net-to-LP nor
realized figures has no validated record at all.

---

## Structural

Flags in the deal's legal and economic structure — the waterfall, the promote,
the preferred return, and related-party fee arrangements. Most are
equity/preferred-specific; affiliate fee stacking (`GEN-06`) is cross-asset.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| EQUITY-01 | Deal-by-deal (American) waterfall with high promote | RED | GP earns promote as each asset exits, before whole-of-fund LP capital is returned; if early deals win and late deals lose, the LP underperforms the pref while the GP is already paid. | "Is the waterfall deal-by-deal or whole-of-fund, and what protects LPs if later assets underperform?" |
| EQUITY-02 | No clawback in a deal-by-deal waterfall | RED | Without clawback the GP keeps promote on early winners even if later losses wipe out LP capital. | "Is there a clawback provision, and how is it secured or escrowed?" |
| EQUITY-03 | GP catch-up at 100% | YELLOW | After the pref, the GP takes 100% of cash flow until caught up, accelerating GP economics ahead of further LP distributions. | "What is the catch-up rate, and why 100% rather than a shared 50/50 catch-up?" |
| EQUITY-04 | Low or absent preferred return (pref <6% or none) | YELLOW–RED | The LP bears equity risk without a priority-return cushion before the GP earns promote. | "What preferred return do LPs receive before the GP earns any promote?" |
| EQUITY-05 | Non-cumulative or simple-only pref where cumulative is standard | YELLOW | Non-cumulative pref means unpaid pref in a weak year is lost, not carried forward — the LP loses time-value protection. | "Is the preferred return cumulative, and does unpaid pref carry forward and compound?" |
| PREF-01 | Promote / catch-up sitting above a preferred-equity pref | YELLOW | A promote above the pref means the position carries equity risk dressed as preferred — the capped-upside pref profile no longer holds. | "If there's a promote above the pref, how is this still a preferred position rather than common equity?" |
| GEN-06 | Affiliate fee stacking | YELLOW–RED | Property management, construction management, and loan placement all flow to GP-affiliated entities, often undisclosed and not arm's-length — the GP earns layered fees regardless of LP return. | "Which service providers are GP-affiliated, what do they charge, and are those rates third-party-benchmarked?" |

**Notes.** *EQUITY-01* and *EQUITY-02* travel together: the deal-by-deal
structure is standard in retail real estate (see `02-fee-stack-library.md` →
Waterfall mechanics), so it isn't a RED on its own — it's RED *when paired with
a high promote and no clawback*, because that combination lets the GP bank
promote on winners with nothing to give back if the portfolio turns. *GEN-06*
is the structural cousin of the fee inventory in `02`: the individual fees can
each be in-range while the *aggregation through related parties* is the
problem. The test is disclosure and benchmarking, not the existence of an
affiliate.

---

## Financial

Flags in the return math and the debt — where the return comes from, how
sensitive it is, and whether the financing can survive the hold. This is where
the skill's sharpest distinction lives: separating an asset story from a
financing story.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| GEN-07 | "Financing story" disguised as an asset story | RED | LP returns are driven primarily by leverage and cap-rate compression rather than operational value creation; the return collapses if rates rise or credit tightens. | "Strip out leverage and cap-rate compression — what is the unlevered, in-place return?" |
| GEN-08 | Exit-dependent IRR (>60% of return from terminal value) | RED | More than 60% of projected LP IRR comes from the exit cap / terminal-value assumption rather than realized cash flow — the return is a future-sale bet, not income. | "What share of projected LP IRR comes from the exit vs in-place cash flow, and what's the IRR at a flat exit cap?" |
| EQUITY-06 | Aggressive exit cap (exit cap below going-in cap) | RED | Assuming the market pays a lower cap (higher price) at exit bakes unproven cap compression into the headline IRR. | "Why is the exit cap below the acquisition cap, and what's the IRR at an exit cap equal to or above going-in?" |
| EQUITY-07 | Refi-dependent business plan | YELLOW–RED | The plan needs a refinance — often at lower rates — to return capital or hit the return; the refi market can freeze (it did in 2022–24). | "Does the plan depend on a refinance, and what happens to distributions if the refi isn't available on the assumed terms?" |
| GEN-09 | Debt maturity inside the business-plan horizon | RED | The loan comes due before the planned exit, forcing a refinance or sale into whatever market exists at maturity. | "When does the debt mature relative to the projected hold, and what is the refinance or extension plan?" |
| GEN-10 | Rate cap expiry risk | RED | Floating-rate debt whose interest-rate cap expires before hold-end or refi; the 2022–24 pattern is cap expires → rates stay elevated → refi frozen → debt service spikes and erases distributions. | "When does the rate cap expire relative to debt maturity, and what's the cost to extend it at current pricing?" |
| GEN-11 | Cash-flow timing / J-curve not disclosed | YELLOW | An IRR with no distribution schedule hides whether capital returns early or is back-loaded to exit; identical IRRs can carry very different risk timing. | "What is the projected distribution schedule, and at what milestones does LP capital start returning?" |
| GEN-12 | Trailing-3 / trailing-6 financials only, no T-12 | YELLOW–RED | Short trailing windows can cherry-pick a strong stretch and hide seasonality or a declining trend. | "Can you provide trailing-twelve-month actuals, not just T-3 or T-6?" |
| GEN-13 | Projections with no sensitivity or downside case | YELLOW | A single-point pro forma conceals how fragile the return is to its key swing assumptions. | "What is the return under a bear case — flat rents, higher exit cap, no refinance?" |

**Notes.** *GEN-07*, *GEN-08*, and *EQUITY-06* are one family viewed from three
angles: a financing story (GEN-07) usually *shows up* as exit-dependent IRR
(GEN-08) resting on an aggressive exit cap (EQUITY-06). When two or three fire
together, the verdict should name the deal a financing story explicitly. *GEN-10*
(rate cap expiry) is the specific, recent failure mode behind many 2022–24
multifamily-syndication capital calls and wipeouts — it is distinct from generic
floating-rate exposure because the cap's *expiry date*, not the rate itself, is
the trigger. *GEN-11* is why two deals with identical headline IRR are not
equivalent: the back-loaded one concentrates all return risk at the exit.

---

## Disclosure

Flags that fire on absence. A deal omitting what its asset class normally
discloses (per `01-asset-class-norms.md`) is scored here, not silently passed.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| GEN-14 | Unrealized-only track record (no realized exits cited) | RED | Marked-to-market or unrealized returns are self-reported and unproven; the GP has not demonstrated it can exit and return capital. | "What are your fully-realized, exited deals, and the actual net-to-LP returns on those?" |
| GEN-15 | Missing financials | YELLOW–RED | Rent roll, T-12, or full debt terms absent means the deal can't be underwritten — the absence is a choice. | "Can you provide the rent roll, trailing-twelve actuals, and complete debt terms?" |
| GEN-16 | No fee or waterfall disclosure | YELLOW–RED | Undisclosed fees are still paid; without the full stack and waterfall, gross-to-net drag is unknowable (see `02-fee-stack-library.md`). | "Can you provide the complete fee schedule and the full distribution waterfall?" |
| GEN-17 | Essential category-specific disclosure absent | YELLOW | A deal omitting a disclosure its asset class normally carries (e.g. office with no physical-occupancy or class disclosure) is unscreenable on that axis. | "[Per `01` baseline] e.g. for office: 'What is the physical — not leased — occupancy, and the building class?'" |

**Notes.** *GEN-14* is the disclosure-side twin of *GEN-05*: a GP that cites
only unrealized marks **and** only project-level IRR has given you no validated
information about LP outcomes at all — that pairing is a RED cluster, not two
separate YELLOWs. *GEN-17* is deliberately a pointer into `01-asset-class-norms.md`
rather than a fixed list — the "essential disclosures" per asset class live
there, and this flag is how an absence against that baseline gets scored.

---

## Market-cycle

Flags tied to where the cycle is, and to the post-2020 structural resets that
`01-asset-class-norms.md` marks *variable*.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| GEN-18 | Rent / NOI growth assumption in a slowing or oversupplied submarket | YELLOW | The pro forma assumes growth the submarket may not deliver; a supply pipeline can flip rent growth negative regardless of the metro trend. | "What submarket supply pipeline and absorption data support the rent-growth assumption?" |
| GEN-19 | Post-2020 office with no occupancy-reset acknowledgement | RED | Underwriting that ignores the structural WFH / physical-occupancy reset is using a pre-2020 baseline that no longer holds (see `01` → Office, *variable*). | "How does the underwriting reflect post-2020 physical occupancy and sublease overhang in this submarket?" |

**Notes.** Market-cycle flags are the ones most likely to be *variable* in
`01-asset-class-norms.md` — office, experiential retail, STR. The flag isn't
"this asset class is bad"; it's "the deal used a category baseline where the
honest answer is the deal's own underwriting." Pair these with *GEN-13* (no
downside case): a cycle-exposed asset with a single-point pro forma is a
sharper flag than either alone.

---

## Hard money / private credit

Debt-fund-specific flags. Without this category the skill misclassifies risk on
debt deals — the equity flags above (waterfall, exit cap) largely don't apply,
and the real risks are LTV basis, concentration, and hidden loss history.

| ID | Flag | Severity | Mechanism — why it's a flag | Response — what to ask |
|---|---|---|---|---|
| HML-01 | LTV quoted on ARV without as-is value | RED | A 70% LTV on after-repair value can be 100%+ of current value — there is no real equity cushion if the renovation thesis fails. | "What is the average portfolio LTV on as-is value, not just ARV?" |
| HML-02 | Geographic concentration | YELLOW | A loan book concentrated in one metro is exposed to a single local downturn with no diversification offset. | "What is the geographic distribution of the loan book?" |
| HML-03 | Default rate not disclosed | YELLOW–RED | A hidden default history obscures the fund's actual credit performance through cycles. | "What is your historical default rate, including through 2020 and 2022–23?" |
| HML-04 | Recovery rate not disclosed | YELLOW–RED | Default rate alone is meaningless without recovery — workout competence determines the LP's realized loss. | "On defaulted loans, what is your realized recovery rate and average workout timeline?" |
| HML-05 | No management-fee step-down in a long-dated fund | YELLOW | A full management fee on committed capital after the investment period drags LP net as the book winds down (see `02-fee-stack-library.md`). | "Does the management fee step down after the investment period?" |
| CREDIT-01 | Fund-level leverage stacked on loan leverage | RED | BDC-style fund leverage amplifies losses on an already-levered loan book; the quoted LP IRR may be a levered figure presented as if unlevered. | "What is the fund's leverage ratio, and is the quoted LP IRR levered or unlevered?" |
| CREDIT-02 | Sector concentration in the loan book | YELLOW | Loans concentrated in one sector carry correlated default risk that diversification is supposed to dampen. | "What is the sector breakdown of the portfolio, and your single-largest-sector exposure?" |

**Notes.** *HML-01* is the single most important debt-fund flag: the ARV-vs-as-is
distinction (see `01-asset-class-norms.md` → Hard Money) is where a fund that
looks conservatively levered is actually lending at or above current value.
*HML-03* and *HML-04* are a pair — a fund will sometimes disclose a low default
rate while staying silent on recovery, but a 2% default rate with 40% recovery
is worse than a 5% default rate with 90% recovery. *CREDIT-01* connects to the
financing-story family (*GEN-07*): fund-level leverage is how a modest loan-book
yield is levered into a marketable LP IRR, and it unwinds the same way.

---

## Provenance

The shared sources in `01-asset-class-norms.md` → Provenance (ILPA
LP-protection standards; Preqin / NCREIF realized-vs-marketed dispersion, the
basis for treating unrealized marks and project-level IRRs skeptically), plus:

- **SEC enforcement patterns.** The recurring fact patterns in real-estate and
  private-fund enforcement actions (undisclosed affiliate fees, unrealized
  marks presented as returns, misleading track-record IRRs).
- **Post-2022 distress case studies.** The rate-cap-expiry / frozen-refi
  failures in 2022–24 retail-LP multifamily syndications — the source for
  `GEN-10`, `GEN-09`, and `EQUITY-07` as a connected failure mode.

*Last reviewed: 2026-06-01. Re-baseline when a new failure mode emerges at scale
(the rate-cap-expiry cluster is the canonical recent example) or when a flag's
threshold drifts from current `01`/`02` norms. New flags append to the relevant
category and take the next ID in their prefix sequence so existing
`04-question-bank.md` cross-references stay stable.*
