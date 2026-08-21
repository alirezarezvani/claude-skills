# Forensic mode — runbook

Use this when: the question is **"can I trust these accounts?"** rather than "is this a good investment?". Triggered by requests like "check if this company is cooking the books", "is the profit real", "run a forensic check", "the cash flow doesn't match the profit", "should I be worried about this company's accounting", or when a Standard/Deep-dive run hits a Stage 3 red flag serious enough that valuation becomes pointless until it is resolved.

Forensic mode is not a shorter version of the full analysis — it has a different question, a different output and a different verdict scale. You are not producing an investment view. You are producing an opinion on **whether the reported numbers can bear weight**, and if not, which specific numbers are load-bearing and unverified.

Two disciplines govern everything below, both inherited from `references/07-forensic-red-flags.md` §16:

- **Never assert fraud.** Describe what the disclosure shows, what it does not let you rule out, and what evidence would resolve it. You are analysing a real company whose reputation is a real thing; an unsupported accusation is both a professional failure and a potential harm. "The cash is fake" is not a finding. "Reported cash earns an implied yield of ~1% against ~6% short rates, which the filings do not explain" is.
- **A single flag is a question; a cluster is a finding.** Most individual anomalies have mundane explanations. What distinguishes a real accounting problem is several independent flags converging on the *same line item*.

## Contents

