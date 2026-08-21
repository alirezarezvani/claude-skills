#!/usr/bin/env python3
"""Parse a human-gate review sidecar into a structured feedback batch (batch.v1).

The sidecar is a plain Markdown file a person can write by hand in any editor,
or export from the review page built by review_page_builder.py. Keeping it
hand-writable is deliberate: it is what lets the review loop work over SSH, in
CI, and on a machine with no browser.

Format
------
    # Review feedback: report.md
    <!-- human-gate:v1 target=report.md round=1 -->

    reviewer: reza

    ## BLOCKER b3
    > the exact quoted text from the block
    We have no data for this claim. Cite it or cut it.

    ## EDIT b7
    - before: The system recieve requests
    + after:  The system receives requests

    ## NIT b9
    Trailing whitespace in the table.

    ## NOTE
    Close. Ship once the blocker is gone.

The `<!-- human-gate:v1 ... -->` header carries `key=value` attributes; quote any
value containing a space (`target="q3 plan.md"`). `target` is a display hint only
— quote verification runs against the path passed as `--target`.

Severities are BLOCKER / MAJOR / MINOR / NIT (the same ladder markdown-html's
md-review uses, from Google's Code Review Developer Guide), plus three
non-severity kinds: EDIT (a verbatim replacement the human already wrote),
NOTE (unanchored commentary) and APPROVE (an explicit sign-off).

Exit codes
----------
    0  parsed cleanly
    1  usage error / unreadable input
    2  parsed, but --strict found problems (unknown severity, EDIT without an
       after, missing reviewer, or a quote that is not in the target)
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys

SCHEMA = "batch.v1"

# Two problems already have a dedicated gate rule in human_gate.py (G3 and G2),
# so its G7 integrity check must skip them rather than report them twice. It
# matches on these prefixes, which is why they live here beside the
# problems.append() calls that emit them: rewording a message without touching
# the constant would silently make a gated problem ungated.
P_NO_REVIEWER = "no 'reviewer:' line"          # human_gate.py G3
P_APPROVE_WITH_BLOCKING = "APPROVE is present alongside"  # human_gate.py G2
GATED_ELSEWHERE = (P_NO_REVIEWER, P_APPROVE_WITH_BLOCKING)

SEVERITIES = ["BLOCKER", "MAJOR", "MINOR", "NIT"]
BLOCKING = {"BLOCKER", "MAJOR"}
OTHER_KINDS = ["EDIT", "NOTE", "APPROVE"]
ALL_HEADINGS = SEVERITIES + OTHER_KINDS

HEADER_RE = re.compile(
    r"^\s*<!--\s*human-gate:v1\s+(?P<attrs>.*?)\s*-->\s*$", re.IGNORECASE
)
# Header attributes are `key=value` pairs. A value containing spaces — a target
# filename with a space in it — must be quoted, or it truncates at the space.
ATTR_RE = re.compile(r"""(\w+)=(?:"([^"]*)"|'([^']*)'|([^\s'"]+))""")
REVIEWER_RE = re.compile(r"^\s*reviewer\s*:\s*(?P<name>.+?)\s*$", re.IGNORECASE)
# "## BLOCKER b3", "## NIT", "## EDIT b7", "## NOTE"
ITEM_RE = re.compile(
    r"^\s*##\s+(?P<kind>[A-Za-z]+)\s*(?P<block>[A-Za-z0-9_-]+)?\s*$"
)
QUOTE_RE = re.compile(r"^\s*>\s?(?P<text>.*)$")
BEFORE_RE = re.compile(r"^\s*-\s*before\s*:\s?(?P<text>.*)$", re.IGNORECASE)
AFTER_RE = re.compile(r"^\s*\+\s*after\s*:\s?(?P<text>.*)$", re.IGNORECASE)

SAMPLE = """# Review feedback: quarterly-plan.md
<!-- human-gate:v1 target=quarterly-plan.md round=1 -->

reviewer: reza

## BLOCKER b2
> We expect a 40% lift in activation.
Where does 40% come from? No source, and it drives the whole plan. Cite it or cut it.

## MAJOR b5
The risks section does not mention the vendor contract expiring in Q3.

## EDIT b7
- before: The team will endeavour to deliver incremental value
+ after: The team ships one usable slice per week

## NIT b9
"recieve" -> "receive".

