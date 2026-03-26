#!/usr/bin/env python3
"""
security-roadmap-planner_tool.py

Builds an investment-prioritized 12-month security program roadmap from posture,
risk, and compliance input data. Every roadmap item is traced to a specific gap
or risk finding. Items are sorted by risk-reduction-per-dollar (priority_score)
and bucketed into Q1–Q4 with overflow in backlog.

Usage:
  python security-roadmap-planner_tool.py --output json
  python security-roadmap-planner_tool.py --input posture.json --output json
  python security-roadmap-planner_tool.py \
    --input posture.json \
    --risk-input risk.json \
    --compliance-input compliance.json \
    --output json
"""

import argparse
import json
import sys
from datetime import datetime, timezone

# Investment band weights (relative cost multiplier for priority scoring)
INVESTMENT_WEIGHTS = {"S": 1, "M": 2, "L": 4}

# Quarterly capacity (max initiatives per quarter)
QUARTER_CAPACITY = {"Q1": 3, "Q2": 4, "Q3": 4, "Q4": 3}

# Domain score threshold below which a gap initiative is generated
POSTURE_GAP_THRESHOLD = 65


def load_json_file(path: str) -> dict:
    """Load a JSON file safely."""
    try:
        with open(path, "r") as fh:
            return json.load(fh)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"[WARN] Could not load {path}: {exc}", file=sys.stderr)
        return {}


def extract_posture_gaps(posture_data: dict) -> list:
    """Extract initiative candidates from posture domain scores."""
    initiatives = []
    domain_scores = posture_data.get("domain_scores", {})
    if not domain_scores:
        # Try common alternate key names
        domain_scores = posture_data.get("domains", {})

    for domain, score in domain_scores.items():
        if isinstance(score, (int, float)) and score < POSTURE_GAP_THRESHOLD:
            gap = POSTURE_GAP_THRESHOLD - score
            risk_reduction = min(100, int(gap * 1.5))  # proportional estimate
            investment = "M" if gap > 20 else "S"
            initiatives.append({
                "initiative": f"Improve {domain} security domain coverage",
                "addresses_gap": f"{domain} posture score {score}/100 — below {POSTURE_GAP_THRESHOLD} threshold",
                "gap_source": "posture_score",
                "risk_reduction_score": risk_reduction,
                "investment_band": investment,
                "owner_role": "Security Manager",
                "success_metric": f"{domain} domain score >= {POSTURE_GAP_THRESHOLD} by end of assigned quarter",
            })

    return initiatives


def extract_risk_initiatives(risk_data: dict) -> list:
    """Extract initiative candidates from enterprise risk assessment output."""
    initiatives = []
    top_risks = risk_data.get("top_risks", [])
    risk_appetite = risk_data.get("risk_appetite", float("inf"))

    for risk in top_risks:
        ale = risk.get("ale", 0) or risk.get("annual_loss_expectancy", 0)
        if ale > risk_appetite:
            risk_name = risk.get("name", risk.get("risk_id", "Unnamed Risk"))
            risk_reduction = min(100, int((ale / max(risk_appetite, 1)) * 40))
            initiatives.append({
                "initiative": f"Mitigate {risk_name}",
                "addresses_gap": f"ALE ${ale:,.0f} exceeds risk appetite ${risk_appetite:,.0f}",
                "gap_source": "enterprise_risk",
                "risk_reduction_score": risk_reduction,
                "investment_band": "L" if ale > risk_appetite * 3 else "M",
                "owner_role": "CISO",
                "success_metric": f"ALE reduced below risk appetite threshold of ${risk_appetite:,.0f}",
            })

    return initiatives


def extract_compliance_initiatives(compliance_data: dict) -> list:
    """Extract initiative candidates from compliance gap data."""
    initiatives = []
    gaps = compliance_data.get("gaps", compliance_data.get("compliance_gaps", []))

    for gap in gaps:
        framework = gap.get("framework", "regulatory")
        control = gap.get("control", gap.get("requirement", "Unknown control"))
        deadline = gap.get("deadline", gap.get("regulatory_deadline", ""))
        # Compliance gaps have moderate fixed risk reduction estimate
        risk_reduction = 55
        initiatives.append({
            "initiative": f"Remediate {framework} gap: {control}",
            "addresses_gap": f"Compliance gap in {framework} — {control}",
            "gap_source": "compliance",
            "risk_reduction_score": risk_reduction,
            "investment_band": "S",
            "owner_role": "Compliance Officer",
            "success_metric": f"{framework} gap closed; control {control} implemented",
            "regulatory_deadline": deadline,
        })

    return initiatives


def compute_priority_score(initiative: dict) -> float:
    """Compute risk-reduction-per-dollar proxy score."""
    risk_reduction = initiative.get("risk_reduction_score", 0)
    weight = INVESTMENT_WEIGHTS.get(initiative.get("investment_band", "M"), 2)
    return round(risk_reduction / weight, 2)


def assign_quarters(initiatives: list) -> list:
    """Sort by priority_score desc and assign to quarterly buckets."""
    # Add priority scores
    for item in initiatives:
        item["priority_score"] = compute_priority_score(item)

    # Sort descending by priority score
    sorted_items = sorted(initiatives, key=lambda x: x["priority_score"], reverse=True)

    # Assign quarters
    quarter_counts = {q: 0 for q in QUARTER_CAPACITY}
    for item in sorted_items:
        assigned = False
        for quarter in ["Q1", "Q2", "Q3", "Q4"]:
            if quarter_counts[quarter] < QUARTER_CAPACITY[quarter]:
                item["quarter"] = quarter
                quarter_counts[quarter] += 1
                assigned = True
                break
        if not assigned:
            item["quarter"] = "backlog"

    return sorted_items


