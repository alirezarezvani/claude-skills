# Domain audit: engineering/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 80 SKILL.md (63 distinct skills; 12 sub-command skills under agenthub/autoresearch; 4 dual-published duplicates; 1 sample asset excluded) · Agents: 14 · Commands: 14 · Plugins: 28 manifests

## Scorecard

Bundle = `engineering/skills/<name>`; standalone = `engineering/<name>/`.

| Skill | Verdict | Top issue |
|---|---|---|
| skills/agent-designer | REWRITE | 279 lines of taxonomy prose a frontier model already knows; 3 root-level scripts never wired |
| skills/agent-workflow-designer | OPTIMIZE | Thin body; overlaps agent-designer + workflow-builder |
| skills/api-design-reviewer | OPTIMIZE | ~300 lines of textbook REST; scripts named but no exact CLI in workflow |
| skills/api-test-suite-builder | KEEP | — |
| skills/browser-automation | KEEP | — |
| skills/changelog-generator | KEEP | — (absorb release-manager into it) |
| skills/chaos-engineering (+ standalone dup) | KEEP | — (deduplicate copies) |
| skills/ci-cd-pipeline-builder | KEEP | — |
| skills/codebase-onboarding | OPTIMIZE | Thin; 1 script, low expertise density |
| skills/command-guide | CUT-OR-MERGE | Documents another repo's (ECC) commands/agents that don't exist here |
| skills/database-designer | CUT-OR-MERGE | Overlaps 2 siblings; claims "included tools" with zero CLI wiring |
| skills/database-schema-designer | CUT-OR-MERGE | No scripts; broken seed-code example; overlaps database family |
| skills/dependency-auditor | REWRITE | Marketing brochure ("Future Enhancements", "Planned Features"); unverifiable claims |
| skills/engineering-advanced-skills | OPTIMIZE | Index says "25 skills", plugin says 40; wrong load paths |
| skills/env-secrets-manager | KEEP | — (fix dead cross-refs) |
| skills/feature-flags-architect (+ dup) | KEEP | — (deduplicate copies) |
| skills/focused-fix | KEEP | — (references external `superpowers:*` skills) |
| skills/full-page-screenshot | KEEP | — |
| skills/git-worktree-manager | KEEP | — |
| skills/interview-system-designer | OPTIMIZE | HR skill in engineering domain; 4 scripts, 1 wired |
| skills/kubernetes-operator (+ dup) | KEEP | — (deduplicate copies) |
| skills/mcp-server-builder | KEEP | — |
| skills/migration-architect | REWRITE | 477 lines textbook; scripts named only in "Tools" section, no CLI |
| skills/monorepo-navigator | KEEP | — |
| skills/observability-designer | REWRITE | Brochure prose; no exact CLI; overlaps slo-architect |
| skills/performance-profiler | KEEP | — |
| skills/pr-review-expert | KEEP | — |
| skills/rag-architect | REWRITE | Stale (ada-002, 2024 Pinecone pricing); 3 scripts never wired; textbook |
| skills/release-manager | CUT-OR-MERGE | 489-line textbook; duplicates changelog-generator; scripts unwired |
| skills/runbook-generator | OPTIMIZE | Thin skeleton generator, low expertise density |
| skills/secrets-vault-manager | KEEP | — |
| skills/self-eval | KEEP | — |
| skills/ship-gate | KEEP | — |
| skills/skill-security-auditor | KEEP | — |
| skills/skill-tester | REWRITE | 390-line brochure incl. "Future Enhancements"; CLI shown without paths |
| skills/slo-architect (+ dup) | KEEP | — (deduplicate copies) |
| skills/spec-driven-workflow | KEEP | — |
| skills/sql-database-assistant | KEEP | — (merge target for the database trio) |
| skills/tc-tracker | KEEP | — |
| skills/tech-debt-tracker | REWRITE | Roadmap/KPI filler; 5 passing scripts, zero CLI wiring |
| agenthub (8 SKILL.md) | KEEP | — |
| autoresearch-agent (6 SKILL.md) | KEEP | — (document evaluator --help exception in SKILL.md) |
| behuman | KEEP | — (not registered in marketplace) |
| caveman | KEEP | — |
| claude-coach | OPTIMIZE | Duplicate frontmatter keys; README content pasted into SKILL.md tail |
| code-tour | KEEP | — |
| data-quality-auditor | KEEP | — |
| demo-video | KEEP | — |
| docker-development | KEEP | — |
| grill-me | KEEP | — |
| grill-with-docs | KEEP | — (not registered in marketplace) |
| handoff (engineering) | KEEP | — |
| helm-chart-builder | KEEP | — |
| karpathy-coder | KEEP | — |
| llm-cost-optimizer | KEEP | — (not registered in marketplace) |
| llm-wiki | KEEP | — |
| prompt-governance | KEEP | — (not registered in marketplace) |
| security-guidance | KEEP | — |
| statistical-analyst | KEEP | — |
| terraform-patterns | KEEP | — |
| universal-scraping-architect | OPTIMIZE | 3 orphan scripts; placeholder agent + command; non-stdlib deps |
| workflow-builder | KEEP | — |
| write-a-skill | KEEP | — |

