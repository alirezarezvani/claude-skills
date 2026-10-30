---
name: "terraform-patterns"
description: "Use for any Terraform module, state backend, provider setup or IaC security review, before editing .tf files. Analyzes modules with tf_module_analyzer.py and scans for misconfigurations with tf_security_scanner.py."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-15
---

# Terraform Patterns

> Predictable infrastructure. Secure state. Modules that compose. No drift.

Opinionated Terraform workflow that turns sprawling HCL into well-structured, secure, production-grade infrastructure code. Covers module design, state management, provider patterns, security hardening, and CI/CD integration.

Not a Terraform tutorial — a set of concrete decisions about how to write infrastructure code that doesn't break at 3 AM.

---

## Slash Commands

| Command | What it does |
|---------|-------------|
| `/terraform:review` | Analyze Terraform code for anti-patterns, security issues, and structure problems |
| `/terraform:module` | Design or refactor a Terraform module with proper inputs, outputs, and composition |
| `/terraform:security` | Audit Terraform code for security vulnerabilities, secrets exposure, and IAM misconfigurations |

---

## When This Skill Activates

Recognize these patterns from the user:

- "Review this Terraform code"
- "Design a Terraform module for..."
- "My Terraform state is..."
- "Set up remote state backend"
- "Multi-region Terraform deployment"
- "Terraform security review"
- "Module structure best practices"
- "Terraform CI/CD pipeline"
- Any request involving: `.tf` files, HCL, Terraform modules, state management, provider configuration, infrastructure-as-code

If the user has `.tf` files or wants to provision infrastructure with Terraform → this skill applies.

---

## Workflow

### `/terraform:review` — Terraform Code Review

1. **Analyze current state**
   - Read all `.tf` files in the target directory
   - Identify module structure (flat vs nested)
   - Count resources, data sources, variables, outputs
   - Check naming conventions

2. **Apply review checklist**

   ```
   MODULE STRUCTURE
   ├── Variables have descriptions and type constraints
   ├── Outputs expose only what consumers need
   ├── Resources use consistent naming: {provider}_{type}_{purpose}
   ├── Locals used for computed values and DRY expressions
   └── No hardcoded values — everything parameterized or in locals

   STATE & BACKEND
   ├── Remote backend configured (S3, GCS, Azure Blob, Terraform Cloud)
   ├── State locking enabled (DynamoDB for S3, native for others)
   ├── State encryption at rest enabled
   ├── No secrets stored in state (or state access is restricted)
   └── Workspaces or directory isolation for environments

   PROVIDERS
   ├── Version constraints use pessimistic operator: ~> 5.0
   ├── Required providers block in terraform {} block
   ├── Provider aliases for multi-region or multi-account
   └── No provider configuration in child modules

   SECURITY
   ├── No hardcoded secrets, keys, or passwords
   ├── IAM follows least-privilege principle
   ├── Encryption enabled for storage, databases, secrets
   ├── Security groups are not overly permissive (no 0.0.0.0/0 ingress on sensitive ports)
   └── Sensitive variables marked with sensitive = true
   ```

3. **Generate report**
   ```bash
   python3 scripts/tf_module_analyzer.py ./terraform
   ```

4. **Run security scan**
   ```bash
   python3 scripts/tf_security_scanner.py ./terraform
   ```

### `/terraform:module` — Module Design

1. **Identify module scope**
   - Single responsibility: one module = one logical grouping
   - Determine inputs (variables), outputs, and resource boundaries
   - Decide: flat module (single directory) vs nested (calling child modules)

2. **Apply module design checklist**

   ```
   STRUCTURE
   ├── main.tf        — Primary resources
   ├── variables.tf   — All input variables with descriptions and types
   ├── outputs.tf     — All outputs with descriptions
   ├── versions.tf    — terraform {} block with required_providers
   ├── locals.tf      — Computed values and naming conventions
   ├── data.tf        — Data sources (if any)
   └── README.md      — Usage examples and variable documentation

   VARIABLES
   ├── Every variable has: description, type, validation (where applicable)
   ├── Sensitive values marked: sensitive = true
   ├── Defaults provided for optional settings
   ├── Use object types for related settings: variable "config" { type = object({...}) }
   └── Validate with: validation { condition = ... }

   OUTPUTS
   ├── Output IDs, ARNs, endpoints — things consumers need
   ├── Include description on every output
   ├── Mark sensitive outputs: sensitive = true
   └── Don't output entire resources — only specific attributes

   COMPOSITION
   ├── Root module calls child modules
   ├── Child modules never call other child modules
   ├── Pass values explicitly — no hidden data source lookups in child modules
   ├── Provider configuration only in root module
   └── Use module "name" { source = "./modules/name" }
   ```

3. **Generate module scaffold**
   - Output file structure with boilerplate
   - Include variable validation blocks
   - Add lifecycle rules where appropriate

### `/terraform:security` — Security Audit

