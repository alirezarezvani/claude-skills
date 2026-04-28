# AgentHub — Multi-Agent Collaboration for Claude Code

AgentHub spawns N parallel agents in isolated git worktrees to compete on the same task, then evaluates results by metric or LLM judge and merges the winner. It turns any optimization, refactoring, content generation, or design problem into a tournament where the best solution wins.

## Quick Start

```bash
# One command — full lifecycle
/hub:run --task "Reduce p50 latency" --agents 3 \
  --eval "pytest bench.py --json" --metric p50_ms --direction lower \
  --template optimizer
```

Or step by step:

```bash
# 1. Initialize a session — define the task, agent count, and evaluation criteria
/hub:init --task "Reduce API p50 latency" --agents 3 \
  --eval "pytest bench.py --json" --metric p50_ms --direction lower

# 2. Spawn agents — launches 3 parallel agents in isolated worktrees
/hub:spawn --template optimizer

# 3. Check progress
/hub:status

# 4. Evaluate — rank agents by metric
/hub:eval

# 5. Merge the winner into your branch
/hub:merge
```

## Commands Reference

| Command | Purpose | Example |
|---------|---------|---------|
| `/hub:init` | Create session with task, agents, eval criteria | `/hub:init --task "Optimize DB queries" --agents 4 --eval "python bench.py" --metric query_ms --direction lower` |
| `/hub:spawn` | Launch all agents in parallel worktrees | `/hub:spawn` (uses latest session) |
| `/hub:status` | Show DAG state, branches, progress posts | `/hub:status` |
| `/hub:eval` | Rank results by metric or LLM judge | `/hub:eval --judge` (LLM judge mode) |
| `/hub:merge` | Merge winner, archive losers, cleanup | `/hub:merge --agent agent-2` (force pick) |
| `/hub:board` | Read/write the message board | `/hub:board --read progress` |
| `/hub:run` | One-shot full lifecycle | `/hub:run --task "Reduce latency" --agents 3 --eval "pytest bench.py" --metric p50_ms --direction lower --template optimizer` |

## The Optimizer Pattern

AgentHub's most powerful pattern: N agents compete using different strategies, each running an iterative improvement loop in its own worktree.

### How It Works

```
/hub:run --task "Reduce p50 latency" --agents 3 \
  --eval "pytest bench.py --json" --metric p50_ms --direction lower \
  --template optimizer
```

Each agent follows the same loop independently:

```
┌─── Agent 1 (worktree) ──────────────────────────┐
│  Strategy: Caching                              │
│  Loop: edit → eval → keep/discard → repeat ×10  │
└─────────────────────────────────────────────────┘
┌─── Agent 2 (worktree) ──────────────────────────┐
│  Strategy: Algorithm optimization               │
│  Loop: edit → eval → keep/discard → repeat ×10  │
└─────────────────────────────────────────────────┘
┌─── Agent 3 (worktree) ──────────────────────────┐
│  Strategy: I/O batching                         │
│  Loop: edit → eval → keep/discard → repeat ×10  │
└─────────────────────────────────────────────────┘
```

The `optimizer` template embeds the iteration loop directly in each agent's dispatch prompt — no external dependencies required.

### Agent Templates

Templates define the dispatch prompt pattern. Use `--template` with `/hub:spawn` or `/hub:run`:

| Template | Pattern | Use Case |
|----------|---------|----------|
| `optimizer` | Edit → eval → keep/discard → repeat x10 | Performance, latency, size reduction, content quality, research depth |
| `refactorer` | Restructure → test → iterate until green | Code quality, tech debt, document restructuring |
| `test-writer` | Write tests → measure coverage → repeat | Test coverage gaps |
| `bug-fixer` | Reproduce → diagnose → fix → verify | Bug fix with competing approaches |

Templates live in `references/agent-templates.md`.

### Example: 3 Strategies Competing on API Latency

```bash
/hub:run --task "Reduce API p50 latency below 150ms" --agents 3 \
  --eval "pytest bench.py --json" --metric p50_ms --direction lower \
  --template optimizer
```

AgentHub automatically:
1. Captures baseline (e.g., `p50_ms = 180ms`)
2. Assigns diverse strategies (caching, algorithm, I/O batching)
3. Spawns 3 agents — each iterates up to 10 times in its worktree
4. Agents commit improvements, revert failures, post progress to the board
5. Evaluates final metrics across all agents
6. Presents ranked results for merge confirmation

```
# Example output:
# RANK  AGENT    METRIC   DELTA    FILES
# 1     agent-2  128ms    -52ms    4
# 2     agent-1  145ms    -35ms    2
# 3     agent-3  171ms    -9ms     1
```

### Example: 3 Agents Drafting Competing Blog Posts

```bash
/hub:run --task "Write a 1500-word blog post on zero-downtime deployments" \
  --agents 3 --judge
```

No eval command needed — `--judge` activates LLM judge mode. Each agent takes a different angle (tutorial, case study, opinion piece). The coordinator reads all three drafts and picks the winner by clarity, depth, and engagement.

### Power-Up: Autoresearch for Richer Tracking

If you also have the **autoresearch-agent** skill installed, agents can optionally use its tracking tools for:

- **results.tsv** — structured iteration history with timestamps and metrics
- **Strategy escalation** — start with low-hanging fruit, escalate to radical changes
- **program.md** — self-improving agent instructions that refine across iterations

