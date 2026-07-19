# Domain audit: project-management/ — deep audit + agentic readiness

Audited: 2026-07-03 · 9 skills · 12 Python tools pre-PR (all pass `--help`; end-to-end
runs of velocity_analyzer and project_health_dashboard reproduce documented fixtures),
15 post-PR · 1 agent pre-PR, 2 post · 3 commands pre-PR (+`/sprint-plan` generic), 6
post · plugin.json valid (`["./skills"]` canonical form).
Rubric: [RUBRIC.md](RUBRIC.md). Method: full SKILL.md reads, script smoke tests, MCP
tool-reference grepping, counter verification.

## Summary

**Headline finding #1 (fixed this PR): the MCP↔analytics gap.** The domain bundles a
live Atlassian Remote MCP (`.mcp.json`) and disciplined tool documentation
(`references/atlassian-mcp-tools.md`, verified live 2026-06-10), yet its two analytics
skills (senior-pm, scrum-master) had **zero** MCP references — nothing connected
`searchJiraIssuesUsingJql` output to the scripts' input schemas. Every sprint-health or
velocity run required hand-built JSON. `jira_snapshot_bridge.py` closes this: raw MCP
search results → scrum-master sprint schema (verified: piped output runs
velocity_analyzer clean) → plus the four Kanban flow metrics + seeded Monte Carlo
forecasting the domain never had.

**Headline finding #2 (fixed this PR): pre-modern agentics.** Zero `context: fork`, zero
forcing questions, no `/cs:*` namespace, no loop with named terminal states. What existed
was raw material: atlassian-admin's 7 concrete VERIFY steps, scrum-master's
data-sufficiency gates with pinned expected outputs (avg 20.2 pts, health 78.3,
action-item completion 46.7%), confluence/templates' verify-before-proceed steps.

**Agentic-readiness distribution (9 skills, post-PR):** HARNESS-READY **1** (pm-skills
upgraded 1→12) · LOOP-CAPABLE **4** (scrum-master, jira-expert, atlassian-admin,
atlassian-templates) · TOOL-ONLY **3** (senior-pm, confluence-expert, meeting-analyzer) ·
PROSE-ONLY **1** (team-communications).

## Per-skill table

Scores AR1·AR2·AR3·AR4·AR5·AR6 (post-PR where this PR changed the skill).

