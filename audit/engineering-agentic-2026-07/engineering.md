# Domain re-audit: engineering/ — delta vs June 2026 + agentic readiness

Audited: 2026-07-03 · 63 distinct skills under `engineering/` · Method: full SKILL.md
reads, June "Verify" criteria re-run, ~30 script smoke tests (all exit codes checked).
Rubric: [RUBRIC.md](RUBRIC.md). June baseline: [../newgen-2026-06/engineering.md](../newgen-2026-06/engineering.md).

## Summary stats

**Delta resolution (19 non-KEEP June verdicts):**

- **RESOLVED: 9** — agent-designer, dependency-auditor, rag-architect, skill-tester,
  tech-debt-tracker (REWRITEs); command-guide (deleted); release-manager (merged into
  changelog-generator, hotfix/rollback tables absorbed); engineering-advanced-skills
  (counters now 37=37=37, paths fixed); universal-scraping-architect (all 3 scripts wired,
  agent/command rebuilt, layout normalized).
- **PARTIALLY-RESOLVED: 6** — migration-architect, observability-designer (CLIs + gates
  added but textbook bodies never pruned); database-designer (wired, not merged);
  agent-workflow-designer, api-design-reviewer, runbook-generator.
- **STILL-OPEN: 4** — database-schema-designer (no merge, zero scripts, broken seed example
  at L154 persists), codebase-onboarding, interview-system-designer, claude-coach (all 3
  June defects untouched: dup frontmatter keys `Name:`+`name:` / `1.0.0`+`2.9.0`, README
  paste L145–205, unwired classifier).
- Side-asks: 5 orphan plugins now marketplace-registered ✅ · 4 dual-published duplicates
  (slo/chaos/k8s/flags) still undeduped (byte-identical, `diff -rq` clean) ❌ · autoresearch
  evaluator `--help`-exception sentence never added ❌ · env-secrets-manager dead cross-refs
  persist ❌ · focused-fix `superpowers:*` still "REQUIRED SUB-SKILL" ❌.

**Agentic-readiness distribution (63 skills):** HARNESS-READY **22** · LOOP-CAPABLE **23**
· TOOL-ONLY **16** · PROSE-ONLY **2**. Weakest dimensions: **AR5 loop discipline**
(caps/stop conditions rare outside v2.4+ skills) and **AR1 goal intake** (most tool-rich
skills accept any input silently).

**KEEP spot-checks (~25 contracts re-run):** PASS except — **ship-gate** (category table 84
vs checks.md 89), **write-a-skill** (fails its own checklist runner: 141 lines vs its <100
rule, exit 1), **workflow-builder** (`--sample` exits 1 *by design* — June criterion wrong,
needs one doc sentence), **focused-fix** (superpowers refs unresolved),
**env-secrets-manager** (all 5 cross-ref paths fail `ls`). Verified anchors reproduce: slo
error-budget 43.20 min, statistical-analyst +1.2pp, tc-tracker rejects `planned→deployed`
(exit 2), commit_linter/mcp_validator `--strict` exit 1 correctly.

## Per-skill table

Scores AR1·AR2·AR3·AR4·AR5·AR6. Class: HR=HARNESS-READY, LC=LOOP-CAPABLE, TO=TOOL-ONLY,
PO=PROSE-ONLY. Delta "—" = KEEP verdict holding.

