---
name: deploy-verify
description: >
  Production deployment closed-loop verification workflow. Ensures zero-surprise
  deployments with a mandatory 7-step process: pre-deploy checks, backup, deploy
  (with atomic swap and sensitive file exclusion), file integrity verification
  (SHA-256 diff), functional verification (HTTP + page checks), log monitoring
  (with secret redaction), and team notification. Covers database migrations,
  cache clearing, rollback with security review, and cross-OS permission fixes.
  Works with any web stack (PHP, Node.js, Python, Go, etc.) and any deployment
  method (tar, rsync, scp, CI/CD). Use this skill whenever deploying code to a
  remote server, syncing files to production, pushing to a live environment, or
  when the user says "deploy", "sync to server", "push to production", "upload
  to server", "go live", or any variation. Also use proactively after making code
  changes that should be deployed. If something goes wrong in production and you
  suspect a deployment issue (missing files, old versions, permission errors),
  use this skill to diagnose.
---

# Deploy & Verify: Production Deployment Closed-Loop

A battle-tested 7-step workflow that ensures every deployment to a production server
is complete, verified, and monitored. Born from real incidents where "it's deployed"
turned out to mean "only 3 of 18 changed files actually made it to the server."

> Note: This document is written in English for AI agent consumption. When communicating
> deployment status or issues to the user, use their preferred language.

## Project-Specific Deploy Scripts

If the project already has deployment scripts (e.g., `deploy.sh`, `deploy-prod.sh`),
**use them instead of running raw commands**. These scripts encode project-specific
knowledge (correct SSH flags, server paths, permission fixes) that this generic
workflow cannot cover.

Use this skill to:
1. **Verify** that existing scripts follow the 7-step pattern
2. **Fill gaps** where scripts skip steps (e.g., missing integrity verification)
3. **Guide manual deployment** when no script exists
4. **Diagnose failures** when something goes wrong after scripted deployment

## The 7-Step Closed Loop

```
PRE-CHECK → BACKUP → DEPLOY → VERIFY FILES → VERIFY FUNCTION → MONITOR LOGS → NOTIFY
    ↓          ↓        ↓          ↓               ↓                ↓            ↓
  Syntax    Snapshot   Transfer   SHA-256       HTTP 200        No new errors   Team
  + scope   + offsite  + perms    diff = 0     + pages work     for 2-5 min    aware
  + build   + rotate   + caches
```

Every step must pass before proceeding to the next. If any step fails, stop and fix
before continuing.

---

## Security: Credential Management

**NEVER hardcode passwords, API keys, or tokens in deployment scripts or source code.**

### Recommended approaches (in order of preference)

1. **SSH key authentication** (strongly recommended):
   ```bash
   ssh-keygen -t ed25519 -C "deploy-key"
   ssh-copy-id -i ~/.ssh/id_ed25519.pub -p PORT root@SERVER
   # Then scripts need no password at all
   ```

2. **Password file** (minimum acceptable):
   ```bash
   # Store password outside the repo, mode 600, secure cleanup
   echo 'your-password' > ~/.deploy_pw && chmod 600 ~/.deploy_pw
   sshpass -f ~/.deploy_pw ssh ...
   # After deploy session: shred -u ~/.deploy_pw
   ```

3. **Environment variables** (for CI/CD):
   ```bash
   export DEPLOY_PASS="..."  # set in CI secrets, never in repo
   sshpass -p "$DEPLOY_PASS" ssh ...
   ```

### Pre-commit safeguards

```bash
# .gitignore — block credential files
*.sshpw
*.pem
*.key
.env*
```

**Audit**: Run `grep -rn 'sshpass -p' *.sh` periodically to find hardcoded passwords.

---

## Step 1: Pre-Deploy Checks

Before touching the server, verify locally that the code is ready.

### Syntax validation

Run language-specific syntax checks on changed files:

```bash
# PHP
find app config core -name "*.php" -exec php -l {} \; 2>&1 | grep -v "No syntax errors"

# Node.js / TypeScript
npx tsc --noEmit  # or: node -c file.js

# Python
python -m py_compile file.py  # or: python -m compileall .

# Go
go build ./... && go vet ./...
```

### Scope assessment

Understand what you're deploying and its blast radius:

