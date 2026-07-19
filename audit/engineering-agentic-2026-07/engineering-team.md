# Domain re-audit: engineering-team/ — delta vs June 2026 + agentic readiness

Audited: 2026-07-03 · 33 `skills/` + 5 standalone packages (52 distinct skills incl.
playwright-pro and self-improving-agent sub-skills). Rubric: [RUBRIC.md](RUBRIC.md).
June baseline: [../newgen-2026-06/engineering-team.md](../newgen-2026-06/engineering-team.md).

## Summary stats

**Delta resolution (16 non-KEEP June verdicts):** RESOLVED 7 · PARTIALLY-RESOLVED 4 ·
STILL-OPEN 5.

- All 4 P0 corrupted-literal sites fixed: grep for `zstringmin1max100` /
  `cdnexamplecom` / `click-mei-tobeinthedocument` → **0 hits**.
- google-workspace-cli P0 fixed: `@anthropic/gws` gone; recoordinated to
  `npm install -g @googleworkspace/cli`, every reference carries a "verify against your
  installed version / pre-v1.0" disclaimer, and `gws_doctor.py` runs gracefully in demo
  mode (exit 0).
- 18 stale `.zip` archives at domain root: **deleted** (0 remain).
- **1 NEW P1 defect found** (senior-data-engineer, below). **1 NEW skill found**
  (named-persona-adversarial-review — in no index or manifest).

**Agentic-readiness distribution (52 skills):** HARNESS-READY **4** · LOOP-CAPABLE **16** ·
TOOL-ONLY **27** · PROSE-ONLY **5**.

## Scorecard

AR1 intake / AR2 decomposition / AR3 deterministic exec / AR4 verification gate / AR5 loop
discipline / AR6 close-out (0–2 each). Delta status only for skills with non-KEEP June
verdicts. Entries marked \* score ≥9 but fail the HARNESS-READY gate because AR5 = 0.

