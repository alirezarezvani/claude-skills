---
name: ms365-tenant-manager
description: Microsoft 365 tenant administration for Global Administrators. Automate M365 tenant setup, Office 365 admin tasks, Azure AD user management, Exchange Online configuration, Teams administration, and security policies. Generate PowerShell scripts for bulk operations, Conditional Access policies, license management, and compliance reporting. Use for M365 tenant manager, Office 365 admin, Azure AD users, Global Administrator, tenant configuration, or Microsoft 365 automation.
---

# Microsoft 365 Tenant Manager

Expert guidance and automation for Microsoft 365 Global Administrators managing tenant setup, user lifecycle, security policies, and organizational optimization.

---

## Table of Contents

- [Trigger Phrases](#trigger-phrases)
- [Quick Start](#quick-start)
- [Tools](#tools)
- [Workflows](#workflows)
- [Best Practices](#best-practices)
- [Reference Guides](#reference-guides)
- [Limitations](#limitations)

---

## Trigger Phrases

Use this skill when you hear:
- "set up Microsoft 365 tenant"
- "create Office 365 users"
- "configure Azure AD"
- "generate PowerShell script for M365"
- "set up Conditional Access"
- "bulk user provisioning"
- "M365 security audit"
- "license management"
- "Exchange Online configuration"
- "Teams administration"

---

## Quick Start

### Generate Security Audit Script

```bash
python scripts/powershell_generator.py --action audit --output audit_script.ps1
```

### Create Bulk User Provisioning Script

```bash
python scripts/user_management.py --action provision --csv users.csv --license E3
```

### Configure Conditional Access Policy

```bash
python scripts/powershell_generator.py --action conditional-access --require-mfa --include-admins
```

---

## Tools

### powershell_generator.py

Generates ready-to-use PowerShell scripts for Microsoft 365 administration.

**Usage:**

```bash
# Generate security audit script
python scripts/powershell_generator.py --action audit

# Generate Conditional Access policy script
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA for Admins" \
  --require-mfa \
  --include-users "All"

# Generate bulk license assignment script
python scripts/powershell_generator.py --action license \
  --csv users.csv \
  --sku "ENTERPRISEPACK"
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--action` | Yes | Script type: `audit`, `conditional-access`, `license`, `users` |
| `--policy-name` | No | Name for Conditional Access policy |
| `--require-mfa` | No | Require MFA in policy |
| `--include-users` | No | Users to include: `All` or specific UPNs |
| `--csv` | No | CSV file path for bulk operations |
| `--sku` | No | License SKU for assignment |
| `--output` | No | Output file path (default: stdout) |

**Output:** Complete PowerShell scripts with error handling, logging, and best practices.

### user_management.py

Automates user lifecycle operations and bulk provisioning.

**Usage:**

```bash
# Provision users from CSV
python scripts/user_management.py --action provision --csv new_users.csv

# Offboard user securely
python scripts/user_management.py --action offboard --user john.doe@company.com

# Generate inactive users report
python scripts/user_management.py --action report-inactive --days 90
```

**Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `--action` | Yes | Operation: `provision`, `offboard`, `report-inactive`, `sync` |
| `--csv` | No | CSV file for bulk operations |
| `--user` | No | Single user UPN |
| `--days` | No | Days for inactivity threshold (default: 90) |
| `--license` | No | License SKU to assign |

### tenant_setup.py

Initial tenant configuration and service provisioning automation.

**Usage:**

```bash
# Generate tenant setup checklist
python scripts/tenant_setup.py --action checklist --company "Acme Inc" --users 50

# Generate DNS records configuration
python scripts/tenant_setup.py --action dns --domain acme.com

# Generate security baseline script
python scripts/tenant_setup.py --action security-baseline
```

---

## Workflows

### Workflow 1: New Tenant Setup

**Step 1: Generate Setup Checklist**

```bash
python scripts/tenant_setup.py --action checklist --company "Company Name" --users 100
```

**Step 2: Configure DNS Records**

```bash
python scripts/tenant_setup.py --action dns --domain company.com
```

**Step 3: Apply Security Baseline**

```bash
python scripts/powershell_generator.py --action audit > initial_audit.ps1
```

**Step 4: Provision Users**

```bash
python scripts/user_management.py --action provision --csv employees.csv --license E3
```

### Workflow 2: Security Hardening

**Step 1: Run Security Audit**

```bash
python scripts/powershell_generator.py --action audit --output security_audit.ps1
```

**Step 2: Create MFA Policy**

```bash
python scripts/powershell_generator.py --action conditional-access \
  --policy-name "Require MFA All Users" \
  --require-mfa \
  --include-users "All"
```

**Step 3: Review Results**

Execute generated scripts and review CSV reports in output directory.

### Workflow 3: User Offboarding

**Step 1: Generate Offboarding Script**

```bash
python scripts/user_management.py --action offboard --user departing.user@company.com
```

**Step 2: Execute Script with -WhatIf**

```powershell
.\offboard_user.ps1 -WhatIf
```

**Step 3: Execute for Real**

```powershell
.\offboard_user.ps1 -Confirm:$false
```

---

## Best Practices

### Tenant Setup

1. Enable MFA before adding users
2. Configure named locations for Conditional Access
3. Use separate admin accounts with PIM
4. Verify custom domains before bulk user creation
5. Apply Microsoft Secure Score recommendations

### Security Operations

1. Start Conditional Access policies in report-only mode
2. Use `-WhatIf` parameter before executing scripts
3. Never hardcode credentials in scripts
4. Enable audit logging for all operations
5. Regular quarterly security reviews

### PowerShell Automation

1. Prefer Microsoft Graph over legacy MSOnline modules
2. Include try/catch blocks for error handling
3. Implement logging for audit trails
4. Use Azure Key Vault for credential management
5. Test in non-production tenant first

---

## Reference Guides

### When to Use Each Reference

**references/powershell-templates.md**

- Ready-to-use script templates
- Conditional Access policy examples
- Bulk user provisioning scripts
- Security audit scripts

**references/security-policies.md**

- Conditional Access configuration
- MFA enforcement strategies
- DLP and retention policies
- Security baseline settings

**references/troubleshooting.md**

- Common error resolutions
- PowerShell module issues
- Permission troubleshooting
- DNS propagation problems

---

## Limitations

| Constraint | Impact |
|------------|--------|
| Global Admin required | Full tenant setup needs highest privilege |
| API rate limits | Bulk operations may be throttled |
| License dependencies | E3/E5 required for advanced features |
| Hybrid scenarios | On-premises AD needs additional configuration |
| PowerShell prerequisites | Microsoft.Graph module required |

### Required PowerShell Modules

```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
```

### Required Permissions

- **Global Administrator** - Full tenant setup
- **User Administrator** - User management
- **Security Administrator** - Security policies
- **Exchange Administrator** - Mailbox management
