#!/usr/bin/env python3
"""
pre_analysis.py — Identity and Access Risk Pre-Analysis

Called by USAP prompt_compiler BEFORE the LLM reasons.
Reads a SecurityFact JSON from stdin, applies deterministic pattern analysis
to detect IAM anomaly types, match CloudTrail attack patterns, and estimate
blast radius. Outputs structured JSON for the LLM to reason on top of.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result (injected into prompt as tool_pre_analysis)
exit:   0=low/medium, 1=high, 2=critical
"""


import argparse
import json
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set, Tuple


# ── Anomaly type detection patterns ──────────────────────────────────────────
# Each entry: (anomaly_type, keywords, severity, mitre_technique)

ANOMALY_PATTERNS: List[Tuple[str, List[str], str, str]] = [
    (
        "privilege_escalation",
        ["passrole", "pass_role", "createpolicyversion", "create_policy_version",
         "attachuserpolicy", "attach_user_policy", "attachrolepolicy", "putuserpolicy",
         "put_user_policy", "privilege escalat", "escalat"],
        "critical",
        "T1078.004 / T1484.001",
    ),
    (
        "lateral_movement",
        ["assumerole", "assume_role", "cross-account", "cross_account", "lateral movement",
         "unfamiliar account", "unknown account", "external account"],
        "high",
        "T1550.001",
    ),
    (
        "credential_stuffing",
        ["credential stuffing", "brute force", "failed login", "failed authentication",
         "multiple failed", "repeated failed", "password spray", "high-frequency"],
        "high",
        "T1110.004",
    ),
    (
        "impossible_travel",
        ["impossible travel", "geographic", "two location", "two ip", "different country",
         "different region", "geo anomal"],
        "high",
        "T1078",
    ),
    (
        "mfa_bypass",
        ["mfa bypass", "mfaused: no", "mfa_used: false", "without mfa", "no mfa",
         "mfa not used", "authentication without mfa", "mfa disabled"],
        "critical",
        "T1556.006",
    ),
    (
        "root_account_usage",
        ["root account", "root user", "aws root", "accountId root", "root credential"],
        "critical",
        "T1078.004",
    ),
    (
        "defense_evasion",
        ["stoplogging", "stop_logging", "deletetrail", "delete_trail", "stoplogging",
         "deletedetector", "disableguardduty", "disablesecurityhub",
         "stopconfigurationrecorder", "logging disabled", "trail deleted", "guardduty disabled"],
        "critical",
        "T1562.008",
    ),
    (
        "backdoor_creation",
        ["createuser", "create_user", "createaccesskey", "create_access_key",
         "new iam user", "new access key", "created user", "created access key"],
        "critical",
        "T1098.001",
    ),
    (
        "dormant_reactivation",
        ["dormant", "inactive", "not used", "last used", "90 day", "long inactive",
         "reactivat", "first use in"],
        "medium",
        "T1078.004",
    ),
    (
        "unusual_api_call_volume",
        ["unusual volume", "spike", "10x", "high volume", "abnormal call", "excessive api",
         "rate anomal", "call volume"],
        "medium",
        "T1078.004",
    ),
    (
        "service_account_interactive",
        ["service account", "svc-", "svc_", "automation account", "interactive", "console login",
         "unexpected login", "human login", "service role interactive"],
        "high",
        "T1078.002",
    ),
    (
        "data_enumeration_burst",
        ["listbuckets", "listusers", "describeinstances", "listsecrets", "list all",
         "enumerate", "enumerating", "reconnaissance", "discovery burst"],
        "high",
        "T1619",
    ),
    (
        "overprivileged_identity",
        ["administrator", "administratoraccess", "admin access", "wildcard permission",
         "overprivileg", "excess permission", "broad permission", "iam:*", "action: *"],
        "medium",
        "T1078.004",
    ),
    (
        "cross_account_anomaly",
        ["cross.account", "unknown account", "external account", "unexpected account",
         "account id", "unfamiliar account"],
        "high",
        "T1550.001",
    ),
]

