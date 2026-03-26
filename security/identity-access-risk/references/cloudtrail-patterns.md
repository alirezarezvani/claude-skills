# AWS CloudTrail Event Analysis Patterns

When analyzing raw CloudTrail events, look for these high-signal patterns:

## Pattern 1: Enumeration Burst (T+0 to T+5 min after compromise)
```
eventNames: [
  "sts:GetCallerIdentity",     // attacker confirms access
  "iam:GetAccountSummary",     // enumerates account structure
  "iam:ListUsers",              // harvests user list
  "iam:ListRoles",              // identifies target roles
  "s3:ListAllMyBuckets",        // identifies data targets
  "ec2:DescribeInstances"       // maps compute infrastructure
]
```
All six calls within a 5-minute window = high-confidence compromise indicator.

## Pattern 2: Backdoor Creation (T+10 to T+20 min)
```
eventNames: [
  "iam:CreateUser",
  "iam:CreateAccessKey",
  "iam:AttachUserPolicy"   // with AdministratorAccess
]
userAgent: "Boto3/1.x.x Python/3.x" (headless CLI tool, not console)
sourceIPAddress: external/unusual IP
```
This pattern = attacker has created persistent access — urgency escalates to critical.

## Pattern 3: Defense Evasion (T+20 to T+30 min)
```
eventNames: [
  "cloudtrail:StopLogging",    // disabling your visibility
  "cloudtrail:DeleteTrail",
  "guardduty:DeleteDetector",
  "config:StopConfigurationRecorder"
]
```
If any of these appear: incident severity automatically escalates to SEV1. The attacker is now actively removing your ability to detect and respond.

## Pattern 4: Privilege Escalation via Role Assumption Chain
```
Account A: sts:AssumeRole → Role in Account B
Account B: sts:AssumeRole → Role in Account C (admin)
```
Multi-hop AssumeRole chains are a classic SolarWinds/APT technique to obscure the original compromised identity and elevate to admin without directly modifying any IAM policy.

## Pattern 5: Data Exfiltration Precursor
```
eventNames: [
  "kms:ListKeys",             // finding encryption keys
  "kms:DescribeKey",
  "s3:GetBucketEncryption",  // understanding encryption
  "s3:GetObject",            // starting data access
  "rds:DescribeDBInstances", // identifying databases
  "secretsmanager:ListSecrets"
]
```
This sequence = attacker has moved from reconnaissance to data collection.
