# CI/CD Pipeline Builder

**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** DevOps / Automation  

---

## Overview

Analyzes your project stack and generates production-ready CI/CD pipeline configurations for GitHub Actions, GitLab CI, and Bitbucket Pipelines. Handles matrix testing, caching strategies, deployment stages, environment promotion, and secret management — tailored to your actual tech stack.

## Core Capabilities

- **Stack detection** — reads `package.json`, `Dockerfile`, `pyproject.toml`, `go.mod`, etc.
- **Pipeline generation** — GitHub Actions, GitLab CI, Bitbucket Pipelines
- **Matrix testing** — multi-version, multi-OS, multi-environment
- **Smart caching** — npm, pip, Docker layer, Gradle, Maven
- **Deployment stages** — build → test → staging → production with approvals
- **Environment promotion** — automatic on green tests, manual gate for production
- **Secret management** — patterns for GitHub Secrets, GitLab CI Variables, Vault, AWS SSM

---

## When to Use

- Starting a new project and need a CI/CD baseline
- Migrating from one CI platform to another
- Adding deployment stages to an existing pipeline
- Auditing a slow pipeline and optimizing caching
- Setting up environment promotion with manual approval gates

---

## Workflow

### Step 1 — Stack Detection

Ask Claude to analyze your repo:

```
Analyze my repo and generate a GitHub Actions CI/CD pipeline.
Check: package.json, Dockerfile, .nvmrc, pyproject.toml, go.mod
```

Claude will inspect:

| File | Signals |
|------|---------|
| `package.json` | Node version, test runner, build tool |
| `.nvmrc` / `.node-version` | Exact Node version |
| `Dockerfile` | Base image, multi-stage build |
| `pyproject.toml` | Python version, test runner |
| `go.mod` | Go version |
| `vercel.json` | Vercel deployment config |
| `k8s/` or `helm/` | Kubernetes deployment |

---

## Complete Example: Next.js + Vercel

```yaml
# .github/workflows/ci.yml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  NODE_VERSION: '20'
  PNPM_VERSION: '8'

jobs:
  lint-typecheck:
    name: Lint & Typecheck
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm lint
      - run: pnpm typecheck

  test:
    name: Test (Node ${{ matrix.node }})
    runs-on: ubuntu-latest
    strategy:
      matrix:
        node: ['18', '20', '22']
      fail-fast: false
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Run tests with coverage
        run: pnpm test:ci
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}
      - name: Upload coverage
        uses: codecov/codecov-action@v4
        with:
          token: ${{ secrets.CODECOV_TOKEN }}

  build:
    name: Build
    runs-on: ubuntu-latest
    needs: [lint-typecheck, test]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: ${{ env.PNPM_VERSION }}
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - name: Build
        run: pnpm build
        env:
          NEXT_PUBLIC_API_URL: ${{ vars.NEXT_PUBLIC_API_URL }}
      - uses: actions/upload-artifact@v4
        with:
          name: build-${{ github.sha }}
          path: .next/
          retention-days: 7

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/develop'
    environment:
      name: staging
      url: https://staging.myapp.com
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main'
    environment:
      name: production
      url: https://myapp.com
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'
```

---

## Complete Example: Python + AWS Lambda

```yaml
# .github/workflows/deploy.yml
name: Python Lambda CI/CD

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.11', '3.12']
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: 'pip'
      - run: pip install -r requirements-dev.txt
      - run: pytest tests/ -v --cov=src --cov-report=xml
      - run: mypy src/
      - run: ruff check src/ tests/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'
      - run: pip install bandit safety
      - run: bandit -r src/ -ll
      - run: safety check

  package:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Build Lambda zip
        run: |
          pip install -r requirements.txt --target ./package
          cd package && zip -r ../lambda.zip .
          cd .. && zip lambda.zip -r src/
      - uses: actions/upload-artifact@v4
        with:
          name: lambda-${{ github.sha }}
          path: lambda.zip

  deploy-staging:
    needs: package
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: lambda-${{ github.sha }}
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-1
      - run: |
          aws lambda update-function-code \
            --function-name myapp-staging \
            --zip-file fileb://lambda.zip

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/download-artifact@v4
        with:
          name: lambda-${{ github.sha }}
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: eu-west-1
      - run: |
          aws lambda update-function-code \
            --function-name myapp-production \
            --zip-file fileb://lambda.zip
          VERSION=$(aws lambda publish-version \
            --function-name myapp-production \
            --query 'Version' --output text)
          aws lambda update-alias \
            --function-name myapp-production \
            --name live \
            --function-version $VERSION
```

---

## Complete Example: Docker + Kubernetes

