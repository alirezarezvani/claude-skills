# Terraform patterns: modules, providers, state, CI/CD, multi-cloud, OpenTofu, Infracost, import, Terragrunt

Moved out of SKILL.md so the skill body stays short. Load the section the task needs.

## Module Design Patterns

### Pattern 1: Flat Module (Small/Medium Projects)

```
infrastructure/
├── main.tf          # All resources
├── variables.tf     # All inputs
├── outputs.tf       # All outputs
├── versions.tf      # Provider requirements
├── terraform.tfvars # Environment values (not committed)
└── backend.tf       # Remote state configuration
```

Best for: Single application, < 20 resources, one team owns everything.

### Pattern 2: Nested Modules (Medium/Large Projects)

```
infrastructure/
├── environments/
│   ├── dev/
│   │   ├── main.tf          # Calls modules with dev params
│   │   ├── backend.tf       # Dev state backend
│   │   └── terraform.tfvars
│   ├── staging/
│   │   └── ...
│   └── prod/
│       └── ...
├── modules/
│   ├── networking/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── compute/
│   │   └── ...
│   └── database/
│       └── ...
└── versions.tf
```

Best for: Multiple environments, shared infrastructure patterns, team collaboration.

### Pattern 3: Mono-Repo with Terragrunt

```
infrastructure/
├── terragrunt.hcl           # Root config
├── modules/                  # Reusable modules
│   ├── vpc/
│   ├── eks/
│   └── rds/
├── dev/
│   ├── terragrunt.hcl       # Dev overrides
│   ├── vpc/
│   │   └── terragrunt.hcl   # Module invocation
│   └── eks/
│       └── terragrunt.hcl
└── prod/
    ├── terragrunt.hcl
    └── ...
```

Best for: Large-scale, many environments, DRY configuration, team-level isolation.

---

## Provider Configuration Patterns

### Version Pinning
```hcl
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"    # Allow 5.x, block 6.0
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.5"
    }
  }
}
```

### Multi-Region with Aliases
```hcl
provider "aws" {
  region = "us-east-1"
}

provider "aws" {
  alias  = "west"
  region = "us-west-2"
}

resource "aws_s3_bucket" "primary" {
  bucket = "my-app-primary"
}

resource "aws_s3_bucket" "replica" {
  provider = aws.west
  bucket   = "my-app-replica"
}
```

### Multi-Account with Assume Role
```hcl
provider "aws" {
  alias  = "production"
  region = "us-east-1"

  assume_role {
    role_arn = "arn:aws:iam::PROD_ACCOUNT_ID:role/TerraformRole"
  }
}
```

---

## State Management Decision Tree

```
Single developer, small project?
├── Yes → Local state (but migrate to remote ASAP)
└── No
    ├── Using Terraform Cloud/Enterprise?
    │   └── Yes → TF Cloud native backend (built-in locking, encryption, RBAC)
    └── No
        ├── AWS?
        │   └── S3 + DynamoDB (encryption, locking, versioning)
        ├── GCP?
        │   └── GCS bucket (native locking, encryption)
        ├── Azure?
        │   └── Azure Blob Storage (native locking, encryption)
        └── Other?
            └── Consul or PostgreSQL backend

Environment isolation strategy:
├── Separate state files per environment (recommended)
│   ├── Option A: Separate directories (dev/, staging/, prod/)
│   └── Option B: Terraform workspaces (simpler but less isolation)
└── Single state file for all environments (never do this)
```

---

## CI/CD Integration Patterns

### GitHub Actions Plan/Apply

```yaml
# .github/workflows/terraform.yml
name: Terraform
on:
  pull_request:
    paths: ['terraform/**']
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  plan:
    runs-on: ubuntu-latest
    if: github.event_name == 'pull_request'
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform validate
      - run: terraform plan -out=tfplan
      - run: terraform show -json tfplan > plan.json
      # Post plan as PR comment

  apply:
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: terraform apply -auto-approve
```

### Drift Detection

```yaml
# Run on schedule to detect drift
name: Drift Detection
on:
  schedule:
    - cron: '0 6 * * 1-5'  # Weekdays at 6 AM

jobs:
  detect:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform init
      - run: |
          terraform plan -detailed-exitcode -out=drift.tfplan 2>&1 | tee drift.log
          EXIT_CODE=$?
          if [ $EXIT_CODE -eq 2 ]; then
            echo "DRIFT DETECTED — review drift.log"
            # Send alert (Slack, PagerDuty, etc.)
          fi
```

---

## Multi-Cloud Provider Configuration

When a single root module must provision across AWS, Azure, and GCP simultaneously.

### Provider Aliasing Pattern

```hcl
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

provider "azurerm" {
  features {}
  subscription_id = var.azure_subscription_id
}

provider "google" {
  project = var.gcp_project_id
  region  = var.gcp_region
}
```

### Shared Variables Across Providers

```hcl
variable "environment" {
  description = "Environment name used across all providers"
  type        = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Must be dev, staging, or prod."
  }
}

locals {
  common_tags = {
    environment = var.environment
    managed_by  = "terraform"
    project     = var.project_name
  }
}
```

### When to Use Multi-Cloud

