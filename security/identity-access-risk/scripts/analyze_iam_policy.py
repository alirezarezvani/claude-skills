#!/usr/bin/env python3
"""
analyze_iam_policy.py — USAP IAM Policy Analyzer

Parses AWS IAM policy JSON to detect privilege escalation paths, dangerous
action combinations, overprivileged grants, and public exposure. Produces
SecurityFact-compatible findings for the identity-access-risk agent.

Usage:
    python analyze_iam_policy.py policy.json
    python analyze_iam_policy.py policy.json --json
    python analyze_iam_policy.py policy.json --check privilege-escalation
    cat policy.json | python analyze_iam_policy.py -
    python analyze_iam_policy.py policies/ --directory

Exit codes:
    0  No high/critical findings — policy appears appropriately scoped
    1  High-severity findings — overprivileged or risky combinations
    2  Critical findings — privilege escalation or public exposure
"""

import argparse
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


# ── High-risk action definitions ──────────────────────────────────────────────

# Individual actions that create privilege escalation risk when scoped to *
PRIVILEGE_ESCALATION_ACTIONS: Set[str] = {
    # IAM direct escalation
    "iam:passrole",
    "iam:createpolicyversion",
    "iam:setdefaultpolicyversion",
    "iam:attachuserpolicy",
    "iam:attachrolepolicy",
    "iam:attachgrouppolicy",
    "iam:putuserpolicy",
    "iam:putrolepolicy",
    "iam:putgrouppolicy",
    "iam:addusertogroup",
    "iam:updateassumerolepolicy",
    "iam:createaccesskey",
    "iam:updateloginprofile",
    "iam:createloginprofile",
    # STS
    "sts:assumerole",
    "sts:assumeroleWithwebidentity",
    "sts:assumeroleWithsaml",
    # Compute-based escalation (requires PassRole)
    "lambda:createfunction",
    "lambda:updatefunctioncode",
    "lambda:updatefunctionconfiguration",
    "ec2:runinstances",
    "cloudformation:createstack",
    "cloudformation:updatestack",
    "glue:createdevendpoint",
    "glue:updatedevendpoint",
    "codebuild:createproject",
    "codebuild:updateproject",
    "datapipeline:createpipeline",
    "datapipeline:putpipelinedefinition",
    "sagemaker:createtrainingjob",
    "sagemaker:createnotebookinstance",
    "ecs:registertaskdefinition",
    "ecs:runtask",
}

