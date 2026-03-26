#!/usr/bin/env python3
"""
pre_analysis.py — Secrets Exposure Pre-Analysis

Called by USAP prompt_compiler BEFORE the LLM reasons.
Reads a SecurityFact JSON from stdin, applies deterministic secret detection
(regex + entropy analysis) to all available text fields, and outputs structured
JSON for the LLM to reason on top of.

The LLM then receives algorithmic ground-truth evidence rather than raw event text.

stdin:  SecurityFact JSON dict
stdout: JSON analysis result (injected into prompt as tool_pre_analysis)
exit:   0=clean/no findings, 1=high findings, 2=critical findings
"""


import argparse
import json
import math
import re
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple


# ── Inline pattern definitions (mirror scan_for_secrets.py) ──────────────────

SECRET_PATTERNS = [
    ("aws_access_key",   r"(AKIA[0-9A-Z]{16})",                                        "full_account",   0.92, 0.0),
    ("github_pat",        r"(ghp_[A-Za-z0-9]{36})",                                     "service_scoped", 0.97, 0.0),
    ("github_oauth",      r"(gho_[A-Za-z0-9]{36})",                                     "service_scoped", 0.97, 0.0),
    ("stripe_live_key",   r"(sk_live_[A-Za-z0-9]{24,})",                                "full_account",   0.98, 0.0),
    ("slack_bot_token",   r"(xoxb-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24})",         "service_scoped", 0.97, 0.0),
    ("google_api_key",    r"(AIza[0-9A-Za-z\-_]{35})",                                  "service_scoped", 0.92, 0.0),
    ("private_key_pem",   r"(-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)",        "full_account",   0.99, 0.0),
    ("sendgrid_key",      r"(SG\.[A-Za-z0-9._]{66,})",                                  "service_scoped", 0.98, 0.0),
    ("database_url",      r"((?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis):\/\/[^:'\"\s]+:[^@'\"\s]{8,}@[a-zA-Z0-9.\-]+)", "service_scoped", 0.92, 0.0),
    ("aws_secret_key",    r"(?i)aws[_\-\s]?secret[_\-\s]?(?:access[_\-\s]?)?key['\"]?\s*[=:]\s*['\"]?([A-Za-z0-9/+]{40})['\"]?", "full_account", 0.85, 4.5),
    ("generic_api_secret", r"(?i)(?:api_key|api_secret|auth_token|secret_key|access_token)\s*[=:]\s*['\"]([A-Za-z0-9!@#$%^&*\-_+=]{20,})['\"]", "service_scoped", 0.62, 4.2),
]

# Known high-risk secret type keywords for context scoring
SECRET_TYPE_KEYWORDS = {
    "aws_access_key":   ["aws_access_key", "aws access key", "akia"],
    "aws_secret_key":   ["aws_secret_key", "aws secret", "aws_secret"],
    "github_pat":       ["github_pat", "github token", "ghp_", "github personal access"],
    "stripe_live_key":  ["stripe", "sk_live", "stripe live"],
    "database_url":     ["database_url", "db_url", "connection string", "postgres://", "mysql://"],
    "private_key_pem":  ["private key", "pem", "rsa key", "ssh key"],
    "jwt_secret":       ["jwt_secret", "jwt secret", "signing key"],
}

FP_VALUE_PATTERN = re.compile(
    r"example|placeholder|your[_\-]?(?:key|secret|token)|replace[_\-]?me|"
    r"xxxx|dummy|fake|test123|password123|changeme|<[a-z_]+>|\$\{[a-z_]+\}",
    re.IGNORECASE,
)


def shannon_entropy(s: str) -> float:
    if not s:
        return 0.0
    freq: Dict[str, int] = {}
    for c in s:
        freq[c] = freq.get(c, 0) + 1
    n = len(s)
    return -sum((v / n) * math.log2(v / n) for v in freq.values())


def redact(value: str) -> str:
    if len(value) <= 8:
        return "****"
    return value[:8] + "..." + value[-4:]