**Totals: KEEP 44 · OPTIMIZE 8 · REWRITE 7 · CUT-OR-MERGE 4** (63 distinct skills)

## Domain-level findings

1. **Two clear generations.** v2.4+ skills (slo-architect, chaos-engineering, kubernetes-operator, feature-flags-architect, karpathy-coder, workflow-builder, the Pocock ports, agenthub, autoresearch) are exemplary: trigger-rich descriptions, exact CLI per tool, refusal gates, "Verifiable success" sections. ~10 v2.0-era skills in `engineering/skills/` are capability brochures ("Future Enhancements", "Conclusion", "Planned Features" sections) whose body is knowledge a frontier model already has — pure context dead weight.
2. **Orphan-script epidemic in v2.0-era skills.** agent-designer, rag-architect, release-manager, database-designer (root-level `.py`), tech-debt-tracker and skill-tester (in `scripts/`) all ship working scripts (`--help` passes) that SKILL.md never invokes with a runnable command. A model following the SKILL.md will never run them — A3 failure across the board. universal-scraping-architect same pattern.
3. **Overlap clusters burning context.** (a) Database trio: database-designer / database-schema-designer / sql-database-assistant — sql-database-assistant alone covers ~90%; (b) release pair: release-manager vs changelog-generator (changelog-generator is the wired, lean one); (c) observability-designer vs slo-architect (slo-architect is strictly better on the SLO half).
4. **Byte-identical dual-published copies.** slo-architect, chaos-engineering, kubernetes-operator, feature-flags-architect each exist in both `engineering/skills/` and `engineering/<name>/skills/<name>/` (verified `diff` identical). No single source of truth; edits will diverge.
5. **Counter and registry drift.** Bundle index SKILL.md says "25 advanced engineering skills"; its plugin.json says 40; the marketplace description for `engineering-advanced-skills` lists skills (llm-cost-optimizer, prompt-governance, behuman, code-tour, demo-video, data-quality-auditor, statistical-analyst, llm-wiki…) that live in standalone plugin folders OUTSIDE the manifest's `"skills": ["./skills"]` path. Separately, 5 plugins with valid plugin.json (behuman, claude-coach, grill-with-docs, llm-cost-optimizer, prompt-governance) are not registered in marketplace.json at all.
6. **Dead cross-references.** env-secrets-manager points to `engineering/senior-secops`, `engineering/infrastructure-as-code`, `engineering/container-orchestration` (none exist; senior-secops lives in engineering-team/); sql-database-assistant points to nonexistent `observability-platform`; focused-fix references external `superpowers:*` skills; command-guide is entirely about a foreign ecosystem.
7. **Freshness spots.** rag-architect: `text-embedding-ada-002` as "quality model", "$70/month Pinecone 1M vectors" — 2023/24 facts presented as current. command-guide: `/fast` "(Opus 4.6 only)". api-design-reviewer example timestamps "2024-…".
8. **Reference quality is bimodal.** v2.0-era references (rag-architect, dependency-auditor, agent-designer) are uncited encyclopedic prose a frontier model regenerates on demand; v2.6+ references cite canon by name (Evans/Nygard/Google SRE Workbook/Pocock).
9. **By-design script exceptions partly documented.** autoresearch evaluators carry "DO NOT MODIFY — fixed evaluator" headers, but the SKILL.md never states they intentionally fail `--help`; security-guidance hook's stdin contract IS documented in its SKILL.md (good).

