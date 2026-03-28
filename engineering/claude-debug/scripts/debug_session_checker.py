#!/usr/bin/env python3
"""Debug Session Checker — validates debug session state and phase transitions."""

import argparse
import json
import os
import sys
from datetime import datetime

VALID_PHASES = ["reproduce", "isolate", "root_cause", "fix", "verify", "complete"]

PHASE_TRANSITIONS = {
    "reproduce": ["isolate"],
    "isolate": ["root_cause"],
    "root_cause": ["fix"],
    "fix": ["verify"],
    "verify": ["complete", "isolate"],
    "complete": [],
}

PHASE_EDIT_RULES = {
    "reproduce": "blocked",
    "isolate": "debug_only",
    "root_cause": "blocked",
    "fix": "allowed",
    "verify": "allowed",
    "complete": "allowed",
}


def find_session_file(project_path):
    """Find the debug session file in a project."""
    session_path = os.path.join(project_path, ".claude", "debug-session.json")
    if os.path.exists(session_path):
        return session_path
    return None


def validate_session(session_data):
    """Validate a debug session structure and return issues."""
    issues = []
    warnings = []

    if "phase" not in session_data:
        issues.append("Missing required field: phase")
    elif session_data["phase"] not in VALID_PHASES:
        issues.append(
            f"Invalid phase '{session_data['phase']}'. "
            f"Valid phases: {', '.join(VALID_PHASES)}"
        )

    if "bug" not in session_data:
        issues.append("Missing required field: bug")
    elif not session_data["bug"].strip():
        warnings.append("Bug description is empty")

    if "started" not in session_data:
        warnings.append("Missing field: started (timestamp)")
    else:
        try:
            datetime.fromisoformat(session_data["started"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            warnings.append(f"Invalid timestamp format: {session_data['started']}")

    phase = session_data.get("phase", "")
    if phase in ("isolate", "root_cause", "fix", "verify"):
        evidence = session_data.get("evidence", {})
        if not evidence:
            warnings.append(
                f"Phase '{phase}' has no evidence recorded. "
                "Evidence should accumulate as phases progress."
            )

    return issues, warnings


def check_edit_allowed(session_data, has_debug_marker=False):
    """Check if an edit would be allowed in the current phase."""
    phase = session_data.get("phase", "")
    rule = PHASE_EDIT_RULES.get(phase, "allowed")

    if rule == "blocked":
        return False, f"Edits blocked in phase '{phase}'"
    elif rule == "debug_only":
        if has_debug_marker:
            return True, f"Diagnostic edit allowed in phase '{phase}'"
        return False, (
            f"Only edits containing '// DEBUG' or '# DEBUG' markers "
            f"are allowed in phase '{phase}'"
        )
    return True, f"Edits allowed in phase '{phase}'"


def main():
    parser = argparse.ArgumentParser(
        description="Validate debug session state and check phase gate rules."
    )
    parser.add_argument(
        "project_path",
        nargs="?",
        default=".",
        help="Path to the project directory (default: current directory)",
    )
    parser.add_argument(
        "--check-edit",
        action="store_true",
        help="Check if an edit would be allowed in the current phase",
    )
    parser.add_argument(
        "--has-debug-marker",
        action="store_true",
        help="Simulate an edit containing // DEBUG marker (used with --check-edit)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output as JSON",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed phase transition rules",
    )
    args = parser.parse_args()

    project_path = os.path.abspath(args.project_path)
    session_file = find_session_file(project_path)

    result = {
        "project": project_path,
        "session_file": session_file,
        "session_active": False,
        "phase": None,
        "edit_rule": None,
        "issues": [],
        "warnings": [],
        "status": "ok",
    }

    if not session_file:
        result["status"] = "no_session"
        result["edit_rule"] = "allowed"
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"No active debug session in {project_path}")
            print("Edit rule: allowed (not in debug mode)")
        sys.exit(0)

    try:
        with open(session_file) as f:
            session_data = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        result["status"] = "error"
        result["issues"].append(f"Cannot read session file: {e}")
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"Error reading {session_file}: {e}")
        sys.exit(2)

    result["session_active"] = True
    result["phase"] = session_data.get("phase")

    issues, warnings = validate_session(session_data)
    result["issues"] = issues
    result["warnings"] = warnings

    phase = session_data.get("phase", "")
    result["edit_rule"] = PHASE_EDIT_RULES.get(phase, "allowed")

    if args.check_edit:
        allowed, reason = check_edit_allowed(session_data, args.has_debug_marker)
        result["edit_allowed"] = allowed
        result["edit_reason"] = reason

    if issues:
        result["status"] = "invalid"
    elif warnings:
        result["status"] = "warnings"

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Debug session: {session_file}")
        print(f"Phase: {phase}")
        print(f"Bug: {session_data.get('bug', '(not set)')}")
        print(f"Edit rule: {PHASE_EDIT_RULES.get(phase, 'allowed')}")

        if args.check_edit:
            allowed, reason = check_edit_allowed(
                session_data, args.has_debug_marker
            )
            print(f"Edit allowed: {'yes' if allowed else 'no'} — {reason}")

        if issues:
            print(f"\nIssues ({len(issues)}):")
            for issue in issues:
                print(f"  - {issue}")

        if warnings:
            print(f"\nWarnings ({len(warnings)}):")
            for w in warnings:
                print(f"  - {w}")

        if args.verbose:
            print(f"\nValid transitions from '{phase}':")
            for target in PHASE_TRANSITIONS.get(phase, []):
                print(f"  {phase} -> {target}")

    exit_code = 0 if not issues else (2 if result["status"] == "error" else 1)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