# Dangerous two-action combinations that together enable privilege escalation
# Format: (action_a, action_b, severity, description, mitre_technique)
ESCALATION_COMBOS: List[Tuple[str, str, str, str, str]] = [
    (
        "iam:passrole", "lambda:createfunction",
        "critical",
        "Lambda PassRole escalation: create a Lambda function with a high-privilege execution role. "
        "Attacker invokes function to execute privileged actions under the role's permissions.",
        "T1078.004 Valid Accounts: Cloud Accounts",
    ),
    (
        "iam:passrole", "lambda:updatefunctioncode",
        "critical",
        "Lambda code injection escalation: update an existing Lambda with malicious code that executes "
        "under the function's privileged role.",
        "T1078.004 Valid Accounts: Cloud Accounts",
    ),
    (
        "iam:passrole", "ec2:runinstances",
        "critical",
        "EC2 instance profile escalation: launch an EC2 instance attached to a high-privilege IAM role. "
        "Instance metadata service (IMDS) exposes role credentials.",
        "T1078.004 Valid Accounts: Cloud Accounts",
    ),
    (
        "iam:passrole", "cloudformation:createstack",
        "critical",
        "CloudFormation PassRole escalation: deploy a stack with a privileged service role. "
        "Stack resources inherit the role's permissions during creation.",
        "T1078.004 Valid Accounts: Cloud Accounts",
    ),
    (
        "iam:passrole", "glue:createdevendpoint",
        "high",
        "Glue dev endpoint PassRole escalation: create a development endpoint with a privileged role, "
        "then attach notebooks with arbitrary code execution.",
        "T1078.004 Valid Accounts: Cloud Accounts",
    ),
    (
        "iam:createaccesskey", "iam:listusers",
        "high",
        "Credential harvesting: enumerate all IAM users then create persistent access keys for any of them.",
        "T1098.001 Account Manipulation: Additional Cloud Credentials",
    ),
    (
        "iam:attachuserpolicy", "sts:getcalleridentity",
        "critical",
        "Self-attach policy escalation: discover own identity then attach AdministratorAccess to self.",
        "T1484.001 Domain Policy Modification: Group Policy Modification",
    ),
    (
        "iam:putuserpolicy", "sts:getcalleridentity",
        "critical",
        "Inline policy self-escalation: discover own username then write an inline policy with Action:* "
        "to grant unrestricted access.",
        "T1484.001 Domain Policy Modification: Group Policy Modification",
    ),
    (
        "iam:updateloginprofile", "iam:listusers",
        "high",
        "Password reset attack: enumerate users and reset console passwords to gain interactive access "
        "as privileged users.",
        "T1098 Account Manipulation",
    ),
    (
        "iam:addusertogroup", "iam:listgroups",
        "high",
        "Group membership escalation: discover admin groups then add attacker's user to gain "
        "all permissions inherited by the group.",
        "T1098 Account Manipulation",
    ),
    (
        "iam:createpolicyversion", "iam:listpolicies",
        "critical",
        "Policy version backdoor: enumerate policies, find one attached to a privileged role, "
        "then create a new version with Action:* to backdoor the role.",
        "T1484.001 Domain Policy Modification",
    ),
    (
        "iam:setdefaultpolicyversion", "iam:listpolicyversions",
        "high",
        "Policy version rollback: revert an existing policy to a previously overprivileged version.",
        "T1484.001 Domain Policy Modification",
    ),
]

# Data exfiltration high-value actions
DATA_EXFILTRATION_ACTIONS: Set[str] = {
    "s3:getobject", "s3:listbucket", "s3:getbucketacl", "s3:listallmybuckets",
    "rds:describedbinstances", "rds:downloaddblogfileportion", "rds-db:connect",
    "dynamodb:scan", "dynamodb:query", "dynamodb:getitem",
    "secretsmanager:getsecretvalue", "secretsmanager:listsecrets",
    "ssm:getparameter", "ssm:getparameters", "ssm:getparameterhistory",
    "ssm:describeinstanceinformation",
    "kms:decrypt", "kms:generatedatakey",
    "lambda:getfunction",  # can retrieve environment variables with secrets
    "ecr:getauthorizationtoken", "ecr:batchgetimage",
    "cloudwatch:getmetricdata", "logs:filterlogevents", "logs:getlogevents",
}


# ── Finding dataclass ─────────────────────────────────────────────────────────

@dataclass
class IAMFinding:
    severity: str                # critical | high | medium | low
    finding_type: str            # privilege_escalation | public_exposure | data_exfil_risk | overprivileged
    statement_sid: str
    actions_involved: List[str]
    resource: str
    description: str
    attack_path: str
    recommended_action: str
    intent_type: str             # always mutating for high/critical
    mutating_category: str       # always policy_change
    mitre_technique: str
    least_privilege_suggestion: str


@dataclass
class IAMAnalysisResult:
    policy_source: str
    timestamp_utc: str
    statements_analyzed: int
    findings: List[IAMFinding]
    critical_count: int
    high_count: int
    medium_count: int
    overall_risk: str
    blast_radius: str
    anomaly_types: List[str]
    recommended_action: str
    intent_type: str
    mutating_category: Optional[str]


# ── Analysis logic ────────────────────────────────────────────────────────────

def normalize_actions(actions) -> List[str]:
    """Normalize to a list of lowercase action strings."""
    if isinstance(actions, str):
        return [actions.lower()]
    return [a.lower() for a in actions]


def is_wildcard_resource(resource) -> bool:
    if isinstance(resource, str):
        return resource == "*"
    if isinstance(resource, list):
        return "*" in resource
    return False


