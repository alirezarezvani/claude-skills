# Env & Secrets Manager

**Tier:** POWERFUL
**Category:** Engineering
**Domain:** Security / DevOps / Configuration Management

---

## Overview

Complete environment and secrets management workflow: .env file lifecycle across dev/staging/prod,
.env.example auto-generation, required-var validation, secret leak detection in git history, and
credential rotation playbook. Integrates with HashiCorp Vault, AWS SSM, 1Password CLI, and Doppler.

---

## Core Capabilities

- **.env lifecycle** — create, validate, sync across environments
- **.env.example generation** — strip values, preserve keys and comments
- **Validation script** — fail-fast on missing required vars at startup
- **Secret leak detection** — regex scan of git history and working tree
- **Rotation workflow** — detect → scope → rotate → deploy → verify
- **Secret manager integrations** — Vault KV v2, AWS SSM, 1Password, Doppler

---

## When to Use

- Setting up a new project — scaffold .env.example and validation
- Before every commit — scan for accidentally staged secrets
- Post-incident response — leaked credential rotation procedure
- Onboarding new developers — they need all vars, not just some
- Environment drift investigation — prod behaving differently from staging

---

## .env File Structure

### Canonical Layout
```bash
# .env.example — committed to git (no values)
# .env.local   — developer machine (gitignored)
# .env.staging — CI/CD or secret manager reference
# .env.prod    — never on disk; pulled from secret manager at runtime

# Application
APP_NAME=
APP_ENV=                    # dev | staging | prod
APP_PORT=3000               # default port if not set
APP_SECRET=                 # REQUIRED: JWT signing secret (min 32 chars)
APP_URL=                    # REQUIRED: public base URL

# Database
DATABASE_URL=               # REQUIRED: full connection string
DATABASE_POOL_MIN=2
DATABASE_POOL_MAX=10

# Auth
AUTH_JWT_SECRET=            # REQUIRED
AUTH_JWT_EXPIRY=3600        # seconds
AUTH_REFRESH_SECRET=        # REQUIRED

# Third-party APIs
STRIPE_SECRET_KEY=          # REQUIRED in prod
STRIPE_WEBHOOK_SECRET=      # REQUIRED in prod
SENDGRID_API_KEY=

# Storage
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=eu-central-1
AWS_S3_BUCKET=

# Monitoring
SENTRY_DSN=
DD_API_KEY=
```

---

## .gitignore Patterns

Add to your project's `.gitignore`:

```gitignore
# Environment files — NEVER commit these
.env
.env.local
.env.development
.env.development.local
.env.test.local
.env.staging
.env.staging.local
.env.production
.env.production.local
.env.prod
.env.*.local

# Secret files
*.pem
*.key
*.p12
*.pfx
secrets.json
secrets.yaml
secrets.yml
credentials.json
service-account.json

# AWS
.aws/credentials

# Terraform state (may contain secrets)
*.tfstate
*.tfstate.backup
.terraform/

# Kubernetes secrets
*-secret.yaml
*-secrets.yaml
```

---

## .env.example Auto-Generation

```bash
#!/bin/bash
# scripts/gen-env-example.sh
# Strips values from .env, preserves keys, defaults, and comments

INPUT="${1:-.env}"
OUTPUT="${2:-.env.example}"

if [ ! -f "$INPUT" ]; then
  echo "ERROR: $INPUT not found"
  exit 1
fi

python3 - "$INPUT" "$OUTPUT" << 'PYEOF'
import sys, re

input_file = sys.argv[1]
output_file = sys.argv[2]
lines = []

with open(input_file) as f:
    for line in f:
        stripped = line.rstrip('\n')
        # Keep blank lines and comments as-is
        if stripped == '' or stripped.startswith('#'):
            lines.append(stripped)
            continue
        # Match KEY=VALUE or KEY="VALUE"
        m = re.match(r'^([A-Z_][A-Z0-9_]*)=(.*)$', stripped)
        if m:
            key = m.group(1)
            value = m.group(2).strip('"\'')
            # Keep non-sensitive defaults (ports, regions, feature flags)
            safe_defaults = re.compile(
                r'^(APP_PORT|APP_ENV|APP_NAME|AWS_REGION|DATABASE_POOL_|LOG_LEVEL|'
                r'FEATURE_|CACHE_TTL|RATE_LIMIT_|PAGINATION_|TIMEOUT_)',
                re.I
            )
            sensitive = re.compile(
                r'(SECRET|KEY|TOKEN|PASSWORD|PASS|CREDENTIAL|DSN|AUTH|PRIVATE|CERT)',
                re.I
            )
            if safe_defaults.match(key) and value:
                lines.append(f"{key}={value}  # default")
            else:
                lines.append(f"{key}=")
        else:
            lines.append(stripped)

with open(output_file, 'w') as f:
    f.write('\n'.join(lines) + '\n')

print(f"Generated {output_file} from {input_file}")
PYEOF
```

