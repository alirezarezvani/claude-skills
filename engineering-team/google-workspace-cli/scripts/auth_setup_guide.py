#!/usr/bin/env python3
"""
Google Workspace CLI Auth Setup Guide — Guided authentication configuration.

Prints step-by-step instructions for OAuth and service account setup,
generates .env templates, lists required scopes, and validates auth.

Usage:
    python3 auth_setup_guide.py --guide oauth
    python3 auth_setup_guide.py --guide service-account
    python3 auth_setup_guide.py --scopes gmail,drive,calendar
    python3 auth_setup_guide.py --generate-env
    python3 auth_setup_guide.py --validate [--json]
    python3 auth_setup_guide.py --check [--json]
"""

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Dict


SERVICE_SCOPES: Dict[str, List[str]] = {
    "gmail": [
        "https://www.googleapis.com/auth/gmail.modify",
        "https://www.googleapis.com/auth/gmail.send",
        "https://www.googleapis.com/auth/gmail.labels",
        "https://www.googleapis.com/auth/gmail.settings.basic",
    ],
    "drive": [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive.metadata.readonly",
    ],
    "sheets": [
        "https://www.googleapis.com/auth/spreadsheets",
    ],
    "calendar": [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/calendar.events",
    ],
    "tasks": [
        "https://www.googleapis.com/auth/tasks",
    ],
    "chat": [
        "https://www.googleapis.com/auth/chat.spaces.readonly",
        "https://www.googleapis.com/auth/chat.messages",
    ],
    "docs": [
        "https://www.googleapis.com/auth/documents",
    ],
    "admin": [
        "https://www.googleapis.com/auth/admin.directory.user.readonly",
        "https://www.googleapis.com/auth/admin.directory.group",
        "https://www.googleapis.com/auth/admin.directory.orgunit.readonly",
    ],
    "meet": [
        "https://www.googleapis.com/auth/meetings.space.created",
    ],
}

OAUTH_GUIDE = """
=== Google Workspace CLI: OAuth Setup Guide ===

Step 1: Create a Google Cloud Project
  1. Go to https://console.cloud.google.com/
  2. Click "Select a project" -> "New Project"
  3. Name it (e.g., "gws-cli-access") and click Create
  4. Note the Project ID

Step 2: Enable Required APIs
  1. Go to APIs & Services -> Library
  2. Search and enable each API you need:
     - Gmail API
     - Google Drive API
     - Google Sheets API
     - Google Calendar API
     - Tasks API
     - Admin SDK API (for admin operations)

Step 3: Configure OAuth Consent Screen
  1. Go to APIs & Services -> OAuth consent screen
  2. Select "Internal" (for Workspace) or "External" (for personal)
  3. Fill in app name, support email
  4. Add scopes for the services you need
  5. Save and continue

Step 4: Create OAuth Credentials
  1. Go to APIs & Services -> Credentials
  2. Click "Create Credentials" -> "OAuth client ID"
  3. Application type: "Desktop app"
  4. Name it "gws-cli"
  5. Download the JSON file

Step 5: Configure gws CLI
  1. Set environment variables:
     export GWS_CLIENT_ID=<your-client-id>
     export GWS_CLIENT_SECRET=<your-client-secret>

  2. Or place the credentials JSON:
     mv client_secret_*.json ~/.config/gws/credentials.json

Step 6: Authenticate
  gws auth setup
  # Opens browser for consent, stores token in system keyring

Step 7: Verify
  gws auth status
  gws gmail users getProfile me
"""

