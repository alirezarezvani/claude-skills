# agent-launcher-orchestrator

`context: fork` goal router for the agent-launcher plugin. Reads the per-session
goal (`./my-agent/goal.json`), routes deterministically to a phase sub-skill, and
compiles the goal+phase into an execution shape (single-pass workflow / bounded
grade→iterate loop / recurring cron deployment loop).

## Usage

```bash
# manage the goal
python3 scripts/goal_state.py init --goal "Triage my inbox every morning"
python3 scripts/goal_state.py status
python3 scripts/goal_state.py advance

# route (exit 0 route / 3 ask / 4 refuse)
python3 scripts/goal_router.py --out-dir ./my-agent

# compile the loop/workflow
python3 scripts/loop_compiler.py --out-dir ./my-agent --max-iterations 5
```

## Tools

| Tool | Purpose |
|---|---|
| `goal_state.py` | init/set/status/advance `./my-agent/goal.json` |
| `goal_router.py` | goal → phase lane (exit-code route/ask/refuse) |
| `loop_compiler.py` | goal+phase → `plan.v1` (single-pass / grade-iterate / cron-loop) |

Shared references live at the domain level: [`../../references/`](../../references/)
(see `session-goal-model.md` and `loops-and-workflows.md`). All tools are
stdlib-only and make no network calls. See [`SKILL.md`](SKILL.md) for the full
workflow and forcing questions.
