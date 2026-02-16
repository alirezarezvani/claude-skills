#!/usr/bin/env python3
"""
Severity Classifier - Classify incident severity and generate escalation paths.

Analyses incident data across multiple dimensions (revenue impact, user scope,
data/security risk, service criticality, blast radius) to produce a weighted
severity score and map it to SEV1-SEV4.  Generates escalation paths, on-call
routing, SLA impact assessments, and immediate action plans.

Table of Contents:
    SeverityLevel         - Enum-like severity definitions (SEV1-SEV4)
    ImpactAssessment      - Parsed impact data from incident input
    SeverityScore         - Multi-dimensional weighted scoring result
    EscalationPath        - Generated escalation routing and timelines
    ActionPlan            - Recommended immediate actions per severity
    SLAImpact             - SLA breach risk and error-budget assessment

    parse_incident_data() - Validate and normalise raw JSON input
    compute_dimension_scores() - Score each weighted dimension
    classify_severity()   - Map composite score to SEV1-SEV4
    build_escalation_path() - Generate escalation routing
    build_action_plan()   - Generate immediate action checklist
    assess_sla_impact()   - SLA breach risk assessment
    format_text()         - Human-readable text output
    format_json()         - Machine-readable JSON output
    format_markdown()     - Markdown report output
    main()                - CLI entry point

Usage:
    python severity_classifier.py incident.json
    python severity_classifier.py incident.json --format json
    python severity_classifier.py incident.json --format markdown
    cat incident.json | python severity_classifier.py --format text
    echo '{"incident":{...}}' | python severity_classifier.py
"""

import argparse
import json
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ---------- Severity Level Definitions ----------------------------------------

class SeverityLevel:
    """Enum-like container for SEV1 through SEV4 definitions."""

    SEV1 = "SEV1"
    SEV2 = "SEV2"
    SEV3 = "SEV3"
    SEV4 = "SEV4"

    DEFINITIONS: Dict[str, Dict[str, Any]] = {
        "SEV1": {
            "label": "Critical",
            "description": (
                "Complete service outage, confirmed data loss or corruption, "
                "active security breach, or more than 50% of users affected."
            ),
            "score_threshold": 0.75,
            "response_time_minutes": 5,
            "update_cadence_minutes": 15,
            "executive_notify": True,
            "war_room": True,
        },
        "SEV2": {
            "label": "Major",
            "description": (
                "Significant service degradation, more than 25% of users "
                "affected, no viable workaround, or high revenue impact."
            ),
            "score_threshold": 0.50,
            "response_time_minutes": 15,
            "update_cadence_minutes": 30,
            "executive_notify": False,
            "war_room": True,
        },
        "SEV3": {
            "label": "Moderate",
            "description": (
                "Partial degradation with workaround available, fewer than "
                "25% of users affected, limited blast radius."
            ),
            "score_threshold": 0.25,
            "response_time_minutes": 30,
            "update_cadence_minutes": 60,
            "executive_notify": False,
            "war_room": False,
        },
        "SEV4": {
            "label": "Minor",
            "description": (
                "Cosmetic issue, low impact, minimal user effect, "
                "informational or non-urgent."
            ),
            "score_threshold": 0.0,
            "response_time_minutes": 120,
            "update_cadence_minutes": 240,
            "executive_notify": False,
            "war_room": False,
        },
    }

    @classmethod
    def from_score(cls, score: float) -> str:
        """Return the severity level string for a given composite score."""
        for level in [cls.SEV1, cls.SEV2, cls.SEV3]:
            if score >= cls.DEFINITIONS[level]["score_threshold"]:
                return level
        return cls.SEV4

    @classmethod
    def get_definition(cls, level: str) -> Dict[str, Any]:
        return cls.DEFINITIONS.get(level, cls.DEFINITIONS[cls.SEV4])


# ---------- Configuration Constants -------------------------------------------

DIMENSION_WEIGHTS: Dict[str, float] = {
    "revenue_impact": 0.25,
    "user_impact_scope": 0.25,
    "data_security_risk": 0.20,
    "service_criticality": 0.15,
    "blast_radius": 0.15,
}

REVENUE_IMPACT_SCORES: Dict[str, float] = {
    "critical": 1.0,
    "high": 0.8,
    "medium": 0.5,
    "low": 0.2,
    "none": 0.0,
}

DEGRADATION_SCORES: Dict[str, float] = {
    "complete": 1.0,
    "major": 0.75,
    "partial": 0.50,
    "minor": 0.25,
    "none": 0.0,
}

ERROR_RATE_THRESHOLDS: List[Tuple[float, float]] = [
    (50.0, 1.0),
    (25.0, 0.8),
    (10.0, 0.6),
    (5.0, 0.4),
    (1.0, 0.2),
]

LATENCY_P99_THRESHOLDS_MS: List[Tuple[float, float]] = [
    (10000, 1.0),
    (5000, 0.8),
    (2000, 0.6),
    (1000, 0.4),
    (500, 0.2),
]