def is_public_principal(principal) -> bool:
    if principal is None:
        return False
    if principal == "*":
        return True
    if isinstance(principal, dict):
        aws = principal.get("AWS", "")
        fed = principal.get("Federated", "")
        svc = principal.get("Service", "")
        if aws == "*" or fed == "*" or svc == "*":
            return True
        if isinstance(aws, list) and "*" in aws:
            return True
    return False


def analyze_statement(stmt: dict) -> List[IAMFinding]:
    """Analyze a single IAM statement and return findings."""
    findings: List[IAMFinding] = []

    effect = stmt.get("Effect", "Allow")
    if effect != "Allow":
        return []  # Deny statements don't create escalation risk

    actions = normalize_actions(stmt.get("Action", []))
    resource = stmt.get("Resource", "*")
    resource_str = resource if isinstance(resource, str) else (resource[0] if resource else "*")
    sid = stmt.get("Sid", "")
    principal = stmt.get("Principal", None)
    wildcard_resource = is_wildcard_resource(resource)

    action_set = set(actions)

    # ── Check 1: Full admin wildcard ──────────────────────────────────────────
    if "*" in action_set and wildcard_resource:
        findings.append(IAMFinding(
            severity="critical",
            finding_type="privilege_escalation",
            statement_sid=sid,
            actions_involved=["*"],
            resource=resource_str,
            description="Full AdministratorAccess: Action=* Resource=* grants unrestricted access to all AWS APIs",
            attack_path=(
                "Any identity with this policy has complete AWS account control. "
                "Attacker can: create persistent IAM backdoors, exfiltrate all data from S3/RDS/DynamoDB, "
                "launch EC2 instances for crypto mining, delete all resources, and disable CloudTrail logging. "
                "No additional privilege escalation steps required."
            ),
            recommended_action="replace_with_least_privilege_policy",
            intent_type="mutating",
            mutating_category="policy_change",
            mitre_technique="T1078.004 Valid Accounts: Cloud Accounts",
            least_privilege_suggestion=(
                "Replace with scoped policies: identify which services this role actually needs, "
                "then create service-specific policies scoped to named resource ARNs."
            ),
        ))

    # ── Check 2: Service-level wildcard (iam:*, s3:*, ec2:*) ─────────────────
    service_wildcards = [a for a in actions if a.endswith(":*") and a != "*:*"]
    for svc_wc in service_wildcards:
        service = svc_wc.split(":")[0].upper()
        findings.append(IAMFinding(
            severity="high",
            finding_type="overprivileged",
            statement_sid=sid,
            actions_involved=[svc_wc],
            resource=resource_str,
            description=f"Service-level wildcard: {svc_wc} grants all {service} actions",
            attack_path=(
                f"All {service} APIs accessible. Depending on the service this includes "
                f"data read, write, delete, and configuration modification. "
                f"Scope to specific required actions."
            ),
            recommended_action="replace_service_wildcard_with_specific_actions",
            intent_type="mutating",
            mutating_category="policy_change",
            mitre_technique="T1078.004 Valid Accounts: Cloud Accounts",
            least_privilege_suggestion=(
                f"Replace {svc_wc} with only the specific {service} actions this identity requires. "
                f"Use AWS Access Analyzer to identify actually-used actions."
            ),
        ))

    # ── Check 3: Dangerous two-action combinations ────────────────────────────
    for action_a, action_b, severity, description, mitre in ESCALATION_COMBOS:
        if action_a in action_set and action_b in action_set:
            findings.append(IAMFinding(
                severity=severity,
                finding_type="privilege_escalation",
                statement_sid=sid,
                actions_involved=[action_a, action_b],
                resource=resource_str,
                description=description,
                attack_path=(
                    f"Escalation path confirmed: {action_a} + {action_b} on resource {resource_str}. "
                    + description
                ),
                recommended_action="remove_dangerous_action_combination",
                intent_type="mutating",
                mutating_category="policy_change",
                mitre_technique=mitre,
                least_privilege_suggestion=(
                    f"Remove {action_a} from this statement or restrict it to specific resource ARNs. "
                    f"Consider separating {action_a} and {action_b} into different roles with "
                    f"separate trust policies."
                ),
            ))

    # ── Check 4: Individual high-risk IAM actions on wildcard resource ────────
    priv_actions_present = [a for a in actions if a in PRIVILEGE_ESCALATION_ACTIONS]
    if priv_actions_present and wildcard_resource and not ("*" in action_set):
        # Only report if not already caught by full-admin check
        findings.append(IAMFinding(
            severity="high",
            finding_type="privilege_escalation",
            statement_sid=sid,
            actions_involved=priv_actions_present[:8],
            resource=resource_str,
            description=(
                f"{len(priv_actions_present)} high-risk IAM actions with wildcard resource: "
                + ", ".join(priv_actions_present[:5])
                + (" ..." if len(priv_actions_present) > 5 else "")
            ),
            attack_path=(
                "These privilege-escalation-capable actions applied to Resource:* mean the identity "
                "can operate on ALL resources of the relevant type. Scope each action to its minimum "
                "required resource ARN."
            ),
            recommended_action="scope_resource_arns_and_review_actions",
            intent_type="mutating",
            mutating_category="policy_change",
            mitre_technique="T1098.003 Account Manipulation: Additional Cloud Credentials",
            least_privilege_suggestion=(
                "Use AWS Access Analyzer to identify actually-needed resources, then replace * "
                "with specific ARNs such as arn:aws:iam::123456789012:role/specific-role-name"
            ),
        ))

    # ── Check 5: Public principal exposure ───────────────────────────────────
    if is_public_principal(principal) and effect == "Allow":
        findings.append(IAMFinding(
            severity="critical",
            finding_type="public_exposure",
            statement_sid=sid,
            actions_involved=actions[:8],
            resource=resource_str,
            description="Policy allows ANY AWS principal (Principal: '*') — this is public exposure",
            attack_path=(
                "Any AWS account worldwide can assume this role or invoke these actions. "
                "This is the equivalent of publishing your internal APIs to the internet. "
                "Attacker only needs an AWS account to exploit this — no credentials required."
            ),
            recommended_action="restrict_principal_to_specific_account_arns",
            intent_type="mutating",
            mutating_category="policy_change",
            mitre_technique="T1190 Exploit Public-Facing Application",
            least_privilege_suggestion=(
                "Replace Principal: '*' with specific account ARNs: "
                "'arn:aws:iam::123456789012:root' or specific role ARNs. "
                "Add a Condition with aws:PrincipalOrgID to restrict to your AWS Organization."
            ),
        ))

    # ── Check 6: Data exfiltration risk on wildcard resource ─────────────────
    data_actions_present = [a for a in actions if a in DATA_EXFILTRATION_ACTIONS]
    if data_actions_present and wildcard_resource:
        findings.append(IAMFinding(
            severity="high",
            finding_type="data_exfil_risk",
            statement_sid=sid,
            actions_involved=data_actions_present[:8],
            resource=resource_str,
            description=(
                f"Data read/exfiltration actions on wildcard resource: "
                + ", ".join(data_actions_present[:5])
                + (" ..." if len(data_actions_present) > 5 else "")
            ),
            attack_path=(
                "Principal can read from ALL resources of these types. "
                "For s3:GetObject on Resource:*, an attacker can download every S3 object in the account. "
                "For secretsmanager:GetSecretValue on Resource:*, all secrets including database passwords, "
                "API keys, and certificates are accessible with no additional steps."
            ),
            recommended_action="scope_data_access_to_named_resource_arns",
            intent_type="mutating",
            mutating_category="policy_change",
            mitre_technique="T1530 Data from Cloud Storage",
            least_privilege_suggestion=(
                "Replace Resource: '*' with the specific ARNs of resources this identity needs. "
                "For S3: arn:aws:s3:::bucket-name/* — for Secrets Manager: "
                "arn:aws:secretsmanager:region:account:secret:secret-name-*"
            ),
        ))

    return findings


