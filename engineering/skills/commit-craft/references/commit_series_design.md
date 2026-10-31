# Commit series design: split, order, verify

A commit series is read three times: by the reviewer before merge, by `git bisect`
when something breaks, and by whoever runs `git blame` on a line a year later.
All three want the same thing: one logical change per commit, in an order where
every commit still builds.

## The rules and where they come from

| Rule | Source | Confidence |
|---|---|---|
| One logical change per commit | Git `SubmittingPatches`: "Make separate commits for logically separate changes." Linux kernel: "Separate each logical change into a separate patch." | High: primary project docs |
| Every commit builds and runs | Kernel: "take special care to ensure that the kernel builds and runs properly after each patch in the series", because `git bisect` may stop at any commit | High |
| Refactors apart from behaviour changes | Google eng-practices, *Small CLs*: "It's usually best to do refactorings in a separate CL from feature changes or bug fixes." Small local cleanups may stay | High |
| Tests ride with the code they test | Google, *Small CLs*: "CLs should include related test code." Independent test changes may land first | High |
| Whitespace and reformatting in their own commit | OpenStack *GitCommitMessages* lists mixing whitespace changes with functional code as a bad practice; it hides the real change in the diff | Moderate: one large project's convention, widely copied |
| Size: about 100 lines is reasonable, 1,000 usually too large | Google, *Small CLs*; the reviewer's judgment decides | Moderate: a guideline, not a law |

## The order commit_planner.py proposes, and why

1. **Dependencies** (manifest with its lockfile). Later commits import the new package; if it lands last, every commit before it fails to build. Never split a lockfile from its manifest.
2. **Pure moves.** Git's rename detection works best when a move carries no edits, so the history shows a rename instead of a delete and an add. A move must carry the import updates of its callers (`MOVE_NEEDS_CALLERS`), or the build breaks at that commit.
3. **Formatting.** Once it is in, the following diffs show only real changes.
4. **Behaviour changes by module**, each with its tests.
5. **Tests without a changed source sibling**, docs, CI.

The planner cannot read intent. It never chooses feat or fix, and it cannot tell
two unrelated fixes in the same file apart. That is what `git add -p` is for.

## Failure modes on both sides

- **Under-splitting:** one commit with a long message covering five changes. Revert and bisect then take all five or none.
- **Over-splitting:** a change cut so fine that no commit can be reviewed alone: a function in one commit, its only caller in the next, its test in a third. Each commit must make sense, and build, by itself. `TOO_MANY_GROUPS` warns when a plan passes `--max-groups`.
- **Test-later commits:** "add tests" as the last commit means every earlier commit is untested at bisect time.
- **Fixup debris:** `fixup!`, `squash!` and WIP commits pushed for review. Run `git rebase -i --autosquash <upstream>` first.

## Proving each commit builds

```bash
git rebase -x "npm test" origin/main      # runs the command after each commit; stops at the first failure
```

`git rebase --exec` replays the series and runs the command at every commit
(see `git-rebase`, `--exec`). Do it on unpushed work only: rewriting commits
others already pulled is a separate decision.

## Sources

1. Git project, *SubmittingPatches*. https://git-scm.com/docs/SubmittingPatches
2. Linux kernel, *Submitting patches: the essential guide*. https://www.kernel.org/doc/html/latest/process/submitting-patches.html
3. Google, *Engineering Practices: Small CLs*. https://google.github.io/eng-practices/review/developer/small-cls.html
4. OpenStack, *Git Commit Good Practice*. https://wiki.openstack.org/wiki/GitCommitMessages
5. Git, `git-rebase` (`--exec`, `--autosquash`). https://git-scm.com/docs/git-rebase
6. Git, `git-bisect`. https://git-scm.com/docs/git-bisect
7. Git, `git-add` (`--patch`). https://git-scm.com/docs/git-add
