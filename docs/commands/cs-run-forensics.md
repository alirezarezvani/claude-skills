---
title: "/cs-run-forensics — Slash Command for AI Coding Agents"
description: "Answer a question about a past agent run from its recorded transcript - find the run, walk back from the step, separate recorded from inferred.. Slash command for Claude Code, Codex CLI, Gemini CLI."
---

# /cs-run-forensics

<div class="page-meta" markdown>
<span class="meta-badge">:material-console: Slash Command</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/2-claude-skills/tree/main/engineering/agent-run-forensics/commands/cs-run-forensics.md">Source</a></span>
</div>


Answer `$ARGUMENTS` from the recording, not from memory.

```bash
S=${CLAUDE_PLUGIN_ROOT}/skills/agent-run-forensics/scripts
python3 $S/trace_finder.py --since 7d                     # add --touched PATH or --grep TEXT; skip for this session
python3 $S/trace_timeline.py --trace <path> --files
python3 $S/trace_timeline.py --trace <path> --grep <TEXT> # or --errors, --file PATH
python3 $S/trace_timeline.py --trace <path> --why <STEP>
```

If the finder exits 2, say the run is not recorded here and stop.

## Report

1. The run: session id, harness, time, source path.
2. The answer, from recorded steps only, each with its step number.
3. The likely cause, labelled inferred, with its rule.
4. What the trace cannot answer.
