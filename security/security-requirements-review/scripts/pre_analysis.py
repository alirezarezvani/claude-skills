#!/usr/bin/env python3
"""
pre_analysis.py — Deterministic document classifier and entity extractor.

Reads raw document text from stdin (plain string or JSON with 'document_text' key).
Outputs a JSON classification result to stdout.

Exit codes:
  0 — informational or low findings only
  1 — security design gaps detected (high findings)
  2 — critical architecture issues (no auth, exposed data, hardcoded creds)
"""

import argparse
import json
import re
import sys

# ---------------------------------------------------------------------------
# Classification keyword tables
# ---------------------------------------------------------------------------

DOC_TYPE_SIGNALS = {
    "poam": [
        "plan of action", "poam", "poa&m", "corrective action", "milestones",
        "weakness", "scheduled completion", "deviation", "control deficiency",
        "finding id", "remediation date",
    ],
    "prd": [
        "product requirements", "user story", "acceptance criteria", "feature",
        "release", "mvp", "roadmap", "persona", "use case", "epic",
        "as a user", "so that", "given when then", "product owner",
    ],
    "architecture": [
        "architecture", "system design", "component", "service mesh",
        "microservice", "data flow", "trust boundary", "dmz", "network diagram",
        "api gateway", "load balancer", "infrastructure", "deployment diagram",
        "sequence diagram", "c4 model", "containerized",
    ],
    "project_plan": [
        "project plan", "sprint", "milestone", "gantt", "wbs",
        "work breakdown", "deliverable", "timeline", "go-live", "phase gate",
        "project schedule", "resource plan",
    ],
    "requirements_spec": [
        "shall", "must", "functional requirement", "non-functional requirement",
        "system requirement", "srs", "software requirements specification",
        "interface requirement", "the system shall", "the system must",
    ],
}

FRAMEWORK_SIGNALS = {
    "PCI DSS": [
        "cardholder", "pan", "payment", "card data", "chd", "cde",
        "pci", "pci dss", "pci-dss",
    ],
    "GDPR": [
        "personal data", "data subject", "consent", "right to erasure",
        "dpa", "dpia", "gdpr", "general data protection",
    ],
    "HIPAA": [
        "phi", "protected health", "ephi", "covered entity", "baa",
        "hipaa", "health insurance portability",
    ],
    "SOC 2": [
        "trust service criteria", "availability", "processing integrity",
        "soc 2", "soc2", "aicpa",
    ],
    "FedRAMP": [
        "federal", "government", "fisma", "ato", "authorization to operate",
        "fedramp", "nist sp 800-53",
    ],
    "NIST CSF": [
        "identify", "protect", "detect", "respond", "recover",
        "csf", "cybersecurity framework", "nist csf",
    ],
}

DATA_FLOW_TERMS = [
    "data flow", "dfd", "flows to", "sends to", "receives from",
    "pipeline", "stream", "data pipeline", "message queue",
    "event bus", "api call", "http request", "data transfer",
]

TRUST_BOUNDARY_TERMS = [
    "trust boundary", "dmz", "zone", "network segment", "perimeter",
    "firewall", "api gateway", "ingress", "egress", "security group",
    "network policy", "zero trust",
]

TECH_KEYWORDS = [
    "kubernetes", "docker", "aws", "azure", "gcp", "terraform", "ansible",
    "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "kafka",
    "rabbitmq", "node.js", "python", "java", "golang", "rust", "react",
    "angular", "vue", "django", "fastapi", "spring", "rails", "nginx",
    "apache", "lambda", "s3", "rds", "dynamodb", "cognito", "iam",
    "cloudfront", "waf", "github actions", "gitlab ci", "jenkins",
]

# Critical security signals that trigger exit code 2
CRITICAL_SIGNALS = [
    r"no authentication",
    r"no auth",
    r"unauthenticated",
    r"without authentication",
    r"public endpoint",
    r"admin endpoint",
    r"hardcoded",
    r"hard-coded",
    r"password\s*[=:]\s*['\"]?\w",
    r"secret\s*[=:]\s*['\"]?\w",
    r"api[_-]?key\s*[=:]\s*['\"]?\w",
    r"no encryption",
    r"plaintext",
    r"plain text",
    r"unencrypted",
    r"no tls",
    r"http://",
]