Usage:
```bash
bash scripts/gen-env-example.sh .env .env.example
# Commit .env.example, never .env
git add .env.example
```

---

## Required Variable Validation Script

```bash
#!/bin/bash
# scripts/validate-env.sh
# Run at app startup or in CI before deploy
# Exit 1 if any required var is missing or empty

set -euo pipefail

MISSING=()
WARNINGS=()

# --- Define required vars by environment ---
ALWAYS_REQUIRED=(
  APP_SECRET
  APP_URL
  DATABASE_URL
  AUTH_JWT_SECRET
  AUTH_REFRESH_SECRET
)

PROD_REQUIRED=(
  STRIPE_SECRET_KEY
  STRIPE_WEBHOOK_SECRET
  SENTRY_DSN
)

# --- Check always-required vars ---
for var in "${ALWAYS_REQUIRED[@]}"; do
  if [ -z "${!var:-}" ]; then
    MISSING+=("$var")
  fi
done

# --- Check prod-only vars ---
if [ "${APP_ENV:-}" = "production" ] || [ "${NODE_ENV:-}" = "production" ]; then
  for var in "${PROD_REQUIRED[@]}"; do
    if [ -z "${!var:-}" ]; then
      MISSING+=("$var (required in production)")
    fi
  done
fi

# --- Validate format/length constraints ---
if [ -n "${AUTH_JWT_SECRET:-}" ] && [ ${#AUTH_JWT_SECRET} -lt 32 ]; then
  WARNINGS+=("AUTH_JWT_SECRET is shorter than 32 chars — insecure")
fi

if [ -n "${DATABASE_URL:-}" ]; then
  if ! echo "$DATABASE_URL" | grep -qE "^(postgres|postgresql|mysql|mongodb|redis)://"; then
    WARNINGS+=("DATABASE_URL doesn't look like a valid connection string")
  fi
fi

if [ -n "${APP_PORT:-}" ]; then
  if ! [[ "$APP_PORT" =~ ^[0-9]+$ ]] || [ "$APP_PORT" -lt 1 ] || [ "$APP_PORT" -gt 65535 ]; then
    WARNINGS+=("APP_PORT=$APP_PORT is not a valid port number")
  fi
fi

# --- Report ---
if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo "WARNINGS:"
  for w in "${WARNINGS[@]}"; do
    echo "  ⚠️  $w"
  done
fi

if [ ${#MISSING[@]} -gt 0 ]; then
  echo ""
  echo "FATAL: Missing required environment variables:"
  for var in "${MISSING[@]}"; do
    echo "  ❌  $var"
  done
  echo ""
  echo "Copy .env.example to .env and fill in missing values."
  exit 1
fi

echo "✅  All required environment variables are set"
```

Node.js equivalent:
```typescript
// src/config/validateEnv.ts
const required = [
  'APP_SECRET', 'APP_URL', 'DATABASE_URL',
  'AUTH_JWT_SECRET', 'AUTH_REFRESH_SECRET',
]

const missing = required.filter(key => !process.env[key])

if (missing.length > 0) {
  console.error('FATAL: Missing required environment variables:', missing)
  process.exit(1)
}

if (process.env.AUTH_JWT_SECRET && process.env.AUTH_JWT_SECRET.length < 32) {
  console.error('FATAL: AUTH_JWT_SECRET must be at least 32 characters')
  process.exit(1)
}

export const config = {
  appSecret: process.env.APP_SECRET!,
  appUrl: process.env.APP_URL!,
  databaseUrl: process.env.DATABASE_URL!,
  jwtSecret: process.env.AUTH_JWT_SECRET!,
  refreshSecret: process.env.AUTH_REFRESH_SECRET!,
  stripeKey: process.env.STRIPE_SECRET_KEY,  // optional
  port: parseInt(process.env.APP_PORT ?? '3000', 10),
} as const
```