def analyze_policy(policy: dict, source: str) -> IAMAnalysisResult:
    statements = policy.get("Statement", [])
    if isinstance(statements, dict):
        statements = [statements]

    all_findings: List[IAMFinding] = []
    anomaly_type_set: Set[str] = set()

    for stmt in statements:
        stmt_findings = analyze_statement(stmt)
        for f in stmt_findings:
            anomaly_type_set.add(f.finding_type)
        all_findings.extend(stmt_findings)

    # Deduplicate: if full admin wildcard was found, don't also report
    # individual overprivileged or priv-esc findings for the same statement
    full_admin_sids = {
        f.statement_sid for f in all_findings
        if f.finding_type == "privilege_escalation" and "Action=*" in f.description
    }
    deduplicated = []
    for f in all_findings:
        if (f.statement_sid in full_admin_sids
                and f.finding_type in ("overprivileged", "data_exfil_risk")
                and "Action=*" not in f.description):
            continue  # Already covered by full-admin finding
        deduplicated.append(f)
    all_findings = deduplicated

    critical = sum(1 for f in all_findings if f.severity == "critical")
    high = sum(1 for f in all_findings if f.severity == "high")
    medium = sum(1 for f in all_findings if f.severity == "medium")

    if critical > 0:
        risk = "critical"
        blast = "full_account"
        intent = "mutating"
        mut_cat = "policy_change"
        action = "detach_policy_immediately_and_investigate"
    elif high > 0:
        risk = "high"
        blast = "data_exfiltration_risk"
        intent = "mutating"
        mut_cat = "policy_change"
        action = "apply_least_privilege_policy"
    else:
        risk = "clean"
        blast = "minimal"
        intent = "read_only"
        mut_cat = None
        action = "no_action_required"

    return IAMAnalysisResult(
        policy_source=source,
        timestamp_utc=datetime.now(timezone.utc).isoformat(),
        statements_analyzed=len(statements),
        findings=all_findings,
        critical_count=critical,
        high_count=high,
        medium_count=medium,
        overall_risk=risk,
        blast_radius=blast,
        anomaly_types=sorted(anomaly_type_set),
        recommended_action=action,
        intent_type=intent,
        mutating_category=mut_cat,
    )


