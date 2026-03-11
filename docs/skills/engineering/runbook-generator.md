---
title: "Runbook Generator"
description: "Runbook Generator - Claude Code skill from the Engineering - POWERFUL domain."
---

# Runbook Generator

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `runbook-generator`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/runbook-generator/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** DevOps / Site Reliability Engineering  

---

## Overview

Analyze a codebase and generate production-grade operational runbooks. Detects your stack (CI/CD, database, hosting, containers), then produces step-by-step runbooks with copy-paste commands, verification checks, rollback procedures, escalation paths, and time estimates. Keeps runbooks fresh with staleness detection linked to config file modification dates.

---

## Core Capabilities

- **Stack detection** — auto-identify CI/CD, database, hosting, orchestration from repo files
- **Runbook types** — deployment, incident response, database maintenance, scaling, monitoring setup
- **Format discipline** — numbered steps, copy-paste commands, ✅ verification checks, time estimates
- **Escalation paths** — L1 → L2 → L3 with contact info and decision criteria
- **Rollback procedures** — every deployment step has a corresponding undo
- **Staleness detection** — runbook sections reference config files; flag when source changes
- **Testing methodology** — dry-run framework for staging validation, quarterly review cadence

---

## When to Use

Use when:
- A codebase has no runbooks and you need to bootstrap them fast
- Existing runbooks are outdated or incomplete (point at the repo, regenerate)
- Onboarding a new engineer who needs clear operational procedures
- Preparing for an incident response drill or audit
- Setting up monitoring and on-call rotation from scratch

Skip when:
- The system is too early-stage to have stable operational patterns
- Runbooks already exist and only need minor updates (edit directly)

---

## Stack Detection

When given a repo, scan for these signals before writing a single runbook line:

```bash
# CI/CD
ls .github/workflows/     → GitHub Actions
ls .gitlab-ci.yml         → GitLab CI
ls Jenkinsfile            → Jenkins
ls .circleci/             → CircleCI
ls bitbucket-pipelines.yml → Bitbucket Pipelines

# Database
grep -r "postgresql\|postgres\|pg" package.json pyproject.toml → PostgreSQL
grep -r "mysql\|mariadb"           package.json               → MySQL
grep -r "mongodb\|mongoose"        package.json               → MongoDB
grep -r "redis"                    package.json               → Redis
ls prisma/schema.prisma            → Prisma ORM (check provider field)
ls drizzle.config.*                → Drizzle ORM

# Hosting
ls vercel.json                     → Vercel
ls railway.toml                    → Railway
ls fly.toml                        → Fly.io
ls .ebextensions/                  → AWS Elastic Beanstalk
ls terraform/  ls *.tf             → Custom AWS/GCP/Azure (check provider)
ls kubernetes/ ls k8s/             → Kubernetes
ls docker-compose.yml              → Docker Compose

# Framework
ls next.config.*                   → Next.js
ls nuxt.config.*                   → Nuxt
ls svelte.config.*                 → SvelteKit
cat package.json | jq '.scripts'   → Check build/start commands
```

Map detected stack → runbook templates. A Next.js + PostgreSQL + Vercel + GitHub Actions repo needs:
- Deployment runbook (Vercel + GitHub Actions)
- Database runbook (PostgreSQL backup, migration, vacuum)
- Incident response (with Vercel logs + pg query debugging)
- Monitoring setup (Vercel Analytics, pg_stat, alerting)

---

## Runbook Types

### 1. Deployment Runbook

```markdown
# Deployment Runbook — [App Name]
**Stack:** Next.js 14 + PostgreSQL 15 + Vercel  
**Last verified:** 2025-03-01  
**Source configs:** vercel.json (modified: git log -1 --format=%ci -- vercel.json)  
**Owner:** Platform Team  
**Est. total time:** 15–25 min  

---

## Pre-deployment Checklist
- [ ] All PRs merged to main
- [ ] CI passing on main (GitHub Actions green)
- [ ] Database migrations tested in staging
- [ ] Rollback plan confirmed

## Steps

### Step 1 — Run CI checks locally (3 min)
```bash
pnpm test
pnpm lint
pnpm build
```
✅ Expected: All pass with 0 errors. Build output in `.next/`

### Step 2 — Apply database migrations (5 min)
```bash
# Staging first
DATABASE_URL=$STAGING_DATABASE_URL npx prisma migrate deploy
```
✅ Expected: `All migrations have been successfully applied.`

```bash
# Verify migration applied
psql $STAGING_DATABASE_URL -c "\d" | grep -i migration
```
✅ Expected: Migration table shows new entry with today's date

### Step 3 — Deploy to production (5 min)
```bash
git push origin main
# OR trigger manually:
vercel --prod
```
✅ Expected: Vercel dashboard shows deployment in progress. URL format:
`https://app-name-<hash>-team.vercel.app`