| Skill | June | Delta | AR1-6 | Tot | Class | Top improvement |
|---|---|---|---|---|---|---|
| skills/agent-designer | REWRITE | RESOLVED | 1·2·2·2·1·2 | 10 | HR | Cap the step-4 re-evaluate loop (max 3 pilot re-runs, then escalate) |
| skills/agent-workflow-designer | OPTIMIZE | PARTIAL | 0·1·2·1·0·0 | 4 | TO | Add June-mandated "When NOT to use → workflow-builder" block + JSON-validity gate on scaffolder output |
| skills/api-design-reviewer | OPTIMIZE | PARTIAL | 0·1·2·2·1·1 | 7 | LC | Cut L31-349 textbook REST to references/ (body ≤200); cap lint-fix cycles at 3 |
| skills/api-test-suite-builder | KEEP | — | 0·1·2·0·0·0 | 3 | TO | Add gate: generated suite must pass `npx vitest run`/`pytest -x` with 0 collection errors; coverage contract per route |
| skills/browser-automation | KEEP | — | 1·1·1·1·1·0 | 5 | TO | Full runnable CLIs in Quick Start; require `anti_detection_checker.py` exit-0 pre-run; retry cap 3 on 429/403 |
| skills/changelog-generator | KEEP | — (merge done) | 1·1·2·2·1·2 | 9 | HR | State retry cap for lint-fix cycle |
| skills/chaos-engineering | KEEP | dedupe open | 2·2·2·2·2·2 | 12 | HR | Deduplicate bundle/standalone copies |
| skills/ci-cd-pipeline-builder | KEEP | — | 0·1·2·1·0·1 | 5 | TO | Require `yaml.safe_load` exit-0 gate on generated pipeline; intake (platform/targets/branches) |
| skills/codebase-onboarding | OPTIMIZE | STILL-OPEN | 0·1·2·1·0·1 | 5 | TO | Add June-mandated gate: execute every setup command in the doc once, 0 ❌ before done |
| skills/database-designer | CUT-OR-MERGE | PARTIAL | 1·1·2·2·1·1 | 8 | LC | Execute the merge into sql-database-assistant (or add explicit routing); cap analyze-fix at 2 cycles |
| skills/database-schema-designer | CUT-OR-MERGE | STILL-OPEN | 0·1·0·1·0·0 | 2 | PO | Retire per June verdict: migrate RLS block + pitfalls table, delete broken L154 seed example |
| skills/dependency-auditor | REWRITE | RESOLVED | 0·1·2·2·1·1 | 7 | LC | Intake (ecosystem/policy/threshold); cap upgrade-rescan at 2 cycles |
| skills/engineering-advanced-skills | OPTIMIZE | RESOLVED | 0·0·0·0·0·0 | 0 | PO (index by design) | Optionally add "state which skill you loaded and why" routing rule |
| skills/env-secrets-manager | KEEP | cross-refs STILL-OPEN | 0·1·2·1·1·1 | 6 | LC | Fix 5 dead cross-ref paths; make `env_auditor.py` 0-critical a binding close gate |
| skills/feature-flags-architect | KEEP | dedupe open | 1·2·2·2·2·2 | 11 | HR | Deduplicate copies |
| skills/focused-fix | KEEP | PARTIAL | 2·2·1·2·2·2 | 11 | HR | Reword `superpowers:*` as optional externals; drop phantom `scope` skill ref (L308) |
| skills/full-page-screenshot | KEEP | — | 1·1·2·2·1·1 | 8 | LC | Hard gate: `file out.png` = PNG & height>viewport; stop after 2 `--wait` increases |
| skills/git-worktree-manager | KEEP | — | 1·1·2·2·1·1 | 8 | LC | Make Validation Checklist a required exit gate with one recovery pass then escalate |
| skills/interview-system-designer | OPTIMIZE | STILL-OPEN | 0·1·1·1·0·0 | 3 | TO | Wire or delete the 3 orphan root-level scripts; relocate out of engineering per June misfit note |
| skills/kubernetes-operator | KEEP | dedupe open | 1·1·2·2·1·2 | 9 | HR | Cap validator fix-rerun cycles at 3; deduplicate copies |
| skills/mcp-server-builder | KEEP | — | 1·1·2·2·0·1 | 7 | LC | Loop rule: fix + re-run `mcp_validator.py --strict` until exit 0, max 3 cycles; done contract (paths + JSON keys) |
| skills/migration-architect | REWRITE | PARTIAL | 1·2·2·2·1·1 | 9 | HR | Cut L55-429 textbook to references/ (Verify cap ≤200); stop condition: 3 failed gate revisions → escalate |
| skills/monorepo-navigator | KEEP | — | 1·0·2·0·0·0 | 3 | TO | Numbered workflow + gate (analyzer JSON `cycles` empty; affected-only CI filter); artifact = workspace map |
| skills/observability-designer | REWRITE | PARTIAL | 1·1·2·1·1·1 | 7 | LC | Prune L35-273 golden-signals brochure; make alert loop a hard gate (duplicate count = 0) with 1-rotation stop |
| skills/performance-profiler | KEEP | — | 1·1·2·1·0·1 | 6 | LC | Before/after numbers as required artifact (<10% improvement → revert); one-bottleneck-at-a-time stop rule |
| skills/pr-review-expert | KEEP | — | 1·1·2·1·0·1 | 6 | LC | Verdict gate (BLOCK on MUST-FIX or coverage < −5%); re-review loop max 3 rounds then human |
| skills/rag-architect | REWRITE | RESOLVED | 1·2·2·2·2·2 | 11 | HR | Move 3 root scripts into scripts/ (layout anomaly only) |
| skills/runbook-generator | OPTIMIZE | PARTIAL | 1·1·2·1·0·1 | 6 | LC | Add June-required post-generation checklist as refusal gate (rollback non-empty, every step has verify line) |
| skills/secrets-vault-manager | KEEP | — | 1·1·1·1·0·0 | 4 | TO | Exact CLIs for all 3 scripts; gate: audit_log_analyzer shows zero old-credential usage before rotation done |
| skills/self-eval | KEEP | — | 1·1·0·2·1·2 | 7 | LC | Prompt-only by design; optional tiny `scores_check.py` JSONL assertion to formalize AR3 |
| skills/ship-gate | KEEP | table-drift FAIL | 2·2·0·2·2·2 | 10 | HR | Wire the fully orphaned `ship_gate_scanner.py` (~1230 LOC) as Step 2 with exit-code verdict; true-up table 84→89 |
| skills/skill-security-auditor | KEEP | — | 1·1·2·2·0·1 | 7 | LC | Remediate→re-scan loop until PASS (max 3); attach JSON report to install decision |
| skills/skill-tester | REWRITE | RESOLVED | 1·1·2·2·2·1 | 9 | HR | Recalibrate `skill_validator.py` tier minimums (still scores new-style <100-line skills POOR) |
| skills/slo-architect | KEEP | dedupe open | 2·1·2·2·1·2 | 10 | HR | Deduplicate copies (bundle Quick Start points at standalone path — deleting standalone breaks bundle docs) |
| skills/spec-driven-workflow | KEEP | — | 2·2·1·2·2·2 | 11 | HR | Fix pathless CLIs (`python spec_validator.py` → `python3 scripts/spec_validator.py`, L151/177/324-333) → AR3=2 |
| skills/sql-database-assistant | KEEP | — | 0·1·2·1·0·0 | 4 | TO | Gate every generated query through `query_optimizer.py` (score <70 → rewrite); fix phantom `observability-platform` ref |
| skills/tc-tracker | KEEP | — | 1·1·2·2·1·2 | 9 | HR | Already strong; add explicit iteration cap on validation-fix loop |
| skills/tech-debt-tracker | REWRITE | RESOLVED | 1·1·2·2·1·1 | 8 | LC | Stop condition (2 flat snapshots → re-prioritize) + sprint artifact contract → ≥9 |
| agenthub (8 sub-skills) | KEEP | — | 2·2·2·2·2·2 | 12 | HR | Wire orphaned `dry_run.py` as mandatory pre-spawn gate in /hub:run; explicit max-attempt cap |
| autoresearch-agent (6) | KEEP | doc-ask STILL-OPEN | 2·2·2·2·2·2 | 12 | HR | Add evaluator `--help`-exception sentence (June ask); replace stale CronCreate/CronDelete tool names |
| behuman | KEEP | registered ✅ | 1·1·0·1·1·1 | 5 | TO | Ship a mirror-check lint as pre-output gate; cap the rewrite loop |
| caveman | KEEP | — | 0·0·1·1·1·1 | 4 | TO | Inline the 3 exact `caveman_lint.py` invocations (now only in companion_tooling.md); require PASS/WARN before sending |
| claude-coach | OPTIMIZE | STILL-OPEN (all 3) | 2·1·1·1·2·1 | 8 | LC | Fix dup frontmatter + delete L145-205 README paste; wire `coach_tip_classifier.py` as Rule-5 gate → HR |
| code-tour | KEEP | — | 1·1·0·1·0·2 | 5 | TO | Add `tour_validator.py` (schema + file/line existence, exit 0 before save); max 2 re-verify passes |
| collab-proof | NEW | — | 2·2·2·2·1·2 | 11 | HR | Add retry/cap rule for token-collection fallback; translate leftover Korean rubric phrases |
| data-quality-auditor | KEEP | — | 1·1·2·2·0·2 | 8 | LC | Remediate→re-profile loop with DQS delta report, cap 3 cycles → HR |
| demo-video | KEEP | — | 1·1·0·1·0·2 | 5 | TO | Ship scenes.json validator required before build.sh; exact ffmpeg fallback commands |
| docker-development | KEEP | — | 0·1·2·2·0·1 | 6 | LC | Intake (Dockerfile path + size/speed/security target); analyzer-score-must-improve loop, max 3 passes |
| grill-me | KEEP | — | 2·2·1·1·2·2 | 10 | HR | Exact flags for extractor/generator CLIs; machine gate = session JSON all branches `resolved` |
| grill-with-docs | KEEP | registered ✅ | 2·2·2·2·2·2 | 12 | HR | None blocking — exemplar |
| handoff (engineering) | KEEP | — | 1·1·1·0·0·2 | 5 | TO | Wire 3 scripts with exact CLIs; port sibling productivity/handoff `handoff_self_check.py` 6-check gate |
| helm-chart-builder | KEEP | — | 1·1·2·2·0·1 | 7 | LC | Fix-and-revalidate loop (`chart_analyzer.py` 0 CRITICAL, cap 3); intake (workload/namespace/secrets) |
| karpathy-coder | KEEP | — | 1·2·1·1·1·0 | 6 | LC | Exact CLIs in SKILL.md (only agent/command carry them); make pre-commit check a required gate not warn-only |
| llm-cost-optimizer | KEEP | registered ✅ | 2·1·0·2·1·1 | 7 | LC | Add one stdlib script (savings estimator) with CLI; before/after cost-JSON gate between techniques |
| llm-wiki | KEEP | — | 1·1·2·1·0·2 | 7 | LC | Make `lint_wiki.py` exit code a required post-ingest gate (now "periodic"); fix 4 phantom related-skill refs |
| prompt-governance | KEEP | registered ✅ | 2·1·0·1·1·1 | 6 | LC | Ship registry-YAML validator; golden-dataset minimum (20) as Mode-2 refusal gate |
| security-guidance | KEEP | — | 0·0·1·2·0·1 | 5 | TO (hook by design) | Optional `--scan <file>` manual mode for deterministic re-run-to-exit-0 |
| statistical-analyst | KEEP | — | 2·1·2·2·1·1 | 9 | HR | Add H1 heading (currently none); cap extend/re-test loop at one extension |
| terraform-patterns | KEEP | — | 0·1·2·1·0·1 | 5 | TO | Gate: 0 Critical from `tf_security_scanner.py --strict` before apply; fix `./scripts/convert.sh` path |
| universal-scraping-architect | OPTIMIZE | RESOLVED | 1·1·2·2·1·1 | 8 | LC | Promote agent's intake to SKILL.md forcing questions; cap re-extraction at 2 attempts → HR |
| workflow-builder | KEEP | — (contract nuance) | 2·2·2·2·2·1 | 11 | HR | Document that `validate_workflow.py --sample` exits 1 by design; add done digest |
| write-a-skill | KEEP | self-check FAIL | 2·1·2·2·1·2 | 10 | HR | Trim own SKILL.md to <100 lines so it passes its own checklist runner; make runner exit-0 a blocking Phase-3 gate |
| zero-hallucination-coder | NEW | — | 2·2·0·2·2·2 | 10 | HR | Add one stdlib plan-linter (scan for unresolved `[UNKNOWN]`/TODO, exit 1) — AR3=0 is the only gap |

