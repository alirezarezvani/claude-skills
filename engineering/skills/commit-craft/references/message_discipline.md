# Commit messages: subject, why, trailers

The diff shows what changed. The message exists for what the diff cannot show:
why the change was needed, why this approach, and what it is safe to assume.

## Subject

- **Imperative mood.** Git: "Describe your changes in imperative mood, e.g. 'make xyzzy do frotz' instead of '[This patch] makes xyzzy do frotz'." The kernel guide says the same. Test: the subject completes "If applied, this commit will …" (Beams).
- **Short.** Git `SubmittingPatches`: "50 characters is the soft limit" and skip the full stop. `message_linter.py` warns past 50 for plain subjects and blocks past 72, the width where many tools truncate. For Conventional Commits it checks 72 only, since the prefix spends part of the budget.
- **Specific.** "fix", "update", "address review comments" give bisect and blame nothing. They block.
- **Area prefix.** Git's own project uses `area: description`. Conventional Commits formalise it as `type(scope): description`. Use what the repo already uses: `--convention auto` enforces Conventional Commits only when at least 60% of the last 50 subjects follow it.

## Body: the why

Git `SubmittingPatches` says the body should explain:

1. the problem: what is wrong with the current code without the change;
2. why the result is better with the change;
3. alternatives considered and discarded, if any.

A body that lists the touched files repeats the diff (`BODY_LISTS_FILES`). A body
for a large change is not optional: `BODY_MISSING` blocks when a commit reaches
`--body-lines` (40) changed lines or `--body-files` (4) files. Dependency bumps,
formatting, docs, tests, CI and reverts are exempt.

`WHY_MISSING` looks for words that usually carry a reason (because, so that,
previously, fails, `#123`). It is a heuristic, so it only warns. A body can
explain why with none of those words, and a body full of them can still say
nothing.

Example:

```
fix(invoices): reject two-letter currency codes at the API

Invoices with a two-letter currency code reached the ledger and failed
at month-end close, because validate() only checked the total. The
schema rejects them at the boundary, where the caller can still fix
the request.

Refs #412
```

## Breaking changes and trailers

- Conventional Commits 1.0.0: a breaking change is marked with `!` before the colon, or a footer `BREAKING CHANGE: <description>` (uppercase). `BREAKING_UNMARKED` warns when the body says "breaking" without either.
- The spec itself defines only `feat` and `fix`. `build`, `chore`, `ci`, `docs`, `style`, `refactor`, `perf` and `test` come from the commitlint convention it cites; pass `--types` for a repo with its own list.
- Trailers (`Refs:`, `Co-authored-by:`, `Signed-off-by:`) go in the last paragraph, `Key: value` per line (`git interpret-trailers`). The linter exempts them from wrapping.

## Sources

1. Git project, *SubmittingPatches*. https://git-scm.com/docs/SubmittingPatches
2. Git, `git-commit`, DISCUSSION. https://git-scm.com/docs/git-commit
3. Linux kernel, *Submitting patches*. https://www.kernel.org/doc/html/latest/process/submitting-patches.html
4. Chris Beams, *How to Write a Git Commit Message*. https://cbea.ms/git-commit/
5. Tim Pope, *A Note About Git Commit Messages* (2008). https://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html
6. *Conventional Commits 1.0.0*. https://www.conventionalcommits.org/en/v1.0.0/
7. Git, `git-interpret-trailers`. https://git-scm.com/docs/git-interpret-trailers
