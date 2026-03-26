# IAM Risk Matrix

## High-Risk IAM Actions (Always Investigate)

| Action | Risk | Notes |
|---|---|---|
| `iam:CreateUser` | High | New privileged user creation |
| `iam:AttachUserPolicy` | High | Adding permissions to user |
| `iam:AttachRolePolicy` | High | Expanding role permissions |
| `iam:CreateAccessKey` | High | New credential creation |
| `sts:AssumeRole` from unknown principal | Critical | Lateral movement indicator |
| `sts:AssumeRoleWithWebIdentity` anomaly | High | OIDC abuse |
| `iam:PassRole` to unexpected service | High | Privilege escalation path |
| `iam:PutRolePolicy` | Critical | Inline policy granting broad access |
| `iam:CreateLoginProfile` on service account | High | Interactive login enabled on service account |
| Root account `ConsoleLogin` | Critical | Root should never login except for billing |

## AssumeRole Chain Analysis

A suspicious AssumeRole chain has these characteristics:
- More than 2 hops in the role chain
- Crossing account boundaries to reach a more privileged role
- Origin principal not in the expected caller list for the target role
- Call from an IP not in the expected range for that principal

## Least Privilege Assessment

When evaluating overprivileged identities:

1. Compare attached policies against actual API calls in the last 90 days
2. Flag any permission that has not been used in 90+ days
3. Flag wildcard resource permissions (`*`) when specific resources are used
4. Flag `AdministratorAccess` on any non-root identity
5. Flag `*` actions on sensitive services: S3, KMS, IAM, STS, Secrets Manager

## MFA Bypass Indicators

- User has MFA device enrolled but session created without MFA token
- AssumeRole from a user principal without MFA condition in the role trust policy
- Authentication from known VPN/proxy IP combined with no MFA
