# Google Workspace CLI Recipes Cookbook

Complete catalog of 43 built-in recipes organized by category, with command sequences and persona mapping.

---

## Recipe Categories

| Category | Count | Description |
|----------|-------|-------------|
| Email | 8 | Gmail operations — send, search, label, filter |
| Files | 7 | Drive file management — upload, share, export |
| Calendar | 6 | Events, scheduling, meeting prep |
| Reporting | 5 | Activity summaries and analytics |
| Collaboration | 5 | Chat, Docs, Tasks teamwork |
| Data | 4 | Sheets read/write and contacts |
| Admin | 4 | User and group management |
| Cross-Service | 4 | Multi-service workflows |

---

## Email Recipes (8)

### send-email
Send an email with optional attachments.
```bash
gws gmail users.messages send me --to "recipient@example.com" \
  --subject "Subject" --body "Body text" [--attachment file.pdf]
```

### reply-to-thread
Reply to an existing email thread.
```bash
gws gmail users.messages reply me --thread-id <THREAD_ID> --body "Reply text"
```

### forward-email
Forward an email to another recipient.
```bash
gws gmail users.messages forward me --message-id <MSG_ID> --to "forward@example.com"
```

### search-emails
Search emails using Gmail query syntax.
```bash
gws gmail users.messages list me --query "from:sender@example.com after:2025/01/01" --json
```
**Query examples:** `is:unread`, `has:attachment`, `label:important`, `newer_than:7d`

### archive-old
Archive read emails older than N days.
```bash
gws gmail users.messages list me --query "is:read older_than:30d" --json
# Extract IDs, then batch modify to remove INBOX label
```

### label-manager
Create and organize Gmail labels.
```bash
gws gmail users.labels list me --json
gws gmail users.labels create me --name "Projects/Alpha"
```

### filter-setup
Create auto-labeling filters.
```bash
gws gmail users.settings.filters create me \
  --criteria '{"from":"notifications@service.com"}' \
  --action '{"addLabelIds":["Label_123"],"removeLabelIds":["INBOX"]}'
```

### unread-digest
Get digest of unread emails.
```bash
gws gmail users.messages list me --query "is:unread" --limit 20 --json
```

---

## Files Recipes (7)

### upload-file
Upload a file to Google Drive.
```bash
gws drive files create --name "Report Q1" --upload report.pdf --parents <FOLDER_ID>
```

### create-sheet
Create a new Google Spreadsheet.
```bash
gws sheets spreadsheets create --title "Budget 2026" --json
```

### share-file
Share a Drive file with a user or domain.
```bash
gws drive permissions create <FILE_ID> --type user --role writer --emailAddress "user@example.com"
```

### export-file
Export a Google Doc/Sheet as PDF.
```bash
gws drive files export <FILE_ID> --mime "application/pdf" --output report.pdf
```

### list-files
List files in a Drive folder.
```bash
gws drive files list --parents <FOLDER_ID> --json
```

### find-large-files
Find the largest files in Drive.
```bash
gws drive files list --orderBy "quotaBytesUsed desc" --limit 20 --json
```

### cleanup-trash
Empty Drive trash.
```bash
gws drive files emptyTrash
```

---

## Calendar Recipes (6)

### create-event
Create a calendar event with attendees.
```bash
gws calendar events insert primary \
  --summary "Sprint Planning" \
  --start "2026-03-15T10:00:00" --end "2026-03-15T11:00:00" \
  --attendees "team@company.com" --location "Room A"
```

### quick-event
Create event from natural language.
```bash
gws helpers quick-event "Lunch with Sarah tomorrow at noon"
```

### find-time
Find available time slots for a meeting.
```bash
gws helpers find-time --attendees "alice@co.com,bob@co.com" --duration 60 \
  --within "2026-03-15,2026-03-19" --json
```

### today-schedule
Show today's calendar events.
```bash
gws calendar events list primary \
  --timeMin "$(date -u +%Y-%m-%dT00:00:00Z)" \
  --timeMax "$(date -u +%Y-%m-%dT23:59:59Z)" --json
```

### meeting-prep
Prepare for an upcoming meeting.
```bash
gws recipes meeting-prep --event-id <EVENT_ID>
```
**Output:** Agenda, attendee list, related Drive files, previous meeting notes.

### reschedule
Move an event to a new time.
```bash
gws calendar events patch primary <EVENT_ID> \
  --start "2026-03-16T14:00:00" --end "2026-03-16T15:00:00"
```

