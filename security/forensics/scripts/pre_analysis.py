#!/usr/bin/env python3
"""
pre_analysis.py — Forensics Pre-Analysis

Reads a SecurityFact JSON from stdin, parses dwell time, exfiltration
confirmation, and affected data stores into an IOC summary for the LLM.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result
exit:   0=investigation, 1=significant findings, 2=confirmed breach/exfiltration
"""


import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


# Dwell time thresholds (hours)
DWELL_CRITICAL = 720    # 30 days
DWELL_HIGH = 168        # 7 days
DWELL_MEDIUM = 24       # 1 day

# Evidence preservation priority
EVIDENCE_SOURCES = [
    "Memory dumps (volatile — capture first)",
    "Running process list and network connections",
    "Authentication and access logs (SIEM)",
    "Cloud trail / audit logs",
    "Endpoint EDR telemetry",
    "File system timeline (MFT, inode changes)",
    "Network flow records (NetFlow/IPFIX)",
    "Email gateway logs",
    "DLP alert history",
]

CHAIN_OF_CUSTODY_STEPS = [
    "Assign unique evidence identifier (EV-XXXX)",
    "Document collection method, timestamp, and collector identity",
    "Hash all collected artifacts (SHA-256)",
    "Store in write-protected evidence repository",
    "Maintain access log for the evidence repository",
    "Notify legal counsel for potential litigation hold",
]


def parse_forensic_fields(fact: Dict[str, Any]) -> Dict[str, Any]:
    payload = fact.get("raw_payload", {})
    if not isinstance(payload, dict):
        payload = {}

    # Dwell time
    dwell_time_hours: Optional[float] = None
    for field in ("dwell_time_hours", "dwell_time", "time_to_detect_hours", "days_undetected"):
        val = payload.get(field) or fact.get(field)
        if val is not None:
            try:
                v = float(val)
                # If field name suggests days, convert
                if "days" in field:
                    v *= 24
                dwell_time_hours = v
                break
            except (ValueError, TypeError):
                continue

    # Exfiltration
    exfiltration_confirmed = bool(
        payload.get("exfiltration_confirmed")
        or payload.get("data_exfiltrated")
        or payload.get("exfil_confirmed")
        or payload.get("data_stolen")
    )

    # Data volume exfiltrated
    exfil_volume_gb: Optional[float] = None
    for field in ("exfil_volume_gb", "data_exfiltrated_gb", "exfil_size_gb"):
        val = payload.get(field)
        if val is not None:
            try:
                exfil_volume_gb = float(val)
                break
            except (ValueError, TypeError):
                continue

    # Affected data stores
    affected_data_stores: List[str] = []
    for field in ("affected_data_stores", "data_stores", "compromised_systems", "affected_systems"):
        val = payload.get(field) or fact.get(field)
        if isinstance(val, list):
            affected_data_stores = [str(s) for s in val]
            break
        if isinstance(val, str) and val:
            affected_data_stores = [val]
            break

    # PII involved
    pii_involved = bool(
        payload.get("pii_involved")
        or payload.get("personal_data")
        or payload.get("sensitive_data")
        or any(kw in str(payload).lower() for kw in ("pii", "personal", "gdpr", "hipaa", "phi", "ssn", "credit card"))
    )

    # Persistence indicators
    persistence_detected = bool(
        payload.get("persistence_detected")
        or payload.get("backdoor")
        or payload.get("scheduled_task")
        or payload.get("startup_modification")
    )

    # Lateral movement
    lateral_movement = bool(
        payload.get("lateral_movement")
        or payload.get("east_west_traffic")
        or payload.get("credential_reuse")
    )

    # Initial access vector
    initial_access_vector = str(payload.get("initial_access_vector") or payload.get("attack_vector") or "unknown")

    # Number of affected hosts
    affected_hosts_count = int(payload.get("affected_hosts") or payload.get("compromised_hosts") or 0)

    return {
        "dwell_time_hours": dwell_time_hours,
        "exfiltration_confirmed": exfiltration_confirmed,
        "exfil_volume_gb": exfil_volume_gb,
        "affected_data_stores": affected_data_stores,
        "pii_involved": pii_involved,
        "persistence_detected": persistence_detected,
        "lateral_movement": lateral_movement,
        "initial_access_vector": initial_access_vector,
        "affected_hosts_count": affected_hosts_count,
    }