def scan_text(text: str) -> List[Dict[str, Any]]:
    """Apply regex patterns to a text string, return list of match dicts."""
    findings = []
    for name, regex, blast_radius, base_conf, entropy_threshold in SECRET_PATTERNS:
        for match in re.finditer(regex, text):
            try:
                value = match.group(1)
            except IndexError:
                value = match.group(0)
            if not value:
                continue

            is_fp = bool(FP_VALUE_PATTERN.search(value))
            ent = shannon_entropy(value)
            conf = base_conf

            if is_fp:
                conf = min(conf, 0.15)
            elif entropy_threshold > 0 and ent < entropy_threshold:
                conf = min(conf, 0.55)

            findings.append({
                "secret_type": name,
                "matched_value_redacted": redact(value),
                "blast_radius": blast_radius,
                "confidence": round(conf, 3),
                "entropy": round(ent, 2),
                "is_false_positive": is_fp,
            })
    return findings


def extract_text_fields(fact: Dict[str, Any]) -> List[Tuple[str, str]]:
    """
    Extract all text fields from the SecurityFact that might contain secrets.
    Returns list of (field_name, text) tuples.
    """
    texts: List[Tuple[str, str]] = []

    # Top-level string fields
    for field in ("finding", "message", "description", "details"):
        val = fact.get(field, "")
        if isinstance(val, str) and val.strip():
            texts.append((field, val))

    # raw_payload fields
    payload = fact.get("raw_payload", {})
    if isinstance(payload, dict):
        for key, val in payload.items():
            if isinstance(val, str) and val.strip():
                texts.append((f"raw_payload.{key}", val))

    # structured_fact fields
    structured = fact.get("structured_fact", {})
    if isinstance(structured, dict):
        for key, val in structured.items():
            if isinstance(val, str) and val.strip():
                texts.append((f"structured_fact.{key}", val))

    return texts


def classify_by_keywords(fact: Dict[str, Any]) -> Tuple[Optional[str], Optional[str], float]:
    """
    If the SecurityFact explicitly states a secret_type, use it to look up
    blast_radius and set a high confidence from the source credibility.
    Returns (secret_type, blast_radius, confidence_from_keywords).
    """
    payload = fact.get("raw_payload", {})
    if not isinstance(payload, dict):
        payload = {}

    # Explicit secret_type field from the scanner that generated this event
    explicit_type = payload.get("secret_type") or payload.get("type")
    source_credibility = float(fact.get("source_credibility", 0.80))

    if explicit_type and isinstance(explicit_type, str):
        explicit_lower = explicit_type.lower()
        # Map to blast radius
        if any(k in explicit_lower for k in ("aws", "stripe_live", "private_key", "pem", "root")):
            blast = "full_account"
        elif any(k in explicit_lower for k in ("stripe_test", "test_")):
            blast = "minimal"
        else:
            blast = "service_scoped"

        # Trust the source scanner — confidence = source_credibility of the fact
        conf = round(min(source_credibility, 0.95), 3)
        return explicit_lower, blast, conf

    # Keyword search across all text
    all_text = " ".join(v for _, v in extract_text_fields(fact)).lower()
    for secret_type, keywords in SECRET_TYPE_KEYWORDS.items():
        if any(kw.lower() in all_text for kw in keywords):
            blast = "full_account" if secret_type in ("aws_access_key", "aws_secret_key", "private_key_pem", "stripe_live_key") else "service_scoped"
            return secret_type, blast, round(source_credibility * 0.85, 3)

    return None, None, 0.0


