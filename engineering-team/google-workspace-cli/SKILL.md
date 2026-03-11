---
name: "google-workspace-cli"
description: "Google Workspace administration via the gws CLI. Install, authenticate, and automate Gmail, Drive, Sheets, Calendar, Docs, Chat, and Tasks. Run security audits, execute 43 built-in recipes, and use 10 persona bundles. Use for Google Workspace admin, gws CLI setup, Gmail automation, Drive management, or Calendar scheduling."
---

# Google Workspace CLI

Expert guidance and automation for Google Workspace administration using the open-source `gws` CLI. Covers installation, authentication, 18+ service APIs, 43 built-in recipes, and 10 persona bundles for role-based workflows.

---

## Quick Start

### Check Installation

```bash
# Verify gws is installed and authenticated
python3 scripts/gws_doctor.py
```

### Send an Email

```bash
gws gmail users.messages send me --to "team@company.com" \
  --subject "Weekly Update" --body "Here's this week's summary..."
```

### List Drive Files

```bash
gws drive files list --json --limit 20 | python3 scripts/output_analyzer.py --select "name,mimeType,modifiedTime" --format table
```

---

## Installation

### npm (recommended)

```bash
npm install -g @anthropic/gws
gws --version
```

### Cargo (from source)

```bash
cargo install gws-cli
gws --version
```

### Pre-built Binaries

