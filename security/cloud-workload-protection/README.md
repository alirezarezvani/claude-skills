# Cloud Workload Protection

Container and serverless runtime security — anomaly detection, container escape detection, and CWPP coverage gap analysis.

## When to use

- You need to assess runtime security coverage for Kubernetes workloads
- You suspect a container escape or anomalous pod behavior
- You want to evaluate Lambda/serverless permission sprawl
- You need to identify which workloads lack CWPP agent coverage

## Quick Start

```bash
python scripts/cloud-workload-protection_tool.py --help
python scripts/cloud-workload-protection_tool.py --output json
```

## Skill Level: L4

Runtime inspection actions require operator approval. Gap analysis and advisory output do not require approval.