def assess_urgency(blast_radius: Optional[str], confidence: float, secret_type: Optional[str]) -> str:
    """Map blast_radius + confidence to human urgency label with timeline context."""
    if secret_type == "aws_access_key" and blast_radius == "full_account" and confidence >= 0.70:
        return "IMMEDIATE — AWS keys abused within 4 minutes on average. Backdoor creation possible within 10 minutes."
    if blast_radius == "full_account" and confidence >= 0.70:
        return "CRITICAL — full account blast radius. Rotation must complete before attacker establishes persistence."
    if blast_radius == "service_scoped" and confidence >= 0.70:
        return "HIGH — service-scoped exposure. Rotate within 30 minutes to prevent data exfiltration."
    if confidence < 0.60:
        return "LOW — low confidence, likely false positive. Verify before acting."
    return "MEDIUM — verify scope before rotation."


def main() -> int:
    try:
        raw = sys.stdin.read()
        fact: Dict[str, Any] = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        fact = {}

    timestamp = datetime.now(timezone.utc).isoformat()
    source_credibility = float(fact.get("source_credibility", 0.80))

    # ── 1. Keyword/explicit classification ───────────────────────────────────
    keyword_type, keyword_blast, keyword_conf = classify_by_keywords(fact)

    # ── 2. Regex scanning on all text fields ─────────────────────────────────
    all_findings: List[Dict[str, Any]] = []
    for field_name, text in extract_text_fields(fact):
        findings = scan_text(text)
        for f in findings:
            f["source_field"] = field_name
        all_findings.extend(findings)

    # ── 3. Merge: use highest-confidence finding, boost from keyword evidence ─
    best_type = keyword_type
    best_blast = keyword_blast
    best_conf = keyword_conf

    for f in all_findings:
        if not f["is_false_positive"] and f["confidence"] > best_conf:
            best_type = f["secret_type"]
            best_blast = f["blast_radius"]
            best_conf = f["confidence"]

    # Apply source_credibility as a multiplier when no explicit match
    if best_conf == 0.0 and source_credibility > 0:
        # Even without direct match, the source credibility tells us how much to trust the alert
        best_conf = round(source_credibility * 0.75, 3)
        if not best_blast:
            best_blast = "service_scoped"  # conservative default

    # ── 4. Intent classification ──────────────────────────────────────────────
    if best_conf >= 0.70 and best_blast in ("full_account", "service_scoped"):
        intent_type = "mutating"
        mutating_category = "credential_operation"
        recommended_action = "rotate_and_revoke_immediately" if best_blast == "full_account" else "rotate_and_revoke"
    else:
        intent_type = "read_only"
        mutating_category = None
        recommended_action = "verify_scope" if best_conf >= 0.50 else "verify_false_positive"

    urgency = assess_urgency(best_blast, best_conf, best_type)

    # ── 5. False positive signals ─────────────────────────────────────────────
    fp_signals = []
    all_text = " ".join(v for _, v in extract_text_fields(fact)).lower()
    if any(kw in all_text for kw in ("example", "placeholder", "test", "dummy", "fake")):
        fp_signals.append("text contains placeholder/test keywords")
    if any(f["is_false_positive"] for f in all_findings):
        fp_signals.append("regex match returned likely false positive value")

    # ── 6. Output ─────────────────────────────────────────────────────────────
    output = {
        "analysis_type": "secrets_pre_analysis",
        "timestamp_utc": timestamp,
        "detected_secret_type": best_type,
        "blast_radius": best_blast,
        "confidence": best_conf,
        "intent_type": intent_type,
        "mutating_category": mutating_category,
        "recommended_action": recommended_action,
        "urgency_assessment": urgency,
        "false_positive_signals": fp_signals,
        "regex_matches": all_findings[:10],  # cap at 10 for prompt size
        "source_credibility_used": source_credibility,
        "attacker_timeline_note": (
            "AWS key: abused within 4 min on average. "
            "Backdoor created T+10 min. "
            "CloudTrail disabled T+25 min. "
            "Full account exfil T+45 min."
        ) if best_type == "aws_access_key" else (
            "Refer to attacker_timeline.md for this secret type's specific timeline."
        ),
    }

    print(json.dumps(output))

    if intent_type == "mutating" and best_blast == "full_account":
        return 2
    if intent_type == "mutating":
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pre-analysis helper")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()
    raise SystemExit(main())
