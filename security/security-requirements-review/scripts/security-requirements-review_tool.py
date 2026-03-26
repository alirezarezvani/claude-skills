#!/usr/bin/env python3
"""
security-requirements-review_tool.py — CLI tool for the security-requirements-review skill.

Accepts any design document (PRD, architecture doc, POA&M, requirements spec, project plan)
and produces a USAP output contract JSON payload.

Uses:
  - shared/scripts/doc_intake.py    for multi-format text extraction
  - scripts/pre_analysis.py         for deterministic classification and entity extraction

Usage:
  python scripts/security-requirements-review_tool.py --input <path> --output json
  python scripts/security-requirements-review_tool.py --input doc.md --output text
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


SKILL_SLUG = "security-requirements-review"

# Paths relative to this script's location
SCRIPT_DIR = Path(__file__).parent
SKILL_ROOT = SCRIPT_DIR.parent
REPO_ROOT = SKILL_ROOT.parent.parent

DOC_INTAKE_PATH = REPO_ROOT / "shared" / "scripts" / "doc_intake.py"
PRE_ANALYSIS_PATH = SCRIPT_DIR / "pre_analysis.py"

SUPPORTED_EXTENSIONS = {".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".pdf", ".docx"}

# Downstream routing based on document type + conditions
ROUTING_MAP = {
    "architecture": ["risk-threat-modeling"],
    "prd": ["appsec-code-review"],
    "poam": ["compliance-mapping"],
    "requirements_spec": ["appsec-code-review"],
    "project_plan": [],
    "unknown": [],
}

COMPLIANCE_ROUTING = {
    "PCI DSS": "compliance-mapping",
    "GDPR": "compliance-mapping",
    "HIPAA": "compliance-mapping",
    "SOC 2": "compliance-mapping",
    "FedRAMP": "compliance-mapping",
    "NIST CSF": "compliance-mapping",
}


def run_doc_intake(input_path: str) -> dict:
    """Extract text from the document using doc_intake.py."""
    if not DOC_INTAKE_PATH.exists():
        # Fallback: try reading the file directly if it's a text format
        path = Path(input_path)
        if path.suffix.lower() in {".md", ".txt", ".rst"}:
            try:
                text = path.read_text(encoding="utf-8", errors="replace")
                return {
                    "document_type_hint": "plaintext",
                    "text": text,
                    "word_count": len(text.split()),
                    "extraction_method": "stdlib-fallback",
                }
            except OSError as exc:
                return {"error": f"Cannot read file: {exc}", "text": ""}
        return {
            "error": "doc_intake.py not found and file format requires it",
            "text": "",
        }

    result = subprocess.run(
        [sys.executable, str(DOC_INTAKE_PATH), "--input", input_path],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0 or not result.stdout.strip():
        return {"error": result.stderr or "doc_intake returned no output", "text": ""}

    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {"error": "doc_intake output was not valid JSON", "text": result.stdout}


def run_pre_analysis(text: str) -> tuple[dict, int]:
    """Run pre_analysis.py with document text on stdin. Returns (result_dict, exit_code)."""
    payload = json.dumps({"document_text": text})

    result = subprocess.run(
        [sys.executable, str(PRE_ANALYSIS_PATH)],
        input=payload,
        capture_output=True,
        text=True,
    )

    try:
        analysis = json.loads(result.stdout)
    except json.JSONDecodeError:
        analysis = {"error": "pre_analysis output was not valid JSON", "exit_code": 0}

    return analysis, result.returncode


def build_severity(analysis: dict) -> str:
    """Map pre_analysis exit code to USAP severity."""
    exit_code = analysis.get("exit_code", 0)
    return {2: "critical", 1: "high", 0: "informational"}.get(exit_code, "informational")


def build_next_agents(doc_type: str, frameworks: list[str], critical_keywords: list[str]) -> list[str]:
    """Build routing list based on document type and detected signals."""
    agents = list(ROUTING_MAP.get(doc_type, []))

    # Add compliance routing if frameworks detected
    if frameworks:
        agents.append("compliance-mapping")

    # Critical issues always route to cs-security-analyst via alert triage
    if critical_keywords:
        agents.append("cs-security-analyst")

    # Architecture docs always get threat modeling
    if doc_type == "architecture" and "risk-threat-modeling" not in agents:
        agents.append("risk-threat-modeling")

    # Deduplicate preserving order
    seen = set()
    result = []
    for a in agents:
        if a not in seen:
            seen.add(a)
            result.append(a)
    return result


def build_key_findings(analysis: dict, severity: str) -> list[str]:
    """Construct key_findings list from pre_analysis results."""
    findings = []
    sev_label = severity.upper()

    for kw in analysis.get("critical_keywords", []):
        findings.append(f"{sev_label}: Critical keyword detected in document — '{kw}'")

    for gap in analysis.get("compliance_gaps", []):
        findings.append(f"HIGH: Compliance framework '{gap}' obligations present without matching control descriptions")

    frameworks = analysis.get("detected_frameworks", [])
    if frameworks:
        findings.append(f"Detected compliance frameworks: {', '.join(frameworks)}")

    if analysis.get("has_data_flows") and not analysis.get("has_trust_boundaries"):
        findings.append("HIGH: Data flows described without trust boundary definitions — lateral movement risk unassessable")

    if not findings:
        findings.append("No critical or high security design gaps detected from deterministic analysis — LLM analysis recommended for full review")

    return findings


def build_evidence_references(input_path: str, analysis: dict) -> list[dict]:
    """Build evidence_references from detected signals."""
    filename = os.path.basename(input_path)
    refs = []

    for kw in analysis.get("critical_keywords", []):
        refs.append({
            "source": "document-intake",
            "source_document": filename,
            "location": "pre_analysis.py deterministic scan",
            "detail": f"Critical keyword match: '{kw}'",
        })

    for gap in analysis.get("compliance_gaps", []):
        refs.append({
            "source": "document-intake",
            "source_document": filename,
            "location": "compliance framework signal scan",
            "detail": f"Framework '{gap}' obligations detected without corresponding control keywords",
        })

    return refs


def build_output(input_path: str, intake: dict, analysis: dict) -> dict:
    """Assemble the USAP output contract payload."""
    doc_type = analysis.get("document_type", "unknown")
    frameworks = analysis.get("detected_frameworks", [])
    critical_keywords = analysis.get("critical_keywords", [])
    severity = build_severity(analysis)
    next_agents = build_next_agents(doc_type, frameworks, critical_keywords)
    key_findings = build_key_findings(analysis, severity)
    evidence_refs = build_evidence_references(input_path, analysis)

    if critical_keywords:
        action = (
            f"Escalate immediately. Critical security signals detected in document "
            f"('{critical_keywords[0]}'). Route to {', '.join(next_agents)} for full analysis."
        )
    elif frameworks:
        action = (
            f"Route to compliance-mapping for {', '.join(frameworks)} control gap analysis. "
            f"Document type: {doc_type}."
        )
    else:
        action = (
            f"Proceed with LLM-level security review. Document type: {doc_type}. "
            f"No critical deterministic signals detected."
        )

    confidence = 0.85 if critical_keywords else (0.70 if frameworks else 0.55)

    return {
        "agent_slug": SKILL_SLUG,
        "intent_type": "analyze",
        "action": action,
        "rationale": (
            f"Document classified as '{doc_type}'. "
            f"Detected frameworks: {frameworks or 'none'}. "
            f"Critical keywords: {critical_keywords or 'none'}. "
            f"Has data flows: {analysis.get('has_data_flows', False)}. "
            f"Has trust boundaries: {analysis.get('has_trust_boundaries', False)}. "
            f"Technology stack: {analysis.get('technology_keywords', [])}."
        ),
        "confidence": confidence,
        "severity": severity,
        "document_metadata": {
            "document_type": doc_type,
            "word_count": intake.get("word_count", 0),
            "detected_frameworks": frameworks,
            "has_data_flows": analysis.get("has_data_flows", False),
            "has_trust_boundaries": analysis.get("has_trust_boundaries", False),
            "technology_keywords": analysis.get("technology_keywords", []),
            "critical_keywords_found": critical_keywords,
            "extraction_method": intake.get("extraction_method", "unknown"),
        },
        "key_findings": key_findings,
        "evidence_references": evidence_refs,
        "next_agents": next_agents,
        "human_approval_required": False,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Security Requirements Review — document intake and security analysis tool"
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to the design document (.md, .txt, .json, .yaml, .pdf, .docx)",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="json",
        help="Output format (default: json)",
    )
    args = parser.parse_args()

    # Validate input file
    input_path = Path(args.input)
    if not input_path.exists():
        msg = {"error": f"Input file not found: {args.input}"}
        if args.output == "json":
            print(json.dumps(msg, indent=2))
        else:
            print(f"ERROR: {msg['error']}", file=sys.stderr)
        return 1

    if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        msg = {
            "error": f"Unsupported file extension: {input_path.suffix}",
            "supported": sorted(SUPPORTED_EXTENSIONS),
        }
        if args.output == "json":
            print(json.dumps(msg, indent=2))
        else:
            print(f"ERROR: {msg['error']}", file=sys.stderr)
        return 1

    # Step 1: Extract text
    intake = run_doc_intake(str(input_path))

    if "error" in intake and not intake.get("text"):
        error_payload = {
            "agent_slug": SKILL_SLUG,
            "intent_type": "escalate",
            "action": "Manual document extraction required — automated extraction failed.",
            "rationale": intake["error"],
            "confidence": 0.0,
            "severity": "informational",
            "key_findings": [f"Extraction failed: {intake['error']}"],
            "evidence_references": [],
            "next_agents": [],
            "human_approval_required": False,
            "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
        if args.output == "json":
            print(json.dumps(error_payload, indent=2))
        else:
            print(f"Extraction error: {intake['error']}")
        return 1

    text = intake.get("text", "")

    # Step 2: Run pre_analysis
    analysis, pre_exit_code = run_pre_analysis(text)

    # Step 3: Build output
    output = build_output(str(input_path), intake, analysis)

    if args.output == "json":
        print(json.dumps(output, indent=2))
    else:
        print(f"Security Requirements Review — {output['severity'].upper()}")
        print(f"Document type: {output['document_metadata']['document_type']}")
        print(f"Action: {output['action']}")
        print(f"Confidence: {output['confidence']}")
        print(f"Key findings ({len(output['key_findings'])}):")
        for finding in output["key_findings"]:
            print(f"  - {finding}")
        print(f"Next agents: {output['next_agents']}")

    # Mirror pre_analysis exit code so callers can check severity programmatically
    return pre_exit_code


if __name__ == "__main__":
    raise SystemExit(main())
