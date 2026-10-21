# CLAUDE.md layering and measuring adoption

What Claude Code loads as instructions at session start, and how to tell
whether a rollout is being used without reading anyone's sessions.

Confidence key: 🟢 verified on code.claude.com/docs · 🟡 observed locally, not documented · 🔴 recommendation or design choice.

## 1. The layers

Loaded at launch, in this order: 🟢 [memory]

1. Managed: `/Library/Application Support/ClaudeCode/CLAUDE.md`, `/etc/claude-code/CLAUDE.md`, `C:\Program Files\ClaudeCode\CLAUDE.md`
2. User: `~/.claude/CLAUDE.md` (and `~/.claude/rules/`)
3. Every `CLAUDE.md` from the filesystem root down to the working directory,
   concatenated root → cwd; `./CLAUDE.md` or `./.claude/CLAUDE.md` for the project
4. `CLAUDE.local.md`, after `CLAUDE.md` in each folder (current, not deprecated; gitignore it)
5. `.claude/rules/**/*.md`; a rule with `paths:` frontmatter loads only for matching files

`CLAUDE.md` files in subdirectories load on demand when Claude works there.
`AGENTS.md` is read only when there is no `CLAUDE.md`. 🟢 [memory]

## 2. Imports

`@path/to/file` imports another file, resolved relative to the importing file,
up to **4 hops** deep. Imports inside code spans and fenced blocks are ignored;
imports outside the project ask for approval once. 🟢 [memory]
A broken import fails silently: the instruction is simply not there.
`claude_md_layering_audit.py` resolves every import and reports broken ones,
cycles and anything past the hop limit.

## 3. Size

Files up to 4 MiB load in full and larger ones are skipped; the docs recommend
keeping each file under 200 lines. 🟢 [memory] Everything resident is sent with
every request, so a 25k-token CLAUDE.md is paid for on every turn of every
session. The script's default budget of 6,000 resident tokens is a heuristic,
not a documented limit. 🔴

Move instructions that apply to part of the repo into `.claude/rules/` with a
`paths:` scope; that is also the fix for most "always X" vs "never X"
contradictions, which are usually true in different directories. 🔴

## 4. What a shared memory file must not hold

- Credentials. Memory files are plaintext context sent to the model.
- Machine-specific paths (`/Users/alice/...`): wrong for everyone else.
- Personal preferences: those go in `~/.claude/CLAUDE.md` or `CLAUDE.local.md`.

## 5. Transcripts and retention

Session transcripts are JSONL at `~/.claude/projects/<project>/<session>.jsonl`;
prompt history is `~/.claude/history.jsonl`. They are plaintext and can contain
secrets that tools read. 🟢 [claude-directory] `cleanupPeriodDays` controls
retention (default 30, minimum 1). 🟢 [settings-reference]
The `<project>` folder name is the absolute path with `/` replaced by `-`. 🟡

`adoption_tracker.py` reads these files locally and outputs only counts:
sessions, active days, prompts, tool calls by kind (built-in / MCP / skill),
skill and slash-command **names**, CLI versions. It never emits prompt text,
file contents, or tool inputs other than a skill name.

## 6. OpenTelemetry, for organizations that want a dashboard

Set `CLAUDE_CODE_ENABLE_TELEMETRY=1` and the `OTEL_*` exporter variables from
**managed or user** settings (repo files cannot enable them). 🟢 [monitoring, settings-reference]
Metrics include `claude_code.session.count`, `claude_code.lines_of_code.count`,
`claude_code.pull_request.count`, `claude_code.commit.count`,
`claude_code.cost.usage`, `claude_code.token.usage`,
`claude_code.code_edit_tool.decision` and `claude_code.active_time.total`.
Prompt and tool-content logging are separate opt-ins (`OTEL_LOG_USER_PROMPTS`,
`OTEL_LOG_TOOL_DETAILS`, ...); leave them off unless a data-protection review
says otherwise. 🟢 [monitoring]

Use OpenTelemetry when you already run a collector. Use the adoption tracker
when you do not, or when you only need a monthly read-out. 🔴

## 7. Adoption stages

The thresholds below are this skill's design choice, chosen to be easy to
explain, not taken from a study. 🔴 They borrow the shape of Rogers' diffusion
curve: early adopters first, then a majority, then routine use. [Rogers]

| Stage | Rule |
|---|---|
| PILOT | under 25% of seats active in the window |
| SPREADING | 25-60% active |
| EMBEDDED | 60%+ active and the median active member uses it 3+ days a week |
| STALLED | under 25% active, 6+ weeks after launch |

A stall is a rollout problem (access, onboarding, missing MCP servers, a policy
that blocks real work), not a people problem. Ask the inactive seats what
stopped them before adding more policy. 🔴

## Sources

1. Claude Code docs — Memory (CLAUDE.md). https://code.claude.com/docs/en/memory
2. Claude Code docs — The .claude directory. https://code.claude.com/docs/en/claude-directory
3. Claude Code docs — Monitoring usage (OpenTelemetry). https://code.claude.com/docs/en/monitoring-usage
4. Claude Code docs — Settings reference. https://code.claude.com/docs/en/settings-reference
5. Claude Code docs — Environment variables. https://code.claude.com/docs/en/env-vars
6. Rogers, E. M. (2003). *Diffusion of Innovations*, 5th ed. Free Press.