1. **Code-level audit**

   | Check | Severity | Fix |
   |-------|----------|-----|
   | Hardcoded secrets in `.tf` files | Critical | Use variables with sensitive = true or vault |
   | IAM policy with `*` actions | Critical | Scope to specific actions and resources |
   | Security group with 0.0.0.0/0 on port 22/3389 | Critical | Restrict to known CIDR blocks or use SSM/bastion |
   | S3 bucket without encryption | High | Add `server_side_encryption_configuration` block |
   | S3 bucket with public access | High | Add `aws_s3_bucket_public_access_block` |
   | RDS without encryption | High | Set `storage_encrypted = true` |
   | RDS publicly accessible | High | Set `publicly_accessible = false` |
   | CloudTrail not enabled | Medium | Add `aws_cloudtrail` resource |
   | Missing `prevent_destroy` on stateful resources | Medium | Add `lifecycle { prevent_destroy = true }` |
   | Variables without `sensitive = true` for secrets | Medium | Add `sensitive = true` to secret variables |

2. **State security audit**

   | Check | Severity | Fix |
   |-------|----------|-----|
   | Local state file | Critical | Migrate to remote backend with encryption |
   | Remote state without encryption | High | Enable encryption on backend (SSE-S3, KMS) |
   | No state locking | High | Enable DynamoDB for S3, native for TF Cloud |
   | State accessible to all team members | Medium | Restrict via IAM policies or TF Cloud teams |

3. **Generate security report**
   ```bash
   python3 scripts/tf_security_scanner.py ./terraform
   python3 scripts/tf_security_scanner.py ./terraform --output json
   ```

---

## Tooling

### `scripts/tf_module_analyzer.py`

CLI utility for analyzing Terraform directory structure and module quality.

**Features:**
- Resource and data source counting
- Variable and output analysis (missing descriptions, types, validation)
- Naming convention checks
- Module composition detection
- File structure validation
- JSON and text output

**Usage:**
```bash
# Analyze a Terraform directory
python3 scripts/tf_module_analyzer.py ./terraform

# JSON output
python3 scripts/tf_module_analyzer.py ./terraform --output json

# Analyze a specific module
python3 scripts/tf_module_analyzer.py ./modules/vpc
```

### `scripts/tf_security_scanner.py`

CLI utility for scanning `.tf` files for common security issues.

**Features:**
- Hardcoded secret detection (AWS keys, passwords, tokens)
- Overly permissive IAM policy detection
- Open security group detection (0.0.0.0/0 on sensitive ports)
- Missing encryption checks (S3, RDS, EBS)
- Public access detection (S3, RDS, EC2)
- Sensitive variable audit
- JSON and text output

**Usage:**
```bash
# Scan a Terraform directory
python3 scripts/tf_security_scanner.py ./terraform

# JSON output
python3 scripts/tf_security_scanner.py ./terraform --output json

# Strict mode (elevate warnings)
python3 scripts/tf_security_scanner.py ./terraform --strict
```

---

## Patterns catalog

Module layouts (flat, nested, Terragrunt mono-repo), provider pinning and aliasing, the state-management decision tree, CI/CD plan/apply and drift detection, multi-cloud, OpenTofu migration, Infracost cost gates, `terraform import` and Terragrunt live in [references/patterns-catalog.md](references/patterns-catalog.md). Load the section the task needs.

---

## Proactive Triggers

Flag these without being asked:

- **No remote backend configured** → Migrate to S3/GCS/Azure Blob with locking and encryption.
- **Provider without version constraint** → Add `version = "~> X.0"` to prevent breaking upgrades.
- **Hardcoded secrets in .tf files** → Use variables with `sensitive = true`, or integrate Vault/SSM.
- **IAM policy with `"Action": "*"`** → Scope to specific actions. No wildcard actions in production.
- **Security group open to 0.0.0.0/0 on SSH/RDP** → Restrict to bastion CIDR or use SSM Session Manager.
- **No state locking** → Enable DynamoDB table for S3 backend, or use TF Cloud.
- **Resources without tags** → Add default_tags in provider block. Tags are mandatory for cost tracking.
- **Missing `prevent_destroy` on databases/storage** → Add lifecycle block to prevent accidental deletion.

---

## Installation

### One-liner (any tool)
```bash
git clone https://github.com/alirezarezvani/claude-skills.git
cp -r claude-skills/engineering/terraform-patterns ~/.claude/skills/
```

### Multi-tool install
```bash
./scripts/convert.sh --skill terraform-patterns --tool codex|gemini|cursor|windsurf|openclaw
```

### OpenClaw
```bash
clawhub install terraform-patterns
```

---

## Related Skills

- **senior-devops** — Broader DevOps scope (CI/CD, monitoring, containerization). Complementary — use terraform-patterns for IaC-specific work, senior-devops for pipeline and infrastructure operations.
- **aws-solution-architect** — AWS architecture design. Complementary — terraform-patterns implements the infrastructure, aws-solution-architect designs it.
- **senior-security** — Application security. Complementary — terraform-patterns covers infrastructure security posture, senior-security covers application-level threats.
- **ci-cd-pipeline-builder** — Pipeline construction. Complementary — terraform-patterns defines infrastructure, ci-cd-pipeline-builder automates deployment.

## More in this skill

Load these only when the task needs them.

- [references/module-patterns.md](references/module-patterns.md) — Terraform Module Design Patterns Reference
- [references/state-management.md](references/state-management.md) — Terraform State Management Reference
