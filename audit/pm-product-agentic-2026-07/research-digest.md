# Research digest — the 2024–2026 canon behind this audit

Web-verified 2026-07-03. Full citations inline; this digest is the source layer for
[improvement-fields.md](improvement-fields.md) and the six new reference docs shipped
into the two orchestrators.

## Product management: where the canon moved

1. **Discovery became a weekly operating rhythm.** Torres (*Continuous Discovery
   Habits*; producttalk.org/opportunity-solution-trees) reframed discovery as weekly
   customer touchpoints anchored to one outcome, with the OST as the structural artifact
   and assumption tests (Bland, *Testing Business Ideas*) as the unit of progress.
2. **The org-level frame is the product operating model.** Cagan's *Transformed* (SVPG,
   2024): empowered teams, outcomes over output, innovation over predictability — 20
   first principles (svpg.com/the-product-operating-model-an-introduction).
3. **Evals are the new PRD for AI features** — the consensus 2025 AI-PM competency:
   golden set + rubric + guardrail SLOs before building (Lenny's Newsletter "Beyond vibe
   checks"; Braintrust "Evals for PMs"; Aakash Gupta "AI Evals"); model cards for the
   buyer-facing half (Mitchell et al., arxiv.org/abs/1810.03993).
4. **Metrics spine: North Star + input tree** (Amplitude, *The North Star Playbook*),
   with PLG benchmark bands for verdicts (ProductLed; OpenView: activation median ~17%,
   best-in-class 33–50%+; free→paid median ~9%, PQL-driven 25–30%).
5. **Prioritization is a bracket, not a framework**: RICE (steady state) + WSJF/cost of
   delay (Reinertsen; SAFe WSJF + Yip's false-precision critique) + ODI opportunity
   scoring (Ulwick). Sensitivity analysis counters the documented WSJF failure mode.
6. **Analytics practice is taxonomy-first** (PostHog product-analytics best practices):
   naming discipline and tracking-plan review before any metric above it.

## Project management / delivery: where the canon moved

1. **Flow metrics are mandatory, not optional.** The Kanban Guide (May 2025,
   kanbanguides.org) mandates exactly four measures — WIP, throughput, cycle time, work
   item age — plus an SLE; age is the leading indicator.
2. **Forecasting went probabilistic.** Vacanti (*Actionable Agile Metrics*; *When Will
   It Be Done?*; scrum.org Monte Carlo guidance): sample historical throughput, answer
   with p50/70/85/95 ranges, never a date; refuse thin history.
3. **DORA 2025** (dora.dev/dora-report-2025) replaced elite/high/medium/low with seven
   team archetypes over eight measures; core finding: AI **amplifies** existing org
   strengths/dysfunctions (individual output up ~98% more merged PRs, org delivery flat
   without enabling capabilities). SPACE (Forsgren/Storey, ACM Queue) remains the
   multi-dimension corrective; EBM (scrum.org) the value-measurement frame.
4. **Risk practice:** Klein's pre-mortem (HBR 2007, ~30% better risk identification);
   RAID hygiene as a linting problem; derived health vs self-reported RAG to catch
   watermelon projects.
5. **Async-first delivery:** GitLab handbook (handbook.gitlab.com, asynchronous work) —
   written 3-question standups 3–5 min vs 15–30 sync; ~37% meeting-hour reduction. Moghe,
   *The Async-First Playbook* (2023).
6. **The vendors shipped agentic PM.** Atlassian Rovo GA'd agents in Jira (assignable,
   @mentionable, "every action logged and auditable", Teamwork Graph 150B+ connections,
   MCP access — atlassian.com/software/rovo; Team '26 coverage, SiliconANGLE 2026-05-06).
   Linear shipped the accountability pattern: agent as contributor, **human stays
   primary assignee** (linear.app/agents; changelog 2026-03-24).

## Agentic harness design principles (applied in this PR)

1. **Workflows first, agents when needed** — Anthropic, "Building Effective Agents"
   (anthropic.com/research/building-effective-agents): prompt chaining, routing,
   parallelization, orchestrator-workers, evaluator-optimizer; the last "when there are
   clear evaluation criteria and iterative refinement provides measurable value."
   → The routers are workflows; the loops engage only for goals with fresh feedback.
2. **Definition-of-done must be machine-checkable; never trust self-report** — the
   plan→act→verify(deterministic)→reflect shape. → G3/G4 in `delivery_loop_gate.py`;
   OST linter exit codes; agent-harness's evidence rule.
3. **Budgets and stop conditions are first-class** — max iterations, attempt caps,
   escalation on confidence loss; otherwise reflection is infinite retry. → 3/12 caps,
   G6, terminal-state taxonomy (loop-library: success, clean no-op, blocked,
   approval-required, exhausted, stagnated).
4. **Human accountability stays attached to delegated work** (Linear; Rovo audit
   discipline). → G1/G2; no un-reviewed Jira transitions; admin actions are
   approval-required states.
5. **Context via structured interfaces, not prompt-stuffing** (Teamwork Graph / MCP;
   Anthropic's ACI emphasis). → snapshot-file pattern: every loop iteration is
   executable by a fresh session from files.
6. **Evaluator-optimizer pairs with PM-owned evals** — the golden set + rubric IS the
   evaluator's criteria; the loop may never edit the gate it is judged by (this repo's
   autoresearch locked-evaluator invariant, generalized).