## Per-skill findings

### engineering/skills/agent-designer
Verdict: REWRITE
Issues:
- Entire 279-line body is generic multi-agent taxonomy (Supervisor/Swarm/Pipeline pros-cons) — A2/A5 fail; a frontier model knows all of it.
- 3 working scripts (`agent_planner.py`, `tool_schema_generator.py`, `agent_evaluator.py`, all pass `--help`) are never mentioned in SKILL.md — A3 fail; assets/expected_outputs unused.
- Description is bare trigger sentence with no mention of tools.
- Overlaps agent-workflow-designer and workflow-builder.
Verify: `python3 engineering/skills/agent-designer/agent_planner.py --help` exits 0 AND SKILL.md contains the literal string `agent_planner.py` with a runnable invocation; SKILL.md < 150 lines; `grep -c "Pros:" SKILL.md` returns 0.

### engineering/skills/agent-workflow-designer
Verdict: OPTIMIZE
Issues:
- 83-line body is mostly headers; pattern map duplicates `references/workflow-patterns.md` one-liners.
- No verification loop — scaffolder output is never validated by a named next step.
- Scope collision with workflow-builder (Claude Code Workflow tool) and agent-designer; needs explicit "NOT for" routing.
Verify: `python3 scripts/workflow_scaffolder.py sequential --name t` exits 0 and emits JSON; SKILL.md gains a "When NOT to use" block naming workflow-builder.

### engineering/skills/api-design-reviewer
Verdict: OPTIMIZE
Issues:
- Lines 41–333 restate REST conventions/pagination/status codes any frontier model knows — cut to references or delete.
- Tools section describes features but the only invocations are inside CI YAML examples; no first-class Quick Start CLI.
- Example timestamp `2024-02-16` (A6 nit).
Verify: `python3 scripts/api_linter.py --help` exits 0; SKILL.md has a Quick Start with all 3 script invocations; body ≤ 200 lines.

### engineering/skills/codebase-onboarding
Verdict: OPTIMIZE
Issues:
- 84 lines, single analyzer script; "Tailor output depth by audience" is the only non-obvious content.
- No verification loop (generated doc never validated against repo facts).
Verify: `python3 scripts/codebase_analyzer.py . --json` exits 0 and emits JSON with language/file-count keys; SKILL.md adds a post-generation check (e.g. "every setup command in the doc was executed once").

### engineering/skills/command-guide
Verdict: CUT-OR-MERGE
Issues:
- Documents commands/agents from the ECC ecosystem (`planner`, `build-error-resolver`, `tdd-guide`, `/build-fix`, `/learn`, `/remember`) — none ship in this repo; actively misleads the model into invoking nonexistent tools.
- `/fast` "(Opus 4.6 only)" — stale model gating (A6).
- Zero scripts, zero references; auto-trigger table tells the model to "immediately invoke" agents that don't exist here.
Verify (if kept at all): every command/agent named in the file resolves to a file in this repo (`grep -o '/[a-z-]*' SKILL.md` cross-checked against commands/); otherwise delete from plugin.

### engineering/skills/database-designer
Verdict: CUT-OR-MERGE (fold unique tables into sql-database-assistant)
Issues:
- "The included tools automate common analysis" but no script invocation anywhere; 3 root scripts orphaned (A3).
- JOIN/CTE/window-function content is textbook (A2); decision matrices duplicate sql-database-assistant's.
- Three-way overlap with database-schema-designer and sql-database-assistant; cross-refs to both admit it.
Verify: after merge, `engineering/skills/sql-database-assistant/SKILL.md` contains the sharding/replication tables; `schema_analyzer.py`/`index_optimizer.py`/`migration_generator.py` either wired into sql-database-assistant or deleted.

