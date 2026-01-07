# How to Use This Skill

Hey Claude—I just added the "ms365-tenant-manager" skill. Can you help me set up my Microsoft 365 tenant?

## Example Invocations

**Example 1: Initial Tenant Setup**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you create a complete setup guide for a new Microsoft 365 tenant for a 50-person company with security best practices?
```

**Example 2: User Provisioning**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you generate a PowerShell script to create 20 new users from a CSV file and assign appropriate licenses?
```

**Example 3: Security Audit**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you create a security audit script to check MFA status, admin accounts, and inactive users?
```

**Example 4: Conditional Access Policy**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you help me create a Conditional Access policy requiring MFA for all admin accounts?
```

**Example 5: User Offboarding**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you generate a secure offboarding script for user john.doe@company.com that converts their mailbox and removes access?
```

**Example 6: License Management**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you analyze my current license usage and recommend cost optimizations for 100 users?
```

**Example 7: DNS Configuration**
```
Hey Claude—I just added the "ms365-tenant-manager" skill. Can you provide all the DNS records I need to configure for my custom domain acme.com?
```

## What to Provide

Depending on your task, provide:

### For Tenant Setup:
- Company name and domain
- Number of users
- Industry/compliance requirements (GDPR, HIPAA, etc.)
- Preferred license types

### For User Management:
- User details (name, email, department, role)
- License requirements
- Group memberships needed
- CSV file (for bulk operations)

### For Security Tasks:
- Policy requirements (MFA, Conditional Access)
- User/group scope
- Compliance standards to follow

### For Reporting:
- Report type needed (license usage, security audit, user activity)
- Time period for analysis
- Specific metrics of interest

## What You'll Get

Based on your request, you'll receive:

### Configuration Guides:
- Step-by-step instructions for Admin Center tasks
- Detailed checklists with time estimates
- Screenshots references and navigation paths
- Best practices and security recommendations

### PowerShell Scripts:
- Ready-to-use automation scripts
- Complete error handling and validation
- Logging and audit trail capabilities
- Dry-run modes for safe testing
- Clear comments and documentation

### Reports:
- Security posture assessments
- License utilization analysis
- User activity summaries
- Compliance status reports
- CSV exports for further analysis

### Documentation:
- Configuration change documentation
- Rollback procedures
- Validation checklists
- Troubleshooting guides

## Common Use Cases

### 1. New Tenant Setup
**Ask for:** "Complete tenant setup guide for [company size] with [compliance requirements]"

**You'll get:**
- Phase-by-phase implementation plan
- DNS records configuration
- Security baseline setup
- Service provisioning steps
- PowerShell automation scripts

### 2. Bulk User Provisioning
**Ask for:** "Script to create [number] users with [license type] from CSV"

**You'll get:**
- User creation PowerShell script
- License assignment automation
- Group membership configuration
- Validation and error handling
- Results reporting

### 3. Security Hardening
**Ask for:** "Security audit and hardening recommendations"

**You'll get:**
- Comprehensive security audit script
- MFA status check
- Admin role review
- Conditional Access policy templates
- Remediation recommendations

### 4. License Optimization
**Ask for:** "License cost analysis and optimization for [user count]"

**You'll get:**
- Current license usage breakdown
- Cost optimization recommendations
- Right-sizing suggestions
- Alternative license combinations
- Projected cost savings

### 5. User Lifecycle Management
**Ask for:** "Onboarding/offboarding process for [role/department]"

**You'll get:**
- Automated provisioning scripts
- Secure deprovisioning procedures
- Checklist for manual tasks
- Audit trail documentation

## Prerequisites

To use the generated PowerShell scripts, ensure you have:

### Required PowerShell Modules:
```powershell
Install-Module Microsoft.Graph -Scope CurrentUser
Install-Module ExchangeOnlineManagement -Scope CurrentUser
Install-Module MicrosoftTeams -Scope CurrentUser
Install-Module SharePointPnPPowerShellOnline -Scope CurrentUser
```

### Required Permissions:
- **Global Administrator** (for full tenant setup)
- **User Administrator** (for user management)
- **Security Administrator** (for security policies)
- **Exchange Administrator** (for mailbox management)

### System Requirements:
- PowerShell 7.0 or later (recommended)
- Windows PowerShell 5.1 (minimum)
- Internet connection for Microsoft 365 services

## Safety & Best Practices

### Before Running Scripts:
1. **Test in non-production first** (if available)
2. **Review scripts thoroughly** - understand what they do
3. **Use -WhatIf parameter** when available for dry-runs
4. **Backup critical data** before making changes
5. **Document changes** for audit trail

### Security Considerations:
- Never hardcode credentials in scripts
- Use Azure Key Vault for credential management
- Enable logging for all operations
- Review audit logs regularly
- Follow principle of least privilege

### Compliance:
- Verify scripts meet your compliance requirements
- Document all configuration changes
- Retain audit logs per compliance policies
- Test disaster recovery procedures

## Troubleshooting

### Common Issues:

**"Access Denied" errors:**
- Verify you have appropriate admin role
- Check Conditional Access policies aren't blocking
- Ensure MFA is completed if required

**PowerShell module errors:**
- Update modules to latest version: `Update-Module -Name Microsoft.Graph`
- Clear PowerShell cache if issues persist
- Reconnect to services

**License assignment failures:**
- Verify license availability
- Check user's UsageLocation is set
- Ensure no conflicting licenses

**DNS propagation delays:**
- DNS changes can take 24-48 hours to propagate
- Use `nslookup` to verify record updates
- Test from multiple locations

## Additional Resources

- Microsoft 365 Admin Center: https://admin.microsoft.com
- Azure AD Portal: https://aad.portal.azure.com
- Microsoft Graph Explorer: https://developer.microsoft.com/graph/graph-explorer
- PowerShell Gallery: https://www.powershellgallery.com
- Microsoft 365 Roadmap: https://www.microsoft.com/microsoft-365/roadmap

## Tips for Best Results

1. **Be specific** about your requirements (user count, compliance needs, industry)
2. **Mention constraints** (budget, timeline, technical limitations)
3. **Specify output format** (step-by-step guide vs. PowerShell script)
4. **Ask for explanations** if you need to understand WHY something is configured
5. **Request alternatives** if you need options to choose from
6. **Clarify urgency** so appropriate testing recommendations are included
