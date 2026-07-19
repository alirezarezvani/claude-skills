# Improvement fields — where investment moves each domain most

Research-backed rollup (sources in [research-digest.md](research-digest.md)) of the
fields where the 2024–2026 canon moved past the two domains' current coverage, ordered
by leverage. Fields marked ✅ shipped in this PR; the rest are the follow-up work list,
each with what a deterministic stdlib tool computes.

## Cross-domain (the harness fields)

- **F1 — Loop discipline (AR5)** ✅ *(orchestrator layer)* / open *(per skill)*. Both
  domains had zero iteration caps or stop conditions. Shipped: the two orchestrators
  carry budgets (3 attempts/task, 12 iterations/goal), named terminal states, and close
  refusal. Open: the one-sentence cap pattern ("max N fix-rerun cycles, then escalate")
  ported into scrum-master, jira-expert, code-to-prd, research-summarizer — the four
  skills one sentence away from HARNESS-READY.
- **F2 — Goal intake (AR1)** ✅ *(routers)* / open *(per skill)*. Both routers refuse
  fuzz with exit codes (2/3); grill commands lock decisions before execution. Open:
  refuse-on-missing-inputs blocks in the 14 tool-rich skills that still accept anything.
- **F3 — Bind existing gates** — open, cheapest wins: spec-to-repo's validator and
  code-to-prd's goldens exist but aren't *required*; scrum-master/senior-pm SKILL.mds
  should name the bridge as their data path (one line each).

## Project-management (delivery) fields

| # | Field | Status | Deterministic tool |
|---|---|---|---|
| F4 | Four Kanban flow metrics + SLE + aging-WIP alerts (Kanban Guide 2025) | ✅ `jira_snapshot_bridge.py --to flow` | WIP, throughput, cycle p50/85/95, work-item age, SLE conformance |
| F5 | Monte Carlo probabilistic forecasting (Vacanti; replaces story-point dates) | ✅ `--forecast N` (seeded; refuses < 10 items) | p50/70/85/95 week ranges |
| F6 | Agentic delegation governance (Linear/Rovo model) | ✅ `delivery_loop_gate.py` | owner/reviewer/acceptance/evidence/close rules G1–G6 |
| F–a | DORA 2025 archetypes + AI-amplifier capabilities check | open | four keys from deploy/incident logs → archetype + enabling-capabilities score |
| F–b | EBM (Scrum.org) four Key Value Areas scorecard | open | map existing metrics → KVA coverage, flag empty CV/UV |
| F–c | Pre-mortem processor (Klein) + RAID hygiene linter | open (playbook documents the loops) | cluster failure reasons → owned risk entries; staleness/owner/mitigation lint |
| F–d | Derived project health vs self-reported RAG ("watermelon" diff) | partial (senior-pm dashboard + bridge signals) | composite from schedule variance, aging WIP, scope churn — diffed against RAG |
| F–e | Async-first meeting audit (GitLab canon) | open | calendar export → async-convertibility classes, recoverable hours |
| F–f | Agent-readiness audit of Jira hygiene (Rovo-era) | open | field completeness %, acceptance-criteria presence, stale statuses → delegation-readiness score |
| F–g | RACI validator | open | exactly-one-A, ≥1 R, overload histogram |

## Product-team fields

| # | Field | Status | Deterministic tool |
|---|---|---|---|
| F7 | Continuous-discovery cadence (Torres weekly habit) | ✅ `discovery_cadence_tracker.py` | streak, coverage, outcome linkage, test throughput → health 0–100 |
| F8 | Opportunity Solution Tree structural linting | ✅ `ost_linter.py` | rules O1–O5 (measurable root, needs-not-features, ≥2 solutions, tests, no orphans) |
| F–h | **AI-feature evals as the PRD quality contract** — the single biggest gap per every 2025–2026 source | reference shipped (`ai_product_evals.md`); tool open | eval-spec linter: golden-set floors, rubric pass-criteria, guardrail SLOs; Cohen's kappa on grader agreement |
| F–i | WSJF / cost-of-delay with rank-stability sensitivity (brackets RICE) | reference shipped (`product_operating_model.md`); tool open | CoD/duration ranking; ±1-step perturbation flags rank flips |
| F–j | Opportunity scoring (Ulwick ODI importance–satisfaction) | open | Opp Score per outcome statement from survey CSV |
| F–k | North Star Metric validator + input tree (Amplitude) | open | leading/value/not-vanity checks; input→NSM correlation |
| F–l | PLG funnel benchmark bands (ProductLed/OpenView) | open | stage conversion vs calibrated bands → weakest-stage verdict |
| F–m | Product operating model maturity (Cagan *Transformed*) | open | questionnaire → per-principle 0–100 gap list |
| F–n | Event-taxonomy / tracking-plan linter (PostHog-era) | open | snake_case, verb allowlist, near-duplicate detection |
| F–o | JTBD switch-interview force coder (Moesta) | open | four-forces lexicon coding, force balance per interview |
| F–p | Story-map validator (Patton) | open | every story on the backbone; slices span end-to-end |
| F–q | Model-card completeness checker (Mitchell et al.) | open | nine canonical sections → completeness % |

## Documentation-debt fields

- **F9 — Source citations**: 60 of 64 pre-PR reference files across both domains cite
  zero sources (six new references cite 6–7 each). Back-fill priority: scrum-master and
  senior-pm references (the canon exists — Vacanti, Kanban Guide, DORA, PMBOK).
- **F10 — Counter/path truth**: product-team README (3 conflicting counts, 9 broken
  paths), project-management legacy trio (README / IMPLEMENTATION_SUMMARY /
  REAL_WORLD_SCENARIO all say "6 skills"), `.codex/instructions.md` broken paths in both
  domains. Domain CLAUDE.mds fixed this PR.
- **F11 — Path-B completion**: meeting-analyzer (0 scripts/refs/assets — its own spec is
  deterministic math), team-communications (0 scripts, 155 lines of references),
  product-discovery (1 reference), 8 asset-less product skills.
