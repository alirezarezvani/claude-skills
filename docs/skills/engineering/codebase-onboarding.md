---
title: "Codebase Onboarding"
description: "Codebase Onboarding - Claude Code skill from the Engineering - POWERFUL domain."
---

# Codebase Onboarding

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `codebase-onboarding`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/codebase-onboarding/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Documentation / Developer Experience  

---

## Overview

Analyze a codebase and generate comprehensive onboarding documentation tailored to your audience. Produces architecture overviews, key file maps, local setup guides, common task runbooks, debugging guides, and contribution guidelines. Outputs to Markdown, Notion, or Confluence.

## Core Capabilities

- **Architecture overview** — tech stack, system boundaries, data flow diagrams
- **Key file map** — what's important and why, with annotations
- **Local setup guide** — step-by-step from clone to running tests
- **Common developer tasks** — how to add a route, run migrations, create a component
- **Debugging guide** — common errors, log locations, useful queries
- **Contribution guidelines** — branch strategy, PR process, code style
- **Audience-aware output** — junior, senior, or contractor mode

---

## When to Use

- Onboarding a new team member or contractor
- After a major refactor that made existing docs stale
- Before open-sourcing a project
- Creating a team wiki page for a service
- Self-documenting before a long vacation

---

## Codebase Analysis Commands

Run these before generating docs to gather facts:

```bash
# Project overview
cat package.json | jq '{name, version, scripts, dependencies: (.dependencies | keys), devDependencies: (.devDependencies | keys)}'

# Directory structure (top 2 levels)
find . -maxdepth 2 -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/.next/*' | sort | head -60

# Largest files (often core modules)
find src/ -name "*.ts" -not -path "*/test*" -exec wc -l {} + | sort -rn | head -20

# All routes (Next.js App Router)
find app/ -name "route.ts" -o -name "page.tsx" | sort

# All routes (Express)
grep -rn "router\.\(get\|post\|put\|patch\|delete\)" src/routes/ --include="*.ts"

# Recent major changes
git log --oneline --since="90 days ago" | grep -E "feat|refactor|breaking"

# Top contributors
git shortlog -sn --no-merges | head -10

# Test coverage summary
pnpm test:ci --coverage 2>&1 | tail -20
```

---

## Generated Documentation Template

### README.md — Full Template

```markdown
# [Project Name]

> One-sentence description of what this does and who uses it.

[![CI](https://github.com/org/repo/actions/workflows/ci.yml/badge.svg)](https://github.com/org/repo/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/org/repo/branch/main/graph/badge.svg)](https://codecov.io/gh/org/repo)

## What is this?

[2-3 sentences: problem it solves, who uses it, current state]

**Live:** https://myapp.com  
**Staging:** https://staging.myapp.com  
**Docs:** https://docs.myapp.com

---

## Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| Node.js | 20+ | `nvm install 20` |
| pnpm | 8+ | `npm i -g pnpm` |
| Docker | 24+ | [docker.com](https://docker.com) |
| PostgreSQL | 16+ | via Docker (see below) |

### Setup (5 minutes)

```bash
# 1. Clone
git clone https://github.com/org/repo
cd repo

# 2. Install dependencies
pnpm install

# 3. Start infrastructure
docker compose up -d   # Starts Postgres, Redis

# 4. Environment
cp .env.example .env
# Edit .env — ask a teammate for real values or see Vault

# 5. Database setup
pnpm db:migrate        # Run migrations
pnpm db:seed           # Optional: load test data

# 6. Start dev server
pnpm dev               # → http://localhost:3000

# 7. Verify
pnpm test              # Should be all green
```

### Verify it works

- [ ] `http://localhost:3000` loads the app
- [ ] `http://localhost:3000/api/health` returns `{"status":"ok"}`
- [ ] `pnpm test` passes

---

## Architecture

### System Overview

```
Browser / Mobile
    │
    ▼
[Next.js App] ←──── [Auth: NextAuth]
    │
    ├──→ [PostgreSQL] (primary data store)
    ├──→ [Redis] (sessions, job queue)
    └──→ [S3] (file uploads)
         
Background:
[BullMQ workers] ←── Redis queue
    └──→ [External APIs: Stripe, SendGrid]
```

### Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Frontend | Next.js 14 (App Router) | SSR, file-based routing |
| Styling | Tailwind CSS + shadcn/ui | Rapid UI development |
| API | Next.js Route Handlers | Co-located with frontend |
| Database | PostgreSQL 16 | Relational, RLS for multi-tenancy |
| ORM | Drizzle ORM | Type-safe, lightweight |
| Auth | NextAuth v5 | OAuth + email/password |
| Queue | BullMQ + Redis | Background jobs |
| Storage | AWS S3 | File uploads |
| Email | SendGrid | Transactional email |
| Payments | Stripe | Subscriptions |
| Deployment | Vercel (app) + Railway (workers) | |
| Monitoring | Sentry + Datadog | |

---

## Key Files

| Path | Purpose |
|------|---------|
| `app/` | Next.js App Router — pages and API routes |
| `app/api/` | API route handlers |
| `app/(auth)/` | Auth pages (login, register, reset) |
| `app/(app)/` | Protected app pages |
| `src/db/` | Database schema, migrations, client |
| `src/db/schema.ts` | **Drizzle schema — single source of truth** |
| `src/lib/` | Shared utilities (auth, email, stripe) |
| `src/lib/auth.ts` | **Auth configuration — read this first** |
| `src/components/` | Reusable React components |
| `src/hooks/` | Custom React hooks |
| `src/types/` | Shared TypeScript types |
| `workers/` | BullMQ background job processors |
| `emails/` | React Email templates |
| `tests/` | Test helpers, factories, integration tests |
| `.env.example` | All env vars with descriptions |
| `docker-compose.yml` | Local infrastructure |

---

## Common Developer Tasks

### Add a new API endpoint

```bash
# 1. Create route handler
touch app/api/my-resource/route.ts
```

```typescript
// app/api/my-resource/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { auth } from '@/lib/auth'
import { db } from '@/db/client'

export async function GET(req: NextRequest) {
  const session = await auth()
  if (!session) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }
  
  const data = await db.query.myResource.findMany({
    where: (r, { eq }) => eq(r.userId, session.user.id),
  })
  
  return NextResponse.json({ data })
}
```

```bash
# 2. Add tests
touch tests/api/my-resource.test.ts

# 3. Add to OpenAPI spec (if applicable)
pnpm generate:openapi
```

### Run a database migration

```bash
# Create migration
pnpm db:generate     # Generates SQL from schema changes

# Review the generated SQL
cat drizzle/migrations/0001_my_change.sql

# Apply
pnpm db:migrate

# Roll back (manual — inspect generated SQL and revert)
psql $DATABASE_URL -f scripts/rollback_0001.sql
```

### Add a new email template

```bash
# 1. Create template
touch emails/my-email.tsx

# 2. Preview in browser
pnpm email:preview

# 3. Send in code
import { sendEmail } from '@/lib/email'
await sendEmail({
  to: user.email,
  subject: 'Subject line',
  template: 'my-email',
  props: { name: "username"
})
```

### Add a background job

```typescript
// 1. Define job in workers/jobs/my-job.ts
import { Queue, Worker } from 'bullmq'
import { redis } from '@/lib/redis'

export const myJobQueue = new Queue('my-job', { connection: redis })

export const myJobWorker = new Worker('my-job', async (job) => {
  const { userId, data } = job.data
  // do work
}, { connection: redis })

// 2. Enqueue
await myJobQueue.add('process', { userId, data }, {
  attempts: 3,
  backoff: { type: 'exponential', delay: 1000 },
})
```

---

## Debugging Guide

### Common Errors

**`Error: DATABASE_URL is not set`**
```bash
# Check your .env file exists and has the var
cat .env | grep DATABASE_URL

# Start Postgres if not running
docker compose up -d postgres
```

**`PrismaClientKnownRequestError: P2002 Unique constraint failed`**
```
User already exists with that email. Check: is this a duplicate registration?
Run: SELECT * FROM users WHERE email = 'test@example.com';
```

**`Error: JWT expired`**
```bash
# Dev: extend token TTL in .env
JWT_EXPIRES_IN=30d

# Check clock skew between server and client
date && docker exec postgres date
```

