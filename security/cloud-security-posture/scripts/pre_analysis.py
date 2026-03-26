#!/usr/bin/env python3
"""
pre_analysis.py — Cloud Security Posture Pre-Analysis

Reads a SecurityFact JSON from stdin, parses cloud misconfiguration signals,
and outputs structured severity scoring for the LLM.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result
exit:   0=informational, 1=high findings, 2=critical findings
"""


import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


CRITICAL_MISCONFIG_TYPES = {
    "public_s3_bucket", "open_security_group", "public_rds", "public_eks",
    "unrestricted_ssh", "unrestricted_rdp", "mfa_disabled_root", "cloudtrail_disabled",
    "root_access_key_active", "encryption_disabled",
}

HIGH_MISCONFIG_TYPES = {
    "overly_permissive_iam", "logging_disabled", "versioning_disabled",
    "public_ami", "open_elasticsearch", "no_flow_logs", "weak_password_policy",
    "no_backup_policy", "public_ecr", "insecure_acl",
}

COMPLIANCE_MAP: Dict[str, List[str]] = {
    "public_s3_bucket": ["CIS 2.1.5", "SOC2 CC6.1", "PCI DSS 1.2"],
    "open_security_group": ["CIS 5.2", "PCI DSS 1.3", "NIST AC-17"],
    "cloudtrail_disabled": ["CIS 3.1", "SOC2 CC7.2", "PCI DSS 10.1"],
    "mfa_disabled_root": ["CIS 1.5", "PCI DSS 8.3.2", "SOC2 CC6.3"],
    "encryption_disabled": ["CIS 2.2", "PCI DSS 3.4", "HIPAA 164.312(e)"],
    "root_access_key_active": ["CIS 1.4", "PCI DSS 7.1"],
    "unrestricted_ssh": ["CIS 5.2", "PCI DSS 1.3.1"],
    "unrestricted_rdp": ["CIS 5.3", "PCI DSS 1.3.1"],
}

REMEDIATION_MAP: Dict[str, str] = {
    "public_s3_bucket": "Enable Block Public Access on the S3 bucket. Review bucket policy and ACLs.",
    "open_security_group": "Restrict inbound rules to known CIDRs. Remove 0.0.0.0/0 and ::/0 ingress.",
    "cloudtrail_disabled": "Enable CloudTrail in all regions with S3 log encryption and log validation.",
    "mfa_disabled_root": "Enable MFA on the root account immediately. Consider hardware MFA.",
    "encryption_disabled": "Enable server-side encryption. For S3, use SSE-S3 or SSE-KMS.",
    "root_access_key_active": "Delete root access keys. Use IAM roles and least-privilege users instead.",
    "unrestricted_ssh": "Restrict SSH (port 22) to bastion host IPs or use SSM Session Manager.",
    "unrestricted_rdp": "Restrict RDP (port 3389) to VPN CIDRs or disable and use SSM instead.",
    "overly_permissive_iam": "Apply least-privilege. Replace * actions with specific permissions.",
    "logging_disabled": "Enable access logging for the resource. Forward logs to centralized SIEM.",
}


def extract_misconfig_signals(fact: Dict[str, Any]) -> Dict[str, Any]:
    payload = fact.get("raw_payload", {})
    if not isinstance(payload, dict):
        payload = {}

    resource_type = str(payload.get("resource_type") or payload.get("resource") or "unknown").lower()
    misconfig_type = str(payload.get("misconfig_type") or payload.get("finding_type") or payload.get("check_id") or "").lower().replace("-", "_").replace(" ", "_")
    public_access = bool(payload.get("public_access") or payload.get("publicly_accessible") or "public" in resource_type)
    compliance_type = str(payload.get("compliance_type") or payload.get("framework") or "").upper()
    region = str(payload.get("region") or payload.get("aws_region") or "unknown")
    account_id = str(payload.get("account_id") or payload.get("aws_account_id") or "unknown")
    resource_arn = str(payload.get("resource_arn") or payload.get("arn") or "unknown")

    # Infer misconfig_type from resource_type if not explicit
    if not misconfig_type or misconfig_type == "unknown":
        if "s3" in resource_type and public_access:
            misconfig_type = "public_s3_bucket"
        elif "security_group" in resource_type or "sg-" in resource_type:
            misconfig_type = "open_security_group"
        elif "rds" in resource_type and public_access:
            misconfig_type = "public_rds"
        elif "cloudtrail" in resource_type:
            misconfig_type = "cloudtrail_disabled"

    return {
        "resource_type": resource_type,
        "misconfig_type": misconfig_type,
        "public_access": public_access,
        "compliance_type": compliance_type,
        "region": region,
        "account_id": account_id,
        "resource_arn": resource_arn,
    }


def score_severity(signals: Dict[str, Any], source_credibility: float) -> tuple[str, float]:
    misconfig_type = signals["misconfig_type"]

    if misconfig_type in CRITICAL_MISCONFIG_TYPES:
        base_score = 0.95
        severity = "critical"
    elif misconfig_type in HIGH_MISCONFIG_TYPES:
        base_score = 0.80
        severity = "high"
    elif signals["public_access"]:
        base_score = 0.75
        severity = "high"
    else:
        base_score = 0.55
        severity = "medium"

    confidence = round(min(base_score * source_credibility, 0.98), 3)
    return severity, confidence


def get_compliance_violations(misconfig_type: str) -> List[str]:
    return COMPLIANCE_MAP.get(misconfig_type, [])


def get_remediation(misconfig_type: str) -> Optional[str]:
    return REMEDIATION_MAP.get(misconfig_type)


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    source_credibility = float(fact.get("source_credibility", 0.80))
    signals = extract_misconfig_signals(fact)
    severity, confidence = score_severity(signals, source_credibility)

    misconfig_type = signals["misconfig_type"]
    compliance_violations = get_compliance_violations(misconfig_type)
    remediation_guidance = get_remediation(misconfig_type)

    is_critical = severity == "critical"
    is_high_public = signals["public_access"] and severity in ("critical", "high")

    output = {
        "analysis_type": "cloud_security_posture_pre_analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "resource_type": signals["resource_type"],
        "misconfig_type": misconfig_type,
        "inferred_severity": severity,
        "confidence": confidence,
        "public_access_confirmed": signals["public_access"],
        "region": signals["region"],
        "account_id": signals["account_id"],
        "resource_arn": signals["resource_arn"],
        "compliance_violations": compliance_violations,
        "remediation_guidance": remediation_guidance,
        "requires_immediate_action": is_critical or is_high_public,
        "intent_type": "mutating" if is_critical else "read_only",
        "mutating_category": "remediation_action" if is_critical else None,
        "attack_surface_note": (
            "Public cloud resource is reachable from the internet. "
            "Unauthorized access, data exfiltration, or cryptomining are common attack outcomes."
        ) if signals["public_access"] else (
            "Resource is not public-facing. Focus on lateral movement and privilege escalation risk."
        ),
    }

    print(json.dumps(output))

    if is_critical:
        return 2
    if severity == "high":
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
