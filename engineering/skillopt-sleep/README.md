# SkillOpt-Sleep (vendored plugin)

This folder started as a **verbatim copy** of the `skillopt_sleep` engine and
the Claude Code plugin surface from
[microsoft/SkillOpt](https://github.com/microsoft/SkillOpt)
(`skillopt_sleep/`, `plugins/claude-code/`, `plugins/run-sleep.sh`), only
relocated so path resolution (`CLAUDE_PLUGIN_ROOT`-relative lookups in
`scripts/sleep.sh` / `scripts/run-sleep.sh`) resolves correctly at this
folder's location. Licensed under the [MIT License](LICENSE) © Microsoft
Corporation. A small number of targeted patches were made afterward to close
gaps between this plugin's own safety claims and what the code actually did
— see **Deviations from upstream** below. Re-apply all of these on re-vendor;
they are not upstream yet.

## Deviations from upstream

1. **Cosmetic — `check_paths.py` wording.** `skills/skillopt-sleep/SKILL.md`'s
   frontmatter `description` said "...consolidate validated CLAUDE.md/SKILL.md
   behind a held-out gate" — the `CLAUDE.md/SKILL.md` substring reads as a
   broken relative path to this repo's `[A-Za-z0-9_\-./]+/SKILL\.md` linter
   regex. Reworded to "CLAUDE.md and SKILL.md"; no behavior or meaning
   changed.
2. **Safety — secrets weren't redacted in the files that actually go live.**
   `staging.py`'s `redact_secrets()` was applied to `diagnostics.json` and CLI
   error logging, but **not** to `proposed_SKILL.md` / `proposed_CLAUDE.md` —
   the exact files `adopt()` copies over your live `CLAUDE.md` / managed
   `SKILL.md` (with `--auto-adopt`, with no human in the loop). Since
   `reflect()`'s prompt is built from real harvested session text, a secret
   pasted into a real debugging session could have landed in your live memory
   file unredacted, despite the "secrets are redacted from prompts" claim
   below. Fixed: `write_staging()` now runs both through `redact_secrets()`
   before writing.
3. **Safety — the crontab line was built via unescaped f-string
   interpolation.** `scheduler.py`'s `_runner_cmd()` wrapped `project` (an
   arbitrary filesystem path) in manual `"..."` quoting, then wrote the result
   straight into your real crontab — which cron runs through `sh -c` on every
   fire. A path containing `"`, `` ` ``, `$( )`, or `;` could break out of the
   quoting and inject an arbitrary command into your crontab. Fixed: `project`,
   `logdir`, `log`, and the repo root are now `shlex.quote()`-d before
   interpolation.
4. **Safety — `max_tokens_per_night` was a dead config key.** `config.py`
   declared it in `DEFAULTS`, and `budget.py` already had a `Budget` /
   `plan_depth` heuristic built for exactly this purpose, but nothing in the
   production `run_sleep_cycle()` path ever read it — a `--backend
   claude`/`--backend codex` night had no real ceiling on API spend. Fixed:
   `cycle.py` now starts a `Budget` right after backend construction (so
   harvest/mine spend counts too), sizes `dream_rollouts` down via
   `plan_depth()` when the remaining budget is tight, and appends a `report`
   note whenever it caps rollouts or the budget is exhausted at night's end —
   no silent truncation. This caps *rollout depth per task*, not a hard
   mid-call abort inside a single `dream_consolidate()` call; a night can
   still overshoot the cap somewhat if an individual rollout is unusually
   token-heavy. That residual gap is real and not yet closed.
5. **Cosmetic — dead hardcoded path.** `backend.py`'s `resolve_codex_path()`
   listed `~/.nvm/versions/node/v22.22.3/bin/codex` as a candidate ahead of
   the generic "any nvm node version" scan a few lines later, which already
   covers it. Removed; no behavior change for anyone not on that exact nvm
   version, one less leftover-looking line for everyone else.
6. **Safety — `redact_secrets` was a dead config key.** `config.py` declared
   `"redact_secrets": True` in `DEFAULTS`, but `write_staging()` called
   `redact_secrets()` unconditionally — the safe direction, but the knob had
   no effect either way. Fixed: `cycle.py` now reads
   `cfg.get("redact_secrets", True)` and threads it through `write_staging()`
   and the `diagnostics.json` fields; disabling it is honored (it's the
   user's config) but never silently — a `report` note fires whenever it's
   off.
7. **Hardening — `adopt()` now re-redacts as defense-in-depth.** Previously
   `adopt()` copied the staged `proposed_SKILL.md`/`proposed_CLAUDE.md`
   straight to the live path with `shutil.copy2`. Since `write_staging()`
   already redacts, this was redundant for the common case, but didn't cover
   a human hand-editing the staged proposal between `stage` and `adopt` (the
   exact workflow staging exists to allow). `adopt()` now reads, re-runs
   `redact_secrets()`, and writes each file rather than a raw byte copy;
   `_backup()` of the *prior* live file is unaffected (that's a backup of
   what already existed, not the incoming content).
8. **Safety — `scheduler.py`'s `extra` param wasn't shell-quoted.**
   `project`/`logdir`/`log`/repo-root were `shlex.quote()`-d in fix #3 above,
   but `extra` (today only ever `""` or the literal `"--auto-adopt"` from
   `__main__.py`) was appended raw. Not exploitable today since it's a
   hardcoded flag literal, but reopens the same class of bug if a future
   change lets `extra` carry anything else. Fixed: `extra` is now
   `shlex.split()` into tokens and each token `shlex.quote()`-d before
   joining, so a multi-token or attacker-influenced `extra` can't break out
   of the command the way `project` used to.
9. **Safety — the cross-night task archive (`state.json`) was never
   redacted.** `state.py`'s `add_to_archive()` persists raw `TaskRecord`
   content (`intent` / `context_excerpt` / `attempted_solution` — real
   harvested prompt/response text) to `~/.skillopt-sleep/state.json`
   indefinitely, for `recall_k` associative recall across nights. Unlike
   `proposed_SKILL.md`/`proposed_CLAUDE.md`/`diagnostics.json` (fixes #2,
   #6), this file lives entirely outside the staging dir a user is ever told
   to review — a secret pasted into a real debugging session would have
   landed there and stayed. Fixed: `cycle.py` now redacts each task dict
   before archiving, using the same `redact_enabled` flag (and loud
   report-note-on-disable) as everything else.
10. **Safety — `report.md` / `report.json` were never redacted.** These are
    the two artifacts a human is told to read *first* (the SKILL.md's own
    workflow says "Read the generated `report.md`... show the user the exact
    proposed edits"), yet `EditRecord.content`/`.rationale` — sourced from
    the optimizer's `reflect()` output over real failing task responses —
    were written unredacted, while the sibling `proposed_SKILL.md`/
    `proposed_CLAUDE.md`/`diagnostics.json` got fixed in earlier rounds.
    Fixed: `write_staging()` now redacts the rendered `report_md` string and
    `report.to_dict()` (via `redact_secrets`'s existing recursive dict/list/
    str handling) before writing `report.md`/`report.json`.
11. **Safety/cosmetic — dead config knob: `replay_mode`.** `config.py`
    declared `"replay_mode": "mock" | "fresh" (worktree)`, but the only
    production code path that reads it prints a cosmetic label in the
    report — there is no worktree-replay implementation anywhere in this
    engine. Implementing real worktree isolation was judged too invasive for
    a vendored copy (a substantial new feature in code this repo doesn't
    otherwise maintain); instead, `cycle.py` now appends a loud report note
    whenever `replay_mode` is set to anything but `"mock"`, so the report
    never implies real worktree isolation that isn't happening.
12. **Sensitive — hardcoded internal Azure OpenAI infrastructure removed.**
    `backend.py` shipped an `AzureOpenAIBackend`/`AzureResponsesBackend` pair
    with 5 internal-looking Azure endpoint hostnames and a hardcoded Managed
    Identity client ID, explicitly commented as sourced from "the intern's
    avail_api.md" — reads like leaked internal Microsoft dev-infra topology.
    This backend was already unreachable from this plugin's documented
    `mock`/`claude`/`codex`/`copilot` `--backend` choices (only settable by
    hand-editing `~/.skillopt-sleep/config.json` directly) and requires
    `azure-identity`/`openai` third-party packages this repo never claims to
    depend on. Removed entirely (classes, constants, `get_backend()`/
    `build_backend()` dispatch branches and the now-unused `azure_endpoint`
    parameter); `get_backend("azure")` now safely falls back to `MockBackend`
    instead of raising or wiring internal infra. Same class of "leftover
    internal-looking detail" as fix #5's dead `nvm` path, but materially more
    sensitive, so it was removed rather than just flagged.
13. **Safety — unvalidated tool names reachable via `--tasks-file`.**
    `attempt_with_tools()` (all three CLI backends) used a task's tool name
    both as a shim *filename* (`os.path.join(work, tname)`) and interpolated
    unescaped into the shim's generated shell body
    (`f'echo "{tname}" >> ...'`). Tool names originate from a hand-authored
    `--tasks-file`'s `judge.checks[].arg` (`op=="tool_called"`), never
    validated as a safe identifier — a crafted name containing `../`, `"`,
    backticks, or `$( )` could traverse out of the working dir or inject a
    command into the generated shim. Not reachable via the harvest/mine path
    today (the LLM miner excludes this check type), but `--tasks-file` is a
    documented, user-facing input. Fixed: a shared `_sanitize_tool_names()`
    helper filters to a safe-identifier allowlist (`^[A-Za-z0-9_-]{1,64}$`)
    before any name is used as a filename or shell text, in all three
    backends.
