# Domain audit: product-team/ + project-management/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 26 (17 product-team + 9 project-management) · Agents: 6 · Commands: 11 · Plugins: 6 (+1 .mcp.json)

## Scorecard

| Skill | Verdict | Top issue |
|---|---|---|
| product-team/skills/product-skills (router) | CUT-OR-MERGE | 61-line index with broken `/read` paths and stale counts; adds no orchestration |
| product-team/skills/product-manager-toolkit | OPTIMIZE | Two contradictory RICE CSV schemas in one file; ~120 lines of generic PM advice |
| product-team/agile-product-owner | KEEP | — |
| product-team/skills/product-strategist | OPTIMIZE | Generator emits canned OKR prose a frontier model writes better; keep the alignment scorer |
| product-team/skills/ux-researcher-designer | KEEP | — |
| product-team/skills/ui-design-system | KEEP | — |
| product-team/skills/competitive-teardown | OPTIMIZE | Its only script (competitive_matrix_builder.py) is never referenced in SKILL.md |
| product-team/skills/landing-page-generator | OPTIMIZE | Own script + all 4 references orphaned; overlaps marketing/landing |
| product-team/skills/saas-scaffolder | OPTIMIZE | project_bootstrapper.py orphaned; stack pins aging (Next.js 14, NextAuth v4) |
| product-team/skills/product-analytics | KEEP | — |
| product-team/skills/experiment-designer | KEEP | — |
| product-team/skills/product-discovery | KEEP | — |
| product-team/skills/roadmap-communicator | OPTIMIZE | Mostly framework-explainer prose; value is the changelog tool + templates |
| product-team/skills/spec-to-repo | KEEP | — |
| product-team/code-to-prd | OPTIMIZE | Malformed frontmatter (duplicate `Name:`/`name:` + non-standard keys) |
| product-team/research-summarizer | CUT-OR-MERGE | Duplicates research/ domain (litreview/dossier); phantom `/research:*` commands |
| product-team/apple-hig-expert | REWRITE | Known 3/6; persona filler, no exact CLI, citation-free references with dubious claims |
| project-management/skills/pm-skills (router) | CUT-OR-MERGE | Thin index; broken paths; says 6 skills, domain has 9 |
| project-management/skills/senior-pm | OPTIMIZE | Strong quant core buried in ~150 lines of governance boilerplate; invented KPI targets |
| project-management/skills/scrum-master | KEEP | — |
| project-management/skills/jira-expert | REWRITE | Fabricated MCP syntax (`mcp jira create_project --flags`) naming tools the bundled server doesn't have |
| project-management/skills/confluence-expert | REWRITE | Fabricated MCP tool names + phantom MACROS.md/PERMISSIONS.md + legacy wiki markup for Cloud |
| project-management/skills/atlassian-admin | OPTIMIZE | Factual errors (DELETE /rest/api/3/user ≠ deactivate; "7 years for GDPR"); script orphaned |
| project-management/skills/atlassian-templates | REWRITE | Claims "exact parameter names expected by the Atlassian MCP server" for tools that don't exist |
| project-management/skills/meeting-analyzer | KEEP | — |
| project-management/skills/team-communications | KEEP | — |

**Totals:** KEEP 10 · OPTIMIZE 9 · REWRITE 4 · CUT-OR-MERGE 3

## Domain-level findings