---

## Secret Leak Detection

### Scan Working Tree
```bash
#!/bin/bash
# scripts/scan-secrets.sh
# Scan staged files and working tree for common secret patterns

FAIL=0

check() {
  local label="$1"
  local pattern="$2"
  local matches

  matches=$(git diff --cached -U0 2>/dev/null | grep "^+" | grep -vE "^(\+\+\+|#|\/\/)" | \
    grep -E "$pattern" | grep -v ".env.example" | grep -v "test\|mock\|fixture\|fake" || true)

  if [ -n "$matches" ]; then
    echo "SECRET DETECTED [$label]:"
    echo "$matches" | head -5
    FAIL=1
  fi
}

# AWS Access Keys
check "AWS Access Key" "AKIA[0-9A-Z]{16}"
check "AWS Secret Key" "aws_secret_access_key\s*=\s*['\"]?[A-Za-z0-9/+]{40}"

# Stripe
check "Stripe Live Key"   "sk_live_[0-9a-zA-Z]{24,}"
check "Stripe Test Key"   "sk_test_[0-9a-zA-Z]{24,}"
check "Stripe Webhook"    "whsec_[0-9a-zA-Z]{32,}"

# JWT / Generic secrets
check "Hardcoded JWT"     "eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}"
check "Generic Secret"    "(secret|password|passwd|api_key|apikey|token)\s*[:=]\s*['\"][^'\"]{12,}['\"]"

# Private keys
check "Private Key Block" "-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----"
check "PEM Certificate"   "-----BEGIN CERTIFICATE-----"

# Connection strings with credentials
check "DB Connection"     "(postgres|mysql|mongodb)://[^:]+:[^@]+@"
check "Redis Auth"        "redis://:[^@]+@\|rediss://:[^@]+@"

# Google
check "Google API Key"    "AIza[0-9A-Za-z_-]{35}"
check "Google OAuth"      "[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com"

# GitHub
check "GitHub Token"      "gh[ps]_[A-Za-z0-9]{36,}"
check "GitHub Fine-grained" "github_pat_[A-Za-z0-9_]{82}"

# Slack
check "Slack Token"       "xox[baprs]-[0-9A-Za-z]{10,}"
check "Slack Webhook"     "https://hooks\.slack\.com/services/[A-Z0-9]{9,}/[A-Z0-9]{9,}/[A-Za-z0-9]{24,}"

# Twilio
check "Twilio SID"        "AC[a-z0-9]{32}"
check "Twilio Token"      "SK[a-z0-9]{32}"

if [ $FAIL -eq 1 ]; then
  echo ""
  echo "BLOCKED: Secrets detected in staged changes."
  echo "Remove secrets before committing. Use environment variables instead."
  echo "If this is a false positive, add it to .secretsignore or use:"
  echo "  git commit --no-verify  (only if you're 100% certain it's safe)"
  exit 1
fi

echo "No secrets detected in staged changes."
```

### Scan Git History (post-incident)
```bash
#!/bin/bash
# scripts/scan-history.sh — scan entire git history for leaked secrets

PATTERNS=(
  "AKIA[0-9A-Z]{16}"
  "sk_live_[0-9a-zA-Z]{24}"
  "sk_test_[0-9a-zA-Z]{24}"
  "-----BEGIN.*PRIVATE KEY-----"
  "AIza[0-9A-Za-z_-]{35}"
  "ghp_[A-Za-z0-9]{36}"
  "xox[baprs]-[0-9A-Za-z]{10,}"
)

for pattern in "${PATTERNS[@]}"; do
  echo "Scanning for: $pattern"
  git log --all -p --no-color 2>/dev/null | \
    grep -n "$pattern" | \
    grep "^+" | \
    grep -v "^+++" | \
    head -10
done

# Alternative: use truffleHog or gitleaks for comprehensive scanning
# gitleaks detect --source . --log-opts="--all"
# trufflehog git file://. --only-verified
```

---

## Pre-commit Hook Installation