SLA_TIERS: Dict[str, Dict[str, Any]] = {
    "SEV1": {
        "target_resolution_hours": 1,
        "target_response_minutes": 5,
        "sla_percentage": 99.95,
        "monthly_error_budget_minutes": 21.6,
    },
    "SEV2": {
        "target_resolution_hours": 4,
        "target_response_minutes": 15,
        "sla_percentage": 99.9,
        "monthly_error_budget_minutes": 43.2,
    },
    "SEV3": {
        "target_resolution_hours": 24,
        "target_response_minutes": 60,
        "sla_percentage": 99.5,
        "monthly_error_budget_minutes": 216.0,
    },
    "SEV4": {
        "target_resolution_hours": 72,
        "target_response_minutes": 480,
        "sla_percentage": 99.0,
        "monthly_error_budget_minutes": 432.0,
    },
}

ESCALATION_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "SEV1": {
        "initial_notify": ["on-call-primary", "on-call-secondary", "engineering-manager"],
        "escalate_after_minutes": 15,
        "escalate_to": ["vp-engineering", "cto"],
        "bridge_required": True,
        "status_page_update": True,
        "customer_comms": True,
    },
    "SEV2": {
        "initial_notify": ["on-call-primary", "on-call-secondary"],
        "escalate_after_minutes": 30,
        "escalate_to": ["engineering-manager"],
        "bridge_required": True,
        "status_page_update": True,
        "customer_comms": False,
    },
    "SEV3": {
        "initial_notify": ["on-call-primary"],
        "escalate_after_minutes": 120,
        "escalate_to": ["on-call-secondary"],
        "bridge_required": False,
        "status_page_update": False,
        "customer_comms": False,
    },
    "SEV4": {
        "initial_notify": ["on-call-primary"],
        "escalate_after_minutes": 480,
        "escalate_to": [],
        "bridge_required": False,
        "status_page_update": False,
        "customer_comms": False,
    },
}


# ---------- Data Model Classes ------------------------------------------------

@dataclass
class ImpactAssessment:
    """Parsed and normalised impact data from incident input."""

    revenue_impact: str = "none"
    affected_users_percentage: float = 0.0
    affected_regions: List[str] = field(default_factory=list)
    data_integrity_risk: bool = False
    security_breach: bool = False
    customer_facing: bool = False
    degradation_type: str = "none"
    workaround_available: bool = True


@dataclass
class SeverityScore:
    """Multi-dimensional scoring result with per-dimension breakdown."""

    composite_score: float = 0.0
    severity_level: str = SeverityLevel.SEV4
    dimensions: Dict[str, float] = field(default_factory=dict)
    weighted_dimensions: Dict[str, float] = field(default_factory=dict)
    contributing_factors: List[str] = field(default_factory=list)
    auto_escalate_reasons: List[str] = field(default_factory=list)


@dataclass
class EscalationPath:
    """Generated escalation routing and notification schedule."""

    severity_level: str = SeverityLevel.SEV4
    immediate_notify: List[str] = field(default_factory=list)
    escalation_chain: List[Dict[str, Any]] = field(default_factory=list)
    cross_team_notify: List[str] = field(default_factory=list)
    war_room_required: bool = False
    bridge_link: str = ""
    status_page_update: bool = False
    customer_comms_required: bool = False
    suggested_smes: List[str] = field(default_factory=list)


@dataclass
class ActionPlan:
    """Recommended immediate actions checklist for the incident."""

    severity_level: str = SeverityLevel.SEV4
    immediate_actions: List[str] = field(default_factory=list)
    diagnostic_steps: List[str] = field(default_factory=list)
    communication_actions: List[str] = field(default_factory=list)
    rollback_assessment: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SLAImpact:
    """SLA breach risk and error-budget assessment."""

    severity_level: str = SeverityLevel.SEV4
    sla_tier: Dict[str, Any] = field(default_factory=dict)
    breach_risk: str = "low"
    error_budget_impact_minutes: float = 0.0
    remaining_budget_percentage: float = 100.0
    estimated_time_to_breach_minutes: float = 0.0
    recommendations: List[str] = field(default_factory=list)


# ---------- Input Parsing -----------------------------------------------------

def parse_incident_data(raw: Dict[str, Any]) -> Tuple[Dict, ImpactAssessment, Dict, Dict]:
    """
    Validate and normalise raw JSON input into typed structures.

    Returns:
        (incident_info, impact_assessment, signals, context)
    """
    incident = raw.get("incident", {})
    if not incident:
        raise ValueError("Input must contain an 'incident' key with title and description.")

    impact_raw = raw.get("impact", {})
    impact = ImpactAssessment(
        revenue_impact=impact_raw.get("revenue_impact", "none"),
        affected_users_percentage=float(impact_raw.get("affected_users_percentage", 0)),
        affected_regions=impact_raw.get("affected_regions", []),
        data_integrity_risk=bool(impact_raw.get("data_integrity_risk", False)),
        security_breach=bool(impact_raw.get("security_breach", False)),
        customer_facing=bool(impact_raw.get("customer_facing", False)),
        degradation_type=impact_raw.get("degradation_type", "none"),
        workaround_available=bool(impact_raw.get("workaround_available", True)),
    )

    signals = raw.get("signals", {})
    context = raw.get("context", {})

    return incident, impact, signals, context


# ---------- Core Scoring Engine -----------------------------------------------

