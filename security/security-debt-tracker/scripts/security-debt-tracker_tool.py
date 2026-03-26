#!/usr/bin/env python3
"""
security-debt-tracker_tool.py

Analyzes aging security findings to compute SLA breach counts, debt accumulation
rate, and debt bucket classification (current / overdue / critical_debt).

Exit codes:
  0 — Debt stable (no overdue items, accumulation_rate <= 0)
  1 — Debt accumulating (overdue items present OR positive accumulation rate)
  2 — Critical debt (critical/high finding with SLA breached 2x+)

Usage:
  python security-debt-tracker_tool.py --output json
  python security-debt-tracker_tool.py --input findings.json --output json
  echo '{"findings": [...]}' | python security-debt-tracker_tool.py
"""

import argparse
import json
import sys
from datetime import datetime, timezone

# SLA bands in days keyed by severity (normal, epss_escalated)
SLA_BANDS = {
    "critical": (15, 7),
    "high":     (30, 15),
    "medium":   (60, 30),
    "low":      (90, 60),
}

INVESTMENT_WEIGHTS = {"S": 1, "M": 2, "L": 4}


def classify_finding(finding: dict) -> dict:
    """Add debt_bucket and computed fields to a finding."""
    severity = finding.get("severity", "low").lower()
    age_days = finding.get("age_days", 0)
    epss = finding.get("epss", 0.0)

    normal_sla, escalated_sla = SLA_BANDS.get(severity, (90, 60))
    effective_sla = escalated_sla if epss > 0.5 else normal_sla

    # Override with provided sla_days if present
    sla_days = finding.get("sla_days", effective_sla)

    if age_days < sla_days:
        bucket = "current"
    elif age_days < 2 * sla_days:
        bucket = "overdue"
    else:
        bucket = "critical_debt"

    return {
        **finding,
        "effective_sla_days": sla_days,
        "debt_age_days": age_days,
        "debt_bucket": bucket,
        "sla_breached": age_days >= sla_days,
    }


def compute_accumulation_rate(findings: list) -> float:
    """Compute net new findings per week over the last 30 days."""
    now = datetime.now(timezone.utc)
    new_count = 0
    closed_count = 0

    for f in findings:
        opened_str = f.get("opened_date", "")
        closed_str = f.get("closed_date", "")

        if opened_str:
            try:
                opened = datetime.fromisoformat(opened_str.replace("Z", "+00:00"))
                if (now - opened).days <= 30:
                    new_count += 1
            except ValueError:
                pass

        if closed_str:
            try:
                closed = datetime.fromisoformat(closed_str.replace("Z", "+00:00"))
                if (now - closed).days <= 30:
                    closed_count += 1
            except ValueError:
                pass

    # Per week over 30-day window (30 / 7 ≈ 4.33 weeks)
    weeks = 30 / 7
    return round((new_count - closed_count) / weeks, 2)