(`named-persona-adversarial-review` is scored in [engineering-team.md](engineering-team.md) —
it lives at `engineering-team/skills/`.)

## Systemic findings

### Patterns

1. **The REWRITE wave worked, but two were patches, not rewrites.** Brochure headings
   ("Future Enhancements"/"Conclusion"/"Planned Features") are now zero across engineering/;
   5 of 7 REWRITEs fully resolved. migration-architect (429 lines) and observability-designer
   (272) got a wired Quick Start + gate bolted onto an unpruned textbook body — the June
   Verify line caps remain unmet.
2. **AR5 (loop discipline) is the domain's weakest muscle.** Only v2.4+/Pocock/orchestrator-
   generation skills state iteration caps or stop conditions. ~20 skills have a "re-run until
   clean" instruction with no cap; ~25 have none at all. A single sentence pattern ("max N
   fix-rerun cycles, then escalate") would lift 8 skills sitting at 7–8 into HARNESS-READY.
3. **AR1 (goal intake) missing from tool-rich skills.** The wiring epidemic was fixed (AR3
   median is now 2), but most wired skills run on whatever input arrives — no forcing
   questions, no refusal on vague goals. The intake patterns already exist in-house
   (workflow-builder, grill-me, zero-hallucination-coder) and just need porting.
