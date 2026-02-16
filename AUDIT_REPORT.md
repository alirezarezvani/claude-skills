# Skills Audit Report

**Date:** 2026-02-15
**Auditor:** Automated Skill Quality Audit
**Scope:** Recently added skills in business-growth/, finance/, marketing-skill/campaign-analytics/, project-management/

---

## Executive Summary

The recently added skills fall into two distinct tiers:

1. **Business-growth, Finance, and Campaign Analytics skills** — Genuinely impressive. Production-ready Python tooling, deep domain frameworks, real structured outputs. These would make a domain practitioner say "this actually knows what it's doing."

2. **Project Management skills** — A mixed bag. The Atlassian-specific skills (jira-expert, confluence-expert, atlassian-admin, atlassian-templates) have strong knowledge-base content. The scrum-master and senior-pm skills are thin and generic. None of the PM skills have scripts or assets — they're pure prompt-engineering skills, which is a fundamentally different (and weaker) category.

**Overall: 4 POWERFUL, 1 SOLID, 4 SOLID, 2 GENERIC, 1 WEAK**

---

## Detailed Skill Audits

---

### 1. business-growth/customer-success-manager

**Code Quality: EXCELLENT**
- 3 Python scripts (438 + 487 + 414 = 1,339 lines total)
- Well-structured: proper typing, argparse CLI, JSON/text dual output, error handling
- Zero external dependencies (stdlib only) — deliberate, documented design choice
- `health_score_calculator.py`: Multi-dimensional weighted scoring with segment-aware benchmarks (Enterprise/Mid-Market/SMB). Not placeholder math — real configurable thresholds, normalization logic, trend analysis
- `churn_risk_analyzer.py`: Behavioral signal detection with renewal urgency multipliers
- `expansion_opportunity_scorer.py`: Whitespace mapping and effort-vs-impact prioritization
- All scripts actually runnable with provided sample data

**Problem-Solving Quality: EXCELLENT**
- Health scoring framework reference (80+ lines) explains *why* each dimension is weighted as it is — genuinely pedagogical
- Real CS playbooks: not "be proactive" platitudes but specific intervention triggers (e.g., "if health score drops below yellow for 2 consecutive periods, escalate")
- QBR template is production-ready — has ROI summary tables, value-delivered sections, next-quarter planning
- Success plan template, onboarding checklist, executive business review — all structured with fill-in tables
- Uses real industry frameworks: DAU/MAU ratio, NPS scoring methodology, multi-threading depth

**Structure: STRONG**
- SKILL.md has proper frontmatter, TOC, input/output schemas, limitations section
- References are actually used by the scripts (health-scoring-framework.md maps directly to score calculation logic)
- Assets include sample data AND expected output JSON for validation

**Verdict: POWERFUL** ⭐
*Evidence: A CS leader could hand this to a team and they'd have a working health scoring system same day. The weighted scoring model with segment-aware thresholds is exactly how real CS platforms (Gainsight, Totango) work. The scripts produce structured JSON that could feed a dashboard.*

---

### 2. business-growth/revenue-operations

**Code Quality: EXCELLENT**
- 3 scripts (496 + 531 + 658 = 1,685 lines total) — the largest script set
- `pipeline_analyzer.py`: Coverage ratios, stage conversion rates, sales velocity formula (Opportunities × Avg Deal × Win Rate / Cycle), deal aging detection, concentration risk warnings
- `forecast_accuracy_tracker.py`: MAPE calculation, period-over-period accuracy trending
- `gtm_efficiency_calculator.py`: CAC, LTV, CAC payback period, magic number, burn multiple — these are real SaaS metrics, not made up
- Proper CLI args, dual output format, input validation

**Problem-Solving Quality: EXCELLENT**
- RevOps metrics guide references real benchmarks (3-4x pipeline coverage, magic number >0.75)
- Pipeline management framework covers qualification methodology
- GTM efficiency benchmarks are industry-standard (Bessemer, OpenView style)
- Templates: pipeline review, forecast report, GTM dashboard — all structured with metric tables

**Structure: STRONG**
- Consistent with customer-success-manager pattern
- Sample data files for all three scripts
- Expected output JSON for validation

**Verdict: POWERFUL** ⭐
*Evidence: The pipeline analyzer alone replaces basic Salesforce reporting. The GTM efficiency calculator uses the exact metrics VCs and board members ask for (magic number, burn multiple, CAC payback). A RevOps manager would find real utility here.*

