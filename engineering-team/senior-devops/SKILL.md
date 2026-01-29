---
name: senior-devops
description: DevOps engineering skill for CI/CD pipelines, infrastructure as code, deployment strategies, and cloud platforms. Provides automated tools for GitHub Actions/GitLab CI generation, Terraform module scaffolding, and deployment orchestration with blue-green, canary, and rolling strategies.
---

# Senior DevOps

Production-ready DevOps toolkit for CI/CD automation, infrastructure as code, and deployment orchestration.

## Table of Contents

- [Trigger Terms](#trigger-terms)
- [Quick Start](#quick-start)
- [Workflows](#workflows)
  - [1. Setup CI/CD Pipeline](#1-setup-cicd-pipeline)
  - [2. Scaffold Infrastructure](#2-scaffold-infrastructure)
  - [3. Deploy Application](#3-deploy-application)
  - [4. Blue-Green Deployment](#4-blue-green-deployment)
- [Tool Reference](#tool-reference)
- [Reference Documentation](#reference-documentation)
- [Platform Patterns](#platform-patterns)
- [Validation Checklist](#validation-checklist)

---

## Trigger Terms

Use this skill when you encounter:

| Term | Context |
|------|---------|
| `CI/CD pipeline` | Setting up automated build/test/deploy |
| `GitHub Actions` | Creating workflow YAML files |
| `GitLab CI` | Configuring .gitlab-ci.yml |
| `Terraform` | Infrastructure as code scaffolding |
| `deploy to production` | Deployment orchestration |
| `blue-green deployment` | Zero-downtime deployment strategy |
| `canary release` | Gradual traffic shifting |
| `rolling update` | Progressive pod replacement |
| `Kubernetes deployment` | K8s manifest generation |
| `ECS service` | AWS container orchestration |
| `infrastructure automation` | IaC module creation |
| `Docker build` | Container image pipelines |

---

## Quick Start

### Generate CI/CD Pipeline

```bash
# GitHub Actions for Node.js project
python scripts/pipeline_generator.py /path/to/project --platform github

# GitLab CI with Docker build
python scripts/pipeline_generator.py /path/to/project --platform gitlab --with-docker

# Full pipeline with deployment
python scripts/pipeline_generator.py /path/to/project --platform github --with-docker --with-deploy --env staging
```

### Scaffold Terraform Infrastructure

```bash
# Generate VPC + ECS + RDS modules
python scripts/terraform_scaffolder.py ./terraform --project myapp

# VPC and ECS only
python scripts/terraform_scaffolder.py ./terraform --project myapp --modules vpc,ecs

# Multiple environments
python scripts/terraform_scaffolder.py ./terraform --project myapp --environments dev,prod --region eu-west-1
```

### Deploy Application

```bash
# Rolling deployment
python scripts/deployment_manager.py deploy --name myapp --image myapp:v2 --strategy rolling

# Blue-green deployment
python scripts/deployment_manager.py deploy --name myapp --image myapp:v2 --strategy blue-green

# Canary deployment with custom steps
python scripts/deployment_manager.py deploy --name myapp --image myapp:v2 --strategy canary --canary-steps 10,25,50,100
```

---

## Workflows

### 1. Setup CI/CD Pipeline

**Goal:** Generate a complete CI/CD pipeline for your project

**Steps:**

1. **Detect tech stack**
   ```bash
   python scripts/pipeline_generator.py /path/to/project --platform github
   ```
   The tool automatically detects:
   - Node.js (package.json, npm/yarn/pnpm)
   - Python (requirements.txt, pyproject.toml)
   - Go (go.mod)

2. **Review generated workflow**
   ```
   .github/workflows/ci.yml generated with:
   - lint job (ESLint/Prettier/Black/golint)
   - test job (Jest/pytest/go test)
   - build job (Docker image)
   - deploy job (if --with-deploy)
   ```

3. **Add secrets to repository**
   - `DOCKER_USERNAME` / `DOCKER_PASSWORD` (if using Docker Hub)
   - `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` (if deploying to AWS)

4. **Commit and push**
   ```bash
   git add .github/workflows/ci.yml
   git commit -m "feat: add CI/CD pipeline"
   git push
   ```

**Output:** Working CI/CD pipeline triggered on push/PR

---

### 2. Scaffold Infrastructure

**Goal:** Generate production-ready Terraform modules

**Steps:**

1. **Generate base infrastructure**
   ```bash
   python scripts/terraform_scaffolder.py ./terraform --project myapp --modules vpc,ecs,rds
   ```

2. **Review generated structure**
   ```
   terraform/
   ├── main.tf              # Provider config + module calls
   ├── variables.tf         # Input variables
   ├── outputs.tf           # Output values
   ├── versions.tf          # Provider constraints
   ├── backend.tf           # S3 state config (commented)
   ├── modules/
   │   ├── vpc/             # VPC with public/private subnets
   │   ├── ecs/             # ECS Fargate with ALB
   │   └── rds/             # PostgreSQL with Secrets Manager
   └── environments/
       ├── dev/terraform.tfvars
       ├── staging/terraform.tfvars
       └── prod/terraform.tfvars
   ```

3. **Initialize and plan**
   ```bash
   cd terraform
   terraform init
   terraform plan -var-file=environments/dev/terraform.tfvars
   ```

4. **Apply infrastructure**
   ```bash
   terraform apply -var-file=environments/dev/terraform.tfvars
   ```

**Output:** Complete Terraform project with VPC, ECS, RDS modules

---

### 3. Deploy Application

**Goal:** Deploy application with chosen strategy

**Steps:**

1. **Preview deployment (dry run)**
   ```bash
   python scripts/deployment_manager.py deploy \
     --name myapp \
     --image myapp:v2 \
     --strategy rolling \
     --dry-run
   ```

2. **Execute deployment**
   ```bash
   python scripts/deployment_manager.py deploy \
     --name myapp \
     --image myapp:v2 \
     --strategy rolling \
     --namespace production
   ```

3. **Monitor status**
   ```bash
   python scripts/deployment_manager.py status --name myapp --namespace production
   ```

4. **Rollback if needed**
   ```bash
   python scripts/deployment_manager.py rollback --name myapp --namespace production
   ```

**Output:** Application deployed with automatic health checks

---

### 4. Blue-Green Deployment

**Goal:** Zero-downtime deployment with instant rollback

**Steps:**

1. **Deploy to green environment**
   ```bash
   python scripts/deployment_manager.py deploy \
     --name myapp \
     --image myapp:v2 \
     --strategy blue-green \
     --namespace production
   ```

2. **Automatic steps performed:**
   - Deploy new version to green
   - Run health checks on green
   - Switch traffic from blue to green
   - Keep blue running for rollback

3. **Verify deployment**
   ```bash
   python scripts/deployment_manager.py status --name myapp-green
   ```

4. **Rollback (if needed)**
   - Traffic switches back to blue instantly
   - No downtime during rollback

**Output:** Zero-downtime deployment with blue as standby

---

## Tool Reference

### pipeline_generator.py

Generate CI/CD pipeline configurations for GitHub Actions or GitLab CI.

| Option | Description | Default |
|--------|-------------|---------|
| `project_path` | Path to project directory | Required |
| `--platform` | Target platform (github, gitlab) | github |
| `--with-docker` | Include Docker build step | false |
| `--with-deploy` | Include deployment step | false |
| `--env` | Deployment environment | staging |
| `--verbose` | Verbose output | false |
| `--json` | Output as JSON | false |

**Tech Stack Detection:**
- Node.js: package.json, package-lock.json, yarn.lock, pnpm-lock.yaml
- Python: requirements.txt, pyproject.toml, setup.py
- Go: go.mod

### terraform_scaffolder.py

Generate production-ready Terraform module templates.

| Option | Description | Default |
|--------|-------------|---------|
| `output_path` | Directory for Terraform files | Required |
| `--project` | Project name | myproject |
| `--modules` | Modules to generate (vpc,ecs,rds) | vpc,ecs,rds |
| `--environments` | Environment list | dev,staging,prod |
| `--region` | AWS region | us-east-1 |
| `--verbose` | Verbose output | false |
| `--json` | Output as JSON | false |

**Generated Modules:**
- VPC: Public/private subnets, NAT gateways, route tables
- ECS: Fargate cluster, ALB, task definitions, IAM roles
- RDS: PostgreSQL, Secrets Manager, security groups

### deployment_manager.py

Orchestrate deployments with blue-green, canary, and rolling strategies.

| Command | Description |
|---------|-------------|
| `deploy` | Execute deployment with selected strategy |
| `status` | Get current deployment status |
| `rollback` | Rollback to previous version |
| `manifest` | Generate Kubernetes manifest |

| Deploy Option | Description | Default |
|---------------|-------------|---------|
| `--name` | Deployment name | Required |
| `--image` | Container image | Required |
| `--strategy` | rolling, blue-green, canary | rolling |
| `--namespace` | Kubernetes namespace | default |
| `--replicas` | Number of replicas | 3 |
| `--canary-steps` | Traffic percentages | 10,25,50,100 |
| `--platform` | kubernetes, ecs | kubernetes |
| `--dry-run` | Preview without executing | false |

---

## Reference Documentation

| Document | Topics Covered |
|----------|----------------|
| [`cicd_pipeline_guide.md`](references/cicd_pipeline_guide.md) | GitHub Actions workflows, GitLab CI configs, matrix builds, security scanning |
| [`infrastructure_as_code.md`](references/infrastructure_as_code.md) | Terraform modules, VPC/ECS/RDS patterns, state management, security |
| [`deployment_strategies.md`](references/deployment_strategies.md) | Blue-green, canary, rolling deployments, rollback procedures |

---

## Platform Patterns

### GitHub Actions

```yaml
# Standard CI workflow structure
name: CI
on: [push, pull_request]
jobs:
  lint:    # Code quality checks
  test:    # Unit/integration tests
  build:   # Docker image build
  deploy:  # Environment deployment
```

### GitLab CI

```yaml
# Standard pipeline structure
stages:
  - lint
  - test
  - build
  - deploy

# Job inheritance with YAML anchors
.node-cache: &node-cache
  cache:
    key: ${CI_COMMIT_REF_SLUG}
    paths: [node_modules/]
```

### Kubernetes Deployments

```yaml
# Rolling update strategy
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```

### AWS ECS

```bash
# Force new deployment
aws ecs update-service \
  --cluster production \
  --service myapp \
  --force-new-deployment

# Wait for stability
aws ecs wait services-stable \
  --cluster production \
  --services myapp
```

---

## Validation Checklist

### CI/CD Pipeline

- [ ] Pipeline triggers on correct branches (main, develop, PRs)
- [ ] Lint stage fails on code quality issues
- [ ] Tests run with proper environment (database services)
- [ ] Docker image tagged with commit SHA
- [ ] Secrets configured in repository settings
- [ ] Deploy stage has environment protection rules

### Infrastructure

- [ ] Terraform validates without errors
- [ ] State backend configured (S3 + DynamoDB)
- [ ] All resources tagged with Project/Environment
- [ ] Security groups follow least privilege
- [ ] RDS encryption enabled
- [ ] Multi-AZ configured for production

### Deployment

- [ ] Health checks configured and passing
- [ ] Rollback procedure tested
- [ ] Monitoring/alerting in place
- [ ] Load balancer health checks passing
- [ ] Zero downtime during deployment
- [ ] Canary metrics collection working

---

## Tech Stack

**CI/CD Platforms:** GitHub Actions, GitLab CI, Jenkins
**Container Orchestration:** Kubernetes, AWS ECS, Docker Compose
**Infrastructure as Code:** Terraform, CloudFormation, Pulumi
**Cloud Providers:** AWS, GCP, Azure
**Container Registry:** ECR, GCR, Docker Hub, GHCR
**Monitoring:** Prometheus, Grafana, CloudWatch, Datadog
