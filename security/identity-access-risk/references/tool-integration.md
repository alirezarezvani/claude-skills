# Tool Integration

```bash
# Analyze an IAM policy JSON for privilege escalation
python skills/identity-access-risk/scripts/analyze_iam_policy.py policy.json

# Scan all IAM policies in a directory
python skills/identity-access-risk/scripts/analyze_iam_policy.py policies/ --directory --json

# Score CVE severity for a related vulnerability
python skills/shared/scripts/cvss_scorer.py --vector "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H"

# Pipe policy JSON from stdin
aws iam get-policy-version --policy-arn arn:aws:iam::...:policy/... --version-id v1 \
  | jq '.PolicyVersion.Document' | python analyze_iam_policy.py -
```
