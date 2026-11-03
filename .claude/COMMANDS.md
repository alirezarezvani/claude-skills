# Maintainer slash commands

Project commands for working **on** this repository. They live in
`.claude/commands/` and load only when Claude Code runs inside a clone of the
repo; they are not part of any marketplace plugin.

This file sits outside `.claude/commands/` on purpose: every `.md` file in that
folder becomes a slash command, so a README there showed up as `/README`.

Verified on Claude Code 2.1.316 (2026-11-02): a file in a subfolder is invoked
as `/<folder>:<name>`, so `git/cm.md` is `/git:cm`.

## Commands

| Command | File | What it does |
|---------|------|--------------|
| `/git:cm` | `git/cm.md` | Review diffs for secrets, stage intentionally, write a Conventional Commit. No push. |
| `/git:cp` | `git/cp.md` | Run `/quality-gate`, commit, push, trigger `ci-quality-gate.yml`. |
| `/git:pr [target]` | `git/pr.md` | Open a PR with `gh pr create`. Target defaults to `dev`; never `main`. |
| `/git:clean` | `git/clean.md` | Delete merged branches locally and on the remote, keeping `main`, `dev`, `gh-pages`. Asks before force-deleting. |
| `/quality-gate` | `quality-gate.md` | yamllint + workflow schema check, `compileall`, markdown link check, optional `safety` audit. |
| `/security-scan` | `security-scan.md` | gitleaks secret scan + `safety` dependency audit. |
| `/update-docs` | `update-docs.md` | Post-creation sync: marketplace, cross-platform mirrors, docs site. |
| `/plugin-audit <path>` | `plugin-audit.md` | 8-phase plugin audit on one skill directory. |
| `/focused-fix <path>` | `focused-fix.md` | 5-phase repair of one feature (`engineering/focused-fix`). |
| `/seo-auditor [path]` | `seo-auditor.md` | SEO pass over `docs/` and the root README. |

`/quality-gate` was called `/review` until v2.14.7. Claude Code's built-in
`/code-review` also answers to `/review`, and the project command of that name
hid it.

## Naming rule

Never name a project command after a Claude Code built-in or one of its aliases
(`/review`, `/init`, `/simplify`, `/deep-research`, ...). The same rule applies
to plugin skills and is enforced for them by `scripts/check_skill_names.py`.
To see the current built-ins, run `claude -p "ok" --output-format stream-json
--verbose` outside the repo and read `slash_commands` in the `init` event.

## Typical flow

```
/quality-gate      # local checks
/security-scan     # secrets + dependencies
/git:cp            # commit and push
/git:pr            # PR to dev
```

CI (`ci-quality-gate.yml`) runs the binding gates on every PR. See the root
`CLAUDE.md` for the gate list and the PR-to-`dev` rule.
