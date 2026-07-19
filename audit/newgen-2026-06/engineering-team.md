# Domain audit: engineering-team/ — new-gen model optimization
Audited: 2026-06-10 · Skills: 51 · Agents: 5 · Commands: 0 · Plugins: 6

## Scorecard
| Skill | Verdict | Top issue |
|---|---|---|
| skills/adversarial-reviewer | KEEP | — |
| skills/ai-security | KEEP | — |
| skills/aws-solution-architect | KEEP | cost figures unverified (minor A6) |
| skills/azure-cloud-architect | KEEP | Bicep API versions pinned to 2023 (minor A6) |
| skills/cloud-security | KEEP | — |
| skills/code-reviewer | KEEP | — |
| skills/email-template-builder | OPTIMIZE | 439-line code dump, zero scripts/references (A3, A7) |
| skills/engineering-skills | OPTIMIZE | index skill claims "23 skills" — actual 32; weak as a skill |
| skills/epic-design | KEEP | "You are a world-class expert" filler (minor A2) |
| skills/gcp-cloud-architect | KEEP | — |
| skills/incident-commander | OPTIMIZE | 3 orphan duplicate scripts; SEV taxonomy duplicates incident-response |
| skills/incident-response | KEEP | — |
| skills/ms365-tenant-manager | OPTIMIZE | 3 scripts exist but never referenced in SKILL.md (A3) |
| skills/red-team | KEEP | — |
| skills/security-pen-testing | KEEP | — |
| skills/senior-architect | OPTIMIZE | generic monolith-vs-microservices prose; no verification loop |
| skills/senior-backend | OPTIMIZE | corrupted code snippet (`name: "zstringmin1max100"`) |
| skills/senior-computer-vision | KEEP | — |
| skills/senior-data-engineer | OPTIMIZE | thin body; generic batch-vs-streaming tables (A2) |
| skills/senior-data-scientist | OPTIMIZE | phantom scripts referenced; real 3 scripts orphaned (A3 hard fail) |
| skills/senior-devops | KEEP | — |
| skills/senior-frontend | OPTIMIZE | corrupted snippet (`"cdnexamplecom"`); mid-file generic React dump |
| skills/senior-fullstack | KEEP | — |
| skills/senior-ml-engineer | OPTIMIZE | GPT-4/GPT-3.5/Claude 3 Opus pricing tables (A6 fail) |
| skills/senior-prompt-engineer | REWRITE | entire skill is GPT-4-era prompt engineering; stale models hardcoded in scripts |
| skills/senior-qa | OPTIMIZE | 2 corrupted code snippets; generic RTL cheatsheet content |
| skills/senior-secops | KEEP | trim BAD/GOOD security basics (minor A2) |
| skills/senior-security | CUT-OR-MERGE | duplicates senior-secops/pen-testing/incident-response; no exact CLI for its 2 scripts |
| skills/stripe-integration-expert | OPTIMIZE | pinned `apiVersion: "2024-04-10"`; pure code dump, no tools |
| skills/tdd-guide | KEEP | — |
| skills/tech-stack-evaluator | OPTIMIZE | "ecosystem health from GitHub/npm metrics" is offline static data — staleness unlabeled |
| skills/threat-detection | KEEP | — |
| a11y-audit/skills/a11y-audit | KEEP | — |
| google-workspace-cli/skills/google-workspace-cli | REWRITE | install coordinates almost certainly fabricated (`npm i -g @anthropic/gws`, `github.com/googleworkspace/cli`) |
| snowflake-development/skills/snowflake-development | KEEP | — |
| playwright-pro/skills/pw | KEEP | — |
| playwright-pro/skills/init | KEEP | — |
| playwright-pro/skills/generate | KEEP | — |
| playwright-pro/skills/review | KEEP | — |
| playwright-pro/skills/fix | KEEP | — |
| playwright-pro/skills/migrate | KEEP | — |
| playwright-pro/skills/coverage | KEEP | — |
| playwright-pro/skills/report | KEEP | — |
| playwright-pro/skills/testrail | KEEP | — |
| playwright-pro/skills/browserstack | KEEP | — |
| self-improving-agent/skills/self-improving-agent | KEEP | — |
| self-improving-agent/skills/review | KEEP | — |
| self-improving-agent/skills/promote | KEEP | — |
| self-improving-agent/skills/extract | KEEP | — |
| self-improving-agent/skills/remember | KEEP | — |
| self-improving-agent/skills/status | KEEP | — |

