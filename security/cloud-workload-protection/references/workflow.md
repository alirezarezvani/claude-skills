# Cloud Workload Protection Workflow

## Phase 1: Inventory

1. List all containers, pods, and serverless functions in scope
2. Identify which workloads have CWPP agents deployed
3. Calculate CWPP coverage percentage

## Phase 2: Container Security Assessment

1. Review Pod Security Standards compliance (Restricted / Baseline / Privileged)
2. Identify privileged containers and hostPath mounts
3. Review Kubernetes RBAC for over-permission service accounts
4. Check for containers running as root

## Phase 3: Runtime Anomaly Review

1. Review CWPP alerts for the past 30 days
2. Identify anomalous process executions (crypto miners, reverse shells)
3. Check for namespace breakout indicators
4. Review unexpected network connections from pods

## Phase 4: Serverless Assessment

1. List all Lambda/Function execution roles
2. Identify roles with AdministratorAccess or * resource policies
3. Check trigger sources for public exposure
4. Scan environment variables for exposed secrets

## Phase 5: Remediation Roadmap

1. Prioritize CWPP deployment to unprotected critical workloads
2. Restrict over-permissioned serverless execution roles
3. Migrate privileged containers to non-privileged equivalents
4. Implement Pod Security Admission controller in Restricted mode