4. **Gates exist but aren't binding.** Many skills *describe* a validator yet don't
   *require* its exit code before proceeding (llm-wiki "periodic" lint, karpathy-coder
   warn-only hook, docker/helm validate-steps without loop closure).
5. **Orphan scripts persist even in KEEP skills** — new cases surfaced: **ship-gate's
   `ship_gate_scanner.py` (~1230 LOC, full exit-code contract, never mentioned in SKILL.md —
   the model is told to scan manually)**, agenthub's `dry_run.py`, interview-system-designer's
   3 root scripts, secrets-vault-manager's 3 unwired tools, handoff's 3 tools.
6. **Dead cross-references survived the phantom-path sweep** because they're skill-name
   table refs, not file paths: env-secrets-manager (5 dead), sql-database-assistant
   (`observability-platform`), llm-wiki (4 phantom related skills), focused-fix (`scope` +
   `superpowers:*` as REQUIRED).
7. **Dual-published dedupe (June finding #4) not executed.** All 4 pairs remain
   byte-identical (no divergence yet); trap: bundle copies' Quick Starts reference the
   *standalone* paths, so naive deletion of standalone copies breaks the bundle's own docs.
8. **Database-trio merge (June finding #3a) not executed** — database-designer got wired
   instead of merged; database-schema-designer remains the domain's worst skill (PROSE-ONLY,
   broken seed example intact).

### New defects found this audit

- ship-gate: orphaned scanner + category-table drift (SKILL.md 84 vs checks.md 89) — its
  KEEP contract now FAILS.
- write-a-skill: fails its own checklist runner (141 lines vs its <100 rule; exit 1) —
  the meta-skill doesn't dogfood.
- autoresearch loop sub-skill: instructs stale `CronCreate`/`CronDelete` tool names and a
  10-min interval that conflicts with the current hourly-minimum trigger surface — broken
  as written.
- claude-coach: zero progress on all 3 June defects (conflicting `Version: 1.0.0` /
  `version: 2.9.0` still parses ambiguously).
- workflow-builder: `validate_workflow.py --sample` exits 1 *by design* (intentionally
  broken sample) — the June KEEP criterion assumed 0; needs one documenting sentence.
- database-schema-designer: broken seed example at L154 persists (explicit June Verify item).
- collab-proof: untranslated Korean rubric phrases from the upstream Vela source.
- terraform-patterns: `./scripts/convert.sh` invocation resolves only from repo root; repo
  version `2.9.0` leaked into an Infracost policy example.
- statistical-analyst: no H1 heading; "You are an expert…" opener also in
  data-quality-auditor.
- skill-tester's `skill_validator.py` still penalizes new-style <100-line skills (scores
  self-eval "POOR 33.3") despite the doc-level scope note.
- No broken scripts: all ~60 `--help`/`--sample`/pipe invocations exited per contract
  (non-zero only where documented).

### Top-10 harness-ready exemplars

**agenthub (12)**, **autoresearch-agent (12)**, **chaos-engineering (12)**,
**grill-with-docs (12)**, **collab-proof (11)**, **feature-flags-architect (11)**,
**spec-driven-workflow (11)**, **workflow-builder (11)**, **rag-architect (11)**,
**focused-fix (11)**. Honorable mentions at 10: slo-architect, ship-gate, grill-me,
zero-hallucination-coder, write-a-skill — each one small fix from exemplar status.

### Highest-leverage next PRs

1. Wire ship-gate's scanner + fix its category table.
2. One-sentence loop-cap sweep across the eight 7–8-point LOOP-CAPABLE skills
   (claude-coach, data-quality-auditor, universal-scraping-architect, docker-development,
   helm-chart-builder, mcp-server-builder, tech-debt-tracker, skill-security-auditor) —
   the cheapest path to ~30 HARNESS-READY.
3. Execute the deferred structural verdicts: dedupe the 4 dual-published pairs, merge/retire
   the database trio, fix claude-coach.