| Skill | AR1-6 | Tot | Class | Top improvement |
|---|---|---|---|---|
| pm-skills (orchestrator) | 2·2·2·2·2·2 | 12 | HR | (upgraded this PR: was a 50-line prose router, PROSE-ONLY) |
| scrum-master | 1·1·2·2·0·1 | 7 | LC | One sentence: cap re-analysis at 2 passes then escalate → instant HR; consume the bridge (`--to sprint`) instead of hand-built JSON |
| atlassian-admin | 0·1·2·2·0·2 | 7 | LC | Intake gate (refuse without approver named); its VERIFY steps are the domain's best — port the pattern to siblings |
| jira-expert | 0·1·2·2·0·1 | 6 | LC | Cap fix-revalidate cycles at 3; ship a sample workflow JSON asset (users must guess the validator's schema) |
| atlassian-templates | 0·1·2·1·1·1 | 6 | LC | Ship static template assets; expected-output fixture for the scaffolder |
| senior-pm | 0·1·2·1·0·1 | 5 | TO | Consume the bridge's flow output in the health dashboard; make KPI thresholds (on-time > 80% etc.) exit-code gates; portfolio-kpis.md is 32 lines |
| confluence-expert | 0·1·2·1·0·1 | 5 | TO | Make its Verify steps blocking; sample input for content_audit_analyzer |
| meeting-analyzer | 1·1·0·1·0·1 | 4 | TO | Ship the deterministic tools its own prose describes (speaking-ratio, filler counts = exactly the repo's "algorithm over AI" case); 0 scripts/refs/assets |
| team-communications | 1·1·0·0·0·0 | 2 | PO | References are 15–65 lines (the skill's premise is "follow the reference exactly"); add a 3P-format linter script |

## Domain-level findings

1. **Orchestration + loop layer (fixed this PR).** `pm-skills` is now a `context: fork`
   orchestrator: deterministic 8-lane router (`pm_goal_router.py`), the Jira bridge, and
   a delegation-governance gate (`delivery_loop_gate.py` — G1 human owner, G2 reviewer
   for agent tasks, G3 machine-checkable acceptance, G4 evidence-before-done, G5 close
   refusal, G6 exhausted-budget-is-escalation), all wired to the repo harness
   (`assets/harnesses/project-management.json`). Agent `cs-pm-orchestrator` +
   `/cs:pm`, `/cs:grill-pm`, `/cs:pm-loop` added. Five reusable PM loops documented in
   `references/pm_loop_playbook.md` (sprint-flow, health, retro-action, RAID-hygiene,
   comms), each with machine gates and named terminal states.
2. **References cited zero sources (partially fixed).** 0 URLs across all 21 pre-PR
   reference files — Schwaber/Sutherland, Vacanti, DORA, Kanban Guide all absent. The 3
   new orchestrator references cite 6–7 sources each; back-filling the other 21 is
   follow-up F9.
3. **Stale counters everywhere except plugin.json (open).** README ("6 world-class
   skills"), IMPLEMENTATION_SUMMARY ("All 6", references `/mnt/user-data/outputs/` build
   paths), REAL_WORLD_SCENARIO ("6 Expert Skills"), cs-project-manager agent ("six
   skills"), CLAUDE.md (lists 6 of 9 — meeting-analyzer, team-communications, pm-skills
   absent). CLAUDE.md updated this PR; the legacy trio (README /
   IMPLEMENTATION_SUMMARY / REAL_WORLD_SCENARIO) should be rewritten or retired (F10).
4. **MCP integration is bimodal (structural, now bridged).** Concrete in 4 skills
   (jira-expert 14 refs, confluence-expert 11, atlassian-templates 11, atlassian-admin 4
   read-only-correct); zero in the 2 analytics skills. The bridge closes the data path;
   the two SKILL.mds should still name it (one line each, F3).
5. **Two contributed skills violate the Path-B contract (open).** meeting-analyzer: zero
   scripts/references/assets — its own spec (speaking-time %, filler-word counts) is
   deterministic computation the repo mandates be scripted. team-communications: zero
   scripts, 4 references totaling 155 lines.
6. **`/sprint-plan` counts against product-team but lives half in this domain** — the
   sprint-planning integration pattern in CLAUDE.md calls product-team's
   user_story_generator; fine, but the CLAUDE.md example used the old positional CLI
   (still works — verified backward-compatible after this PR's argparse fix).

## Verification criteria (executable)

- **pm-skills (orchestrator):** `pm_goal_router.py --sample` exits 0 routing to
  `scrum-master`; `--text "audit our jira permissions"` exits 2 (single signal → ask);
  `--text "hello world"` exits 3. `jira_snapshot_bridge.py --input
  assets/sample_jira_snapshot.json --to flow --forecast 20` exits 0 and matches
  `assets/expected_flow_metrics.json` (p50=9, p85=14, p95=16 days; 90.9% SLE conformance;
  aging alert on PHX-112; forecast p85 = 10 weeks, sampled over zero-filled observed
  weeks); `--to sprint` output runs
  `velocity_analyzer.py` to exit 0 (avg 11.8 pts over 4 sprints); a 2-sprint snapshot
  exits 5. `delivery_loop_gate.py --sample` exits 0; sample plan passes `--mode plan`
  (exit 0) and is refused by `--mode close` (exit 4, T2 in_progress).
- **scrum-master:** existing fixture contract holds — velocity_analyzer on
  `assets/sample_sprint_data.json` reports avg 20.2 pts on 6 sprints.
- **atlassian-admin:** each VERIFY step names a concrete check (e.g. `GET
  /rest/api/3/user?accountId=... returns "active": false`) — keep as the domain's AR4
  exemplar.
- **Manifest truth:** `harness_manifest_builder.py --domain project-management
  --no-timestamp` produces a diff-clean `project-management.json` with `pm-skills`
  scoring all five `agentic_signals` true and 3 wired, sample-supporting tools.