def _score_revenue_impact(impact: ImpactAssessment) -> Tuple[float, List[str]]:
    """Score the revenue impact dimension (0.0 - 1.0)."""
    factors: List[str] = []
    score = REVENUE_IMPACT_SCORES.get(impact.revenue_impact, 0.0)

    if impact.customer_facing and score >= 0.5:
        score = min(1.0, score + 0.1)
        factors.append("Customer-facing service with revenue exposure")

    if not impact.workaround_available and score >= 0.5:
        score = min(1.0, score + 0.1)
        factors.append("No workaround available, prolonging revenue impact")

    if score >= 0.8:
        factors.append(f"Revenue impact rated '{impact.revenue_impact}'")

    return score, factors


def _score_user_impact(impact: ImpactAssessment, signals: Dict) -> Tuple[float, List[str]]:
    """Score the user impact scope dimension (0.0 - 1.0)."""
    factors: List[str] = []
    pct = impact.affected_users_percentage

    if pct >= 75:
        score = 1.0
    elif pct >= 50:
        score = 0.85
    elif pct >= 25:
        score = 0.65
    elif pct >= 10:
        score = 0.45
    elif pct >= 1:
        score = 0.25
    else:
        score = 0.1

    if pct > 0:
        factors.append(f"{pct}% of users affected")

    customer_reports = signals.get("customer_reports", 0)
    if customer_reports > 20:
        score = min(1.0, score + 0.15)
        factors.append(f"{customer_reports} customer reports received")
    elif customer_reports > 5:
        score = min(1.0, score + 0.08)
        factors.append(f"{customer_reports} customer reports received")

    degradation_boost = DEGRADATION_SCORES.get(impact.degradation_type, 0.0) * 0.15
    score = min(1.0, score + degradation_boost)
    if impact.degradation_type in ("complete", "major"):
        factors.append(f"Degradation type: {impact.degradation_type}")

    return score, factors


def _score_data_security(impact: ImpactAssessment) -> Tuple[float, List[str]]:
    """Score the data/security risk dimension (0.0 - 1.0)."""
    factors: List[str] = []
    score = 0.0

    if impact.security_breach:
        score = 1.0
        factors.append("Active security breach confirmed")
    elif impact.data_integrity_risk:
        score = 0.8
        factors.append("Data integrity at risk")

    if impact.customer_facing and impact.data_integrity_risk:
        score = min(1.0, score + 0.1)
        factors.append("Customer data potentially affected")

    return score, factors


def _score_service_criticality(signals: Dict, context: Dict) -> Tuple[float, List[str]]:
    """Score service criticality based on signals and dependency graph."""
    factors: List[str] = []
    score = 0.0

    dependent_services = signals.get("dependent_services", [])
    dep_count = len(dependent_services)
    if dep_count >= 5:
        score = 1.0
        factors.append(f"{dep_count} dependent services (critical hub)")
    elif dep_count >= 3:
        score = 0.75
        factors.append(f"{dep_count} dependent services")
    elif dep_count >= 1:
        score = 0.5
        factors.append(f"{dep_count} dependent service(s)")
    else:
        score = 0.2

    affected_endpoints = signals.get("affected_endpoints", [])
    if len(affected_endpoints) >= 5:
        score = min(1.0, score + 0.15)
        factors.append(f"{len(affected_endpoints)} endpoints affected")
    elif len(affected_endpoints) >= 2:
        score = min(1.0, score + 0.08)
        factors.append(f"{len(affected_endpoints)} endpoints affected")

    return score, factors


def _score_blast_radius(
    impact: ImpactAssessment, signals: Dict
) -> Tuple[float, List[str]]:
    """Score blast radius from region spread, alert volume, and error rate."""
    factors: List[str] = []
    score = 0.0

    region_count = len(impact.affected_regions)
    if region_count >= 3:
        score = 0.9
        factors.append(f"Spanning {region_count} regions")
    elif region_count == 2:
        score = 0.6
        factors.append(f"Spanning {region_count} regions")
    elif region_count == 1:
        score = 0.3

    error_rate = signals.get("error_rate_percentage", 0.0)
    for threshold, rate_score in ERROR_RATE_THRESHOLDS:
        if error_rate >= threshold:
            score = max(score, rate_score)
            factors.append(f"Error rate at {error_rate}%")
            break

    latency = signals.get("latency_p99_ms", 0)
    for threshold, lat_score in LATENCY_P99_THRESHOLDS_MS:
        if latency >= threshold:
            score = max(score, lat_score)
            factors.append(f"P99 latency at {latency}ms")
            break

    alert_count = signals.get("alert_count", 0)
    if alert_count >= 20:
        score = min(1.0, score + 0.15)
        factors.append(f"{alert_count} alerts firing")
    elif alert_count >= 10:
        score = min(1.0, score + 0.08)
        factors.append(f"{alert_count} alerts firing")

    return score, factors