- **Yes**: Regulatory requirements mandate data residency across providers, or the org has existing workloads on multiple clouds.
- **No**: "Avoiding vendor lock-in" alone is not sufficient justification. Multi-cloud doubles operational complexity. Prefer single-cloud unless there is a concrete business requirement.

---

## OpenTofu Compatibility

OpenTofu is an open-source fork of Terraform maintained by the Linux Foundation under the MPL 2.0 license.

### Migration from Terraform to OpenTofu

```bash
# 1. Install OpenTofu
brew install opentofu        # macOS
snap install --classic tofu  # Linux

# 2. Replace the binary — state files are compatible
tofu init                    # Re-initializes with OpenTofu
tofu plan                    # Identical plan output
tofu apply                   # Same apply workflow
```

### License Considerations

| | Terraform (1.6+) | OpenTofu |
|---|---|---|
| **License** | BSL 1.1 (source-available) | MPL 2.0 (open-source) |
| **Commercial use** | Restricted for competing products | Unrestricted |
| **Community governance** | HashiCorp | Linux Foundation |

### Feature Parity

OpenTofu tracks Terraform 1.6.x features. Key additions unique to OpenTofu:
- Client-side state encryption (`tofu init -encryption`)
- Early variable/locals evaluation
- Provider-defined functions

### When to Choose OpenTofu

- You need a fully open-source license for your supply chain.
- You want client-side state encryption without Terraform Cloud.
- Otherwise, either tool works — the HCL syntax and provider ecosystem are identical.

---

## Infracost Integration

Infracost estimates cloud costs from Terraform code before resources are provisioned.

### PR Workflow

```bash
# Show cost breakdown for current code
infracost breakdown --path .

# Compare cost difference between current branch and main
infracost diff --path . --compare-to infracost-base.json
```

### GitHub Actions Cost Comment

```yaml
# .github/workflows/infracost.yml
name: Infracost
on: [pull_request]

jobs:
  cost:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: infracost/actions/setup@v3
        with:
          api-key: ${{ secrets.INFRACOST_API_KEY }}
      - run: infracost breakdown --path ./terraform --format json --out-file /tmp/infracost.json
      - run: infracost comment github --path /tmp/infracost.json --repo $GITHUB_REPOSITORY --pull-request ${{ github.event.pull_request.number }} --github-token ${{ secrets.GITHUB_TOKEN }} --behavior update
```

### Budget Thresholds and Cost Policy

```yaml
# infracost.yml — policy file
version: 2.9.0
policies:
  - path: "*"
    max_monthly_cost: "5000"    # Fail PR if estimated cost exceeds $5,000/month
    max_cost_increase: "500"    # Fail PR if cost increase exceeds $500/month
```

---

## Import Existing Infrastructure

Bring manually-created resources under Terraform management.

### terraform import Workflow

```bash
# 1. Write the resource block first (empty body is fine)
# main.tf:
# resource "aws_s3_bucket" "legacy" {}

# 2. Import the resource into state
terraform import aws_s3_bucket.legacy my-existing-bucket-name

# 3. Run plan to see attribute diff
terraform plan

# 4. Fill in the resource block until plan shows no changes
```

### Bulk Import with Config Generation (Terraform 1.5+)

```bash
# Generate HCL for imported resources
terraform plan -generate-config-out=generated.tf

# Review generated.tf, then move resources into proper files
```

### Common Pitfalls

- **Resource drift after import**: The imported resource may have attributes Terraform does not manage. Run `terraform plan` immediately and resolve every diff.
- **State manipulation**: Use `terraform state mv` to rename or reorganize. Use `terraform state rm` to remove without destroying. Always back up state before manipulation: `terraform state pull > backup.tfstate`.
- **Sensitive defaults**: Imported resources may expose secrets in state. Restrict state access and enable encryption.

---

## Terragrunt Patterns

Terragrunt is a thin wrapper around Terraform that provides DRY configuration for multi-environment setups.

### Root terragrunt.hcl (Shared Config)

```hcl
# terragrunt.hcl (root)
remote_state {
  backend = "s3"
  generate = {
    path      = "backend.tf"
    if_exists = "overwrite_terragrunt"
  }
  config = {
    bucket         = "my-org-terraform-state"
    key            = "${path_relative_to_include()}/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-locks"
  }
}
```

### Child terragrunt.hcl (Environment Override)

```hcl
# prod/vpc/terragrunt.hcl
include "root" {
  path = find_in_parent_folders()
}

terraform {
  source = "../../modules/vpc"
}

inputs = {
  environment = "prod"
  cidr_block  = "10.0.0.0/16"
}
```

### Dependencies Between Modules

```hcl
# prod/eks/terragrunt.hcl
dependency "vpc" {
  config_path = "../vpc"
}

inputs = {
  vpc_id     = dependency.vpc.outputs.vpc_id
  subnet_ids = dependency.vpc.outputs.private_subnet_ids
}
```

### When Terragrunt Adds Value

- **Yes**: 3+ environments with identical module structure, shared backend config, or cross-module dependencies.
- **No**: Single environment, small team, or simple directory-based isolation already works. Terragrunt adds a learning curve and another binary to manage.