# Control keywords that indicate a framework obligation has a matching control
CONTROL_KEYWORDS = [
    "encrypt", "tokeniz", "hash", "tls", "ssl", "https",
    "authentication", "authorization", "rbac", "mfa", "2fa",
    "audit log", "access control", "firewall", "waf",
    "penetration test", "vulnerability scan", "patch",
]


# ---------------------------------------------------------------------------
# Analysis functions
# ---------------------------------------------------------------------------

def classify_document_type(text: str) -> str:
    """Return the best-matching document type from DOC_TYPE_SIGNALS."""
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for doc_type, signals in DOC_TYPE_SIGNALS.items():
        score = sum(1 for signal in signals if signal in text_lower)
        scores[doc_type] = score
    best = max(scores, key=lambda k: scores[k])
    return best if scores[best] > 0 else "unknown"


def detect_frameworks(text: str) -> list[str]:
    """Return all compliance frameworks whose keyword signals appear in the text."""
    text_lower = text.lower()
    detected = []
    for framework, signals in FRAMEWORK_SIGNALS.items():
        if any(signal in text_lower for signal in signals):
            detected.append(framework)
    return detected


def detect_data_flows(text: str) -> bool:
    """Return True if any data flow terminology is found."""
    text_lower = text.lower()
    return any(term in text_lower for term in DATA_FLOW_TERMS)


def detect_trust_boundaries(text: str) -> bool:
    """Return True if any trust boundary terminology is found."""
    text_lower = text.lower()
    return any(term in text_lower for term in TRUST_BOUNDARY_TERMS)


def extract_technology_keywords(text: str) -> list[str]:
    """Return all detected technology stack terms."""
    text_lower = text.lower()
    return [kw for kw in TECH_KEYWORDS if kw in text_lower]


def find_critical_keywords(text: str) -> list[str]:
    """Return all critical security signal matches found in the text."""
    matches = []
    for pattern in CRITICAL_SIGNALS:
        found = re.search(pattern, text, re.IGNORECASE)
        if found:
            matches.append(found.group(0).strip())
    return list(set(matches))


def detect_compliance_gaps(text: str, frameworks: list[str]) -> list[str]:
    """
    For each detected framework, check whether any control keywords are present.
    Return a list of framework names where obligations appear without controls.
    """
    text_lower = text.lower()
    has_controls = any(kw in text_lower for kw in CONTROL_KEYWORDS)
    gaps = []
    if not has_controls:
        gaps.extend(frameworks)
    return gaps


def assign_exit_code(critical_keywords: list[str], compliance_gaps: list[str], frameworks: list[str]) -> int:
    """
    0 — informational/low only
    1 — design gaps (frameworks detected with gaps, or compliance gaps)
    2 — critical issues (critical keywords found)
    """
    if critical_keywords:
        return 2
    if compliance_gaps or frameworks:
        return 1
    return 0


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    raw_input = sys.stdin.read().strip()
    if not raw_input:
        error = {"error": "No input provided on stdin", "exit_code": 1}
        print(json.dumps(error, indent=2))
        return 1

    # Accept either a plain text string or JSON with 'document_text'
    text = raw_input
    try:
        parsed = json.loads(raw_input)
        if isinstance(parsed, dict):
            text = parsed.get("document_text", raw_input)
        elif isinstance(parsed, str):
            text = parsed
    except (json.JSONDecodeError, ValueError):
        # Not JSON — treat as plain text
        text = raw_input

    document_type = classify_document_type(text)
    detected_frameworks = detect_frameworks(text)
    has_data_flows = detect_data_flows(text)
    has_trust_boundaries = detect_trust_boundaries(text)
    technology_keywords = extract_technology_keywords(text)
    critical_keywords = find_critical_keywords(text)
    compliance_gaps = detect_compliance_gaps(text, detected_frameworks)

    exit_code = assign_exit_code(critical_keywords, compliance_gaps, detected_frameworks)

    result = {
        "document_type": document_type,
        "detected_frameworks": detected_frameworks,
        "has_data_flows": has_data_flows,
        "has_trust_boundaries": has_trust_boundaries,
        "technology_keywords": technology_keywords,
        "critical_keywords": critical_keywords,
        "compliance_gaps": compliance_gaps,
        "exit_code": exit_code,
        "severity_hint": {2: "critical", 1: "high", 0: "informational"}[exit_code],
    }

    print(json.dumps(result, indent=2))
    return exit_code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