def compute_dimension_scores(
    impact: ImpactAssessment, signals: Dict, context: Dict
) -> SeverityScore:
    """Score each weighted dimension and produce a composite severity score."""
    dimensions: Dict[str, float] = {}
    weighted: Dict[str, float] = {}
    all_factors: List[str] = []
    auto_escalate: List[str] = []

    # -- Revenue impact --
    rev_score, rev_factors = _score_revenue_impact(impact)
    dimensions["revenue_impact"] = round(rev_score, 3)
    weighted["revenue_impact"] = round(rev_score * DIMENSION_WEIGHTS["revenue_impact"], 3)
    all_factors.extend(rev_factors)

    # -- User impact scope --
    user_score, user_factors = _score_user_impact(impact, signals)
    dimensions["user_impact_scope"] = round(user_score, 3)
    weighted["user_impact_scope"] = round(user_score * DIMENSION_WEIGHTS["user_impact_scope"], 3)
    all_factors.extend(user_factors)

    # -- Data / security risk --
    sec_score, sec_factors = _score_data_security(impact)
    dimensions["data_security_risk"] = round(sec_score, 3)
    weighted["data_security_risk"] = round(sec_score * DIMENSION_WEIGHTS["data_security_risk"], 3)
    all_factors.extend(sec_factors)

    # -- Service criticality --
    svc_score, svc_factors = _score_service_criticality(signals, context)
    dimensions["service_criticality"] = round(svc_score, 3)
    weighted["service_criticality"] = round(svc_score * DIMENSION_WEIGHTS["service_criticality"], 3)
    all_factors.extend(svc_factors)

    # -- Blast radius --
    blast_score, blast_factors = _score_blast_radius(impact, signals)
    dimensions["blast_radius"] = round(blast_score, 3)
    weighted["blast_radius"] = round(blast_score * DIMENSION_WEIGHTS["blast_radius"], 3)
    all_factors.extend(blast_factors)

    composite = sum(weighted.values())

    # -- Auto-escalation overrides --
    if impact.security_breach:
        composite = max(composite, 0.85)
        auto_escalate.append("Security breach triggers automatic SEV1 escalation")
    if impact.data_integrity_risk and impact.customer_facing:
        composite = max(composite, 0.76)
        auto_escalate.append("Customer-facing data integrity risk triggers SEV1 floor")
    if impact.affected_users_percentage >= 50 and impact.degradation_type == "complete":
        composite = max(composite, 0.80)
        auto_escalate.append("Complete outage affecting 50%+ users triggers SEV1 floor")

    composite = min(1.0, round(composite, 3))
    severity_level = SeverityLevel.from_score(composite)

    return SeverityScore(
        composite_score=composite,
        severity_level=severity_level,
        dimensions=dimensions,
        weighted_dimensions=weighted,
        contributing_factors=all_factors,
        auto_escalate_reasons=auto_escalate,
    )


# ---------- Classification Wrapper --------------------------------------------

def classify_severity(
    incident: Dict, impact: ImpactAssessment, signals: Dict, context: Dict
) -> SeverityScore:
    """
    Top-level classification: compute scores and return the final
    SeverityScore including the resolved severity level.
    """
    return compute_dimension_scores(impact, signals, context)


# ---------- Escalation Path Builder -------------------------------------------

def build_escalation_path(
    severity_score: SeverityScore,
    signals: Dict,
    context: Dict,
) -> EscalationPath:
    """Generate the escalation routing based on severity and context."""
    level = severity_score.severity_level
    template = ESCALATION_TEMPLATES.get(level, ESCALATION_TEMPLATES["SEV4"])

    on_call = context.get("on_call", {})
    primary = on_call.get("primary", "on-call-primary@company.com")
    secondary = on_call.get("secondary", "on-call-secondary@company.com")

    immediate: List[str] = []
    for role in template["initial_notify"]:
        if role == "on-call-primary":
            immediate.append(primary)
        elif role == "on-call-secondary":
            immediate.append(secondary)
        else:
            immediate.append(role)

    chain: List[Dict[str, Any]] = []
    if template["escalate_to"]:
        chain.append({
            "trigger_after_minutes": template["escalate_after_minutes"],
            "notify": template["escalate_to"],
            "reason": f"No resolution within {template['escalate_after_minutes']} minutes",
        })

    sev_def = SeverityLevel.get_definition(level)
    if sev_def.get("executive_notify"):
        chain.append({
            "trigger_after_minutes": 15,
            "notify": ["vp-engineering", "cto"],
            "reason": "SEV1 executive notification policy",
        })

    cross_team: List[str] = []
    dependent_services = signals.get("dependent_services", [])
    for svc in dependent_services:
        cross_team.append(f"{svc}-team")

    suggested_smes: List[str] = []
    affected_endpoints = signals.get("affected_endpoints", [])
    if affected_endpoints:
        suggested_smes.append(f"API owner for: {', '.join(affected_endpoints[:3])}")
    if dependent_services:
        suggested_smes.append(f"Service owners: {', '.join(dependent_services[:3])}")

    ongoing = context.get("ongoing_incidents", [])
    if ongoing:
        suggested_smes.append("Incident coordinator (multiple active incidents)")

    bridge_link = ""
    if template["bridge_required"]:
        bridge_link = f"https://bridge.company.com/incident-{level.lower()}"

    return EscalationPath(
        severity_level=level,
        immediate_notify=immediate,
        escalation_chain=chain,
        cross_team_notify=cross_team,
        war_room_required=template["bridge_required"],
        bridge_link=bridge_link,
        status_page_update=template["status_page_update"],
        customer_comms_required=template.get("customer_comms", False),
        suggested_smes=suggested_smes,
    )


# ---------- Action Plan Builder -----------------------------------------------

