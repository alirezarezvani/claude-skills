---
name: yylo-ledger-tasks
description: "Run coding-agent work on a git-native Kanban ledger: create/search/mark tasks with mandatory response receipts, manage blocked_by dependency graphs, compute ready queues and topological work order, and consolidate scattered boards — all state stored as hash-chained Markdown inside the repository. Use when the user asks to 'track this feature as a task', 'what's ready to work on', 'mark this task done', wants durable cross-session task state for coding agents, or needs dependency-aware ordering for parallel agent worktrees. NOT for ephemeral in-session todo lists (use Claude Code's built-in todo tool), CI pipeline authoring (workflow-builder), or delegating subtasks to other agent CLIs (hivemind)."
---

# YYLO Ledger Tasks: Git-Native Kanban for Coding Agents

Tasks live in the repository as hash-chained Markdown, so every status change leaves
an auditable receipt that diffs, reviews, and rolls back like any other file. The
ledger is the durable memory between agent sessions: pick up exactly where the last
session stopped, with dependency state intact.

## Prerequisites (external dependency)

This skill is a thin workflow layer over **YYLO**, a third-party MIT-licensed CLI.
It is not bundled — install it yourself first:

| Requirement | Notes |
|---|---|
| Node.js >= 18 | The `yy` CLI is an npm package. |
| `yy` CLI on `PATH` | `npm i -g @yylo/cli`. |
| A repository with a `.juno_task/` controller | Run `yy init` once in the repo that owns task state. |

Canonical home: <https://github.com/yylo-dev/yylo> (MIT). This skill is a snapshot
adapted from the official skills pack (<https://github.com/yylo-dev/yylo-skills>);
fixes land there first. Verify the installed surface with `yy ledger --help` before
relying on any command below — the CLI version-gates its namespaces.

## Task lifecycle

Status flow: `backlog → todo → in_progress → done` (or `archive` for abandoned work).
Every mutation is routed through `yy ledger` — never edit `.juno_task/` files by hand;
the hash chain makes hand edits detectable and untrustworthy.

### CREATE — add a task

```bash
yy ledger create "Implement OAuth token refresh" --status backlog --tags feature,backend
```

Options: `--status` (backlog|todo|in_progress|done), `--tags`, `--blocked-by` (task
IDs), `--related-tasks` (task IDs). Dependencies can also be declared inline in the
body (see below).

### LIST / SEARCH — inspect the board

```bash
yy ledger list --status todo,in_progress --limit 10 --sort asc
yy ledger search --status todo --tag backend --limit 10
yy ledger search --body "OAuth" --open
```

Filters: `--status`, `--tag`, `--body`, `--commit`, `--open` (awaiting a response),
`--recent`, `--exclude`.

### GET / MARK / UPDATE / ARCHIVE — move work forward

```bash
yy ledger get TASK_ID                          # full detail + resolved dependencies
yy ledger mark in_progress --id TASK_ID --response "Starting: repro'd the bug"
yy ledger mark done --id TASK_ID --response "Implemented refresh; tested expiry path" --commit abc123def
yy ledger update TASK_ID --tags backend,urgent
yy ledger archive TASK_ID                      # soft delete, data preserved
```

`mark` **requires** `--response` — a one-line receipt of what was done and how it was
verified. Attach `--commit HASH` when marking done so the ledger links to git history.

## Dependency management

```bash
yy ledger deps TASK_ID                                  # blockers + dependents + priority score
yy ledger deps add --id TASK_ID --blocked-by BLOCKER1 BLOCKER2
yy ledger deps remove --id TASK_ID --blocked-by BLOCKER1
yy ledger ready                                         # unblocked tasks (backlog/todo/in_progress)
yy ledger order --scores                                # topological sort for safe parallelism
```

Cycle detection prevents circular dependencies automatically. `ready` returns tasks
whose `blocked_by` set is fully done/archived; `order` extends this to a full
execution sequence — use it to plan parallel pipelines.

Inline body markup is parsed at create/update time:

```
[blocked_by]TASK_ID[/blocked_by]     — this task waits on TASK_ID
[task_id]RELATED_ID[/task_id]        — cross-reference related work
```

## Merge (multi-directory consolidation)

When task state scatters across subdirectories, plan first, apply second:

```bash
yy ledger merge ./sub1/.juno_task ./sub2/.juno_task --into ./.juno_task \
  --dry-run --plan-file /tmp/ledger-merge-plan.json
yy ledger merge ./sub1/.juno_task ./sub2/.juno_task --into ./.juno_task \
  --apply-plan /tmp/ledger-merge-plan.json --receipt-file /tmp/ledger-merge-receipt.json
```

Never apply a plan you have not read. Failures fail closed — resolve and re-plan.

## Output formats

All commands accept `-f json|ndjson|table|xml` (ndjson default), `--raw` for compact
output, `-p` for pretty-print. Prefer `-f json` when piping into other tooling.

## Workflow pattern (opinionated)

1. **Size tasks small** — one task should complete in one agent iteration without
   flooding the context window.
2. **Plan dependencies up front** — declare `blocked_by` at create time; the board
   computes readiness, you never track it mentally.
3. **Pull, don't guess** — run `ready` before starting work; start only unblocked
   tasks.
4. **Sequence parallelism** — `order --scores` gives the safe parallel execution
   order across concurrent agent worktrees.
5. **Close with evidence** — every `mark done` carries a `--response` receipt and a
   `--commit` hash. A done task without a commit is an unverified claim.

## Anti-patterns

| Anti-pattern | Why it breaks | Do this instead |
|---|---|---|
| Editing `.juno_task/` Markdown files directly | Bypasses the hash chain — hand-edited state is detectable and untrustworthy | Route every mutation through `yy ledger` |
| `mark done` without `--response`/`--commit` | The receipt is the audit trail; a bare status flip is unverifiable | Always include both — what you did, and the commit that proves it |
| Starting a task without checking `ready` | Blocked tasks create rework when their blockers change underneath them | `yy ledger ready` first; start only unblocked rows |
| Creating one giant task for a whole feature | Blows the context window; done/in_progress granularity disappears | Split into dependency-linked tasks sized to one iteration |
| Reading stale board state before mutating | Concurrent sessions may have advanced the board | `list`/`get` immediately before the mutation, then mark |
| Trusting an unreviewed merge plan | Consolidation moves state en masse | Always `--dry-run`, read the plan file, then `--apply-plan` |
| Using the ledger for in-session scratch todos | Hash-chained receipts are overkill for ephemeral lists; pollutes history | Use Claude Code's built-in todo tool for session-local items |

## Cross-references

- `engineering/agent-harness` — wrap this ledger in a bounded verify-retry loop for
  fully agentic execution
- `engineering/hivemind` — delegate ledger-tracked subtasks to parallel worker agents
- `engineering/workflow-builder` — deterministic pipelines that should NOT depend on
  agent judgment (and therefore not on this ledger)
- `engineering/handoff` — session-to-session context transfer; this ledger is the
  durable task-state half of a handoff
