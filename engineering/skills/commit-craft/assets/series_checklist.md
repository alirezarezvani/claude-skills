# Commit series checklist (before push)

Branch: ________________   Upstream: ________________   Date: ________

## Plan
- [ ] `commit_planner.py` run; verdict: ______ ; commits planned: ____
- [ ] No DO_NOT_COMMIT files staged; `.gitignore` updated where needed
- [ ] Moves carry their callers' import edits (no MOVE_NEEDS_CALLERS left)
- [ ] Formatting is its own commit; mixed files were staged with `git add -p`
- [ ] Each behaviour change carries its tests

## Gate
- [ ] `secret_gate.py` clean (or WARN only) for every commit
- [ ] Every waiver in `.commit-craft-allow` names a reason a reviewer would accept
- [ ] Anything that was ever pushed or shared and looked like a secret has been rotated

## Messages
- [ ] `message_linter.py --range <upstream>..HEAD` has no BLOCKER
- [ ] Every commit over ~40 lines says why in its body
- [ ] No fixup!/squash!/WIP commits left (`git rebase -i --autosquash <upstream>`)

## Proof
- [ ] `git rebase -x "<test command>" <upstream>` passed at every commit

Signed off by: ________________ (a person, not the agent)