This is entirely optional. The optimizer template works standalone — autoresearch just adds richer per-agent tracking if available. Both plugins remain independent; install either or both.

### Step-by-Step Walkthrough

1. **Init + Baseline** — Sets up session config with task description, agent count, eval command, and target metric. Captures baseline metric value. Creates `.agenthub/sessions/{id}/config.yaml`.

2. **Spawn** — The coordinator writes dispatch posts to `.agenthub/board/dispatch/` with strategy-specific instructions for each agent. Each agent is launched with `isolation: "worktree"` so it works on an isolated copy of the repo. When a template is used, the dispatch prompt contains the full iteration loop.

3. **Agents iterate** — Each agent independently: reads its dispatch instructions, makes changes to the target files, runs the eval command, commits improvements, reverts failures, and posts progress updates.

4. **Evaluate** — Runs `result_ranker.py` which checks out each agent's final branch, runs the eval command, extracts the metric, and produces a ranked table with deltas from baseline.

5. **Merge** — Merges the winning branch with `--no-ff`, archives loser branches as tags (`hub/archive/{session}/{agent}`), cleans up worktrees, and posts a merge summary to the board.

## Coordination Patterns

### Fan-Out / Fan-In (Default)

One coordinator spawns N agents with the same task but different strategies or constraints. All run in parallel. Results are evaluated and one winner is merged.

**Best for:** Performance optimization, competing implementations, A/B testing approaches, competing marketing copy variations.

### Tournament (Multi-Round Elimination)

Multiple rounds of fan-out/fan-in. Winners advance, losers are eliminated. Each round can narrow the strategy space.

**Best for:** Large solution spaces where you want to prune early, iterative refinement of the best approaches, multi-round content refinement.

### Ensemble (Combine All Agents' Work)

Each agent works on a *different subtask* rather than competing on the same one. Results are combined rather than compared.

**Best for:** Large refactoring tasks, multi-file changes where work can be parallelized by module, multi-section reports or whitepapers.

### Pipeline (Sequential Phases)

Agent 1's output becomes Agent 2's input. Each phase builds on the previous result.

**Best for:** Multi-stage workflows (e.g., Agent 1 writes tests, Agent 2 writes implementation, Agent 3 optimizes) or research → draft → edit pipelines.

## Scripts

| Script | Purpose | Example |
|--------|---------|---------|
| `hub_init.py` | Create session directory and config | `python scripts/hub_init.py --task "Optimize queries" --agents 3 --eval "python bench.py" --metric query_ms --direction lower` |
| `board_manager.py` | Message board CRUD (dispatch, progress, results) | `python scripts/board_manager.py --post --channel progress --author agent-1 --message "Iteration 3: p50=145ms"` |
| `session_manager.py` | Session state machine (init→running→evaluating→merged) | `python scripts/session_manager.py --list` |
| `dag_analyzer.py` | Git DAG analysis — frontier detection, branch status | `python scripts/dag_analyzer.py --status --session 20260317-143022` |
| `result_ranker.py` | Evaluate and rank agent results by metric or diff | `python scripts/result_ranker.py --session 20260317-143022 --eval-cmd "pytest bench.py --json" --metric p50_ms --direction lower` |

All scripts support `--help` for full usage and `--demo` for example output.

## Installation

### Claude Code

```bash
# Install from ClawHub
claude install agenthub

# Or add manually — copy the engineering/agenthub/ folder to your project,
# then add to your .claude/settings.json:
{
  "skills": ["./engineering/agenthub"]
}
```

### OpenAI Codex

```bash
# Copy to your agents directory
cp -r engineering/agenthub/ .codex/agents/agenthub/
```

### OpenClaw

```bash
openclaw install agenthub
```

## Architecture

### Session Model

Each `/hub:init` creates a session with a timestamp-based ID (`YYYYMMDD-HHMMSS`). Sessions progress through states:

```
init → running → evaluating → merged
                            → archived
```

State is tracked in `.agenthub/sessions/{session-id}/state.json`.

### Branch Naming

```
hub/{session-id}/agent-{N}/attempt-{M}

# Example:
hub/20260317-143022/agent-1/attempt-1
hub/20260317-143022/agent-2/attempt-1
hub/20260317-143022/agent-3/attempt-1
```

### Board Channels

The message board uses three channels stored as YAML-frontmatter markdown files:

| Channel | Direction | Purpose |
|---------|-----------|---------|
| `dispatch` | coordinator → agents | Task assignments and strategy prompts |
| `progress` | agents → coordinator | Status updates, iteration results |
| `results` | bidirectional | Final metrics, merge summaries |

### Immutability Rules

- **Append-only board** — posts are never edited or deleted
- **Append-only DAG** — no rebase, no force-push
- **Archive losers** — loser branches become tags, not deleted
- **Worktree cleanup** — removed only after merge is complete

### Directory Structure

```
.agenthub/
├── sessions/{session-id}/
│   ├── config.yaml          # Task, agents, eval criteria
│   └── state.json           # State machine, agent status
└── board/
    ├── _index.json          # Channel metadata
    ├── dispatch/            # Coordinator → agents
    ├── progress/            # Agents → coordinator
    └── results/             # Final results + merge summary
```

## License

MIT