1. **MCP wiring is fiction in 3 of the 4 Atlassian skills (highest-severity finding).** The bundled `.mcp.json` correctly points to the Atlassian Remote MCP (`https://mcp.atlassian.com/v1/sse`, SSE), whose real tools are camelCase: `createJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `transitionJiraIssue`, `createConfluencePage`, `updateConfluencePage`, `searchConfluenceUsingCql`, etc. The skills document three different *invented* conventions, none matching: jira-expert uses CLI-flag pseudo-syntax (`mcp jira create_project --name ... --type scrum`), confluence-expert uses snake_case JS calls (`create_space({...})`, `delete_page`, `add_label`), atlassian-templates uses JSON tool blocks (`confluence_create_page`, `jira_update_field_configuration`) while asserting these are "the exact parameter names expected by the Atlassian MCP server." Several referenced capabilities (`create_project`, `create_sprint`, `create_filter`, `create_space`, field-configuration editing) do not exist on the Remote MCP at all. `project-management/CLAUDE.md` adds a fourth convention (`mcp__atlassian__create_issue`, `mcp__atlassian__create_sprint`, `mcp__atlassian__link_issue`). A new-gen model following any of these will emit failing tool calls.
2. **8 orphaned scripts (A3 systemic).** Script dirs exist but SKILL.md never invokes them: competitive-teardown, landing-page-generator, saas-scaffolder, atlassian-admin (1 each); jira-expert, confluence-expert (2 each); atlassian-templates (1). The repo-wide smoke test passes them (D1 fine) but no workflow consumes their output — dead weight per the rubric.
3. **Stale path layout in agents, commands, and routers.** Skills moved under `*/skills/` subdirs but `agents/product/*` reference `../../product-team/product-manager-toolkit/`, commands reference `project-management/scrum-master/SKILL.md`, and both router skills instruct `/read product-team/product-manager-toolkit/SKILL.md`. All resolve to nothing.
4. **Count drift everywhere.** product-skills plugin.json: "13 production-ready product skills" then lists 16 names. product-skills SKILL.md: "10" in description, "8" in body, 13 on disk. pm-skills: 9 in marketplace, 6 in plugin description and SKILL.md, 9 on disk. project-management/CLAUDE.md claims 9 skills but documents only 6 — meeting-analyzer and team-communications (two of the three best skills in the domain) are invisible to it.
5. **PM references are citation-free**, consistent with the repo-wide flag: jql-examples.md (0 sources), team-dynamics-framework.md (0), governance-framework.md (0), template-design-patterns.md (0), retro-formats.md (1). Only senior-pm's prioritization/risk references cite anything.
6. **Generic-knowledge dead weight (A2).** "Handoff Protocols", "Best Practices", "Common Pitfalls" sections across senior-pm, jira-expert, confluence-expert, product-manager-toolkit, roadmap-communicator restate what a frontier model already knows. The skills that skip this (product-analytics, experiment-designer, meeting-analyzer, scrum-master) are the domain's best.

## Per-skill findings

### product-team/skills/product-skills — CUT-OR-MERGE
- Issues: (1) Pure index page — no routing logic, no classifier, nothing a model can execute. (2) Quick Start path `/read product-team/product-manager-toolkit/SKILL.md` is wrong (missing `skills/`). (3) Description says 10 skills, body table lists 8, directory holds 13. (4) Duplicates product-team/CLAUDE.md content.
- Verify: `grep -c "product-team/skills/" product-team/skills/product-skills/SKILL.md` ≥ 1 if retained; otherwise plugin.json `"skills"` array still validates via `python3 scripts/check_plugin_json.py --all` after removal.

### product-team/skills/product-manager-toolkit — OPTIMIZE
- Issues: (1) Two incompatible RICE CSV schemas shown — Quick Start (`feature,reach,impact,confidence,effort` numeric) vs Tools Reference (`name,reach,impact,confidence,effort,description` with `high`/`massive`/`l` categorical values); only one can match the script's parser. (2) ~120 lines of generic PM advice (Best Practices, Pitfalls tables) a frontier model already knows. (3) Verification loop is checklist-only — no machine-checkable gate.
- Verify: `python3 scripts/rice_prioritizer.py sample && python3 scripts/rice_prioritizer.py sample_features.csv --output json` exits 0 and emits JSON with per-feature `rice_score`; the single canonical CSV header in SKILL.md matches `sample_features.csv` byte-for-byte; `python3 scripts/customer_interview_analyzer.py <file> json` exits 0 emitting `pain_points` key.

### product-team/skills/product-strategist — OPTIMIZE
- Issues: (1) Generator output is canned objective prose ("Build viral product features...") — new-gen models write better OKRs unaided; the durable value is the 4-score alignment math (vertical/horizontal/coverage/balance) and thresholds. (2) Sample output hardcodes "Q1 2025" (A6 minor). (3) No verification loop beyond a checklist.
- Verify: `python3 scripts/okr_cascade_generator.py growth --json | python3 -c "import json,sys; d=json.load(sys.stdin); assert d['alignment_scores']['overall']>0"` exits 0; thresholds table (>90/>75/>80/>80) still present in SKILL.md after trimming.

### product-team/skills/competitive-teardown — OPTIMIZE
- Issues: (1) `scripts/competitive_matrix_builder.py` exists but is never mentioned — the 12-dimension rubric is manual-only. (2) Step 4 templates live in `references/analysis-templates.md`; the workflow never says when to load it vs the inline summary (mild progressive-disclosure confusion). (3) No final verification gate after step 6.
- Verify: `python3 scripts/competitive_matrix_builder.py --help` exits 0 AND SKILL.md contains an exact `python3 scripts/competitive_matrix_builder.py` invocation whose output feeds step 3 (scorecard); validation checkpoint at step 2 (pricing + ≥20 reviews + job counts) retained.

### product-team/skills/landing-page-generator — OPTIMIZE
- Issues: (1) `scripts/landing_page_scaffolder.py` (the tool product-team/CLAUDE.md advertises for this skill) is never referenced — only marketing-skill's brand_voice_analyzer is. (2) All 4 reference files (conversion-patterns, copy-frameworks, landing-page-patterns, seo-checklist) unreferenced. (3) Functional overlap with `marketing/landing` (v2.7.0) — needs an explicit distinct-from note (TSX/Next.js vs single-file HTML). (4) SEO "validation step" is honor-system, no executable check.
- Verify: `python3 scripts/landing_page_scaffolder.py --help` exits 0 and SKILL.md shows `--format tsx|html` invocation consumed by the generation workflow; a "distinct from marketing/landing" sentence exists; all 4 reference files cited or deleted.

### product-team/skills/saas-scaffolder — OPTIMIZE
- Issues: (1) `scripts/project_bootstrapper.py` orphaned — phase checklist never calls it. (2) Freshness: NextAuth v4 patterns (`NextAuthOptions`, `getServerSession`) and "Next.js 14+" pins will mislead in 2026 (Auth.js v5 / Next 15 era). (3) Reference Files section asks the model to *generate* CUSTOMIZATION.md/PITFALLS.md/BEST_PRACTICES.md rather than shipping them (A7 — shells).
- Verify: `python3 scripts/project_bootstrapper.py --help` exits 0 and is invoked in Phase 1 of the checklist; Phase 4 webhook idempotency validation retained; stack-version claims dated or generalized.

### product-team/skills/roadmap-communicator — OPTIMIZE
- Issues: (1) ~70% of body is audience-framing advice a frontier model knows (board = outcomes, engineers = dependencies). (2) Only real asset is `changelog_generator.py` + two template references; quality checklist is non-executable. (3) No JSON-mode mention despite the script supporting `--json` (per CLAUDE.md).
- Verify: from a git repo, `python3 scripts/changelog_generator.py --from <tag> --to HEAD --json` exits 0 emitting grouped conventional-commit entries; both `references/roadmap-templates.md` and `references/communication-templates.md` load (exist, non-empty).

### product-team/code-to-prd — OPTIMIZE
- Issues: (1) Frontmatter contains duplicate keys (`Name:` and `name:`) plus non-standard `Tier/Category/Dependencies/Author/Version` at top level — fragile under strict YAML parsers and fails the repo's own description conventions. (2) 507 lines; the README/per-page templates could move to `references/` (progressive disclosure). (3) Otherwise the strongest large skill in the domain (mock-detection signals, enum exhaustiveness, [TBC] uncertainty rule).
- Verify: `python3 -c "import yaml; yaml.safe_load(open('SKILL.md').read().split('---')[1])"` parses with exactly one `name` key; `python3 scripts/codebase_analyzer.py <dir> -o analysis.json && python3 scripts/prd_scaffolder.py analysis.json -o /tmp/prd` exits 0 producing `prd/README.md`.

### product-team/research-summarizer — CUT-OR-MERGE
- Issues: (1) Core capability (structured summarization) is native frontier-model behavior; wrapper value is one regex citation extractor. (2) Direct overlap with `research/litreview`, `research/dossier`, `research/notebooklm` (v2.7.0) — no disambiguation anywhere. (3) Advertises `/research:summarize|compare|cite` slash commands that exist nowhere in `commands/` (phantom). (4) `format_summary.py` emits empty templates — a template printer, not analysis. (5) Installation section references `./scripts/convert.sh` not shipped with the skill.
- Verify: if retained, `grep -r "research:summarize" commands/` returns ≥1 file or the Slash Commands section is removed; a "distinct from research/litreview" note exists; `python3 scripts/extract_citations.py <file> --output json` exits 0 with deduplicated entries.

### product-team/apple-hig-expert — REWRITE
- Issues: (1) Confirmed 3/6 on repo checklist: description has no "Use when" trigger phrases; "You are a Senior Apple Design Lead with decades of experience" is exactly the A2 filler the rubric bans; zero concrete examples (no sample audit, no before/after). (2) A3 fail: "Run the `hig_checker.py` tool" with no invocation — actual CLI is `hig_checker.py {contrast,target,batch}` with subcommand args the SKILL.md never shows. (3) References cite zero sources (no developer.apple.com links) and contain unverifiable claims ("SF Camera" as a public SF variant; "Liquid Glass introduced in late 2025" — WWDC25 was June 2025) — for a freshness-critical Apple skill this is fatal. (4) 90 lines of pointers with the actual expertise missing: no Liquid Glass API names (`glassEffect`, materials hierarchy), no per-platform metric tables in SKILL.md. (5) Scorecard "0-100" output promised with no rubric to compute it.
- Verify: `python3 scripts/hig_checker.py contrast --help && python3 scripts/hig_checker.py batch --help` exit 0 and both invocations appear verbatim in SKILL.md; description matches `Use when` trigger regex of `scripts/audit_skills.py` (skill scores ≥5/6 on `skill_review_checklist_runner.py`); every reference doc cites ≥3 developer.apple.com URLs; at least one worked audit example (input mockup description → scored findings) present.

### project-management/skills/pm-skills — CUT-OR-MERGE
- Issues: (1) Index-only router; `/read project-management/jira-expert/SKILL.md` path wrong (missing `skills/`). (2) Claims 6 skills; domain ships 9 — meeting-analyzer, team-communications invisible. (3) Example tool paths (`senior-pm/scripts/...`) also missing the `skills/` segment.
- Verify: every path in the file resolves (`while read p; do test -e "$p"; done`) or the file is removed and pm-skills plugin.json still passes `check_plugin_json.py --all`.

### project-management/skills/senior-pm — OPTIMIZE
- Issues: (1) ~150 lines of Handoff Protocols / Continuous Improvement / Stakeholder Feedback boilerplate (A2 dead weight). (2) Success-metric targets (">70% risk prediction accuracy", "10% transformational") presented with no source or basis (A5 weakness). (3) Description promises "Monte Carlo simulation" — confirm `risk_matrix_analyzer.py` actually simulates rather than just the formula snippets shown. (4) Quant core (EMV, category weights, three-point estimation, response thresholds >18/12-18/8-12/<8, STOP gates) is genuinely good — keep all of it.
- Verify: all three scripts run against `assets/sample_project_data.json` exiting 0; `project_health_dashboard.py ... --format json` emits composite score + RAG consistent with the >80/60-80/<60 thresholds documented; if Monte Carlo isn't in the scripts, the claim is removed from the description.

### project-management/skills/jira-expert — REWRITE
- Issues: (1) Every "MCP" example uses invented CLI syntax (`mcp jira create_project --name "My Project" --type scrum`) — not MCP, not the bundled server. Real server: `createJiraIssue`, `searchJiraIssuesUsingJql`, `editJiraIssue`, `transitionJiraIssue`; it has NO project/sprint/filter creation. (2) Both scripts (`jql_query_builder.py`, `workflow_validator.py` — which work and produce useful JQL) are never mentioned. (3) `--startDate "2024-06-01"` 2024-ism (A6). (4) JQL operator/function content is generic knowledge a frontier model has; the JQL examples references cite 0 sources. (5) Verdict REWRITE not CUT: the JQL recipes + escalation framework + the two scripts are a salvageable core.
- Verify: every MCP call in SKILL.md names a tool that exists on the Atlassian Remote MCP (assert each appears in the server's tool list; non-existent operations rewritten as REST-API or UI steps); `python3 scripts/jql_query_builder.py "high priority bugs assigned to me"` exits 0 emitting valid JQL and is wired into the JQL workflow; no pre-2026 literal dates.

### project-management/skills/confluence-expert — REWRITE
- Issues: (1) MCP examples (`create_space`, `update_page`, `delete_page`, `get_children`, `add_label`) don't match the real server (`createConfluencePage`, `updateConfluencePage`, `getConfluencePage`, `getConfluencePageDescendants`, `searchConfluenceUsingCql`; no space-creation/delete/label tools). (2) Phantom references: cites `MACROS.md`, `TEMPLATES.md`, `PERMISSIONS.md` — actual files are `macro-cheat-sheet.md`, `templates.md`, `space-architecture-patterns.md`; PERMISSIONS.md doesn't exist at all. (3) Macro sections teach legacy wiki markup (`{info}`, `{section}{column}`) which Confluence Cloud pages (what the MCP writes, storage-format XHTML/ADF) won't accept. (4) Scripts (`space_structure_generator.py`, `content_audit_analyzer.py`) orphaned. (5) Long generic sections (governance, handoffs) a model already knows.
- Verify: every file path cited in SKILL.md exists (`grep -oE '[A-Za-z-]+\.md' SKILL.md` all resolve under references/); every MCP example names a real Remote-MCP tool; macro examples shown in storage format with a note on wiki-markup legacy; both scripts invoked with exact CLI and outputs consumed by Space Creation / KB audit workflows.

### project-management/skills/atlassian-admin — OPTIMIZE
- Issues: (1) Factual errors: `DELETE /rest/api/3/user` deletes (org-admin deactivation is a different endpoint) yet documented as "Deactivate"; "minimum 7 years for SOC 2/GDPR compliance" is invented — GDPR mandates no such retention and pushes minimization. (2) `permission_audit_tool.py` orphaned. (3) Strength: admin.atlassian.com click-paths and REST endpoints are real specificity (A5 pass) — admin operations aren't covered by the Remote MCP, so the "Atlassian MCP Integration" closing section over-promises and should be cut or scoped. (4) References dir exists but is never pointed to from the workflows.
- Verify: `python3 scripts/permission_audit_tool.py --help` exits 0 and an exact invocation appears in the Permission Scheme Design workflow; deactivation step cites the org API (`POST /admin/v1/orgs/{orgId}/directory/users/{accountId}/suspend-access`) or the console path only; retention claim sourced or deleted.

### project-management/skills/atlassian-templates — REWRITE
- Issues: (1) States "All MCP calls below use the exact parameter names expected by the Atlassian MCP server" — then lists `confluence_create_page`, `confluence_update_page`, `confluence_get_page`, `jira_update_field_configuration`, none of which exist (real: `createConfluencePage`/`updateConfluencePage`/`getConfluencePage`; no field-configuration tool at all). False precision is worse than vagueness. (2) Phantom references: `TEMPLATES.md` and `HANDOFFS.md` cited; actual files are `governance-framework.md`, `template-design-patterns.md`. (3) Conflates "Confluence storage format (wiki markup)" — storage format is XHTML, wiki markup is a different legacy syntax; the example is wiki markup and will not round-trip through the Cloud API. (4) `template_scaffolder.py` (which generates storage-format XHTML per CLAUDE.md — the actually-correct artifact) is never mentioned.
- Verify: `python3 scripts/template_scaffolder.py meeting-notes` exits 0 emitting storage-format XHTML and is the documented deployment path; every MCP tool named in SKILL.md exists on the Remote MCP; cited reference filenames resolve on disk; "storage format" vs "wiki markup" used correctly throughout.

## KEEP-verdict verification criteria

- **agile-product-owner**: AC-count-by-points table (1-2→3-4 … 13+→split) and availability-factor table intact; `python3 scripts/user_story_generator.py sprint 30` exits 0 emitting committed ≤85% of capacity; weighted prioritization (40/30/15/15) unchanged.
- **ux-researcher-designer**: `python3 scripts/persona_generator.py json` exits 0 with `confidence` field; sample-size confidence table (5-10 low / 11-30 med / 31+ high) and severity 1-4 table retained.
- **ui-design-system**: `python3 scripts/design_token_generator.py "#0066CC" modern json` exits 0 emitting color/typography/spacing token groups; WCAG AA thresholds (4.5:1 / 3:1) stated in Workflow 1 step 5.
- **product-analytics**: all three subcommands (`retention`, `cohort`, `funnel`) run against documented CSV headers with `--format json` exiting 0; anti-pattern table (6 rows) retained.
- **experiment-designer**: `python3 scripts/sample_size_calculator.py --baseline-rate 0.12 --mde 0.02 --mde-type absolute` exits 0 printing `n_per_group`/`n_total`; If/Then/Because hypothesis gate and peeking warning retained.
- **product-discovery**: `python3 scripts/assumption_mapper.py <csv>` exits 0 emitting prioritized test plan; OST quality gates (≥3 opportunities, ≥2 experiments/opportunity) retained.
- **spec-to-repo**: `python3 scripts/validate_project.py <dir> --format json` exits 0; Phase 4 checklist wired to the script; anti-pattern table (9 rows incl. phantom-imports) retained.
- **scrum-master**: all 3 scripts run on `assets/sample_sprint_data.json` matching `assets/expected_output.json` anchors (velocity avg ≈20.2, CV ≈12.7%, health ≈78.3); <3-sprint refusal gate fires on truncated input.
- **meeting-analyzer**: calibrated thresholds preserved (filler >3/100 words, speaking share >60%, interruption >2:1, 3+ meetings for trends); no script claims introduced without scripts existing.
- **team-communications**: all 4 routing targets (`references/3p-updates.md` etc.) exist and load; ambiguity rule ("ask one clarifying question") retained.

## Agents

6 agents (5 product + 1 PM), all `model: sonnet`, all `tools: [Read, Write, Bash, Grep, Glob]`.

- **B1 partial fail (all 6):** descriptions state capability but no trigger phrasing ("Use when…" / "Use PROACTIVELY") — they read like catalog blurbs.
- **Stale skill paths (all 6):** `skills:` values and body paths (`../../product-team/product-manager-toolkit/`, `../../project-management/senior-pm/scripts/...`) predate the `skills/` subdirectory move; none resolve. cs-project-manager's `skills: project-management` is the only one that survives by accident (directory-level).
- **B2 weak:** cs-product-manager orchestrates all 8 legacy skills (incl. landing-page + saas-scaffolder — scope sprawl into build work); cs-product-strategist and cs-product-manager bodies are interchangeable catalog tables, not differentiated behavior. cs-product-analyst is the cleanest (2 skills, focused).
- Verify: every path in each agent file resolves from `agents/<domain>/`; each description gains a trigger clause; cs-product-manager skill list trimmed to PM-decision skills.

## Commands

11 in scope: /rice, /okr, /persona, /user-story, /competitive-matrix, /prd, /sprint-plan, /code-to-prd (product); /sprint-health, /project-health, /retro (PM).

- **C1 pass** all 11 (frontmatter description present, usage string embedded).
- **C3 strong:** /sprint-health, /project-health, /retro, /code-to-prd — wire exact scripts with input schemas and JSON examples. Keep.
- **C3 weak:** /prd and /sprint-plan are thin prompt wrappers (output-structure bullets a bare prompt produces) — merge candidates into /rice and /user-story or beef up with script gates.
- **Stale skill-reference paths (all that cite SKILL.md):** `project-management/scrum-master/SKILL.md`, `product-team/product-manager-toolkit/SKILL.md` etc. all miss the `skills/` segment.
- **Mismatch:** /retro and /sprint-health input JSON schemas (flat per-sprint objects) don't match the scripts' actual schema (`team_info` + `sprints[]` + `retrospectives[]` per scrum-master SKILL.md) — a model following the command's example will feed the script malformed input. Verify: run each command's documented example JSON through its script; exit 0 required.

## Plugin manifests + MCP wiring

- **E1 pass:** all 6 plugin.json files schema-valid (`"skills": ["./skills"]` / `["./skills"]` canonical forms); repo-wide `check_plugin_json.py --all` green.
- **E2 fail — count/description drift:** product-skills plugin.json says "13 production-ready product skills" then enumerates 16 (incl. code-to-prd, research-summarizer, apple-hig-expert, spec-to-repo — three of which are *separate* plugins, so the description oversells what `./skills` ships). pm-skills plugin description lists 6 skills; marketplace.json says 9; disk has 9 (meeting-analyzer + team-communications + router undocumented). product-team/CLAUDE.md header says 13, lists 16, footer says "13/13". project-management/CLAUDE.md says 9, documents 6.
- **E3 pass:** all at 2.9.0, coherent with marketplace.json.
- **.mcp.json:** correct and minimal (`atlassian` → SSE `https://mcp.atlassian.com/v1/sse`). This is the only accurate piece of MCP wiring in the domain.
- **MCP documentation contradiction (cross-cutting):** four different fabricated tool-naming conventions across project-management/CLAUDE.md (`mcp__atlassian__create_issue`, `create_sprint`, `link_issue`), jira-expert (CLI flags), confluence-expert (snake_case JS), atlassian-templates (JSON blocks) — zero match the live Remote MCP surface (`createJiraIssue`, `editJiraIssue`, `searchJiraIssuesUsingJql`, `getJiraIssue`, `transitionJiraIssue`, `createConfluencePage`, `updateConfluencePage`, `getConfluencePage`, `searchConfluenceUsingCql`, `getConfluenceSpaces`, …). One canonical tool-name appendix should be written once and referenced from all four places. Verify: `grep -rE "mcp jira |mcp__atlassian__[a-z_]+|confluence_create_page|create_space\(" project-management/` returns 0 hits after fix.