### Step 4 — Smoke test production (5 min)
```bash
# Health check
curl -sf https://your-app.vercel.app/api/health | jq .

# Critical path
curl -sf https://your-app.vercel.app/api/users/me \
  -H "Authorization: Bearer $TEST_TOKEN" | jq '.id'
```
✅ Expected: health returns `{"status":"ok","db":"connected"}`. Users API returns valid ID.

### Step 5 — Monitor for 10 min
- Check Vercel Functions log for errors: `vercel logs --since=10m`
- Check error rate in Vercel Analytics: < 1% 5xx
- Check DB connection pool: `SELECT count(*) FROM pg_stat_activity;` (< 80% of max_connections)

---

## Rollback

If smoke tests fail or error rate spikes:

```bash
# Instant rollback via Vercel (preferred — < 30 sec)
vercel rollback [previous-deployment-url]

# Database rollback (only if migration was applied)
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate reset --skip-seed
# WARNING: This resets to previous migration. Confirm data impact first.
```

✅ Expected after rollback: Previous deployment URL becomes active. Verify with smoke test.

---

## Escalation
- **L1 (on-call engineer):** Check Vercel logs, run smoke tests, attempt rollback
- **L2 (platform lead):** DB issues, data loss risk, rollback failed — Slack: @platform-lead
- **L3 (CTO):** Production down > 30 min, data breach — PagerDuty: #critical-incidents
```

---

### 2. Incident Response Runbook

```markdown
# Incident Response Runbook
**Severity levels:** P1 (down), P2 (degraded), P3 (minor)  
**Est. total time:** P1: 30–60 min, P2: 1–4 hours  

## Phase 1 — Triage (5 min)

### Confirm the incident
```bash
# Is the app responding?
curl -sw "%{http_code}" https://your-app.vercel.app/api/health -o /dev/null

# Check Vercel function errors (last 15 min)
vercel logs --since=15m | grep -i "error\|exception\|5[0-9][0-9]"
```
✅ 200 = app up. 5xx or timeout = incident confirmed.

Declare severity:
- Site completely down → P1 — page L2/L3 immediately
- Partial degradation / slow responses → P2 — notify team channel
- Single feature broken → P3 — create ticket, fix in business hours

---

## Phase 2 — Diagnose (10–15 min)

```bash
# Recent deployments — did something just ship?
vercel ls --limit=5

# Database health
psql $DATABASE_URL -c "SELECT pid, state, wait_event, query FROM pg_stat_activity WHERE state != 'idle' LIMIT 20;"

# Long-running queries (> 30 sec)
psql $DATABASE_URL -c "SELECT pid, now() - pg_stat_activity.query_start AS duration, query FROM pg_stat_activity WHERE state = 'active' AND now() - pg_stat_activity.query_start > interval '30 seconds';"

# Connection pool saturation
psql $DATABASE_URL -c "SELECT count(*), max_conn FROM pg_stat_activity, (SELECT setting::int AS max_conn FROM pg_settings WHERE name='max_connections') t GROUP BY max_conn;"
```

Diagnostic decision tree:
- Recent deploy + new errors → rollback (see Deployment Runbook)
- DB query timeout / pool saturation → kill long queries, scale connections
- External dependency failing → check status pages, add circuit breaker
- Memory/CPU spike → check Vercel function logs for infinite loops

---

## Phase 3 — Mitigate (variable)

```bash
# Kill a runaway DB query
psql $DATABASE_URL -c "SELECT pg_terminate_backend(<pid>);"

# Scale DB connections (Supabase/Neon — adjust pool size)
# Vercel → Settings → Environment Variables → update DATABASE_POOL_MAX

# Enable maintenance mode (if you have a feature flag)
vercel env add MAINTENANCE_MODE true production
vercel --prod  # redeploy with flag
```

---

## Phase 4 — Resolve & Postmortem

After incident is resolved, within 24 hours:

1. Write incident timeline (what happened, when, who noticed, what fixed it)
2. Identify root cause (5-Whys)
3. Define action items with owners and due dates
4. Update this runbook if a step was missing or wrong
5. Add monitoring/alert that would have caught this earlier

**Postmortem template:** `docs/postmortems/YYYY-MM-DD-incident-title.md`

---

## Escalation Path

| Level | Who | When | Contact |
|-------|-----|------|---------|
| L1 | On-call engineer | Always first | PagerDuty rotation |
| L2 | Platform lead | DB issues, rollback needed | Slack @platform-lead |
| L3 | CTO/VP Eng | P1 > 30 min, data loss | Phone + PagerDuty |
```

---

### 3. Database Maintenance Runbook

```markdown
# Database Maintenance Runbook — PostgreSQL
**Schedule:** Weekly vacuum (automated), monthly manual review  

## Backup