### engineering/skills/database-schema-designer
Verdict: CUT-OR-MERGE
Issues:
- No scripts at all; SKILL.md is one worked example + RLS snippets.
- Seed-data example is syntactically broken (`name: "fakercompanycatchphrase"` — missing comma, dead faker call, line ~155).
- ERD/normalization mandate duplicates database-designer's claims.
Verify: RLS policy block and pitfalls table migrated into the surviving database skill; broken seed example deleted or fixed to parse with `npx tsc --noEmit`.

### engineering/skills/dependency-auditor
Verdict: REWRITE
Issues:
- ~250 of 337 lines are brochure ("Use Cases & Applications", "Future Enhancements", "Metrics & KPIs") — A2/A7 fail.
- Claims "built-in vulnerability database with 500+ CVE patterns", live "PyPI/npm advisory" cross-referencing — SKILL.md's own scripts are offline pattern matchers; over-claims capability.
- Quick Start has 3 CLI lines buried at the bottom; no output-consumption step, no verification loop.
Verify: `python3 scripts/dep_scanner.py --help` exits 0; rewritten SKILL.md ≤ 150 lines, leads with the 3 CLIs + JSON keys consumed; no "Future Enhancements"/"Planned Features" headings remain.

### engineering/skills/engineering-advanced-skills
Verdict: OPTIMIZE
Issues:
- H1/body says "25 advanced engineering skills"; plugin.json says 40; folder has 39 + index — three different counts.
- Quick Start path `/read engineering/agent-designer/SKILL.md` is wrong (real path `engineering/skills/agent-designer/SKILL.md`).
- Table lists 25 of 39 skills; missing the reliability quartet, ship-gate, self-eval, tc-tracker, etc.
Verify: `ls engineering/skills | wc -l` matches the count stated in SKILL.md and plugin.json description; every path in the table resolves.

### engineering/skills/interview-system-designer
Verdict: OPTIMIZE
Issues:
- Hiring-process skill living in the engineering plugin — domain misfit (product-team/c-level fit better).
- 4 scripts present, only `interview_planner.py` wired; 59-line body with generic best practices.
Verify: all shipped scripts referenced with exact CLI in SKILL.md or removed; `python3 scripts/interview_planner.py --role "SWE" --level senior --json` exits 0 with JSON.

### engineering/skills/migration-architect
Verdict: REWRITE
Issues:
- 477 lines; Strangler Fig/CDC/blue-green content is textbook (A2); "Communication Templates" and "Success Metrics" sections are filler (A7).
- Scripts (`migration_planner.py`, `compatibility_checker.py`, `rollback_generator.py`) appear only as bullet names + one CI YAML snippet — no Quick Start CLI (A3).
- No verification loop; checklists are prose, not machine-checkable.
Verify: `python3 engineering/skills/migration-architect/migration_planner.py --help` exits 0; rewritten SKILL.md ≤ 200 lines with all 3 CLIs and a "plan must pass compatibility_checker with 0 CRITICAL" gate.

### engineering/skills/observability-designer
Verdict: REWRITE
Issues:
- 268 lines of golden-signals/RED/USE/three-pillars prose — pure frontier-model knowledge (A2/A5).
- "Scripts Overview" describes I/O shapes but gives zero runnable commands (A3); scripts pass `--help`.
- Overlaps slo-architect (which does the SLO half with thresholds + math + refusal gates); this skill should shrink to dashboards + alert-noise tooling and route SLO work to slo-architect.
Verify: `python3 scripts/slo_designer.py --help`, `alert_optimizer.py --help`, `dashboard_generator.py --help` all exit 0 AND appear as exact CLIs in SKILL.md; "When NOT to use → slo-architect" block present.

### engineering/skills/rag-architect
Verdict: REWRITE
Issues:
- Stale facts as current: `text-embedding-ada-002` as the quality tier, "Pinecone $70/month for 1M vectors", model lists from 2023/24 (A6).
- 3 root scripts (`chunking_optimizer.py`, `rag_pipeline_designer.py`, `retrieval_evaluator.py`, all pass `--help`) never referenced in SKILL.md (A3).
- 318 lines of chunking/retrieval taxonomy a frontier model knows; only 1 reference doc, uncited (A7).
Verify: `python3 engineering/skills/rag-architect/chunking_optimizer.py --help` exits 0 AND is invoked in SKILL.md; zero occurrences of `ada-002` / hardcoded vendor prices; body ≤ 200 lines.