---

### 3. business-growth/sales-engineer

**Code Quality: EXCELLENT**
- 3 scripts (557 + 525 + 765 = 1,847 lines total) — largest individual script set
- `rfp_response_analyzer.py`: Weighted coverage scoring (Full/Partial/Planned/Gap × Must-have/Should-have/Nice-to-have), automated bid/no-bid recommendation with configurable thresholds
- `competitive_matrix_builder.py`: Feature-by-feature comparison with differentiator/vulnerability identification
- `poc_planner.py`: Timeline generation, resource planning, success criteria definition, evaluation scorecards
- 765-line POC planner is genuinely comprehensive

**Problem-Solving Quality: EXCELLENT**
- 5-phase workflow (Discovery → Solution Design → Demo → POC → Close) maps to real SE methodology
- RFP analyzer produces structured gap analysis with mitigation strategies — not just "you have gaps"
- Competitive positioning framework includes feature-level comparison, not just "we're better"
- Demo script template and POC scorecard are practitioner-level artifacts
- Technical proposal template has architecture section

**Structure: STRONG**
- Same consistent pattern as other business-growth skills
- Rich asset set: demo script template, POC scorecard, technical proposal template, sample RFP data
- References cover competitive positioning, POC best practices, RFP response methodology

**Verdict: POWERFUL** ⭐
*Evidence: The RFP analyzer with weighted coverage scoring and bid/no-bid recommendation is something SEs actually need and usually do in spreadsheets. The POC planner at 765 lines is the most substantive single script in this batch. A pre-sales team could adopt this immediately.*

---

### 4. finance/financial-analyst

**Code Quality: EXCELLENT**
- 4 scripts (432 + 449 + 406 + 494 = 1,781 lines total)
- `ratio_calculator.py`: 20+ ratios across 5 categories (profitability, liquidity, leverage, efficiency, valuation) — ROE, ROA, DSCR, DSO, EV/EBITDA, PEG ratio
- `dcf_valuation.py`: Full DCF model with WACC via CAPM, 5-year projections, terminal value (perpetuity growth AND exit multiple methods), two-way sensitivity analysis, equity bridge
- `budget_variance_analyzer.py`: Favorable/unfavorable classification by department and category
- `forecast_builder.py`: Driver-based forecasting with scenario modeling (base/bull/bear)
- All stdlib only, handles edge cases (inf values in JSON serialization)

**Problem-Solving Quality: EXCELLENT**
- DCF model implements real finance: CAPM cost of equity, after-tax cost of debt, terminal value via both methods, sensitivity matrix — this is textbook corporate finance done correctly
- Ratio guide includes interpretation context (not just "here's the number" but "here's what it means")
- Valuation methodology reference explains when to use DCF vs. comparables vs. precedent transactions
- Forecasting best practices cover driver-based vs. trend-based approaches
- Variance report template is exactly what FP&A teams produce monthly

**Structure: STRONG**
- Consistent format with other skills
- 4 scripts (most of any skill) — comprehensive coverage of analyst workflow
- Sample data, expected output, 3 templates (DCF, forecast, variance)

**Verdict: POWERFUL** ⭐
*Evidence: The DCF valuation model alone is genuinely useful — it implements WACC calculation, cash flow projection, terminal value via two methods, and sensitivity analysis. A junior analyst could use this as a learning tool; a senior analyst could use it for quick-and-dirty valuations. The sensitivity table output is exactly what you'd see in an investment banking pitch book.*

---

### 5. marketing-skill/campaign-analytics

**Code Quality: VERY GOOD**
- 3 scripts (347 + 459 + 305 = 1,111 lines total) — smallest script set but still substantive
- `attribution_analyzer.py`: 5 attribution models (first-touch, last-touch, linear, time-decay, position-based) — these are the real standard models used in marketing analytics
- `campaign_roi_calculator.py`: ROI, ROAS, CPA, CPL, CAC with industry benchmarking
- `funnel_analyzer.py`: Stage-by-stage conversion rates, drop-off identification, bottleneck detection
- Time-decay model uses configurable half-life parameter — not just a label

**Problem-Solving Quality: VERY GOOD**
- Attribution models guide explains when to use each model (rare — most resources just list them)
- Funnel optimization framework covers real concepts (stage-specific interventions, not just "improve conversion")
- Campaign metrics benchmarks provide industry reference points
- A/B test template and channel comparison template are useful artifacts

