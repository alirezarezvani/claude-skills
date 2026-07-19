# Master report — Product & PM agentic-loop audit + domain harness upgrade

**Audited:** 2026-07-03 · **Branch:** `claude/pm-audit-agentic-loops-jxurlq` ·
**Scope:** both product/project domains — `product-team/` (17 skills) and
`project-management/` (9 skills) — deep-audited on quality AND scored on the
**agentic-readiness** rubric established by the engineering audit
([../engineering-agentic-2026-07/](../engineering-agentic-2026-07/00-MASTER.md)).
Plus: both domains upgraded into **agent harnesses** — fork-orchestrators with
deterministic routers, reusable loops, machine-checkable verification gates, and
integration with the repo-wide `engineering/agent-harness` framework.

**Method:** (1) two parallel deep-dive agents read every SKILL.md, smoke-tested all 31
scripts, and cross-referenced agents/commands/manifests; (2) one explorer mapped the
repo's harness conventions (loop-library contract, agent-harness state machine,
fork-orchestrator pattern) so the upgrade reuses rather than reinvents; (3) one research
agent web-verified the 2024–2026 PM/product/harness canon
([research-digest.md](research-digest.md)).

---

## 1. The two questions

The June 2026 audit asked: does each skill earn its context window? This audit asks the
engineering follow-up question for these two domains: **can an agent pick up a goal here
and drive it to a verified close?** — and additionally: **what should these domains
teach that the 2024–2026 canon now demands?**
([improvement-fields.md](improvement-fields.md) answers the second.)

## 2. Combined scorecard (26 skills, post-PR)

| Class | product-team | project-management | Total | Meaning |
|---|---|---|---|---|
| **HARNESS-READY** (≥9, AR4≥1, AR5≥1) | 2 | 1 | **3** | An agent can loop this today |
| **LOOP-CAPABLE** (6–8) | 4 | 4 | **8** | One or two additions away |
| **TOOL-ONLY** (3–5) | 11 | 3 | **14** | Good tools, no loop spine |
| **PROSE-ONLY** (0–2) | 0 | 1 | **1** | Needs structural rebuild |

Pre-PR both domain routers were PROSE-ONLY (score ≤ 1) and neither domain had a single
`context: fork`, forcing question, iteration cap, or `/cs:*` command — they predate every
v2.8+ convention. The weakest dimensions mirror engineering exactly: **AR5 loop
discipline** (zero caps anywhere pre-PR) and **AR1 goal intake** (most skills accept any
input silently).

## 3. The three biggest findings

1. **The MCP↔analytics gap (project-management).** The domain bundles a live Jira MCP
   and ships real analytics tools, with no data path between them — sprint health and
   velocity ran on hand-typed JSON. Fixed: `jira_snapshot_bridge.py` converts saved
   `searchJiraIssuesUsingJql` results into the scrum-master schema (verified end-to-end
   into velocity_analyzer) and computes the four Kanban-Guide-2025 flow metrics + seeded
   Monte Carlo forecasts the domain never had.
2. **Verification exists but nothing binds it (both domains).** spec-to-repo's
   validator, code-to-prd's golden outputs, scrum-master's pinned fixtures,
   atlassian-admin's 7 VERIFY steps — good gates, all optional, none looped. Fixed at
   the orchestration layer: plans are gated before execution and closes are refused
   (exit 4) while tasks are unverified/unwaived; per-skill binding is follow-up F3.
3. **The canon moved (both domains).** No continuous-discovery cadence, no OST
   discipline, no AI-feature evals, no flow metrics, no probabilistic forecasting, no
   agentic-delegation governance, and 60 of 64 reference files cite zero sources. This
   PR ships the two highest-leverage tool fields per domain plus six cited reference
   docs; the remaining 14 fields are enumerated with tool specs in
   [improvement-fields.md](improvement-fields.md).

## 4. What this PR ships: two domain harnesses

Both prose routers were rebuilt as `context: fork` orchestrators that plug into
`engineering/agent-harness` (manifests regenerated; both orchestrators now score all
five `agentic_signals`):

**project-management → `pm-skills`** — the *delivery loop*:
`pm_goal_router.py` (8 lanes, exit 0/2/3 — route/ask/refuse) ·
`jira_snapshot_bridge.py` (MCP snapshot → flow metrics | sprint schema; SLE conformance,
aging-WIP alerts, `--forecast` Monte Carlo, refuses thin history) ·
`delivery_loop_gate.py` (delegation governance G1–G6: human owner, reviewer for agent
tasks, machine-checkable acceptance, evidence-before-done, close refusal,
exhausted-budget-is-escalation). Five reusable PM loops (sprint-flow, health,
retro-action, RAID-hygiene, comms) documented with terminal states. Agent
`cs-pm-orchestrator`; commands `/cs:pm`, `/cs:grill-pm`, `/cs:pm-loop`.

**product-team → `product-skills`** — the *discovery loop*:
`product_goal_router.py` (16 lanes incl. the 4 standalone plugins) ·
`discovery_cadence_tracker.py` (Torres weekly-habit scoring: streak, coverage, outcome
linkage, test throughput → health 0–100 with named gaps and a `next_loop_action`) ·
`ost_linter.py` (O1–O5: measurable outcome root, needs-not-features, ≥2 solutions per
target, tests per solution, no orphan solutions — exit 2 blocks the tree from driving a
roadmap). Graduation stop-states hand validated assumptions to experiment-designer/PRD.
Agent `cs-product-orchestrator`; commands `/cs:product`, `/cs:grill-product`,
`/cs:product-loop`.

Also fixed: the two CLI-noncompliant product tools (`user_story_generator.py`,
`persona_generator.py` — real argparse `--help`, seeded determinism, backward-compatible
positionals); domain CLAUDE.md counters; plugin manifests + marketplace descriptions.

All 8 new/changed tools pass `--help` and `--sample`; fixtures pinned
(`expected_flow_metrics.json`; sample OST with two planted violations). Every design
decision traces to the loop-library contract, the agent-harness invariants (locked
gates, evidence-before-status, budgets-as-terminal-states), and the cited canon.

## 5. Per-domain reports

- [product-team.md](product-team.md) — 17 skills, AR table, 7 domain findings,
  executable verification criteria.
- [project-management.md](project-management.md) — 9 skills, AR table, 6 domain
  findings, executable verification criteria.
- [improvement-fields.md](improvement-fields.md) — the per-field improvement rollup
  (11 cross-domain/delivery/product fields shipped or specced + documentation debt).
- [research-digest.md](research-digest.md) — the web-verified 2024–2026 canon.
- [RUBRIC.md](RUBRIC.md) — the AR rubric as applied here.

## 6. Recommended follow-up PRs (in leverage order)

1. **Loop-cap sweep** — one-sentence caps in scrum-master, jira-expert, code-to-prd,
   research-summarizer (~4 skills → HARNESS-READY).
2. **Bind the gates** — make spec-to-repo's validator and code-to-prd's goldens
   *required*; name the bridge in scrum-master/senior-pm SKILL.mds.
3. **AI-evals tool** (F–h) — eval-spec linter + kappa calculator; the single
   most-demanded missing PM competency.
4. **Path-B completion** — meeting-analyzer scripts (its spec is deterministic math),
   team-communications linter, product-discovery references.
5. **Documentation truth** — product-team README (3 conflicting counts, 9 broken paths),
   project-management legacy trio, citation back-fill (F9/F10).
6. **Remaining improvement fields** — DORA/EBM/pre-mortem/RACI (delivery); NSM/PLG
   bands/WSJF/ODI/taxonomy linter (product), per the specs in improvement-fields.md.