| What changed | Impact | Extra steps needed |
|---|---|---|
| Routes / middleware | Global — all pages affected | Test all page types |
| Templates / views | Specific pages affected | Test affected pages |
| Frontend JS/CSS | Need rebuild/bundle | Run build before deploy |
| Database schema | May need migration | See Step 3.5 below |
| Config files | May need env var updates | Check server .env |
| Core framework | Everything affected | Full verification |

### Build step (if frontend changed)

```bash
npm run build  # or: node scripts/build.js
ls -la dist/   # verify timestamps updated
```

### Diff review

```bash
git diff --stat HEAD~1   # what changed in the last commit
git log --oneline -5     # recent commit context
```

---

## Step 2: Backup

Always have a rollback path. Store backups in at least TWO locations.

```bash
# Primary: on the server (fast restore)
ssh SERVER "tar czf /root/backup_$(date +%Y%m%d_%H%M%S).tar.gz \
  -C /path/to/site app/ config/ public/ core/ resources/"

# Secondary: pull a copy locally (disaster recovery)
scp SERVER:/root/backup_LATEST.tar.gz ~/backups/server_$(date +%Y%m%d).tar.gz
```

### Backup rotation

```bash
# Keep only last 10 backups on server
ssh SERVER "ls -t /root/backup_*.tar.gz | tail -n +11 | xargs -r rm"
```

### Database backup (if migrations are involved)

```bash
# MySQL
ssh SERVER "mysqldump -u USER -pPASS DB_NAME > /root/db_backup_$(date +%Y%m%d_%H%M%S).sql"

# PostgreSQL
ssh SERVER "pg_dump -U USER DB_NAME > /root/db_backup_$(date +%Y%m%d_%H%M%S).sql"
```

---

## Step 3: Deploy

### File transfer — ALWAYS exclude sensitive files

```bash
# tar method (recommended)
tar czf - \
  --exclude='.env' --exclude='.env.*' \
  --exclude='*.pem' --exclude='*.key' --exclude='*.p12' \
  --exclude='storage/database/*.sqlite' \
  --exclude='storage/logs/*' \
  --exclude='storage/sessions/*' \
  --exclude='node_modules' --exclude='vendor' \
  app/ config/ core/ public/ resources/ scripts/ \
  | ssh SERVER "cd /path/to/site && tar xzf - --no-same-owner --no-same-permissions"

# rsync method
rsync -avz --chmod=D755,F644 \
  --exclude='.env' --exclude='.env.*' --exclude='*.pem' --exclude='*.key' \
  --exclude='storage/logs/*' --exclude='storage/sessions/*' \
  -e "ssh -p PORT" app/ config/ public/ root@SERVER:/path/to/site/
```

**Files to NEVER deploy** (server-specific):
- `.env` — database credentials, API keys, environment flags
- `*.pem`, `*.key` — SSL certificates, private keys
- `storage/database/` — production database files
- `storage/logs/`, `storage/sessions/` — runtime data
- `vendor/`, `node_modules/` — install from lock file on server

### Handling interrupted transfers

Network interruptions can leave the server in an inconsistent state.

```bash
# Safer: deploy to staging directory first, then swap
ssh SERVER "mkdir -p /tmp/deploy_staging"
tar czf - --exclude='.env' app/ config/ | \
  ssh SERVER "cd /tmp/deploy_staging && tar xzf - --no-same-owner"

# Only after full extraction succeeds, copy to production
ssh SERVER "rsync -a /tmp/deploy_staging/ /path/to/site/ && rm -rf /tmp/deploy_staging"
```

### Permission fix (CRITICAL for cross-OS deployments)

When deploying from macOS/Windows to Linux, file ownership gets mangled.

```bash
# Fix ownership — use the correct web server user
ssh SERVER "chown -R www:www /path/to/site/app/ /path/to/site/config/ /path/to/site/public/"

# Fix file permissions — distinguish scripts from code files
ssh SERVER "find /path/to/site/app /path/to/site/config /path/to/site/resources \
  -type f -not -name '*.sh' -not -name '.user.ini' -perm 600 | xargs -r chmod 644"
ssh SERVER "find /path/to/site/scripts -type f -name '*.sh' | xargs -r chmod 750"
ssh SERVER "find /path/to/site -type d | xargs -r chmod 755"
```

### Restart application server

