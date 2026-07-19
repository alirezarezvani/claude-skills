# Domain audit: research/ + research-ops/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 13 (8 research/ + 5 research-ops/) · Agents: 9 · Commands: 14 · Plugins: 9

## Scorecard
| Skill | Verdict | Top issue |
|---|---|---|
| research-ops/research-ops-skills (orchestrator) | KEEP | Routing is prose-only (no classifier script like research/ ships) — acceptable, but inconsistent with sibling |
| research-ops/clinical-research | KEEP | — (model citizen; all hard rules verified in tool output) |
| research-ops/research-finance | KEEP | — (capex router never auto-decides; named owner verified) |
| research-ops/market-research | KEEP | — (both-methods TAM + triangulation flag verified) |
| research-ops/product-research | KEEP | — (INSIGHT vs ANECDOTE gate verified) |
| research/research (orchestrator) | OPTIMIZE | Single-keyword signals ("funding", "fda", "patent", "grant") cause weak-match misroutes; 319-line body restates generic search methodology |
| research/pulse | OPTIMIZE | Unauthenticated reddit.com/search.json is post-2023-API fragile; duplicated Agent Integrity boilerplate |
| research/litreview | OPTIMIZE | Hard Consensus-MCP dependency with no free-API fallback; phantom `scripts/office/validate.py` |
| research/grants | OPTIMIZE | Phantom `scripts/office/validate.py`; otherwise the strongest skill in the pack (RePORTER POST, dynamic FY, correct NIH receipt dates) |
| research/dossier | OPTIMIZE | Phantom `scripts/office/validate.py`; 318-line body |
| research/patent | OPTIMIZE | Phantom validate.py; `patents.uspto.gov/patent/...` hyperlink pattern is wrong (PPS lives at ppubs.uspto.gov) |
| research/syllabus | OPTIMIZE | Phantom validate.py; bundled JS requires npm `docx` (fails clean, but install path undocumented in plugin) |
| research/notebooklm | REWRITE | Hardcoded UI inventory of a fast-moving Google product has already rotted; description (8 Studio types) contradicts body (9) |

Verdict counts: **KEEP 5 · OPTIMIZE 7 · REWRITE 1 · CUT-OR-MERGE 0**

## Domain-level findings

