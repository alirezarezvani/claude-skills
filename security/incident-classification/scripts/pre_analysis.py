#!/usr/bin/env python3
"""
pre_analysis.py — Incident Classification Pre-Analysis

Reads a SecurityFact JSON from stdin, triages event_type + severity +
source_credibility into a NIST IR phase and incident category.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result
exit:   0=detect/monitor, 1=respond, 2=critical/contain
"""


import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# NIST SP 800-61 Incident Response lifecycle phases
NIST_PHASES = ("Preparation", "Detection", "Analysis", "Containment", "Eradication", "Recovery", "Post-Incident")

# Event type to NIST phase + category mapping
EVENT_TYPE_CLASSIFICATION: Dict[str, Dict[str, Any]] = {
    "secret_exposure": {
        "nist_phase": "Containment",
        "category": "Credential Compromise",
        "severity_floor": "high",
        "iocs": ["leaked credential", "unauthorized API call", "new IAM user"],
    },
    "iam_anomaly": {
        "nist_phase": "Analysis",
        "category": "Privilege Escalation",
        "severity_floor": "high",
        "iocs": ["AssumeRole abuse", "policy attach", "new admin user"],
    },
    "network_intrusion": {
        "nist_phase": "Containment",
        "category": "Unauthorized Access",
        "severity_floor": "high",
        "iocs": ["lateral movement", "C2 beacon", "port scan"],
    },
    "data_breach": {
        "nist_phase": "Containment",
        "category": "Data Exfiltration",
        "severity_floor": "critical",
        "iocs": ["large outbound transfer", "PII access", "database dump"],
    },
    "endpoint_compromise": {
        "nist_phase": "Containment",
        "category": "Malware / Ransomware",
        "severity_floor": "high",
        "iocs": ["malware process", "encrypted files", "C2 callback"],
    },
    "insider_threat": {
        "nist_phase": "Analysis",
        "category": "Insider Threat",
        "severity_floor": "medium",
        "iocs": ["bulk download", "off-hours access", "data staging"],
    },
    "cloud_misconfiguration": {
        "nist_phase": "Analysis",
        "category": "Configuration Error",
        "severity_floor": "medium",
        "iocs": ["public resource", "open security group", "missing encryption"],
    },
    "vulnerability_found": {
        "nist_phase": "Analysis",
        "category": "Vulnerability",
        "severity_floor": "medium",
        "iocs": ["CVE identifier", "CVSS score", "affected component"],
    },
    "zero_day": {
        "nist_phase": "Containment",
        "category": "Zero-Day Exploitation",
        "severity_floor": "critical",
        "iocs": ["no patch", "exploitation in wild", "CISA KEV"],
    },
    "compliance_violation": {
        "nist_phase": "Analysis",
        "category": "Compliance Failure",
        "severity_floor": "low",
        "iocs": ["audit finding", "control gap", "framework violation"],
    },
    "devsecops_event": {
        "nist_phase": "Detection",
        "category": "Pipeline Security",
        "severity_floor": "medium",
        "iocs": ["failed SAST", "IaC violation", "dependency CVE"],
    },
    "supply_chain_event": {
        "nist_phase": "Analysis",
        "category": "Supply Chain Compromise",
        "severity_floor": "high",
        "iocs": ["malicious package", "build artifact tampering", "dependency confusion"],
    },
    "threat_intel": {
        "nist_phase": "Detection",
        "category": "Threat Intelligence",
        "severity_floor": "medium",
        "iocs": ["malicious IP/domain", "IOC match", "threat actor TTP"],
    },
    "red_team_finding": {
        "nist_phase": "Analysis",
        "category": "Red Team / Pentest",
        "severity_floor": "medium",
        "iocs": ["attack path", "exploited control", "compromise evidence"],
    },
}

SEVERITY_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}

CONTAINMENT_ACTIONS: Dict[str, List[str]] = {
    "Credential Compromise": ["Revoke affected credentials", "Enable MFA", "Audit recent API activity"],
    "Privilege Escalation": ["Revoke escalated permissions", "Review CloudTrail", "Alert SOC lead"],
    "Unauthorized Access": ["Block source IP", "Isolate affected host", "Capture forensic image"],
    "Data Exfiltration": ["Block outbound transfer", "Notify DPO", "Preserve evidence chain"],
    "Malware / Ransomware": ["Isolate host from network", "Suspend backups (prevent encryption)", "Engage IR team"],
    "Insider Threat": ["Suspend user account", "Preserve audit logs", "Legal hold"],
    "Configuration Error": ["Apply remediation", "Verify no unauthorized access occurred"],
    "Zero-Day Exploitation": ["Apply compensating controls", "Patch or isolate immediately"],
    "Supply Chain Compromise": ["Pin dependency versions", "Rebuild from known-good", "Notify downstream users"],
}


def classify_incident(fact: Dict[str, Any]) -> Dict[str, Any]:
    event_type = str(fact.get("event_type") or "unknown").lower()
    severity = str(fact.get("severity") or "medium").lower()
    source_credibility = float(fact.get("source_credibility") or 0.80)

    classification = EVENT_TYPE_CLASSIFICATION.get(event_type, {
        "nist_phase": "Detection",
        "category": "Unknown",
        "severity_floor": "low",
        "iocs": [],
    })

    # Escalate to severity_floor if current severity is lower
    floor = classification["severity_floor"]
    effective_severity = severity if SEVERITY_RANK.get(severity, 0) >= SEVERITY_RANK.get(floor, 0) else floor

    # Phase elevation based on severity
    if effective_severity == "critical" and classification["nist_phase"] in ("Detection", "Analysis"):
        escalated_phase = "Containment"
    else:
        escalated_phase = classification["nist_phase"]

    containment_actions = CONTAINMENT_ACTIONS.get(classification["category"], [
        "Triage event with senior analyst",
        "Preserve evidence",
        "Assess blast radius",
    ])

    confidence = round(min(source_credibility * (0.90 if event_type in EVENT_TYPE_CLASSIFICATION else 0.65), 0.95), 3)
    is_containment = escalated_phase == "Containment"

    return {
        "event_type": event_type,
        "inferred_severity": effective_severity,
        "nist_ir_phase": escalated_phase,
        "incident_category": classification["category"],
        "expected_iocs": classification["iocs"],
        "containment_actions": containment_actions,
        "confidence": confidence,
        "requires_immediate_containment": is_containment and effective_severity in ("high", "critical"),
    }


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    result = classify_incident(fact)
    is_critical = result["inferred_severity"] == "critical"
    is_high = result["inferred_severity"] == "high"
    is_containment = result["requires_immediate_containment"]

    output = {
        "analysis_type": "incident_classification_pre_analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **result,
        "intent_type": "mutating" if is_containment else "read_only",
        "mutating_category": "remediation_action" if is_containment else None,
        "triage_note": (
            f"NIST IR Phase: {result['nist_ir_phase']}. "
            f"Category: {result['incident_category']}. "
            f"Immediate containment {'required' if is_containment else 'not yet required'}."
        ),
    }

    print(json.dumps(output))

    if is_critical and is_containment:
        return 2
    if is_high:
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