```bash
# Full backup
pg_dump $DATABASE_URL \
  --format=custom \
  --compress=9 \
  --file="backup-$(date +%Y%m%d-%H%M%S).dump"
```
✅ Expected: File created, size > 0. `pg_restore --list backup.dump | head -20` shows tables.

Verify backup is restorable (test monthly):
```bash
pg_restore --dbname=$STAGING_DATABASE_URL backup.dump
psql $STAGING_DATABASE_URL -c "SELECT count(*) FROM users;"
```
✅ Expected: Row count matches production.

## Migration

```bash
# Always test in staging first
DATABASE_URL=$STAGING_DATABASE_URL npx prisma migrate deploy
# Verify, then:
DATABASE_URL=$PROD_DATABASE_URL npx prisma migrate deploy
```
✅ Expected: `All migrations have been successfully applied.`

⚠️ For large table migrations (> 1M rows), use `pg_repack` or add column with DEFAULT separately to avoid table locks.

## Vacuum & Reindex

```bash
# Check bloat before deciding
psql $DATABASE_URL -c "
SELECT schemaname, tablename, 
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size,
       n_dead_tup, n_live_tup,
       ROUND(n_dead_tup::numeric / NULLIF(n_live_tup + n_dead_tup, 0) * 100, 1) AS dead_ratio
FROM pg_stat_user_tables
ORDER BY n_dead_tup DESC LIMIT 10;"

# Vacuum high-bloat tables (non-blocking)
psql $DATABASE_URL -c "VACUUM ANALYZE users;"
psql $DATABASE_URL -c "VACUUM ANALYZE events;"

# Reindex (use CONCURRENTLY to avoid locks)
psql $DATABASE_URL -c "REINDEX INDEX CONCURRENTLY users_email_idx;"
```
✅ Expected: dead_ratio drops below 5% after vacuum.
```

---

## Staleness Detection

Add a staleness header to every runbook:

```markdown
## Staleness Check
This runbook references the following config files. If they've changed since the
"Last verified" date, review the affected steps.

| Config File | Last Modified | Affects Steps |
|-------------|--------------|---------------|
| vercel.json | `git log -1 --format=%ci -- vercel.json` | Step 3, Rollback |
| prisma/schema.prisma | `git log -1 --format=%ci -- prisma/schema.prisma` | Step 2, DB Maintenance |
| .github/workflows/deploy.yml | `git log -1 --format=%ci -- .github/workflows/deploy.yml` | Step 1, Step 3 |
| docker-compose.yml | `git log -1 --format=%ci -- docker-compose.yml` | All scaling steps |
```

**Automation:** Add a CI job that runs weekly and comments on the runbook doc if any referenced file was modified more recently than the runbook's "Last verified" date.

---

## Runbook Testing Methodology

### Dry-Run in Staging

Before trusting a runbook in production, validate every step in staging:

```bash
# 1. Create a staging environment mirror
vercel env pull .env.staging
source .env.staging

# 2. Run each step with staging credentials
# Replace all $DATABASE_URL with $STAGING_DATABASE_URL
# Replace all production URLs with staging URLs

# 3. Verify expected outputs match
# Document any discrepancies and update the runbook

# 4. Time each step — update estimates in the runbook
time npx prisma migrate deploy
```

### Quarterly Review Cadence

Schedule a 1-hour review every quarter:

1. **Run each command** in staging — does it still work?
2. **Check config drift** — compare "Last Modified" dates vs "Last verified"
3. **Test rollback procedures** — actually roll back in staging
4. **Update contact info** — L1/L2/L3 may have changed
5. **Add new failure modes** discovered in the past quarter
6. **Update "Last verified" date** at top of runbook

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Commands that require manual copy of dynamic values | Use env vars — `$DATABASE_URL` not `postgres://user:pass@host/db` |
| No expected output specified | Add ✅ with exact expected string after every verification step |
| Rollback steps missing | Every destructive step needs a corresponding undo |
| Runbooks that never get tested | Schedule quarterly staging dry-runs in team calendar |
| L3 escalation contact is the former CTO | Review contact info every quarter |
| Migration runbook doesn't mention table locks | Call out lock risk for large table operations explicitly |

---

## Best Practices

1. **Every command must be copy-pasteable** — no placeholder text, use env vars
2. **✅ after every step** — explicit expected output, not "it should work"
3. **Time estimates are mandatory** — engineers need to know if they have time to fix before SLA breach
4. **Rollback before you deploy** — plan the undo before executing
5. **Runbooks live in the repo** — `docs/runbooks/`, versioned with the code they describe
6. **Postmortem → runbook update** — every incident should improve a runbook
7. **Link, don't duplicate** — reference the canonical config file, don't copy its contents into the runbook
8. **Test runbooks like you test code** — untested runbooks are worse than no runbooks (false confidence)