def analyze_debt(findings: list) -> dict:
    """Run full debt analysis on a list of findings."""
    classified = [classify_finding(f) for f in findings]

    buckets = {"current": [], "overdue": [], "critical_debt": []}
    for f in classified:
        buckets[f["debt_bucket"]].append(f)

    current_count = len(buckets["current"])
    overdue_count = len(buckets["overdue"])
    critical_debt_count = len(buckets["critical_debt"])
    total = len(classified)

    sla_breach_count = sum(1 for f in classified if f["sla_breached"])
    sla_breach_rate = round(sla_breach_count / total * 100, 1) if total > 0 else 0.0

    critical_unmitigated = [
        f for f in classified
        if f["debt_bucket"] == "critical_debt"
        and f.get("severity", "").lower() in ("critical", "high")
    ]

    accumulation_rate = compute_accumulation_rate(findings)

    # Determine exit code
    if critical_unmitigated:
        exit_code = 2
        exit_code_meaning = "critical"
        severity = "critical"
    elif overdue_count > 0 or accumulation_rate > 0:
        exit_code = 1
        exit_code_meaning = "accumulating"
        severity = "high" if overdue_count > 0 else "medium"
    else:
        exit_code = 0
        exit_code_meaning = "stable"
        severity = "informational"

    accumulation_direction = (
        "growing" if accumulation_rate > 0
        else "reducing" if accumulation_rate < 0
        else "stable"
    )

    key_findings = []
    if critical_unmitigated:
        key_findings.append(
            f"{len(critical_unmitigated)} critical/high finding(s) with SLA breached 2x+ — exit code 2"
        )
    if sla_breach_count > 0:
        key_findings.append(f"SLA breach count: {sla_breach_count} ({sla_breach_rate}% of total findings)")
    if accumulation_rate != 0:
        key_findings.append(
            f"Debt accumulation rate: {accumulation_rate:+.2f} net new findings/week ({accumulation_direction})"
        )
    if not key_findings:
        key_findings.append(
            f"All {total} finding(s) within SLA; accumulation rate stable. Debt health: GOOD."
        )

    # Routing
    next_agents = []
    if critical_unmitigated:
        next_agents.append("cs-security-analyst")
        next_agents.append("ciso-brief-generator")
    if exit_code >= 1:
        next_agents.append("vulnerability-management")
    if not next_agents:
        next_agents = []

    return {
        "agent_slug": "security-debt-tracker",
        "intent_type": "analyze",
        "action": (
            "Immediately route critical_debt findings to cs-security-analyst and ciso-brief-generator"
            if exit_code == 2
            else "Accelerate remediation for overdue findings via vulnerability-management"
            if exit_code == 1
            else "Debt stable — document clean digest; no routing required"
        ),
        "rationale": (
            f"Security debt analysis of {total} finding(s): "
            f"{current_count} current, {overdue_count} overdue, {critical_debt_count} critical_debt"
        ),
        "confidence": 0.90 if total > 0 else 0.50,
        "severity": severity,
        "key_findings": key_findings,
        "evidence_references": [],
        "debt_summary": {
            "total_findings": total,
            "current_count": current_count,
            "overdue_count": overdue_count,
            "critical_debt_count": critical_debt_count,
            "sla_breach_count": sla_breach_count,
            "sla_breach_rate_pct": sla_breach_rate,
            "critical_unmitigated": [
                {"id": f.get("id"), "severity": f.get("severity"), "age_days": f.get("age_days")}
                for f in critical_unmitigated
            ],
            "accumulation_rate": accumulation_rate,
            "accumulation_direction": accumulation_direction,
        },
        "debt_buckets": {
            "current": [f.get("id") for f in buckets["current"]],
            "overdue": [f.get("id") for f in buckets["overdue"]],
            "critical_debt": [f.get("id") for f in buckets["critical_debt"]],
        },
        "exit_code": exit_code,
        "exit_code_meaning": exit_code_meaning,
        "next_agents": next_agents,
        "human_approval_required": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def load_input(args) -> list:
    """Load findings from --input file, stdin, or return empty list."""
    raw = None

    if args.input:
        with open(args.input, "r") as fh:
            raw = json.load(fh)
    elif not sys.stdin.isatty():
        raw = json.load(sys.stdin)

    if raw is None:
        return []

    # Accept either a top-level list or {"findings": [...]}
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict):
        return raw.get("findings", [])

    return []


def main():
    parser = argparse.ArgumentParser(
        description="Security Debt Tracker — analyze aging findings and SLA breach status"
    )
    parser.add_argument(
        "--input", "-i",
        help="Path to findings JSON file (list or {findings:[...]})",
    )
    parser.add_argument(
        "--output", "-o",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    findings = load_input(args)
    result = analyze_debt(findings)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Security Debt Tracker — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"Total findings analyzed: {result['debt_summary']['total_findings']}")
        print(f"  Current (within SLA):  {result['debt_summary']['current_count']}")
        print(f"  Overdue:               {result['debt_summary']['overdue_count']}")
        print(f"  Critical Debt (2x SLA): {result['debt_summary']['critical_debt_count']}")
        print(f"SLA breach count: {result['debt_summary']['sla_breach_count']} ({result['debt_summary']['sla_breach_rate_pct']}%)")
        print(f"Critical unmitigated: {len(result['debt_summary']['critical_unmitigated'])}")
        print(f"Accumulation rate: {result['debt_summary']['accumulation_rate']:+.2f} net new/week ({result['debt_summary']['accumulation_direction']})")
        print(f"Exit code: {result['exit_code']} ({result['exit_code_meaning']})")
        print()
        for finding in result["key_findings"]:
            print(f"  - {finding}")

    sys.exit(result["exit_code"])


if __name__ == "__main__":
    main()