| Skill | June | Delta | AR1-6 | Tot | Class | Top improvement |
|---|---|---|---|---|---|---|
| senior-fullstack | KEEP | — | 2/2/2/2/1/1 | 10 | **HARNESS-READY** | Add re-run rule after kill-criterion fix ("re-run engine, assert `kill_criteria_tripped` empty") to lift AR5 to 2 |
| tdd-guide | KEEP | — | 1/1/2/2/2/1 | 9 | **HARNESS-READY** | "Bounded Autonomy Rules" + threshold exits are the loop template; add state persistence (write cycle log) for AR6=2 |
| senior-security | CUT-OR-MERGE | **RESOLVED** (rewritten as 64-line STRIDE + router; re-run-is-the-done-signal gate) | 1/1/2/2/1/2 | 9 | **HARNESS-READY** | Add DREAD≥7-without-owner as a machine check (`jq` assertion on threats.json) |
| playwright-pro/fix | KEEP | — | 0/1/2/2/2/2 | 9 | **HARNESS-READY** | Best loop in the domain ("all 10 must pass, else back to step 3"); add an iteration cap (max 3 fix rounds → escalate) |
| red-team | KEEP | — | 2/2/2/2/0/2 | 10\* | LOOP-CAPABLE\* | Add explicit retry/stop rules per engagement phase (e.g., abort criteria on detection) |
| ai-security | KEEP | — | 2/1/2/2/0/1 | 8 | LOOP-CAPABLE | Add remediate→re-scan loop: "re-run scanner after fixes, exit 0 required" |
| security-pen-testing | KEEP | — | 1/2/2/2/0/2 | 9\* | LOOP-CAPABLE\* | AR5=0 blocks HARNESS; add rescan-until-clean loop with cap |
| senior-secops | KEEP | — | 1/2/2/2/1/1 | 9\* | LOOP-CAPABLE\* | Add CVE-SLA-driven stop condition to formalize AR5 |
| threat-detection | KEEP | — | 1/2/2/2/0/1 | 8 | LOOP-CAPABLE | Add tuning loop (adjust baseline, re-run until FP rate < target) |
| cloud-security | KEEP | — | 1/2/2/2/0/1 | 8 | LOOP-CAPABLE | Add fix→re-check-until-exit-0 loop; add close-out DoD |
| incident-response | KEEP | — | 1/2/2/2/0/1 | 8 | LOOP-CAPABLE | Add containment-verification re-run gate |
| code-reviewer | KEEP | — | 1/1/2/2/0/1 | 7 | LOOP-CAPABLE | Regression-fixture pattern is exemplary; add re-review-after-fix loop |
| senior-frontend | OPTIMIZE | **RESOLVED** (corrupted config fixed; decision engine + forcing questions present) | 2/1/2/2/1/1 | 9 | **HARNESS-READY** | Still 572 lines — move React/Next patterns to references/ per June Verify |
| senior-backend | OPTIMIZE | **RESOLVED** (Zod literal fixed; decision engine refuses on missing inputs) | 2/2/2/1/0/1 | 8 | LOOP-CAPABLE | Add executable SLO-floor verification gate + re-run loop (AR4→2, AR5) |
| senior-qa | OPTIMIZE | **PARTIALLY** (corrupted snippets fixed; still `msw rest.` v1 API L274 + `upload-artifact@v3` L220) | 1/1/2/2/0/1 | 7 | LOOP-CAPABLE | Bump msw to `http`/`HttpResponse`, artifact@v4; add TS-block parse gate |
| senior-architect | OPTIMIZE | **PARTIALLY** (tools well-wired; workflow still ends at "document decision") | 1/1/2/1/0/1 | 6 | LOOP-CAPABLE | Add "re-run dependency_analyzer, assert circular=0" close-out gate (AR4/AR5) |
| senior-ml-engineer | OPTIMIZE | **STILL-OPEN** (12 stale-model hits: GPT-4/3.5/Claude-3 2024 pricing in SKILL.md L154-157 + llm_integration_guide.md L181-251) | 1/1/1/2/2/0 | 7 | LOOP-CAPABLE | Strip 2024 pricing/context tables → model-agnostic; wire tool output→next-step |
| senior-prompt-engineer | REWRITE | **RESOLVED** (0 stale-model hits; workflows end in executable eval gates with ≥baseline loop) | 1/1/2/2/2/0 | 8 | LOOP-CAPABLE | Add AR6 close-out (persist eval baseline as DoD artifact); intake forcing questions |
| senior-data-scientist | OPTIMIZE | **RESOLVED** (phantom scripts replaced by real ones) | 1/1/1/1/0/2 | 6 | LOOP-CAPABLE | Add exact CLI invocations + machine-checkable eval gate |
| senior-data-engineer | OPTIMIZE | **STILL-OPEN + NEW P1** (see below) | 0/1/1/0/0/0 | 2 | **PROSE-ONLY** | Fix documented CLI to match actual argparse; add a verification gate |
| stripe-integration-expert | OPTIMIZE | **STILL-OPEN** (pinned `apiVersion: "2024-04-10"` L72; 0 scripts/refs; 476-line code dump) | 0/0/0/0/1/0 | 1 | **PROSE-ONLY** | Replace pinned version with placeholder+instruction; add `stripe trigger` smoke gate |
| email-template-builder | OPTIMIZE | **STILL-OPEN** (439-line single-file dump; no executable gate) | 0/0/0/0/0/2 | 2 | **PROSE-ONLY** | Invert code:rules ratio, move code to references/, add `react-email` render gate |
| incident-commander | OPTIMIZE | **RESOLVED** (3 scripts all wired; security-triage disambiguation added) | 1/1/2/2/0/1 | 7 | LOOP-CAPABLE | Add re-run gate + iteration cap on timeline reconstruction |
| ms365-tenant-manager | OPTIMIZE | **RESOLVED** (all 3 scripts referenced with exact paths) | 1/1/2/1/0/2 | 7 | LOOP-CAPABLE | Add machine-checkable verify gate (CA report-only assertion) |
| tech-stack-evaluator | OPTIMIZE | **STILL-OPEN** (no `data_as_of` field; embedded ecosystem data undated) | 0/0/2/0/0/0 | 2 | **PROSE-ONLY** | Add `data_as_of` to JSON output; wire all 7 scripts; add TCO regression gate |
| engineering-skills (index) | OPTIMIZE | **PARTIALLY** (32 vs actual 33 after new skill; named-persona absent from every index) | 0/0/0/0/0/0 | 0 | **PROSE-ONLY** (index by design) | Retrue to 33; add named-persona row; single source of truth |
| adversarial-reviewer | KEEP | — | 1/2/0/0/1/1 | 5 | TOOL-ONLY | Add a scored verdict tool + machine gate |
| named-persona-adversarial-review | **NEW (not in June)** | n/a | 1/2/0/1/1/1 | 6 | LOOP-CAPABLE | No scripts; has BLOCKER promotion + re-review exit condition. Add a verdict-emitting tool; register in indexes |
| aws-solution-architect | KEEP | — | 1/2/2/1/1/1 | 8 | LOOP-CAPABLE | Add `cfn-lint`/validate-template close-out gate |
| azure-cloud-architect | KEEP | — | 1/2/2/0/0/1 | 6 | LOOP-CAPABLE | Add `az bicep build` verification gate |
| gcp-cloud-architect | KEEP | — | 1/2/2/0/0/2 | 7 | LOOP-CAPABLE | Add IaC validate gate + retry loop |
| epic-design | KEEP | — | 1/2/0/0/0/2 | 5 | TOOL-ONLY | Wire inspect-assets.py output into a pass/fail gate |
| senior-computer-vision | KEEP | — | 1/2/2/0/0/0 | 5 | TOOL-ONLY | Add eval-metric gate (mAP threshold) + close-out |
| senior-devops | KEEP | — | 1/1/2/1/0/0 | 5 | TOOL-ONLY | Add `terraform validate` gate + healthz retry loop as explicit AR5 |
| snowflake-development | KEEP | — | 1/2/1/1/0/0 | 5 | TOOL-ONLY | Add SQL-lint/dry-run gate |
| a11y-audit | KEEP | — | 1/1/1/2/1/1 | 7 | LOOP-CAPABLE | Baseline-compare loop present; add iteration cap |
| google-workspace-cli | REWRITE | **PARTIALLY** (coordinates fixed + disclaimers; tool provenance still unverifiable) | 1/2/2/0/0/0 | 5 | TOOL-ONLY | Add `gws --version` precondition gate; recipe-vs-`--help` validation step |
| playwright-pro/pw | KEEP | — | 0/1/1/2/1/0 | 5 | TOOL-ONLY | Router; fine as-is |
| playwright-pro/init | KEEP | — | 0/1/1/1/1/0 | 4 | TOOL-ONLY | Add config-assertion gate (retries=2 in CI) |
| playwright-pro/generate | KEEP | — | 0/1/1/2/1/0 | 5 | TOOL-ONLY | Strong (reporter=list gate before done); add iteration cap |
| playwright-pro/review | KEEP | — | 0/1/0/2/0/0 | 3 | TOOL-ONLY | Add fix-loop handoff to /pw:fix |
| playwright-pro/migrate | KEEP | — | 0/1/1/0/0/0 | 2 | PROSE-ONLY | Add parity-check gate before decommission (June Verify) |
| playwright-pro/coverage | KEEP | — | 0/2/0/0/0/0 | 2 | PROSE-ONLY | Wire a coverage-report tool + priority-ranked gate |
| playwright-pro/report | KEEP | — | 0/1/1/0/1/1 | 4 | TOOL-ONLY | Add absent-input error gate |
| playwright-pro/testrail | KEEP | — | 0/0/1/0/0/0 | 1 | PROSE-ONLY | Env-var precondition refusal is the AR1 win; document it as a gate |
| playwright-pro/browserstack | KEEP | — | 0/0/1/0/0/0 | 1 | PROSE-ONLY | Same as testrail |
| self-improving-agent (root) | KEEP | — | 0/0/0/0/0/0 | 0 | PROSE-ONLY (overview by design) | No executable surface |
| si/review | KEEP | — | 0/2/0/0/0/0 | 2 | PROSE-ONLY | Add bucket-count assertion gate |
| si/promote | KEEP | — | 1/2/0/0/0/1 | 4 | TOOL-ONLY | Both-halves check (write + remove source) should be a machine gate |
| si/extract | KEEP | — | 0/2/0/0/0/0 | 2 | PROSE-ONLY | Wire `audit_skills.py` no-FAIL gate (June Verify) explicitly |
| si/remember | KEEP | — | 0/2/0/0/0/1 | 3 | TOOL-ONLY | Add timestamp+category write assertion |
| si/status | KEEP | — | 0/2/0/0/0/1 | 3 | TOOL-ONLY | Add 200-line-budget overflow gate |

