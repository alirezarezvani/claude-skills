---
description: Clean up merged branches locally and on remote, keeping only main, dev, and gh-pages.
---

Clean up stale branches that have been merged or are no longer needed.

## Steps

1. **List local branches** to delete (excluding `main`, `dev`, `gh-pages`):

```bash
git branch | grep -v -E '^\*|main$|dev$|gh-pages$'
```

Report what will be deleted. If no branches found, say "No local branches to clean" and skip to step 3.

2. **Delete local branches** that are fully merged:

```bash
git branch -d <branch-name>
```

If a branch is not fully merged, report it to the user and ask whether to force-delete. Do NOT force-delete without confirmation.

3. **List remote branches** to delete (excluding `main`, `dev`, `gh-pages`, `HEAD`):

```bash
git branch -r | grep -v -E 'origin/main$|origin/dev$|origin/gh-pages$|origin/HEAD'
```

Report what will be deleted. If no branches found, say "No remote branches to clean" and skip to step 5.

4. **Confirm with the user** before deleting remote branches. Show the full list and wait for approval. Then delete:

```bash
git push origin --delete <branch-names>
```

5. **Prune stale remote refs**:

```bash
git remote prune origin
```

6. **Report final state**:

```bash
git branch        # local
git branch -r     # remote
```

Present a summary:

| Item | Count |
|------|-------|
| Local branches deleted | N |
| Remote branches deleted | N |
| Remaining local | main, dev |
| Remaining remote | origin/main, origin/dev, origin/gh-pages |
