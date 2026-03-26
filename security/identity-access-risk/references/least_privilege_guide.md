# Least Privilege Guide — Identity and Access Risk

## Purpose

Provides specific remediation guidance for overprivileged IAM patterns.
Used by the identity-access-risk agent to compose concrete `recommended_action`
and `least_privilege_suggestion` fields in findings.

---

## Principle 1: Replace Service Wildcards with Specific Actions

### BAD — Service wildcard
```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

### GOOD — Specific actions scoped to resource
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:PutObject",
    "s3:DeleteObject"
  ],
  "Resource": "arn:aws:s3:::my-application-bucket/*"
}
```

**Tool**: Use AWS Access Analyzer to identify which S3 actions are actually used
by the role over the last 90 days: `aws accessanalyzer get-generated-policy --job-id <id>`

---

## Principle 2: Scope IAM PassRole to Specific Role ARNs

### BAD — PassRole with wildcard
```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": "*"
}
```

### GOOD — PassRole scoped to specific role
```json
{
  "Effect": "Allow",
  "Action": "iam:PassRole",
  "Resource": "arn:aws:iam::123456789012:role/lambda-execution-role",
  "Condition": {
    "StringEquals": {
      "iam:PassedToService": "lambda.amazonaws.com"
    }
  }
}
```

This prevents PassRole escalation while still allowing the legitimate Lambda deployment use case.

---

## Principle 3: Use Permission Boundaries for Developer Roles

Permission boundaries cap the maximum permissions a role can have, even if directly
attached policies are overprivileged.

```json
{
  "Effect": "Allow",
  "Action": ["iam:CreateRole", "iam:AttachRolePolicy"],
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "iam:PermissionsBoundary": "arn:aws:iam::123456789012:policy/DeveloperBoundary"
    }
  }
}
```

**Use case**: Developers need to create IAM roles for Lambda functions but must not
be able to create roles with admin permissions.

---

## Principle 4: Remove iam:CreateAccessKey from Non-Admin Roles

### Pattern that enables credential harvesting
```json
{
  "Action": ["iam:CreateAccessKey", "iam:ListUsers"],
  "Resource": "*"
}
```

### Corrected — Scope to self only
```json
{
  "Effect": "Allow",
  "Action": "iam:CreateAccessKey",
  "Resource": "arn:aws:iam::*:user/${aws:username}"
}
```

This allows users to manage their own access keys without being able to create
keys for other users.

---

## Principle 5: Use Conditions to Enforce MFA

For sensitive operations, require MFA even if the user is already authenticated.

```json
{
  "Effect": "Deny",
  "Action": [
    "iam:*",
    "s3:DeleteObject",
    "ec2:TerminateInstances"
  ],
  "Resource": "*",
  "Condition": {
    "BoolIfExists": {
      "aws:MultiFactorAuthPresent": "false"
    }
  }
}
```

**Note**: Add this as a Service Control Policy (SCP) at the AWS Organization level
to enforce MFA across all accounts for sensitive actions.

---

## Principle 6: Restrict Cross-Account Access with Conditions

### BAD — Trust any AWS account
```json
{
  "Principal": {"AWS": "*"},
  "Action": "sts:AssumeRole"
}
```

### GOOD — Restrict to org and require MFA/ExternalId
```json
{
  "Principal": {"AWS": "arn:aws:iam::123456789012:root"},
  "Action": "sts:AssumeRole",
  "Condition": {
    "StringEquals": {
      "aws:PrincipalOrgID": "o-xxxxxxxxxx"
    },
    "Bool": {
      "aws:MultiFactorAuthPresent": "true"
    }
  }
}
```

---

## Principle 7: Data Exfiltration Prevention for S3

Prevent bulk data exfiltration even if credentials are compromised.

### VPC Endpoint Policy (limits S3 access to within VPC)
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::sensitive-bucket/*",
  "Condition": {
    "StringNotEquals": {
      "aws:SourceVpc": "vpc-xxxxxxxx"
    }
  }
}
```

### S3 Bucket Policy (block downloads over threshold)
```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::sensitive-bucket/*",
  "Condition": {
    "NumericGreaterThan": {
      "s3:max-keys": "1000"
    }
  }
}
```

---

## AWS IAM Best Practices Checklist

```
Access Keys:
[ ] No long-term access keys for human users (use SSO/Identity Center instead)
[ ] Rotate any existing access keys < 90 days old
[ ] No access keys for root account
[ ] Access keys have no console password (service-only)

MFA:
[ ] MFA required for all IAM users with console access
[ ] MFA required for all sensitive API operations via SCP
[ ] Hardware MFA (FIDO2/YubiKey) for root and admin accounts
[ ] No root account API access keys exist

Policies:
[ ] No inline policies except temporary emergency access
[ ] All custom policies reviewed for wildcards with Access Analyzer
[ ] AWS Managed policies used where appropriate (not Customer Managed with wildcards)
[ ] Permission boundaries on all developer/team roles

Monitoring:
[ ] CloudTrail enabled in all regions with CloudWatch integration
[ ] AWS Config rules for IAM policy changes
[ ] GuardDuty enabled for anomaly detection
[ ] IAM Access Analyzer enabled for external access detection
[ ] Amazon Detective enabled for investigation (if budget allows)

Lifecycle:
[ ] Unused IAM users disabled after 90 days (CloudFormation or Lambda automated)
[ ] Service accounts reviewed quarterly
[ ] Access reviews conducted via IAM Access Analyzer or third-party tool
```

---

## USAP Action → Policy Fix Mapping

| USAP Recommended Action | Policy Fix | Time to Implement |
|---|---|---|
| `detach_overprivileged_policy` | Detach policy and replace with scoped version | Hours |
| `apply_permission_boundary` | Attach permission boundary to restrict max permissions | Minutes |
| `quarantine_role` | Attach explicit-deny policy to role | Minutes |
| `require_mfa_reenrollment` | Force MFA device deregistration + re-enrollment | Minutes |
| `revoke_session_tokens` | Call `iam:DeactivateMFADevice` + revoke all sessions | Minutes |
| `disable_user` | `iam:UpdateLoginProfile` + deactivate access keys | Minutes |
| `apply_least_privilege_policy` | Run Access Analyzer, generate least-privilege policy | Days |
| `flag_for_access_review` | Schedule review in next sprint | Days |