- [When NOT to run this mode](#when-not-to-run-this-mode)
- [Stage F0 — Scope and applicability gate](#stage-f0--scope-and-applicability-gate)
- [Stage F1 — The one-hour triage](#stage-f1--the-one-hour-triage)
- [Stage F2 — Follow the money to the line item](#stage-f2--follow-the-money-to-the-line-item)
- [Stage F3 — Documents and people](#stage-f3--documents-and-people)
- [Stage F4 — Independent verification](#stage-f4--independent-verification)
- [Stage F5 — Quantify the dependency](#stage-f5--quantify-the-dependency)
- [The verdict scale](#the-verdict-scale)
- [Output template](#output-template)
- [Checklist](#checklist)

## When NOT to run this mode

Say so plainly rather than producing a weak forensic report:

- **You cannot obtain the primary filings.** Forensic work on aggregator summaries is not forensic work. Screener data has no notes to accounts, no auditor's report, no related-party disclosure — the places where the answers live. If you only have aggregated financials, run the Stage F1 arithmetic tests, report verdict **U**, and list exactly which documents are needed.
- **The company is a lender or insurer and you are reaching for the generic battery.** Accrual ratios, DSO and cash conversion are undefined or inverted for banks, NBFCs and insurers. Go to the sector translation section below.
- **The user wants a general analysis.** Forensic mode deliberately skips business quality, growth and valuation. If they wanted an investment view, run Standard mode with a forensic pass inside it.

## Stage F0 — Scope and applicability gate

1. **Identity and basis.** Which entity, which listing, and — critically — **consolidated or standalone**. Most tunnelling and most hidden leverage live in subsidiaries; a standalone-only forensic pass will miss them by construction. If only standalone is available, say so and treat it as a material limitation.
2. **Sector translation.** Confirm the generic battery applies. See the table below.
3. **Document inventory.** List what you actually have: annual report (which years), auditor's report, notes to accounts, cash flow statements, shareholding pattern, concall transcripts, rating rationales. **Write this list into the output.** A forensic verdict is only as strong as its document base, and the reader must be able to see that base.

### Sector translation

| Sector | Generic tests that are undefined or inverted | What replaces them |
|---|---|---|
| Banks, NBFCs | Cash conversion, DSO, accrual ratio, working capital — all meaningless. CFO is dominated by deposit and loan flows | Provisioning adequacy vs slippages, PCR trend vs flat GNPA (reserve release), restructured/written-off pool, RBI divergence disclosure (India), evergreening indicators, Stage-2 migration, related-party lending |
| Insurers | Revenue timing, receivables | Reserve adequacy and prior-year development, actuarial assumption changes, persistency vs reported VNB |
| REITs, InvITs | Earnings-based accrual tests | Fair-value gains vs realised NOI, capitalised leasing costs, AFFO adjustments, related-party asset purchases from the sponsor |
| Miners, oil & gas | Depreciation adequacy | Reserve restatements, capitalised exploration/stripping costs, rehabilitation provision adequacy |
| EPC, infrastructure | Standard revenue tests | Percentage-of-completion assumptions, unbilled revenue growth, claims and arbitration recognised as receivables, retention money ageing |

## Stage F1 — The one-hour triage

These six tests are cheap, quantitative, and catch the large majority of distortion cases. Run all six before going deeper. Run `python scripts/ratios.py <input.json>` — it computes most of them and raises the warnings automatically.

| # | Test | Compute | What it means |
|---|---|---|---|
| 1 | **Cash conversion** | Cumulative CFO ÷ cumulative PAT over 5 years | The headline test. Below ~0.8 sustained means profit is not becoming cash. **This is a scoring gate: below 0.5 over 3+ years caps the composite at 4.0** |
| 2 | **Proof of cash** | Investment income ÷ average cash & liquid investments, vs short rates for that currency | An implied yield far below the risk-free rate means the cash is absent, pledged, restricted, or non-interest-bearing. India: include Ind-AS fair-value gains on liquid funds or you manufacture a false flag |
| 3 | **Receivables vs sales** | DSO trend over 5 years; receivables CAGR − revenue CAGR | Revenue that has not been collected is a hypothesis. **Gate: sustained divergence 2+ years caps at 6.0** |
| 4 | **Capex vs depreciation** | Capex ÷ D&A; implied asset life; CWIP ageing | Persistent capex far above depreciation with flat revenue is where deferred costs hide |
| 5 | **Audit opinion** | Opinion type, Key Audit Matters, Emphasis of Matter, IFC/SOX opinion, auditor changes and stated reasons | **Gates: adverse/disclaimer = veto. Qualified = cap 4.0. Resignation without clean reason = cap 4.5** |
| 6 | **Related party and pledge** | RPT as % of revenue; loans/advances to related parties; promoter pledge level and trend (India) | The primary tunnelling route. **Gates: unexplained RPT/diversion = cap 4.5; pledge >50% = cap 4.0** |

**Before flagging test 1 or 3, rule out the innocent explanation.** A genuinely growing, working-capital-intensive business (distribution, EPC, capital goods) consumes cash while growing — that is arithmetic, not fraud. Compute **working capital as a % of sales**. Stable ratio with a growing absolute number = growth. Rising ratio = the growth is being bought. Write this test into the output whichever way it resolves.

## Stage F2 — Follow the money to the line item

If triage raises anything, stop generalising and answer one question: **if profit did not become cash, which asset did it become?**

Build the five-year bridge — PAT, CFO, capex, FCF, ΔWorking capital, D&A, non-cash items — and attribute the gap to a named balance-sheet line. Each destination routes to a different investigation in `07-forensic-red-flags.md`:

| Where the profit went | Investigate | Section |
|---|---|---|
| Receivables / unbilled revenue | Revenue recognition, ageing, ECL adequacy, channel stuffing, vendor financing | §3, §4 |
| Inventory | Obsolescence, provisioning, cost absorption into inventory | §4 |
| CWIP / intangibles / capitalised development | Cost capitalisation, useful lives, impairment timing | §5 |
| Loans & advances to related parties | Tunnelling, promoter-group diversion | §9, §10 |
| Goodwill from acquisitions | Purchase accounting, acquisition reserves, serial-acquirer distortion | §6 |
| "Other current assets" | Read the note. This is where unclassifiable claims are parked | §4 |

Then test the **cluster rule**: are several independent flags pointing at the *same* line item? Rising DSO alone is a question. Rising DSO + shrinking ECL allowance + revenue concentrated in Q4 + a related-party customer is a finding.

## Stage F3 — Documents and people

- **Auditor's report in full** — opinion, basis, KAMs/CAMs, Emphasis of Matter, internal-financial-controls opinion. India: the **CARO annexure** forces explicit comment on fund diversion, related-party loans, and end-use of borrowings. Read every clause.
- **Component-auditor coverage** — what % of consolidated revenue, assets and profit is *not* audited by the principal auditor. A high unaudited share in a complex group is a structural concern in itself.
- **Year-over-year redline** — diff this year's disclosure against last year's and hunt specifically for **deletions**. Management highlights additions and never mentions removals.
- **People signals** — map CFO, controller, treasurer, internal-audit head and audit-committee-chair turnover over 5+ years. Serial finance-team churn is among the more reliable pre-restatement tells. Read resignation letters where available.
- **Enforcement and litigation history** — SEBI/SFIO/NFRA (India), SEC comment letters and enforcement (US), restatements, exchange actions. Read short-seller reports as *primary documents to be evaluated*: attribute their claims, verify independently, do not adopt.

## Stage F4 — Independent verification

The decisive point, and the reason a filings-only forensic pass has a ceiling:

> Every major accounting fraud reconciled internally. The balance sheet balanced, the ratios computed, and a competent desk analyst could complete a full checklist without the numbers contradicting each other. Fabricated financials are internally consistent by construction.

So where the fraud hypothesis is live, attack the specific load-bearing claim with **non-company evidence**: registry and insolvency filings (MCA/ROC, Companies House, EDGAR), customs and shipping records, satellite or street-level imagery for claimed physical assets, employment and hiring data, app/web traffic panels, customer and ex-employee contact, and the charge registry for pledged assets.

State plainly what you attempted, what you obtained, and what you could not verify. **"Not verified" must never be presented as "verified clean."**

## Stage F5 — Quantify the dependency

A forensic pass that ends in a list of flags is unfinished. The useful output is a sentence of this shape:

> *Roughly X% of reported EBITDA over the last three years depends on capitalisation and one-off treatments the peer group does not use; on a peer-consistent basis EBITDA would be approximately Y.*

Derive it from disclosed line items and show the working, or state explicitly that it cannot be derived. Never invent it. Then carry the adjusted figures — not the reported ones — into `references/05-returns-and-dupont.md` and `references/06-valuation.md` if the analysis continues.

## Challenge the verdict before assigning it

Run `references/20-challenge-pass.md` before you settle on a letter. A forensic verdict is unusually costly to get wrong in **both** directions — a false clean bill misleads someone about to commit money, and a false concern damages a real company — so the adversarial pass is mandatory here rather than recommended.

Attack in both directions, and say which way you tested:

- **Against a clean verdict:** what did you not look at? Which document would most likely change the answer? Is "no flags found" actually "no flags searched for"?
- **Against a concerning verdict:** is the innocent explanation stronger than you allowed? Is this a single flag dressed as a cluster? Would a sector specialist call this normal for the industry?

## The verdict scale

Assign exactly one. The scale maps to the three severities in `07-forensic-red-flags.md` §16, plus an explicit "insufficient evidence" band that must never be collapsed into "clean".

| Verdict | Meaning | What it implies |
|---|---|---|
| **A — No material concerns identified** | The triage battery ran on primary documents and surfaced nothing beyond normal accounting variation | Reported figures can bear weight. State which tests were run |
| **B — Aggressive but disclosed** | Permissive but legal and visible choices: generous capitalisation, flattering non-GAAP add-backs, a disclosed tax holiday | Adjust the numbers yourself, show the adjustment, proceed |
| **C — Unexplained anomalies** | A cluster of flags converging on a line item that disclosure does not account for | Raise the required margin of safety materially. State the specific evidence that would resolve it. Not an accusation |
| **D — Structural integrity risk** | Adverse/disclaimer/qualified opinion, auditor resignation, cash-existence KAM, large unaudited group share, Big-R restatement, regulator enforcement, related-party tunnelling | Belongs in the opening line of the report. Sufficient on its own to stop the analysis. Do not rely on reported figures |
| **U — Insufficient evidence** | Primary documents unobtainable; the tests that matter could not be run | **Explicitly not a clean bill.** List the documents required. An unchecked test and a passed test look identical unless you say which is which |

Report the verdict with its evidence base, never as a bare grade.

## Output template

```markdown
# Forensic review — <Company> (<TICKER>)
**Verdict: <A/B/C/D/U> — <label>**
As of <date> · Basis: <consolidated/standalone> · Currency/units: <INR crore / USD mn>

## Document base
Documents obtained: <list with years>
Documents NOT obtained: <list> — and what each would have tested.

## Summary
<3-5 sentences. Lead with the verdict and the single most load-bearing unresolved item.>

## Triage results
| # | Test | Result | Reading |
|---|---|---|---|
| 1 | Cash conversion (5y cumulative CFO/PAT) | | |
| 2 | Implied yield on cash vs short rates | | |
| 3 | DSO trend / receivables vs sales growth | | |
| 4 | Capex vs depreciation | | |
| 5 | Audit opinion, KAMs, auditor changes | | |
| 6 | Related-party exposure and pledge | | |

## Findings
For each finding:
- **What the disclosure shows** — the figures, sourced and dated.
- **Severity** — aggressive-and-disclosed / unexplained anomaly / structural integrity risk.
- **The innocent explanation** — the most plausible benign reading, stated fairly.
- **What would resolve it** — the specific document, disclosure or external evidence.
- **Cluster?** — which other flags point at the same line item.

## Quantified dependency
<X% of reported EBITDA/PAT depends on <treatment>; peer-consistent figure ≈ Y. Or: cannot be derived, because ...>

## Gates raised
<From scripts/score.py — list each gate, its severity, and whether it was CHECKED-AND-CLEARED or NOT CHECKED.>

## What was not verified
<Explicit list. This section is mandatory and must never be empty unless every test was genuinely run on primary documents.>

---
*This is analysis of publicly disclosed information, not an allegation of wrongdoing and not licensed financial advice. Findings describe what disclosure does and does not explain; they are not conclusions of fraud.*
```

## Checklist

- [ ] Consolidated basis confirmed, or standalone-only flagged as a material limitation.
- [ ] Sector translation applied — generic battery not run on a lender, insurer or REIT.
- [ ] Document base listed in the output, including what was **not** obtained.
- [ ] All six triage tests run, or their absence stated.
- [ ] Working capital as % of sales checked before any cash-vs-profit flag in a growing business.
- [ ] India: Ind-AS fair-value gains on liquid funds included in the cash-yield test.
- [ ] Cash gap attributed to a **named** balance-sheet line item.
- [ ] Cluster rule applied — no finding asserted on a single isolated flag.
- [ ] Every flag paired with its innocent explanation and its resolving evidence.
- [ ] Auditor's report, KAMs, IFC opinion and (India) CARO clauses read in full.
- [ ] CFO / audit-committee turnover mapped over 5+ years.
- [ ] At least one independent non-company corroboration attempted for the load-bearing claim.
- [ ] Dependency quantified and shown, or explicitly stated as underivable.
- [ ] Verdict assigned on the A–D/U scale, with U used wherever documents were missing.
- [ ] No assertion of fraud anywhere in the output; short-seller claims attributed, not adopted.
- [ ] "What was not verified" section present and populated.
