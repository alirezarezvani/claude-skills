# agent-harness

Turn any domain folder of this repo into a **bounded agentic loop**: pick up a goal,
compile it into tasks with machine-run verification, execute, verify, retry with caps,
escalate to a human when budgets exhaust, and close only when everything is verified.

```
GOAL → goal_compiler → PLAN → loop_controller: [execute → verify]* → CLOSE
                                     ↑ retry ≤ caps, changed approach
                                     └ ESCALATE — never fake success
```

## What ships

| Piece | Purpose |
|---|---|
| `scripts/harness_manifest_builder.py` | Scan a domain folder → `manifest.v1` JSON (skills, tools, checks, agentic signals) |
| `scripts/goal_compiler.py` | Goal + manifest → `plan.v1` task plan; refuses vague goals (exit 3, forcing questions) |
| `scripts/loop_controller.py` | `init/next/record/verify/close/status` state machine; controller runs checks itself |
| `assets/harnesses/*.json` | 18 committed per-domain manifests (regenerable, diff-stable) |
| `assets/harness_manifest.schema.json` | Manifest schema |
| `references/` | Agentic-loop canon, verification discipline, domain-harness design (cited) |
| `agents/harness-runner.md` | Stateless one-task-per-invocation executor |
| `commands/cs-harness.md` | `/cs:harness <domain> <goal>` end-to-end driver |

All tools are stdlib-only, pass `--help` and `--sample`, and emit JSON.

## Design lineage

Anthropic's long-running-agents harness (feature-list + stateless shifts), verifier's law,
SWE-agent's environment-feedback lesson, Ralph-loop fresh-context iteration, Cognition's
serialize-writers rule, and this repo's own tc-tracker / autoresearch locked-evaluator /
loop-library stop-state primitives. See `skills/agent-harness/references/`.
