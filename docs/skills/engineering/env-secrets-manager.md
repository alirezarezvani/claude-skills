---
title: "Env & Secrets Manager"
description: "Env & Secrets Manager - Claude Code skill from the Engineering - POWERFUL domain."
---

# Env & Secrets Manager

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `env-secrets-manager`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/env-secrets-manager/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


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
→ See references/validation-detection-rotation.md for details

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