```bash
# PHP-FPM — CHOOSE based on your server setup:

# Option A: Full restart (clears OPcache, brief downtime)
# Use when: standalone server, no CDN/proxy in front
ssh SERVER "/etc/init.d/php-fpm restart"

# Option B: Graceful reload via USR2 (minimal downtime)
# Use when: server behind Cloudflare/CDN where restart causes 520/502
ssh SERVER "kill -USR2 $(cat /run/php-fpm.pid)"
# Note: USR2 does NOT clear OPcache. Clear separately if needed.

# Node.js (PM2)
ssh SERVER "pm2 restart app-name"

# Python (gunicorn)
ssh SERVER "systemctl restart gunicorn"
```

> **Warning**: If your server is behind Cloudflare or a reverse proxy, a full `restart`
> creates a brief window triggering 520 errors. Use Option B or graceful restart.

### Clear server-side caches

```bash
# FastCGI cache (nginx)
ssh SERVER "find /www/server/fastcgi_cache -type f -delete 2>/dev/null; nginx -s reload"

# Varnish
ssh SERVER "varnishadm 'ban req.url ~ .'"

# CDN cache (Cloudflare)
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/purge_cache" \
  -H "Authorization: Bearer TOKEN" -d '{"purge_everything":true}'

# Redis application cache
ssh SERVER "redis-cli FLUSHDB"  # or selective: redis-cli DEL key_pattern
```

---

## Step 3.5: Database Migration (if applicable)

Database schema changes must be coordinated with code deployment.

### Migration order depends on the change type

| Change type | Order | Rationale |
|---|---|---|
| Add nullable column | Migrate FIRST, then deploy | Old code ignores new column |
| Add NOT NULL column | Deploy code (with default) FIRST | Old DB won't have column |
| Drop column | Deploy code that stops using it FIRST | Old code would crash |
| Add index | Migrate FIRST (can be done live) | No code dependency |
| Drop table | Deploy code FIRST, then migrate | Old code references it |
| Rename column | Two-step: add new → deploy → copy → drop old | Atomic rename breaks old code |

### Execution

```bash
# Backup database FIRST (see Step 2)

# Run migration
ssh SERVER "cd /path/to/site && php artisan migrate"
# or: ssh SERVER "mysql -u USER -pPASS DB_NAME < migration.sql"

# Verify
ssh SERVER "mysql -u USER -pPASS DB_NAME -e 'DESCRIBE table_name;'"
```

### Migration rollback

```bash
# Reverse migration (preferred — preserves new data)
ssh SERVER "cd /path/to/site && php artisan migrate:rollback"

# Full DB restore (loses data created after backup — last resort)
ssh SERVER "mysql -u USER -pPASS DB_NAME < /root/db_backup_XXXXXXXX.sql"
```

> **Warning**: If the migration ran in production and users created new data,
> restoring from backup will LOSE that data. Prefer reverse migrations.

---

## Step 4: Verify File Integrity

This is the step most people skip — and it's the most important one.

### Cross-platform checksums

```bash
# Detect local checksum command
if command -v sha256sum &>/dev/null; then
    SUMCMD="sha256sum"
elif command -v shasum &>/dev/null; then
    SUMCMD="shasum -a 256"
else
    echo "ERROR: No SHA-256 tool found"; exit 1
fi

# Local checksums
find app config core bootstrap resources public/assets scripts \
  -type f \( -name "*.php" -o -name "*.js" -o -name "*.css" -o -name "*.html" \
             -o -name "*.json" -o -name "*.sh" -o -name "*.py" -o -name "*.go" \) \
  -not -name ".env" -not -name "*.key" -not -name "*.pem" \
  -exec $SUMCMD {} \; | awk '{print $1, $NF}' | sort -k2 > /tmp/local_checksums.txt

# Remote checksums (Linux)
ssh SERVER "cd /path/to/site && find app config core bootstrap resources public/assets scripts \
  -type f \( -name '*.php' -o -name '*.js' -o -name '*.css' -o -name '*.html' \
             -o -name '*.json' -o -name '*.sh' -o -name '*.py' -o -name '*.go' \) \
  -not -name '.env' -not -name '*.key' -not -name '*.pem' \
  -exec sha256sum {} \;" | awk '{print $1, $NF}' | sort -k2 > /tmp/remote_checksums.txt

# Compare — must show 0 differences
diff /tmp/local_checksums.txt /tmp/remote_checksums.txt
```

**Note**: Using `$NF` (last field) instead of `$2` handles filenames with spaces.

### Interpreting results