---

## Reporting Recipes (5)

### standup-report
Generate daily standup from calendar and tasks.
```bash
gws recipes standup-report --json
```
**Output:** Yesterday's events, today's schedule, pending tasks, blockers.

### weekly-summary
Summarize week's emails, events, and tasks.
```bash
gws recipes weekly-summary --json
```

### drive-activity
Report on Drive file activity.
```bash
gws drive activities list --json
```

### email-stats
Email volume statistics for the past 7 days.
```bash
gws gmail users.messages list me --query "newer_than:7d" --json | python3 output_analyzer.py --count
```

### task-progress
Report on task completion.
```bash
gws tasks tasks list <TASKLIST_ID> --json | python3 output_analyzer.py --group-by "status"
```

---

## Collaboration Recipes (5)

### share-folder
Share a Drive folder with a team.
```bash
gws drive permissions create <FOLDER_ID> --type group --role writer --emailAddress "team@company.com"
```

### create-doc
Create a Google Doc with initial content.
```bash
gws docs documents create --title "Meeting Notes - March 15" --json
```

### chat-message
Send a message to a Google Chat space.
```bash
gws chat spaces.messages create <SPACE_NAME> --text "Deployment complete!"
```

### list-spaces
List Google Chat spaces.
```bash
gws chat spaces list --json
```

### task-create
Create a task in Google Tasks.
```bash
gws tasks tasks insert <TASKLIST_ID> --title "Review PR #42" --due "2026-03-16"
```

---

## Data Recipes (4)

### sheet-read
Read data from a spreadsheet range.
```bash
gws sheets spreadsheets.values get <SHEET_ID> --range "Sheet1!A1:D10" --json
```

### sheet-write
Write data to a spreadsheet.
```bash
gws sheets spreadsheets.values update <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Name","Score"],["Alice",95],["Bob",87]]'
```

### sheet-append
Append rows to a spreadsheet.
```bash
gws sheets spreadsheets.values append <SHEET_ID> --range "Sheet1!A1" \
  --values '[["Charlie",92]]'
```

### export-contacts
Export contacts list.
```bash
gws people people.connections list me --personFields names,emailAddresses --json
```

---

## Admin Recipes (4)

### list-users
List all users in the Workspace domain.
```bash
gws admin users list --domain company.com --json
```
**Prerequisites:** Admin SDK API enabled, `admin.directory.user.readonly` scope.

### list-groups
List all groups in the domain.
```bash
gws admin groups list --domain company.com --json
```

### user-info
Get detailed user information.
```bash
gws admin users get user@company.com --json
```

### audit-logins
Audit recent login activity.
```bash
gws admin activities list login --json
```

---

## Cross-Service Recipes (4)

### morning-briefing
Today's events + unread emails + pending tasks.
```bash
gws recipes morning-briefing --json
```
**Combines:** Calendar events, Gmail unread count, Tasks pending.

### eod-wrap
End-of-day summary: completed, pending, tomorrow's schedule.
```bash
gws recipes eod-wrap --json
```

### project-status
Aggregate project status from Drive, Sheets, Tasks.
```bash
gws recipes project-status --project "Project Alpha" --json
```

### inbox-zero
Process inbox to zero: label, archive, reply, or create task.
```bash
gws recipes inbox-zero --interactive
```

---

## Persona Mapping

| Persona | Top Recipes |
|---------|-------------|
| Executive Assistant | morning-briefing, today-schedule, find-time, send-email, meeting-prep, eod-wrap |
| Project Manager | standup-report, create-event, find-time, task-create, project-status, weekly-summary |
| HR | list-users, user-info, send-email, create-event, create-doc, export-contacts |
| Sales | send-email, search-emails, create-event, find-time, create-doc, share-file |
| IT Admin | list-users, list-groups, audit-logins, drive-activity, find-large-files, cleanup-trash |
| Developer | sheet-read, sheet-write, upload-file, chat-message, task-create, send-email |
| Marketing | send-email, create-doc, share-file, upload-file, create-sheet, chat-message |
| Finance | sheet-read, sheet-write, sheet-append, create-sheet, export-file, share-file |
| Legal | create-doc, share-file, export-file, search-emails, upload-file, audit-logins |
| Customer Support | search-emails, send-email, reply-to-thread, label-manager, task-create, inbox-zero |
