# Interview → CMA config mapping

How Phase-1 interview answers map to CMA primitives. `interview_planner.py`
implements this table deterministically.

## The six intake slots

| Slot | Question | Maps to |
|---|---|---|
| **Job** | "What one job should this agent do end-to-end?" | agent `system` + outcome `description` |
| **Trigger** | "What kicks it off — you ask it, an event, or a schedule?" | on-demand session vs event `user.message` vs `schedule.cron` deployment |
| **Inputs** | "What does it read? (files, repo, memory, third-party systems)" | `file` / `repository` / `memory_store` resources; `mcp_servers` + `vault_ids` |
| **Actions** | "What does it do? (draft, write files, call APIs, run code)" | agent toolset vs custom tools vs MCP tools + permission policy |
| **Definition of done** | "How would you grade a good run?" | outcome `rubric` (required, markdown) |
| **Recurrence** | "Does it run once, on request, or on a cadence?" | single-pass vs grade→iterate loop vs cron deployment loop |

## Mapping rules

1. **Connectors are mockable in v0.** If a real MCP server / credential isn't ready,
   default to a **custom tool** with a schema-true `input_schema` (the agent calls
   it; the founder returns a mock `user.custom_tool_result`), or to a **draft**
   action. Wire the real MCP server as **v1** when credentials arrive. Record the
   deferral with its reason and exact mechanism.
2. **Their problem, their words.** Populate `name`, `system`, and `rubric` from what
   the founder actually stated. Never invent specifics they didn't claim.
3. **Permission defaults.** Agent toolset → `always_allow`; every MCP toolset →
   `always_ask`.
4. **Networking defaults.** Start `unrestricted` for v0 cloud; tighten to `limited`
   with an explicit `allowed_hosts` list as a v1 hardening step.
5. **Memory only if run #10 should beat run #1.** Attach a `read_write` memory store
   only when the job benefits from cross-session learning; otherwise skip it (a
   store attaches only at creation and adds prompt-injection surface).
6. **Recurrence decides the loop.** once → single-pass workflow; "grade until good"
   → grade→iterate loop (`max_iterations`); "every morning / weekly" → cron
   deployment loop.

## Build-sheet shape (produced by `build_sheet_builder.py`)

```
{
  "agent_name": "...",
  "goal": "one-sentence job",
  "primitives": {
    "agent":       {"model": "...", "system": "...", "tools": [...], "mcp_servers": [...], "skills": [...]},
    "environment": {"type": "cloud", "networking": "unrestricted", "packages": {...}},
    "session":     {"resources": [...], "vault_ids": [...]},
    "outcome":     {"description": "...", "rubric": "markdown", "max_iterations": 3},
    "deployment":  {"schedule": {"expression": "0 9 * * *", "timezone": "..."}}  // optional
  },
  "deferrals": [{"version": "v1", "item": "...", "reason": "...", "mechanism": "..."}],
  "eval_plan": {"success_criteria": [...], "held_back_cases": [...]}
}
```

## Sources

1. anthropics/launch-your-agent — `interview-to-config.md`.
2. Claude Managed Agents — Overview (primitive semantics).
3. Anthropic — "Building effective agents": workflows (predefined paths) vs agents (dynamic).
4. Teresa Torres — *Continuous Discovery Habits* (interview → opportunity mapping discipline).
5. Amy Hoy / Jobs-to-be-Done — "job the customer hires the product to do".
6. Fitzpatrick, R. — *The Mom Test* (2013): asking about past behavior instead of hypotheticals — the interview questions here follow that rule.
7. Nielsen Norman Group — "User Interviews: How, When, and Why": open-ended-first sequencing behind the interview script ordering.