# ── Output formatting ─────────────────────────────────────────────────────────

_COLORS = {
    "critical": "\033[91m",
    "high":     "\033[33m",
    "medium":   "\033[36m",
    "low":      "\033[37m",
    "clean":    "\033[92m",
}
_RESET = "\033[0m"


def print_text_report(result: IAMAnalysisResult) -> None:
    color = _COLORS.get(result.overall_risk, "")
    print(f"\nUSAP IAM Policy Analyzer")
    print(f"Source   : {result.policy_source}")
    print(f"Analyzed : {result.statements_analyzed} statements  |  {result.timestamp_utc}")
    print(f"Risk     : {color}{result.overall_risk.upper()}{_RESET}  "
          f"Critical: {result.critical_count}  High: {result.high_count}  "
          f"Medium: {result.medium_count}")
    print(f"Blast    : {result.blast_radius}")
    if result.anomaly_types:
        print(f"Types    : {', '.join(result.anomaly_types)}")
    print(f"Intent   : {result.intent_type}"
          + (f"  Category: {result.mutating_category}" if result.mutating_category else ""))
    print(f"Action   : {result.recommended_action}")
    print()

    if not result.findings:
        print(f"{_COLORS['clean']}No high/critical findings. Policy appears appropriately scoped.{_RESET}")
        return

    for idx, f in enumerate(result.findings, start=1):
        sev_color = _COLORS.get(f.severity, "")
        print(f"  [{idx:03d}] {sev_color}{f.severity.upper()}{_RESET} — {f.finding_type}")
        if f.statement_sid:
            print(f"        Sid     : {f.statement_sid}")
        print(f"        Actions : {', '.join(f.actions_involved[:6])}"
              + (" ..." if len(f.actions_involved) > 6 else ""))
        print(f"        Resource: {f.resource}")
        print(f"        Issue   : {f.description}")
        # Truncate long attack paths in text mode
        attack_short = f.attack_path[:200] + "..." if len(f.attack_path) > 200 else f.attack_path
        print(f"        Path    : {attack_short}")
        print(f"        MITRE   : {f.mitre_technique}")
        print(f"        Fix     : {f.recommended_action}")
        print(f"        Suggest : {f.least_privilege_suggestion[:150]}...")
        print()