```bash
#!/bin/bash
# Install the pre-commit hook
HOOK_PATH=".git/hooks/pre-commit"

cat > "$HOOK_PATH" << 'HOOK'
#!/bin/bash
# Pre-commit: scan for secrets before every commit

SCRIPT="scripts/scan-secrets.sh"

if [ -f "$SCRIPT" ]; then
  bash "$SCRIPT"
else
  # Inline fallback if script not present
  if git diff --cached -U0 | grep "^+" | grep -qE "AKIA[0-9A-Z]{16}|sk_live_|-----BEGIN.*PRIVATE KEY"; then
    echo "BLOCKED: Possible secret detected in staged changes."
    exit 1
  fi
fi
HOOK

chmod +x "$HOOK_PATH"
echo "Pre-commit hook installed at $HOOK_PATH"
```

Using `pre-commit` framework (recommended for teams):
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: local
    hooks:
      - id: validate-env-example
        name: Check .env.example is up to date
        language: script
        entry: bash scripts/check-env-example.sh
        pass_filenames: false
```

---

## Credential Rotation Workflow

When a secret is leaked or compromised:

### Step 1 — Detect & Confirm
```bash
# Confirm which secret was exposed
git log --all -p --no-color | grep -A2 -B2 "AKIA\|sk_live_\|SECRET"

# Check if secret is in any open PRs
gh pr list --state open | while read pr; do
  gh pr diff $(echo $pr | awk '{print $1}') | grep -E "AKIA|sk_live_" && echo "Found in PR: $pr"
done
```

### Step 2 — Identify Exposure Window
```bash
# Find first commit that introduced the secret
git log --all -p --no-color -- "*.env" "*.json" "*.yaml" "*.ts" "*.py" | \
  grep -B 10 "THE_LEAKED_VALUE" | grep "^commit" | tail -1

# Get commit date
git show --format="%ci" COMMIT_HASH | head -1

# Check if secret appears in public repos (GitHub)
gh api search/code -X GET -f q="THE_LEAKED_VALUE" | jq '.total_count, .items[].html_url'
```

### Step 3 — Rotate Credential
Per service — rotate immediately:
- **AWS**: IAM console → delete access key → create new → update everywhere
- **Stripe**: Dashboard → Developers → API keys → Roll key
- **GitHub PAT**: Settings → Developer Settings → Personal access tokens → Revoke → Create new
- **DB password**: `ALTER USER app_user PASSWORD 'new-strong-password-here';`
- **JWT secret**: Rotate key (all existing sessions invalidated — users re-login)

### Step 4 — Update All Environments
```bash
# Update secret manager (source of truth)
# Then redeploy to pull new values

# Vault KV v2
vault kv put secret/myapp/prod \
  STRIPE_SECRET_KEY="sk_live_NEW..." \
  APP_SECRET="new-secret-here"

# AWS SSM
aws ssm put-parameter \
  --name "/myapp/prod/STRIPE_SECRET_KEY" \
  --value "sk_live_NEW..." \
  --type "SecureString" \
  --overwrite

# 1Password
op item edit "MyApp Prod" \
  --field "STRIPE_SECRET_KEY[password]=sk_live_NEW..."

# Doppler
doppler secrets set STRIPE_SECRET_KEY="sk_live_NEW..." --project myapp --config prod
```

### Step 5 — Remove from Git History
```bash
# WARNING: rewrites history — coordinate with team first
git filter-repo --path-glob "*.env" --invert-paths

# Or remove specific string from all commits
git filter-repo --replace-text <(echo "LEAKED_VALUE==>REDACTED")

# Force push all branches (requires team coordination + force push permissions)
git push origin --force --all

# Notify all developers to re-clone
```

### Step 6 — Verify
```bash
# Confirm secret no longer in history
git log --all -p | grep "LEAKED_VALUE" | wc -l  # should be 0

# Test new credentials work
curl -H "Authorization: Bearer $NEW_TOKEN" https://api.service.com/test

# Monitor for unauthorized usage of old credential (check service audit logs)
```

---

## Secret Manager Integrations

### HashiCorp Vault KV v2
```bash
# Setup
export VAULT_ADDR="https://vault.internal.company.com"
export VAULT_TOKEN="$(vault login -method=oidc -format=json | jq -r '.auth.client_token')"

# Write secrets
vault kv put secret/myapp/prod \
  DATABASE_URL="postgres://user:pass@host/db" \
  APP_SECRET="$(openssl rand -base64 32)"

# Read secrets into env
eval $(vault kv get -format=json secret/myapp/prod | \
  jq -r '.data.data | to_entries[] | "export \(.key)=\(.value)"')