def build_action_plan(
    severity_score: SeverityScore,
    incident: Dict,
    impact: ImpactAssessment,
    signals: Dict,
    context: Dict,
) -> ActionPlan:
    """Generate the immediate action plan for the classified incident."""
    level = severity_score.severity_level
    sev_def = SeverityLevel.get_definition(level)

    # -- Immediate actions --
    immediate: List[str] = [
        f"Acknowledge incident within {sev_def['response_time_minutes']} minutes",
        "Join the war room / bridge call" if sev_def["war_room"] else "Open incident channel",
        f"Post status update every {sev_def['update_cadence_minutes']} minutes",
    ]

    if level in (SeverityLevel.SEV1, SeverityLevel.SEV2):
        immediate.append("Page secondary on-call if primary unresponsive within 5 minutes")
        immediate.append("Begin impact quantification for executive update")

    if impact.security_breach:
        immediate.insert(0, "CRITICAL: Initiate security incident response playbook")
        immediate.append("Engage security team immediately")
        immediate.append("Preserve forensic evidence -- do not restart services yet")

    if impact.data_integrity_risk:
        immediate.append("Halt writes to affected data stores if safe to do so")
        immediate.append("Begin data integrity verification")

    # -- Diagnostic steps --
    diagnostics: List[str] = [
        "Check service dashboards and recent metric trends",
        "Review application logs for error spikes",
        "Verify upstream and downstream dependency health",
    ]

    error_rate = signals.get("error_rate_percentage", 0)
    if error_rate > 10:
        diagnostics.append(f"Investigate error rate spike ({error_rate}%)")

    latency = signals.get("latency_p99_ms", 0)
    if latency > 2000:
        diagnostics.append(f"Investigate latency degradation (P99 = {latency}ms)")

    affected_endpoints = signals.get("affected_endpoints", [])
    if affected_endpoints:
        diagnostics.append(
            f"Trace requests to affected endpoints: {', '.join(affected_endpoints[:5])}"
        )

    dependent_services = signals.get("dependent_services", [])
    if dependent_services:
        diagnostics.append(
            f"Check health of dependent services: {', '.join(dependent_services)}"
        )

    # -- Communication actions --
    comms: List[str] = []
    if sev_def.get("executive_notify"):
        comms.append("Draft executive summary within 15 minutes")
    if level in (SeverityLevel.SEV1, SeverityLevel.SEV2):
        comms.append("Post initial status page update")
        comms.append("Notify customer success team for proactive outreach")
    comms.append(f"Schedule post-incident review within 48 hours")

    # -- Rollback assessment --
    recent_deploys = context.get("recent_deployments", [])
    rollback: Dict[str, Any] = {"recent_deployment_detected": False, "recommendation": ""}

    if recent_deploys:
        latest = recent_deploys[0]
        rollback["recent_deployment_detected"] = True
        rollback["service"] = latest.get("service", "unknown")
        rollback["version"] = latest.get("version", "unknown")
        rollback["deployed_at"] = latest.get("deployed_at", "unknown")

        detected_at = incident.get("detected_at", "")
        deploy_time = latest.get("deployed_at", "")
        if detected_at and deploy_time:
            try:
                det = datetime.fromisoformat(detected_at.replace("Z", "+00:00"))
                dep = datetime.fromisoformat(deploy_time.replace("Z", "+00:00"))
                delta_minutes = (det - dep).total_seconds() / 60
                rollback["minutes_since_deploy"] = round(delta_minutes, 1)
                if 0 < delta_minutes < 120:
                    rollback["recommendation"] = (
                        f"STRONG: Deployment of {latest.get('service')} v{latest.get('version')} "
                        f"occurred {round(delta_minutes)} minutes before detection. "
                        "Consider immediate rollback."
                    )
                else:
                    rollback["recommendation"] = (
                        "Recent deployment is outside the typical correlation window. "
                        "Investigate other root causes first."
                    )
            except (ValueError, TypeError):
                rollback["recommendation"] = (
                    "Unable to parse timestamps. Manually assess deployment correlation."
                )
    else:
        rollback["recommendation"] = (
            "No recent deployments detected. Focus on infrastructure and dependency investigation."
        )

    return ActionPlan(
        severity_level=level,
        immediate_actions=immediate,
        diagnostic_steps=diagnostics,
        communication_actions=comms,
        rollback_assessment=rollback,
    )


# ---------- SLA Impact Assessment ---------------------------------------------

