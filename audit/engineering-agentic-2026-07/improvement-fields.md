# Improvement fields — what to fix, per field, across both engineering domains

The per-skill line items live in [engineering.md](engineering.md) and
[engineering-team.md](engineering-team.md). This file rolls them up into the **eight
fields** where investment moves the most skills, ordered by leverage (skills lifted per
unit of work). Distribution today, 115 distinct skills across both domains:
**26 HARNESS-READY · 39 LOOP-CAPABLE · 43 TOOL-ONLY · 7 PROSE-ONLY.**

## Field 1 — Loop discipline (AR5): the single biggest lever

~45 skills either say "re-run until clean" with no cap or have no retry/stop language at
all. The fix is one standardized block per skill:

> Remediate → re-run `<tool>` → exit 0 required. Max **3** cycles; a repeat failure for the
> same reason after 2 attempts means a structural assumption is wrong — stop and escalate
> with the evidence log.

- Cheapest wins (already 7–8 points, one sentence from HARNESS-READY):
  claude-coach, data-quality-auditor, universal-scraping-architect, docker-development,
  helm-chart-builder, mcp-server-builder, tech-debt-tracker, skill-security-auditor
  (engineering/); ai-security, threat-detection, cloud-security, incident-response,
  senior-secops, red-team, security-pen-testing (engineering-team/).
- Estimated movement: **~15 skills → HARNESS-READY** from this field alone.

## Field 2 — Goal intake (AR1): refuse to run on fuzz

40+ skills accept any input silently. Three proven in-house patterns to propagate:
1. Decision-engine refusal (senior-fullstack/frontend/backend): refuse when required
   inputs are missing, list them.
2. Forcing-question library with recommended answers (grill-me, the fork-orchestrators,
   zero-hallucination-coder).
3. Exit-code intake gates (agent-harness `goal_compiler.py` exits 3 on vague goals).

Priority targets: every security skill (authorization scope!), ci-cd-pipeline-builder,
docker-development, helm-chart-builder, dependency-auditor, sql-database-assistant.

## Field 3 — Binding verification (AR4): described ≠ required

Validators exist but their exit codes aren't load-bearing. Convert "run the validator"
into "the workflow does not proceed past step N until `<cmd>` exits 0":
- llm-wiki (`lint_wiki.py` is "periodic"), karpathy-coder (warn-only pre-commit),
  docker/helm (validate steps without loop closure), senior-architect ("document decision"
  instead of "re-run dependency_analyzer, assert circular=0"), cloud architects (no
  `cfn-lint` / `az bicep build` / terraform-validate gates), api-test-suite-builder
  (generated suite never executed).

## Field 4 — Orphan and mismatched tooling (AR3): the recurring A3 debt

- **New P1:** senior-data-engineer's documented CLI doesn't match the shipped argparse
  (`--checks`/`--input` don't exist; `etl_performance_optimizer.py` missing).
- **Worst orphan:** ship-gate's `ship_gate_scanner.py` (~1230 LOC, full exit-code contract,
  never mentioned in its SKILL.md).
- Others: agenthub `dry_run.py`, interview-system-designer (3 root scripts),
  secrets-vault-manager (3), engineering/handoff (3), spec-driven-workflow (pathless CLIs).
- Prevention: extend CI gate G2 to assert every `scripts/*.py` basename appears in its
  SKILL.md (the harness manifests already record `wired: true/false` per tool — a
  one-line CI check over the manifests catches this class forever).

## Field 5 — Close-out & state (AR6): make "done" an artifact

Most skills just end. Adopt tc-tracker's handoff block or the agent-harness close contract
(`close` refuses while unverified; emits evidence log + waivers). Targets: performance-
profiler (before/after numbers as required artifact), senior-prompt-engineer (persist eval
baseline), monorepo-navigator (workspace map artifact), all nine un-upgraded senior-* roles.

## Field 6 — Structural verdicts deferred since June

1. Dedupe the 4 dual-published pairs (slo/chaos/k8s/flags) — mind the trap: bundle Quick
   Starts reference standalone paths.
2. Merge/retire the database trio (database-schema-designer is still PROSE-ONLY with the
   broken L154 seed example).
3. Rebuild the three engineering-team PROSE-ONLY dumps: stripe-integration-expert,
   email-template-builder, tech-stack-evaluator.
4. claude-coach's three June defects (dup frontmatter, README paste, unwired classifier).

## Field 7 — Freshness & correctness spot-fixes

- senior-ml-engineer: 12 stale-model hits (2024 GPT-4/Claude-3 pricing as current).
- senior-qa: msw v1 API + `upload-artifact@v3`.
- autoresearch loop sub-skill: stale `CronCreate`/`CronDelete` tool names + interval below
  the current hourly trigger minimum.
- stripe-integration-expert: pinned `apiVersion: "2024-04-10"`.
- collab-proof: untranslated Korean rubric phrases.
- Registry drift: named-persona-adversarial-review in zero indexes; engineering-team
  CLAUDE.md lists 8 phantom script names; ship-gate table 84 vs 89.
- write-a-skill fails its own checklist runner (dogfooding gap).

## Field 8 — Role-skill loop template (engineering-team's bi