# In CI/CD (GitHub Actions)
# Use vault-action: hashicorp/vault-action@v2
```

### AWS SSM Parameter Store
```bash
# Write (SecureString = encrypted with KMS)
aws ssm put-parameter \
  --name "/myapp/prod/DATABASE_URL" \
  --value "postgres://..." \
  --type "SecureString" \
  --key-id "alias/myapp-secrets"

# Read all params for an app/env into shell
eval $(aws ssm get-parameters-by-path \
  --path "/myapp/prod/" \
  --with-decryption \
  --query "Parameters[*].[Name,Value]" \
  --output text | \
  awk '{split($1,a,"/"); print "export " a[length(a)] "=\"" $2 "\""}')

# In Node.js at startup
# Use @aws-sdk/client-ssm to pull params before server starts
```

### 1Password CLI
```bash
# Authenticate
eval $(op signin)

# Get a specific field
op read "op://MyVault/MyApp Prod/STRIPE_SECRET_KEY"

# Export all fields from an item as env vars
op item get "MyApp Prod" --format json | \
  jq -r '.fields[] | select(.value != null) | "export \(.label)=\"\(.value)\""' | \
  grep -E "^export [A-Z_]+" | source /dev/stdin

# .env injection
op inject -i .env.tpl -o .env
# .env.tpl uses {{ op://Vault/Item/field }} syntax
```

### Doppler
```bash
# Setup
doppler setup  # interactive: select project + config

# Run any command with secrets injected
doppler run -- node server.js
doppler run -- npm run dev

# Export to .env (local dev only — never commit output)
doppler secrets download --no-file --format env > .env.local

# Pull specific secret
doppler secrets get DATABASE_URL --plain

# Sync to another environment
doppler secrets upload --project myapp --config staging < .env.staging.example
```

---

## Environment Drift Detection

Check if staging and prod have the same set of keys (values may differ):

```bash
#!/bin/bash
# scripts/check-env-drift.sh

# Pull key names from both environments (not values)
STAGING_KEYS=$(doppler secrets --project myapp --config staging --format json 2>/dev/null | \
  jq -r 'keys[]' | sort)
PROD_KEYS=$(doppler secrets --project myapp --config prod --format json 2>/dev/null | \
  jq -r 'keys[]' | sort)

ONLY_IN_STAGING=$(comm -23 <(echo "$STAGING_KEYS") <(echo "$PROD_KEYS"))
ONLY_IN_PROD=$(comm -13 <(echo "$STAGING_KEYS") <(echo "$PROD_KEYS"))

if [ -n "$ONLY_IN_STAGING" ]; then
  echo "Keys in STAGING but NOT in PROD:"
  echo "$ONLY_IN_STAGING" | sed 's/^/  /'
fi

if [ -n "$ONLY_IN_PROD" ]; then
  echo "Keys in PROD but NOT in STAGING:"
  echo "$ONLY_IN_PROD" | sed 's/^/  /'
fi

if [ -z "$ONLY_IN_STAGING" ] && [ -z "$ONLY_IN_PROD" ]; then
  echo "✅ No env drift detected — staging and prod have identical key sets"
fi
```

---

## Common Pitfalls

- **Committing .env instead of .env.example** — add `.env` to .gitignore on day 1; use pre-commit hooks
- **Storing secrets in CI/CD logs** — never `echo $SECRET`; mask vars in CI settings
- **Rotating only one place** — secrets often appear in Heroku, Vercel, Docker, K8s, CI — update ALL
- **Forgetting to invalidate sessions after JWT secret rotation** — all users will be logged out; communicate this
- **Using .env.example with real values** — example files are public; strip everything sensitive
- **Not monitoring after rotation** — watch audit logs for 24h after rotation to catch unauthorized old-credential use
- **Weak secrets** — `APP_SECRET=mysecret` is not a secret. Use `openssl rand -base64 32`

---

## Best Practices

1. **Secret manager is source of truth** — .env files are for local dev only; never in prod
2. **Rotate on a schedule**, not just after incidents — quarterly minimum for long-lived keys
3. **Principle of least privilege** — each service gets its own API key with minimal permissions
4. **Audit access** — log every secret read in Vault/SSM; alert on anomalous access
5. **Never log secrets** — add log scrubbing middleware that redacts known secret patterns
6. **Use short-lived credentials** — prefer OIDC/instance roles over long-lived access keys
7. **Separate secrets per environment** — never share a key between dev and prod
8. **Document rotation runbooks** — before an incident, not during one