### engineering/skills/release-manager
Verdict: CUT-OR-MERGE (into changelog-generator)
Issues:
- 489-line SemVer/Git-Flow/conventional-commits textbook (A2); changelog-generator already ships the wired, lean version of the changelog/bump core.
- 3 root scripts named in "Key Components" but never invoked (A3).
- Hotfix SLAs and rollback triggers are the only practitioner content — migrate those tables.
Verify: hotfix-severity and rollback-trigger tables present in the surviving skill; `version_bumper.py`/`release_planner.py` wired with exact CLI or deleted; no duplicate conventional-commit spec across the two skills.

### engineering/skills/runbook-generator
Verdict: OPTIMIZE
Issues:
- 76 lines, one template-skeleton script, generic best practices; weakest of the wired DevOps set.
- No verification loop (runbook never validated — e.g., "every command block has an expected-output check").
Verify: `python3 scripts/runbook_generator.py payments-api --owner x` exits 0 and emits the standard sections; SKILL.md adds a post-generation checklist the model executes (rollback section non-empty, every step has a verify line).

### engineering/skills/skill-tester
Verdict: REWRITE
Issues:
- 390 lines, heavy brochure: "Performance & Scalability", "Security & Safety", "Future Enhancements", "Conclusion" (A7).
- CLI examples lack paths (`skill_validator.py path/to/skill` won't run from repo root); one example references nonexistent `trend_analyzer.py` (phantom script, A3).
- Tier line-count requirements conflict with write-a-skill's "SKILL.md under 100 lines" doctrine — repo-internal contradiction.
Verify: `python3 engineering/skills/skill-tester/scripts/skill_validator.py engineering/skills/self-eval --json` exits 0 with JSON; no reference to `trend_analyzer.py`; body ≤ 200 lines.

### engineering/skills/tech-debt-tracker
Verdict: REWRITE
Issues:
- Body is a 6-week "Implementation Roadmap" + aspirational KPIs ("25% reduction in debt interest rate") — filler, zero operational instructions (A2/A5).
- 5 scripts incl. `debt_scanner.py`/`debt_prioritizer.py`/`debt_dashboard.py` all pass `--help` but SKILL.md contains not one CLI invocation (A3) — worst wiring gap in the domain relative to tooling quality.
- 4 references + 4 assets unreferenced from the body (A7).
Verify: SKILL.md Quick Start runs all 3 core scripts with exact flags; `python3 scripts/debt_scanner.py --help` exits 0; scan→prioritize→dashboard pipeline shows which JSON keys flow between steps.

### engineering/claude-coach
Verdict: OPTIMIZE
Issues:
- Frontmatter has duplicate/case-variant keys (`Name:` + `name:`, `Version: 1.0.0` + `version: 2.9.0`, stray `Tier/Category/Dependencies`) — undefined parse behavior.
- Lines 145–205 re-paste Name/Description/Features/Usage (README content) after the body ends — duplication (A7).
- Scripts listed at the very bottom with no CLI; `coach_tip_classifier.py` is core to Rule 5 but never invoked.
Verify: `python3 -c "import yaml,io; yaml.safe_load(open('engineering/claude-coach/skills/claude-coach/SKILL.md').read().split('---')[1])"` yields exactly one `name`/`version`; `python3 scripts/coach_tip_classifier.py --help` exits 0 and appears as a CLI in the body.

### engineering/universal-scraping-architect
Verdict: OPTIMIZE
Issues:
- 3 scripts (`validate_extraction.py`, `firecrawl_example.py`, `local_bs4_example.py`) never referenced in SKILL.md (A3).
- Agent (`cs-scraping-architect.md`, 6 lines) and command (`cs-scrape.md`, 6 lines) are placeholders — B3/C3 fail.
- "You are an expert…" opener (A2 filler); non-stdlib deps (firecrawl/pandas/bs4) acceptable (BYOK documented) but should be listed per-script.
- Layout anomaly: only engineering plugin with SKILL.md at plugin root (no `skills/` dir).
Verify: `python3 engineering/universal-scraping-architect/scripts/validate_extraction.py --help` exits 0 and is invoked in SKILL.md step 4 ("Validate & Clean"); agent file ≥ 40 lines with tools + triggers or deleted.

## KEEP-verdict verification criteria

- **api-test-suite-builder** — Next.js route-scan command from SKILL.md runs against a sample app dir without error; auth matrix table retains all 6 rows.
- **browser-automation** — `python3 scripts/anti_detection_checker.py --help` exits 0; all 3 referenced reference files exist.
- **changelog-generator** — `printf 'feat: x\nfix: y\n' | python3 scripts/generate_changelog.py --next-version v1.0.0 --format json` exits 0 with `Added`/`Fixed` sections; `commit_linter.py --strict` exits non-zero on `bad message`.
- **chaos-engineering** — `python3 scripts/blast_radius_calculator.py --traffic-share 0.05 --user-pop 1000000 --duration-min 15` exits 0, output contains GREEN/YELLOW/RED; bundle and standalone copies stay byte-identical (`diff -r`) until deduped.
- **ci-cd-pipeline-builder** — `python3 scripts/stack_detector.py --repo . --format json` exits 0 with detected-language keys; generated YAML parses (`python3 -c "import yaml,sys; yaml.safe_load(open('out.yml'))"`).
- **env-secrets-manager** — `python3 scripts/env_auditor.py . --json` exits 0 with severity-tagged findings; cross-reference table contains no path that fails `ls`.
- **feature-flags-architect** — `python3 scripts/rollout_planner.py --population 100000 --target-percent 100 --duration-days 14 --strategy ring` exits 0 with a phased table; `kill_switch_audit.py --help` exits 0.
- **focused-fix** — 5-phase headings (SCOPE/TRACE/DIAGNOSE/FIX/VERIFY) and the 3-strike escalation rule remain; `superpowers:` references either resolve or are reworded as optional externals.
- **full-page-screenshot** — `node scripts/full-page-screenshot.mjs --check` exits with documented status; anti-pattern table intact.
- **git-worktree-manager** — `python3 scripts/worktree_manager.py --help` and `worktree_cleanup.py --help` exit 0; validation checklist (ports file, env copy) retained.
- **kubernetes-operator** — `python3 scripts/crd_validator.py --help` exits 0; capability levels L1–L5 retained; dedupe with bundle copy.
- **mcp-server-builder** — `python3 scripts/openapi_to_mcp.py --help` and `mcp_validator.py --help` exit 0; strict mode returns non-zero on a manifest with a duplicate tool name.
- **monorepo-navigator** — `python3 scripts/monorepo_analyzer.py . --json` exits 0; pitfalls table keeps the `--filter` and `git filter-repo` rows.
- **performance-profiler** — `python3 scripts/performance_profiler.py . --json` exits 0; before/after template and "Measure First" rule retained.
- **pr-review-expert** — security-scan grep block runs against a sample diff without syntax errors; 30+ item checklist count ≥ 30.
- **secrets-vault-manager** — 3 tool names in the Tools table map to existing files in scripts/ (add exact CLI when touched); Vault HCL snippets parse visually.
- **self-eval** — composite matrix unchanged (Low ambition caps at 2; 5 requires High+Strong); scores append to `.self-eval-scores.jsonl`.
- **ship-gate** — `references/checks.md` and `references/patterns.md` exist; category table sums (55 auto + 27 manual) match checks.md entries.
- **skill-security-auditor** — `python3 scripts/skill_security_auditor.py engineering/skills/self-eval --json` exits 0 with verdict ∈ {PASS, WARN, FAIL}.
- **slo-architect** — `python3 scripts/error_budget_calculator.py --target 99.9 --window-days 30` exits 0 and prints 43.20 min allowed downtime (verified this audit); `slo_review.py` flags `target ≥ 99.99` docs.
- **spec-driven-workflow** — `python3 scripts/spec_validator.py --help` and `test_extractor.py --help` exit 0; Iron Law + bounded-autonomy STOP list retained.
- **sql-database-assistant** — `python3 scripts/query_optimizer.py --query "SELECT * FROM t" --dialect postgres` exits 0 with findings; dialect table retains all 4 engines.
- **tc-tracker** — `python3 scripts/tc_init.py --project T --root /tmp/tc-test && python3 scripts/tc_validator.py --registry /tmp/tc-test/docs/TC/tc_registry.json` both exit 0; state machine rejects `planned → deployed`.
- **agenthub** — `python3 scripts/hub_init.py --help`, `dag_analyzer.py --help`, `result_ranker.py --help` exit 0; all 7 `/hub:*` sub-skills name a script or Agent-tool call.
- **autoresearch-agent** — `python3 scripts/run_experiment.py --help` exits 0; evaluators intentionally fail `--help` (fixed contract) — add one sentence to SKILL.md documenting this; `setup_experiment.py --help` exits 0.
- **behuman** — Show/Quiet mode contract + 3 worked examples retained; token-cost table present. Register in marketplace or document why not.
- **caveman** — Matt's persistence + auto-clarity rules verbatim; `python3 scripts/caveman_lint.py "Sure! I'd be happy to help" ` flags filler.
- **code-tour** — schema block contains `$schema: https://aka.ms/codetour-schema`; validation checklist (verified line numbers, ≤2 content steps) intact.
- **data-quality-auditor** — `python3 scripts/data_profiler.py --help`, `missing_value_analyzer.py --help`, `outlier_detector.py --help` all exit 0; DQS weights sum to 100%.
- **demo-video** — fallback ladder (MCPs → manual build.sh) retained; output artifact list (scenes/, narration/, scenes.json, build.sh) unchanged.
- **docker-development** — `python3 scripts/dockerfile_analyzer.py --help` and `compose_validator.py --help` exit 0; 3 multi-stage patterns + base-image decision tree retained.
- **grill-me / grill-with-docs** — one-question-per-turn + recommended-answer rules verbatim; `python3 scripts/context_md_linter.py --help` (grill-with-docs) exits 0. Register grill-with-docs in marketplace.
- **handoff** — `mktemp` convention + no-duplication rule verbatim; 5 sections list unchanged.
- **helm-chart-builder** — `python3 scripts/chart_analyzer.py --help` exits 0; scaffold tree includes pdb.yaml + networkpolicy.yaml.
- **karpathy-coder** — `python3 scripts/complexity_checker.py --help` and `diff_surgeon.py --help` exit 0; 4 principles + relax conditions retained.
- **llm-cost-optimizer** — ROI-ordered 6 techniques with % ranges retained; proactive-flag table (max_tokens unset, >2k-token system prompt) intact; model-tier examples refreshed when model names rotate.
- **llm-wiki** — `python3 scripts/init_vault.py --help` and `lint_wiki.py --help` exit 0; Iron rule (never write raw/) retained; 8 references exist.
- **prompt-governance** — registry YAML schema + eval-type table retained; golden-dataset minimums (20/100+) intact.
- **security-guidance** — `echo '{}' | python3 hooks/security_reminder_hook.py` exits 0 (clean input); pattern table has all 12 rows; attribution block in plugin.json present.
- **statistical-analyst** — `python3 scripts/hypothesis_tester.py --test ztest --control-n 5000 --control-x 250 --treatment-n 5000 --treatment-x 310` exits 0 reporting +1.2pp (verified this audit); effect-size tables intact.
- **terraform-patterns** — `python3 scripts/tf_module_analyzer.py --help` and `tf_security_scanner.py --help` exit 0; review checklist (state, providers, security) retained.
- **workflow-builder** — `python3 scripts/validate_workflow.py --sample` and `workflow_intake.py --help` exit 0; hard-rules list (pure-literal meta, no Date.now, thunks) retained.
- **write-a-skill** — Matt's 3-phase flow + description requirements verbatim; `python3 scripts/skill_review_checklist_runner.py engineering/write-a-skill/skills/write-a-skill` exits 0.

## Agents

| Agent | Verdict | Issue |
|---|---|---|
| agenthub/hub-coordinator | KEEP | Strong: scoped tools allowlist/denylist, hard rules, re-spawn policy |
| autoresearch/experiment-runner | OPTIMIZE | No YAML frontmatter at all (no name/description/tools) — B1 fail; body is good |
| caveman/cs-caveman-mode | KEEP | — |
| claude-coach/cs-claude-coach | KEEP | — |
| grill-me/cs-grill-master | KEEP | Distinct voice + forcing-question pattern |
| grill-with-docs/cs-grill-with-docs | KEEP | — |
| handoff/cs-handoff-author | KEEP | Hard refusals make persona behavioral, not adjectival |
| karpathy-coder/karpathy-reviewer | KEEP | Model exemplar: tool allow/deny lists, exact workflow, report shape |
| llm-wiki/wiki-ingestor | KEEP | — |
| llm-wiki/wiki-librarian | KEEP | — |
| llm-wiki/wiki-linter | KEEP | — |
| universal-scraping-architect/cs-scraping-architect | REWRITE | 6-line placeholder: no tools, no triggers, no workflow — B1/B2/B3 fail |
| workflow-builder/cs-workflow-architect | KEEP | — |
| write-a-skill/cs-skill-author | KEEP | — |

## Commands

| Command | Verdict | Issue |
|---|---|---|
| caveman/cs-caveman | KEEP | Enforces persistence + auto-clarity; wires 3 scripts |
| claude-coach/cs-claude-coach | KEEP | Handles $ARGUMENTS, fixed activation sequence |
| grill-me/cs-grill-me | KEEP | — |
| grill-with-docs/cs-grill-with-docs | KEEP | — |
| handoff/cs-handoff | KEEP | — |
| karpathy-coder/karpathy-check | KEEP | Orchestrates 2 scripts + sub-agent — earns its slot |
| llm-wiki/wiki-init | KEEP | — |
| llm-wiki/wiki-ingest | KEEP | — |
| llm-wiki/wiki-query | KEEP | — |
| llm-wiki/wiki-lint | KEEP | — |
| llm-wiki/wiki-log | KEEP | — |
| universal-scraping-architect/cs-scrape | CUT-OR-MERGE | 6-line placeholder; a bare prompt does strictly more — C3 fail; no $ARGUMENTS handling |
| workflow-builder/cs-workflow-build | KEEP | — |
| write-a-skill/cs-write-a-skill | KEEP | — |

Note: agenthub's 7 `/hub:*` and autoresearch's 5 `/ar:*` surfaces ship as command-style sub-skills (frontmatter `command:` key) rather than `commands/*.md` files — all are substantive and wired; counted under their parent skill verdicts.

## Plugin manifests

1. **engineering-advanced-skills (engineering/.claude-plugin/plugin.json + marketplace.json:227)** — description claims skills not shipped by the manifest: llm-cost-optimizer, prompt-governance, behuman, code-tour, demo-video, data-quality-auditor, statistical-analyst, llm-wiki live in standalone plugin folders, while `"skills": ["./skills"]` only packages `engineering/skills/` (40 dirs). E2 fail.
2. **Triple count mismatch** — bundle index SKILL.md "25 skills" vs plugin description "40" vs 39 actual skills + 1 index dir.
3. **Five orphan plugins** — behuman, claude-coach, grill-with-docs, llm-cost-optimizer, prompt-governance have valid `.claude-plugin/plugin.json` but no marketplace.json entry (handoff is registered as `handoff-engineering`; these five aren't registered at all).
4. **Dual-published duplicates** — slo-architect, chaos-engineering, kubernetes-operator, feature-flags-architect exist byte-identical in two paths; only the standalone copies are marketplace-registered, but the bundle copies also ship via engineering-advanced-skills → users installing both get duplicates with identical trigger descriptions.
5. **Version coherence** — workflow-builder plugin.json is `1.0.0` while every sibling is `2.9.0` (marketplace itself is at v2.10.x per root CLAUDE.md — domain-wide version lag is cosmetic but uniform).
