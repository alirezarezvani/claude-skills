# Worked examples — gold-standard reference analyses

These are **illustrative exemplars**: complete analyses the skill is meant to
produce, written so a new run can see the target quality rather than infer it
from the template alone. Read them alongside `references/12-report-template.md`
(structure) — the template shows the *shape*, these show the *bar*.

**Every company here is fictional and every figure is invented.** That is
deliberate: it lets the numbers be internally consistent and freely shown
without any risk of presenting fabricated data about a real company as if it
were sourced. In a real analysis the same citations (`[FY26 AR, p.112]`) must
point at real documents, and the non-negotiables — never invent a number,
document-first sourcing, the recency gate — apply in full. **Do not lift any
figure from these files into a real analysis.**

| File | Mode | What it demonstrates |
|---|---|---|
| `standard-analysis-example.md` | Standard | The full workflow on a (fictional) FMCG franchise: sector playbook and suppressed metrics, DuPont, working-capital and cash-conversion analysis, a document-sourced data-quality note with source tiers, a sector-relative scorecard with the gate disclosure, `valuation.py` output (EV bridge, trailing multiples, reverse-DCF implied growth, scenario table), a genuine bear case, and observable invalidation triggers. Passes `scripts/lint_report.py`. |
| `forensic-analysis-example.md` | Forensic | A forensic read of the `evals/fixtures/synthetic-ar-excerpt.md` extracts (fictional Kesar Agro): the F0–F5 runbook, the accruals and proof-of-cash tests, the CARO and related-party evidence, and a "can these accounts bear weight?" verdict that stops short of valuation on purpose. |

Both were checked with the bundled gates: the standard example passes
`python scripts/lint_report.py`, and its valuation section is the verbatim output
of `python scripts/valuation.py` on the same inputs.
