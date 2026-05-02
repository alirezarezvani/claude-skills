#!/usr/bin/env python3
"""
Incident Timeline Builder

Builds structured incident timelines with automatic phase detection, gap analysis,
communication template generation, and response metrics calculation. Produces
professional reports suitable for post-incident review and stakeholder briefing.

Usage:
    python incident_timeline_builder.py incident_data.json
    python incident_timeline_builder.py incident_data.json --format json
    python incident_timeline_builder.py incident_data.json --format markdown
    cat incident_data.json | python incident_timeline_builder.py --format text
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Configuration Constants
# ---------------------------------------------------------------------------

ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

EVENT_TYPES = [
    "detection", "declaration", "escalation", "investigation",
    "mitigation", "communication", "resolution", "action_item",
]

SEVERITY_LEVELS = {
    "SEV1": {"label": "Critical", "rank": 1},
    "SEV2": {"label": "Major", "rank": 2},
    "SEV3": {"label": "Minor", "rank": 3},
    "SEV4": {"label": "Low", "rank": 4},
}

PHASE_DEFINITIONS = [
    {"name": "Detection", "trigger_types": ["detection"],
     "description": "Issue detected via monitoring, alerting, or user report."},
    {"name": "Triage", "trigger_types": ["declaration", "escalation"],
     "description": "Incident declared, severity assessed, commander assigned."},
    {"name": "Investigation", "trigger_types": ["investigation"],
     "description": "Root cause analysis and impact assessment underway."},
    {"name": "Mitigation", "trigger_types": ["mitigation"],
     "description": "Active work to reduce or eliminate customer impact."},
    {"name": "Resolution", "trigger_types": ["resolution"],
     "description": "Service restored to normal operating parameters."},
]

GAP_THRESHOLD_MINUTES = 15

DECISION_EVENT_TYPES = {"escalation", "mitigation", "declaration", "resolution"}


# ---------------------------------------------------------------------------
# Data Model Classes
# ---------------------------------------------------------------------------

class IncidentEvent:
    """Represents a single event in the incident timeline."""

    def __init__(self, data: Dict[str, Any]):
        self.timestamp_raw: str = data.get("timestamp", "")
        self.timestamp: Optional[datetime] = _parse_timestamp(self.timestamp_raw)
        self.type: str = data.get("type", "unknown").lower().strip()
        self.actor: str = data.get("actor", "unknown")
        self.description: str = data.get("description", "")
        self.metadata: Dict[str, Any] = data.get("metadata", {})

    def to_dict(self) -> Dict[str, Any]:
        result: Dict[str, Any] = {
            "timestamp": self.timestamp_raw, "type": self.type,
            "actor": self.actor, "description": self.description,
        }
        if self.metadata:
            result["metadata"] = self.metadata
        return result

    @property
    def is_decision_point(self) -> bool:
        return self.type in DECISION_EVENT_TYPES


class IncidentPhase:
    """Represents a detected phase of the incident lifecycle."""

    def __init__(self, name: str, description: str):
        self.name: str = name
        self.description: str = description
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
        self.events: List[IncidentEvent] = []

    @property
    def duration_minutes(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds() / 60.0
        return None

    def to_dict(self) -> Dict[str, Any]:
        dur = self.duration_minutes
        return {
            "name": self.name, "description": self.description,
            "start_time": self.start_time.strftime(ISO_FORMAT) if self.start_time else None,
            "end_time": self.end_time.strftime(ISO_FORMAT) if self.end_time else None,
            "duration_minutes": round(dur, 1) if dur is not None else None,
            "event_count": len(self.events),
        }


class CommunicationTemplate:
    """A generated communication message for a specific audience."""

    def __init__(self, template_type: str, audience: str, subject: str, body: str):
        self.template_type = template_type
        self.audience = audience
        self.subject = subject
        self.body = body

    def to_dict(self) -> Dict[str, Any]:
        return {"template_type": self.template_type, "audience": self.audience,
                "subject": self.subject, "body": self.body}


class TimelineGap:
    """Represents a gap in the timeline where no events were logged."""

    def __init__(self, start: datetime, end: datetime, duration_minutes: float):
        self.start = start
        self.end = end
        self.duration_minutes = duration_minutes

    def to_dict(self) -> Dict[str, Any]:
        return {"start": self.start.strftime(ISO_FORMAT),
                "end": self.end.strftime(ISO_FORMAT),
                "duration_minutes": round(self.duration_minutes, 1)}


class TimelineAnalysis:
    """Holds the complete analysis result for an incident timeline."""

    def __init__(self):
        self.incident_id: str = ""
        self.incident_title: str = ""
        self.severity: str = ""
        self.status: str = ""
        self.commander: str = ""
        self.service: str = ""
        self.affected_services: List[str] = []
        self.declared_at: Optional[datetime] = None
        self.resolved_at: Optional[datetime] = None
        self.events: List[IncidentEvent] = []
        self.phases: List[IncidentPhase] = []
        self.gaps: List[TimelineGap] = []
        self.decision_points: List[IncidentEvent] = []
        self.metrics: Dict[str, Any] = {}
        self.communications: List[CommunicationTemplate] = []
        self.errors: List[str] = []


# ---------------------------------------------------------------------------
# Timestamp Helpers
# ---------------------------------------------------------------------------

def _parse_timestamp(raw: str) -> Optional[datetime]:
    """Parse an ISO-8601 timestamp string into a datetime object."""
    if not raw:
        return None
    cleaned = raw.replace("Z", "+00:00") if raw.endswith("Z") else raw
    try:
        return datetime.fromisoformat(cleaned).replace(tzinfo=None)
    except (ValueError, AttributeError):
        pass
    try:
        return datetime.strptime(raw, ISO_FORMAT)
    except ValueError:
        return None


def _fmt_duration(minutes: Optional[float]) -> str:
    """Format a duration in minutes as a human-readable string."""
    if minutes is None:
        return "N/A"
    if minutes < 1:
        return f"{minutes * 60:.0f}s"
    if minutes < 60:
        return f"{minutes:.0f}m"
    hours, remaining = int(minutes // 60), int(minutes % 60)
    return f"{hours}h" if remaining == 0 else f"{hours}h {remaining}m"


def _fmt_ts(dt: Optional[datetime]) -> str:
    """Format a datetime as HH:MM:SS for display."""
    return dt.strftime("%H:%M:%S") if dt else "??:??:??"


def _sev_label(sev: str) -> str:
    """Return the human label for a severity code."""
    return SEVERITY_LEVELS.get(sev, {}).get("label", sev)


# ---------------------------------------------------------------------------
# Core Analysis Functions
# ---------------------------------------------------------------------------

def parse_incident_data(data: Dict[str, Any]) -> TimelineAnalysis:
    """Parse raw incident JSON into a TimelineAnalysis with populated fields."""
    a = TimelineAnalysis()
    inc = data.get("incident", {})
    a.incident_id = inc.get("id", "UNKNOWN")
    a.incident_title = inc.get("title", "Untitled Incident")
    a.severity = inc.get("severity", "UNKNOWN").upper()
    a.status = inc.get("status", "unknown").lower()
    a.commander = inc.get("commander", "Unassigned")
    a.service = inc.get("service", "unknown")
    a.affected_services = inc.get("affected_services", [])
    a.declared_at = _parse_timestamp(inc.get("declared_at", ""))
    a.resolved_at = _parse_timestamp(inc.get("resolved_at", ""))

    raw_events = data.get("events", [])
    if not raw_events:
        a.errors.append("No events found in incident data.")
        return a

    for raw in raw_events:
        event = IncidentEvent(raw)
        if event.timestamp is None:
            a.errors.append(f"Skipping event with unparseable timestamp: {raw.get('timestamp', '')}")
            continue
        a.events.append(event)

    a.events.sort(key=lambda e: e.timestamp)  # type: ignore[arg-type]
    return a


def detect_phases(analysis: TimelineAnalysis) -> None:
    """Detect incident lifecycle phases from the ordered event stream."""
    if not analysis.events:
        return

    trigger_map: Dict[str, Dict[str, str]] = {}
    for pdef in PHASE_DEFINITIONS:
        for ttype in pdef["trigger_types"]:
            trigger_map[ttype] = {"name": pdef["name"], "description": pdef["description"]}

    phase_by_name: Dict[str, IncidentPhase] = {}
    phase_order: List[str] = []
    current: Optional[IncidentPhase] = None

    for event in analysis.events:
        pinfo = trigger_map.get(event.type)
        if pinfo and pinfo["name"] not in phase_by_name:
            if current is not None:
                current.end_time = event.timestamp
            phase = IncidentPhase(pinfo["name"], pinfo["description"])
            phase.start_time = event.timestamp
            phase_by_name[pinfo["name"]] = phase
            phase_order.append(pinfo["name"])
            current = phase
        if current is not None:
            current.events.append(event)

    if current is not None:
        current.end_time = analysis.resolved_at or analysis.events[-1].timestamp

    analysis.phases = [phase_by_name[n] for n in phase_order]


def detect_gaps(analysis: TimelineAnalysis) -> None:
    """Identify gaps longer than GAP_THRESHOLD_MINUTES between consecutive events."""
    for i in range(len(analysis.events) - 1):
        ts_a, ts_b = analysis.events[i].timestamp, analysis.events[i + 1].timestamp
        if ts_a is None or ts_b is None:
            continue
        delta = (ts_b - ts_a).total_seconds() / 60.0
        if delta >= GAP_THRESHOLD_MINUTES:
            analysis.gaps.append(TimelineGap(start=ts_a, end=ts_b, duration_minutes=delta))


def identify_decision_points(analysis: TimelineAnalysis) -> None:
    """Extract key decision-point events from the timeline."""
    analysis.decision_points = [e for e in analysis.events if e.is_decision_point]


def calculate_metrics(analysis: TimelineAnalysis) -> None:
    """Calculate incident response metrics: MTTD, MTTR, phase durations."""
    m: Dict[str, Any] = {}
    det = [e for e in analysis.events if e.type == "detection"]
    first_det = det[0].timestamp if det else None
    first_ts = analysis.events[0].timestamp if analysis.events else None

    # MTTD: first event to first detection.
    if first_ts and first_det:
        m["mttd_minutes"] = round((first_det - first_ts).total_seconds() / 60.0, 1)
    else:
        m["mttd_minutes"] = None

    # MTTR: detection to resolution.
    if first_det and analysis.resolved_at:
        m["mttr_minutes"] = round((analysis.resolved_at - first_det).total_seconds() / 60.0, 1)
    else:
        m["mttr_minutes"] = None

    # Total duration.
    if analysis.declared_at and analysis.resolved_at:
        m["total_duration_minutes"] = round(
            (analysis.resolved_at - analysis.declared_at).total_seconds() / 60.0, 1)
    else:
        m["total_duration_minutes"] = None

    # Phase durations.
    m["phase_durations"] = {
        p.name: (round(p.duration_minutes, 1) if p.duration_minutes is not None else None)
        for p in analysis.phases
    }

    # Event counts by type.
    tc: Dict[str, int] = {}
    for e in analysis.events:
        tc[e.type] = tc.get(e.type, 0) + 1
    m["event_counts_by_type"] = tc

    # Gap statistics.
    m["gap_count"] = len(analysis.gaps)
    if analysis.gaps:
        gm = [g.duration_minutes for g in analysis.gaps]
        m["longest_gap_minutes"] = round(max(gm), 1)
        m["total_gap_minutes"] = round(sum(gm), 1)
    else:
        m["longest_gap_minutes"] = 0
        m["total_gap_minutes"] = 0

    m["total_events"] = len(analysis.events)
    m["decision_point_count"] = len(analysis.decision_points)
    m["phase_count"] = len(analysis.phases)
    analysis.metrics = m


# ---------------------------------------------------------------------------
# Communication Template Generation
# ---------------------------------------------------------------------------

def generate_communications(analysis: TimelineAnalysis) -> None:
    """Generate four communication templates based on incident data."""
    sev, sl = analysis.severity, _sev_label(analysis.severity)
    title, svc = analysis.incident_title, analysis.service
    affected = ", ".join(analysis.affected_services) or "none identified"
    cmd, iid = analysis.commander, analysis.incident_id
    decl = analysis.declared_at.strftime("%Y-%m-%d %H:%M UTC") if analysis.declared_at else "TBD"
    resv = analysis.resolved_at.strftime("%Y-%m-%d %H:%M UTC") if analysis.resolved_at else "TBD"
    dur = _fmt_duration(analysis.metrics.get("total_duration_minutes"))
    resolved = analysis.status == "resolved"

    # 1 -- Initial stakeholder notification
    analysis.communications.append(CommunicationTemplate(
        "initial_notification", "internal", f"[{sev}] Incident Declared: {title}",
        f"An incident has been declared for {svc}.\n\n"
        f"Incident ID: {iid}\nSeverity: {sev} ({sl})\nCommander: {cmd}\n"
        f"Declared at: {decl}\nAffected services: {affected}\n\n"
        f"The incident team is actively investigating. Updates will follow.",
    ))

    # 2 -- Status page update
    if resolved:
        sp_subj = f"[Resolved] {title}"
        sp_body = (f"The incident affecting {svc} has been resolved.\n\n"
                   f"Duration: {dur}\nAll affected services ({affected}) are restored. "
                   f"A post-incident review will be published within 48 hours.")
    else:
        sp_subj = f"[Investigating] {title}"
        sp_body = (f"We are investigating degraded performance in {svc}. "
                   f"Affected services: {affected}.\n\n"
                   f"Our team is working to identify the root cause. Updates every 30 minutes.")
    analysis.communications.append(CommunicationTemplate(
        "status_page", "external", sp_subj, sp_body))

    # 3 -- Executive summary
    phase_lines = "\n".join(
        f"  - {p.name}: {_fmt_duration(p.duration_minutes)}" for p in analysis.phases
    ) or "  No phase data available."
    mttd = _fmt_duration(analysis.metrics.get("mttd_minutes"))
    mttr = _fmt_duration(analysis.metrics.get("mttr_minutes"))
    analysis.communications.append(CommunicationTemplate(
        "executive_summary", "executive", f"Executive Summary: {iid} - {title}",
        f"Incident: {iid} - {title}\nSeverity: {sev} ({sl})\n"
        f"Service: {svc}\nCommander: {cmd}\nStatus: {analysis.status.capitalize()}\n"
        f"Declared: {decl}\nResolved: {resv}\nDuration: {dur}\n\n"
        f"Key Metrics:\n  - MTTD: {mttd}\n  - MTTR: {mttr}\n"
        f"  - Timeline Gaps: {analysis.metrics.get('gap_count', 0)}\n\n"
        f"Phase Breakdown:\n{phase_lines}\n\nAffected Services: {affected}",
    ))

    # 4 -- Customer notification
    if resolved:
        cust_body = (f"We experienced an issue affecting {svc} starting at {decl}.\n\n"
                     f"The issue was resolved at {resv} (duration: {dur}). "
                     f"We apologize for any inconvenience and are reviewing to prevent recurrence.")
    else:
        cust_body = (f"We are experiencing an issue affecting {svc} starting at {decl}.\n\n"
                     f"Our engineering team is actively working to resolve this. "
                     f"We will provide updates as the situation develops. We apologize for the inconvenience.")
    analysis.communications.append(CommunicationTemplate(
        "customer_notification", "external", f"Service Update: {title}", cust_body))


# ---------------------------------------------------------------------------
# Main Analysis Orchestrator
# ---------------------------------------------------------------------------

def build_timeline(data: Dict[str, Any]) -> TimelineAnalysis:
    """Run the full timeline analysis pipeline on raw incident data."""
    analysis = parse_incident_data(data)
    if analysis.errors and not analysis.events:
        return analysis
    detect_phases(analysis)
    detect_gaps(analysis)
    identify_decision_points(analysis)
    calculate_metrics(analysis)
    generate_communications(analysis)
    return analysis


# ---------------------------------------------------------------------------
# Output Formatters
# ---------------------------------------------------------------------------

def format_text_output(analysis: TimelineAnalysis) -> str:
    """Format the analysis as a human-readable text report."""
    L: List[str] = []
    w = 64

    L.append("=" * w)
    L.append("INCIDENT TIMELINE REPORT")
    L.append("=" * w)
    L.append("")

    if analysis.errors:
        for err in analysis.errors:
            L.append(f"  WARNING: {err}")
        L.append("")
        if not analysis.events:
            return "\n".join(L)

    # Summary
    L.append("INCIDENT SUMMARY")
    L.append("-" * 32)
    L.append(f"  ID:         {analysis.incident_id}")
    L.append(f"  Title:      {analysis.incident_title}")
    L.append(f"  Severity:   {analysis.severity}")
    L.append(f"  Status:     {analysis.status.capitalize()}")
    L.append(f"  Commander:  {analysis.commander}")
    L.append(f"  Service:    {analysis.service}")
    if analysis.affected_services:
        L.append(f"  Affected:   {', '.join(analysis.affected_services)}")
    L.append(f"  Duration:   {_fmt_duration(analysis.metrics.get('total_duration_minutes'))}")
    L.append("")

    # Key metrics
    L.append("KEY METRICS")
    L.append("-" * 32)
    L.append(f"  MTTD (Mean Time to Detect):   {_fmt_duration(analysis.metrics.get('mttd_minutes'))}")
    L.append(f"  MTTR (Mean Time to Resolve):  {_fmt_duration(analysis.metrics.get('mttr_minutes'))}")
    L.append(f"  Total Events:                 {analysis.metrics.get('total_events', 0)}")
    L.append(f"  Decision Points:              {analysis.metrics.get('decision_point_count', 0)}")
    L.append(f"  Timeline Gaps (>{GAP_THRESHOLD_MINUTES}m):      {analysis.metrics.get('gap_count', 0)}")
    L.append("")

    # Phases
    L.append("INCIDENT PHASES")
    L.append("-" * 32)
    if analysis.phases:
        for p in analysis.phases:
            L.append(f"  [{_fmt_ts(p.start_time)} - {_fmt_ts(p.end_time)}]  {p.name} ({_fmt_duration(p.duration_minutes)})")
            L.append(f"    {p.description}")
            L.append(f"    Events: {len(p.events)}")
    else:
        L.append("  No phases detected.")
    L.append("")

    # Chronological timeline
    L.append("CHRONOLOGICAL TIMELINE")
    L.append("-" * 32)
    for e in analysis.events:
        marker = "*" if e.is_decision_point else " "
        L.append(f"  {_fmt_ts(e.timestamp)} {marker} [{e.type.upper():13s}] {e.actor}")
        L.append(f"             {e.description}")
    L.append("")
    L.append("  (* = key decision point)")
    L.append("")

    # Gap warnings
    if analysis.gaps:
        L.append("GAP ANALYSIS")
        L.append("-" * 32)
        for g in analysis.gaps:
            L.append(f"  WARNING: {_fmt_duration(g.duration_minutes)} gap between {_fmt_ts(g.start)} and {_fmt_ts(g.end)}")
        L.append("")

    # Decision points
    if analysis.decision_points:
        L.append("KEY DECISION POINTS")
        L.append("-" * 32)
        for dp in analysis.decision_points:
            L.append(f"  {_fmt_ts(dp.timestamp)}  [{dp.type.upper()}] {dp.description}")
        L.append("")

    # Communications
    if analysis.communications:
        L.append("GENERATED COMMUNICATIONS")
        L.append("-" * 32)
        for c in analysis.communications:
            L.append(f"  Type:     {c.template_type}")
            L.append(f"  Audience: {c.audience}")
            L.append(f"  Subject:  {c.subject}")
            L.append("  ---")
            for bl in c.body.split("\n"):
                L.append(f"  {bl}")
            L.append("")

    L.append("=" * w)
    L.append("END OF REPORT")
    L.append("=" * w)
    return "\n".join(L)


def format_json_output(analysis: TimelineAnalysis) -> Dict[str, Any]:
    """Format the analysis as a structured JSON-serializable dictionary."""
    return {
        "incident": {
            "id": analysis.incident_id, "title": analysis.incident_title,
            "severity": analysis.severity, "status": analysis.status,
            "commander": analysis.commander, "service": analysis.service,
            "affected_services": analysis.affected_services,
            "declared_at": analysis.declared_at.strftime(ISO_FORMAT) if analysis.declared_at else None,
            "resolved_at": analysis.resolved_at.strftime(ISO_FORMAT) if analysis.resolved_at else None,
        },
        "timeline": [e.to_dict() for e in analysis.events],
        "phases": [p.to_dict() for p in analysis.phases],
        "gaps": [g.to_dict() for g in analysis.gaps],
        "decision_points": [e.to_dict() for e in analysis.decision_points],
        "metrics": analysis.metrics,
        "communications": [c.to_dict() for c in analysis.communications],
        "errors": analysis.errors if analysis.errors else [],
    }


def format_markdown_output(analysis: TimelineAnalysis) -> str:
    """Format the analysis as a professional Markdown report."""
    L: List[str] = []

    L.append(f"# Incident Timeline Report: {analysis.incident_id}")
    L.append("")

    if analysis.errors:
        L.append("> **Warnings:**")
        for err in analysis.errors:
            L.append(f"> - {err}")
        L.append("")
        if not analysis.events:
            return "\n".join(L)

    # Summary table
    L.append("## Incident Summary")
    L.append("")
    L.append("| Field | Value |")
    L.append("|-------|-------|")
    L.append(f"| **ID** | {analysis.incident_id} |")
    L.append(f"| **Title** | {analysis.incident_title} |")
    L.append(f"| **Severity** | {analysis.severity} ({_sev_label(analysis.severity)}) |")
    L.append(f"| **Status** | {analysis.status.capitalize()} |")
    L.append(f"| **Commander** | {analysis.commander} |")
    L.append(f"| **Service** | {analysis.service} |")
    if analysis.affected_services:
        L.append(f"| **Affected Services** | {', '.join(analysis.affected_services)} |")
    L.append(f"| **Duration** | {_fmt_duration(analysis.metrics.get('total_duration_minutes'))} |")
    L.append("")

    # Key metrics
    L.append("## Key Metrics")
    L.append("")
    L.append(f"- **MTTD (Mean Time to Detect):** {_fmt_duration(analysis.metrics.get('mttd_minutes'))}")
    L.append(f"- **MTTR (Mean Time to Resolve):** {_fmt_duration(analysis.metrics.get('mttr_minutes'))}")
    L.append(f"- **Total Events:** {analysis.metrics.get('total_events', 0)}")
    L.append(f"- **Decision Points:** {analysis.metrics.get('decision_point_count', 0)}")
    L.append(f"- **Timeline Gaps (>{GAP_THRESHOLD_MINUTES}m):** {analysis.metrics.get('gap_count', 0)}")
    if analysis.metrics.get("longest_gap_minutes", 0) > 0:
        L.append(f"- **Longest Gap:** {_fmt_duration(analysis.metrics.get('longest_gap_minutes'))}")
    L.append("")

    # Phases table
    L.append("## Incident Phases")
    L.append("")
    if analysis.phases:
        L.append("| Phase | Start | End | Duration | Events |")
        L.append("|-------|-------|-----|----------|--------|")
        for p in analysis.phases:
            L.append(f"| {p.name} | {_fmt_ts(p.start_time)} | {_fmt_ts(p.end_time)} | {_fmt_duration(p.duration_minutes)} | {len(p.events)} |")
        L.append("")
        # ASCII bar chart
        max_dur = max((p.duration_minutes for p in analysis.phases if p.duration_minutes), default=0)
        if max_dur and max_dur > 0:
            L.append("### Phase Duration Distribution")
            L.append("")
            L.append("```")
            for p in analysis.phases:
                d = p.duration_minutes or 0
                bar = "#" * int((d / max_dur) * 40)
                L.append(f"  {p.name:15s} |{bar} {_fmt_duration(d)}")
            L.append("```")
            L.append("")
    else:
        L.append("No phases detected.")
        L.append("")

    # Chronological timeline
    L.append("## Chronological Timeline")
    L.append("")
    for e in analysis.events:
        dm = " **[KEY DECISION]**" if e.is_decision_point else ""
        L.append(f"- `{_fmt_ts(e.timestamp)}` **{e.type.upper()}** ({e.actor}){dm}")
        L.append(f"  - {e.description}")
    L.append("")

    # Gap analysis
    if analysis.gaps:
        L.append("## Gap Analysis")
        L.append("")
        L.append(f"> {len(analysis.gaps)} gap(s) of >{GAP_THRESHOLD_MINUTES} minutes detected. "
                 f"These may represent blind spots where important activity was not recorded.")
        L.append("")
        for g in analysis.gaps:
            L.append(f"- **{_fmt_duration(g.duration_minutes)}** gap from `{_fmt_ts(g.start)}` to `{_fmt_ts(g.end)}`")
        L.append("")

    # Decision points
    if analysis.decision_points:
        L.append("## Key Decision Points")
        L.append("")
        for dp in analysis.decision_points:
            L.append(f"1. `{_fmt_ts(dp.timestamp)}` **{dp.type.upper()}** - {dp.description}")
        L.append("")

    # Communications
    if analysis.communications:
        L.append("## Generated Communications")
        L.append("")
        for c in analysis.communications:
            L.append(f"### {c.template_type.replace('_', ' ').title()} ({c.audience})")
            L.append("")
            L.append(f"**Subject:** {c.subject}")
            L.append("")
            for bl in c.body.split("\n"):
                L.append(bl)
            L.append("")
            L.append("---")
            L.append("")

    # Event type breakdown
    tc = analysis.metrics.get("event_counts_by_type", {})
    if tc:
        L.append("## Event Type Breakdown")
        L.append("")
        L.append("| Type | Count |")
        L.append("|------|-------|")
        for etype, count in sorted(tc.items(), key=lambda x: -x[1]):
            L.append(f"| {etype} | {count} |")
        L.append("")

    L.append("---")
    L.append(f"*Report generated for incident {analysis.incident_id}. All timestamps in UTC.*")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# CLI Interface
# ---------------------------------------------------------------------------

def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Build structured incident timelines with phase detection and communication templates."
    )
    parser.add_argument(
        "data_file", nargs="?", default=None,
        help="JSON file with incident data (reads stdin if omitted)",
    )
    parser.add_argument(
        "--format", choices=["text", "json", "markdown"], default="text",
        help="Output format (default: text)",
    )
    args = parser.parse_args()

    try:
        if args.data_file:
            try:
                with open(args.data_file, "r") as f:
                    raw_data = json.load(f)
            except FileNotFoundError:
                print(f"Error: File '{args.data_file}' not found.", file=sys.stderr)
                return 1
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in '{args.data_file}': {e}", file=sys.stderr)
                return 1
        else:
            if sys.stdin.isatty():
                print("Error: No input file specified and stdin is a terminal. "
                      "Provide a file argument or pipe JSON to stdin.", file=sys.stderr)
                return 1
            try:
                raw_data = json.load(sys.stdin)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON on stdin: {e}", file=sys.stderr)
                return 1

        if not isinstance(raw_data, dict):
            print("Error: Input must be a JSON object.", file=sys.stderr)
            return 1
        if "incident" not in raw_data and "events" not in raw_data:
            print("Error: Input must contain at least 'incident' or 'events' keys.", file=sys.stderr)
            return 1

        analysis = build_timeline(raw_data)

        if args.format == "json":
            print(json.dumps(format_json_output(analysis), indent=2))
        elif args.format == "markdown":
            print(format_markdown_output(analysis))
        else:
            print(format_text_output(analysis))
        return 0

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
