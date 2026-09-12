---
name: "agent-run-forensics"
description: "Answer questions about a past agent run from its recording instead of from memory - which step changed a file, why a command ran, where the build broke - and replay or fork that run offline. Use when someone asks why an earlier run did something, or whether a recorded failure still reproduces."
---

# Agent Run Forensics

## Overview

A recording is evidence. Your memory of a session is not, and neither is a transcript you were
handed - both are missing the tool results, the exit codes, and the files that changed without
anyone mentioning them.

**The rule: when a question is about something that already happened, read the trace before you
answer.** Do not reconstruct it. If a recording exists, guessing is the wrong move even when the
guess would have been right.

Use this skill when the question is about the past:

- "Why did you delete / overwrite / move X?"
- "What changed this file?" / "Which step broke the build?"
- "Can you reproduce yesterday's failure?"
- "Would a different model have got this right?"

This is the forensic counterpart to `zero-hallucination-coder`:
that one stops the agent inventing facts about code it has not read; this one stops it inventing
facts about work it has already done.

## Prerequisites

Recording is out-of-process: the agent is launched as a child process with its model-provider
origin pointed at a local proxy, so nothing is installed into the agent itself.

```bash
node --version                          # Node 20+
which orca || npm install -g orcareplay # exposes an MCP server, register it as `orca`
orca list                               # at least one run, or there is nothing to read
```

Disclosure: `orcareplay` is Apache-2.0 and runs entirely locally - no account, no service, no data
leaving the machine. It is maintained by the author of this skill.

## Workflow

### 1. Find the run

`orca_list_runs` - newest first, and it names the run each fork came from. Skip it only when the
user clearly means the most recent run; every other tool defaults to `run: "last"`.

### 2. Narrow to the chain that produced the thing being asked about

Two tools, two different questions:

| Question | Tool |
|---|---|
| *What happened?* | `orca_show_run` - the whole timeline: model turns with token counts and stop reasons, tool calls with arguments and results, shell commands with exit codes, every file changed |
| *Why did this happen?* | `orca_graph` with `to: <event seq>` - **only** the causal chain that produced that one event |

Reach for `orca_graph` first on a "why" question. Dumping a 200-event timeline and reasoning over
it is slower, costs more context, and invites exactly the confident guess this skill exists to
prevent.

### 3. Keep `recorded` and `inferred` apart in your answer

Every edge `orca_graph` returns is labelled:

- **`recorded`** - the recorder watched it happen and wrote it into the trace.
- **`inferred`** - derived at query time from a rule the edge names. The trace does not vouch for it.

These are different claims and must stay different in the answer:

- Correct: "The trace shows the `rm` at step 14 removed it."
- Correct: "This looks like the `rm` at step 14, going by timing - that edge is inferred, not recorded."
- Wrong: "Step 14 removed it." (when the edge was inferred)

Name the rule when you lean on an inferred edge.

### 4. Reproduce it before explaining it

`orca_replay` re-runs the recording and reports what could not be reproduced.

```
info replaying exchanges=6 egress=blocked
info replay.done reused=6/6 exact=6 divergences=0 exit=0
```

`exact=6` means every request matched the recording byte for byte. Anything that drifted is
reported with its size rather than quietly matched.

**Always pass `worktree: true`.** It replays into a scratch copy. Without it, replay restores the
recorded filesystem over the working tree for the duration of the run - uncommitted work is absent
in the meantime, and stays absent if the replay is interrupted before it can restore.

**Check what re-executes before the first replay of a run, not after.** Model responses come from
the trace and no provider is contacted, but the agent process runs again for real, so every shell
command it issued runs again too. Read them with `orca_show_run` first and tell the user what will
re-run. A run that only read files and edited the repository is free and repeatable; one that
reached `/tmp`, Docker, a database, a package manager or another host is not, and needs explicit
approval or a container.

**`reused=3/5` is usually not a partial failure.** Harnesses make calls for themselves - a quota
probe, a session-naming request - and a replay does not repeat them.

### 5. Only then consider comparing models

`orca_compare` forks one run onto several models from the same checkpoint: same files, same
conversation prefix, so the model is the only variable. Pick the fork point with
`orca_checkpoints`. Grade with `verify` - a shell command whose exit code is the verdict.

Use something the repository already declares (`npm test`, `npm run typecheck`) or an explicitly
local binary (`./node_modules/.bin/tsc --noEmit`). Never `npx <tool>`: with no local install, npx
runs whatever the registry has under that name, and `npx tsc` resolves a package deprecated in 2016
that is not TypeScript.

Three approvals are needed, and they are not the same question:

1. **Disclosure** - each model named receives the run's files and conversation prefix, so whatever
   that run touched is sent to every provider behind those model ids. Scrub first if the trace is
   not safe to send as-is.
2. **Side effects** - each fork is a live agent, not a replay. From the fork point on the model is
   really being asked, and its shell commands execute for real.
3. **Cost** - models times forks, in real money.

Replay is free; comparison is not. See `llm-cost-optimizer` before
turning comparison into a habit.

## If there is no recording

Say so plainly and offer to start one. Do not fall back to reconstructing the session.

```bash
orca record claude          # or codex, opencode, openclaw, grok
orca record generic-openai -- python my_agent.py
```

A run started with its prompt in argv (`orca record claude -- -p "..."`) replays exactly. A session
someone typed into replays approximately, because those prompts were never on the wire and are
recovered from the harness's own transcript; the replay output says which is which.

## Sharing a run

`orca export last -o run.html` writes one self-contained file.

A trace holds whatever the run held, so scrub before sending one anywhere - and treat scrubbing as
best-effort: it matches known key shapes and high-entropy strings, and cannot know that a particular
internal hostname or customer name is confidential. Have the user look at what is going out. See
`handoff` for what else belongs in a handover package.

## Anti-patterns

**Do not answer a "why did you..." question from memory when a recording exists.** This is the whole
point. A fluent reconstruction that happens to be right is still the wrong process, because the next
one will be wrong and read identically.

**Do not present an inferred edge as recorded.** Merging the two into one confident sentence is the
specific failure this skill prevents. If the trace does not vouch for it, say which rule does.

**Do not replay without `worktree: true` and without reading the run's shell commands first.** A
replay is not a dry run - the agent's own commands execute for real, and an in-place replay hides
uncommitted work while it runs.

**Do not call a matching replay a determinism result.** The model is not re-asked; its recorded
answers are served back. Whether a *fresh* run would fail the same way is a different question, and
replay cannot answer it. Say that rather than letting the user assume otherwise.

**Do not describe replay as a sandbox.** `egress=blocked` means model-provider egress, not network
isolation. A recorded tool call that ran `curl` runs it again. Only a network-isolated container
makes it a sandbox. See `chaos-engineering` for isolating blast
radius properly.

**Do not run `orca_compare` to satisfy curiosity the user did not express.** It uploads the run's
context to every provider named and spends real money doing it.

**Do not treat an empty trace as "nothing happened".** It means the harness was not captured -
usually an agent that reads no base-URL variable and pins its own origin, which needs TLS
interception or cannot be recorded at all.

## Related skills

- `zero-hallucination-coder` - same discipline, applied to
  code the agent has not read
- `agent-harness` - building the harness whose runs this reads
- `handoff` - packaging work for the next person
- `llm-cost-optimizer` - replay is free, forking is not
