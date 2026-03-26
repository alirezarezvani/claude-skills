# Remediation Commands by Provider

These commands are for documentation and human execution only. The CSPM agent does not execute them autonomously.

## AWS CLI

```bash
# AWS-01: Enable S3 Block Public Access
aws s3api put-public-access-block --bucket BUCKET_NAME \
  --public-access-block-configuration "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"

# AWS-07: Enable CloudTrail
aws cloudtrail create-trail --name org-audit-trail --s3-bucket-name audit-logs-bucket --is-multi-region-trail
```

## Azure CLI

```bash
# AZ-01: Disable public blob access
az storage account update --name ACCOUNT_NAME --resource-group RG_NAME --allow-blob-public-access false
```

## GCP CLI

```bash
# GCP-01: Remove public access from bucket
gsutil iam ch -d allUsers gs://BUCKET_NAME
gsutil iam ch -d allAuthenticatedUsers gs://BUCKET_NAME
```
