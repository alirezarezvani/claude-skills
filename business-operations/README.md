# business-operations

**Internal-operations skills for BizOps leads, COO direct reports, vendor management, IT ops.**

v2.8.0 — 7 skills (orchestrator + 6 sub-skills), 18 stdlib Python tools, 24 references citing 7+ authoritative sources each.

## Skills

| Skill | Job-to-be-done |
|---|---|
| [`business-operations-skills`](skills/business-operations-skills/) | Orchestrator — routes to the right sub-skill via `context: fork` + Matt Pocock grill discipline |
| [`process-mapper`](skills/process-mapper/) | "Where does the work spend most of its time waiting?" — BPMN + bottleneck + cycle-time |
| [`vendor-management`](skills/vendor-management/) | "Is this vendor delivering, and what's the risk if they fail?" — scorecard + SLA + risk |
| [`capacity-planner`](skills/capacity-planner/) | "Are we sized to peak demand without burning the team?" — Erlang-C + utilization + hiring sequence |
| [`internal-comms`](skills/internal-comms/) | "How do I announce a re-org / rollout / policy change?" — ADKAR + Kotter 8-step |
| [`knowledge-ops`](skills/knowledge-ops/) | "Is our company wiki actually usable?" — SOP + runbook + KB hygiene |
| [`procurement-optimizer`](skills/procurement-optimizer/) | "Why is software spend up 40% YoY?" — UNSPSC spend categorization + supplier consolidation |

## Commands

- `/cs:bizops <inquiry>` — top-level router
- `/cs:grill-bizops <plan>` — Matt Pocock-style docs-anchored grilling
- `/cs:process-map`, `/cs:vendor-review`, `/cs:capacity-plan`, `/cs:internal-comms`, `/cs:knowledge-ops`, `/cs:procurement` — direct per-skill invocation

## Agent

- `cs-bizops-orchestrator` — process-obsessed BizOps lead persona

## Distinct from

- `business-growth/` — external sales motion (CSM, sales engineering)
- `c-level-advisor/coo-advisor` — strategic COO judgment (not tactical operations)
- `c-level-advisor/vpe-advisor` — engineering throughput (capacity-planner is for non-eng ops)
- `engineering/slo-architect` — system reliability (not business-process reliability)
- `engineering/llm-wiki` — personal PKM (not company SOPs)
- `engineering-team/runbook-generator` — system-ops runbooks (knowledge-ops is org-wide SOPs+runbooks)

## License

MIT