- Same file, different hash → old version on server, re-deploy
- Local only → missing on server, re-sync
- Remote only → server-generated file, usually fine

**Rule: don't declare "deployed" until the diff count is 0.**

### When to run full verification

- **Every deploy**: spot-check changed files (minimum)
- **Every 5th incremental deploy**: full SHA-256 sweep
- **User reports missing feature**: full sweep immediately
- **First deploy to new server**: full sweep mandatory

---

## Step 5: Verify Function

Files being present doesn't mean the app works. Test it.

### HTTP status check

```bash
# Use HEAD requests to avoid triggering business logic or polluting analytics
ssh SERVER "curl -s -I -o /dev/null -w '%{http_code}' \
  -H 'Host: example.com' http://localhost/"
# Expected: 200

# Health endpoint (if available — preferred over page checks)
ssh SERVER "curl -s http://localhost/health | \
  python3 -c 'import sys,json; d=json.load(sys.stdin); print(\"OK\" if d.get(\"status\")==\"ok\" else \"FAIL\")'"
```

### What to verify based on what changed

| Change type | What to test |
|---|---|
| Middleware / routing | Every major page type (home, detail, list, API) |
| Admin templates | Admin panel login + all menu sections visible |
| Frontend JS/CSS | Hard refresh, check browser console for errors |
| API endpoints | curl each changed endpoint, verify response format |
| Database changes | Test queries that use changed tables/columns |
| Auth / session | Login flow, protected pages, logout |

---

## Step 6: Monitor Logs

After deployment, watch for new errors for 2-5 minutes.

- **Minimum**: 2 minutes of active monitoring
- **Routing/middleware changes**: 5 minutes
- **Database migrations**: 15 minutes

> **Security note**: Error logs may contain database passwords, API keys, and user PII.
> Always redact sensitive data when viewing logs, especially during screen sharing.

```bash
# Redacted log monitoring — strips passwords, tokens, and keys
ssh SERVER "tail -50 /path/to/site/storage/logs/error.log 2>/dev/null" | \
  grep -i "error\|fatal\|exception" | \
  sed 's/password=[^ ]*/password=***REDACTED***/gi' | \
  sed 's/Bearer [A-Za-z0-9._-]*/Bearer ***REDACTED***/g' | \
  sed "s/token=[^ &'\"]*/token=***REDACTED***/gi"

# Or just count errors (zero information leakage)
ssh SERVER "tail -50 /path/to/site/storage/logs/error.log 2>/dev/null" | \
  grep -ci "error\|fatal\|exception"

# Nginx error log
ssh SERVER "tail -20 /var/log/nginx/error.log 2>/dev/null" | grep -v "favicon"
```

### Interpreting results

- **No new errors** → Deployment successful
- **New errors related to your changes** → Fix immediately or rollback
- **Pre-existing errors** → Note them, don't block on them

---

## Step 7: Notify (recommended)

For team environments or critical deployments, send a notification.

```bash
# Telegram
curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/sendMessage" \
  -d chat_id="${CHAT_ID}" \
  -d text="Deploy to ${SERVER} completed at $(date). Status: OK"

# Slack
curl -s -X POST "$SLACK_WEBHOOK" \
  -H 'Content-Type: application/json' \
  -d "{\"text\":\"Deploy to ${SERVER} completed at $(date)\"}"
```

Even for solo developers, a notification creates an audit trail.

---

## Rollback

> **Security warning**: Rolling back to an older version may re-introduce security
> vulnerabilities that were fixed in the deployment you're reverting. If the current
> deployment was a security fix, prefer hot-patching the old version instead.

### Step 1: Find the backup

```bash
ssh SERVER "ls -lt /root/backup_*.tar.gz | head -5"
```

### Step 2: Restore files

```bash
ssh SERVER "cd /path/to/site && \
  tar xzf /root/backup_YYYYMMDD_HHMMSS.tar.gz --no-same-owner --no-same-permissions && \
  chown -R www:www app/ config/ public/ core/ resources/ && \
  find . -type f -perm 600 -not -name '.user.ini' | xargs -r chmod 644"
```

### Step 3: Restart + clear caches

```bash
ssh SERVER "/etc/init.d/php-fpm restart"
ssh SERVER "find /www/server/fastcgi_cache -type f -delete 2>/dev/null; nginx -s reload"
ssh SERVER "redis-cli FLUSHDB 2>/dev/null"
```

