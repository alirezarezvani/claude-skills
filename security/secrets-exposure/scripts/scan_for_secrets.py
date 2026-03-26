#!/usr/bin/env python3
"""
scan_for_secrets.py — USAP Secrets Exposure Scanner

Scans a directory or file for exposed credentials using regex patterns
and Shannon entropy analysis. Produces SecurityFact-compatible JSON
findings for the secrets-exposure agent reasoning pipeline.

Usage:
    python scan_for_secrets.py /path/to/scan
    python scan_for_secrets.py /path/to/scan --severity high
    python scan_for_secrets.py /path/to/scan --json --output findings.json
    python scan_for_secrets.py /path/to/scan --exclude "*.test.*,*.example"

Exit codes:
    0  No findings at or above threshold
    1  High-severity findings (service_scoped blast radius)
    2  Critical findings (full_account blast radius — immediate action required)
"""

import argparse
import json
import math
import os
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple


# ── Secret pattern registry ───────────────────────────────────────────────────

@dataclass
class SecretPattern:
    type: str
    regex: str
    blast_radius: str        # full_account | service_scoped | minimal
    base_confidence: float   # confidence on regex match alone
    entropy_threshold: float # 0.0 = no entropy check; >0 = must exceed this
    capture_group: int       # which regex group holds the secret value
    description: str
    mitre_technique: str


