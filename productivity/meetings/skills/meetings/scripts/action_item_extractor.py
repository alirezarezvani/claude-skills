#!/usr/bin/env python3
"""action_item_extractor.py — Turn raw meeting notes into an owned, dated action checklist.

The `meetings` skill's third discipline: a meeting that ends without owned, dated actions was
theater. This script parses raw notes (from --input FILE or stdin) and extracts action items via
deterministic patterns:

  - "- [ ] ..." / "* [ ] ..."          markdown checkboxes
  - "ACTION: ..." / "TODO: ..."        explicit prefixes (case-insensitive)
  - "@name will ..." / "@name to ..."  mention-owned commitments
  - "Name will <verb> ... by <date>"   prose commitments (capitalized name, pronouns excluded)

For every item it captures the OWNER (an @mention leading the item, or the leading
"Name will/to" name) and the DUE DATE ("by/due/before <weekday|today|tomorrow|EOD|EOW|
YYYY-MM-DD|D/M|Month D>") when present, then flags:

  ORPHAN  — no owner captured. Unowned actions die; assign before posting.
  NO-DUE  — owner but no date. Undated actions drift; date them now.

Output: a markdown checklist grouped by owner (orphans last, loudly) + summary counts, or --json.

NO LLM CALLS. Pure regex + grouping. Stdlib only. Nothing is sent anywhere.

Usage:
    python action_item_extractor.py --input notes.md
    cat notes.md | python action_item_extractor.py
    python action_item_extractor.py --sample --json
"""

import argparse
import json
import re
import sys
from typing import Any, Dict, List, Optional, Tuple

CHECKBOX_RE = re.compile(r"^\s*[-*]\s*\[\s*\]\s*(?P<text>.+)$")
PREFIX_RE = re.compile(r"^\s*(?:ACTION|TODO)\s*:\s*(?P<text>.+)$", re.IGNORECASE)
MENTION_OWNED_RE = re.compile(r"^\s*@(?P<owner>[A-Za-z][\w.\-]*)\s+(?:will|to)\s+(?P<text>.+)$")
NAME_WILL_RE = re.compile(r"^\s*(?P<owner>[A-Z][a-zA-Z]+)\s+(?:will|to)\s+(?P<text>.+)$")
MENTION_HEAD_RE = re.compile(r"^\s*@(?P<owner>[A-Za-z][\w.\-]*)\s*[:,—-]?\s*(?P<text>.*)$")
INNER_NAME_WILL_RE = re.compile(r"^(?P<owner>[A-Z][a-zA-Z]+)\s+(?:will|to)\s+(?P<text>.+)$")

_DATE_TOKEN = (
    r"(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday|today|tomorrow|eod|eow"
    r"|\d{4}-\d{2}-\d{2}"
    r"|\d{1,2}/\d{1,2}(?:/\d{2,4})?"
    r"|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s+\d{1,2})"
)
DUE_RE = re.compile(r"\b(?:by|due|before)\s+(?P<due>" + _DATE_TOKEN + r")\b", re.IGNORECASE)

PRONOUNS = {"We", "I", "It", "They", "This", "That", "You", "He", "She",
            "Everyone", "Someone", "Anybody", "Nobody", "Team", "The"}

# Sentence-initial capitalized words that are never a person committing to an action.
NON_OWNER_WORDS = PRONOUNS | {
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday",
    "January", "February", "March", "April", "May", "June", "July", "August",
    "September", "October", "November", "December",
    "Today", "Tomorrow", "Tonight", "Next", "Last", "There",
    "Everything", "Nothing", "Something", "Everybody",
}

# "Name will <stative>" is a prediction or status, not a commitment
# ("Friday will be a half day", "Design will need another pass").
STATIVE_CONTINUATIONS = {"be", "need", "probably", "likely", "not", "also",
                         "still", "never", "just", "only"}


def _is_commitment(text: str, owner: str) -> bool:
    """A 'Name will/to ...' line is a commitment only if Name can be a person
    and what follows reads as an action, not a stative prediction."""
    if owner in NON_OWNER_WORDS:
        return False
    first = text.strip().split(None, 1)[0].lower() if text.strip() else ""
    return first not in STATIVE_CONTINUATIONS

EPILOG = """\
exit codes:
  0   success — checklist emitted (ORPHAN / NO-DUE items are flagged in the output, not fatal)
  2   no input — neither --input, --sample, nor piped stdin was provided (or file unreadable)

--help and --sample exit 0.
"""


def _extract_owner_and_text(text: str, owner: Optional[str]) -> Tuple[Optional[str], str]:
    """Refine owner from an already-captured action text.

    Only a mention that LEADS the item confers ownership ("@sam: book the room",
    "@sam to book the room"). A mid-text mention is the task's object, not its
    owner ("follow up with @sam") — those stay ORPHAN for a human to assign.
    """
    m = MENTION_OWNED_RE.match(text.strip())
    if m:  # "@owner will/to rest" at the head — strip the owner phrase from the text
        return m.group("owner"), m.group("text")
    m = MENTION_HEAD_RE.match(text.strip())
    if m:
        return m.group("owner"), (m.group("text") or text)
    m = INNER_NAME_WILL_RE.match(text.strip())
    if m and _is_commitment(m.group("text"), m.group("owner")):
        return m.group("owner"), m.group("text")
    return owner, text