1. **Phantom tool path across 5 research/ skills (A3 fail).** `python scripts/office/validate.py <docx>` is referenced as the DOCX validation step in litreview, grants, dossier, patent, and syllabus SKILL.md (plus litreview's README/agent/command and two reference docs). The file exists nowhere in the repo (`find -path "*office/validate.py"` → empty). Every DOCX workflow ends with an instruction the model cannot execute. One fix (ship the validator or delete the step) clears 5 skills at once.
2. **research-ops/ hard rules are genuinely operationalized — all sample runs passed.** `sample_size_estimator.py --sample` prints the "ESTIMATE ONLY — confirm with a biostatistician" banner + assumptions block + named-owner requirement; `market_sizer.py --sample` prints top-down AND bottoms-up TAM/SAM/SOM, a 73.4% divergence figure, and a "TRIANGULATION FAILED" flag; `insight_synthesizer.py --sample` promotes the 3-participant cluster to INSIGHT and flags 1- and 2-participant clusters as ANECDOTE; `capex_vs_opex_router.py --sample` routes all three verdicts to "R&D Finance Controller (+ External Auditor)"; `phase_gate_scorer.py --sample --output json` emits `verdict: GO` with a 3-name owner chain. Config consumption is real (tools import `config_loader`, CLI overrides, `RESEARCH_OPS_NO_CONFIG=1` bypass). This domain is the template the research/ pack should be refactored toward.
3. **research/ context economy is poor and boilerplate is forked, not shared.** SKILL.md bodies run 251–319 lines each; the "Agent Integrity Rules (Research-Pack Convention)" block is repeated near-verbatim in 7 files; `citation_tracker.py` exists as **6 divergent copies** (217–303 lines, all different md5s, 1,556 lines total). Per-skill self-containment is repo policy, but the variants have already drifted — a bug fix in one will not propagate. A shared reference + per-skill thin wrapper would cut ~40% of the pack's context weight.
4. **The repo's own checklist flags are partly a phrasing artifact, partly real.** Re-ran `skill_review_checklist_runner.py` on all 13: research-ops = 4/6 across the board (only fails the under-100-lines rule + the light 'skill'/'tool' terminology heuristic); research/ = 2–4/6. The "Missing trigger" failures on 7 of 8 research/ skills are because descriptions say `Triggers: 'pulse on [topic]'…` instead of the validator's `Use when…` pattern — the descriptions themselves are substantively rich (A1 passes on content, fails the repo gate on phrasing). The notebooklm 2/6 and research 2/6 KNOWN scores reproduce; research additionally trips the time-sensitive check ("in 2026").
5. **External-surface fragility is concentrated in research/.** Consensus MCP is a hard dependency for litreview, syllabus, and grants Phase 2A with zero fallback to free academic APIs (PubMed E-utilities, OpenAlex, Semantic Scholar — all keyless); pulse leans on unauthenticated Reddit JSON endpoints that Reddit increasingly blocks from datacenter IPs; notebooklm hardcodes a Google SPA's UI inventory. New-gen models with native WebSearch/WebFetch make free-API fallbacks cheap to specify — the skills predate that assumption.
6. **The orchestrator routing claim verifies.** `classifier.py` SIGNALS dict matches the SKILL.md table phrase-for-phrase; live tests: 3-signal litreview question → `route_to: litreview`, "research Microsoft" → `fallback` (as the SKILL.md explicitly promises), "dossier on Acme Corp for due diligence" → `dossier` (2 signals). The ≥2-signal threshold, single-weak-match rule, and fallback rule are all implemented. The followability problem is precision, not existence (see per-skill).
7. **All 48 Python scripts across both domains pass `--help` exit 0**; stdlib-only confirmed. The one non-Python script (`generate_reading_list.js`) fails without `npm install docx` but fails with a clear actionable message (acceptable, documented).
8. **Stray `__pycache__/*.pyc` committed under 4 research-ops script dirs** — repo hygiene, should be gitignored.

## Per-skill findings

### research/research (orchestrator) — OPTIMIZE
- Single-keyword signals over-trigger: "funding", "fda", "grant" (grants), "patent", "invention" (patent), "curriculum" (syllabus) each score 1 alone → the "single weak match" rule silently routes e.g. "research FDA approval trends" to grants. Multi-word phrases route reliably; bare nouns don't.
- 319 lines; Phase 3b fallback (decompose → search → synthesize → cite) restates what a frontier model does unprompted — keep the budget numbers + audit-log contract, cut the how-to prose.
- "Waits 1 turn… or auto-proceeds after 5s" is an un-executable affordance (the model cannot wait wall-clock time); checklist also flags "in 2026" as time-sensitive.
- Description lacks `Use when` phrasing → fails repo A1 gate (2/6 known score reproduces).
- Verify: `python3 scripts/classifier.py --question "research Microsoft" --output json` → `route_to: "fallback"`.
- Verify: `python3 scripts/classifier.py --question "literature review on PICO meta-analysis" --output json` → `route_to: "litreview"`, ≥2 signals.
- Verify: bare-noun precision test added: "research FDA approval trends" must NOT route to grants (after signal-list fix).
- Verify: checklist runner item 1 (trigger) and item 3 (time-sensitive) pass.

### research/pulse — OPTIMIZE
- Reddit phase depends on unauthenticated `reddit.com/search.json`; since the 2023 API changes these endpoints are routinely 403'd from non-browser/datacenter clients. Fallbacks exist (`raw_json=1`, subreddit-restricted) but a "Reddit fully blocked → degrade to Web-phase reddit site: search" path is missing.
- Hardcoded trusted-publisher `site:` list (NYT/WSJ/Wired/Verge/TechCrunch) is US-tech-centric and will silently skew non-tech topics.
- 258 lines incl. duplicated Agent Integrity block; checklist fails under-100-lines + terminology.
- Verify: `python3 scripts/time_window_calculator.py --window 30d` exits 0 and emits both HN `created_at_i` timestamp and Reddit `t=month`.
- Verify: `python3 scripts/citation_tracker.py --help` exits 0; session file lands at `~/.pulse_sessions/`.
- Verify: SKILL.md documents an explicit all-Reddit-blocked degradation path.

### research/litreview — OPTIMIZE
- Hard Consensus-MCP dependency; no fallback to free academic APIs (PubMed E-utilities / OpenAlex / Semantic Scholar are keyless) — the skill is inert in any harness without that one MCP.
- References phantom `python scripts/office/validate.py output.docx` (file does not exist anywhere in repo).
- Plan-tier detection parses marketing copy ("Showing top 10" / "upgrade") — brittle heuristic; will mis-detect when Consensus rewords.
- Verify: `python3 scripts/framework_recommender.py --help` and `cross_search_aggregator.py --help` exit 0.
- Verify: no reference to `scripts/office/validate.py` remains (grep returns empty) OR the validator ships.
- Verify: SKILL.md names at least one free-API fallback for the no-Consensus case.

### research/grants — OPTIMIZE
- Phantom `scripts/office/validate.py` in Phase 4 (only blocking edit — domain expertise is otherwise the best in the pack: RePORTER v2 POST templates, NOSI URL pattern, scope-aware mechanism matrix, dynamic FY window, NIH standard receipt dates all check out).
- Phase 2A (5 Consensus searches) has no free fallback; RePORTER core works without it but the SKILL treats Consensus as mandatory.
- Description fails the `Use when` gate (phrasing only).
- Verify: `python3 scripts/fiscal_year_calculator.py --output json` → `current_fy` correct for today's date (Oct 1 boundary), 4-year window.
- Verify: `python3 scripts/mechanism_matcher.py --career-stage early_career --prelim-data pilot --environment r01_eligible --scope single_site --output json` → shortlist excludes R01, includes R21/K-series.
- Verify: phantom validate.py reference removed or implemented.

### research/dossier — OPTIMIZE
- Phantom `scripts/office/validate.py` in Phase 10; 318-line body (longest in pack) with duplicated integrity boilerplate.
- The ≥30% disconfirming-evidence rule, source-tier tagging, and mandatory-hypothesis gate are excellent new-gen design (forces the model out of confirmation mode) — preserve verbatim.
- Glassdoor/Comparably scraping listed as a source will be blocked in practice; "degrade gracefully" is stated but the degraded output shape isn't.
- Verify: `python3 scripts/disconfirming_evidence_balance.py --help` exits 0; given a session with <30% disconfirming queries it returns a non-zero/warn signal.
- Verify: `python3 scripts/source_tier_classifier.py --help` exits 0; sec.gov → primary, a substack URL → tertiary.
- Verify: phantom validate.py reference removed or implemented.

### research/patent — OPTIMIZE
- Phantom `scripts/office/validate.py` in Phase 7.
- DOCX styling section gives `https://patents.uspto.gov/patent/...` as the USPTO hyperlink pattern — that host pattern is wrong (the skill's own source list correctly says `ppubs.uspto.gov`); links generated from it will 404.
- Sub-use-case routing, date discipline (filing/priority/publication/grant per use case), and CPC class follow-up are real practitioner expertise — keep.
- Verify: `python3 scripts/sub_use_case_router.py --sub-use-case novelty --jurisdictions "" --risk strict --known-art "US10000000B2"` exits 0 and emits a 5-8 query plan.
- Verify: `python3 scripts/family_resolver.py --help` exits 0.
- Verify: no `patents.uspto.gov/patent/` literal remains in SKILL.md.

### research/syllabus — OPTIMIZE
- Phantom `python scripts/office/validate.py` in Phase 6; Consensus-MCP hard dependency (same fix as litreview).
- `generate_reading_list.js` requires npm `docx`; fails with a clear message (verified) but neither SKILL.md Portability note nor plugin docs give the install one-liner next to the invocation.
- Applied-domain weaving + Bloom higher-order validator are genuinely non-obvious value — keep.
- Verify: `node scripts/generate_reading_list.js --help` without docx installed exits non-zero with the "npm install docx" message (graceful-fail contract).
- Verify: `python3 scripts/discussion_question_validator.py --help` and `topic_grouper.py --help` exit 0.
- Verify: phantom validate.py reference removed or implemented.

### research/notebooklm — REWRITE
- Freshness rot on a fast-iterating Google SPA: the hardcoded Studio inventory (9 types incl. "Table of Contents") no longer matches the product — NotebookLM added Video Overviews (2025) and Flashcards/Quiz, and reorganized report-style outputs; none appear anywhere in skill, scripts, or references (moderate-high confidence; needs re-verification against the live UI).
- Internal inconsistency: frontmatter description lists 8 Studio types, body Action 3 lists 9 — the plugin.json mirrors the stale 8.
- Known 2/6 checklist score reproduces: no `Use when` trigger phrasing, 290 lines, zero code blocks (no concrete invocation examples).
- Structure is salvageable (Step-0 environment gate, fire-and-notify async table, screenshot-first, find()-before-click are all sound discipline; `async_action_classifier.py` works); the rot-prone content is the hardcoded UI inventory + timing estimates. Rewrite to discover output types from the live Studio panel screenshot instead of enumerating them, add a "verified against NotebookLM as of <date>" maintenance marker, fix the 8-vs-9 contradiction.
- Verify: `python3 scripts/async_action_classifier.py --action "audio overview"` → `FIRE_AND_NOTIFY`; `--action "add source"` → wait verdict.
- Verify: frontmatter description and Action 3 list enumerate the same set (or neither enumerates).
- Verify: SKILL.md contains ≥1 fenced concrete-example block and a `Use when`-style trigger; checklist item 5 passes.
- Verify: a dated "UI verified" marker exists and is < 6 months old at release time.

## KEEP-verdict verification criteria

- **research-ops-skills (orchestrator):** SKILL.md signal table lists exactly 4 lanes matching the 4 sub-skill folder names; `grep -c "Never silently chain" SKILL.md` ≥ 1; every `skills/<sub-skill>/scripts/onboard.py` path it references resolves from `research-ops/`.
- **clinical-research:** `python3 scripts/sample_size_estimator.py --sample` exits 0, output contains "ESTIMATE" banner and `n_group1_with_dropout` > `n_group1_raw`; `phase_gate_scorer.py --sample --output json` → `verdict` ∈ {GO, GO-WITH-CONDITIONS, REDESIGN, NO-GO} and `named_owners` non-empty; `endpoint_selector.py --sample` flags the unvalidated surrogate below PRIMARY.
- **research-finance:** `capex_vs_opex_router.py --sample --standard ifrs` exits 0, every item carries `route to:` a named owner and the "DECISION SUPPORT ONLY" banner prints; `burn_runway_tracker.py --sample --output json` → `runway_months_approx` float + per-milestone `verdict`.
- **market-research:** `market_sizer.py --sample` prints BOTH `[top-down]` and `[bottoms-up]` TAM/SAM/SOM lines, a divergence %, and "TRIANGULATION FAILED" when delta > tolerance; `sample_size_planner.py --population 62000 --confidence 0.95 --moe 0.05` exits 0 with FPC-corrected n; `segmentation_scorer.py --sample` drops the solopreneur slice.
- **product-research:** `insight_synthesizer.py --sample --min-sources 3` promotes the 3-source cluster to INSIGHT and labels 1–2-source clusters ANECDOTE; `saturation_planner.py --method thematic --segments 3` emits a confidence label and the "not a power calculation" disclaimer; `study_designer.py --goal evaluative --stage live` redirects live A/B to experiment-designer.

## Agents

9 agents total (8 in `research/<plugin>/agents/`, 1 in `research-ops/agents/`). **All pass B2/B3 strongly** — each persona has distinct refusal behaviors that change outcomes (cs-dossier refuses without a hypothesis; cs-patent refuses without a sub-use-case; cs-research surfaces routing + override; cs-research-ops-orchestrator demands method-before-number) and verbatim voice lines, not adjective swaps. B1 issues:
- research/ agent descriptions describe behavior but lack `Use when`/`Use PROACTIVELY` trigger phrasing (same artifact as the SKILL.md gate).
- All 8 research/ agents pin `model: opus` — for a deterministic-routing front door (cs-research) sonnet would do; cost note only.
- research/ agents carry non-standard `skills:`/`domain:` frontmatter keys (harmless, but not part of the agent schema the repo's other domains use).
- cs-research-ops-orchestrator is the cleanest: standard frontmatter, `model: sonnet`, Skill tool wired for fork-routing.

## Commands

14 total: 8 `/cs:*` in research/ plugins, 6 in research-ops/. All pass C1 + C3 (each orchestrates intake gates, tool sequences, and refusal rules a bare prompt would not enforce). Findings:
- **research-ops commands are the better pattern:** proper `argument-hint:` field + explicit `$ARGUMENTS` interpolation + per-command three-tool workflow. `/cs:grill-research-ops` adds real value (docs-anchored one-question-at-a-time gate before any sub-skill).
- **research/ commands** embed the argument shape inside the description string and omit `argument-hint` / `$ARGUMENTS` (C2 partial) — they read as documentation pages for the agent rather than parameterized commands. Targeted fix: add `argument-hint` + `$ARGUMENTS` block to all 8.
- Mild redundancy: `/cs:research` + 6 specialist commands + the router skill itself is three entry points to the same routing logic; acceptable, but the specialist commands should state "or just use /cs:research" to avoid user confusion.

## Plugin manifests

All 9 pass `scripts/check_plugin_json.py --all` (E1). Versions uniformly 2.9.0 and present in marketplace.json (E3). Issues:
- **Name mismatch (E3 minor):** marketplace entry `research-orchestrator` points at `./research/research` whose plugin.json `name` is `research`. Intentional slug-disambiguation per ClawHub rules, but the inconsistency is undocumented in either file.
- **Stale content drift (E2):** `notebooklm` plugin.json description carries the 8-type Studio list (mirrors the stale SKILL.md frontmatter) — fix together with the notebooklm rewrite.
- research-ops single-domain-plugin description accurately enumerates the 4 sub-skills + orchestrator; matches contents.
- Hygiene: committed `__pycache__/*.pyc` under `research-ops/skills/{clinical-research,market-research,product-research,research-finance}/scripts/` should be removed/ignored.
