#!/usr/bin/env python3
"""
Postmortem Generator - Generate structured postmortem reports with 5-Whys analysis.

Produces comprehensive incident postmortem documents from structured JSON input,
including root cause analysis, contributing factor classification, action item
validation, MTTD/MTTR metrics, and customer impact summaries.

Usage:
    python postmortem_generator.py incident_data.json
    python postmortem_generator.py incident_data.json --format markdown
    python postmortem_generator.py incident_data.json --format json
    cat incident_data.json | python postmortem_generator.py

Input:
    JSON object with keys: incident, timeline, resolution, action_items, participants.
    See SKILL.md for the full input schema.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ---------- Constants and Configuration ----------

VERSION = "1.0.0"
SEVERITY_ORDER = {"SEV0": 0, "SEV1": 1, "SEV2": 2, "SEV3": 3, "SEV4": 4}
FACTOR_CATEGORIES = ("process", "tooling", "human", "environment", "external")
ACTION_TYPES = ("detection", "prevention", "mitigation", "process")
PRIORITY_ORDER = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
POSTMORTEM_TARGET_HOURS = 72

# Industry benchmarks for incident response (minutes, except postmortem)
BENCHMARKS = {
    "SEV0": {"mttd": 5, "mttr": 60, "mitigate": 30, "declare": 5},
    "SEV1": {"mttd": 10, "mttr": 120, "mitigate": 60, "declare": 10},
    "SEV2": {"mttd": 30, "mttr": 480, "mitigate": 120, "declare": 30},
    "SEV3": {"mttd": 60, "mttr": 1440, "mitigate": 240, "declare": 60},
    "SEV4": {"mttd": 120, "mttr": 2880, "mitigate": 480, "declare": 120},
}

CAT_TO_ACTION = {"process": "process", "tooling": "detection", "human": "prevention",
                 "environment": "mitigation", "external": "prevention"}
CAT_WEIGHT = {"process": 1.0, "tooling": 0.9, "human": 0.8, "environment": 0.7, "external": 0.6}

# Keywords used to classify contributing factors into categories
FACTOR_KEYWORDS = {
    "process": ["process", "procedure", "workflow", "review", "approval", "checklist",
                 "runbook", "documentation", "policy", "standard", "protocol", "canary",
                 "deployment", "rollback", "change management"],
    "tooling": ["tool", "monitor", "alert", "threshold", "automation", "test", "pipeline",
                "ci/cd", "observability", "dashboard", "logging", "infrastructure",
                "configuration", "config"],
    "human": ["training", "knowledge", "experience", "communication", "handoff", "fatigue",
              "oversight", "mistake", "error", "misunderstand", "assumption", "awareness"],
    "environment": ["load", "traffic", "scale", "capacity", "resource", "network", "hardware",
                    "region", "latency", "timeout", "connection", "performance", "spike"],
    "external": ["vendor", "third-party", "upstream", "downstream", "provider", "api",
                 "dependency", "partner", "dns", "cdn", "certificate"],
}

# 5-Whys templates per category (each list is 5 why->answer steps)
WHY_TEMPLATES = {
    "process": [
        "Why did this process gap exist? -> The existing process did not account for this scenario.",
        "Why was the scenario not accounted for? -> It was not identified during the last process review.",
        "Why was the process review incomplete? -> Reviews focus on known failure modes, not emerging risks.",
        "Why are emerging risks not surfaced? -> No systematic mechanism to capture lessons from near-misses.",
        "Why is there no near-miss capture mechanism? -> Incident learning is ad-hoc rather than systematic."],
    "tooling": [
        "Why did the tooling fail to catch this? -> The relevant metric was not monitored or the threshold was misconfigured.",
        "Why was the threshold misconfigured? -> It was set during initial deployment and never revisited.",
        "Why was it never revisited? -> There is no scheduled review of monitoring configurations.",
        "Why is there no scheduled review? -> Monitoring ownership is diffuse across teams.",
        "Why is ownership diffuse? -> No clear operational runbook assigns monitoring review responsibilities."],
    "human": [
        "Why did the human factor contribute? -> The individual lacked context needed to prevent the issue.",
        "Why was context lacking? -> Knowledge was siloed and not documented accessibly.",
        "Why was knowledge siloed? -> No structured onboarding or knowledge-sharing process for this area.",
        "Why is there no knowledge-sharing process? -> Team capacity has been focused on feature delivery.",
        "Why is capacity skewed toward features? -> Operational excellence is not weighted equally in planning."],
    "environment": [
        "Why did the environment cause this failure? -> System capacity was insufficient for the load pattern.",
        "Why was capacity insufficient? -> Load projections did not account for this traffic pattern.",
        "Why were projections inaccurate? -> Load testing does not replicate production-scale variability.",
        "Why doesn't load testing replicate production? -> Test environments lack realistic traffic generators.",
        "Why are traffic generators missing? -> Investment in production-like test infrastructure was deferred."],
    "external": [
        "Why did the external factor cause an incident? -> The system had a hard dependency with no fallback.",
        "Why was there no fallback? -> The integration was assumed to be highly available.",
        "Why was high availability assumed? -> SLA review of the external dependency was not performed.",
        "Why was SLA review skipped? -> No standard checklist for evaluating third-party dependencies.",
        "Why is there no evaluation checklist? -> Vendor management practices are informal and undocumented."],
}

THEME_RECS = {
    "process": ["Establish a quarterly process review cadence covering change management and deployment procedures.",
                "Implement a near-miss tracking system to surface latent risks before they become incidents.",
                "Create pre-deployment checklists that require sign-off from the service owner."],
    "tooling": ["Schedule quarterly reviews of alerting thresholds and monitoring coverage.",
                "Assign explicit monitoring ownership per service in operational runbooks.",
                "Invest in synthetic monitoring and canary analysis for critical paths."],
    "human": ["Build structured onboarding that covers incident-prone areas and past postmortems.",
              "Implement blameless knowledge-sharing sessions after each incident.",
              "Balance operational excellence work alongside feature delivery in sprint planning."],
    "environment": ["Conduct periodic capacity planning reviews using production traffic replays.",
                    "Invest in production-like load-testing infrastructure with realistic traffic profiles.",
                    "Implement auto-scaling policies with validated upper-bound thresholds."],
    "external": ["Perform formal SLA reviews for all third-party dependencies annually.",
                 "Implement circuit breakers and fallbacks for external service integrations.",
                 "Maintain a dependency registry with risk ratings and contingency plans."],
}

MISSING_ACTION_TEMPLATES = {
    "process": "Create or update runbook/checklist to prevent recurrence of this process gap",
    "detection": "Add monitoring and alerting to detect this class of issue earlier",
    "mitigation": "Implement auto-scaling or circuit-breaker to reduce blast radius",
    "prevention": "Add automated safeguards (canary deploy, load test gate) to prevent recurrence",
}


# ---------- Data Model Classes ----------

class IncidentData:
    """Parsed incident metadata."""
    def __init__(self, data: Dict[str, Any]) -> None:
        self.id: str = data.get("id", "UNKNOWN")
        self.title: str = data.get("title", "Untitled Incident")
        self.severity: str = data.get("severity", "SEV3").upper()
        self.commander: str = data.get("commander", "Unassigned")
        self.service: str = data.get("service", "unknown-service")
        self.affected_services: List[str] = data.get("affected_services", [])

    def to_dict(self) -> Dict[str, Any]:
        return {"id": self.id, "title": self.title, "severity": self.severity,
                "commander": self.commander, "service": self.service,
                "affected_services": self.affected_services}


class TimelineMetrics:
    """MTTD, MTTR, and other timing metrics computed from raw timestamps."""
    def __init__(self, timeline: Dict[str, str], severity: str) -> None:
        self.severity = severity
        self.issue_started = self._parse(timeline.get("issue_started"))
        self.detected_at = self._parse(timeline.get("detected_at"))
        self.declared_at = self._parse(timeline.get("declared_at"))
        self.mitigated_at = self._parse(timeline.get("mitigated_at"))
        self.resolved_at = self._parse(timeline.get("resolved_at"))
        self.postmortem_at = self._parse(timeline.get("postmortem_at"))

    @staticmethod
    def _parse(ts: Optional[str]) -> Optional[datetime]:
        if ts is None:
            return None
        for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S"):
            try:
                dt = datetime.strptime(ts, fmt)
                return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
            except ValueError:
                continue
        return None

    def _delta_min(self, start: Optional[datetime], end: Optional[datetime]) -> Optional[float]:
        if start is None or end is None:
            return None
        return round((end - start).total_seconds() / 60.0, 1)

    @property
    def mttd(self) -> Optional[float]:
        return self._delta_min(self.issue_started, self.detected_at)

    @property
    def mttr(self) -> Optional[float]:
        return self._delta_min(self.detected_at, self.resolved_at)

    @property
    def time_to_mitigate(self) -> Optional[float]:
        return self._delta_min(self.detected_at, self.mitigated_at)

    @property
    def time_to_declare(self) -> Optional[float]:
        return self._delta_min(self.detected_at, self.declared_at)

    @property
    def postmortem_timeliness_hours(self) -> Optional[float]:
        m = self._delta_min(self.resolved_at, self.postmortem_at)
        return round(m / 60.0, 1) if m is not None else None

    @property
    def postmortem_on_time(self) -> Optional[bool]:
        h = self.postmortem_timeliness_hours
        return h <= POSTMORTEM_TARGET_HOURS if h is not None else None

    def benchmark_comparison(self) -> Dict[str, Dict[str, Any]]:
        bench = BENCHMARKS.get(self.severity, BENCHMARKS["SEV3"])
        results: Dict[str, Dict[str, Any]] = {}
        for name, actual, target in [("mttd", self.mttd, bench["mttd"]),
                                     ("mttr", self.mttr, bench["mttr"]),
                                     ("time_to_mitigate", self.time_to_mitigate, bench["mitigate"]),
                                     ("time_to_declare", self.time_to_declare, bench["declare"])]:
            if actual is not None:
                results[name] = {"actual_minutes": actual, "benchmark_minutes": target,
                                 "met_benchmark": actual <= target,
                                 "delta_minutes": round(actual - target, 1)}
        h = self.postmortem_timeliness_hours
        if h is not None:
            results["postmortem_timeliness"] = {
                "actual_hours": h, "target_hours": POSTMORTEM_TARGET_HOURS,
                "met_target": self.postmortem_on_time, "delta_hours": round(h - POSTMORTEM_TARGET_HOURS, 1)}
        return results

    def to_dict(self) -> Dict[str, Any]:
        return {"mttd_minutes": self.mttd, "mttr_minutes": self.mttr,
                "time_to_mitigate_minutes": self.time_to_mitigate,
                "time_to_declare_minutes": self.time_to_declare,
                "postmortem_timeliness_hours": self.postmortem_timeliness_hours,
                "postmortem_on_time": self.postmortem_on_time,
                "benchmarks": self.benchmark_comparison()}


class ContributingFactor:
    """A classified contributing factor with weight and action-type mapping."""
    def __init__(self, description: str, index: int) -> None:
        self.description = description
        self.index = index
        self.category = self._classify()
        self.weight = round(max(1.0 - index * 0.15, 0.3) * CAT_WEIGHT.get(self.category, 0.8), 2)
        self.mapped_action_type = CAT_TO_ACTION.get(self.category, "process")

    def _classify(self) -> str:
        lower = self.description.lower()
        scores = {cat: sum(1 for kw in kws if kw in lower) for cat, kws in FACTOR_KEYWORDS.items()}
        best = max(scores, key=lambda k: scores[k])
        return best if scores[best] > 0 else "process"

    def to_dict(self) -> Dict[str, Any]:
        return {"description": self.description, "category": self.category,
                "weight": self.weight, "mapped_action_type": self.mapped_action_type}


class FiveWhysAnalysis:
    """Structured 5-Whys chain for a contributing factor."""
    def __init__(self, factor: ContributingFactor) -> None:
        self.factor = factor
        self.systemic_theme: str = factor.category
        self.chain: List[str] = [f"Why? {factor.description}"] + \
            WHY_TEMPLATES.get(factor.category, WHY_TEMPLATES["process"])

    def to_dict(self) -> Dict[str, Any]:
        return {"factor": self.factor.description, "category": self.factor.category,
                "chain": self.chain, "systemic_theme": self.systemic_theme}


class ActionItem:
    """Parsed and validated action item."""
    def __init__(self, data: Dict[str, Any]) -> None:
        self.title: str = data.get("title", "")
        self.owner: str = data.get("owner", "")
        self.priority: str = data.get("priority", "P3")
        self.deadline: str = data.get("deadline", "")
        self.type: str = data.get("type", "process")
        self.status: str = data.get("status", "open")
        self.validation_issues: List[str] = []
        self.quality_score: int = 0
        self._validate()

    def _validate(self) -> None:
        self.validation_issues = []
        if not self.title:
            self.validation_issues.append("Missing title")
        if not self.owner:
            self.validation_issues.append("Missing owner")
        if not self.deadline:
            self.validation_issues.append("Missing deadline")
        if self.priority not in PRIORITY_ORDER:
            self.validation_issues.append(f"Invalid priority: {self.priority}")
        if self.type not in ACTION_TYPES:
            self.validation_issues.append(f"Invalid type: {self.type}")
        self.quality_score = self._score_quality()

    def _score_quality(self) -> int:
        """Score 0-100: specific, measurable, achievable."""
        s = 0
        if len(self.title) > 10: s += 20
        if self.owner: s += 20
        if self.deadline: s += 20
        if self.priority in PRIORITY_ORDER: s += 10
        if self.type in ACTION_TYPES: s += 10
        if any(kw in self.title.lower() for kw in ["%", "threshold", "within", "before",
                                                     "after", "less than", "greater than"]):
            s += 10
        if len(self.title.split()) >= 5: s += 10
        return min(s, 100)

    @property
    def is_valid(self) -> bool:
        return len(self.validation_issues) == 0

    @property
    def is_past_deadline(self) -> bool:
        if not self.deadline or self.status != "open":
            return False
        try:
            dl = datetime.strptime(self.deadline, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > dl
        except ValueError:
            return False

    def to_dict(self) -> Dict[str, Any]:
        return {"title": self.title, "owner": self.owner, "priority": self.priority,
                "deadline": self.deadline, "type": self.type, "status": self.status,
                "is_valid": self.is_valid, "validation_issues": self.validation_issues,
                "quality_score": self.quality_score, "is_past_deadline": self.is_past_deadline}


class PostmortemReport:
    """Complete postmortem document assembled from all analysis components."""

    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.incident = IncidentData(raw.get("incident", {}))
        self.timeline = TimelineMetrics(raw.get("timeline", {}), self.incident.severity)
        self.resolution: Dict[str, Any] = raw.get("resolution", {})
        self.participants: List[Dict[str, str]] = raw.get("participants", [])
        # Derived analysis
        self.contributing_factors = [ContributingFactor(f, i)
                                     for i, f in enumerate(self.resolution.get("contributing_factors", []))]
        self.five_whys = [FiveWhysAnalysis(f) for f in self.contributing_factors]
        self.action_items = [ActionItem(a) for a in raw.get("action_items", [])]
        self.factor_distribution = self._compute_factor_distribution()
        self.coverage_gaps = self._find_coverage_gaps()
        self.suggested_actions = self._suggest_missing_actions()
        self.theme_recommendations = self._build_theme_recommendations()

    def _compute_factor_distribution(self) -> Dict[str, float]:
        dist: Dict[str, float] = {c: 0.0 for c in FACTOR_CATEGORIES}
        total = sum(f.weight for f in self.contributing_factors) or 1.0
        for f in self.contributing_factors:
            dist[f.category] += f.weight
        return {k: round(v / total * 100, 1) for k, v in dist.items()}

    def _find_coverage_gaps(self) -> List[str]:
        factor_cats = {f.category for f in self.contributing_factors}
        action_types = {a.type for a in self.action_items}
        gaps = []
        for cat in factor_cats:
            expected = CAT_TO_ACTION.get(cat)
            if expected and expected not in action_types:
                gaps.append(f"No '{expected}' action item to address '{cat}' contributing factor")
        return gaps

    def _suggest_missing_actions(self) -> List[Dict[str, str]]:
        factor_cats = {f.category for f in self.contributing_factors}
        action_types = {a.type for a in self.action_items}
        suggestions = []
        for cat in factor_cats:
            expected = CAT_TO_ACTION.get(cat)
            if expected and expected not in action_types:
                suggestions.append({
                    "type": expected,
                    "suggestion": MISSING_ACTION_TEMPLATES.get(expected, "Add an action item for this gap"),
                    "reason": f"No action item addresses the '{cat}' contributing factor"})
        return suggestions

    def _build_theme_recommendations(self) -> Dict[str, List[str]]:
        seen: Dict[str, List[str]] = {}
        for a in self.five_whys:
            if a.systemic_theme not in seen:
                seen[a.systemic_theme] = THEME_RECS.get(a.systemic_theme, [])
        return seen

    def customer_impact_summary(self) -> Dict[str, Any]:
        impact = self.resolution.get("customer_impact", {})
        affected = impact.get("affected_users", 0)
        failed_tx = impact.get("failed_transactions", 0)
        revenue = impact.get("revenue_impact_usd", 0)
        data_loss = impact.get("data_loss", False)
        comm_required = affected > 1000 or data_loss or revenue > 10000
        sev = "high" if (affected > 10000 or revenue > 50000) else (
            "medium" if (affected > 1000 or revenue > 5000) else "low")
        return {"affected_users": affected, "failed_transactions": failed_tx,
                "revenue_impact_usd": revenue, "data_loss": data_loss,
                "data_integrity": "compromised" if data_loss else "intact",
                "customer_communication_required": comm_required, "impact_severity": sev}

    def executive_summary(self) -> str:
        mttr = self.timeline.mttr
        ci = self.customer_impact_summary()
        mttr_str = f"{mttr:.0f} minutes" if mttr is not None else "unknown duration"
        parts = [
            f"On {self._fmt_date(self.timeline.issue_started)}, a {self.incident.severity} "
            f"incident (\"{self.incident.title}\") impacted the {self.incident.service} service.",
            f"The root cause was identified as: {self.resolution.get('root_cause', 'Unknown root cause')}.",
            f"The incident was resolved in {mttr_str}, affecting approximately "
            f"{ci['affected_users']:,} users with an estimated revenue impact of ${ci['revenue_impact_usd']:,.2f}.",
            "Data loss was confirmed; affected customers must be notified." if ci["data_loss"]
            else "No data loss occurred during this incident."]
        return " ".join(parts)

    @staticmethod
    def _fmt_date(dt: Optional[datetime]) -> str:
        return dt.strftime("%Y-%m-%d at %H:%M UTC") if dt else "an unknown date"

    def overdue_p1_items(self) -> List[Dict[str, str]]:
        return [{"title": a.title, "owner": a.owner, "deadline": a.deadline}
                for a in self.action_items if a.priority in ("P0", "P1") and a.is_past_deadline]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": VERSION, "incident": self.incident.to_dict(),
            "executive_summary": self.executive_summary(),
            "timeline_metrics": self.timeline.to_dict(),
            "customer_impact": self.customer_impact_summary(),
            "root_cause": self.resolution.get("root_cause", ""),
            "contributing_factors": [f.to_dict() for f in self.contributing_factors],
            "factor_distribution": self.factor_distribution,
            "five_whys_analysis": [a.to_dict() for a in self.five_whys],
            "theme_recommendations": self.theme_recommendations,
            "mitigation_steps": self.resolution.get("mitigation_steps", []),
            "permanent_fix": self.resolution.get("permanent_fix", ""),
            "action_items": [a.to_dict() for a in self.action_items],
            "action_item_coverage_gaps": self.coverage_gaps,
            "suggested_actions": self.suggested_actions,
            "overdue_p1_items": self.overdue_p1_items(),
            "participants": self.participants}


# ---------- Core Analysis Helpers ----------

def _bar(pct: float, width: int = 30) -> str:
    """Render a text-based horizontal bar chart segment."""
    filled = int(round(pct / 100 * width))
    return "[" + "#" * filled + "." * (width - filled) + "]"


def _generate_lessons(report: PostmortemReport) -> List[str]:
    """Derive lessons learned from the analysis."""
    lessons: List[str] = []
    bench = BENCHMARKS.get(report.incident.severity, BENCHMARKS["SEV3"])
    mttd = report.timeline.mttd
    if mttd is not None and mttd > bench["mttd"]:
        lessons.append(
            f"Detection took {mttd:.0f} minutes, exceeding the {bench['mttd']}-minute "
            f"benchmark for {report.incident.severity}. Invest in earlier detection mechanisms.")
    dist = report.factor_distribution
    dominant = max(dist, key=lambda k: dist[k])
    if dist[dominant] >= 50:
        lessons.append(
            f"The '{dominant}' category accounts for {dist[dominant]:.0f}% of contributing factors. "
            f"Targeted improvements in this area will yield the highest return.")
    if report.coverage_gaps:
        lessons.append(
            f"There are {len(report.coverage_gaps)} action item coverage gap(s). "
            "Ensure every contributing factor category has a corresponding remediation action.")
    avg_q = (sum(a.quality_score for a in report.action_items) / len(report.action_items)
             if report.action_items else 0)
    if avg_q < 70:
        lessons.append(
            f"Average action item quality score is {avg_q:.0f}/100. "
            "Make action items more specific with measurable targets and clear ownership.")
    if report.timeline.postmortem_on_time is False:
        h = report.timeline.postmortem_timeliness_hours
        lessons.append(
            f"Postmortem was held {h:.0f} hours after resolution, exceeding the "
            f"{POSTMORTEM_TARGET_HOURS}-hour target. Schedule postmortems sooner to capture context.")
    if not lessons:
        lessons.append("This incident was handled within benchmarks. Continue reinforcing "
                       "current practices and share this postmortem for organizational learning.")
    return lessons


# ---------- Output Formatters ----------

def format_text(report: PostmortemReport) -> str:
    """Format the postmortem as plain text."""
    L: List[str] = []
    W = 72

    def h1(title: str) -> None:
        L.append(""); L.append("=" * W); L.append(f"  {title}"); L.append("=" * W)

    def h2(title: str) -> None:
        L.append(""); L.append(f"--- {title} ---")

    inc = report.incident
    h1(f"POSTMORTEM: {inc.title}")
    L.append(f"  ID: {inc.id}  |  Severity: {inc.severity}  |  Service: {inc.service}")
    L.append(f"  Commander: {inc.commander}")
    if inc.affected_services:
        L.append(f"  Affected services: {', '.join(inc.affected_services)}")
    # Executive Summary
    h1("EXECUTIVE SUMMARY")
    L.append("")
    for sentence in report.executive_summary().split(". "):
        s = sentence.strip()
        if s and not s.endswith("."): s += "."
        if s: L.append(f"  {s}")
    # Timeline Metrics
    h1("TIMELINE METRICS")
    tm = report.timeline
    L.append("")
    for label, val, unit in [("MTTD (Time to Detect)", tm.mttd, "min"),
                             ("MTTR (Time to Resolve)", tm.mttr, "min"),
                             ("Time to Mitigate", tm.time_to_mitigate, "min"),
                             ("Time to Declare", tm.time_to_declare, "min"),
                             ("Postmortem Timeliness", tm.postmortem_timeliness_hours, "hrs")]:
        L.append(f"  {label:<30s} {f'{val:.1f} {unit}' if val is not None else 'N/A'}")
    h2("Benchmark Comparison")
    for name, d in tm.benchmark_comparison().items():
        if "actual_minutes" in d:
            st = "PASS" if d["met_benchmark"] else "FAIL"
            L.append(f"  {name:<25s} actual={d['actual_minutes']}min  benchmark={d['benchmark_minutes']}min  [{st}]")
        elif "actual_hours" in d:
            st = "PASS" if d["met_target"] else "FAIL"
            L.append(f"  {name:<25s} actual={d['actual_hours']}hrs  target={d['target_hours']}hrs  [{st}]")
    # Customer Impact
    h1("CUSTOMER IMPACT")
    ci = report.customer_impact_summary()
    L.append("")
    L.append(f"  Affected users:          {ci['affected_users']:,}")
    L.append(f"  Failed transactions:     {ci['failed_transactions']:,}")
    L.append(f"  Revenue impact:          ${ci['revenue_impact_usd']:,.2f}")
    L.append(f"  Data integrity:          {ci['data_integrity']}")
    L.append(f"  Impact severity:         {ci['impact_severity']}")
    L.append(f"  Comms required:          {'Yes' if ci['customer_communication_required'] else 'No'}")
    # Root Cause
    h1("ROOT CAUSE ANALYSIS")
    L.append("")
    L.append(f"  {report.resolution.get('root_cause', 'Unknown')}")
    h2("Contributing Factors")
    for f in report.contributing_factors:
        L.append(f"  [{f.category.upper():<12s} w={f.weight:.2f}] {f.description}")
    h2("Factor Distribution")
    for cat, pct in sorted(report.factor_distribution.items(), key=lambda x: -x[1]):
        if pct > 0:
            L.append(f"  {cat:<14s} {pct:5.1f}%  {_bar(pct)}")
    # 5-Whys
    h1("5-WHYS ANALYSIS")
    for analysis in report.five_whys:
        L.append("")
        L.append(f"  Factor: {analysis.factor.description}")
        L.append(f"  Theme:  {analysis.systemic_theme}")
        for i, step in enumerate(analysis.chain):
            L.append(f"    {i}. {step}")
    h2("Theme-Based Recommendations")
    for theme, recs in report.theme_recommendations.items():
        L.append(f"  [{theme.upper()}]")
        for rec in recs:
            L.append(f"    - {rec}")
    # Mitigation & Fix
    h1("MITIGATION AND RESOLUTION")
    h2("Mitigation Steps Taken")
    for step in report.resolution.get("mitigation_steps", []):
        L.append(f"  - {step}")
    h2("Permanent Fix")
    L.append(f"  {report.resolution.get('permanent_fix', 'TBD')}")
    # Action Items
    h1("ACTION ITEMS")
    L.append("")
    hdr = f"  {'Priority':<10s} {'Type':<14s} {'Owner':<25s} {'Deadline':<12s} {'Quality':<8s} Title"
    L.append(hdr)
    L.append("  " + "-" * (len(hdr) - 2))
    for a in sorted(report.action_items, key=lambda x: PRIORITY_ORDER.get(x.priority, 99)):
        flag = " *OVERDUE*" if a.is_past_deadline else ""
        L.append(f"  {a.priority:<10s} {a.type:<14s} {a.owner:<25s} {a.deadline:<12s} "
                 f"{a.quality_score:<8d} {a.title}{flag}")
    if report.coverage_gaps:
        h2("Coverage Gaps")
        for gap in report.coverage_gaps:
            L.append(f"  WARNING: {gap}")
    if report.suggested_actions:
        h2("Suggested Additional Actions")
        for s in report.suggested_actions:
            L.append(f"  [{s['type'].upper()}] {s['suggestion']}")
            L.append(f"    Reason: {s['reason']}")
    overdue = report.overdue_p1_items()
    if overdue:
        h2("Overdue P0/P1 Items")
        for item in overdue:
            L.append(f"  OVERDUE: {item['title']} (owner: {item['owner']}, deadline: {item['deadline']})")
    # Participants
    h1("PARTICIPANTS")
    L.append("")
    for p in report.participants:
        L.append(f"  {p.get('name', 'Unknown'):<25s} {p.get('role', '')}")
    # Lessons Learned
    h1("LESSONS LEARNED")
    L.append("")
    for i, lesson in enumerate(_generate_lessons(report), 1):
        L.append(f"  {i}. {lesson}")
    L.append("")
    L.append("=" * W)
    L.append(f"  Generated by postmortem_generator v{VERSION}")
    L.append("=" * W)
    L.append("")
    return "\n".join(L)


def format_json(report: PostmortemReport) -> str:
    """Format the postmortem as JSON."""
    data = report.to_dict()
    data["lessons_learned"] = _generate_lessons(report)
    return json.dumps(data, indent=2, default=str)


def format_markdown(report: PostmortemReport) -> str:
    """Format the postmortem as a Markdown document."""
    L: List[str] = []
    inc = report.incident
    L.append(f"# Postmortem: {inc.title}")
    L.append("")
    L.append("| Field | Value |")
    L.append("|-------|-------|")
    L.append(f"| **ID** | {inc.id} |")
    L.append(f"| **Severity** | {inc.severity} |")
    L.append(f"| **Service** | {inc.service} |")
    L.append(f"| **Commander** | {inc.commander} |")
    if inc.affected_services:
        L.append(f"| **Affected Services** | {', '.join(inc.affected_services)} |")
    L.append("")
    # Executive Summary
    L.append("## Executive Summary\n")
    L.append(report.executive_summary())
    L.append("")
    # Timeline Metrics
    L.append("## Timeline Metrics\n")
    L.append("| Metric | Value | Benchmark | Status |")
    L.append("|--------|-------|-----------|--------|")
    labels = {"mttd": "MTTD (Time to Detect)", "mttr": "MTTR (Time to Resolve)",
              "time_to_mitigate": "Time to Mitigate", "time_to_declare": "Time to Declare",
              "postmortem_timeliness": "Postmortem Timeliness"}
    for key, label in labels.items():
        b = report.timeline.benchmark_comparison().get(key)
        if b and "actual_minutes" in b:
            st = "PASS" if b["met_benchmark"] else "FAIL"
            L.append(f"| {label} | {b['actual_minutes']} min | {b['benchmark_minutes']} min | {st} |")
        elif b and "actual_hours" in b:
            st = "PASS" if b["met_target"] else "FAIL"
            L.append(f"| {label} | {b['actual_hours']} hrs | {b['target_hours']} hrs | {st} |")
    L.append("")
    # Customer Impact
    L.append("## Customer Impact\n")
    ci = report.customer_impact_summary()
    L.append(f"- **Affected users:** {ci['affected_users']:,}")
    L.append(f"- **Failed transactions:** {ci['failed_transactions']:,}")
    L.append(f"- **Revenue impact:** ${ci['revenue_impact_usd']:,.2f}")
    L.append(f"- **Data integrity:** {ci['data_integrity']}")
    L.append(f"- **Impact severity:** {ci['impact_severity']}")
    L.append(f"- **Customer communication required:** {'Yes' if ci['customer_communication_required'] else 'No'}")
    L.append("")
    # Root Cause Analysis
    L.append("## Root Cause Analysis\n")
    L.append(f"**Root cause:** {report.resolution.get('root_cause', 'Unknown')}")
    L.append("")
    L.append("### Contributing Factors\n")
    L.append("| # | Category | Weight | Description |")
    L.append("|---|----------|--------|-------------|")
    for i, f in enumerate(report.contributing_factors, 1):
        L.append(f"| {i} | {f.category} | {f.weight:.2f} | {f.description} |")
    L.append("")
    L.append("### Factor Distribution\n")
    L.append("```")
    for cat, pct in sorted(report.factor_distribution.items(), key=lambda x: -x[1]):
        if pct > 0:
            L.append(f"  {cat:<14s} {pct:5.1f}%  {_bar(pct, 25)}")
    L.append("```")
    L.append("")
    # 5-Whys
    L.append("## 5-Whys Analysis\n")
    for analysis in report.five_whys:
        L.append(f"### Factor: {analysis.factor.description}")
        L.append(f"**Systemic theme:** {analysis.systemic_theme}\n")
        for i, step in enumerate(analysis.chain):
            L.append(f"{i}. {step}")
        L.append("")
    L.append("### Theme-Based Recommendations\n")
    for theme, recs in report.theme_recommendations.items():
        L.append(f"**{theme.capitalize()}:**")
        for rec in recs:
            L.append(f"- {rec}")
        L.append("")
    # Mitigation
    L.append("## Mitigation and Resolution\n")
    L.append("### Mitigation Steps Taken\n")
    for step in report.resolution.get("mitigation_steps", []):
        L.append(f"- {step}")
    L.append("")
    L.append("### Permanent Fix\n")
    L.append(report.resolution.get("permanent_fix", "TBD"))
    L.append("")
    # Action Items
    L.append("## Action Items\n")
    L.append("| Priority | Type | Owner | Deadline | Quality | Title |")
    L.append("|----------|------|-------|----------|---------|-------|")
    for a in sorted(report.action_items, key=lambda x: PRIORITY_ORDER.get(x.priority, 99)):
        flag = " **OVERDUE**" if a.is_past_deadline else ""
        L.append(f"| {a.priority} | {a.type} | {a.owner} | {a.deadline} | {a.quality_score}/100 | {a.title}{flag} |")
    L.append("")
    if report.coverage_gaps:
        L.append("### Coverage Gaps\n")
        for gap in report.coverage_gaps:
            L.append(f"> **WARNING:** {gap}")
        L.append("")
    if report.suggested_actions:
        L.append("### Suggested Additional Actions\n")
        for s in report.suggested_actions:
            L.append(f"- **[{s['type'].upper()}]** {s['suggestion']}")
            L.append(f"  - _Reason: {s['reason']}_")
        L.append("")
    overdue = report.overdue_p1_items()
    if overdue:
        L.append("### Overdue P0/P1 Items\n")
        for item in overdue:
            L.append(f"- **{item['title']}** (owner: {item['owner']}, deadline: {item['deadline']})")
        L.append("")
    # Participants
    L.append("## Participants\n")
    L.append("| Name | Role |")
    L.append("|------|------|")
    for p in report.participants:
        L.append(f"| {p.get('name', 'Unknown')} | {p.get('role', '')} |")
    L.append("")
    # Lessons Learned
    L.append("## Lessons Learned\n")
    for i, lesson in enumerate(_generate_lessons(report), 1):
        L.append(f"{i}. {lesson}")
    L.append("")
    L.append("---")
    L.append(f"_Generated by postmortem_generator v{VERSION}_")
    L.append("")
    return "\n".join(L)


# ---------- Input Loading ----------

def load_input(filepath: Optional[str]) -> Dict[str, Any]:
    """Load incident data from a file path or stdin."""
    if filepath:
        try:
            with open(filepath, "r", encoding="utf-8") as fh:
                return json.load(fh)
        except FileNotFoundError:
            print(f"Error: File not found: {filepath}", file=sys.stderr)
            sys.exit(1)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON in {filepath}: {exc}", file=sys.stderr)
            sys.exit(1)
    else:
        if sys.stdin.isatty():
            print("Error: No input file specified and no data on stdin.", file=sys.stderr)
            print("Usage: postmortem_generator.py [data_file] or pipe JSON via stdin.", file=sys.stderr)
            sys.exit(1)
        try:
            return json.load(sys.stdin)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON on stdin: {exc}", file=sys.stderr)
            sys.exit(1)


def validate_input(data: Dict[str, Any]) -> List[str]:
    """Return a list of validation warnings (non-fatal)."""
    warnings: List[str] = []
    for key in ("incident", "timeline", "resolution", "action_items"):
        if key not in data:
            warnings.append(f"Missing '{key}' section")
    for ts in ("issue_started", "detected_at", "mitigated_at", "resolved_at"):
        if ts not in data.get("timeline", {}):
            warnings.append(f"Missing timeline field: {ts}")
    res = data.get("resolution", {})
    if "root_cause" not in res:
        warnings.append("Missing 'root_cause' in resolution")
    if not res.get("contributing_factors"):
        warnings.append("No contributing factors provided")
    return warnings


# ---------- CLI Entry Point ----------

def main() -> None:
    """CLI entry point for postmortem generation."""
    parser = argparse.ArgumentParser(
        description="Generate structured postmortem reports with 5-Whys analysis.",
        epilog="Reads JSON from a file or stdin. Outputs text, JSON, or markdown.")
    parser.add_argument("data_file", nargs="?", default=None,
                        help="JSON file with incident + resolution data (reads stdin if omitted)")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text",
                        dest="output_format", help="Output format (default: text)")
    args = parser.parse_args()

    data = load_input(args.data_file)
    warnings = validate_input(data)
    for w in warnings:
        print(f"Warning: {w}", file=sys.stderr)

    report = PostmortemReport(data)
    formatters = {"text": format_text, "json": format_json, "markdown": format_markdown}
    print(formatters[args.output_format](report))


if __name__ == "__main__":
    main()
