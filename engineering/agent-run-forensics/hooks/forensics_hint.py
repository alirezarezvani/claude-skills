#!/usr/bin/env python3
"""UserPromptSubmit hook: point questions about past work at the recording.

Reads the hook payload on stdin. When the prompt asks about something that
already happened ("why did you delete...", "what did the agent run last
night", "did the tests actually pass"), it prints one short note with this
session's transcript path and the command that reads it. Any other prompt
gets no output. The note is a pointer, not an instruction to run anything.

Fails open: any error prints nothing and exits 0. Never blocks a prompt.
Disable with AGENT_RUN_FORENSICS_HOOK=0.

Usage (Claude Code runs it; to try it by hand):
  echo '{"prompt":"why did you change config.yaml?","transcript_path":"/x.jsonl"}' | python3 forensics_hint.py
  python3 forensics_hint.py --sample
"""
import json
import os
import re
import sys

# A question about the past, aimed at the agent or a run. Each pattern needs a
# past-tense action word, so "why does this function fail" does not match.
PATTERNS = [
    r"\bwhy did (you|it|the agent|claude|codex)\b",
    r"\bwhy (have|had) you\b",
    r"\bwhat did (you|the agent|claude|codex|it) (do|change|run|touch|delete|edit|break|modify)\b",
    r"\bdid (you|the agent|claude|codex) (actually |really |even )?(run|test|change|delete|touch|modify|edit|break|commit|push|read)\b",
    r"\bdid the (tests?|build|checks?|ci|linter|migration)s? (actually |really )?(pass|run|fail|succeed)\b",
    r"\bwho (changed|deleted|removed|overwrote|broke)\b",
    r"\b(you|the agent|claude|codex) (changed|deleted|removed|overwrote|broke|reverted)\b.*\?",
    r"\bwhat happened (in|during|with|to) (the |that |this |last |yesterday)",
    r"\b(last|previous|earlier|yesterday's|last night's) (session|run|night's run)\b",
    r"\bwhen did (you|the agent|claude|codex)\b",
    r"\b(walk|take) me through what (you|the agent|it) did\b",
    r"\bverify (your|the|that) (summary|report|claims?)\b",
]
RX = re.compile("|".join(PATTERNS), re.I)

NOTE = ("This question is about work that already happened. Answer from the recording, not from memory: "
        "the transcript of this session is {path}. Read it with "
        "`python3 {scripts}/trace_timeline.py --trace {path}` (add --files, --errors, --grep TEXT or --why STEP); "
        "for an earlier session use `{scripts}/trace_finder.py --since 7d`. Label each cause recorded or inferred, "
        "and if the trace does not hold the answer, say so.")


def note_for(payload):
    prompt = str(payload.get("prompt") or "")
    if not prompt or not RX.search(prompt):
        return None
    root = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    scripts = os.path.join(root, "skills", "agent-run-forensics", "scripts")
    path = payload.get("transcript_path") or "(unknown: use trace_finder.py)"
    return NOTE.format(path=path, scripts=scripts)


def main():
    if os.environ.get("AGENT_RUN_FORENSICS_HOOK", "1") == "0":
        return 0
    if "--help" in sys.argv or "-h" in sys.argv:
        print(__doc__)
        return 0
    try:
        if "--sample" in sys.argv:
            payload = {"prompt": "Why did you change the timeout in config.yaml?",
                       "transcript_path": "~/.claude/projects/-work-shop-api/sample.jsonl"}
        else:
            payload = json.loads(sys.stdin.read() or "{}")
        note = note_for(payload if isinstance(payload, dict) else {})
        if note:
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "UserPromptSubmit",
                                                     "additionalContext": note}}))
    except Exception:  # noqa: BLE001 - a hook must never break the prompt
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
