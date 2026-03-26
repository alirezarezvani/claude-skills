# AppSec Code Review

Security-focused static code analysis covering OWASP Top 10, logic flaws, and dependency audits — designed for use as a PR security gate.

## When to use

- Reviewing a pull request for security vulnerabilities before merge
- Assessing a new feature for OWASP Top 10 risks
- Checking dependency changes for known vulnerable packages
- Validating cryptographic implementation correctness

## Quick Start

```bash
python scripts/appsec-code-review_tool.py --help
python scripts/appsec-code-review_tool.py --output json
```

## Skill Level: L4

Critical and High findings block PR merge. Produces CWE-mapped findings with developer-friendly remediation guidance.
