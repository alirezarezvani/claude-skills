# Domain audit: business-operations/ + commercial/ + finance/ + business-growth/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 24 · Agents: 2 · Commands: 17 (+2 root finance commands) · Plugins: 5

## Scorecard

| Skill | Verdict | Top issue |
|---|---|---|
| business-operations/business-operations-skills | KEEP | — (orchestrator routing is real: signal table + 2-signal threshold + no-silent-chain) |
| business-operations/process-mapper | KEEP | — (deterministic VA% bands, 3 detection rules, profiles) |
| business-operations/vendor-management | OPTIMIZE | Frontmatter description 1,106 chars (> 1024 A1 limit) |
| business-operations/capacity-planner | KEEP | — (Erlang-C, P50/P90/P99, manager-trigger; best forcing-question library in scope) |
| business-operations/internal-comms | OPTIMIZE | Description 1,284 chars (> 1024) |
| business-operations/knowledge-ops | OPTIMIZE | Description 1,314 chars (> 1024) — the actual cause of its 2/6 repo-checklist infamy; content itself is strong |
| business-operations/procurement-optimizer | OPTIMIZE | Description 1,266 chars (> 1024) |
| commercial/commercial-skills | KEEP | — (orchestrator; 7-lane signal table, depth-first chaining gates) |
| commercial/pricing-strategist | KEEP | — (model+range hard rule operationalized in workflow Step 5 + anti-pattern #1) |
| commercial/deal-desk | OPTIMIZE | Margin math is internally contradictory (SKILL.md says 37.5% loss; script computes 24-pt / 30% via a different formula) |
| commercial/partnerships-architect | KEEP | — (deterministic tier floors, kill-criteria mandate) |
| commercial/channel-economics | OPTIMIZE | Description 1,178 chars (> 1024) |
| commercial/commercial-policy | KEEP | — (4-dim matrix, 10-rule linter, precedent-risk flag verified) |
| commercial/rfp-responder | KEEP | — (GAP-never-invent rule, no-bid < 20% threshold; winrate sample verified) |
| commercial/commercial-forecaster | KEEP | — (assumption block verified NON-OPTIONAL in script output) |
| finance/finance-skills | CUT-OR-MERGE | 55-line plugin README posing as a skill; broken paths; no trigger description |
| finance/financial-analyst | OPTIMIZE | All 4 scripts silently fail (exit 0, zeros) against their own bundled sample — schema mismatch |
| finance/saas-metrics-coach | KEEP | — (benchmark tables with thresholds, strict output contract, status labels) |
| finance/business-investment-advisor | OPTIMIZE | Nested plugin unregistered in marketplace; manifest description truncated mid-word |
| business-growth/business-growth-skills | CUT-OR-MERGE | References phantom "BizDev-toolkit" skill; broken quick-start paths |
| business-growth/contract-and-proposal-writer | OPTIMIZE | 423-line SKILL.md with full contract templates inline; no scripts/references/assets at all |
| business-growth/customer-success-manager | KEEP | — (weighted scorers with explicit weights/thresholds, segment-aware) |
| business-growth/revenue-operations | KEEP | — (formula+threshold tables, CRM cross-check verification steps) |
| business-growth/sales-engineer | KEEP | — (executable validation checkpoints between phases; strongest A4 in scope) |

**Counts: 14 KEEP · 8 OPTIMIZE · 0 REWRITE · 2 CUT-OR-MERGE**

## Domain-level findings

1. **The v2.8.0 claims hold.** Both orchestrators (`business-operations-skills`, `commercial-skills`) have `context: fork` in frontmatter and real routing logic — signal tables, a 2-signal confidence threshold, single-question fallback with recommended answer, and explicit "never silently chain" gates. Every one of the 13 bizops/commercial sub-skills ships a 5-8 question forcing-question library with per-question recommended answer + canon citation. This is not vague prose.
2. **Hard rules are operationalized, not just claimed.** Verified by execution: `deal_scorer.py --sample` emits an approver chain and "2 critical signal(s) detected; cannot APPROVE" (never auto-approves); `bookings_forecaster.py --sample` emits an "Assumption block (NON-OPTIONAL)" section; pricing-strategist's workflow Step 5 and anti-pattern #1 enforce model+range-never-a-number; vendor/procurement outputs are framed as "inputs to a human decision" with refusal logic (single-source tier-1 consolidation refused without break-glass).
3. **Systemic A1 failure in the v2.8.0 batch: 5 of 15 frontmatter descriptions exceed the 1,024-char limit** (knowledge-ops 1,314 · internal-comms 1,284 · procurement-optimizer 1,266 · channel-economics 1,178 · vendor-management 1,106). They cram "Distinct from" and tool inventories into the trigger field. This — not content quality — is what tanked knowledge-ops/procurement-optimizer on the repo's own checklist. One-pass fix: move everything after the trigger sentence into the body.
4. **Systemic A3 gap in the v2.8.0 batch: almost no fenced CLI examples.** 8 of 13 sub-skills score "0 code blocks" on the repo checklist; invocations live in prose/tables. deal-desk and commercial-policy (which have "Quick examples" sections) show the right pattern.
5. **finance/ and business-growth/ are a different generation.** No forcing questions, no profiles, no named-owner routing, meta-skills (`finance-skills`, `business-growth-skills`) that are plugin READMEs with broken paths. The per-skill content (saas-metrics-coach, customer-success-manager, revenue-operations, sales-engineer) still earns KEEP on calibrated thresholds, but the wrappers are dead weight.
6. **One genuinely broken tool chain: financial-analyst.** Its `assets/sample_financial_data.json` nests data under per-tool keys (`ratio_analysis`, `dcf_valuation`, `budget_variance`, `forecast`) while all four scripts read top-level keys. Result: every documented quick-start command "succeeds" (exit 0) while emitting all-zero ratios, "Error: Historical revenue data is required" (still exit 0), `Total Items: 0`, and $0.00 forecasts. The repo-wide `--help` smoke test cannot catch this class of failure.
7. **Domain-math inconsistency in deal-desk.** SKILL.md (citing `discount_economics.md`) says "a 30% discount on an 80% gross-margin product loses 37.5% of margin, not 30%" — correct under fixed COGS: margin dollars fall 30/80 = 37.5%. But `deal_scorer.py` and `discount_economics.md` actually use `net_margin = G − D·(G/100)` (proportional COGS) → 24-pt loss / 30% relative. The script's own docstring writes the correct `(G−D)/(1−D/100)` formulation, then discards it. Pick one model; the scorer's margin dimension (weight 0.30) currently understates discount damage.

## Per-skill findings

### business-operations/vendor-management — OPTIMIZE
- Issues: (1) description 1,106 chars > 1024 — trim to trigger sentence, move "Ships 3 tools…" and "Distinct from…" into the body; (2) no fenced CLI examples (checklist rule 5); (3) SKILL.md 170 lines — body content fine, but Steps 2-4 partially duplicate script-level docs.
- Verify: `python3 -c "import re;t=open('business-operations/skills/vendor-management/SKILL.md').read();d=re.search(r'description:(.*?)\n\w+:',t,re.S).group(1);assert len(d.strip())<1024"` · `python3 skills/vendor-management/scripts/vendor_scorer.py --sample` exits 0 with KEEP/REVIEW/REPLACE verdicts · `--profile healthcare` output differs from `--profile saas` · SKILL.md contains ≥ 1 fenced ```bash block.

### business-operations/internal-comms — OPTIMIZE
- Issues: (1) description 1,284 chars > 1024; (2) zero fenced CLI examples; (3) "Distinct from" appears in both description and body (duplicated context cost).
- Verify: description < 1024 chars · all 3 scripts pass `--sample` exit 0 · `change_announcement_builder.py` still rejects "exciting news" tone on `disruptive` magnitude (magnitude/tone validation preserved) · ≥ 1 fenced code block in SKILL.md.

### business-operations/knowledge-ops — OPTIMIZE
- Issues: (1) description 1,314 chars > 1024 — worst in repo, and the real driver of its 2/6 checklist score; (2) zero fenced CLI examples; (3) "a procurement tool sunset in 2024" tripped the time-sensitivity rule — rephrase relatively; (4) content (5W2H validator thresholds, SAFE ≥ 80 / NOT-SAFE < 60 bands, staleness×inbound-links ranking) is genuinely strong — do not rewrite.
- Verify: description < 1024 chars · `kb_ingester.py --sample` exits 0 and reports orphan/stale/glossary-drift counts on the synthetic 8-page vault · `runbook_validator.py --sample` returns NOT-SAFE on the deliberately-broken runbook · repo checklist (`skill_review_checklist_runner.py <folder>`) reaches ≥ 4/6.

### business-operations/procurement-optimizer — OPTIMIZE
- Issues: (1) description 1,266 chars > 1024; (2) zero fenced CLI examples; (3) SKILL.md 167 lines with tool inventory repeated 3× (description, Workflow, Scripts table).
- Verify: description < 1024 chars · `supplier_consolidation.py --sample` exits 0 and still emits the "DO NOT CONSOLIDATE — tier-1 cluster, no break-glass" refusal on a tier-1 cluster without break-glass flag · `spend_categorizer.py --sample --profile enterprise` differs from `--profile tech-startup`.

### commercial/deal-desk — OPTIMIZE
- Issues: (1) margin-formula contradiction: SKILL.md claims 37.5% margin loss (fixed-COGS, correct), `deal_scorer.py:123-133` + `references/discount_economics.md` compute `G − D·G/100` = 24 pts (proportional-COGS); the docstring names the correct `(G−D)/(1−D/100)` formula then ignores it — reconcile to one model across all three files; (2) discount_economics.md "Why the conventional shorthand is wrong" section is itself wrong under the standard fixed-COGS assumption.
- Verify: `deal_scorer.py --sample` exits 0, verdict DECLINE, output contains "cannot APPROVE" and a ≥ 4-hop approver chain · SKILL.md margin example, `discount_economics.md` worked table, and `score_margin()` produce the same number for (G=80, D=30) · `--profile services` composite differs from `--profile saas` · `terms_redliner.py --sample` flags uncapped indemnity as CRITICAL.

### commercial/channel-economics — OPTIMIZE
- Issues: (1) description 1,178 chars > 1024 — it embeds four "Not X (that's Y)" disambiguations plus a keyword list; (2) zero fenced CLI examples.
- Verify: description < 1024 chars · all 3 scripts pass `--sample` exit 0 · `channel_roi_analyzer.py --sample` emits one of DOUBLE-DOWN/MAINTAIN/DEFUND/EXIT per channel · cost-to-serve output contains both per-deal and per-$-ARR lines.

### finance/finance-skills — CUT-OR-MERGE
- Issues: (1) it is a plugin README, not a skill — no workflow, no decision rules, no trigger phrasing ("Financial analyst agent skill and plugin for Claude Code, Codex…"); (2) quick-start path `finance/financial-analyst/SKILL.md` doesn't exist (actual: `finance/skills/financial-analyst/`); (3) wholly duplicates plugin.json + finance/CLAUDE.md. Merge useful lines into README.md/plugin.json and delete, or rebuild as a real router (the bizops/commercial orchestrator pattern exists to copy).
- Verify (if merged): `finance/skills/finance-skills/` removed AND `finance/.claude-plugin/plugin.json` `skills` array updated AND `check_plugin_json.py --all` passes · no references to `finance/financial-analyst/` (without `/skills/`) remain: `grep -r "finance/financial-analyst" finance/ | grep -v skills/` returns nothing.

### finance/financial-analyst — OPTIMIZE
- Issues: (1) **broken tool wiring**: all 4 scripts read top-level keys (`income_statement`, …) while `assets/sample_financial_data.json` nests them under `ratio_analysis`/`dcf_valuation`/`budget_variance`/`forecast` — every documented quick-start emits zeros; (2) error masking: `dcf_valuation.py` prints "Error: Historical revenue data is required" and exits 0; (3) `references/financial-ratios-guide.md` cites zero sources (A7); (4) Phase 1/5 of the workflow is filler a frontier model doesn't need ("Define analysis objectives and stakeholder requirements").
- Verify: `ratio_calculator.py assets/sample_financial_data.json` produces zero "Insufficient data" lines and a nonzero Gross Margin · `dcf_valuation.py <bad input>` exits nonzero · `budget_variance_analyzer.py assets/sample_financial_data.json` reports Total Items > 0 · `forecast_builder.py` base-case revenue > $0 on the bundled sample.

### finance/business-investment-advisor — OPTIMIZE
- Issues: (1) nested plugin `finance/business-investment-advisor/.claude-plugin/plugin.json` is not registered in marketplace.json — either register it or fold the skill into the finance plugin's `skills` array and delete the nested manifest; (2) that manifest's description is truncated mid-word ("Also use f"); (3) prompt-only skill claiming "show all math" with no deterministic tool — acceptable for an advisor, but the IRR/NPV sections restate model-known formulas (A2); the rubric + proactive-triggers + anti-pattern table are the parts that earn context — trim the formula restatements.
- Verify: skill is reachable via exactly one registered plugin (`python3 scripts/check_plugin_json.py --all` passes; marketplace lookup finds it) · manifest description is a complete sentence < 1024 chars · SKILL.md ≤ ~150 lines after trimming formula primers.

### business-growth/business-growth-skills — CUT-OR-MERGE
- Issues: (1) names a fifth skill "BizDev-toolkit" that does not exist anywhere in the repo; (2) quick-start path `business-growth/customer-success-manager/SKILL.md` is wrong (actual: `business-growth/skills/customer-success-manager/`); (3) body says "4 production-ready skills", description says 5 — neither matches a real router; (4) duplicates plugin.json + CLAUDE.md. Same disposition as finance-skills: delete-and-merge, or rebuild on the bizops orchestrator pattern.
- Verify (if merged): folder removed, plugin.json skills path still valid, `grep -ri "bizdev-toolkit" business-growth/` returns nothing, `check_plugin_json.py --all` passes.

### business-growth/contract-and-proposal-writer — OPTIMIZE
- Issues: (1) 423-line SKILL.md with three full contract templates + a GDPR DPA block inline — move Templates A/B/C and the DPA block to `assets/` and keep selection logic + jurisdiction notes + pitfalls in SKILL.md (progressive disclosure, A2); (2) only single-file skill in scope — no references/assets despite being template-heavy by nature; (3) static legal claims (§126 BGB, §74 HGB, "post-Brexit") carry freshness risk with no last-reviewed marker; add one; (4) overlaps `commercial/rfp-responder` and `c-level-advisor/general-counsel-advisor` — the existing scope sentence is good, keep it.
- Verify: SKILL.md ≤ ~150 lines · `assets/` contains ≥ 4 template files referenced by name from SKILL.md · description still trigger-phrased ("Use when drafting…") · a "last legal review" date line exists.

## KEEP-verdict verification criteria

- **business-operations-skills**: frontmatter retains `context: fork`; signal table lists exactly 6 lanes matching plugin.json skill paths; "Do NOT chain silently" and ≤ 200-word digest rules present.
- **process-mapper**: 3 scripts pass `--sample` exit 0; `cycle_time_analyzer` emits VA% verdict ∈ {HEALTHY, TYPICAL, WASTE-HEAVY} with 25%/10% bounds; `bottleneck_detector.py --profile healthcare` ≠ `--profile saas` output.
- **capacity-planner**: `capacity_modeler.py --sample` exits 0 with risk band ∈ {SAFE, WATCH, AT_RISK, CRITICAL} and a P50/P90/P99 breach table; `hiring_sequencer` triggers a manager hire when span crosses 7; 7 forcing questions remain canon-cited.
- **commercial-skills**: `context: fork` retained; 7-lane signal table matches the 7 sub-skill folders; anti-pattern list keeps "recommend a range + model" and "never auto-approve" lines.
- **pricing-strategist**: `wtp_analyzer.py --sample` exits 0, emits OPP/IDP/PMC/PME + a sub-100-N sample-size warning; `packaging_designer.py --sample` flags ≥ 1 anti-pattern; SKILL.md anti-pattern #1 ("Recommending a specific number") intact.
- **partnerships-architect**: `partner_tier_classifier.py --sample` exits 0; STRATEGIC floor still requires named_accounts ≥ 5 AND multi-year commit AND dedicated resources; kill-criteria mandate in Assumptions.
- **commercial-policy**: `policy_linter.py --sample` exits FAIL-by-design with 4 BLOCKERs; `exception_router.py --sample` routes the 42% exception with ≥ 3 compensating commitments; precedent-risk (3+ similar exceptions) flag preserved.
- **rfp-responder**: `winrate_predictor.py --sample` exits 0 with estimate + confidence band + verdict ∈ {BID, PARTNER-BID, NO-BID}; < 20% auto-no-bid threshold intact; "never invents claims" GAP rule in both description and Step 2.
- **commercial-forecaster**: `bookings_forecaster.py --sample` output contains "Assumption block (NON-OPTIONAL"; three tiers (commit/best-case/pipe-only) emitted; CoV bands (10/25/50%) in `funnel_confidence_scorer` unchanged.
- **finance/saas-metrics-coach**: `metrics_calculator.py --mrr 50000 --customers 100 --churned 5 --json` exits 0 with `_missing` array; quick-ratio bands (<1 CRITICAL, >4 EXCELLENT) match references/benchmarks.md; output-format template (Metrics at a Glance → 90-Day Focus) preserved.
- **customer-success-manager**: all 3 scripts exit 0 against `assets/sample_customer_data.json` (its sample actually works — unlike financial-analyst's); dimension weights sum to 100% in both SKILL.md tables and scripts; Green/Yellow/Red bounds 75/50 unchanged.
- **revenue-operations**: 3 scripts exit 0 against bundled samples; coverage target 3-4x, MAPE rating table, and Rule-of-40 thresholds present in both SKILL.md and script output.
- **sales-engineer**: the inline python validation one-liners in Phases 1/3/4 execute without KeyError against `--format json` output of the corresponding scripts (these are the skill's A4 backbone — keep them runnable).

## Agents

2 agents in scope (`business-operations/agents/cs-bizops-orchestrator.md`, `commercial/agents/cs-commercial-orchestrator.md`); finance/ and business-growth/ ship none.

- **B1**: both have name/description/tools/model. Descriptions are persona-stated rather than "Use when…"-phrased — minor A1-style gap; routing context is otherwise clear. Both pin `model: sonnet` — verify that's intended for orchestration-heavy work on new-gen defaults.
- **B2**: genuinely differentiated — different signature questions ("Where does the work spend most of its time waiting?" vs "What's the margin at full discount?"), different lane tables, different hard-output contracts (named approver / model+range / disclosed assumption). Not swappable.
- **B3**: no boilerplate. One staleness bug in both: the "Available commands" sections still annotate 9 commands with "(Sprint 2)" although all shipped — delete the annotations.
- Gap: business-growth and finance rely on root-level `/saas-health`, `/financial-health` and no persona agent; acceptable for legacy skills, but if the meta-skills are rebuilt as routers, add agents then — not before.

## Commands

17 in scope (8 bizops, 9 commercial) + 2 root finance commands (`/saas-health`, `/financial-health`).

- **C1/C2**: all sampled commands have accurate frontmatter descriptions and `argument-hint`, and interpolate `$ARGUMENTS`.
- **C3**: routers (`/cs:bizops`, `/cs:commercial`) and grills (`/cs:grill-bizops`, `/cs:grill-commercial`) clearly orchestrate (signal scoring, one-question discipline, refusal-to-route gates) — pass. Per-skill commands (`/cs:vendor-review`, `/cs:deal-review`, `/cs:knowledge-ops`, etc.) mostly restate their SKILL.md's tool table + "Distinct from" section; they pass C3 only because they name exact tools/profiles/verdicts. If context budget ever matters, these 13 per-skill commands are the first merge candidates into their routers — but no action required now.
- `/saas-health` and `/financial-health` are thin wrappers over the scripts; `/financial-health` inherits the financial-analyst sample-schema bug (its documented `ratios <data.json>` path silently zeroes). Fix rides on the financial-analyst OPTIMIZE.
- business-growth/ has zero commands — its 4 real skills are invocable only by description-matching. Acceptable; note for any future refresh.

## Plugin manifests

All 5 schema-valid (repo-wide E1 pass confirmed); versions coherent at 2.9.0 where registered. E2 drift everywhere:

1. **business-operations**: claims "24+ reference docs each citing ≥7 authoritative sources" — actual count is 18 (6 sub-skills × 3). Fix the number.
2. **commercial**: claims "28+ reference docs" — actual is 21 (7 × 3). Fix the number.
3. **finance**: description counts business-investment-advisor among its "3 finance skills", but `"skills": ["./skills"]` excludes it (it lives at `finance/business-investment-advisor/`, outside the path). Either move the skill under `finance/skills/` or correct the description.
4. **business-investment-advisor** (nested): description truncated mid-word ("…Also use f"); not registered in `.claude-plugin/marketplace.json` — it is currently undiscoverable as a plugin. Register or fold into finance-skills.
5. **business-growth**: description enumerates "BizDev-toolkit", a skill that does not exist; "5 business & growth skills" counts the meta-README skill. Correct to the 4 real skills (or 5 only after the meta-skill is rebuilt as a real router).