def result_to_dict(result: IAMAnalysisResult) -> dict:
    return {
        "policy_source": result.policy_source,
        "timestamp_utc": result.timestamp_utc,
        "statements_analyzed": result.statements_analyzed,
        "overall_risk": result.overall_risk,
        "critical_count": result.critical_count,
        "high_count": result.high_count,
        "medium_count": result.medium_count,
        "blast_radius": result.blast_radius,
        "anomaly_types": result.anomaly_types,
        "recommended_action": result.recommended_action,
        "intent_type": result.intent_type,
        "mutating_category": result.mutating_category,
        "findings": [
            {
                "severity": f.severity,
                "finding_type": f.finding_type,
                "statement_sid": f.statement_sid,
                "actions_involved": f.actions_involved,
                "resource": f.resource,
                "description": f.description,
                "attack_path": f.attack_path,
                "recommended_action": f.recommended_action,
                "intent_type": f.intent_type,
                "mutating_category": f.mutating_category,
                "mitre_technique": f.mitre_technique,
                "least_privilege_suggestion": f.least_privilege_suggestion,
            }
            for f in result.findings
        ],
    }


# ── CLI entry point ───────────────────────────────────────────────────────────

def main() -> int:
    parser = argparse.ArgumentParser(
        description="USAP IAM Policy Analyzer — detect privilege escalation and overprivileged grants",
        epilog="Exit codes: 0=clean, 1=high findings, 2=critical findings",
    )
    parser.add_argument(
        "policy",
        help="Path to IAM policy JSON file, directory of policy files, or '-' for stdin",
    )
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    parser.add_argument("--output", "-o", metavar="FILE", help="Write JSON results to file")
    parser.add_argument(
        "--check",
        choices=["privilege-escalation", "data-exfil", "public-exposure", "all"],
        default="all",
        help="Analysis type to run (default: all)",
    )
    parser.add_argument("--directory", "-d", action="store_true", help="Treat path as directory of policy files")
    args = parser.parse_args()

    policies_to_analyze: List[Tuple[str, dict]] = []

    try:
        if args.policy == "-":
            text = sys.stdin.read()
            policies_to_analyze.append(("stdin", json.loads(text)))
        elif args.directory or (args.policy != "-" and Path(args.policy).is_dir()):
            policy_dir = Path(args.policy)
            for fpath in policy_dir.rglob("*.json"):
                try:
                    policies_to_analyze.append((str(fpath), json.loads(fpath.read_text())))
                except json.JSONDecodeError:
                    print(f"WARNING: skipping invalid JSON: {fpath}", file=sys.stderr)
        else:
            fpath = Path(args.policy)
            if not fpath.exists():
                print(f"ERROR: File not found: {fpath}", file=sys.stderr)
                return 2
            policies_to_analyze.append((str(fpath), json.loads(fpath.read_text())))
    except json.JSONDecodeError as exc:
        print(f"ERROR: Invalid JSON: {exc}", file=sys.stderr)
        return 2

    if not policies_to_analyze:
        print("ERROR: No policy files found.", file=sys.stderr)
        return 2

    results = [analyze_policy(policy, source) for source, policy in policies_to_analyze]

    max_critical = sum(r.critical_count for r in results)
    max_high = sum(r.high_count for r in results)

    if args.json:
        output_data = results[0] if len(results) == 1 else {"policies": [result_to_dict(r) for r in results]}
        if len(results) == 1:
            output_str = json.dumps(result_to_dict(results[0]), indent=2)
        else:
            output_str = json.dumps({"policies": [result_to_dict(r) for r in results]}, indent=2)

        if args.output:
            Path(args.output).write_text(output_str, encoding="utf-8")
            print(f"Results written to {args.output}")
        else:
            print(output_str)
    else:
        for r in results:
            print_text_report(r)

    if max_critical > 0:
        return 2
    if max_high > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
