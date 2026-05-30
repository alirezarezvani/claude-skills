# Feature Flags Architect

End-to-end discipline for feature flags: classify, ship, ramp, retire.

Most teams treat flags as throwaway `if`-statements. This skill treats them as a controlled lifecycle with measurable debt — and ships the tools to enforce it.

## What's inside

- **3 stdlib Python tools** — flag debt scanner, rollout planner, kill-switch auditor
- **4 reference docs** — taxonomy, provider comparison, rollout strategies, lifecycle
- **/flag-cleanup slash command** — runs the full quarterly cleanup workflow
- **Asset template** — feature flag request form

## Install

### Claude Code

```bash
# Via Claude Code marketplace
/plugin install feature-flags-architect

# Or clone the repo
git clone https://github.com/alirezarezvani/claude-skills.git
cd claude-skills/engineering/feature-flags-architect
```

### Other tools (Codex CLI, Cursor, Antigravity, OpenCode, Gemini CLI)

The skill ships with a `context: fork` SKILL.md, so it loads via the standard skill mechanism each tool supports. See cross-tool compatibility in the SKILL.md frontmatter.

## Quick start

```bash
SKILL=engineering/feature-flags-architect/skills/feature-flags-architect

# Audit your repo for stale flags
python "$SKILL/scripts/flag_debt_scanner.py" --repo . --max-age-days 90

# Plan a phased rollout
python "$SKILL/scripts/rollout_planner.py" --population 100000 --target-percent 100 --duration-days 14 --strategy ring

# Verify every flag has a kill switch
python "$SKILL/scripts/kill_switch_audit.py" --repo . --flag-doc docs/feature-flags.md
```

## When to use

- Adding a new flag and need a rollout plan
- Auditing a codebase for orphaned or stale flags
- Choosing a flag provider (LaunchDarkly vs GrowthBook vs Statsig vs Unleash vs Flipt vs DIY)
- Designing a kill-switch path for a risky launch
- Cleaning up flag debt before a release freeze

## Key principles

1. **Flags are a lifecycle**, not an `if`-statement: `request → design → ship → ramp → cleanup → archive`
2. **4 flag types** with different lifespans: Release / Experiment / Operational / Permission
3. **Every flag has a documented kill switch** — owner, type, trigger, dashboard
4. **Rollout strategy by risk**, not preference (ring for risky, linear for medium, log for low)
5. **Quarterly cleanup is non-negotiable** — debt compounds

## Skill structure

```
feature-flags-architect/
├── README.md                              # this file
├── .claude-plugin/plugin.json             # 8-field plugin manifest
└── skills/feature-flags-architect/
    ├── SKILL.md                           # main skill spec
    ├── scripts/
    │   ├── flag_debt_scanner.py           # find stale flags
    │   ├── rollout_planner.py             # generate phased schedule
    │   └── kill_switch_audit.py           # verify documentation
    ├── references/
    │   ├── flag_taxonomy.md               # 4 types decision tree
    │   ├── provider_comparison.md         # LD/GB/Statsig/Unleash/Flipt/DIY
    │   ├── rollout_strategies.md          # ring/linear/log/cohort
    │   └── flag_lifecycle.md              # 6-phase lifecycle
    └── assets/
        └── flag_request_template.md       # PR template
```

## Verifiable success

A team using this skill should achieve:

- 100% of new flags pass `kill_switch_audit.py` at merge time
- `flag_debt_scanner.py --max-age-days 90` returns ≤5 stale flags repo-wide
- Every flag has a documented owner, type, kill switch, and dashboard
- Mean time to retire a Release flag: <60 days from 100% rollout

## License

MIT — see repo root LICENSE.
