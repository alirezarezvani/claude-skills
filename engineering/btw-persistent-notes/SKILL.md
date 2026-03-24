# /btw — Quick Notes That Stay In Context

Side notes, asides, "by the way" comments that would otherwise vanish from the conversation.

## Usage

- `/btw [note]` — Save a note
- `/btw` (no args) — Show all active notes
- `/btw clear` — Archive current notes and start fresh
- `/btw [project]` — Show notes for a specific project

## Architecture

Notes are **project-scoped** — each working directory gets its own scratchpad:

```
~/.claude/projects/{project-key}/btw-notes.md
```

This means SVIN notes don't bleed into Replayable notes, etc.

## On Save (`/btw [note]`):

1. Determine the project scratchpad path from the current working directory's project key
2. Read existing notes (or create file)
3. If note count >= 15, remove the oldest note (FIFO — prevents bloat)
4. Append with timestamp:
   ```
   - **[HH:MM]** [note text]
   ```
5. Respond: "Noted." — nothing else.

## On Show (`/btw`):

1. Read the project scratchpad
2. Display all notes
3. If empty: "No active notes."

## On Clear (`/btw clear`):

1. Move current notes to `btw-archive.md` in same directory (append with date header)
2. Empty the active scratchpad
3. Respond: "Archived and cleared."

## CRITICAL: Keeping Notes In Context

**These rules apply AT ALL TIMES, not just when /btw is invoked:**

### Rule 1: Re-read on every response
Before generating ANY response, check if `btw-notes.md` exists for the current project. If it does, read it silently. These notes are the user's active context — they override anything compacted away.

### Rule 2: Re-inject after compaction
If context compaction occurs mid-session, the btw notes file survives (it's on disk). Re-read it immediately. The notes are the user's way of saying "DO NOT FORGET THIS."

### Rule 3: Match against user references
If the user says ANY of these:
- "what I said" / "what did I say"
- "btw" / "by the way" / "my note"
- "earlier" / "remember when I said"
- "that thing" / "the thing about"

→ Check btw-notes.md FIRST before responding. If a note matches, reference it.

### Rule 4: Auto-expire stale notes
Notes older than 24 hours get moved to archive on next read. Active scratchpad stays fresh.

## Bloat Prevention

- **Max 15 notes** per project scratchpad. Oldest drops when 16th is added.
- **Auto-archive** at 24 hours. Active file never grows unbounded.
- **Project-scoped**. Each project's notes are independent. No cross-contamination.
- **Archive file** grows but is never loaded into context. Only active notes load.
- **Zero idle cost**. File only enters context when read. Not part of MEMORY.md.

## File Format

```markdown
# BTW — Active Notes

- **3:47 PM** check if claim 31 covers the scanner feature
- **4:12 PM** order test prints on spandex
- **4:30 PM** flowcode might be a blocker, need FTO
```

## Rules

- Confirmations: ONE WORD. "Noted." Period.
- User's exact words. Never edit, rephrase, or "improve."
- Never comment on the note content. Just save it.
- This is the user's short-term memory aid. Treat it as sacred.
