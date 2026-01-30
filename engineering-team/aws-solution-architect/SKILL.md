---
name: aws-solution-architect
description: Design AWS architectures for startups using serverless patterns and IaC templates. Use when asked to design serverless architecture, create CloudFormation templates, optimize AWS costs, set up CI/CD pipelines, or migrate to AWS. Covers Lambda, API Gateway, DynamoDB, ECS, Aurora, and cost optimization.
---

# AWS Solution Architect

Design scalable, cost-effective AWS architectures for startups with infrastructure-as-code templates.

---

## Table of Contents

- [Trigger Terms](#trigger-terms)
- [Workflow](#workflow)
- [Tools](#tools)
- [Quick Start](#quick-start)
- [Input Requirements](#input-requirements)
- [Output Formats](#output-formats)

---

## Trigger Terms

Use this skill when you encounter:

| Category | Terms |
|----------|-------|
| **Architecture Design** | serverless architecture, AWS architecture, cloud design, microservices, three-tier |
| **IaC Generation** | CloudFormation, CDK, Terraform, infrastructure as code, deploy template |
| **Serverless** | Lambda, API Gateway, DynamoDB, Step Functions, EventBridge, AppSync |
| **Containers** | ECS, Fargate, EKS, container orchestration, Docker on AWS |
| **Cost Optimization** | reduce AWS costs, optimize spending, right-sizing, Savings Plans |
| **Database** | Aurora, RDS, DynamoDB design, database migration, data modeling |
| **Security** | IAM policies, VPC design, encryption, Cognito, WAF |
| **CI/CD** | CodePipeline, CodeBuild, CodeDeploy, GitHub Actions AWS |
| **Monitoring** | CloudWatch, X-Ray, observability, alarms, dashboards |
| **Migration** | migrate to AWS, lift and shift, replatform, DMS |

---

## Workflow

### Step 1: Gather Requirements

Collect application specifications:

```
- Application type (web app, mobile backend, data pipeline, SaaS)
- Expected users and requests per second
- Budget constraints (monthly spend limit)
- Team size and AWS experience level
- Compliance requirements (GDPR, HIPAA, SOC 2)
- Availability requirements (SLA, RPO/RTO)
```

### Step 2: Design Architecture

Run the architecture designer to get pattern recommendations:

```bash
python scripts/architecture_designer.py --input requirements.json
```

Select from recommended patterns:
- **Serverless Web**: S3 + CloudFront + API Gateway + Lambda + DynamoDB
- **Event-Driven Microservices**: EventBridge + Lambda + SQS + Step Functions
- **Three-Tier**: ALB + ECS Fargate + Aurora + ElastiCache
- **GraphQL Backend**: AppSync + Lambda + DynamoDB + Cognito

See `references/architecture_patterns.md` for detailed pattern specifications.

### Step 3: Generate IaC Templates

Create infrastructure-as-code for the selected pattern:

```bash
# Serverless stack (CloudFormation)
python scripts/serverless_stack.py --app-name my-app --region us-east-1

# Output: CloudFormation YAML template ready to deploy
```

### Step 4: Review Costs

Analyze estimated costs and optimization opportunities:

```bash
python scripts/cost_optimizer.py --resources current_setup.json --monthly-spend 2000
```

Output includes:
- Monthly cost breakdown by service
- Right-sizing recommendations
- Savings Plans opportunities
- Potential monthly savings

### Step 5: Deploy

Deploy the generated infrastructure:

```bash
# CloudFormation
aws cloudformation create-stack \
  --stack-name my-app-stack \
  --template-body file://template.yaml \
  --capabilities CAPABILITY_IAM

# CDK
cdk deploy

# Terraform
terraform init && terraform apply
```

### Step 6: Validate

Verify deployment and set up monitoring:

```bash
# Check stack status
aws cloudformation describe-stacks --stack-name my-app-stack

# Set up CloudWatch alarms
aws cloudwatch put-metric-alarm --alarm-name high-errors ...
```

---

## Tools

### architecture_designer.py

Generates architecture patterns based on requirements.

```bash
python scripts/architecture_designer.py --input requirements.json --output design.json
```

**Input:** JSON with app type, scale, budget, compliance needs
**Output:** Recommended pattern, service stack, cost estimate, pros/cons

### serverless_stack.py

Creates serverless CloudFormation templates.

```bash
python scripts/serverless_stack.py --app-name my-app --region us-east-1
```

**Output:** Production-ready CloudFormation YAML with:
- API Gateway + Lambda
- DynamoDB table
- Cognito user pool
- IAM roles with least privilege
- CloudWatch logging

### cost_optimizer.py

Analyzes costs and recommends optimizations.

```bash
python scripts/cost_optimizer.py --resources inventory.json --monthly-spend 5000
```

**Output:** Recommendations for:
- Idle resource removal
- Instance right-sizing
- Reserved capacity purchases
- Storage tier transitions
- NAT Gateway alternatives

---

## Quick Start

### MVP Architecture (< $100/month)

```
Ask: "Design a serverless MVP backend for a mobile app with 1000 users"

Result:
- Lambda + API Gateway for API
- DynamoDB pay-per-request for data
- Cognito for authentication
- S3 + CloudFront for static assets
- Estimated: $20-50/month
```

### Scaling Architecture ($500-2000/month)

```
Ask: "Design a scalable architecture for a SaaS platform with 50k users"

Result:
- ECS Fargate for containerized API
- Aurora Serverless for relational data
- ElastiCache for session caching
- CloudFront for CDN
- CodePipeline for CI/CD
- Multi-AZ deployment
```

### Cost Optimization

```
Ask: "Optimize my AWS setup to reduce costs by 30%. Current spend: $3000/month"

Provide: Current resource inventory (EC2, RDS, S3, etc.)

Result:
- Idle resource identification
- Right-sizing recommendations
- Savings Plans analysis
- Storage lifecycle policies
- Target savings: $900/month
```

### IaC Generation

```
Ask: "Generate CloudFormation for a three-tier web app with auto-scaling"

Result:
- VPC with public/private subnets
- ALB with HTTPS
- ECS Fargate with auto-scaling
- Aurora with read replicas
- Security groups and IAM roles
```

---

## Input Requirements

Provide these details for architecture design:

| Requirement | Description | Example |
|-------------|-------------|---------|
| Application type | What you're building | SaaS platform, mobile backend |
| Expected scale | Users, requests/sec | 10k users, 100 RPS |
| Budget | Monthly AWS limit | $500/month max |
| Team context | Size, AWS experience | 3 devs, intermediate |
| Compliance | Regulatory needs | HIPAA, GDPR, SOC 2 |
| Availability | Uptime requirements | 99.9% SLA, 1hr RPO |

**JSON Format:**

```json
{
  "application_type": "saas_platform",
  "expected_users": 10000,
  "requests_per_second": 100,
  "budget_monthly_usd": 500,
  "team_size": 3,
  "aws_experience": "intermediate",
  "compliance": ["SOC2"],
  "availability_sla": "99.9%"
}
```

---

## Output Formats

### Architecture Design

- Pattern recommendation with rationale
- Service stack diagram (ASCII)
- Configuration specifications
- Monthly cost estimate
- Scaling characteristics
- Trade-offs and limitations

### IaC Templates

- **CloudFormation YAML**: Production-ready SAM/CFN templates
- **CDK TypeScript**: Type-safe infrastructure code
- **Terraform HCL**: Multi-cloud compatible configs

### Cost Analysis

- Current spend breakdown
- Optimization recommendations with savings
- Priority action list (high/medium/low)
- Implementation checklist

---

## Reference Documentation

| Document | Contents |
|----------|----------|
| `references/architecture_patterns.md` | 6 patterns: serverless, microservices, three-tier, data processing, GraphQL, multi-region |
| `references/service_selection.md` | Decision matrices for compute, database, storage, messaging |
| `references/best_practices.md` | Serverless design, cost optimization, security hardening, scalability |

---

## Limitations

- Lambda: 15-minute execution, 10GB memory max
- API Gateway: 29-second timeout, 10MB payload
- DynamoDB: 400KB item size, eventually consistent by default
- Regional availability varies by service
- Some services have AWS-specific lock-in
