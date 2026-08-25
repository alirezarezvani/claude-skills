---
description: Transcript-level interview mapping. Route intake to one of 16 lenses, code the transcript with verbatim quote verification, run a reliability council on unstable analytic cells, and (for >=2 interviews) synthesize triangulated cross-interview insights. Every conclusion carries a verified quote + line number; disagreement is flagged for a human, never auto-resolved. Direct invocation of the interview-mapper skill.
argument-hint: "<transcript path or task: goal, respondent type, number of interviews>"
---

# /cs:interview-mapper — Transcript coding + reliability council + insight synthesis

Run the `interview-mapper` skill on this input:

**$ARGUMENTS**

## Workflow

1. **`route.py`** — Maps (goal × respondent) to one of 16 lenses (org-mapping, JTBD, CustDev,
   expert, usability, exit, win/loss, candidate, intercept, conflict-mediation, ethnographic,
   change-readiness, focus-group, team-retro, visitor-experience, brand-positioning) and returns
   the applicable pipeline steps.

2. **`number_lines.py` → coding → `extract_claims.py` → `verify_quotes.py` → `check_support.py`** —
   Numbers the transcript for traceability, codes Layer 1 (facts) and Layer 2 (analysis) from the
   lens template, then checks every quote is verbatim in the source AND that the conclusion is
   actually entailed by it (verbatim ≠ support — these are two separate checks).

3. **`consensus.py`** (for unstable Layer-2 cells) — N isolated re-runs, fresh context each time,
   re-fed the transcript. Agreement → `[consensus]`. Disagreement → `[⚑ disputed]`, routed to
   `make_adjudication.py` for a human to decide blind.

4. **For >=2 interviews: `extract_nuggets.py` → cluster → `score_insights.py --k 3` →
   `build_provenance.py` + `render_board.py`** — Atomizes each mapping into nuggets, clusters by
   theme (counting distinct interviews, not quotes), and only promotes a cluster to `insight` once
   >=k independent interviews carry a verified quote. Below the threshold: `watchlist` or `weak`.

## Output

- Coded mapping with grounding status per cell (`verified/paraphrase/rejected` x
  `supported/unsupported`), plus `[consensus]` or `[⚑ disputed]` marks on Layer 2.
- Change log, omission list, rejected-quotes list (transparency is a feature, not an afterthought).
- For >=2 interviews: insight cards with verified evidence, prevalence, tension, counter-evidence,
  and confidence — or `watchlist`/`weak` if triangulation isn't met.
- A standalone HTML provenance board (`render_board.py`) tracing insight → quote → line → interview.

## Hard rule

**No verbatim quote + line number, checked by script, no cell.** Verbatim does not imply support —
check both. Disagreement between independent runs is flagged for a human, never picked by the
model. A pattern requires >=k distinct interviews with a verified quote; one participant is a
signal to probe, not an insight.

## Distinct from

- `research-ops/skills/product-research` (sibling, via `/cs:product-research`) — that selects the
  research *method*, sizes the sample, and synthesizes *already-coded* observations into a
  repository. It never opens a transcript. This command produces the coded, verified evidence that
  feeds it, or runs standalone on one transcript.
- `product-team/ux-researcher-designer` — that turns synthesized research into personas/journey
  design artifacts. This produces the grounded coding those artifacts should be built from.

## First run

Onboarding-free: run `skills/interview-mapper/scripts/route.py --goal <goal> --respondent <who>` first — it is the deterministic
entry point that decides the lens and pipeline for you. No config file, no defaults to set.