def assess_sla_impact(
    severity_score: SeverityScore,
    impact: ImpactAssessment,
    signals: Dict,
) -> SLAImpact:
    """Calculate SLA breach risk and error-budget consumption."""
    level = severity_score.severity_level
    tier = SLA_TIERS.get(level, SLA_TIERS["SEV4"])

    # Estimate ongoing burn rate (minutes of budget consumed per real minute)
    user_pct = impact.affected_users_percentage / 100.0
    degradation_factor = DEGRADATION_SCORES.get(impact.degradation_type, 0.25)
    burn_rate = user_pct * degradation_factor
    if burn_rate <= 0:
        burn_rate = 0.01  # minimum if incident is open

    monthly_budget = tier["monthly_error_budget_minutes"]

    # Assume 30% of budget already consumed this month for conservative estimate
    assumed_consumed_pct = 30.0
    remaining_budget = monthly_budget * (1 - assumed_consumed_pct / 100.0)

    if burn_rate > 0:
        time_to_breach = remaining_budget / burn_rate
    else:
        time_to_breach = float("inf")

    # Classify breach risk
    if time_to_breach <= 30:
        breach_risk = "critical"
    elif time_to_breach <= 120:
        breach_risk = "high"
    elif time_to_breach <= 480:
        breach_risk = "medium"
    else:
        breach_risk = "low"

    budget_impact_per_hour = burn_rate * 60
    error_budget_impact = round(budget_impact_per_hour, 2)

    remaining_pct = round(
        max(0.0, (remaining_budget / monthly_budget) * 100.0), 1
    )

    recommendations: List[str] = []
    if breach_risk == "critical":
        recommendations.append(
            "SLA breach imminent. Prioritize resolution above all other work."
        )
        recommendations.append(
            "Prepare customer communication about potential SLA credit."
        )
    elif breach_risk == "high":
        recommendations.append(
            "SLA breach likely within hours. Escalate to ensure rapid resolution."
        )
    elif breach_risk == "medium":
        recommendations.append(
            "Monitor error budget consumption. Resolve before end of business."
        )
    else:
        recommendations.append(
            "SLA impact is contained. Continue standard incident response."
        )

    recommendations.append(
        f"Current burn rate: {round(burn_rate * 100, 1)}% of error budget per minute"
    )
    recommendations.append(
        f"Estimated time to SLA breach: {round(time_to_breach, 0)} minutes "
        f"({round(time_to_breach / 60, 1)} hours)"
    )

    return SLAImpact(
        severity_level=level,
        sla_tier=tier,
        breach_risk=breach_risk,
        error_budget_impact_minutes=error_budget_impact,
        remaining_budget_percentage=remaining_pct,
        estimated_time_to_breach_minutes=round(time_to_breach, 1),
        recommendations=recommendations,
    )


# ---------- Output Formatters -------------------------------------------------

def _header_line(char: str, width: int = 72) -> str:
    return char * width


def format_text(
    incident: Dict,
    severity_score: SeverityScore,
    escalation: EscalationPath,
    action_plan: ActionPlan,
    sla_impact: SLAImpact,
) -> str:
    """Render a human-readable text report."""
    lines: List[str] = []
    w = 72

    lines.append(_header_line("=", w))
    lines.append("INCIDENT SEVERITY CLASSIFICATION REPORT")
    lines.append(_header_line("=", w))
    lines.append("")

    # -- Incident Summary --
    lines.append(f"Title:       {incident.get('title', 'N/A')}")
    lines.append(f"Service:     {incident.get('service', 'N/A')}")
    lines.append(f"Detected:    {incident.get('detected_at', 'N/A')}")
    lines.append(f"Reporter:    {incident.get('reporter', 'N/A')}")
    lines.append("")

    # -- Severity --
    sev_def = SeverityLevel.get_definition(severity_score.severity_level)
    lines.append(_header_line("-", w))
    lines.append(f"SEVERITY: {severity_score.severity_level} ({sev_def['label']})")
    lines.append(f"Composite Score: {severity_score.composite_score:.3f}")
    lines.append(_header_line("-", w))
    lines.append(f"  {sev_def['description']}")
    lines.append("")

    # -- Dimension Breakdown --
    lines.append("Dimension Scores:")
    for dim, raw in severity_score.dimensions.items():
        wt = severity_score.weighted_dimensions.get(dim, 0)
        weight_cfg = DIMENSION_WEIGHTS.get(dim, 0)
        label = dim.replace("_", " ").title()
        lines.append(f"  {label:<25s}  raw={raw:.3f}  weight={weight_cfg:.2f}  weighted={wt:.3f}")
    lines.append("")

    if severity_score.contributing_factors:
        lines.append("Contributing Factors:")
        for f in severity_score.contributing_factors:
            lines.append(f"  - {f}")
        lines.append("")

    if severity_score.auto_escalate_reasons:
        lines.append("Auto-Escalation Overrides:")
        for r in severity_score.auto_escalate_reasons:
            lines.append(f"  * {r}")
        lines.append("")

    # -- Escalation Path --
    lines.append(_header_line("-", w))
    lines.append("ESCALATION PATH")
    lines.append(_header_line("-", w))
    lines.append(f"Immediate Notify: {', '.join(escalation.immediate_notify)}")
    if escalation.war_room_required:
        lines.append(f"War Room:         Required ({escalation.bridge_link})")
    else:
        lines.append("War Room:         Not required")
    lines.append(f"Status Page:      {'Update required' if escalation.status_page_update else 'No update needed'}")
    lines.append(f"Customer Comms:   {'Required' if escalation.customer_comms_required else 'Not required'}")
    lines.append("")

    if escalation.escalation_chain:
        lines.append("Escalation Chain:")
        for step in escalation.escalation_chain:
            lines.append(
                f"  After {step['trigger_after_minutes']}min -> "
                f"Notify: {', '.join(step['notify'])} ({step['reason']})"
            )
        lines.append("")

    if escalation.cross_team_notify:
        lines.append(f"Cross-Team Notify: {', '.join(escalation.cross_team_notify)}")
    if escalation.suggested_smes:
        lines.append("Suggested SMEs:")
        for sme in escalation.suggested_smes:
            lines.append(f"  - {sme}")
    lines.append("")

    # -- Action Plan --
    lines.append(_header_line("-", w))
    lines.append("ACTION PLAN")
    lines.append(_header_line("-", w))

    lines.append("Immediate Actions:")
    for i, action in enumerate(action_plan.immediate_actions, 1):
        lines.append(f"  {i}. {action}")
    lines.append("")

    lines.append("Diagnostic Steps:")
    for i, step in enumerate(action_plan.diagnostic_steps, 1):
        lines.append(f"  {i}. {step}")
    lines.append("")

    lines.append("Communication Actions:")
    for i, action in enumerate(action_plan.communication_actions, 1):
        lines.append(f"  {i}. {action}")
    lines.append("")

    rb = action_plan.rollback_assessment
    lines.append("Rollback Assessment:")
    if rb.get("recent_deployment_detected"):
        lines.append(f"  Recent Deploy: {rb.get('service', '?')} v{rb.get('version', '?')}")
        lines.append(f"  Deployed At:   {rb.get('deployed_at', '?')}")
        if "minutes_since_deploy" in rb:
            lines.append(f"  Minutes Before Detection: {rb['minutes_since_deploy']}")
    lines.append(f"  Recommendation: {rb.get('recommendation', 'N/A')}")
    lines.append("")

    # -- SLA Impact --
    lines.append(_header_line("-", w))
    lines.append("SLA IMPACT ASSESSMENT")
    lines.append(_header_line("-", w))
    lines.append(f"Breach Risk:              {sla_impact.breach_risk.upper()}")
    lines.append(f"Error Budget Impact:      {sla_impact.error_budget_impact_minutes} min/hr")
    lines.append(f"Remaining Budget:         {sla_impact.remaining_budget_percentage}%")
    lines.append(f"Est. Time to Breach:      {sla_impact.estimated_time_to_breach_minutes} min")
    tier = sla_impact.sla_tier
    lines.append(f"Target Resolution:        {tier.get('target_resolution_hours', '?')} hours")
    lines.append(f"Target Response:          {tier.get('target_response_minutes', '?')} minutes")
    lines.append("")

    if sla_impact.recommendations:
        lines.append("SLA Recommendations:")
        for rec in sla_impact.recommendations:
            lines.append(f"  - {rec}")
    lines.append("")
    lines.append(_header_line("=", w))

    return "\n".join(lines)