14. **Cosmetic — dead cross-reference in `SKILL.md`.**
    `skills/skillopt-sleep/SKILL.md` pointed to
    `docs/superpowers/specs/2026-06-07-skillopt-sleep-claude-code-plugin-design.md`
    "for the full design" — that path is not in this repo (see "What was and
    wasn't vendored" below; `docs/` was deliberately excluded). An agent
    following the pointer hits a missing file. Fixed: points to the real
    upstream guide URL (microsoft.github.io/SkillOpt/docs/guideline.html#sleep)
    instead, with a note on why the local path is absent.
15. **Safety — `commands/skillopt-sleep.md` didn't signal that `schedule`
    installs immediately.** The command doc's action table listed `schedule`
    as an ordinary action alongside `status`/`dry-run`/`run` (all of which
    are safe previews or explicitly staged), while its own "Safety
    reminders" section separately said to point users at the print-only
    `install-cron.sh` instead — two different, uncoordinated stories about
    the same action. `scheduler.schedule()` writes directly to the user's
    real crontab the moment it runs, with no confirmation step in between.
    Fixed: "Steps to follow" now has an explicit step 1 telling the agent to
    confirm with the user *before* running `schedule` (what project/hour/
    minute/backend will be scheduled), with `install-cron.sh` offered as the
    print-only alternative; "Safety reminders" now says the same thing
    instead of contradicting the action table.
16. **Hardening — state/staging directories and files had no restrictive
    permissions.** `state.json` (the cross-night task archive) and
    `.skillopt-sleep/staging/<ts>/`'s proposal/report/diagnostics files
    contain real harvested session content in plaintext, created via plain
    `os.makedirs`/`open(..., "w")` — world-readable-by-default on a typical
    multi-user Linux box (subject to the process umask). `redact_secrets()`
    scrubs known secret *patterns*, but the files still carry real task
    intents, code excerpts, and project context otherwise. Fixed: both
    `state.py` and `staging.py` now `os.chmod()` every directory they create
    to `0o700` and every file they write to `0o600` (best-effort, silently
    skipped on platforms without POSIX permission bits). Live `CLAUDE.md`/
    `SKILL.md` files themselves are intentionally left at their existing
    permissions — those are the user's own, often-committed files, not new
    output this plugin introduces.
17. **Cosmetic — misleading redaction placeholder label.** `staging.py`'s
    `sk-[A-Za-z0-9_-]{10,}` pattern matched any `sk-`-prefixed key (OpenAI,
    Anthropic's `sk-ant-...`, and other vendors sharing the convention) but
    labeled every match `[REDACTED_OPENAI_KEY]` regardless of which vendor's
    key shape it actually was. Redaction itself was unaffected — the text
    was scrubbed either way — but the placeholder implied a narrower match
    than the pattern actually has. Fixed: relabeled to `[REDACTED_API_KEY]`.
18. **Cosmetic/hardening — stale fallback paths in the shell launchers.**
    `scripts/sleep.sh`'s header comment and its `SKILLOPT_SLEEP_REPO`
    fallback branch referenced upstream's `<repo>/plugins/run-sleep.sh`
    layout; `scripts/run-sleep.sh`'s header comment and its
    `CLAUDE_PLUGIN_ROOT` branch likewise assumed the upstream three-level
    `<repo>/plugins/claude-code/` structure (`CLAUDE_PLUGIN_ROOT/../../
    skillopt_sleep`). In this vendored copy `scripts/` and `skillopt_sleep/`
    are siblings directly under the plugin root
    (`engineering/skillopt-sleep/`), so `CLAUDE_PLUGIN_ROOT` (when Claude
    Code sets it) points straight at a dir containing `skillopt_sleep/`, not
    two levels above one. Both scripts' primary co-located/repo-relative
    resolution branches happen to still succeed for this layout regardless
    (so this was unreachable in normal operation), but the documented
    `SKILLOPT_SLEEP_REPO` and `CLAUDE_PLUGIN_ROOT` escape hatches would have
    silently failed to resolve for anyone actually relying on them — e.g.
    after a future re-vendor that missed copying `run-sleep.sh` into
    `scripts/`. Fixed: `sleep.sh`'s explicit-env branch now checks
    `$SKILLOPT_SLEEP_REPO/scripts/run-sleep.sh`; `run-sleep.sh` now checks
    `$CLAUDE_PLUGIN_ROOT/skillopt_sleep` (this repo's actual layout) ahead of
    the upstream two-levels-up check (kept for portability if this script is
    ever reused in that shape again). Verified both fixed branches resolve
    correctly in isolation from the co-located fallback.
19. **Safety — the CLI's own stdout/`--json`/`--output` bypassed
    `redact_secrets()` entirely.** Rounds 1-3 covered every *file*
    `write_staging()`/`state.py` write, but `__main__.py`'s `cmd_run()` reads
    the same in-memory `Report` object and prints `EditRecord.content`
    (raw, from `reflect()`'s output over real task responses) directly to
    the console, and `_report_payload()` serializes it unredacted for
    `--json` — `write_staging()`'s redaction runs on a *copy*
    (`redact_secrets(report.to_dict())`) used only for the on-disk JSON, it
    never touches `report.edits` itself. Concretely: `scheduler.py`'s cron
    entry redirects `run`'s stdout/stderr straight into
    `<project>/.skillopt-sleep/cron.log` — a secret that leaked into a
    proposed edit's content would land there in plaintext on every scheduled
    night, in a file that (unlike `state.json`/staged files) also had no
    `chmod` protection (see the second fix below). `cmd_harvest()`'s debug
    output (`--json`, `--output <file>`, and the plain-text loop) has the
    same shape: it prints raw mined `TaskRecord.intent` text so a human can
    review it before setting `"reviewed": true` on a `--tasks-file`, which
    means redacting it doesn't reduce what's reviewable (only secret-shaped
    substrings are stripped) while closing the same leak path. Fixed:
    `_report_payload()` and `cmd_run()`'s plain-text edit printing, and
    `cmd_harvest()`'s payload (covering its `--output` file, `--json`
    stdout, and plain-text loop uniformly), all now run through
    `redact_secrets()`, gated on the same `redact_secrets` config flag as
    everywhere else. Also hardened `scheduler.py`'s generated cron line to
    `chmod 700` the `.skillopt-sleep` log dir and `chmod 600` `cron.log`
    itself (best-effort, `2>/dev/null`) before each run appends to it —
    that file was never covered by the state/staging chmod pass in fix #16.
    Verified: a synthetic secret seeded into a task's intent no longer
    appears in `cmd_run`'s `--json` payload or plain-text edit output, or in
    `cmd_harvest`'s redacted payload; executing the actual generated cron
    line end-to-end produces a `0700` log dir and `0600` log file on disk.
20. **Bug — `scheduler.py`'s per-project marker match used unanchored
    substring comparison.** `schedule()`/`unschedule()` both located "this
    project's" managed cron line via `marker not in ln`, a bare substring
    test, not an exact-match or delimiter-anchored check. Failure scenario:
    two projects scheduled where one path is a literal prefix of the other
    (e.g. `/home/user/app` and `/home/user/app-v2`) — `_project_marker`
    produces `# project=/home/user/app`, which is itself a substring of
    `# project=/home/user/app-v2`'s line. Running `schedule()` or
    `unschedule()` for `/home/user/app` would silently drop
    `/home/user/app-v2`'s cron entry too, with no error or warning — the
    user's other project's nightly job just disappears. `harvest.py`'s
    `_project_matches()` (added in this same PR) already gets this right a
    few hundred lines away (`a == b or a.startswith(b + os.sep) or
    b.startswith(a + os.sep)`); `scheduler.py`'s marker matching didn't
    follow the same discipline. Fixed: added `_line_matches_project()`,
    which anchors on `ln.rstrip().endswith(marker)` since the marker is
    always the last token of a generated line (see `schedule()`'s
    `cron_line` construction) — used at both call sites. Verified two ways:
    a standalone reproduction confirmed the bug before the fix and its
    absence after, and a full `schedule()`/`unschedule()` round-trip through
    the actual public API (with `crontab -l`/`crontab -` swapped for an
    in-memory fake) confirmed scheduling both `/home/user/app` and
    `/home/user/app-v2`, then unscheduling only `app`, correctly leaves
    `app-v2`'s line intact.
21. **Cosmetic — `install-cron.sh`'s printed `--backend` value was
    unquoted.** `scheduler.py::_runner_cmd` quotes every interpolated value
    with `shlex.quote()`, but the standalone `install-cron.sh` script
    (which only *prints* a crontab line for the user to copy into `crontab
    -e` — nothing is executed automatically) interpolated `--backend
    ${BACKEND}` unquoted in its heredoc, next to otherwise-quoted
    `${RUNNER}`/`${PROJECT}`. Low risk since `BACKEND` is normally one of a
    fixed small set of values and the script never executes anything
    itself, but inconsistent with the quoting discipline applied everywhere
    else. Fixed: quoted as `"${BACKEND}"`.
22. **Hardening — `schedule` had no confirmation gate at the CLI layer.**
    The deviation #15 "confirm with the user before `schedule`" safeguard lived
    only in `commands/skillopt-sleep.md`'s agent-facing instructions —
    `cmd_schedule()` itself called `scheduler.schedule()` directly and
    installed a real crontab entry immediately. That's fine for the
    documented Claude Code agent workflow (which confirms in chat first),
    but anyone invoking `python -m skillopt_sleep schedule` directly
    bypassed it entirely, with no gate in the CLI itself. Fixed: `schedule`
    now requires `--yes`; without it, an interactive terminal gets a
    `[y/N]` prompt and a non-interactive one (no TTY) refuses outright with
    an exit code (2) pointing at `--yes`. `commands/skillopt-sleep.md`
    updated so the driving agent passes `--yes` once *it* has confirmed
    with the user in chat — that chat confirmation is what `--yes` records,
    not a redundant re-prompt (which would hang forever with no TTY to
    answer from inside a non-interactive Bash tool call anyway). Verified:
    non-interactive `schedule` without `--yes` refuses with exit 2; with
    `--yes` it proceeds to the same `scheduler.schedule()` call as before.
23. **Hardening — mkdir-then-chmod wasn't atomic.** `write_staging()`
    (`staging.py`) and `SleepState.save()` (`state.py`) called
    `os.makedirs(path, exist_ok=True)` and only `chmod`'d afterward,
    leaving a brief window where a freshly-created sensitive directory sat
    at the process's default umask — exactly what this plugin's chmod
    hardening (deviation #16) exists to close. Fixed: the `os.makedirs()`
    calls that create the state dir, the per-run staging leaf dir, and the
    adopt-time backup dir now pass `mode=0o700` directly, closing the
    window for the common first-creation case. The existing post-creation
    `chmod` calls are kept, not removed — `mode=` only governs the leaf
    directory `mkdir()` itself creates (intermediate parent directories
    still fall back to the umask default) and is itself still subject to
    umask, so it narrows the window rather than eliminating every case
    (e.g. a directory that already existed from before this fix, or an
    intermediate parent). The equivalent race for individual *files*
    (`open(path, "w")` then `chmod` after) is a smaller, harder-to-close
    window — closing it fully would mean rewriting every file-write call
    site to use `os.open()` with an explicit mode instead of the builtin
    `open()`, which felt like a larger rewrite than this specific,
    low-severity (requires a local attacker with precise timing) finding
    warranted; left as a known, narrower residual gap rather than silently
    claimed as fully closed.

## What this plugin is

SkillOpt-Sleep gives a local Claude Code agent a nightly **sleep cycle**: it
reviews real past sessions in this repo, replays recurring tasks offline on
your own API budget, and consolidates what it learns into this repo's
`CLAUDE.md` memory and `SKILL.md` skills — but **only** through a held-out
validation gate, and **only** after you explicitly adopt the staged proposal.

It is the deployment-time companion to the (not vendored) `skillopt` training
package: SkillOpt trains a skill offline against a labeled benchmark;
SkillOpt-Sleep applies the same bounded-edit + held-out-gate discipline to
*actual usage of this repo* instead, so it needs no benchmark dataset.

```
harvest ~/.claude transcripts (read-only)
  → mine recurring tasks
  → replay offline
  → consolidate (reflect → bounded edit → GATE)
  → stage proposal (nothing live changes)
  → you review and run "adopt" (backs up first)
```

## Why this is a fit for a skills library with no test harness

This repo's [CLAUDE.md](../../CLAUDE.md) intentionally has no build system or
test framework, and skill `scripts/` are stdlib-only with no LLM calls, so the
full `microsoft/SkillOpt` training package (benchmark-driven, requires
labeled train/val/test data per task, needs `numpy`/`openai`/`azure-*`) was
**not** vendored — there is no natural ground-truth benchmark for something
like `finance/dcf-valuation` or `c-level-advisor/vpe-advisor`.

`skillopt_sleep`, by contrast, has **zero third-party dependencies** (stdlib
only), its default `mock` backend spends no API budget, and it mines its
"benchmark" from how the skills in *this* repo actually get used in real
sessions rather than a pre-labeled dataset. That matches the repo's
deterministic-first, portable-first philosophy far better than the training
package does.

## Use in this repo

```bash
# from the repo root:
engineering/skillopt-sleep/scripts/sleep.sh status                          # what's happened (read-only)
engineering/skillopt-sleep/scripts/sleep.sh dry-run  --project "$(pwd)"     # safe preview, stages nothing
engineering/skillopt-sleep/scripts/sleep.sh run      --project "$(pwd)"     # full cycle, stages a proposal
engineering/skillopt-sleep/scripts/sleep.sh adopt    --project "$(pwd)"     # apply staged proposal (backs up first)
```

Or, once the plugin is installed via Claude Code's plugin marketplace, use
the bundled `/skillopt-sleep [run|dry-run|status|adopt|harvest|schedule|unschedule]`
slash command (see `commands/skillopt-sleep.md` and `skills/skillopt-sleep/SKILL.md`).

Default backend is `mock` (deterministic, **no API spend** — safe to try
immediately). Add `--backend claude` to spend real budget replaying this
repo's own recurring tasks and get genuine lift on `CLAUDE.md` / a target
`SKILL.md`.

## Safety model

- Harvest is **read-only** over `~/.claude` session transcripts.
- Edits are proposed, gated against a held-out replay slice, and **staged**
  under `.skillopt-sleep/staging/<date>/` — nothing live is touched.
- `adopt` is explicit and backs up the prior file first (unless you opt into
  `--auto-adopt`).
- `max_tasks_per_night` is a hard cap (mining stops there). `max_tokens_per_night`
  sizes `dream_rollouts` down via `plan_depth()` and is reported when hit, but
  is not a hard mid-call abort — see deviation #4 above for the exact scope.
- Secrets (API keys, bearer tokens, private-key blocks) are redacted before
  anything is written to the staging dir, including `proposed_SKILL.md` /
  `proposed_CLAUDE.md` (deviation #2 above) — not just diagnostics — and
  re-redacted again at `adopt()` time as defense-in-depth against a
  hand-edited staged proposal (deviation #7). Disabling this via
  `redact_secrets: false` is honored but never silent — it logs a report
  note (deviation #6). The same flag now also covers the cross-night task
  archive (`state.json`, deviation #9), `report.md`/`report.json`
  (deviation #10) — the two files a human is actually told to read first —
  and every CLI console/`--json`/`--output` code path (`cmd_run`,
  `cmd_harvest`), not just what gets written to disk (deviation #19).
  `cron.log` (the CLI's redirected stdout/stderr) is now `chmod 600` too,
  matching state/staging (deviation #19).
- The generated crontab line, including the `extra` flags parameter, is
  fully `shlex.quote()`-d, not just the path arguments (deviations #3, #8,
  #21). `schedule`/`unschedule` locate a project's own line via an anchored
  end-of-line match, not a bare substring test, so scheduling/unscheduling
  one project can't silently drop a sibling project whose path happens to
  be a prefix of it (deviation #20).
- `replay_mode: "fresh"` (worktree replay) is not implemented — every replay
  runs as `"mock"` regardless, and the report says so explicitly rather than
  implying isolation that isn't happening (deviation #11).
- Tool names reachable via a hand-authored `--tasks-file` are validated
  against a safe-identifier allowlist before being used as a shim filename or
  interpolated into generated shell text (deviation #13).
- Only `mock`/`claude`/`codex`/`copilot` backends are supported — a
  Microsoft-internal Azure OpenAI backend was removed rather than carried
  forward (deviation #12).
- `schedule` installs a real crontab entry **immediately** — unlike every
  other action, it is not a preview or a staged proposal. An agent driving
  `/skillopt-sleep schedule` must confirm with the user first (deviation
  #15); `install-cron.sh` remains available as a print-only alternative.
- Every directory `state.py`/`staging.py` create is `chmod 0700` and every
  file they write is `chmod 0600` (best-effort), so `state.json` and staged
  proposals/reports/diagnostics aren't left at the world-readable process
  umask default on a shared machine (deviation #16).

## What was and wasn't vendored

| Vendored | Not vendored |
|---|---|
| `skillopt_sleep/` engine (stdlib-only) | `skillopt/` training package (needs `numpy`/`openai`/`azure-*` + labeled benchmarks) |
| `plugins/claude-code/skills\|hooks\|commands\|scripts/` | `plugins/codex/`, `plugins/copilot/`, `plugins/devin/`, `plugins/openclaw/` (other-agent plugin variants) |
| `plugins/run-sleep.sh` shared launcher | `skillopt_webui/` (optional Gradio dashboard) |
| `LICENSE` | `docs/`, `ckpt/`, `data/`, `index.html` (training-package docs/site/checkpoints) |
| | `AzureOpenAIBackend`/`AzureResponsesBackend` from `backend.py` — removed post-vendor, see deviation #12 (Microsoft-internal endpoints/client ID, unreachable from this plugin's supported `--backend` choices, needs deps not vendored here) |

## Updating

Re-vendor from upstream when the plugin changes:

```bash
git clone --depth 1 https://github.com/microsoft/SkillOpt.git /tmp/skillopt-upstream
cp -r /tmp/skillopt-upstream/skillopt_sleep engineering/skillopt-sleep/skillopt_sleep
cp -r /tmp/skillopt-upstream/plugins/claude-code/skills/skillopt-sleep engineering/skillopt-sleep/skills/skillopt-sleep
cp -r /tmp/skillopt-upstream/plugins/claude-code/hooks engineering/skillopt-sleep/hooks
cp -r /tmp/skillopt-upstream/plugins/claude-code/commands engineering/skillopt-sleep/commands
cp /tmp/skillopt-upstream/plugins/claude-code/scripts/sleep.sh /tmp/skillopt-upstream/plugins/claude-code/scripts/install-cron.sh engineering/skillopt-sleep/scripts/
cp /tmp/skillopt-upstream/plugins/run-sleep.sh engineering/skillopt-sleep/scripts/run-sleep.sh
cp /tmp/skillopt-upstream/LICENSE engineering/skillopt-sleep/LICENSE
```