# CloudTrail attack pattern signatures (5 patterns from SKILL.md)
CLOUDTRAIL_PATTERNS: List[Tuple[str, List[str], str]] = [
    (
        "enumeration_burst",
        ["getcalleridentity", "getaccountsummary", "listusers", "listroles",
         "listallmybuckets", "describeinstances"],
        "Attacker confirmed access and mapped the environment — enumeration phase complete.",
    ),
    (
        "backdoor_creation",
        ["createuser", "createaccesskey", "attachuserpolicy"],
        "Backdoor creation sequence detected — attacker may have persistent access now.",
    ),
    (
        "defense_evasion",
        ["stoplogging", "deletetrail", "deletedetector", "stopconfigurationrecorder"],
        "CRITICAL: Defense evasion sequence — attacker is destroying your visibility.",
    ),
    (
        "role_assumption_chain",
        ["assumerole", "assumeroleWithwebidentity", "assumeroleWithsaml"],
        "Role assumption chain — may be multi-hop lateral movement between accounts.",
    ),
    (
        "data_exfil_precursor",
        ["listkeys", "getbucketencryption", "listsecrets", "describedbinstances", "getparameter"],
        "Data exfiltration precursor — attacker is mapping encryption and data stores.",
    ),
]

# Blast radius keyword signals
BLAST_RADIUS_SIGNALS: Dict[str, List[str]] = {
    "full_account": [
        "administrator", "administeraccess", "iam:*", "action: *", "resource: *",
        "root account", "root user", "all resources", "full access",
        "poweruser", "power_user", "cross-account admin",
    ],
    "data_exfiltration_risk": [
        "s3", "rds", "dynamodb", "redshift", "secretsmanager", "ssm parameter",
        "data access", "database", "secret", "customer data", "pii", "sensitive",
    ],
    "infrastructure_manipulation": [
        "ec2", "eks", "ecs", "lambda", "cloudformation", "vpc", "network",
        "compute", "instance", "container", "serverless",
    ],
}


def extract_all_text(fact: Dict[str, Any]) -> str:
    """Flatten all string fields in the SecurityFact to a single searchable string."""
    parts = []

    def _extract(obj: Any, depth: int = 0) -> None:
        if depth > 5:
            return
        if isinstance(obj, str):
            parts.append(obj)
        elif isinstance(obj, dict):
            for v in obj.values():
                _extract(v, depth + 1)
        elif isinstance(obj, list):
            for item in obj:
                _extract(item, depth + 1)

    _extract(fact)
    return " ".join(parts).lower()


def detect_anomaly_types(text: str) -> List[Dict[str, Any]]:
    """Scan text for IAM anomaly type indicators."""
    detected = []
    for anomaly_type, keywords, severity, mitre in ANOMALY_PATTERNS:
        matched_keywords = [kw for kw in keywords if kw.lower() in text]
        if matched_keywords:
            detected.append({
                "anomaly_type": anomaly_type,
                "severity": severity,
                "mitre_technique": mitre,
                "matched_on": matched_keywords[:3],
            })
    return detected


def detect_cloudtrail_patterns(text: str) -> List[Dict[str, Any]]:
    """Check for known CloudTrail attack pattern signatures in the text."""
    matched = []
    for pattern_name, event_names, description in CLOUDTRAIL_PATTERNS:
        found = [e for e in event_names if e.lower() in text]
        if len(found) >= 2:  # Require at least 2 matching events for a pattern
            matched.append({
                "pattern": pattern_name,
                "matched_events": found,
                "description": description,
                "confidence": round(min(0.95, 0.60 + len(found) * 0.07), 3),
            })
    return matched


def assess_blast_radius(text: str) -> str:
    """Estimate blast radius from available text signals."""
    for tier, signals in BLAST_RADIUS_SIGNALS.items():
        if any(s.lower() in text for s in signals):
            return tier
    return "service_scoped"  # conservative default


def estimate_severity(
    anomaly_types: List[Dict],
    cloudtrail_patterns: List[Dict],
    blast_radius: str,
) -> Tuple[str, str]:
    """Return (severity, primary_reason)."""
    # Defense evasion is always critical — attacker is destroying evidence
    if any(a["anomaly_type"] == "defense_evasion" for a in anomaly_types):
        return "critical", "Defense evasion events detected — escalated to SEV1"

    if any(a["anomaly_type"] == "backdoor_creation" for a in anomaly_types):
        return "critical", "Backdoor creation events detected — attacker may have persistent access"

    if any(a["severity"] == "critical" for a in anomaly_types):
        critical_types = [a["anomaly_type"] for a in anomaly_types if a["severity"] == "critical"]
        return "critical", f"Critical anomaly types: {', '.join(critical_types)}"

    if any(p["pattern"] == "enumeration_burst" for p in cloudtrail_patterns):
        return "high", "Enumeration burst pattern — attacker mapped environment"

    if any(a["severity"] == "high" for a in anomaly_types):
        high_types = [a["anomaly_type"] for a in anomaly_types if a["severity"] == "high"]
        return "high", f"High anomaly types: {', '.join(high_types)}"

    if blast_radius == "full_account":
        return "high", "Full account blast radius with anomaly indicators"

    return "medium", "Medium-severity IAM anomalies detected"