## Systemic findings

1. **Loop discipline (AR5) is the domain-wide bottleneck.** The security suite (red-team
   10, security-pen-testing 9, senior-secops 9) and cloud architects have excellent intake,
   deterministic tools, and exit-code gates but almost no explicit retry/stop-condition/
   iteration-cap language. Adding a single "remediate → re-run tool → exit 0 required, max
   N rounds then escalate" block would promote ~6 skills to HARNESS-READY at low cost.
2. **Best harness exemplars (template these):** playwright-pro/fix ("run `--repeat-each=10`,
   all 10 must pass, else back to step 3" — the cleanest verify+loop in the domain);
   senior-fullstack (decision engine that *refuses* on missing inputs + forcing-question
   library + kill criteria — the new-gen role template); code-reviewer (committed regression
   fixtures with expected `--json` output); senior-security rewritten ("the re-run is the
   done signal, not the document" — model close-out phrasing); senior-prompt-engineer
   (every workflow now ends in an executable gate — a genuine REWRITE→RESOLVED turnaround).
3. **Role skills split into two generations.** UPGRADED (decision engine + forcing questions
   + kill criteria): senior-fullstack, senior-frontend, senior-backend. UN-UPGRADED (no
   forcing questions, no decision engine, workflows end at "document"): senior-architect,
   senior-devops, senior-qa, senior-data-engineer, senior-data-scientist,
   senior-ml-engineer, senior-computer-vision, senior-secops, senior-prompt-engineer. The
   three upgraded roles should export a shared loop template — `Assumptions → decision
   engine (refuse on missing input) → forcing questions with kill criteria → execute →
   re-run engine/tool → assert gate → DoD` — and the nine un-upgraded roles should adopt
   it. senior-architect and senior-devops are the highest-value targets.
4. **NEW P1 — senior-data-engineer documents a CLI the tool doesn't have.** SKILL.md L74
   shows `data_quality_validator.py validate --checks freshness,completeness,uniqueness
   --input …`, but the shipped `validate` subcommand has **no `--checks` and no `--input`**
   (input is positional). SKILL.md also invokes `etl_performance_optimizer.py`, which is
   **not present** in `scripts/`. Any agent following the docs emits failing commands.
5. **STILL-OPEN staleness — senior-ml-engineer.** 12 hits of GPT-4 / GPT-3.5 / Claude 3
   Opus 2024 pricing and "GPT-4 8,192 context" presented as current. The parallel A6 fix
   landed for senior-prompt-engineer (0 hits) but not here.
6. **Count drift persists + new skill unregistered.** Actual `skills/` dir = 33 (June said
   32). named-persona-adversarial-review (PR #867) appears in **no** index — not
   engineering-skills SKILL.md, README, START_HERE, or plugin.json `skills`.
   engineering-team/CLAUDE.md still lists **8 phantom script filenames**
   (`fullstack_scaffolder.py`, `statistical_analyzer.py`, `etl_generator.py`,
   `mlops_setup_tool.py`, `llm_integration_builder.py`, `rag_system_builder.py`,
   `video_processor.py`) — June finding #6 unresolved.
7. **Three PROSE-ONLY skills need structural rebuild, not tuning:** stripe-integration-expert
   (1/12), email-template-builder (2/12), tech-stack-evaluator (2/12). All were OPTIMIZE in
   June and are STILL-OPEN — code/prose dumps with no wired-tool→gate→loop spine.
8. **Intake (AR1) is near-universally absent.** Only 5 skills score AR1≥2 (the upgraded
   role trio via decision-engine refusal; red-team, ai-security via authorization gates).
   40+ skills have zero forcing-question/refusal-on-vague-input intake. The decision-engine
   "refuse without required inputs" pattern is the cheapest AR1 fix to propagate.
