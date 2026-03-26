#!/usr/bin/env python3
"""
pre_analysis.py — Zero-Day Response Pre-Analysis

Reads a SecurityFact JSON from stdin, assesses zero-day exposure based on
patch availability, exploitation status, and internal system exposure.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result
exit:   0=monitoring, 1=high urgency, 2=critical/active exploitation
"""


import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


COMPENSATING_CONTROLS: Dict[str, List[str]] = {
    "network": [
        "Block inbound traffic to affected service at perimeter firewall",
        "Enable enhanced network monitoring for exploitation signatures",
        "Isolate affected system to dedicated VLAN",
    ],
    "web": [
        "Deploy WAF rule to block known exploit payloads",
        "Disable affected feature/endpoint until patch available",
        "Enable rate limiting and request inspection",
    ],
    "memory": [
        "Enable exploit mitigation flags (ASLR, DEP, NX bit)",
        "Consider process isolation or sandboxing",
        "Monitor for unusual memory access patterns",
    ],
    "authentication": [
        "Force MFA for all access to affected system",
        "Revoke and rotate all credentials for affected service",
        "Enable enhanced authentication logging",
    ],
    "default": [
        "Increase monitoring and alerting thresholds for affected systems",
        "Restrict access to known-good principals only",
        "Prepare rollback plan for when patch becomes available",
        "Enable enhanced endpoint detection on affected hosts",
    ],
}


def extract_zero_day_fields(fact: Dict[str, Any]) -> Dict[str, Any]:
    payload = fact.get("raw_payload", {})
    if not isinstance(payload, dict):
        payload = {}

    patch_available = _parse_bool(payload.get("patch_available") or payload.get("fix_available"))
    exploitation_observed = _parse_bool(
        payload.get("exploitation_observed")
        or payload.get("actively_exploited")
        or payload.get("in_the_wild")
        or payload.get("exploitation_in_wild")
    )
    cisa_kev = _parse_bool(payload.get("cisa_kev") or payload.get("in_kev"))
    affected_internal_systems = int(
        payload.get("affected_internal_systems")
        or payload.get("affected_systems")
        or payload.get("affected_hosts")
        or 0
    )
    vulnerability_type = str(payload.get("vulnerability_type") or payload.get("vuln_type") or "unknown").lower()
    affected_vendor = str(payload.get("vendor") or payload.get("affected_vendor") or payload.get("product_vendor") or "unknown")
    affected_product = str(payload.get("product") or payload.get("affected_product") or "unknown")
    cvss_score: Optional[float] = None
    for field in ("cvss_score", "cvss_v3_score", "base_score"):
        val = payload.get(field) or fact.get(field)
        if val is not None:
            try:
                cvss_score = float(val)
                break
            except (ValueError, TypeError):
                continue

    internet_facing = _parse_bool(
        payload.get("internet_facing")
        or payload.get("public_facing")
        or payload.get("external_exposure")
    )

    return {
        "patch_available": patch_available,
        "exploitation_observed": exploitation_observed,
        "cisa_kev": cisa_kev,
        "affected_internal_systems": affected_internal_systems,
        "vulnerability_type": vulnerability_type,
        "affected_vendor": affected_vendor,
        "affected_product": affected_product,
        "cvss_score": cvss_score,
        "internet_facing": internet_facing,
    }


def _parse_bool(val: Any) -> bool:
    if val is None:
        return False
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        return bool(val)
    return str(val).lower() in ("true", "yes", "1", "confirmed", "active")


def assess_urgency(fields: Dict[str, Any]) -> tuple[str, str]:
    if fields["exploitation_observed"] or fields["cisa_kev"]:
        return "CRITICAL — active exploitation confirmed. Implement compensating controls immediately.", "critical"
    if not fields["patch_available"] and fields["affected_internal_systems"] > 0:
        return "HIGH — no patch available and internal systems affected. Deploy compensating controls.", "high"
    if not fields["patch_available"] and fields["internet_facing"]:
        return "HIGH — no patch and internet-facing systems exposed. Restrict access immediately.", "high"
    if fields["cvss_score"] is not None and fields["cvss_score"] >= 9.0:
        return "HIGH — critical CVSS with no patch. Monitor threat intelligence channels for exploit PoC.", "high"
    return "MEDIUM — monitoring phase. Track vendor advisories and threat intel feeds.", "medium"


def select_controls(vulnerability_type: str) -> List[str]:
    for key in COMPENSATING_CONTROLS:
        if key in vulnerability_type:
            return COMPENSATING_CONTROLS[key]
    return COMPENSATING_CONTROLS["default"]


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    source_credibility = float(fact.get("source_credibility", 0.80))
    fields = extract_zero_day_fields(fact)
    urgency_message, severity = assess_urgency(fields)
    compensating_controls = select_controls(fields["vulnerability_type"])

    is_critical = severity == "critical"
    is_high = severity == "high"
    confidence = round(min(source_credibility * (0.95 if fields["exploitation_observed"] else 0.80), 0.97), 3)

    output = {
        "analysis_type": "zero_day_response_pre_analysis",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "patch_available": fields["patch_available"],
        "exploitation_observed": fields["exploitation_observed"],
        "cisa_kev_listed": fields["cisa_kev"],
        "affected_internal_systems": fields["affected_internal_systems"],
        "internet_facing": fields["internet_facing"],
        "vulnerability_type": fields["vulnerability_type"],
        "affected_vendor": fields["affected_vendor"],
        "affected_product": fields["affected_product"],
        "cvss_score": fields["cvss_score"],
        "inferred_severity": severity,
        "urgency_assessment": urgency_message,
        "recommended_compensating_controls": compensating_controls,
        "confidence": confidence,
        "intent_type": "mutating" if is_critical or is_high else "read_only",
        "mutating_category": "remediation_action" if is_critical or is_high else None,
        "patch_status_note": (
            "Patch available — prioritise deployment in emergency change window."
            if fields["patch_available"] else
            "No patch available — compensating controls are the only mitigation. "
            "Subscribe to vendor security advisories for patch release notification."
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
