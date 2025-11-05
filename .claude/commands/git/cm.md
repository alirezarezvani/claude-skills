---
description: Stage working tree changes and create a Conventional Commit (no push).
---

1. Run `git status --short` to review pending changes.
2. For each file, open a diff (`git diff -- path/to/file`) and ensure no secrets or credentials are present.
3. Stage the files intentionally (`git add path/to/file`). Avoid `git add .` unless every change was reviewed.
4. Generate a Conventional Commit message (types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert).
   - Commit subject ≤ 72 chars.
   - Scope uses kebab-case (e.g., `feat(marketing-skill): ...`).
   - Use `.github/commit-template.txt` for Context / Testing / Reviewers sections.
5. Run `git commit` and paste the generated message + context from the template.
6. Show the resulting commit (`git log -1 --stat`) and keep the commit hash handy.
7. **Do not push** in this command. Use `git/cp.md` when you're ready to publish.