**Structure: STRONG**
- Consistent with business-growth pattern
- References tied to script functionality
- Sample data with customer journeys for attribution testing

**Verdict: SOLID** (borderline POWERFUL)
*Evidence: The 5 attribution models are correctly implemented and genuinely useful for any marketing team not yet using a dedicated attribution platform. However, the funnel analyzer (305 lines) is thinner than the equivalent scripts in other skills, and the overall scope is narrower than the business-growth skills.*

---

### 6. project-management/jira-expert

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: GOOD**
- JQL examples reference is genuinely useful — covers sprint queries, team workload, SLA tracking, change management queries
- Automation examples reference covers real Jira automation rules
- SKILL.md has comprehensive workflow descriptions for project creation, workflow design, JQL building
- Actually teaches JQL syntax with practical examples, not just theory

**Structure: ADEQUATE**
- No scripts, no assets, no sample data
- But the references are substantive (415 + 423 = 838 lines of reference material)
- Workflows reference other PM skills (Scrum Master, Confluence Expert) — good cross-linking

**Verdict: SOLID**
*Evidence: The JQL examples alone are a legitimate reference resource. The automation examples cover real-world rules. But without scripts or structured output tooling, this is fundamentally a knowledge-base skill, not a tool skill. It makes Claude better at Jira advice but doesn't produce artifacts.*

---

### 7. project-management/confluence-expert

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: GOOD**
- Templates reference (725 lines) contains 10+ ready-to-use Confluence page templates: meeting notes, decision log, project status, runbook, postmortem, ADR, onboarding guide
- Space architecture guidance is practical and specific (max 3 levels deep, naming conventions)
- Macro usage examples are helpful for Confluence power users

**Structure: ADEQUATE**
- Strong reference content compensates for lack of scripts
- Templates are the actual artifact output — when Claude uses this skill, it produces Confluence pages

**Verdict: SOLID**
*Evidence: The templates reference is the real value here — it's a curated library of production-quality Confluence page templates. A team setting up Confluence from scratch would find this genuinely useful. The space architecture guidance reflects real organizational experience.*

---

### 8. project-management/atlassian-admin

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: GOOD**
- SKILL.md is comprehensive at 414 lines covering user provisioning, deprovisioning, group management, permission schemes, security configuration
- Workflows are procedural and actionable (step-by-step with handoffs to other skills)
- Permission scheme design section is practical — distinguishes public/team/restricted/confidential project types
- SSO/SAML and security policy coverage is relevant

**Structure: ADEQUATE**
- No references, no assets — all content in SKILL.md
- Good cross-references to other PM skills (Jira Expert, Confluence Expert)

**Verdict: SOLID**
*Evidence: The user provisioning/deprovisioning workflows with audit steps reflect real admin concerns (content reassignment before account deletion). Permission scheme design is specific enough to be useful. But without reference docs or scripts, it's a well-written playbook rather than a tool.*

---

### 9. project-management/atlassian-templates

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: GOOD**
- SKILL.md at 751 lines is the longest PM skill — contains actual template content inline
- Template creation process (10-step) and modification process (8-step) are well-structured
- Contains ready-to-use templates: meeting notes, decision log, sprint planning, retrospective, project charter
- Blueprint development workflow is practical

**Structure: ADEQUATE**
- All content in SKILL.md — no separate references or assets
- Templates are embedded directly rather than in a templates/ directory

**Verdict: SOLID**
*Evidence: The templates themselves are the deliverable, and they're decent. The template governance process (versioning, deprecation, migration) shows organizational maturity. However, significant overlap with confluence-expert/references/templates.md raises questions about redundancy.*

---

### 10. project-management/scrum-master

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: MEDIOCRE**
- SKILL.md at 189 lines is thin — covers basic Scrum ceremonies at a surface level
- Nothing here goes beyond what's in the Scrum Guide
- No velocity tracking formulas, no capacity planning models, no sprint health metrics
- Retro formats reference (336 lines) is the saving grace — covers Start/Stop/Continue, Glad/Sad/Mad, 4Ls, Sailboat, DAKI formats with actual process steps

**Structure: WEAK**
- No assets, no sample data
- Single reference file
- Cross-references to Jira Expert and Confluence Expert add some value

**Verdict: GENERIC**
*Evidence: A certified Scrum Master would find nothing new here. The retro formats reference is genuinely useful but is the only substantive content. The SKILL.md reads like a job description, not a methodology. No metrics, no anti-patterns, no "when sprints go wrong" playbooks. Missing: burndown analysis tools, velocity prediction, capacity planning scripts.*

