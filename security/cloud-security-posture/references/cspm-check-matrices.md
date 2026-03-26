# CSPM Check Matrices

## AWS CSPM Check Matrix

| Check ID | Resource | Finding | Severity | CIS Benchmark |
|---|---|---|---|---|
| AWS-01 | S3 Bucket | Block Public Access disabled | Critical | CIS AWS 2.1.1 |
| AWS-02 | S3 Bucket | Bucket ACL grants public read | Critical | CIS AWS 2.1.2 |
| AWS-03 | RDS Instance | Publicly accessible flag = true | Critical | CIS AWS 2.3.3 |
| AWS-04 | Security Group | Ingress rule: 0.0.0.0/0 to port 22 | High | CIS AWS 5.2 |
| AWS-05 | Security Group | Ingress rule: 0.0.0.0/0 to port 3389 | Critical | CIS AWS 5.3 |
| AWS-06 | Security Group | Ingress rule: 0.0.0.0/0 to any port | Critical | CIS AWS 5.1 |
| AWS-07 | CloudTrail | CloudTrail not enabled in all regions | Critical | CIS AWS 3.1 |
| AWS-08 | IAM | Root account has active access key | Critical | CIS AWS 1.4 |
| AWS-09 | IAM | Root account MFA not enabled | Critical | CIS AWS 1.5 |
| AWS-10 | IAM | Password policy: min length < 14 | Medium | CIS AWS 1.8 |
| AWS-11 | IAM | Password policy: no MFA requirement | High | CIS AWS 1.10 |
| AWS-12 | IAM | IAM user with AdministratorAccess and no MFA | Critical | CIS AWS 1.10 |
| AWS-13 | IAM | Access key not rotated in 90+ days | Medium | CIS AWS 1.14 |
| AWS-14 | KMS | CMK rotation not enabled | Medium | CIS AWS 3.8 |
| AWS-15 | VPC | VPC Flow Logs disabled | High | CIS AWS 3.9 |
| AWS-16 | Config | AWS Config not enabled | High | CIS AWS 3.5 |
| AWS-17 | Lambda | Function with admin IAM role | High | Custom |
| AWS-18 | ECR | Repository scan on push disabled | Medium | Custom |
| AWS-19 | EBS | Snapshot is public | Critical | CIS AWS 2.2.1 |
| AWS-20 | Secrets Manager | Secret not rotated in 90+ days | High | Custom |

## Azure CSPM Check Matrix

| Check ID | Resource | Finding | Severity | Framework |
|---|---|---|---|---|
| AZ-01 | Storage Account | Public blob access enabled | Critical | CIS Azure 3.1 |
| AZ-02 | NSG | Inbound rule: Any source to RDP (3389) | Critical | CIS Azure 6.1 |
| AZ-03 | NSG | Inbound rule: Any source to SSH (22) | High | CIS Azure 6.2 |
| AZ-04 | Azure AD | Global Admin role with no MFA | Critical | CIS Azure 1.1 |
| AZ-05 | RBAC | Owner role assigned to service principal | High | CIS Azure 1.21 |
| AZ-06 | RBAC | Custom role with * wildcard permissions | High | Custom |
| AZ-07 | Defender | Defender for Cloud not enabled on subscription | High | CIS Azure 2.1 |
| AZ-08 | Monitor | Diagnostic settings: no activity log export | High | CIS Azure 5.1 |
| AZ-09 | SQL Database | Auditing disabled | High | CIS Azure 4.1 |
| AZ-10 | Key Vault | Soft delete disabled | Medium | CIS Azure 8.4 |

## GCP CSPM Check Matrix

| Check ID | Resource | Finding | Severity | Framework |
|---|---|---|---|---|
| GCP-01 | Cloud Storage | Bucket IAM: allUsers or allAuthenticatedUsers | Critical | CIS GCP 5.1 |
| GCP-02 | Compute | VPC firewall rule: 0.0.0.0/0 to port 22 | High | CIS GCP 3.6 |
| GCP-03 | Compute | VPC firewall rule: 0.0.0.0/0 to port 3389 | Critical | CIS GCP 3.7 |
| GCP-04 | IAM | Default service account used by compute instance | High | CIS GCP 4.1 |
| GCP-05 | IAM | Service account has editor or owner role | High | CIS GCP 1.5 |
| GCP-06 | Logging | Cloud Audit Logs: admin activity disabled | Critical | CIS GCP 2.1 |
| GCP-07 | SQL | Cloud SQL instance is publicly accessible | Critical | CIS GCP 6.2 |
| GCP-08 | GKE | Legacy authorization enabled on cluster | High | CIS GCP 7.3 |
| GCP-09 | GKE | Dashboard addon enabled | High | CIS GCP 7.7 |
| GCP-10 | IAM | API keys not restricted (any API access) | Medium | CIS GCP 1.13 |