### Step 4: Verify rollback

Run Step 5 (Verify Function) and Step 6 (Monitor Logs).

### Step 5: Record the incident

```bash
ssh SERVER "echo '[ROLLBACK] $(date): rolled back to backup_XXXXXXXX. Reason: ...' >> /var/log/deploy_audit.log"
```

### Database rollback

If migrations were run, code rollback alone is NOT enough.
See Step 3.5 for database-specific rollback strategies.

### When rollback isn't enough

1. Check `git log` for the last known-good commit
2. `git checkout <good-commit>` locally
3. Re-deploy through the full 7-step workflow

---

## Multi-Server Deployment

When deploying to multiple servers, deploy in order of least risk:

### Canary deployment

1. Deploy to the **least critical** server first
2. Run full verification (Steps 4-6)
3. Wait 5-10 minutes, monitor for error spikes
4. If clean, deploy to remaining servers one at a time
5. If issues found, fix before proceeding

### Environment considerations

| Item | Staging | Production |
|---|---|---|
| .env | Test DB, debug=true | Prod DB, debug=false |
| Error display | Detailed errors | Log only |
| Caches | Disabled | Enabled |
| Deploy frequency | Every commit | Batched, low-traffic window |

---

## CI/CD Integration

The 7 steps map directly to CI/CD stages:

| Step | CI/CD stage |
|---|---|
| Pre-check | Build: lint, syntax, unit tests |
| Backup | Pre-deploy job: SSH backup |
| Deploy | Deploy job: rsync/tar/docker push |
| Verify files | Post-deploy: checksum script |
| Verify function | Smoke tests: curl health endpoints |
| Monitor logs | Post-deploy: tail + alert on errors |
| Notify | Final job: Slack/Telegram webhook |

---

## Quick Reference Checklist

- [ ] **PRE-CHECK**: Syntax passes, scope understood, assets built
- [ ] **BACKUP**: Server backup + local copy, DB backed up if migrating
- [ ] **DEPLOY**: Files transferred (secrets excluded), permissions fixed, caches cleared
- [ ] **VERIFY FILES**: SHA-256 diff shows 0 differences
- [ ] **VERIFY FUNCTION**: HTTP 200 on key pages, changed features work
- [ ] **MONITOR LOGS**: No new errors for 2+ minutes (redacted output)
- [ ] **NOTIFY**: Team informed of deployment status

---

## Anti-Patterns

| Anti-pattern | Consequence | Correct approach |
|---|---|---|
| Deploy only changed files, skip verification | Files silently stay outdated | Full SHA-256 diff |
| Say "deployed" without checking | Broken features discovered later | Evidence before claims |
| Skip permission fix on cross-OS deploy | 500 errors (web server can't read) | Always chown after deploy |
| `reload` instead of `restart` for PHP-FPM | OPcache serves stale bytecode | `restart` or USR2 + opcache_reset |
| Deploy without backup | Can't rollback | Always backup first |
| Don't check error logs | Silent errors accumulate | Tail logs 2-5 minutes |
| Deploy .env to production | Overwrites server credentials | Always exclude .env |
| `chmod 644` everything | Shell scripts lose execute bit | Distinguish .sh from code files |
| Deploy frontend JS without rebuild | Browser loads stale bundles | Rebuild + cache-bust first |
| Skip DB backup before migration | Can't reverse bad migration | Always backup DB first |

---

## Real-World Incidents

1. **18-file silent desync** — Incremental deployments over weeks left 18 files outdated.
   Admin panel missing entire menu sections. Root cause: never ran full checksum comparison.

2. **macOS ownership = Linux 500** — Files from macOS had owner `501:staff` with `600`
   permissions. Web server couldn't read them. Entire site 500 for 30 minutes.
   Root cause: no `--no-same-owner` and no `chown`.

3. **OPcache served old code** — PHP-FPM `reload` didn't clear OPcache. New code on disk
   but old bytecode executed. Root cause: reload ≠ restart for OPcache.

4. **CDN 520 from restart** — PHP-FPM `restart` behind Cloudflare caused brief upstream
   failure. All active users got 520 errors. Root cause: should have used graceful USR2.

5. **.env overwritten** — tar deployed entire config/ directory including local .env.
   Production DB credentials replaced with dev values. Site connected to wrong database.
   Root cause: no `--exclude='.env'` in deployment command.