def score_confidence(
    fact: Dict[str, Any],
    anomaly_count: int,
    cloudtrail_count: int,
) -> float:
    """Estimate confidence from source credibility + evidence density."""
    source_credibility = float(fact.get("source_credibility", 0.80))
    base = source_credibility

    # More matching anomaly types = higher confidence
    base += min(anomaly_count * 0.05, 0.15)

    # CloudTrail patterns are strong signals
    base += min(cloudtrail_count * 0.08, 0.16)

    return round(min(base, 0.99), 3)


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    timestamp = datetime.now(timezone.utc).isoformat()

    # Extract all searchable text from the SecurityFact
    full_text = extract_all_text(fact)

    # Run analyses
    anomaly_types = detect_anomaly_types(full_text)
    cloudtrail_patterns = detect_cloudtrail_patterns(full_text)
    blast_radius = assess_blast_radius(full_text)
    severity, severity_reason = estimate_severity(anomaly_types, cloudtrail_patterns, blast_radius)
    confidence = score_confidence(fact, len(anomaly_types), len(cloudtrail_patterns))

    # Intent classification
    if severity in ("critical", "high") and blast_radius != "minimal":
        # Determine which mutating category applies
        has_policy_issues = any(
            a["anomaly_type"] in ("privilege_escalation", "overprivileged_identity", "mfa_bypass")
            for a in anomaly_types
        )
        has_credential_issues = any(
            a["anomaly_type"] in ("backdoor_creation", "lateral_movement", "root_account_usage")
            for a in anomaly_types
        )
        if has_credential_issues:
            intent_type = "mutating"
            mutating_category = "credential_operation"
            recommended_action = "revoke_session_tokens"
        elif has_policy_issues:
            intent_type = "mutating"
            mutating_category = "policy_change"
            recommended_action = "detach_overprivileged_policy"
        else:
            intent_type = "mutating"
            mutating_category = "credential_operation"
            recommended_action = "revoke_session_tokens"
    else:
        intent_type = "read_only"
        mutating_category = None
        recommended_action = "flag_for_access_review"

    # False positive check
    fp_signals = []
    payload = fact.get("raw_payload", {})
    if isinstance(payload, dict):
        principal = str(payload.get("principal", ""))
        if any(kw in principal.lower() for kw in ("automation", "cicd", "pipeline", "deploy", "ci-")):
            fp_signals.append(f"principal '{principal}' looks like CI/CD automation — verify before action")

    # Extract principal info
    principal = None
    if isinstance(payload, dict):
        principal = (
            payload.get("principal")
            or payload.get("principal_arn")
            or payload.get("user")
            or payload.get("role")
        )

    output = {
        "analysis_type": "iam_pre_analysis",
        "timestamp_utc": timestamp,
        "detected_anomaly_types": anomaly_types,
        "cloudtrail_patterns_matched": cloudtrail_patterns,
        "blast_radius": blast_radius,
        "severity_estimate": severity,
        "severity_reason": severity_reason,
        "confidence": confidence,
        "intent_type": intent_type,
        "mutating_category": mutating_category,
        "recommended_action": recommended_action,
        "principal_identified": principal,
        "false_positive_signals": fp_signals,
        "key_risk_summary": (
            f"Detected {len(anomaly_types)} anomaly type(s): "
            + ", ".join(a["anomaly_type"] for a in anomaly_types[:5])
            + (f". {len(cloudtrail_patterns)} CloudTrail attack pattern(s) matched." if cloudtrail_patterns else "")
        ) if anomaly_types else "No explicit anomaly type matched — use SecurityFact context for classification.",
        "mitre_techniques": list({
            a["mitre_technique"] for a in anomaly_types
        }),
    }

    print(json.dumps(output))

    if severity == "critical":
        return 2
    if severity == "high":
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