**`500 on /api/*` in local dev**
```bash
# 1. Check terminal for stack trace
# 2. Check database connectivity
psql $DATABASE_URL -c "SELECT 1"
# 3. Check Redis
redis-cli ping
# 4. Check logs
pnpm dev 2>&1 | grep -E "error|Error|ERROR"
```

### Useful SQL Queries

```sql
-- Find slow queries (requires pg_stat_statements)
SELECT query, mean_exec_time, calls, total_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 20;

-- Check active connections
SELECT count(*), state FROM pg_stat_activity GROUP BY state;

-- Find bloated tables
SELECT relname, n_dead_tup, n_live_tup,
  round(n_dead_tup::numeric/nullif(n_live_tup,0)*100, 2) AS dead_pct
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC;
```

### Debug Authentication

```bash
# Decode a JWT (no secret needed for header/payload)
echo "YOUR_JWT" | cut -d. -f2 | base64 -d | jq .

# Check session in DB
psql $DATABASE_URL -c "SELECT * FROM sessions WHERE user_id = 'usr_...' ORDER BY expires_at DESC LIMIT 5;"
```

### Log Locations

| Environment | Logs |
|-------------|------|
| Local dev | Terminal running `pnpm dev` |
| Vercel production | Vercel dashboard → Logs |
| Workers (Railway) | Railway dashboard → Deployments → Logs |
| Database | `docker logs postgres` (local) |
| Background jobs | `pnpm worker:dev` terminal |

---

## Contribution Guidelines

### Branch Strategy

```
main           → production (protected, requires PR + CI)
  └── feature/PROJ-123-short-desc
  └── fix/PROJ-456-bug-description
  └── chore/update-dependencies
```

### PR Requirements

- [ ] Branch name includes ticket ID (e.g., `feature/PROJ-123-...`)
- [ ] PR description explains the why
- [ ] All CI checks pass
- [ ] Test coverage doesn't decrease
- [ ] Self-reviewed (read your own diff before requesting review)
- [ ] Screenshots/video for UI changes

### Commit Convention

```
feat(scope): short description       → new feature
fix(scope): short description        → bug fix
chore: update dependencies           → maintenance
docs: update API reference           → documentation
```

### Code Style

```bash
# Lint + format
pnpm lint
pnpm format

# Type check
pnpm typecheck

# All checks (run before pushing)
pnpm validate
```

---

## Audience-Specific Notes

### For Junior Developers
- Start with `src/lib/auth.ts` to understand authentication
- Read existing tests in `tests/api/` — they document expected behavior
- Ask before touching anything in `src/db/schema.ts` — schema changes affect everyone
- Use `pnpm db:seed` to get realistic local data

### For Senior Engineers / Tech Leads
- Architecture decisions are documented in `docs/adr/` (Architecture Decision Records)
- Performance benchmarks: `pnpm bench` — baseline is in `tests/benchmarks/baseline.json`
- Security model: RLS policies in `src/db/rls.sql`, enforced at DB level
- Scaling notes: `docs/scaling.md`

### For Contractors
- Scope is limited to `src/features/[your-feature]/` unless discussed
- Never push directly to `main`
- All external API calls go through `src/lib/` wrappers (for mocking in tests)
- Time estimates: log in Linear ticket comments daily

---

## Output Formats
→ See references/output-format-templates.md for details

## Common Pitfalls

- **Docs written once, never updated** — add doc updates to PR checklist
- **Missing local setup step** — test setup instructions on a fresh machine quarterly
- **No error troubleshooting** — debugging section is the most valuable part for new hires
- **Too much detail for contractors** — they need task-specific, not architecture-deep docs
- **No screenshots** — UI flows need screenshots; they go stale but are still valuable
- **Skipping the "why"** — document why decisions were made, not just what was decided

---

## Best Practices

1. **Keep setup under 10 minutes** — if it takes longer, fix the setup, not the docs
2. **Test the docs** — have a new hire follow them literally, fix every gap they hit
3. **Link, don't repeat** — link to ADRs, issues, and external docs instead of duplicating
4. **Update in the same PR** — docs changes alongside code changes
5. **Version-specific notes** — call out things that changed in recent versions
6. **Runbooks over theory** — "run this command" beats "the system uses Redis for..."