def build_investment_summary(roadmap_items: list) -> dict:
    """Build per-quarter investment summary."""
    summary = {
        q: {"initiatives": 0, "bands": []}
        for q in ["Q1", "Q2", "Q3", "Q4", "backlog"]
    }
    for item in roadmap_items:
        q = item.get("quarter", "backlog")
        if q in summary:
            summary[q]["initiatives"] += 1
            band = item.get("investment_band", "M")
            if band not in summary[q]["bands"]:
                summary[q]["bands"].append(band)
    return summary


def determine_confidence(has_posture: bool, has_risk: bool, has_compliance: bool) -> float:
    """Determine output confidence based on available inputs."""
    if has_posture and has_risk and has_compliance:
        return 0.90
    if has_posture and has_risk:
        return 0.80
    if has_posture:
        return 0.60
    return 0.40


def build_roadmap(posture_data: dict, risk_data: dict, compliance_data: dict) -> dict:
    """Build the full roadmap output."""
    has_posture = bool(posture_data)
    has_risk = bool(risk_data)
    has_compliance = bool(compliance_data)

    initiatives = []
    data_notes = []

    if has_posture:
        initiatives.extend(extract_posture_gaps(posture_data))
    else:
        data_notes.append("Posture score data unavailable — roadmap quality significantly reduced")

    if has_risk:
        initiatives.extend(extract_risk_initiatives(risk_data))
    else:
        data_notes.append("Enterprise risk data unavailable — confidence capped at 0.60")

    if has_compliance:
        initiatives.extend(extract_compliance_initiatives(compliance_data))
    else:
        data_notes.append("Compliance gap data unavailable — regulatory deadlines not included")

    if not initiatives:
        # Produce minimal output when no data available
        initiatives = [{
            "initiative": "Run security posture assessment to baseline program gaps",
            "addresses_gap": "No posture, risk, or compliance data provided",
            "gap_source": "meta",
            "risk_reduction_score": 80,
            "investment_band": "S",
            "priority_score": 80.0,
            "quarter": "Q1",
            "owner_role": "Security Manager",
            "success_metric": "Posture score baseline established",
        }]

    roadmap_items = assign_quarters(initiatives)
    investment_summary = build_investment_summary(roadmap_items)
    confidence = determine_confidence(has_posture, has_risk, has_compliance)

    # Key findings
    key_findings = []
    if roadmap_items:
        q1_items = [i for i in roadmap_items if i.get("quarter") == "Q1"]
        key_findings.append(
            f"{len(roadmap_items)} initiatives identified across {len([q for q in ['Q1','Q2','Q3','Q4'] if investment_summary[q]['initiatives'] > 0])} quarters"
        )
        if q1_items:
            key_findings.append(
                f"Q1 quick wins ({len(q1_items)} initiatives): {', '.join(i['initiative'][:50] for i in q1_items[:2])}"
            )
    for note in data_notes:
        key_findings.append(f"DATA GAP: {note}")

    # Posture summary line for rationale
    posture_score = posture_data.get("overall_score", posture_data.get("composite_score", "N/A"))
    total_ale = risk_data.get("total_ale", "N/A")
    gap_count = len(compliance_data.get("gaps", compliance_data.get("compliance_gaps", [])))
    rationale = (
        f"Roadmap derived from posture score {posture_score}, "
        f"enterprise risk ALE {total_ale}, "
        f"and {gap_count} compliance gap(s). "
        f"All {len(roadmap_items)} initiative(s) are traceable to a specific gap or risk finding."
    )

    return {
        "agent_slug": "security-roadmap-planner",
        "intent_type": "advise",
        "action": "Implement the 12-month security program roadmap as prioritized below",
        "rationale": rationale,
        "confidence": confidence,
        "severity": "informational",
        "key_findings": key_findings,
        "evidence_references": [],
        "roadmap_items": roadmap_items,
        "investment_summary": investment_summary,
        "data_availability": {
            "posture_score": has_posture,
            "enterprise_risk": has_risk,
            "compliance_gaps": has_compliance,
        },
        "data_notes": data_notes,
        "next_agents": ["ciso-brief-generator", "metrics-reporting"],
        "human_approval_required": False,
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(
        description="Security Roadmap Planner — build investment-prioritized 12-month security roadmap"
    )
    parser.add_argument(
        "--input", "-i",
        help="Path to posture score JSON file",
    )
    parser.add_argument(
        "--risk-input",
        help="Path to enterprise risk assessment JSON file",
    )
    parser.add_argument(
        "--compliance-input",
        help="Path to compliance mapping JSON file",
    )
    parser.add_argument(
        "--output", "-o",
        choices=["json", "text"],
        default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    posture_data = load_json_file(args.input) if args.input else {}
    risk_data = load_json_file(args.risk_input) if args.risk_input else {}
    compliance_data = load_json_file(args.compliance_input) if args.compliance_input else {}

    result = build_roadmap(posture_data, risk_data, compliance_data)

    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"Security Roadmap Planner — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        print(f"Confidence: {result['confidence']:.0%}")
        print(f"Total initiatives: {len(result['roadmap_items'])}")
        print()
        for q in ["Q1", "Q2", "Q3", "Q4", "backlog"]:
            q_items = [i for i in result["roadmap_items"] if i.get("quarter") == q]
            if q_items:
                print(f"  {q} ({len(q_items)} initiatives):")
                for item in q_items:
                    print(f"    [{item['investment_band']}] score={item['priority_score']} — {item['initiative']}")
        if result["data_notes"]:
            print()
            print("Data gaps:")
            for note in result["data_notes"]:
                print(f"  - {note}")

    sys.exit(0)


if __name__ == "__main__":
    main()
