# Pipeline Security Scan

Scan CI/CD pipeline configurations for secrets, missing security stages, unsigned artifacts, and insecure third-party action usage.

## When to use

- Auditing a CI/CD pipeline configuration for security issues
- Checking if a new pipeline has all required security stages
- Detecting secrets accidentally committed to pipeline YAML
- Verifying artifact signing and action pinning configuration

## Quick Start

```bash
python scripts/pipeline-security-scan_tool.py --help
python scripts/pipeline-security-scan_tool.py --output json
```

## Skill Level: L4

Hardcoded secrets findings escalated to secrets-exposure. Artifact signing gaps escalated to build-integrity.

## Supported Pipelines

- GitHub Actions
- GitLab CI
- Jenkins
- CircleCI
- Bitbucket Pipelines
