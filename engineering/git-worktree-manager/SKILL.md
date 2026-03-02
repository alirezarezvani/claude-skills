# Git Worktree Manager

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Parallel Development & Branch Isolation

## Overview

The Git Worktree Manager skill provides systematic management of Git worktrees for parallel development workflows. It handles worktree creation with automatic port allocation, environment file management, secret copying, and cleanup — enabling developers to run multiple Claude Code instances on separate features simultaneously without conflicts.

## Core Capabilities

- **Worktree Lifecycle Management** — create, list, switch, and cleanup worktrees with automated setup
- **Port Allocation & Isolation** — automatic port assignment per worktree to avoid dev server conflicts
- **Environment Synchronization** — copy .env files, secrets, and config between main and worktrees
- **Docker Compose Overrides** — generate per-worktree port override files for multi-service stacks
- **Conflict Prevention** — detect and warn about shared resources, database names, and API endpoints
- **Cleanup & Pruning** — safe removal with stale branch detection and uncommitted work warnings

## When to Use This Skill

- Running multiple Claude Code sessions on different features simultaneously
- Working on a hotfix while a feature branch has uncommitted work
- Reviewing a PR while continuing development on your branch
- Parallel CI/testing against multiple branches
- Monorepo development with isolated package changes

## Worktree Creation Workflow

### Step 1: Create Worktree

```bash
# Create worktree for a new feature branch
git worktree add ../project-feature-auth -b feature/auth

# Create worktree from an existing remote branch
git worktree add ../project-fix-123 origin/fix/issue-123

# Create worktree with tracking
git worktree add --track -b feature/new-api ../project-new-api origin/main
```

### Step 2: Environment Setup

After creating the worktree, automatically:

1. **Copy environment files:**
   ```bash
   cp .env ../project-feature-auth/.env
   cp .env.local ../project-feature-auth/.env.local 2>/dev/null
   ```

2. **Install dependencies:**
   ```bash
   cd ../project-feature-auth
   [ -f "pnpm-lock.yaml" ] && pnpm install
   [ -f "yarn.lock" ] && yarn install
   [ -f "package-lock.json" ] && npm install
   [ -f "bun.lockb" ] && bun install
   ```

3. **Allocate ports:**
   ```
   Main worktree:     localhost:3000 (dev), :5432 (db), :6379 (redis)
   Worktree 1:        localhost:3010 (dev), :5442 (db), :6389 (redis)
   Worktree 2:        localhost:3020 (dev), :5452 (db), :6399 (redis)
   ```

### Step 3: Docker Compose Override

For Docker Compose projects, generate per-worktree override:

```yaml
# docker-compose.worktree.yml (auto-generated)
services:
  app:
    ports:
      - "3010:3000"
  db:
    ports:
      - "5442:5432"
  redis:
    ports:
      - "6389:6379"
```

Usage: `docker compose -f docker-compose.yml -f docker-compose.worktree.yml up`

### Step 4: Database Isolation

```bash
# Option A: Separate database per worktree
createdb myapp_feature_auth

# Option B: DATABASE_URL override
echo 'DATABASE_URL="postgresql://localhost:5442/myapp_wt1"' >> .env.local

# Option C: SQLite — file-based, automatic isolation
```

## Monorepo Optimization

Combine worktrees with sparse checkout for large repos:

```bash
git worktree add --no-checkout ../project-packages-only
cd ../project-packages-only
git sparse-checkout init --cone
git sparse-checkout set packages/shared packages/api
git checkout feature/api-refactor
```

## Claude Code Integration

Each worktree gets auto-generated CLAUDE.md:

```markdown
# Worktree: feature/auth
# Dev server port: 3010
# Created: 2026-03-01

## Scope
Focus on changes related to this branch only.

## Commands
- Dev: PORT=3010 npm run dev
- Test: npm test -- --related
- Lint: npm run lint
```

Run parallel sessions:
```bash
# Terminal 1: Main feature
cd ~/project && claude
# Terminal 2: Hotfix
cd ~/project-hotfix && claude
# Terminal 3: PR review
cd ~/project-pr-review && claude
```

## Common Pitfalls

1. **Shared node_modules** — Worktrees share git dir but NOT node_modules. Always install deps.
2. **Port conflicts** — Two dev servers on :3000 = silent failures. Always allocate unique ports.
3. **Database migrations** — Migrations in one worktree affect all if sharing same DB. Isolate.
4. **Git hooks** — Live in `.git/hooks` (shared). Worktree-specific hooks need symlinks.
5. **IDE confusion** — VSCode may show wrong branch. Open as separate window.
6. **Stale worktrees** — Prune regularly: `git worktree prune`.

## Best Practices

1. Name worktrees by purpose: `project-auth`, `project-hotfix-123`, `project-pr-456`
2. Never create worktrees inside the main repo directory
3. Keep worktrees short-lived — merge and cleanup within days
4. Use the setup script — manual creation skips env/port/deps
5. One Claude Code instance per worktree — isolation is the point
6. Commit before switching — even WIP commits prevent lost work
