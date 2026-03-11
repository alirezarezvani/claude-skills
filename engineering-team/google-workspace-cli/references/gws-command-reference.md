# Google Workspace CLI Command Reference

Comprehensive reference for the `gws` CLI covering 18 services, 22 helper commands, global flags, and environment variables.

---

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Output as JSON |
| `--format ndjson` | Output as newline-delimited JSON |
| `--dry-run` | Show what would be done without executing |
| `--limit <n>` | Maximum results to return |
| `--page-all` | Fetch all pages of results |
| `--fields <spec>` | Partial response field mask |
| `--quiet` | Suppress non-error output |
| `--verbose` | Verbose debug output |
| `--timeout <ms>` | Request timeout in milliseconds |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GWS_CLIENT_ID` | OAuth client ID | — |
| `GWS_CLIENT_SECRET` | OAuth client secret | — |
| `GWS_TOKEN_PATH` | Token storage location | `~/.config/gws/token.json` |
| `GWS_SERVICE_ACCOUNT_KEY` | Service account JSON key path | — |
| `GWS_DELEGATED_USER` | User to impersonate (service accounts) | — |
| `GWS_DEFAULT_FORMAT` | Default output format | `text` |
| `GWS_PAGINATION_LIMIT` | Default pagination limit | `100` |
| `GWS_LOG_LEVEL` | Logging level (debug/info/warn/error) | `warn` |

---

## Services

### Gmail

```bash
gws gmail users.messages list me --query "<query>" --json
gws gmail users.messages get me <messageId> --json
gws gmail users.messages send me --to <email> --subject <subj> --body <body>
gws gmail users.messages reply me --thread-id <id> --body <body>
gws gmail users.messages forward me --message-id <id> --to <email>
gws gmail users.messages modify me <id> --addLabelIds <label> --removeLabelIds INBOX
gws gmail users.messages trash me <id>
gws gmail users.labels list me --json
gws gmail users.labels create me --name <name>
gws gmail users.settings.filters create me --criteria <json> --action <json>
gws gmail users.settings.forwardingAddresses list me --json
gws gmail users getProfile me --json
```

### Google Drive

```bash
gws drive files list --json --limit <n>
gws drive files list --query "name contains '<term>'" --json
gws drive files list --parents <folderId> --json
gws drive files get <fileId> --json
gws drive files create --name <name> --upload <path> --parents <folderId>
gws drive files create --name <name> --mimeType application/vnd.google-apps.folder
gws drive files update <fileId> --upload <path>
gws drive files delete <fileId>
gws drive files export <fileId> --mime <mimeType> --output <path>
gws drive files copy <fileId> --name <newName>
gws drive permissions list <fileId> --json
gws drive permissions create <fileId> --type <user|group|domain> --role <reader|writer|owner> --emailAddress <email>
gws drive permissions delete <fileId> <permissionId>
gws drive about get --json
gws drive files emptyTrash
```

### Google Sheets

```bash
gws sheets spreadsheets create --title <title> --json
gws sheets spreadsheets get <spreadsheetId> --json
gws sheets spreadsheets.values get <spreadsheetId> --range <range> --json
gws sheets spreadsheets.values update <spreadsheetId> --range <range> --values <json>
gws sheets spreadsheets.values append <spreadsheetId> --range <range> --values <json>
gws sheets spreadsheets.values clear <spreadsheetId> --range <range>
gws sheets spreadsheets.values batchGet <spreadsheetId> --ranges <range1>,<range2> --json
gws sheets spreadsheets.values batchUpdate <spreadsheetId> --data <json>
```

### Google Calendar

```bash
gws calendar calendarList list --json
gws calendar calendarList get <calendarId> --json
gws calendar events list <calendarId> --timeMin <datetime> --timeMax <datetime> --json
gws calendar events get <calendarId> <eventId> --json
gws calendar events insert <calendarId> --summary <title> --start <datetime> --end <datetime> --attendees <emails>
gws calendar events update <calendarId> <eventId> --summary <title>
gws calendar events patch <calendarId> <eventId> --start <datetime> --end <datetime>
gws calendar events delete <calendarId> <eventId>
gws calendar freebusy query --timeMin <start> --timeMax <end> --items <calendarId1>,<calendarId2> --json
```

### Google Docs

```bash
gws docs documents create --title <title> --json
gws docs documents get <documentId> --json
gws docs documents batchUpdate <documentId> --requests <json>
```

### Google Slides

```bash
gws slides presentations create --title <title> --json
gws slides presentations get <presentationId> --json
gws slides presentations.pages get <presentationId> <pageId> --json
gws slides presentations.pages getThumbnail <presentationId> <pageId> --json
```

### Google Chat

```bash
gws chat spaces list --json
gws chat spaces get <spaceName> --json
gws chat spaces.messages create <spaceName> --text <message>
gws chat spaces.messages list <spaceName> --json
gws chat spaces.messages get <messageName> --json
gws chat spaces.members list <spaceName> --json
```

### Google Tasks

```bash
gws tasks tasklists list --json
gws tasks tasklists get <tasklistId> --json
gws tasks tasklists insert --title <title> --json
gws tasks tasks list <tasklistId> --json
gws tasks tasks get <tasklistId> <taskId> --json
gws tasks tasks insert <tasklistId> --title <title> --due <datetime>
gws tasks tasks update <tasklistId> <taskId> --status completed
gws tasks tasks delete <tasklistId> <taskId>
```

### Admin SDK (Directory)

```bash
gws admin users list --domain <domain> --json
gws admin users get <email> --json
gws admin users insert --primaryEmail <email> --name.givenName <first> --name.familyName <last>
gws admin users update <email> --suspended true
gws admin groups list --domain <domain> --json
gws admin groups get <email> --json
gws admin groups insert --email <email> --name <name>
gws admin groups.members list <groupEmail> --json
gws admin groups.members insert <groupEmail> --email <memberEmail> --role MEMBER
gws admin orgunits list --customerId my_customer --json
```

### Google Groups

```bash
gws groups groups list --domain <domain> --json
gws groups groups get <email> --json
gws groups memberships list <groupEmail> --json
```

### Google People (Contacts)

```bash
gws people people.connections list me --personFields names,emailAddresses --json
gws people people get <resourceName> --personFields names,emailAddresses,phoneNumbers --json
gws people people searchContacts --query <term> --readMask names,emailAddresses --json
```

### Google Meet

```bash
gws meet spaces create --json
gws meet spaces get <spaceName> --json
gws meet conferenceRecords list --json
```

### Google Classroom

```bash
gws classroom courses list --json
gws classroom courses get <courseId> --json
gws classroom courses.courseWork list <courseId> --json
gws classroom courses.students list <courseId> --json
```

### Google Forms

```bash
gws forms forms get <formId> --json
gws forms forms.responses list <formId> --json
```

### Google Keep

```bash
gws keep notes list --json
gws keep notes get <noteId> --json
```

### Google Sites

```bash
gws sites sites list --json
gws sites sites get <siteId> --json
```

### Google Vault

```bash
gws vault matters list --json
gws vault matters get <matterId> --json
gws vault matters.holds list <matterId> --json
```

### Admin Reports / Activities

```bash
gws admin activities list <applicationName> --json
gws admin activities list login --json
gws admin activities list drive --json
gws admin activities list admin --json
```

---

## Helper Commands (22)

| Helper | Description | Example |
|--------|-------------|---------|
| `send` | Quick send email | `gws helpers send --to a@b.com --subject Hi --body Hello` |
| `reply` | Quick reply | `gws helpers reply --thread <id> --body Thanks` |
| `forward` | Quick forward | `gws helpers forward --message <id> --to a@b.com` |
| `upload` | Quick upload to Drive | `gws helpers upload file.pdf --folder <id>` |
| `download` | Quick download | `gws helpers download <fileId> --output file.pdf` |
| `share` | Quick share | `gws helpers share <fileId> --with a@b.com --role writer` |
| `quick-event` | Natural language event | `gws helpers quick-event "Lunch tomorrow at noon"` |
| `find-time` | Find free slots | `gws helpers find-time --attendees a,b --duration 60` |
| `standup-report` | Daily standup | `gws helpers standup-report` |
| `meeting-prep` | Prep for meeting | `gws helpers meeting-prep --event <id>` |
| `weekly-summary` | Week summary | `gws helpers weekly-summary` |
| `morning-briefing` | Morning overview | `gws helpers morning-briefing` |
| `eod-wrap` | End of day wrap | `gws helpers eod-wrap` |
| `inbox-zero` | Process inbox | `gws helpers inbox-zero` |
| `search` | Cross-service search | `gws helpers search "quarterly report"` |
| `create-task` | Quick task creation | `gws helpers create-task "Review PR" --due tomorrow` |
| `list-tasks` | Quick task listing | `gws helpers list-tasks` |
| `chat-send` | Quick chat message | `gws helpers chat-send --space <id> --text "Hello"` |
| `export-pdf` | Export as PDF | `gws helpers export-pdf <fileId> --output file.pdf` |
| `trash-old` | Trash old files | `gws helpers trash-old --older-than 365d` |
| `audit-sharing` | Audit file sharing | `gws helpers audit-sharing --folder <id>` |
| `backup-labels` | Backup Gmail labels | `gws helpers backup-labels --output labels.json` |

---

## Schema Introspection

```bash
# View the API schema for any service method
gws schema gmail.users.messages.list
gws schema drive.files.create
gws schema calendar.events.insert

# List all available services
gws schema --list

# List methods for a service
gws schema gmail --methods
```

---

## Authentication Commands

```bash
gws auth setup                      # Interactive OAuth setup
gws auth setup --service-account    # Service account setup
gws auth status                     # Check current auth
gws auth status --json              # JSON auth details
gws auth refresh                    # Refresh expired token
gws auth revoke                     # Revoke current token
gws auth switch <profile>           # Switch auth profile
gws auth profiles list              # List saved profiles
```

---

## Recipe Commands

```bash
gws recipes list                    # List all 43 recipes
gws recipes list --category email   # Filter by category
gws recipes describe <name>         # Show recipe details
gws recipes run <name>              # Execute a recipe
gws recipes run <name> --dry-run    # Preview recipe commands
```

---

## Persona Commands

```bash
gws persona list                    # List all 10 personas
gws persona select <name>           # Activate a persona
gws persona show                    # Show active persona
gws persona recipes                 # Show recipes for active persona
```