## NOTE
Structure is right. Fix the blocker and this is good to go.
"""


def _strip_comments(lines):
    """Drop HTML-comment content, keeping the human-gate:v1 header line.

    Sidecars carry explanatory comments — the shipped example asset documents
    the format inside one. Without this, a '## APPROVE' written as an example
    inside a comment parses as a real sign-off, which is exactly the kind of
    silent false approval this whole skill exists to prevent.

    Comments inside fenced code blocks are left alone; there they are content.
    """
    kept = []
    fence = False
    in_comment = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            kept.append(line)
            continue
        if fence:
            kept.append(line)
            continue

        if in_comment:
            if "-->" in line:
                in_comment = False
                remainder = line.split("-->", 1)[1]
                if remainder.strip():
                    kept.append(remainder)
            continue

        if "<!--" in line:
            if HEADER_RE.match(line):
                kept.append(line)
                continue
            head = line.split("<!--", 1)[0]
            rest = line.split("<!--", 1)[1]
            if "-->" in rest:
                tail = rest.split("-->", 1)[1]
                merged = head + tail
                if merged.strip():
                    kept.append(merged)
            else:
                in_comment = True
                if head.strip():
                    kept.append(head)
            continue

        kept.append(line)
    return kept


def _strip_fence_markers(lines):
    """Yield (line, in_code_fence) so fenced blocks never parse as items."""
    fence = False
    for line in lines:
        if line.lstrip().startswith("```"):
            fence = not fence
            yield line, True
            continue
        yield line, fence


def parse(text, target_hint=None):
    """Parse sidecar text into a batch.v1 dict plus a list of problem strings."""
    problems = []
    lines = _strip_comments(text.splitlines())

    meta = {"target": target_hint or "", "round": 1}
    reviewer = ""

    items = []
    current = None
    overall = []

    def flush():
        nonlocal current
        if current is None:
            return
        body = "\n".join(current.pop("_body")).strip()
        if current["kind"] == "NOTE":
            if body:
                overall.append(body)
            current = None
            return
        if current["kind"] == "EDIT":
            if not current.get("after"):
                problems.append(
                    "EDIT item on block %s has no '+ after:' line; an edit "
                    "without replacement text cannot be applied"
                    % (current.get("block") or "?")
                )
            if body:
                current["feedback"] = body
        else:
            current["feedback"] = body
            if not body and not current.get("quote"):
                problems.append(
                    "%s item on block %s is empty"
                    % (current["kind"], current.get("block") or "?")
                )
        items.append(current)
        current = None

    for raw, in_fence in _strip_fence_markers(lines):
        if in_fence:
            if current is not None:
                current["_body"].append(raw)
            continue

        header = HEADER_RE.match(raw)
        if header:
            for match in ATTR_RE.finditer(header.group("attrs")):
                key = match.group(1)
                value = next(g for g in match.groups()[1:] if g is not None)
                if key == "round":
                    try:
                        meta["round"] = int(value)
                    except ValueError:
                        problems.append("round=%r is not an integer" % value)
                else:
                    meta[key] = value
            continue

        if current is None:
            found = REVIEWER_RE.match(raw)
            if found and not reviewer:
                reviewer = found.group("name")
                continue

        item = ITEM_RE.match(raw)
        if item:
            flush()
            kind = item.group("kind").upper()
            if kind not in ALL_HEADINGS:
                problems.append(
                    "unknown severity/kind %r (expected one of %s)"
                    % (kind, ", ".join(ALL_HEADINGS))
                )
            current = {
                "id": "f%d" % (len(items) + 1),
                "kind": kind,
                "block": item.group("block") or "",
                "quote": "",
                "feedback": "",
                "_body": [],
            }
            if kind == "EDIT":
                current["before"] = ""
                current["after"] = ""
            continue

        if current is None:
            continue

        quote = QUOTE_RE.match(raw)
        if quote and not current["feedback"]:
            existing = current["quote"]
            current["quote"] = (
                existing + "\n" + quote.group("text") if existing else quote.group("text")
            )
            continue

        if current["kind"] == "EDIT":
            before = BEFORE_RE.match(raw)
            if before:
                current["before"] = before.group("text")
                continue
            after = AFTER_RE.match(raw)
            if after:
                current["after"] = after.group("text")
                continue

        current["_body"].append(raw)

    flush()

    for item in items:
        item.pop("_body", None)
        if item["kind"] in SEVERITIES:
            item["severity"] = item["kind"]
            item["kind"] = "comment"
        elif item["kind"] == "EDIT":
            item["severity"] = "MINOR"
            item["kind"] = "edit"
        elif item["kind"] == "APPROVE":
            item["severity"] = "NIT"
            item["kind"] = "approve"
        else:
            item["severity"] = "NIT"
            item["kind"] = "comment"

    counts = {}
    for item in items:
        key = {"edit": "EDIT", "approve": "APPROVE"}.get(item["kind"], item["severity"])
        counts[key] = counts.get(key, 0) + 1

    approved = any(i["kind"] == "approve" for i in items)
    blocking = [
        i for i in items if i["kind"] == "comment" and i["severity"] in BLOCKING
    ]

    if not reviewer:
        problems.append(
            "%s — human-gate requires a named reviewer so the approval "
            "belongs to a person, not to the loop" % P_NO_REVIEWER
        )
    if approved and blocking:
        problems.append(
            "%s %d unresolved BLOCKER/MAJOR item(s); resolve or downgrade "
            "them before signing off" % (P_APPROVE_WITH_BLOCKING, len(blocking))
        )

    batch = {
        "schema": SCHEMA,
        "target": meta.get("target", ""),
        "round": meta.get("round", 1),
        "reviewer": reviewer,
        "approved": approved and not blocking,
        "blocking_open": len(blocking),
        "counts": counts,
        "items": items,
        "overall_note": "\n\n".join(overall),
    }
    return batch, problems


def plain_text(source, is_html=False):
    """Approximate what the browser renders, so quotes can be matched fairly.

    A reviewer selects text in the *rendered* page, so `window.getSelection()`
    hands back "We expect a 40% lift" for source that reads
    "We expect a **40%** lift". Comparing that against raw markup would flag a
    perfectly good quote — and since integrity problems now block the gate
    (G7), a false positive here refuses a legitimate close.
    """
    text = source
    if is_html:
        text = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
        text = re.sub(r"(?s)<!--.*?-->", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        return html.unescape(text)

    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)   # images -> alt
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)     # links -> label
    text = re.sub(r"`([^`]+)`", r"\1", text)                 # inline code
    text = re.sub(r"\*\*([^*]+)\*\*", r"\1", text)           # bold
    text = re.sub(r"__([^_]+)__", r"\1", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", text)  # italic
    text = re.sub(r"(?<!_)_([^_\n]+)_(?!_)", r"\1", text)
    text = re.sub(r"(?m)^\s{0,3}#{1,6}\s+", "", text)        # heading markers
    text = re.sub(r"(?m)^\s{0,3}>\s?", "", text)             # blockquote markers
    return text


def verify_quotes(batch, target_path):
    """Report quotes that appear in neither the raw source nor its rendered text."""
    problems = []
    try:
        with open(target_path, "r", encoding="utf-8") as handle:
            source = handle.read()
    except OSError as err:
        return ["could not read target %s to verify quotes: %s" % (target_path, err)]

    squash = lambda s: re.sub(r"\s+", " ", s)
    is_html = os.path.splitext(target_path)[1].lower() in (".html", ".htm")
    haystacks = (squash(source), squash(plain_text(source, is_html=is_html)))

    for item in batch["items"]:
        quote = item.get("quote", "").strip()
        if not quote:
            continue
        needle = squash(quote)
        if not any(needle in hay for hay in haystacks):
            problems.append(
                "item %s quotes text not found in %s: %r"
                % (item["id"], os.path.basename(target_path), quote[:60])
            )
    return problems


def render_human(batch, problems):
    out = []
    out.append("Review batch — %s (round %d)" % (batch["target"] or "?", batch["round"]))
    out.append("Reviewer: %s" % (batch["reviewer"] or "(none — required)"))
    order = SEVERITIES + ["EDIT", "APPROVE"]
    summary = " · ".join(
        "%d %s" % (batch["counts"][k], k) for k in order if k in batch["counts"]
    )
    out.append("Items: %s" % (summary or "none"))
    out.append(
        "Verdict: %s"
        % (
            "APPROVED"
            if batch["approved"]
            else "%d blocking item(s) open" % batch["blocking_open"]
        )
    )
    if batch["items"]:
        out.append("")
        for item in batch["items"]:
            label = {"edit": "EDIT", "approve": "APPROVE"}.get(
                item["kind"], item["severity"]
            )
            where = (" @%s" % item["block"]) if item["block"] else ""
            out.append("  [%s]%s %s" % (label, where, item["id"]))
            if item.get("quote"):
                out.append('      > "%s"' % item["quote"].replace("\n", " ")[:76])
            if item["kind"] == "edit":
                out.append("      before: %s" % item.get("before", ""))
                out.append("      after:  %s" % item.get("after", ""))
            if item.get("feedback"):
                out.append("      %s" % item["feedback"].replace("\n", " ")[:76])
    if batch["overall_note"]:
        out.append("")
        out.append("Overall: %s" % batch["overall_note"])
    if problems:
        out.append("")
        out.append("Problems (%d):" % len(problems))
        for problem in problems:
            out.append("  - %s" % problem)
    return "\n".join(out)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Parse a human-gate review sidecar into a batch.v1 feedback batch.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("sidecar", nargs="?", help="path to <artifact>.review.md")
    parser.add_argument("--target", help="reviewed artifact, for quote verification")
    parser.add_argument(
        "--output", choices=["human", "json"], default="human", help="output format"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="exit 2 when any problem is found (use in the gate, not while drafting)",
    )
    parser.add_argument(
        "--sample", action="store_true", help="parse a built-in sample sidecar and exit"
    )
    args = parser.parse_args(argv)

    if args.sample:
        text, target_hint = SAMPLE, "quarterly-plan.md"
    elif args.sidecar:
        try:
            with open(args.sidecar, "r", encoding="utf-8") as handle:
                text = handle.read()
        except OSError as err:
            parser.error("cannot read %s: %s" % (args.sidecar, err))
            return 1
        target_hint = args.target or ""
    else:
        parser.error("provide a sidecar path or --sample")
        return 1

    batch, problems = parse(text, target_hint or None)
    if args.target and os.path.exists(args.target):
        problems.extend(verify_quotes(batch, args.target))

    if args.output == "json":
        print(json.dumps({"batch": batch, "problems": problems}, indent=2))
    else:
        print(render_human(batch, problems))

    return 2 if (problems and args.strict) else 0


if __name__ == "__main__":
    sys.exit(main())
