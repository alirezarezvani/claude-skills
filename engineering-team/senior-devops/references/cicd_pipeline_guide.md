# CI/CD Pipeline Guide

Reference for designing and implementing CI/CD pipelines across GitHub Actions, GitLab CI, and Jenkins.

---

## Table of Contents

- [Pipeline Architecture](#pipeline-architecture)
- [GitHub Actions](#github-actions)
- [GitLab CI](#gitlab-ci)
- [Pipeline Patterns](#pipeline-patterns)
- [Security Scanning](#security-scanning)
- [Artifact Management](#artifact-management)

---

## Pipeline Architecture

### Standard Pipeline Stages

```
┌─────────────────────────────────────────────────────────────┐
│                    CI/CD PIPELINE FLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────┐   ┌───────┐   ┌──────┐   ┌────────┐   ┌──────┐ │
│  │ LINT   │ → │ TEST  │ → │BUILD │ → │ SCAN   │ → │DEPLOY│ │
│  │        │   │       │   │      │   │        │   │      │ │
│  │ESLint  │   │Unit   │   │Docker│   │SAST    │   │Stage │ │
│  │Prettier│   │Integ  │   │Build │   │DAST    │   │Prod  │ │
│  │        │   │E2E    │   │Push  │   │Deps    │   │      │ │
│  └────────┘   └───────┘   └──────┘   └────────┘   └──────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Stage Responsibilities

| Stage | Purpose | Failure Action |
|-------|---------|----------------|
| Lint | Code style, formatting | Block merge |
| Test | Unit, integration, E2E | Block merge |
| Build | Container image, artifacts | Block deploy |
| Scan | Security vulnerabilities | Block deploy (high/critical) |
| Deploy | Release to environment | Rollback |

### Environment Progression

```
Feature Branch → PR → main → staging → production
     │           │      │        │           │
     │           │      │        │           └── Manual approval
     │           │      │        └── Auto deploy
     │           │      └── Auto deploy (main merge)
     │           └── PR checks pass
     └── Push triggers CI
```

---

## GitHub Actions

### Basic Workflow Structure

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run lint
      - run: npm run format:check

  test:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'
      - run: npm ci
      - run: npm run test:coverage
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      - uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  build:
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image_tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
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
            type=sha,prefix=
            type=ref,event=branch
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  security-scan:
    runs-on: ubuntu-latest
    needs: build
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          format: 'sarif'
          output: 'trivy-results.sarif'
          severity: 'CRITICAL,HIGH'

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
```

### Deploy Workflow

```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  workflow_run:
    workflows: ["CI Pipeline"]
    branches: [main]
    types: [completed]

jobs:
  deploy-staging:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster staging-cluster \
            --service app-service \
            --force-new-deployment

      - name: Wait for deployment
        run: |
          aws ecs wait services-stable \
            --cluster staging-cluster \
            --services app-service

  deploy-production:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster production-cluster \
            --service app-service \
            --force-new-deployment
```

### Reusable Workflows

```yaml
# .github/workflows/reusable-deploy.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
      cluster:
        required: true
        type: string
    secrets:
      AWS_ACCESS_KEY_ID:
        required: true
      AWS_SECRET_ACCESS_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment: ${{ inputs.environment }}
    steps:
      - name: Configure AWS
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1

      - name: Deploy
        run: |
          aws ecs update-service \
            --cluster ${{ inputs.cluster }} \
            --service app-service \
            --force-new-deployment
```

---

## GitLab CI

### Basic Pipeline

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - build
  - scan
  - deploy

variables:
  DOCKER_TLS_CERTDIR: "/certs"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA

# Cache node_modules across jobs
.node-cache: &node-cache
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths:
      - node_modules/

lint:
  stage: lint
  image: node:20-alpine
  <<: *node-cache
  script:
    - npm ci
    - npm run lint
    - npm run format:check
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

test:unit:
  stage: test
  image: node:20-alpine
  <<: *node-cache
  services:
    - postgres:15
  variables:
    POSTGRES_DB: test
    POSTGRES_PASSWORD: postgres
    DATABASE_URL: postgresql://postgres:postgres@postgres:5432/test
  script:
    - npm ci
    - npm run test:coverage
  coverage: '/Lines\s*:\s*(\d+\.?\d*)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura-coverage.xml

test:e2e:
  stage: test
  image: cypress/included:latest
  <<: *node-cache
  script:
    - npm ci
    - npm run build
    - npm run start &
    - npx wait-on http://localhost:3000
    - npm run test:e2e
  artifacts:
    when: on_failure
    paths:
      - cypress/screenshots/
      - cypress/videos/

build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  before_script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
  script:
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

security:sast:
  stage: scan
  image: returntocorp/semgrep
  script:
    - semgrep --config auto --sarif --output semgrep.sarif .
  artifacts:
    reports:
      sast: semgrep.sarif
  allow_failure: true

security:container:
  stage: scan
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE_TAG
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:staging:
  stage: deploy
  image: alpine/k8s:1.28.0
  environment:
    name: staging
    url: https://staging.example.com
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n staging
    - kubectl rollout status deployment/app -n staging --timeout=300s
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

deploy:production:
  stage: deploy
  image: alpine/k8s:1.28.0
  environment:
    name: production
    url: https://app.example.com
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n production
    - kubectl rollout status deployment/app -n production --timeout=300s
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
```

---

## Pipeline Patterns

### Matrix Builds

**GitHub Actions:**
```yaml
test:
  strategy:
    matrix:
      node-version: [18, 20, 22]
      os: [ubuntu-latest, macos-latest]
  runs-on: ${{ matrix.os }}
  steps:
    - uses: actions/setup-node@v4
      with:
        node-version: ${{ matrix.node-version }}
    - run: npm test
```

**GitLab CI:**
```yaml
test:
  parallel:
    matrix:
      - NODE_VERSION: ['18', '20', '22']
  image: node:${NODE_VERSION}
  script:
    - npm test
```

### Conditional Deployment

```yaml
# Deploy only when specific paths change
deploy:
  rules:
    - if: $CI_COMMIT_BRANCH == "main"
      changes:
        - src/**/*
        - package.json
        - Dockerfile
```

### Monorepo Pipeline

```yaml
# GitHub Actions for monorepo
on:
  push:
    paths:
      - 'packages/api/**'
      - 'packages/web/**'

jobs:
  detect-changes:
    outputs:
      api: ${{ steps.filter.outputs.api }}
      web: ${{ steps.filter.outputs.web }}
    steps:
      - uses: dorny/paths-filter@v2
        id: filter
        with:
          filters: |
            api:
              - 'packages/api/**'
            web:
              - 'packages/web/**'

  build-api:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.api == 'true' }}
    # ...

  build-web:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.web == 'true' }}
    # ...
```

---

## Security Scanning

### SAST Tools Integration

| Tool | Language | Integration |
|------|----------|-------------|
| Semgrep | Multi-language | CLI, CI action |
| CodeQL | Multi-language | GitHub native |
| Bandit | Python | CLI |
| ESLint security | JavaScript | npm |
| Gosec | Go | CLI |

### Dependency Scanning

```yaml
# GitHub Actions
- name: Dependency Review
  uses: actions/dependency-review-action@v3
  with:
    fail-on-severity: high

# npm audit in CI
- name: Security audit
  run: npm audit --audit-level=high
```

### Container Scanning

```yaml
# Trivy scan
- name: Scan container
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: ${{ env.IMAGE }}
    exit-code: '1'
    severity: 'CRITICAL,HIGH'
    ignore-unfixed: true
```

---

## Artifact Management

### Docker Image Tagging

| Tag Type | Example | Use Case |
|----------|---------|----------|
| SHA | `abc123f` | Unique identifier |
| Branch | `main`, `develop` | Latest from branch |
| Semver | `v1.2.3` | Release versions |
| Latest | `latest` | Convenience (avoid in prod) |

### Caching Strategies

**GitHub Actions:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

**Docker layer caching:**
```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

---

## Quick Reference

### GitHub Actions Syntax

| Concept | Syntax |
|---------|--------|
| Environment variable | `${{ env.VAR }}` |
| Secret | `${{ secrets.SECRET }}` |
| Context | `${{ github.sha }}` |
| Output | `${{ steps.id.outputs.name }}` |
| Conditional | `if: ${{ condition }}` |

### GitLab CI Keywords

| Keyword | Purpose |
|---------|---------|
| `rules` | When to run job |
| `needs` | Job dependencies |
| `artifacts` | Pass files between jobs |
| `cache` | Speed up jobs |
| `services` | Linked containers |
| `environment` | Deployment target |

---

*See also: `deployment_strategies.md` for deployment patterns*
