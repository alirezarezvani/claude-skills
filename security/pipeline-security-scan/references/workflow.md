# Pipeline Security Scan Workflow

## Phase 1: Pipeline Inventory

1. List all CI/CD pipeline files (.github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile)
2. Identify all stages, jobs, and steps
3. List all environment variables defined in pipeline files and CI platform settings

## Phase 2: Secrets Scan

1. Scan all env var values for high-entropy strings (potential secrets)
2. Check for known secret patterns: AWS keys, GCP service account JSON, API keys
3. Scan step commands for inline credential usage
4. Check container image arguments for embedded credentials

## Phase 3: Security Stage Audit

For each pipeline:
- [ ] SAST stage present and runs on all PRs
- [ ] SCA/dependency scanning stage present
- [ ] Secrets scanning stage present (trufflehog, gitleaks, or equivalent)
- [ ] Container image scanning stage (Trivy, Grype)
- [ ] DAST stage present (at minimum for main branch)

## Phase 4: Artifact Integrity

- [ ] Artifact signing configured (Sigstore/cosign or equivalent)
- [ ] SBOM generation step present
- [ ] Provenance attestation configured
- [ ] Docker images pushed with digest (not just tag)

## Phase 5: Permissions and Actions

- [ ] GitHub Actions: explicit permission restrictions (not write-all)
- [ ] All third-party actions pinned to commit hash
- [ ] No actions from unverified publishers
- [ ] Self-hosted runner scope is minimal

## Phase 6: Findings Report

1. Classify findings by severity
2. Escalate hardcoded secrets to secrets-exposure immediately
3. Produce remediation roadmap with priorities
