# Data-integrity tools — verify_data.py and lint_report.py

Use this when: you are running a real analysis and want the two mechanical gates that guard the skill's single most important discipline — that every number is sourced, current and internally consistent. Blinded adversarial review of this skill's own reports found the dominant failure was never analytical reasoning; it was data integrity. Figures that could not be traced to a source, a peer's ratio quoted wrong, and a quarter that was already public but absent from the report. These two scripts turn the sourcing rules from advice you might follow into checks you run.

Neither tool judges the analysis. They judge whether the *inputs* and the *finished artefact* meet the non-negotiables, so that a reviewer — or the challenge pass in `references/20-challenge-pass.md` — is not the first thing standing between a sloppy figure and the verdict.

## verify_data.py — the intake gate (Stage 1)

Run this after you have gathered data and before you compute anything on it.

**Workflow.** As you collect figures, record each one as a datapoint with its provenance rather than pasting bare numbers into a working file. Then run the gate:

```
python scripts/verify_data.py --template          # prints the intake schema to fill
python scripts/verify_data.py my-intake.json      # runs the checks
python scripts/verify_data.py my-intake.json --json
```

Each datapoint carries: `metric`, `value`, `period`, `basis` (consolidated/standalone), `unit`, `source`, and optionally an `alt` list of the same figure from a second source. The file header carries `as_of`, the reporting basis, currency/units, and `latest_reported_period` with its publication date.

**What it catches, and why each matters:**

| Check | Catches | Why it is here |
|---|---|---|
| Provenance missing | A figure with no source or period | A number you cannot cite is a number you cannot defend; it is the raw material of a hallucinated report |
| Cross-source divergence | The same figure differing between two sources beyond tolerance (>2% warn, >10% error) | This is the exact defect that put a wrong peer NPA into a real report. When sources disagree, the answer is to find out which is right, never to average |
| Basis mixing | Consolidated and standalone figures used together without labels | Silently mixing the two invalidates every ratio built from them |
| Unit / currency mixing | A crore figure sitting beside a million figure for the same metric | The 10x error is common, silent and embarrassing |
| Period misalignment | FY vs CY vs TTM, or non-aligned fiscal years, among figures meant to be compared | A peer comparison across mismatched periods is not a comparison |
| Staleness | The newest figure you gathered is older than a period the company has already published | The single most common way a careful analysis is simply out of date |
| Source tier | A headline metric (revenue, PAT, EBITDA, debt, equity, operating cash flow) sourced only from a Tier-4 aggregator (screener/tickertape/yahoo...) is an **error**; other aggregator-only figures warn; a headline figure whose source cannot be confirmed as a filing warns. Tag each datapoint's `source_tier` (1 filing, 2 company secondary, 3 regulator/rating, 4 aggregator) or let it be inferred from the source text | This is the exact hole a report falls through when it *looks* sourced — a period label beside every figure — yet the numbers came off an aggregator screen. Current price/market cap is the one exempt exception. Also reports the share of figures that are primary-sourced |

Fix every **error**-level finding before proceeding. Treat **warnings** as things to resolve or to state explicitly in the report's data-quality note. Metrics you have honestly marked unavailable are reported as coverage context, not defects — disclosing a gap is the correct behaviour, not a failure.

The verified intake also feeds cleanly into `scripts/ratios.py`, so the same structured data does double duty.

## lint_report.py — the delivery gate (Stage 10)

Run this on the finished markdown report, just before you deliver it.

```
python scripts/lint_report.py report.md
python scripts/lint_report.py report.md --json
python scripts/lint_report.py report.md --strict     # promotes warnings to errors
```

**What it checks:**

- **Structure and non-negotiables** — recency statement, data-quality note, reporting basis, currency and units, a verdict near the top, a risks/bear-case section, a not-financial-advice disclaimer, and — if a scorecard is shown — that its gate disclosure is present. A composite with no statement of which gates were checked is flagged, because an unchecked gate and a cleared gate look identical otherwise.
- **Figure sourcing (the core check)** — it scans every percentage, currency amount and multiple in the report and measures the share that sit near a provenance cue (a period label, a filing reference, a page number, "as of", a URL). It reports that ratio and lists a sample of the bare figures by line. This is a **heuristic that prompts review, not proof of fabrication** — but it is discriminating: on this skill's own test reports it separated well-sourced analyses from thin ones cleanly, and a ratio below roughly 60% reliably means "go back and cite", not "ship".
- **Aggregator-only sourcing** — the complement to the tier check on the intake side: it flags figures whose only nearby cue is an aggregator (screener/tickertape/yahoo...) with no filing/report/transcript cue in the same line. Such a figure passes the ratio check above (an aggregator name *is* a cue) yet traces to no document — so it warns you to replace it with the filing or mark it as a labelled cross-check beside the document figure. Price/market cap is exempt.
- **Hygiene** — leftover `TODO`/`TBD`/template angle-bracket fields, empty table cells where a figure is implied, and imperative personalised instructions ("buy N shares", "allocate N%") that would breach the analysis-not-advice boundary.

A low figure-sourcing ratio is an instruction to add citations, not a number to accept. The linter is a floor beneath the report, never a ceiling on judgement — passing it does not make an analysis good, but failing it means the analysis is not yet ready to be seen.

## How they relate to the rest of the skill

- The **recency gate** in `SKILL.md` Stage 1 is the reasoning; `verify_data.py`'s staleness check is its mechanical enforcement.
- The **anti-hallucination non-negotiables** in `SKILL.md` are the rules; `lint_report.py` is the automated check that the finished report actually kept them.
- The **challenge pass** (`references/20-challenge-pass.md`) verifies figures adversarially and by hand. The linter is the cheap first pass that clears the obvious defects so the challenge pass can spend its effort on the ones that require judgement.

## Checklist

- [ ] Gathered data recorded as datapoints with provenance, not bare numbers.
- [ ] `verify_data.py` run at Stage 1; every error-level finding resolved; warnings resolved or disclosed.
- [ ] Cross-source disagreements settled by finding the correct figure, not by averaging.
- [ ] `lint_report.py` run at Stage 10; error-level findings fixed.
- [ ] Figure-sourcing ratio checked; bare figures cited before delivery.
- [ ] No template placeholders, no advice-boundary breaches left in the report.
