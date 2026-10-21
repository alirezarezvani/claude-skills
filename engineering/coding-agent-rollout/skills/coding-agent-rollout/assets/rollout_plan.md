# Claude Code rollout plan

Fill in the blanks. Each phase has an exit criterion that a script checks, so
"done" is not a matter of opinion.

| Field | Value |
|---|---|
| Rollout owner | |
| Security reviewer | |
| Seats in scope | |
| Launch date (pilot) | |
| Repos in scope | |

## Phase 1 — Guardrails (before the first seat)

- [ ] Managed settings drafted from `managed-settings.example.json` and shipped through MDM
- [ ] Secrets denied (`.env*`, keys, cloud credentials); destructive commands on `ask` or `deny`
- [ ] `disableBypassPermissionsMode: "disable"` in managed settings
- [ ] Decision recorded: telemetry (OpenTelemetry on / off) and transcript retention (`cleanupPeriodDays`)

**Exit:** `settings_linter.py --repo <each repo> --managed <managed file>` exits 0 or 2 with every WARN accepted in writing.

## Phase 2 — Inventory (before pilot)

- [ ] `approved-components.json` lists every MCP server, plugin and marketplace you allow
- [ ] Each entry passed the six-question review in `mcp_and_plugin_governance.md` §5
- [ ] Servers and marketplaces pinned

**Exit:** `mcp_plugin_inventory.py --repo <each repo> --allowlist approved-components.json` exits 0 or 2.

## Phase 3 — Instructions (pilot, 2-4 weeks)

- [ ] One shared `CLAUDE.md` per repo, under 200 lines, scoped rules in `.claude/rules/`
- [ ] `CLAUDE.local.md` gitignored
- [ ] Pilot group (3-8 people) named; weekly 15-minute feedback slot booked

**Exit:** `claude_md_layering_audit.py --repo <each repo>` has no BLOCKER and no L2 (broken import).

## Phase 4 — Adoption (expand)

- [ ] Each member runs `adoption_tracker.py --output json` monthly and shares only the JSON
- [ ] Monthly read-out: stage, active share, skills and MCP servers actually used, CLI version spread
- [ ] For a STALLED read-out: interview three inactive seats before changing policy

**Exit:** `adoption_tracker.py --merge ... --seats N` reports SPREADING or EMBEDDED.

## Decisions log

| Date | Decision | Owner | Revisit by |
|---|---|---|---|
| | | | |