SERVICE_ACCOUNT_GUIDE = """
=== Google Workspace CLI: Service Account Setup Guide ===

Step 1: Create a Google Cloud Project
  (Same as OAuth Step 1)

Step 2: Create a Service Account
  1. Go to IAM & Admin -> Service Accounts
  2. Click "Create Service Account"
  3. Name: "gws-cli-service"
  4. Grant roles as needed (no role needed for Workspace API access)
  5. Click "Done"

Step 3: Create Key
  1. Click on the service account
  2. Go to "Keys" tab
  3. Add Key -> Create new key -> JSON
  4. Download and store securely

Step 4: Enable Domain-Wide Delegation
  1. On the service account page, click "Edit"
  2. Check "Enable Google Workspace domain-wide delegation"
  3. Save
  4. Note the Client ID (numeric)

Step 5: Authorize in Google Admin
  1. Go to admin.google.com
  2. Security -> API Controls -> Domain-wide Delegation
  3. Add new:
     - Client ID: <numeric client ID from Step 4>
     - Scopes: (paste required scopes)
  4. Authorize

Step 6: Configure gws CLI
  export GWS_SERVICE_ACCOUNT_KEY=/path/to/service-account-key.json
  export GWS_DELEGATED_USER=admin@yourdomain.com

Step 7: Verify
  gws auth status
  gws gmail users getProfile me
"""

ENV_TEMPLATE = """# Google Workspace CLI Configuration
# Copy to .env and fill in values

# OAuth Credentials (for interactive auth)
GWS_CLIENT_ID=
GWS_CLIENT_SECRET=
GWS_TOKEN_PATH=~/.config/gws/token.json

# Service Account (for headless/CI auth)
# GWS_SERVICE_ACCOUNT_KEY=/path/to/key.json
# GWS_DELEGATED_USER=admin@yourdomain.com

# Defaults
GWS_DEFAULT_FORMAT=json
GWS_PAGINATION_LIMIT=100
"""


@dataclass
class ValidationResult:
    service: str
    status: str  # PASS, FAIL
    message: str


@dataclass
class ValidationReport:
    auth_method: str = ""
    user: str = ""
    results: List[dict] = field(default_factory=list)
    summary: str = ""
    demo_mode: bool = False


DEMO_VALIDATION = ValidationReport(
    auth_method="oauth",
    user="admin@company.com",
    results=[
        {"service": "gmail", "status": "PASS", "message": "Gmail API accessible"},
        {"service": "drive", "status": "PASS", "message": "Drive API accessible"},
        {"service": "calendar", "status": "PASS", "message": "Calendar API accessible"},
        {"service": "sheets", "status": "PASS", "message": "Sheets API accessible"},
        {"service": "tasks", "status": "FAIL", "message": "Scope not authorized"},
    ],
    summary="4/5 services validated (demo mode)",
    demo_mode=True,
)