---

### 11. project-management/senior-pm

**Code Quality: N/A** — No scripts

**Problem-Solving Quality: WEAK**
- SKILL.md at 146 lines is the thinnest skill in the entire batch
- `references/api_reference.md` is literally a placeholder: "This is a placeholder for detailed reference documentation. Replace with actual reference content or delete if not needed."
- Content is generic PM advice: "develop product roadmaps aligned with business objectives," "identify and mitigate project risks"
- No frameworks, no decision models, no risk quantification methods
- No RACI template, no project charter template despite mentioning them

**Structure: WEAK**
- Placeholder reference file is a red flag
- No assets, no templates, no sample data
- Mentions creating artifacts (RACI matrix, project charter) but provides no templates

**Verdict: WEAK**
*Evidence: The placeholder reference file tells the whole story — this skill was scaffolded but never completed. A senior PM would find nothing actionable. Compare to the financial-analyst skill (1,781 lines of working code + templates) vs. this (146 lines of generic advice + a placeholder). This is "act as a Senior PM" prompting dressed up as a skill.*

---

## Comparative Analysis

| Skill | Scripts (LOC) | References | Assets/Templates | Verdict |
|-------|--------------|------------|-------------------|---------|
| customer-success-manager | 3 (1,339) | 3 deep | 5 templates + sample data | **POWERFUL** |
| revenue-operations | 3 (1,685) | 3 deep | 7 templates + sample data | **POWERFUL** |
| sales-engineer | 3 (1,847) | 3 deep | 5 templates + sample data | **POWERFUL** |
| financial-analyst | 4 (1,781) | 3 deep | 4 templates + sample data | **POWERFUL** |
| campaign-analytics | 3 (1,111) | 3 deep | 5 templates + sample data | **SOLID** |
| jira-expert | 0 | 2 substantive | 0 | **SOLID** |
| confluence-expert | 0 | 1 (725 lines) | 0 | **SOLID** |
| atlassian-admin | 0 | 0 | 0 | **SOLID** |
| atlassian-templates | 0 | 0 | 0 | **SOLID** |
| scrum-master | 0 | 1 (336 lines) | 0 | **GENERIC** |
| senior-pm | 0 | 1 (placeholder!) | 0 | **WEAK** |

## Key Observations

### What Works (business-growth, finance, campaign-analytics)
1. **Scripts that actually compute things** — Not wrappers, not boilerplate. Real algorithms with real business logic (DCF valuation, attribution modeling, health scoring)
2. **Zero external dependencies** — Deliberate stdlib-only design means they run anywhere, immediately
3. **Dual output format** — JSON for automation, text for humans. This is good engineering
4. **Sample data + expected output** — Enables validation and serves as documentation
5. **References that explain *why*** — The health scoring framework doesn't just list metrics; it explains why each dimension is weighted as it is
6. **Templates that are fill-in-ready** — QBR template, variance report, demo script — these save real time

### What Doesn't Work (parts of project-management)
1. **Senior PM is unfinished** — Placeholder reference file, no templates despite claiming to produce them
2. **Scrum Master is generic** — Doesn't exceed the Scrum Guide in depth or utility
3. **No scripts in any PM skill** — The business-growth skills prove that scripts add massive value. The PM skills could have had: sprint velocity calculator, capacity planner, risk matrix scorer, RACI generator
4. **Two-tier quality** — The gap between POWERFUL and WEAK skills in the same repo is jarring

### Recommendations
1. **Senior PM needs a complete rewrite or removal** — The placeholder reference is unacceptable. Either build it to the standard of financial-analyst (scripts + real frameworks) or don't ship it
2. **Scrum Master needs depth** — Add velocity tracking scripts, burndown analysis, capacity planning calculator, sprint health scorer
3. **PM skills should get scripts** — Even simple ones: RACI matrix generator, risk register scorer, project status report formatter
4. **Deduplicate PM templates** — atlassian-templates and confluence-expert overlap significantly
5. **Add expected_output.json to PM skills** — If they can't have scripts, at least define what "good output" looks like

---

*Report generated 2026-02-15. Skills assessed against the bar: "Would this make someone say 'holy shit, this actually knows what it's doing?'"*

*Business-growth and finance skills clear that bar. Campaign-analytics nearly does. PM skills mostly don't.*
