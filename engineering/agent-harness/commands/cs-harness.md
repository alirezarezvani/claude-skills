---
description: Compile a goal into a verified agent-harness loop for a domain and drive it to close — /cs:harness <domain> <goal>
argument-hint: <domain> <goal text>
---

# /cs:harness — run a goal through a domain's agent harness

Parse `$ARGUMENTS`: the first token is the domain (one of the 18 manifest names under
`engineering/agent-harness/skills/agent-harness/assets/harnesses/`); the rest is the goal.
If the domain token doesn't match a manifest file, list the available manifests and ask.

## Sequence (gates are blocking — never skip forward)

1. **Compile** —
   `python3 engineering/agent-harness/skills/agent-harness/scripts/goal_compiler.py --goal "<goal>" --manifest engineering/agent-harness/skills/agent-harness/assets/harnesses/<domain>.json --out .agent-harness/plan.json`
   - Exit 3: relay the forcing questions to the user one at a time (recommended answer
     first), then recompile with the enriched goal. Do not proceed on a vague goal.
   - Exit 4: show `nearest_candidates`, ask whether to switch domain or refine the goal.
2. **Review the plan with the user** — show tasks, verifications, and caps. Confirm before
   initializing: this is the only approval gate in the loop.
3. **Init** — `python3 .../scripts/loop_controller.py init --plan .agent-harness/plan.json --state .agent-harness/state.json`
4. **Drive** — repeat: `next` → execute the task per its skill's SKILL.md → `record` →
   `verify`. For long goals, spawn the `harness-runner` agent per task instead of executing
   inline, one at a time (writes stay serialized).
5. **On exit 2 or 5** — stop, show `status` and the failing evidence; the user decides:
   fix and continue, waive with a reason, or abandon.
6. **Close** — `close --state .agent-harness/state.json`; paste the handoff block
   (tasks, statuses, evidence, waivers) as the deliverable summary.

## Rules

- Never edit checks, manifests, or the plan mid-loop to make verification pass.
- Never report an exhausted budget as success.
- `.agent-harness/` is git-ignorable working state; the handoff block is the record.