def check_auth_status() -> dict:
    """Check current gws auth status."""
    try:
        result = subprocess.run(
            ["gws", "auth", "status", "--json"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                return {"status": "authenticated", "raw": result.stdout.strip()}
        return {"status": "not_authenticated", "error": result.stderr.strip()[:200]}
    except (FileNotFoundError, OSError):
        return {"status": "gws_not_found"}


def validate_services(services: List[str]) -> ValidationReport:
    """Validate auth by testing each service."""
    report = ValidationReport()

    auth = check_auth_status()
    if auth.get("status") == "gws_not_found":
        report.summary = "gws CLI not installed"
        return report
    if auth.get("status") == "not_authenticated":
        report.auth_method = "none"
        report.summary = "Not authenticated"
        return report

    report.auth_method = auth.get("method", "oauth")
    report.user = auth.get("user", auth.get("email", "unknown"))

    service_cmds = {
        "gmail": ["gws", "gmail", "users", "getProfile", "me", "--json"],
        "drive": ["gws", "drive", "files", "list", "--limit", "1", "--json"],
        "calendar": ["gws", "calendar", "calendarList", "list", "--limit", "1", "--json"],
        "sheets": ["gws", "sheets", "spreadsheets", "get", "test", "--json"],
        "tasks": ["gws", "tasks", "tasklists", "list", "--limit", "1", "--json"],
    }

    for svc in services:
        cmd = service_cmds.get(svc)
        if not cmd:
            report.results.append(asdict(
                ValidationResult(svc, "WARN", f"No test available for {svc}")
            ))
            continue
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if result.returncode == 0:
                report.results.append(asdict(
                    ValidationResult(svc, "PASS", f"{svc.title()} API accessible")
                ))
            else:
                report.results.append(asdict(
                    ValidationResult(svc, "FAIL", result.stderr.strip()[:100])
                ))
        except (subprocess.TimeoutExpired, OSError) as e:
            report.results.append(asdict(
                ValidationResult(svc, "FAIL", str(e)[:100])
            ))

    passed = sum(1 for r in report.results if r["status"] == "PASS")
    total = len(report.results)
    report.summary = f"{passed}/{total} services validated"
    return report


def main():
    parser = argparse.ArgumentParser(
        description="Guided authentication setup for Google Workspace CLI (gws)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --guide oauth               # OAuth setup instructions
  %(prog)s --guide service-account      # Service account setup
  %(prog)s --scopes gmail,drive         # Show required scopes
  %(prog)s --generate-env               # Generate .env template
  %(prog)s --check                      # Check current auth status
  %(prog)s --validate --json            # Validate all services (JSON)
        """,
    )
    parser.add_argument("--guide", choices=["oauth", "service-account"],
                        help="Print setup guide")
    parser.add_argument("--scopes", help="Comma-separated services to show scopes for")
    parser.add_argument("--generate-env", action="store_true",
                        help="Generate .env template")
    parser.add_argument("--check", action="store_true",
                        help="Check current auth status")
    parser.add_argument("--validate", action="store_true",
                        help="Validate auth by testing services")
    parser.add_argument("--services", default="gmail,drive,calendar,sheets,tasks",
                        help="Services to validate (default: gmail,drive,calendar,sheets,tasks)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    if not any([args.guide, args.scopes, args.generate_env, args.check, args.validate]):
        parser.print_help()
        return

    if args.guide:
        if args.guide == "oauth":
            print(OAUTH_GUIDE)
        else:
            print(SERVICE_ACCOUNT_GUIDE)
        return

    if args.scopes:
        services = [s.strip() for s in args.scopes.split(",") if s.strip()]
        if args.json:
            output = {}
            for svc in services:
                output[svc] = SERVICE_SCOPES.get(svc, [])
            print(json.dumps(output, indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"  REQUIRED OAUTH SCOPES")
            print(f"{'='*60}\n")
            for svc in services:
                scopes = SERVICE_SCOPES.get(svc, [])
                print(f"  {svc.upper()}:")
                if scopes:
                    for scope in scopes:
                        print(f"    - {scope}")
                else:
                    print(f"    (no scopes defined for '{svc}')")
                print()
            # Print combined for easy copy-paste
            all_scopes = []
            for svc in services:
                all_scopes.extend(SERVICE_SCOPES.get(svc, []))
            if all_scopes:
                print(f"  COMBINED (for consent screen):")
                print(f"  {','.join(all_scopes)}")
            print(f"\n{'='*60}\n")
        return

    if args.generate_env:
        print(ENV_TEMPLATE)
        return

    if args.check:
        if shutil.which("gws"):
            status = check_auth_status()
        else:
            status = {"status": "gws_not_found",
                      "note": "Install gws first: cargo install gws-cli  OR  https://github.com/googleworkspace/cli/releases"}
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print(f"\nAuth Status: {status.get('status', 'unknown')}")
            for k, v in status.items():
                if k != "status":
                    print(f"  {k}: {v}")
            print()
        return

    if args.validate:
        services = [s.strip() for s in args.services.split(",") if s.strip()]
        if not shutil.which("gws"):
            report = DEMO_VALIDATION
        else:
            report = validate_services(services)

        if args.json:
            print(json.dumps(asdict(report), indent=2))
        else:
            print(f"\n{'='*60}")
            print(f"  AUTH VALIDATION REPORT")
            if report.demo_mode:
                print(f"  (DEMO MODE)")
            print(f"{'='*60}\n")
            if report.user:
                print(f"  User: {report.user}")
                print(f"  Method: {report.auth_method}\n")
            for r in report.results:
                icon = "PASS" if r["status"] == "PASS" else "FAIL"
                print(f"  [{icon}] {r['service']}: {r['message']}")
            print(f"\n  {report.summary}")
            print(f"\n{'='*60}\n")


if __name__ == "__main__":
    main()