def assess_dwell_severity(dwell_hours: Optional[float]) -> tuple[str, str]:
    if dwell_hours is None:
        return "unknown", "Dwell time unknown — investigate log gaps for timeline reconstruction."
    if dwell_hours >= DWELL_CRITICAL:
        return "critical", f"Long-term compromise: {dwell_hours:.0f} hours ({dwell_hours/24:.0f} days). Advanced persistence likely. Full forensic investigation required."
    if dwell_hours >= DWELL_HIGH:
        return "high", f"Extended dwell: {dwell_hours:.0f} hours ({dwell_hours/24:.1f} days). Lateral movement and data staging probable."
    if dwell_hours >= DWELL_MEDIUM:
        return "medium", f"Moderate dwell: {dwell_hours:.0f} hours. Assess for privilege escalation and data access."
    return "low", f"Short dwell: {dwell_hours:.0f} hours. Early detection — limit blast radius assessment."


def build_ioc_summary(fields: Dict[str, Any]) -> List[str]:
    iocs = []
    if fields["exfiltration_confirmed"]:
        vol = f" ({fields['exfil_volume_gb']:.1f} GB)" if fields["exfil_volume_gb"] else ""
        iocs.append(f"Data exfiltration confirmed{vol}")
    if fields["pii_involved"]:
        iocs.append("PII/sensitive data involved — GDPR/regulatory notification may be required")
    if fields["persistence_detected"]:
        iocs.append("Persistence mechanism detected — full environment clean required before recovery")
    if fields["lateral_movement"]:
        iocs.append("Lateral movement observed — scope extends beyond initial compromise point")
    if fields["affected_data_stores"]:
        iocs.append(f"Affected data stores: {', '.join(fields['affected_data_stores'][:5])}")
    if fields["affected_hosts_count"] > 1:
        iocs.append(f"{fields['affected_hosts_count']} hosts affected")
    if not iocs:
        iocs.append("No confirmed exfiltration or persistence — investigation ongoing")
    return iocs


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    source_credibility = float(fact.get("source_credibility", 0.80))
    fields = parse_forensic_fields(fact)

    dwell_severity, dwell_note = assess_dwell_severity(fields["dwell_time_hours"])
    ioc_summary = build_ioc_summary(fields)

    # Determine overall severity
    severity_rank = {"low": 0, "medium": 1, "high": 2, "critical": 3, "unknown": 1}
    rank = severity_rank.get(dwell_severity, 1)
    if fields["exfiltration_confirmed"]:
        rank = max(rank, 3)  # critical
    elif fields["persistence_detected"] or fields["lateral_movement"]:
        rank = max(rank, 2)  # high

    severity_labels = ["low", "medium", "high", "critical"]
    final_severity = severity_labels[min(rank, 3)]

    is_critical = final_severity == "critical"
    is_high = final_severity == "high"
    confidence = round(min(source_credibility * (0.92 if fields["exfiltration_confirmed"] else 0.78), 0.96), 3)

    # Regulatory notification requirement
    requires_notification = bool(fields["pii_involved"] and fields["exfiltration_confirmed"])

    output = {
        "analysis_type": "forensics_pre_analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "dwell_time_hours": fields["dwell_time_hours"],
        "dwell_severity_assessment": dwell_severity,
        "dwell_note": dwell_note,
        "exfiltration_confirmed": fields["exfiltration_confirmed"],
        "exfil_volume_gb": fields["exfil_volume_gb"],
        "pii_involved": fields["pii_involved"],
        "persistence_detected": fields["persistence_detected"],
        "lateral_movement": fields["lateral_movement"],
        "initial_access_vector": fields["initial_access_vector"],
        "affected_data_stores": fields["affected_data_stores"],
        "affected_hosts_count": fields["affected_hosts_count"],
        "ioc_summary": ioc_summary,
        "inferred_severity": final_severity,
        "confidence": confidence,
        "requires_regulatory_notification": requires_notification,
        "evidence_preservation_priority": EVIDENCE_SOURCES[:5],
        "chain_of_custody_steps": CHAIN_OF_CUSTODY_STEPS,
        "intent_type": "mutating" if is_critical or is_high else "read_only",
        "mutating_category": "remediation_action" if is_critical else None,
        "regulatory_note": (
            "PII exfiltration confirmed. GDPR Article 33 requires DPA notification within 72 hours. "
            "HIPAA requires HHS notification within 60 days for PHI breach."
            if requires_notification else
            "No confirmed PII exfiltration. Continue investigation before regulatory determination."
        ),
    }

    print(json.dumps(output))

    if is_critical:
        return 2
    if is_high:
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