```yaml
# .github/workflows/k8s-deploy.yml
name: Docker + Kubernetes

on:
  push:
    branches: [main]
    tags: ['v*']

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    outputs:
      image-digest: ${{ steps.push.outputs.digest }}

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix=sha-

      - name: Build and push
        id: push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    needs: build-push
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - name: Set kubeconfig
        run: |
          echo "${{ secrets.KUBE_CONFIG_STAGING }}" | base64 -d > /tmp/kubeconfig
          echo "KUBECONFIG=/tmp/kubeconfig" >> $GITHUB_ENV
      - name: Deploy
        run: |
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build-push.outputs.image-digest }} \
            -n staging
          kubectl rollout status deployment/myapp -n staging --timeout=5m

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: azure/setup-kubectl@v3
      - name: Set kubeconfig
        run: |
          echo "${{ secrets.KUBE_CONFIG_PROD }}" | base64 -d > /tmp/kubeconfig
          echo "KUBECONFIG=/tmp/kubeconfig" >> $GITHUB_ENV
      - name: Canary deploy
        run: |
          kubectl set image deployment/myapp-canary \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build-push.outputs.image-digest }} \
            -n production
          kubectl rollout status deployment/myapp-canary -n production --timeout=5m
          sleep 120
          kubectl set image deployment/myapp \
            myapp=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}@${{ needs.build-push.outputs.image-digest }} \
            -n production
          kubectl rollout status deployment/myapp -n production --timeout=10m
```

---

## GitLab CI Equivalent

```yaml
# .gitlab-ci.yml
stages: [lint, test, build, deploy-staging, deploy-production]

variables:
  NODE_VERSION: "20"
  DOCKER_BUILDKIT: "1"

.node-cache: &node-cache
  cache:
    key:
      files: [pnpm-lock.yaml]
    paths:
      - node_modules/
      - .pnpm-store/

lint:
  stage: lint
  image: node:${NODE_VERSION}-alpine
  <<: *node-cache
  script:
    - corepack enable && pnpm install --frozen-lockfile
    - pnpm lint && pnpm typecheck

test:
  stage: test
  image: node:${NODE_VERSION}-alpine
  <<: *node-cache
  parallel:
    matrix:
      - NODE_VERSION: ["18", "20", "22"]
  script:
    - corepack enable && pnpm install --frozen-lockfile
    - pnpm test:ci
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'

deploy-staging:
  stage: deploy-staging
  environment:
    name: staging
    url: https://staging.myapp.com
  only: [develop]
  script:
    - npx vercel --token=$VERCEL_TOKEN

deploy-production:
  stage: deploy-production
  environment:
    name: production
    url: https://myapp.com
  only: [main]
  when: manual
  script:
    - npx vercel --prod --token=$VERCEL_TOKEN
```

---

## Secret Management Patterns

### GitHub Actions — Secret Hierarchy
```
Repository secrets   → all branches
Environment secrets  → only that environment
Organization secrets → all repos in org
```

### Fetching from AWS SSM at runtime
```yaml
- name: Load secrets from SSM
  run: |
    DB_URL=$(aws ssm get-parameter \
      --name "/myapp/production/DATABASE_URL" \
      --with-decryption \
      --query 'Parameter.Value' --output text)
    echo "DATABASE_URL=$DB_URL" >> $GITHUB_ENV
  env:
    AWS_REGION: eu-west-1
```

### HashiCorp Vault integration
```yaml
- uses: hashicorp/vault-action@v2
  with:
    url: ${{ secrets.VAULT_ADDR }}
    token: ${{ secrets.VAULT_TOKEN }}
    secrets: |
      secret/data/myapp/prod DATABASE_URL | DATABASE_URL ;
      secret/data/myapp/prod API_KEY | API_KEY
```

---

## Caching Cheat Sheet

| Stack | Cache key | Cache path |
|-------|-----------|------------|
| npm | `package-lock.json` | `~/.npm` |
| pnpm | `pnpm-lock.yaml` | `~/.pnpm-store` |
| pip | `requirements.txt` | `~/.cache/pip` |
| poetry | `poetry.lock` | `~/.cache/pypoetry` |
| Docker | SHA of Dockerfile | GHA cache (type=gha) |
| Go | `go.sum` | `~/go/pkg/mod` |

---

## Common Pitfalls

- **Secrets in logs** — never `echo $SECRET`; use `::add-mask::$SECRET` if needed
- **No concurrency limits** — add `concurrency:` to cancel stale runs on PR push
- **Skipping `--frozen-lockfile`** — lockfile drift breaks reproducibility
- **No rollback plan** — test `kubectl rollout undo` or `vercel rollback` before you need it
- **Mutable image tags** — never use `latest` in production; tag by git SHA
- **Missing environment protection rules** — set required reviewers in GitHub Environments

---

## Best Practices

1. **Fail fast** — lint/typecheck before expensive test jobs
2. **Artifact immutability** — Docker image tagged by git SHA
3. **Environment parity** — same image through all envs, config via env vars
4. **Canary first** — 10% traffic + error rate check before 100%
5. **Pin action versions** — `@v4` not `@main`
6. **Least privilege** — each job gets only the IAM scopes it needs
7. **Notify on failure** — Slack webhook for production deploy failures