**Totals: KEEP 35 · OPTIMIZE 13 · REWRITE 2 · CUT-OR-MERGE 1**

## Domain-level findings

1. **Bulk-edit code corruption (systemic, 4 confirmed sites).** A past YAML/quoting sweep mangled string literals inside code blocks: `senior-qa/SKILL.md:123` (`name: "click-mei-tobeinthedocument"` — was `getByRole('button', { name: /click me/i })` + `toBeInTheDocument()`), `senior-qa:244` (`"submiti"`), `senior-backend:253` (`name: "zstringmin1max100"` — was `z.string().min(1).max(100)`), `senior-frontend:425` (`hostname: "cdnexamplecom"` — dots stripped). Any model copying these examples emits broken code. Grep pattern to find more: strings that are concatenated identifiers with punctuation stripped.
2. **Stale LLM-era content concentrated in 2 skills + their scripts.** senior-prompt-engineer and senior-ml-engineer present GPT-4/GPT-3.5/Claude 3 Opus model names, 8K context windows, and 2024 pricing as current — in SKILL.md, references (`llm_integration_guide.md`), and hardcoded in scripts (`prompt_optimizer.py` MODEL choices/prices, `agent_orchestrator.py` cost tables). A6 fail across the whole package, not just prose.
3. **Two generations of skills coexist.** The 2026-upgraded trio (senior-fullstack/frontend/backend: decision engines, profiles, forcing questions, composition maps, kill criteria) and the v2.2 security suite (ai-security, threat-detection, incident-response, cloud-security, red-team: exit-code contracts, ATT&CK/ATLAS mapping, anti-patterns) are the new-gen template. The 2025-era role skills (architect, data-scientist, data-engineer, prompt-engineer, qa) still carry "cheatsheet" bodies — generic tables (HTTP status codes, RTL queries, zero-shot vs few-shot) that a frontier model embodies and that cost context for nothing.
4. **Security skill sprawl with duplicated incident-response content.** Four skills carry SEV1-SEV4 frameworks + IR phase checklists (senior-secops, senior-security, incident-response, incident-commander), and OWASP Top 10 appears in 4 places. The v2.2 suite has explicit "this is NOT X" disambiguation tables; the older senior-security does not and is ~80% subsumed.
5. **Orphan/phantom script wiring (A3).** senior-data-scientist references `scripts/train.py`/`evaluate.py`/`health_check.py` (don't exist) while its 3 real scripts go unmentioned; ms365-tenant-manager never references its 3 scripts; incident-commander ships 6 scripts but wires only 3 (`severity_classifier.py`, `incident_timeline_builder.py`, `postmortem_generator.py` are duplicates of the wired ones).
6. **Count drift everywhere.** README says 18 skills, START_HERE says 14, engineering-skills SKILL.md says 23, plugin.json says 32, root CLAUDE.md says 51. engineering-team/CLAUDE.md documents 7 scripts that don't exist under those names (`fullstack_scaffolder.py`, `statistical_analyzer.py`, `etl_generator.py`, `mlops_setup_tool.py`, `llm_integration_builder.py`, `rag_system_builder.py` under prompt-engineer, `video_processor.py`).
7. **18 stale .zip archives at domain root** (senior-*.zip, code-reviewer.zip, etc.) — dead weight shipped to every cloner; almost certainly out of sync with the live folders.
8. **Unverifiable external-tool provenance.** google-workspace-cli teaches a `gws` CLI installed via `npm install -g @anthropic/gws` (not an Anthropic package) with releases at `github.com/googleworkspace/cli` (not a real repo). If the CLI doesn't exist under these coordinates, the entire 373-line skill + 43 recipes is unusable.
9. **Bright spots worth templating:** playwright-pro sub-skills end every workflow with an executable gate ("run `--repeat-each=10`, all 10 must pass"); code-reviewer ships regression fixtures with committed expected `--json` outputs; the security suite's exit-code contracts (0/1/2 with required action) are exactly the A4 pattern the rubric wants.

## Per-skill findings

### engineering-team/skills/senior-prompt-engineer
Verdict: REWRITE
Issues:
- A6 hard fail: GPT-4 cost estimates in sample output (line 57), `--model gpt-4` examples (line 72); `prompt_optimizer.py` restricts `--model` to gpt-4/gpt-3.5-turbo/claude-3-* with 2024 prices; `agent_orchestrator.py` defaults to `model: gpt-4` with stale cost table.
- A2: zero-shot/few-shot/CoT/role-prompting tables and "add format enforcement" guidance are 2023-era basics a frontier model embodies.
- A5 gap: nothing on current practice — structured outputs/tool-use APIs, prompt caching, eval-driven iteration, agent context engineering.
- No verification loop beyond "run both prompts against your eval set" (manual).
Verify (definition of done):
- `grep -rE "gpt-4|gpt-3\.5|claude-3-" skills/senior-prompt-engineer/` returns 0 hits.
- `python3 scripts/prompt_optimizer.py /tmp/p.txt --analyze` exits 0 and model list contains only current-generation model IDs (or is model-agnostic).
- SKILL.md workflow ends with an executable eval gate (script run + exit-code assertion), not "compare outputs".

### engineering-team/google-workspace-cli/skills/google-workspace-cli
Verdict: REWRITE
Issues:
- Install section points to `npm install -g @anthropic/gws` and `github.com/googleworkspace/cli/releases` — neither coordinate is verifiable as real; skill is unusable if the CLI doesn't exist as described.
- All 43 recipes, persona bundles, and command syntax inherit this provenance risk (A5/A6).
- The 5 Python wrappers (`gws_doctor.py` etc.) are fine but only meaningful if `gws` resolves.
Verify (definition of done):
- Documented install command succeeds on a clean machine (`gws --version` exits 0), or the skill is rebuilt around a verifiable tool (GAM7 / Google Workspace Admin SDK + gcloud).
- `python3 scripts/gws_doctor.py` exits non-zero with a clear "gws not installed" message (graceful degradation check).
- 5 randomly sampled recipe commands validated against the CLI's actual `--help` output.

### engineering-team/skills/senior-security
Verdict: CUT-OR-MERGE (fold into senior-secops; keep threat modeling)
Issues:
- ~80% duplicates siblings: incident-response workflow (also in senior-secops + incident-response), secure-code-review checklist (code-reviewer), security headers (senior-secops), tool lists (security-pen-testing).
- A3: scripts section says "see the script source files directly" — no exact CLI invocations for `threat_modeler.py`/`secret_scanner.py`, no output consumption.
- Unique value is only the STRIDE-per-element matrix + DREAD scoring + threat_modeler.py.
Verify (definition of done):
- `python3 scripts/threat_modeler.py --help` exits 0 and the surviving SKILL.md (wherever it lands) shows an exact invocation whose JSON output feeds a named next step.
- After merge, `grep -l "STRIDE" engineering-team/skills/*/SKILL.md` returns exactly one file.
- No SEV/IR phase table remains in the merged body (route to incident-response instead).

### engineering-team/skills/senior-ml-engineer
Verdict: OPTIMIZE
Issues:
- A6: cost table (lines 154-157) lists GPT-4/GPT-3.5/Claude 3 Opus/Haiku at 2024 prices; `references/llm_integration_guide.md` repeats it plus "GPT-4 8,192 context" and `model="gpt-4"` defaults.
- Provider abstraction + tenacity retry code is generic boilerplate (A2).
- Tools shown with one-line CLI but no output-consumption step (`--deploy` flag semantics unstated).
Verify (definition of done):
- `grep -rE "GPT-4|GPT-3\.5|Claude 3 " skills/senior-ml-engineer/` returns 0 hits.
- `python3 scripts/model_deployment_pipeline.py --help` exits 0 and SKILL.md states what artifact each tool emits and which workflow step consumes it.

### engineering-team/skills/senior-data-scientist
Verdict: OPTIMIZE
Issues:
- A3 hard fail: "Common Commands" references `scripts/train.py`, `scripts/evaluate.py`, `scripts/health_check.py` — none exist; the real scripts (`experiment_designer.py`, `feature_engineering_pipeline.py`, `model_evaluation_suite.py`) are never mentioned.
- Body is inline Python a frontier model writes on demand; the embedded checklists (SRM check <0.01, Bonferroni, parallel trends, HC3) are the actual value — keep those, cut the function bodies.
- Generic kubectl/docker/helm command block is irrelevant filler (A7).
Verify (definition of done):
- Every script path in SKILL.md exists: `grep -o "scripts/[a-z_]*\.py" SKILL.md | xargs -I{} test -f skills/senior-data-scientist/{}` all pass.
- `python3 scripts/experiment_designer.py --help` exits 0 and SKILL.md shows an exact invocation per tool.

### engineering-team/skills/senior-qa
Verdict: OPTIMIZE
Issues:
- Corrupted snippets at lines 123 and 244 (mangled `getByRole` calls) — copy-paste hazards.
- RTL query/async/MSW quick-reference is frontier-model-embodied content (A2); MSW example uses deprecated `rest` API (v1) — current msw is `http` (A6).
- `actions/upload-artifact@v3` in CI example is deprecated.
- Coverage workflow is good (threshold + `--strict` exit 1) — keep.
Verify (definition of done):
- All TS/TSX code blocks in SKILL.md parse (extract fenced blocks, run through `tsc --noEmit` or eslint-parse smoke check).
- `python3 scripts/coverage_analyzer.py assets-or-sample --threshold 80` documented and exits per stated contract (0 pass / 1 below threshold).

### engineering-team/skills/senior-frontend
Verdict: OPTIMIZE
Issues:
- Corrupted config at line 425: `remotePatterns: [{ hostname: "cdnexamplecom" }]` (dots stripped).
- Lines 197-465: compound-components/render-props/Image/Suspense dump duplicates what the model knows and what `references/react_patterns.md` already holds — violates progressive disclosure (A2).
- The 2026 wrapper (profiles, decision engine, forcing questions) is excellent; the legacy middle dilutes it.
Verify (definition of done):
- `python3 scripts/frontend_decision_engine.py --primary-device mobile-4g --lcp-target-ms 2000 --seo-dependent true --auth-walled false --team-size 5` exits 0 and emits matched profile + thresholds.
- SKILL.md under 350 lines with pattern code moved to references/; corrupted snippet fixed.

### engineering-team/skills/senior-backend
Verdict: OPTIMIZE
Issues:
- Corrupted Zod snippet at line 253 (`name: "zstringmin1max100"`).
- HTTP status-code table, REST response formats = frontier-embodied filler (A2).
- Load-tester flags shown (`--expect-rate-limit`, `--expect-status`) need verification against actual argparse surface.
Verify (definition of done):
- `python3 scripts/backend_decision_engine.py --team-size 8 --qps-p99 50 --read-write-ratio 20 --tenancy shared-multi-tenant --data-sensitivity pii --pattern modular-monolith --language-preference typescript` exits 0 with profile + SLO floor + approver chain.
- `python3 scripts/api_load_tester.py --help` lists every flag SKILL.md uses.

### engineering-team/skills/senior-architect
Verdict: OPTIMIZE
Issues:
- Monolith-vs-microservices checkboxes and team-size tables are generic (A2) — senior-fullstack's forcing-question + kill-criterion treatment of the same decision is strictly better; cross-link instead of duplicating.
- No verification loop: workflows end at "document decision" (A4).
- Tools are well-wired (exact CLI, sample outputs) — keep.
Verify (definition of done):
- `python3 scripts/dependency_analyzer.py . --output json` exits 0 and emits `circular` + `coupling_score` keys; SKILL.md workflow ends with "re-run analyzer, assert circular = 0".
- ADR step references a concrete template file that exists in the package.

### engineering-team/skills/senior-data-engineer
Verdict: OPTIMIZE
Issues:
- 34-line trigger-phrase section is frontmatter duplication (A2); body's batch-vs-streaming and Lambda-vs-Kappa tables are textbook content.
- "Workflows → See references/workflows.md" and "Troubleshooting → See ..." one-liners make the body a stub while references hold the substance — inverted disclosure (workflows.md is solid at 624 lines).
- Tool subcommand contracts (`generate`/`validate`/`analyze`) shown but outputs not consumed by named steps.
Verify (definition of done):
- `python3 scripts/data_quality_validator.py --help` exits 0 and supports the `validate --checks freshness,completeness,uniqueness` syntax shown.
- SKILL.md inlines a 10-line decision rule per workflow with the deep dive staying in references/.

### engineering-team/skills/incident-commander
Verdict: OPTIMIZE
Issues:
- Orphan scripts: `severity_classifier.py`, `incident_timeline_builder.py`, `postmortem_generator.py` duplicate the 3 wired tools (A3/A7) — delete or wire.
- SEV1-SEV4 definitions overlap incident-response (security flavor) with no disambiguation table; add "this is NOT security incident triage" routing.
- Marketing-prose header block ("battle-tested practices ... at scale") is filler (A2).
Verify (definition of done):
- `ls scripts/ | wc -l` equals the number of scripts referenced in SKILL.md.
- `echo '{"description":"...","affected_users":"80%","business_impact":"high"}' | python3 scripts/incident_classifier.py` exits 0 and output matches `expected_outputs/incident_classification_text_output.txt` semantics.

### engineering-team/skills/ms365-tenant-manager
Verdict: OPTIMIZE
Issues:
- 3 scripts (`powershell_generator.py`, `tenant_setup.py`, `user_management.py`) never referenced in SKILL.md; root-level `sample_input.json`/`expected_output.json` orphaned too (A3).
- PowerShell content is genuinely expert (Graph SDK, CA report-only-first) — keep; just wire or delete the Python layer.
- Verify Graph cmdlet names still current (MSOnline/AzureAD modules retired; this correctly uses Mg* — confirm references do too).
Verify (definition of done):
- Either SKILL.md shows exact CLI for all 3 scripts with consumed output, or `scripts/` is removed.
- `python3 scripts/powershell_generator.py --help` exits 0 (if retained).

### engineering-team/skills/stripe-integration-expert
Verdict: OPTIMIZE
Issues:
- Pinned `apiVersion: "2024-04-10"` presented as current (A6).
- 476 lines of TSX/route-handler code a frontier model writes; the durable value (lifecycle state machine, webhook event ordering, idempotency discipline) should lead, code moved to references/.
- No scripts, no references, no verification loop (A3/A4) — e.g., no webhook-handler checklist gate.
Verify (definition of done):
- `grep -c "apiVersion" SKILL.md` hits use a placeholder + "check current API version" instruction, not a pinned date.
- Workflow ends with executable check: `stripe listen`/`stripe trigger checkout.session.completed` smoke procedure with expected handler behavior stated.

### engineering-team/skills/email-template-builder
Verdict: OPTIMIZE (merge candidate with marketing email skills if it stays code-only)
Issues:
- Entire skill is one 439-line code dump: no scripts/, references/, assets/ (A3/A7).
- React Email component code is frontier-embodied; the value is the pitfalls list (600px, inline styles, dark-mode `!important`, separate sending domains) and provider matrix — invert the ratio.
- No verification loop (no spam-score check step, no preview-render gate) (A4).
Verify (definition of done):
- SKILL.md ≤ 200 lines centered on client-compatibility rules + deliverability checklist; full code in references/.
- Workflow ends with an executable gate (e.g., render template via `npx react-email` preview + checklist assertion of plain-text part present).

### engineering-team/skills/tech-stack-evaluator
Verdict: OPTIMIZE
Issues:
- "Ecosystem health from GitHub, npm metrics" is a stdlib offline tool — data is embedded snapshots with no as-of date; comparisons silently age (A6).
- Quick-start examples are bare prose prompts, not tool invocations — wire them to the scripts.
- 7 scripts but SKILL.md gives exact CLI for only 5 (format_detector, report_generator unmentioned).
Verify (definition of done):
- `python3 scripts/tco_calculator.py --input assets/sample_input_tco.json` exits 0 and matches `assets/expected_output_comparison.json` schema.
- Every embedded-data script prints a `data_as_of` field in JSON output and SKILL.md tells the model to label conclusions with it.

### engineering-team/skills/engineering-skills
Verdict: OPTIMIZE
Issues:
- Claims "23 production-ready engineering skills"; `skills/` holds 32; plugin.json says 32; README says 18; START_HERE says 14 — pick one truth (A6/E2).
- As a skill it's a static catalog; its only durable instruction ("load one SKILL.md, don't bulk-load") could live in the plugin description.
- `npx agent-skills-cli add ...` install path needs verification.
Verify (definition of done):
- `ls -d engineering-team/skills/*/ | wc -l` equals the count stated in SKILL.md, plugin.json, README.md, and START_HERE.md.
- Skill table lists every actual folder (no missing security-suite rows).

## KEEP-verdict verification criteria

- **adversarial-reviewer** — review output contains all 3 persona sections each with ≥1 finding and ends with verdict ∈ {BLOCK, CONCERNS, CLEAN}; promotion rule applied when 2+ personas overlap.
- **ai-security** — `python3 scripts/ai_threat_scanner.py --target-type llm --access-level black-box --json` exits 0/1/2 per contract and JSON has `overall_risk` + `findings[].finding_type`; `--access-level gray-box` without `--authorized` exits 2.
- **aws-solution-architect** — `python3 scripts/architecture_designer.py --input <sample>` emits `recommended_pattern` + `estimated_monthly_cost_usd`; CloudFormation output passes `aws cloudformation validate-template` (or cfn-lint) when run.
- **azure-cloud-architect** — `python3 scripts/bicep_generator.py --arch-type web-app --output /tmp/main.bicep` exits 0 and output parses with `az bicep build` where available.
- **cloud-security** — `python3 scripts/cloud_posture_check.py <iam-sample>.json --check iam --json` exits 2 on a PassRole+CreateFunction policy and 0 on least-privilege sample.
- **code-reviewer** — `python3 scripts/code_quality_checker.py assets/sample_java_smells.java --json | diff - expected_outputs/sample_java_smells_quality.json` is empty (regression fixture green); dispatch table covers every `languages/*.md` file.
- **epic-design** — `python3 scripts/inspect-assets.py --help` exits 0 without Pillow installed; output format matches references/asset-pipeline.md Step 4 contract.
- **gcp-cloud-architect** — `python3 scripts/cost_optimizer.py --resources <sample>.json --monthly-spend 2000` exits 0 with itemized savings.
- **incident-response** — `echo '{"event_type":"ransomware","host":"x","raw_payload":{}}' | python3 scripts/incident_triage.py --classify --json` exits 2 (SEV1) and maps T1486.
- **red-team** — `python3 scripts/engagement_planner.py --techniques T1059 --access-level external --json` (no `--authorized`) exits 1; with `--authorized` exits 0 and orders phases by kill chain.
- **security-pen-testing** — `python3 scripts/vulnerability_scanner.py --target web --scope quick --json` exits 0 and emits OWASP A01-A10 checklist items; `dependency_auditor.py --file package.json --json` parses.
- **senior-computer-vision** — `python3 scripts/dataset_pipeline_builder.py --help` lists `--analyze/--clean/--split/--generate-config` flags used in SKILL.md; `inference_optimizer.py --help` lists `--benchmark/--export`.
- **senior-devops** — `python3 scripts/terraform_scaffolder.py /tmp/infra --provider=aws --module=ecs-service` exits 0; generated HCL passes `terraform validate` where available; rollback procedure's `curl -sf .../healthz` gate retained.
- **senior-fullstack** — `python3 scripts/fullstack_decision_engine.py --sample --output json` exits 0 with `ranked_matches[0].profile_name` and empty `kill_criteria_tripped` (verified this audit); engine refuses (non-zero) when any of the 4 required inputs missing.
- **senior-secops** — `python3 scripts/security_scanner.py <dir>` exit codes follow 0/1/2 contract; `compliance_checker.py --framework soc2 --json` emits per-control results; CVE-triage SLA table retained (9.0+ internet-facing = 24h).
- **tdd-guide** — `python3 scripts/coverage_analyzer.py --report assets/sample_coverage_report.lcov --threshold 80` exits per contract and P0/P1/P2 buckets present; `test_generator.py --input <py> --framework pytest` output compiles.
- **threat-detection** — `python3 scripts/threat_signal_analyzer.py --mode anomaly --events-file <sample> --baseline-mean 100 --baseline-std 25 --json` exits 2 only when z ≥ 3.0; IOC mode flags >30-day-old IPs as `stale`.
- **a11y-audit** — `python3 scripts/contrast_checker.py --fg "#777777" --bg "#ffffff"` reports fail at 4.5:1; `a11y_scanner.py <dir> --ci` exits non-zero only on critical findings; `--baseline` comparison runs.
- **snowflake-development** — `python3 scripts/snowflake_query_helper.py merge --target t --source s --key id --columns a,b` exits 0 and emitted SQL contains colon-prefix rule compliance in proc templates.
- **playwright-pro/pw** — all 9 sub-skill routes listed exist as skill folders; Quick Start sequence references only shipped commands.
- **playwright-pro/init** — generated `playwright.config.ts` sets `retries: 2` in CI / `0` local and `trace: 'on-first-retry'`; first smoke test runs.
- **playwright-pro/generate** — workflow step 7 retained: `npx playwright test <file> --reporter=list` must run before reporting done; no `waitForTimeout` in output.
- **playwright-pro/review** — review loads `anti-patterns.md` (file exists) and flags a seeded `page.waitForTimeout()` fixture.
- **playwright-pro/fix** — fix loads `flaky-taxonomy.md` (file exists); completion requires `--repeat-each=10` 10/10 green.
- **playwright-pro/migrate** — post-migration step routes to `/pw:coverage` parity check before decommissioning old suite.
- **playwright-pro/coverage** — output lists tested vs untested routes with priority ranking.
- **playwright-pro/report** — report generation consumes `playwright-report/` or JSON reporter output, errors clearly when absent.
- **playwright-pro/testrail** — refuses gracefully with setup instructions when `TESTRAIL_URL/USER/API_KEY` unset.
- **playwright-pro/browserstack** — refuses gracefully when `BROWSERSTACK_USERNAME/ACCESS_KEY` unset.
- **self-improving-agent (root)** — memory-paths table matches current Claude Code memory layout (`~/.claude/projects/<path>/memory/MEMORY.md`, 200-line load) — recheck against docs each release.
- **si/review** — spawns memory-analyst; output buckets = promotion candidates / stale / consolidation / conflicts / health.
- **si/promote** — promotion writes to CLAUDE.md or `.claude/rules/` AND removes the MEMORY.md source entry (both halves verified).
- **si/extract** — extracted skill passes `scripts/audit_skills.py` (repo validator) with no FAIL.
- **si/remember** — entry written with timestamp + category into the active memory dir.
- **si/status** — dashboard reports line counts vs 200-line budget and flags overflow topic files.

## Agents

| Agent | B1 frontmatter | B2 differentiation | B3 body | Verdict |
|---|---|---|---|---|
| playwright-pro/agents/test-architect | PASS (read-only tools) | PASS — plans, explicitly does not write tests | PASS | KEEP |
| playwright-pro/agents/test-debugger | PASS — exemplary scoped `Bash(npx playwright test *)` allowlist + disallowedTools | PASS — taxonomy-driven diagnosis | PASS | KEEP |
| playwright-pro/agents/migration-planner | PASS (read-only) | PASS — detection protocol per framework | PASS | KEEP |
| self-improving-agent/agents/memory-analyst | PASS (Read/Glob/Grep, maxTurns 30) | PASS — read-only analyst, distinct outputs | PASS | KEEP |
| self-improving-agent/agents/skill-extractor | PASS (Write/Edit + disallowedTools) | PASS — portability rules (no hardcoded paths) | PASS | KEEP |

Note: agent descriptions use "Invoked by /pw:..." rather than "Use when..." trigger phrasing — acceptable since they are command-spawned, not auto-triggered.

## Commands

None in scope. engineering-team/ ships no `commands/` directory; the `/pw:*` and `/si:*` surfaces are skills-as-commands (audited above). The grep hits under `commands*` are reference docs, not slash commands.

## Plugin manifests

| Plugin | Issue |
|---|---|
| `.claude-plugin/plugin.json` (engineering-skills) | Says "32 skills" — matches `skills/` dir count, but conflicts with SKILL.md (23), README (18), START_HERE (14). Description is a 1,100-char wall; trim. |
| `a11y-audit` | Clean; description matches contents. |
| `google-workspace-cli` | Description repeats the unverifiable `gws` CLI claims; fix alongside the skill REWRITE. |
| `playwright-pro` (name: `pw`) | Clean; "55+ templates, 3 agents" — template count not verified file-by-file but folder structure exists. |
| `self-improving-agent` (name: `si`) | Clean; commands listed all exist as sub-skills. |
| `snowflake-development` | Description's "query helper script, 3 reference guides" verified accurate (1 script, 3 refs). Clean. |

Additional manifest-adjacent debt: 18 stale `.zip` archives at engineering-team root; engineering-team/CLAUDE.md documents 7 nonexistent script filenames and a "32 skills / 39+ tools" inventory that predates the security suite and sub-plugins.