Download from [github.com/googleworkspace/cli/releases](https://github.com/googleworkspace/cli/releases) for macOS, Linux, or Windows.

### Verify Installation

```bash
python3 scripts/gws_doctor.py
# Checks: PATH, version, auth status, service connectivity
```

---

## Authentication

### OAuth Setup (Interactive)

```bash
# Step 1: Create Google Cloud project and OAuth credentials
python3 scripts/auth_setup_guide.py --guide oauth

# Step 2: Run auth setup
gws auth setup

# Step 3: Validate
gws auth status --json
```

### Service Account (Headless/CI)

```bash
# Generate setup instructions
python3 scripts/auth_setup_guide.py --guide service-account

# Configure with key file
export GWS_SERVICE_ACCOUNT_KEY=/path/to/key.json
export GWS_DELEGATED_USER=admin@company.com
gws auth status
```

### Environment Variables

```bash
# Generate .env template
python3 scripts/auth_setup_guide.py --generate-env
```

| Variable | Purpose |
|----------|---------|
| `GWS_CLIENT_ID` | OAuth client ID |
| `GWS_CLIENT_SECRET` | OAuth client secret |
| `GWS_TOKEN_PATH` | Custom token storage path |
| `GWS_SERVICE_ACCOUNT_KEY` | Service account JSON key path |
| `GWS_DELEGATED_USER` | User to impersonate (service accounts) |
| `GWS_DEFAULT_FORMAT` | Default output format (json/ndjson/table) |

### Validate Authentication

```bash
python3 scripts/auth_setup_guide.py --validate --json
# Tests each service endpoint
```

---

## Workflow 1: Gmail Automation

**Goal:** Automate email operations — send, search, label, and filter management.

### Send and Reply

```bash
# Send a new email
gws gmail users.messages send me --to "client@example.com" \
  --subject "Proposal" --body "Please find attached..." \
  --attachment proposal.pdf

# Reply to a thread
gws gmail users.messages reply me --thread-id <THREAD_ID> \
  --body "Thanks for your feedback..."

# Forward a message
gws gmail users.messages forward me --message-id <MSG_ID> \
  --to "manager@company.com"
```

### Search and Filter

```bash
# Search emails
gws gmail users.messages list me --query "from:client@example.com after:2025/01/01" --json \
  | python3 scripts/output_analyzer.py --count

# List labels
gws gmail users.labels list me --json

# Create a filter
gws gmail users.settings.filters create me \
  --criteria '{"from":"notifications@service.com"}' \
  --action '{"addLabelIds":["Label_123"],"removeLabelIds":["INBOX"]}'
```

### Bulk Operations

```bash
# Archive all read emails older than 30 days
gws gmail users.messages list me --query "is:read older_than:30d" --json \
  | python3 scripts/output_analyzer.py --select "id" --format json \
  | xargs -I {} gws gmail users.messages modify me {} --removeLabelIds INBOX
```

---

## Workflow 2: Drive & Sheets

**Goal:** Manage files, create spreadsheets, configure sharing, and export data.

### File Operations

```bash
# List files
gws drive files list --json --limit 50 \
  | python3 scripts/output_analyzer.py --select "name,mimeType,size" --format table

# Upload a file
gws drive files create --name "Q1 Report" --upload report.pdf \
  --parents <FOLDER_ID>

# Create a Google Sheet
gws sheets spreadsheets create --title "Budget 2026" --json

# Download/export
gws drive files export <FILE_ID> --mime "application/pdf" --output report.pdf
```

### Sharing

```bash
# Share with user
gws drive permissions create <FILE_ID> \
  --type user --role writer --emailAddress "colleague@company.com"

# Share with domain (view only)
gws drive permissions create <FILE_ID> \
  --type domain --role reader --domain "company.com"

# List who has access
gws drive permissions list <FILE_ID> --json
```

### Sheets Data

```bash
# Read a range
gws sheets spreadsheets.values get <SHEET_ID> --range "Sheet1!A1:D10" --json

# Write data
gws sheets spreadsheets.values update <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Name","Score"],["Alice",95],["Bob",87]]'

# Append rows
gws sheets spreadsheets.values append <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Charlie",92]]'
```

---

## Workflow 3: Calendar & Meetings

**Goal:** Schedule events, find available times, and generate standup reports.

### Event Management

```bash
# Create an event
gws calendar events insert primary \
  --summary "Sprint Planning" \
  --start "2026-03-15T10:00:00" --end "2026-03-15T11:00:00" \
  --attendees "team@company.com" \
  --location "Conference Room A"

# List upcoming events
gws calendar events list primary --timeMin "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
  --maxResults 10 --json

# Quick event (natural language)
gws helpers quick-event "Lunch with Sarah tomorrow at noon"
```

### Find Available Time

```bash
# Check free/busy for multiple people
gws helpers find-time \
  --attendees "alice@co.com,bob@co.com,charlie@co.com" \
  --duration 60 --within "2026-03-15,2026-03-19" --json
```

### Standup Report

```bash
# Generate daily standup from calendar + tasks
gws recipes standup-report --json \
  | python3 scripts/output_analyzer.py --format table

# Meeting prep (agenda + attendee info)
gws recipes meeting-prep --event-id <EVENT_ID>
```

---

## Workflow 4: Security Audit

**Goal:** Audit Google Workspace security configuration and generate remediation commands.

### Run Full Audit

```bash
# Full audit across all services
python3 scripts/workspace_audit.py --json

# Audit specific services
python3 scripts/workspace_audit.py --services gmail,drive,calendar

# Demo mode (no gws required)
python3 scripts/workspace_audit.py --demo
```

### Audit Checks

| Area | Check | Risk |
|------|-------|------|
| Drive | External sharing enabled | Data exfiltration |
| Gmail | Auto-forwarding rules | Data exfiltration |
| Gmail | DMARC/SPF/DKIM records | Email spoofing |
| Calendar | Default sharing visibility | Information leak |
| OAuth | Third-party app grants | Unauthorized access |
| Admin | Super admin count | Privilege escalation |
| Admin | 2-Step verification enforcement | Account takeover |

### Review and Remediate

```bash
# Review findings
python3 scripts/workspace_audit.py --json | python3 scripts/output_analyzer.py \
  --filter "status=FAIL" --select "area,check,remediation"

# Execute remediation (example: restrict external sharing)
gws drive about get --json  # Check current settings
# Follow remediation commands from audit output
```

---

## Python Tools

| Script | Purpose | Usage |
|--------|---------|-------|
| `gws_doctor.py` | Pre-flight diagnostics | `python3 scripts/gws_doctor.py [--json] [--services gmail,drive]` |
| `auth_setup_guide.py` | Guided auth setup | `python3 scripts/auth_setup_guide.py --guide oauth` |
| `gws_recipe_runner.py` | Recipe catalog & runner | `python3 scripts/gws_recipe_runner.py --list [--persona pm]` |
| `workspace_audit.py` | Security/config audit | `python3 scripts/workspace_audit.py [--json] [--demo]` |
| `output_analyzer.py` | JSON/NDJSON analysis | `gws ... --json \| python3 scripts/output_analyzer.py --count` |

All scripts are stdlib-only, support `--json` output, and include demo mode with embedded sample data.

---

## Best Practices

### Security

1. Use OAuth with minimal scopes — request only what each workflow needs
2. Store tokens in the system keyring, never in plain text files
3. Rotate service account keys every 90 days
4. Audit third-party OAuth app grants quarterly
5. Use `--dry-run` before bulk destructive operations

### Automation

1. Pipe `--json` output through `output_analyzer.py` for filtering and aggregation
2. Use recipes for multi-step operations instead of chaining raw commands
3. Select a persona bundle to scope recipes to your role
4. Use NDJSON format (`--format ndjson`) for streaming large result sets
5. Set `GWS_DEFAULT_FORMAT=json` in your shell profile for scripting

### Performance

1. Use `--fields` to request only needed fields (reduces payload size)
2. Use `--limit` to cap results when browsing
3. Use `--page-all` only when you need complete datasets
4. Batch operations with recipes rather than individual API calls
5. Cache frequently accessed data (e.g., label IDs, folder IDs) in variables

---

## Limitations

| Constraint | Impact |
|------------|--------|
| OAuth tokens expire after 1 hour | Re-auth needed for long-running scripts |
| API rate limits (per-user, per-service) | Bulk operations may hit 429 errors |
| Scope requirements vary by service | Must request correct scopes during auth |
| Pre-v1.0 CLI status | Breaking changes possible between releases |
| Google Cloud project required | Free, but requires setup in Cloud Console |
| Admin API needs admin privileges | Some audit checks require Workspace Admin role |

### Required Scopes by Service

```bash
# List scopes for specific services
python3 scripts/auth_setup_guide.py --scopes gmail,drive,calendar,sheets
```

| Service | Key Scopes |
|---------|-----------|
| Gmail | `gmail.modify`, `gmail.send`, `gmail.labels` |
| Drive | `drive.file`, `drive.metadata.readonly` |
| Sheets | `spreadsheets` |
| Calendar | `calendar`, `calendar.events` |
| Admin | `admin.directory.user.readonly`, `admin.directory.group` |
| Tasks | `tasks` |