def format_json(
    incident: Dict,
    severity_score: SeverityScore,
    escalation: EscalationPath,
    action_plan: ActionPlan,
    sla_impact: SLAImpact,
) -> str:
    """Render a machine-readable JSON report."""
    report = {
        "classification_timestamp": datetime.now(timezone.utc).isoformat(),
        "incident": incident,
        "severity": asdict(severity_score),
        "severity_definition": SeverityLevel.get_definition(severity_score.severity_level),
        "escalation": asdict(escalation),
        "action_plan": asdict(action_plan),
        "sla_impact": asdict(sla_impact),
    }
    return json.dumps(report, indent=2, default=str)


def format_markdown(
    incident: Dict,
    severity_score: SeverityScore,
    escalation: EscalationPath,
    action_plan: ActionPlan,
    sla_impact: SLAImpact,
) -> str:
    """Render a Markdown report suitable for incident tickets or wikis."""
    lines: List[str] = []
    sev_def = SeverityLevel.get_definition(severity_score.severity_level)

    lines.append(f"# Incident Severity Classification: {severity_score.severity_level}")
    lines.append("")
    lines.append(f"**Classified:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    lines.append("")

    lines.append("## Incident Summary")
    lines.append("")
    lines.append(f"| Field | Value |")
    lines.append(f"|-------|-------|")
    lines.append(f"| Title | {incident.get('title', 'N/A')} |")
    lines.append(f"| Service | {incident.get('service', 'N/A')} |")
    lines.append(f"| Detected | {incident.get('detected_at', 'N/A')} |")
    lines.append(f"| Reporter | {incident.get('reporter', 'N/A')} |")
    lines.append("")

    lines.append("## Severity Classification")
    lines.append("")
    lines.append(
        f"> **{severity_score.severity_level} -- {sev_def['label']}** "
        f"(Score: {severity_score.composite_score:.3f})"
    )
    lines.append(f">")
    lines.append(f"> {sev_def['description']}")
    lines.append("")

    lines.append("### Dimension Scores")
    lines.append("")
    lines.append("| Dimension | Raw | Weight | Weighted |")
    lines.append("|-----------|-----|--------|----------|")
    for dim, raw in severity_score.dimensions.items():
        wt = severity_score.weighted_dimensions.get(dim, 0)
        weight_cfg = DIMENSION_WEIGHTS.get(dim, 0)
        label = dim.replace("_", " ").title()
        lines.append(f"| {label} | {raw:.3f} | {weight_cfg:.2f} | {wt:.3f} |")
    lines.append("")

    if severity_score.contributing_factors:
        lines.append("### Contributing Factors")
        lines.append("")
        for f in severity_score.contributing_factors:
            lines.append(f"- {f}")
        lines.append("")

    if severity_score.auto_escalate_reasons:
        lines.append("### Auto-Escalation Overrides")
        lines.append("")
        for r in severity_score.auto_escalate_reasons:
            lines.append(f"- **{r}**")
        lines.append("")

    lines.append("## Escalation Path")
    lines.append("")
    lines.append(f"**Immediate Notify:** {', '.join(escalation.immediate_notify)}")
    lines.append("")

    if escalation.war_room_required:
        lines.append(f"**War Room:** [Join Bridge]({escalation.bridge_link})")
    else:
        lines.append("**War Room:** Not required")
    lines.append("")

    if escalation.escalation_chain:
        lines.append("### Escalation Chain")
        lines.append("")
        for step in escalation.escalation_chain:
            lines.append(
                f"- **After {step['trigger_after_minutes']} min:** "
                f"Notify {', '.join(step['notify'])} -- {step['reason']}"
            )
        lines.append("")

    if escalation.cross_team_notify:
        lines.append(f"**Cross-Team:** {', '.join(escalation.cross_team_notify)}")
        lines.append("")

    if escalation.suggested_smes:
        lines.append("### Suggested SMEs")
        lines.append("")
        for sme in escalation.suggested_smes:
            lines.append(f"- {sme}")
        lines.append("")

    lines.append("## Action Plan")
    lines.append("")

    lines.append("### Immediate Actions")
    lines.append("")
    for i, action in enumerate(action_plan.immediate_actions, 1):
        lines.append(f"{i}. {action}")
    lines.append("")

    lines.append("### Diagnostic Steps")
    lines.append("")
    for i, step in enumerate(action_plan.diagnostic_steps, 1):
        lines.append(f"{i}. {step}")
    lines.append("")

    lines.append("### Communication")
    lines.append("")
    for i, action in enumerate(action_plan.communication_actions, 1):
        lines.append(f"{i}. {action}")
    lines.append("")

    rb = action_plan.rollback_assessment
    lines.append("### Rollback Assessment")
    lines.append("")
    if rb.get("recent_deployment_detected"):
        lines.append(
            f"| Deploy | {rb.get('service', '?')} v{rb.get('version', '?')} |"
        )
        lines.append(f"|--------|------|")
        lines.append(f"| Deployed At | {rb.get('deployed_at', '?')} |")
        if "minutes_since_deploy" in rb:
            lines.append(f"| Minutes Before Detection | {rb['minutes_since_deploy']} |")
        lines.append("")
    lines.append(f"**Recommendation:** {rb.get('recommendation', 'N/A')}")
    lines.append("")

    lines.append("## SLA Impact")
    lines.append("")
    tier = sla_impact.sla_tier
    lines.append(f"| Metric | Value |")
    lines.append(f"|--------|-------|")
    lines.append(f"| Breach Risk | **{sla_impact.breach_risk.upper()}** |")
    lines.append(f"| Error Budget Impact | {sla_impact.error_budget_impact_minutes} min/hr |")
    lines.append(f"| Remaining Budget | {sla_impact.remaining_budget_percentage}% |")
    lines.append(f"| Est. Time to Breach | {sla_impact.estimated_time_to_breach_minutes} min |")
    lines.append(f"| Target Resolution | {tier.get('target_resolution_hours', '?')} hours |")
    lines.append(f"| Target Response | {tier.get('target_response_minutes', '?')} minutes |")
    lines.append("")

    if sla_impact.recommendations:
        lines.append("### SLA Recommendations")
        lines.append("")
        for rec in sla_impact.recommendations:
            lines.append(f"- {rec}")
        lines.append("")

    lines.append("---")
    lines.append("*Generated by severity_classifier.py*")

    return "\n".join(lines)


# ---------- CLI Entry Point ---------------------------------------------------

def main() -> None:
    """Parse arguments, read input, classify, and emit output."""
    parser = argparse.ArgumentParser(
        description="Classify incident severity and generate escalation paths.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
examples:
  %(prog)s incident.json
  %(prog)s incident.json --format json
  %(prog)s incident.json --format markdown
  cat incident.json | %(prog)s
  cat incident.json | %(prog)s --format json
""",
    )

    parser.add_argument(
        "data_file",
        nargs="?",
        default=None,
        help="JSON file with incident data (reads stdin if omitted)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "markdown"],
        default="text",
        dest="output_format",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # -- Read input --
    try:
        if args.data_file:
            with open(args.data_file, "r", encoding="utf-8") as fh:
                raw_data = json.load(fh)
        else:
            if sys.stdin.isatty():
                parser.error("No input file provided and stdin is a terminal. Pipe JSON or pass a file.")
            raw_data = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(f"Error: invalid JSON input -- {exc}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print(f"Error: file not found -- {args.data_file}", file=sys.stderr)
        sys.exit(1)
    except IOError as exc:
        print(f"Error: could not read input -- {exc}", file=sys.stderr)
        sys.exit(1)

    # -- Parse and validate --
    try:
        incident, impact, signals, context = parse_incident_data(raw_data)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # -- Classify --
    severity_score = classify_severity(incident, impact, signals, context)

    # -- Build outputs --
    escalation = build_escalation_path(severity_score, signals, context)
    action_plan = build_action_plan(severity_score, incident, impact, signals, context)
    sla_impact = assess_sla_impact(severity_score, impact, signals)

    # -- Format and print --
    if args.output_format == "json":
        output = format_json(incident, severity_score, escalation, action_plan, sla_impact)
    elif args.output_format == "markdown":
        output = format_markdown(incident, severity_score, escalation, action_plan, sla_impact)
    else:
        output = format_text(incident, severity_score, escalation, action_plan, sla_impact)

    print(output)

    # -- Exit code reflects severity --
    if severity_score.severity_level == SeverityLevel.SEV1:
        sys.exit(2)
    elif severity_score.severity_level == SeverityLevel.SEV2:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