def extract(notes: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    for lineno, raw in enumerate(notes.splitlines(), 1):
        line = raw.rstrip()
        if not line.strip():
            continue
        owner: Optional[str] = None
        text: Optional[str] = None

        m = CHECKBOX_RE.match(line)
        if m:
            text = m.group("text").strip()
        else:
            m = PREFIX_RE.match(line)
            if m:
                text = m.group("text").strip()
            else:
                m = MENTION_OWNED_RE.match(line)
                if m:
                    owner, text = m.group("owner"), m.group("text").strip()
                else:
                    m = NAME_WILL_RE.match(line)
                    if m and _is_commitment(m.group("text"), m.group("owner")):
                        owner, text = m.group("owner"), m.group("text").strip()

        if text is None:
            continue

        # Refine only when no owner was captured at the head of the line — an
        # already-owned commitment may legitimately name other people in its text
        # ("@maria will ask @sam to review") without transferring ownership.
        if owner is None:
            owner, text = _extract_owner_and_text(text, owner)
        due_m = DUE_RE.search(line)
        due = due_m.group("due") if due_m else None
        text = text.rstrip(".").strip()

        flags: List[str] = []
        if not owner:
            flags.append("ORPHAN")
        if not due:
            flags.append("NO-DUE")
        items.append({"line": lineno, "text": text, "owner": owner, "due": due, "flags": flags})
    return items


def summarize(items: List[Dict[str, Any]]) -> Dict[str, int]:
    return {
        "total": len(items),
        "owned": sum(1 for i in items if i["owner"]),
        "orphans": sum(1 for i in items if "ORPHAN" in i["flags"]),
        "no_due": sum(1 for i in items if "NO-DUE" in i["flags"]),
    }


def render_markdown(items: List[Dict[str, Any]]) -> str:
    out: List[str] = ["## Action Items", ""]
    if not items:
        out.append("_No action items detected. If decisions were made, they left no owners — "
                    "that is worth fixing in the room next time._")
        return "\n".join(out)

    owners = sorted({i["owner"] for i in items if i["owner"]}, key=str.lower)
    for owner in owners:
        out.append(f"### {owner}")
        for i in items:
            if i["owner"] == owner:
                due = f" — due {i['due']}" if i["due"] else "  **[NO-DUE — date it now]**"
                out.append(f"- [ ] {i['text']}{due}")
        out.append("")

    orphans = [i for i in items if not i["owner"]]
    if orphans:
        out.append("### (unassigned) — ORPHANS, assign before posting")
        for i in orphans:
            due = f" — due {i['due']}" if i["due"] else ""
            out.append(f"- [ ] {i['text']}{due}  **[ORPHAN]**")
        out.append("")

    s = summarize(items)
    out.append(f"**Summary:** {s['total']} actions · {s['owned']} owned · "
               f"{s['orphans']} ORPHAN · {s['no_due']} NO-DUE")
    if s["orphans"]:
        out.append("")
        out.append("_Every action item has an owner and a date — or it is not an action item. "
                   "Assign the orphans while the room still remembers agreeing to them._")
    return "\n".join(out)


SAMPLE_NOTES = """\
Notes — Q3 planning sync

Maria will send the pricing one-pager by Friday.
We agreed the roadmap shape looks fine overall.
- [ ] update the launch checklist
ACTION: @sam to book the security review by 2026-07-24
TODO: draft the customer announcement email
Alex will confirm vendor pricing.
It will probably rain during the offsite.
"""


def main(argv: List[str]) -> int:
    p = argparse.ArgumentParser(
        description="Extract owned, dated action items from raw meeting notes (flags ORPHAN / NO-DUE).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG,
    )
    p.add_argument("--input", metavar="FILE", help="Notes file to read (otherwise stdin is used)")
    p.add_argument("--sample", action="store_true", help="Run on the embedded example notes")
    p.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of markdown")
    args = p.parse_args(argv)

    if args.sample:
        notes = SAMPLE_NOTES
    elif args.input:
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                notes = f.read()
        except OSError as e:
            print(f"error: cannot read {args.input}: {e}", file=sys.stderr)
            return 2
    elif not sys.stdin.isatty():
        notes = sys.stdin.read()
    else:
        p.print_help()
        print("\nerror: provide --input FILE, pipe notes on stdin, or use --sample", file=sys.stderr)
        return 2

    items = extract(notes)
    if args.json:
        print(json.dumps({"items": items, "summary": summarize(items)}, indent=2))
    else:
        print(render_markdown(items))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
