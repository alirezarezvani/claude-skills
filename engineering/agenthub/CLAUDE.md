# AgentHub — Claude Code Instructions

This plugin enables multi-agent collaboration. Spawn N parallel subagents that compete on the same task, evaluate results, and merge the winner.

## Commands

Claude Code namespaces these commands by the plugin name, `/agenthub:<name>`. The `hub-*` names are unique, so their bare forms work; the generic ones (`spawn`, `eval`, `merge`, `board`) use the namespaced form:

- `/hub-init` — Create a new collaboration session (task, agent count, eval criteria)
- `/agenthub:spawn` — Launch N parallel subagents in isolated worktrees (supports `--template`)
- `/hub-status` — Show DAG state, agent progress, and branch status
- `/agenthub:eval` — Rank agent results by metric or LLM judge
- `/agenthub:merge` — Merge the winning branch, archive losers
- `/agenthub:board` — Read/write the agent message board
- `/hub-run` — One-shot lifecycle: init → baseline → spawn → eval → merge

## How It Works

You (the coordinator) orchestrate N subagents working in parallel:

1. `/hub-init` — define the task, number of agents, and evaluation criteria
2. `/agenthub:spawn` — launch all agents simultaneously via the Agent tool with `isolation: "worktree"`
3. Each agent works independently in its own git worktree, commits results, writes to the board
4. `/agenthub:eval` — compare results (run eval command per worktree, or LLM-judge diffs)
5. `/agenthub:merge` — merge the best branch into base, tag and archive the rest

## Key Principle

**Parallel competition. Immutable history. Best result wins.**

Agents never see each other's work. Every approach is preserved in the git DAG. The coordinator evaluates objectively and merges only the winner.

## Agents

- **hub-coordinator** — Dispatches tasks, monitors progress, evaluates results, merges winner. This is YOUR role as the main Claude Code session.

## Branch Naming

```
hub/{session-id}/agent-{N}/attempt-{M}
```

## Message Board

Agents communicate via `.agenthub/board/` markdown files:
- `dispatch/` — task assignments from coordinator
- `progress/` — status updates from agents
- `results/` — final result summaries from agents

## When to Use

- User says "try multiple approaches" or "have agents compete"
- Optimization tasks where different strategies might win
- Code generation where diversity of solutions helps
- Competing content drafts — 3 agents write blog posts or landing page copy, LLM judge picks best
- Research synthesis — agents explore different source sets or analytical frameworks
- Process optimization — agents propose competing workflow improvements
- Feature prioritization — agents build different RICE/ICE scoring models
- Any task that benefits from parallel exploration