PATTERNS: List[SecretPattern] = [
    SecretPattern(
        type="aws_access_key",
        regex=r"(AKIA[0-9A-Z]{16})",
        blast_radius="full_account",
        base_confidence=0.92,
        entropy_threshold=0.0,
        capture_group=1,
        description="AWS IAM Access Key ID — grants API access to AWS account",
        mitre_technique="T1552.005 Unsecured Credentials: Cloud Instance Metadata",
    ),
    SecretPattern(
        type="aws_secret_key",
        regex=r"(?i)aws[_\-\s]?secret[_\-\s]?(?:access[_\-\s]?)?key['\"]?\s*[=:]\s*['\"]?([A-Za-z0-9/+]{40})['\"]?",
        blast_radius="full_account",
        base_confidence=0.85,
        entropy_threshold=4.5,
        capture_group=1,
        description="AWS IAM Secret Access Key — paired with access key for full API auth",
        mitre_technique="T1552.005 Unsecured Credentials: Cloud Instance Metadata",
    ),
    SecretPattern(
        type="github_pat_classic",
        regex=r"(ghp_[A-Za-z0-9]{36})",
        blast_radius="service_scoped",
        base_confidence=0.97,
        entropy_threshold=0.0,
        capture_group=1,
        description="GitHub Personal Access Token (classic) — repo and account access",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="github_oauth_token",
        regex=r"(gho_[A-Za-z0-9]{36})",
        blast_radius="service_scoped",
        base_confidence=0.97,
        entropy_threshold=0.0,
        capture_group=1,
        description="GitHub OAuth App Token",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="github_actions_token",
        regex=r"(ghs_[A-Za-z0-9]{36})",
        blast_radius="service_scoped",
        base_confidence=0.97,
        entropy_threshold=0.0,
        capture_group=1,
        description="GitHub Actions workflow token",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="stripe_live_key",
        regex=r"(sk_live_[A-Za-z0-9]{24,})",
        blast_radius="full_account",
        base_confidence=0.98,
        entropy_threshold=0.0,
        capture_group=1,
        description="Stripe Live Secret Key — full payment processing and cardholder data access",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="stripe_test_key",
        regex=r"(sk_test_[A-Za-z0-9]{24,})",
        blast_radius="minimal",
        base_confidence=0.98,
        entropy_threshold=0.0,
        capture_group=1,
        description="Stripe Test Secret Key — test environment only, low risk",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="slack_bot_token",
        regex=r"(xoxb-[0-9]{10,13}-[0-9]{10,13}-[a-zA-Z0-9]{24})",
        blast_radius="service_scoped",
        base_confidence=0.97,
        entropy_threshold=0.0,
        capture_group=1,
        description="Slack Bot OAuth Token — full workspace API access",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="slack_user_token",
        regex=r"(xoxp-[0-9]+-[0-9]+-[0-9]+-[a-f0-9]{32})",
        blast_radius="service_scoped",
        base_confidence=0.97,
        entropy_threshold=0.0,
        capture_group=1,
        description="Slack User OAuth Token — user-level workspace access",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="google_api_key",
        regex=r"(AIza[0-9A-Za-z\-_]{35})",
        blast_radius="service_scoped",
        base_confidence=0.92,
        entropy_threshold=0.0,
        capture_group=1,
        description="Google API Key — scope depends on enabled APIs",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="private_key_pem",
        regex=r"(-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----)",
        blast_radius="full_account",
        base_confidence=0.99,
        entropy_threshold=0.0,
        capture_group=1,
        description="PEM Private Key — access depends on associated certificate/system",
        mitre_technique="T1552.004 Unsecured Credentials: Private Keys",
    ),
    SecretPattern(
        type="sendgrid_api_key",
        regex=r"(SG\.[A-Za-z0-9._]{66,})",
        blast_radius="service_scoped",
        base_confidence=0.98,
        entropy_threshold=0.0,
        capture_group=1,
        description="SendGrid API Key — full email sending and contact list access",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="database_connection_string",
        regex=r"((?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis):\/\/[^:'\"\s]+:[^@'\"\s]{8,}@[a-zA-Z0-9.\-]+)",
        blast_radius="service_scoped",
        base_confidence=0.92,
        entropy_threshold=0.0,
        capture_group=1,
        description="Database connection string with embedded credentials",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="jwt_secret",
        regex=r"(?i)jwt[_\-]?secret['\"]?\s*[=:]\s*['\"]([A-Za-z0-9!@#$%^&*()\-_+=]{32,})['\"]",
        blast_radius="service_scoped",
        base_confidence=0.82,
        entropy_threshold=4.0,
        capture_group=1,
        description="JWT signing secret — allows forging of authentication tokens",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
    SecretPattern(
        type="generic_api_secret",
        regex=r"(?i)(?:api_key|api_secret|auth_token|secret_key|access_token|private_key)\s*[=:]\s*['\"]([A-Za-z0-9!@#$%^&*\-_+=]{20,})['\"]",
        blast_radius="service_scoped",
        base_confidence=0.62,
        entropy_threshold=4.2,
        capture_group=1,
        description="Generic named secret — context-dependent blast radius",
        mitre_technique="T1552.001 Unsecured Credentials: Credentials in Files",
    ),
]

# ── False positive detection ──────────────────────────────────────────────────

FP_VALUE_PATTERN = re.compile(
    r"example|placeholder|your[_\-]?(?:key|secret|token)|replace[_\-]?me|"
    r"todo|xxxx|dummy|fake|test123|password123|changeme|insert[_\-]?here|"
    r"<[a-z_]+>|\$\{[a-z_]+\}|\$\([a-z_]+\)|REPLACE|INSERT|CHANGE|"
    r"sample|demo|staging_key|dev_key",
    re.IGNORECASE,
)

FP_PATH_PATTERN = re.compile(
    r"/__tests__/|/spec/|/test/|\.test\.|\.spec\.|/mock/|/fixture|"
    r"/node_modules/|/\.git/|\.example$|\.sample$|\.template$",
    re.IGNORECASE,
)

SKIP_EXTENSIONS = frozenset({
    ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".ico", ".svg", ".webp",
    ".pdf", ".docx", ".xlsx", ".pptx", ".zip", ".tar", ".gz", ".bz2",
    ".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".class", ".wasm",
    ".woff", ".woff2", ".ttf", ".eot", ".mp4", ".mp3", ".wav", ".avi",
    ".lock",  # package-lock.json IS worth scanning; .lock for Cargo/Gemfile is not
})

SKIP_DIRS = frozenset({
    "node_modules", ".git", ".venv", "venv", "env", "__pycache__",
    ".mypy_cache", ".pytest_cache", "dist", "build", ".next", ".nuxt",
    "vendor", ".terraform", "coverage", ".coverage",
})


# ── Shannon entropy ───────────────────────────────────────────────────────────

def shannon_entropy(value: str) -> float:
    """Calculate Shannon entropy of a string (bits per character)."""
    if not value:
        return 0.0
    freq: Dict[str, int] = {}
    for ch in value:
        freq[ch] = freq.get(ch, 0) + 1
    n = len(value)
    return -sum((c / n) * math.log2(c / n) for c in freq.values())


# ── Finding dataclass ─────────────────────────────────────────────────────────

@dataclass
class SecretFinding:
    secret_type: str
    file_path: str
    line_number: int
    matched_value_redacted: str   # first 8 chars + "..." for safe logging
    blast_radius: str
    confidence: float
    entropy: float
    is_false_positive: bool
    false_positive_reason: str
    description: str
    mitre_technique: str
    recommended_action: str
    intent_type: str
    mutating_category: Optional[str]


@dataclass
class ScanReport:
    scan_target: str
    timestamp_utc: str
    files_scanned: int
    findings: List[SecretFinding]
    critical_count: int       # full_account, not FP, confidence >= 0.70
    high_count: int           # service_scoped, not FP, confidence >= 0.70
    informational_count: int  # FP candidates or low confidence
    overall_risk: str         # critical | high | medium | low | clean
    recommended_action: str
    intent_type: str
    mutating_category: Optional[str]


# ── Scoring and classification ────────────────────────────────────────────────

def redact(value: str) -> str:
    if len(value) <= 8:
        return "****"
    return value[:8] + "..." + value[-4:]


def detect_false_positive(value: str, file_path: str, line: str) -> Tuple[bool, str]:
    """Returns (is_false_positive, reason)."""
    if FP_VALUE_PATTERN.search(value):
        return True, "value matches placeholder/example pattern"
    if FP_PATH_PATTERN.search(file_path):
        return True, "file is in test/mock/fixture directory"
    # Low unique character ratio (repeated chars = likely dummy)
    unique_ratio = len(set(value)) / max(len(value), 1)
    if len(value) >= 16 and unique_ratio < 0.15:
        return True, f"low character diversity (unique ratio {unique_ratio:.2f}) — likely dummy value"
    # Comment line
    stripped = line.strip()
    if stripped.startswith(("#", "//", "*", "<!--", "--")):
        return True, "value appears on a comment line"
    return False, ""


def adjust_confidence(
    pattern: SecretPattern,
    value: str,
    file_path: str,
    line: str,
    is_fp: bool,
) -> float:
    conf = pattern.base_confidence

    if is_fp:
        return min(conf, 0.15)

    # Entropy check
    if pattern.entropy_threshold > 0.0:
        ent = shannon_entropy(value)
        if ent < pattern.entropy_threshold:
            conf = min(conf, 0.55)

    # Context boosters: production indicators
    ctx = line.lower()
    path_lower = file_path.lower()

    if ".env" in path_lower and ".example" not in path_lower and ".sample" not in path_lower:
        conf = min(1.0, conf + 0.05)  # .env files are high-confidence

    if any(kw in ctx for kw in ("production", "prod_", "_prod", "live_", "_live")):
        conf = min(1.0, conf + 0.04)

    if any(kw in ctx for kw in ("# example", "# replace", "your_", "TODO")):
        conf = max(0.0, conf - 0.20)

    return round(conf, 3)


def classify_intent(blast_radius: str, confidence: float) -> Tuple[str, Optional[str]]:
    if confidence >= 0.70 and blast_radius in ("full_account", "service_scoped"):
        return "mutating", "credential_operation"
    return "read_only", None


def choose_action(blast_radius: str, confidence: float, is_fp: bool) -> str:
    if is_fp:
        return "verify_false_positive"
    if confidence < 0.60:
        return "manual_review"
    if blast_radius == "full_account":
        return "rotate_and_revoke_immediately"
    if blast_radius == "service_scoped":
        return "rotate_and_revoke"
    return "verify_scope"  # minimal


# ── File scanner ──────────────────────────────────────────────────────────────

def scan_file(file_path: Path) -> List[SecretFinding]:
    """Scan a single file for secrets. Returns list of findings."""
    findings: List[SecretFinding] = []
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except (OSError, PermissionError):
        return []

    lines = content.splitlines()
    path_str = str(file_path)

    for pattern in PATTERNS:
        compiled = re.compile(pattern.regex)
        for line_no, line in enumerate(lines, start=1):
            for match in compiled.finditer(line):
                try:
                    raw_value = match.group(pattern.capture_group) or match.group(0)
                except IndexError:
                    raw_value = match.group(0)

                if not raw_value:
                    continue

                is_fp, fp_reason = detect_false_positive(raw_value, path_str, line)
                entropy = shannon_entropy(raw_value)
                confidence = adjust_confidence(pattern, raw_value, path_str, line, is_fp)
                intent, mut_cat = classify_intent(pattern.blast_radius, confidence)
                action = choose_action(pattern.blast_radius, confidence, is_fp)

                findings.append(SecretFinding(
                    secret_type=pattern.type,
                    file_path=path_str,
                    line_number=line_no,
                    matched_value_redacted=redact(raw_value),
                    blast_radius=pattern.blast_radius,
                    confidence=confidence,
                    entropy=round(entropy, 2),
                    is_false_positive=is_fp,
                    false_positive_reason=fp_reason,
                    description=pattern.description,
                    mitre_technique=pattern.mitre_technique,
                    recommended_action=action,
                    intent_type=intent,
                    mutating_category=mut_cat,
                ))

    return findings


def _severity_rank(f: SecretFinding) -> int:
    """Numeric rank for filtering by severity threshold."""
    if f.is_false_positive or f.blast_radius == "minimal":
        return 0
    if f.confidence < 0.70:
        return 1
    if f.blast_radius == "service_scoped":
        return 2
    return 3  # full_account


_SEVERITY_RANKS = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def scan_directory(target: Path, min_severity: str = "low") -> ScanReport:
    """Walk a directory and scan all text files."""
    min_rank = _SEVERITY_RANKS.get(min_severity, 0)
    all_findings: List[SecretFinding] = []
    files_scanned = 0

    for root, dirs, files in os.walk(target):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            fpath = Path(root) / fname
            if fpath.suffix.lower() in SKIP_EXTENSIONS:
                continue
            file_findings = scan_file(fpath)
            all_findings.extend(file_findings)
            files_scanned += 1

    visible = [f for f in all_findings if _severity_rank(f) >= min_rank]

    critical = sum(
        1 for f in all_findings
        if not f.is_false_positive and f.blast_radius == "full_account" and f.confidence >= 0.70
    )
    high = sum(
        1 for f in all_findings
        if not f.is_false_positive and f.blast_radius == "service_scoped" and f.confidence >= 0.70
    )
    informational = len(all_findings) - critical - high

    if critical > 0:
        risk = "critical"
        intent = "mutating"
        mut_cat = "credential_operation"
        action = "rotate_and_revoke_immediately"
    elif high > 0:
        risk = "high"
        intent = "mutating"
        mut_cat = "credential_operation"
        action = "rotate_and_revoke"
    elif informational > 0:
        risk = "low"
        intent = "read_only"
        mut_cat = None
        action = "verify_scope"
    else:
        risk = "clean"
        intent = "read_only"
        mut_cat = None
        action = "no_action_required"

    return ScanReport(
        scan_target=str(target),
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        files_scanned=files_scanned,
        findings=visible,
        critical_count=critical,
        high_count=high,
        informational_count=informational,
        overall_risk=risk,
        recommended_action=action,
        intent_type=intent,
        mutating_category=mut_cat,
    )


# ── Text report ───────────────────────────────────────────────────────────────

_COLORS = {
    "critical": "\033[91m",
    "high":     "\033[33m",
    "medium":   "\033[36m",
    "low":      "\033[37m",
    "clean":    "\033[92m",
}
_RESET = "\033[0m"


def print_text_report(report: ScanReport) -> None:
    color = _COLORS.get(report.overall_risk, "")
    print(f"\nUSAP Secrets Scanner")
    print(f"Target  : {report.scan_target}")
    print(f"Scanned : {report.files_scanned} files  |  {report.timestamp_utc}")
    print(f"Risk    : {color}{report.overall_risk.upper()}{_RESET}  "
          f"Critical: {report.critical_count}  High: {report.high_count}  "
          f"Informational: {report.informational_count}")
    print(f"Intent  : {report.intent_type}"
          + (f"  Category: {report.mutating_category}" if report.mutating_category else ""))
    print(f"Action  : {report.recommended_action}")
    print()

    if not report.findings:
        print(f"{_COLORS['clean']}No findings at or above threshold.{_RESET}")
        return

    for idx, f in enumerate(report.findings, start=1):
        if f.blast_radius == "full_account" and not f.is_false_positive:
            sev_color = _COLORS["critical"]
        elif f.blast_radius == "service_scoped" and not f.is_false_positive:
            sev_color = _COLORS["high"]
        else:
            sev_color = _COLORS["low"]

        fp_tag = "  [LIKELY FALSE POSITIVE]" if f.is_false_positive else ""
        print(f"  [{idx:03d}] {sev_color}{f.secret_type}{_RESET}{fp_tag}")
        print(f"        File    : {f.file_path}:{f.line_number}")
        print(f"        Value   : {f.matched_value_redacted}")
        print(f"        Blast   : {sev_color}{f.blast_radius}{_RESET}  "
              f"Conf: {f.confidence:.3f}  Entropy: {f.entropy:.2f}")
        print(f"        Action  : {f.recommended_action}  Intent: {f.intent_type}")
        print(f"        MITRE   : {f.mitre_technique}")
        if f.false_positive_reason:
            print(f"        FP Note : {f.false_positive_reason}")
        print()


# ── JSON serialization ────────────────────────────────────────────────────────

def report_to_dict(report: ScanReport) -> dict:
    return {
        "scan_target": report.scan_target,
        "timestamp_utc": report.timestamp_utc,
        "files_scanned": report.files_scanned,
        "overall_risk": report.overall_risk,
        "critical_count": report.critical_count,
        "high_count": report.high_count,
        "informational_count": report.informational_count,
        "recommended_action": report.recommended_action,
        "intent_type": report.intent_type,
        "mutating_category": report.mutating_category,
        "findings": [
            {
                "secret_type": f.secret_type,
                "file_path": f.file_path,
                "line_number": f.line_number,
                "matched_value_redacted": f.matched_value_redacted,
                "blast_radius": f.blast_radius,
                "confidence": f.confidence,
                "entropy": f.entropy,
                "is_false_positive": f.is_false_positive,
                "false_positive_reason": f.false_positive_reason,
                "description": f.description,
                "mitre_technique": f.mitre_technique,
                "recommended_action": f.recommended_action,
                "intent_type": f.intent_type,
                "mutating_category": f.mutating_category,
            }
            for f in report.findings
        ],
    }


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="USAP Secrets Scanner — detect exposed credentials in source code",
        epilog="Exit codes: 0=clean, 1=high findings, 2=critical findings",
    )
    parser.add_argument("target", help="Directory or file to scan")
    parser.add_argument(
        "--severity", "-s",
        choices=["low", "medium", "high", "critical"],
        default="low",
        help="Minimum severity to include in results (default: low)",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--output", "-o", metavar="FILE", help="Write JSON to file (requires --json)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show each file as it is scanned")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"ERROR: Target path does not exist: {target}", file=sys.stderr)
        return 2

    if target.is_file():
        findings = scan_file(target)
        critical = sum(1 for f in findings if not f.is_false_positive and f.blast_radius == "full_account" and f.confidence >= 0.70)
        high = sum(1 for f in findings if not f.is_false_positive and f.blast_radius == "service_scoped" and f.confidence >= 0.70)
        info = len(findings) - critical - high
        if critical > 0:
            risk, intent, mut_cat, action = "critical", "mutating", "credential_operation", "rotate_and_revoke_immediately"
        elif high > 0:
            risk, intent, mut_cat, action = "high", "mutating", "credential_operation", "rotate_and_revoke"
        else:
            risk, intent, mut_cat, action = "clean", "read_only", None, "no_action_required"
        report = ScanReport(
            scan_target=str(target),
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            files_scanned=1,
            findings=findings,
            critical_count=critical,
            high_count=high,
            informational_count=info,
            overall_risk=risk,
            recommended_action=action,
            intent_type=intent,
            mutating_category=mut_cat,
        )
    else:
        report = scan_directory(target, min_severity=args.severity)

    if args.json:
        output_str = json.dumps(report_to_dict(report), indent=2)
        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"Results written to {args.output}")
        else:
            print(output_str)
    else:
        print_text_report(report)

    # Exit codes for CI/CD integration
    if report.critical_count > 0:
        return 2
    if report.high_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
