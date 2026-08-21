#!/usr/bin/env python3
"""Audit what a memory store actually holds: facts, skills, or logs.

Microsoft's PlugMem starts from a result that should unsettle anyone adding
memory to an agent: giving it more raw memory can make it worse. History piles
up, retrieval drowns, and the agent burns attention wading through transcripts
for the one line that mattered. The fix borrows from human memory -- we do not
replay events, we keep the facts and the skills we pulled out of them.

This tool classifies every record in a memory store as FACT, SKILL, or LOG,
finds near-duplicates, flags staleness, and scores knowledge density: how much
decision-relevant material there is per 1,000 tokens of context it costs.

It runs on either shape of memory:
  --dir   a directory of markdown/text memory files (CLAUDE.md, a wiki vault,
          agent memory files) -- records are split on markdown headings
  --jsonl a JSONL file of records, one object per line with a "text" field

Deterministic classification by lexical signal. No LLM calls, no network,
stdlib only. Classification is a triage aid, not ground truth -- it is tuned to
over-report LOG, because storing a log you thought was a fact is the failure
mode this tool exists to catch.

Exit codes:
    0  store is knowledge-dense
    2  actionable finding (log-heavy, duplicate-bloated, or stale)
    3  invalid input
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone

# Above this share of LOG records, the store is replaying events rather than
# keeping the knowledge extracted from them.
LOG_HEAVY_SHARE = 0.35

# Above this share of near-duplicate records, retrieval is competing with itself.
DUPLICATE_SHARE = 0.15

# Above this share of signal-less narrative records, the store is documentation
# rather than retrievable memory.
PROSE_HEAVY_SHARE = 0.40

# Jaccard similarity over word shingles at which two records are near-duplicates.
DUPLICATE_THRESHOLD = 0.75

SHINGLE_SIZE = 3

# A heading whose body is shorter than this is a section marker, not a record.
MIN_RECORD_WORDS = 3

# Records shorter than this are excluded from duplicate comparison. Two short
# fragments share shingle sets trivially, which produces 1.00 "duplicates"
# between unrelated files.
MIN_DUPLICATE_WORDS = 20

# Duplicate detection is O(n^2) pairwise. Above this many eligible records the
# scan is capped -- and the number skipped is reported, never dropped silently.
MAX_DUPLICATE_SCAN = 2000

# Records whose newest date is older than this are candidates for review.
DEFAULT_STALE_DAYS = 180

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".mdx"}

# --- classification signals ------------------------------------------------

LOG_PATTERNS = [
    re.compile(r"^\s*(user|assistant|human|ai|system)\s*:", re.IGNORECASE | re.M),
    re.compile(r"^\s*\[?\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}", re.M),
    re.compile(r"\b(session|conversation|transcript|chat log)\b", re.IGNORECASE),
    re.compile(
        r"\b(then (?:i|we|the user)|(?:i|we) (?:ran|tried|asked|noticed|said)"
        r"|the user (?:said|asked|wanted|reported))\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bon \w+ \d{1,2}(?:st|nd|rd|th)?,? \d{4}\b", re.IGNORECASE),
]

SKILL_PATTERNS = [
    re.compile(r"^\s*\d+[.)]\s+\S", re.M),  # numbered procedure
    re.compile(
        r"\b(always|never|must|should|prefer|avoid|do not|don't)\b", re.IGNORECASE
    ),
    re.compile(r"\bto\s+\w+,\s+(?:use|run|call|set|add|check)\b", re.IGNORECASE),
    re.compile(
        r"^\s*(use|run|call|set|add|check|prefer|avoid|install|configure|deploy)\b",
        re.IGNORECASE | re.M,
    ),
    re.compile(r"\b(workflow|procedure|steps?|recipe|playbook|how to)\b", re.IGNORECASE),
]

FACT_PATTERNS = [
    re.compile(
        r"\b\w+\s+(?:is|are|was|were|uses|runs on|lives in|owns|has|equals)\s+\S",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*[-*]\s*\*?\*?[\w ./-]+\*?\*?\s*[:=]\s*\S", re.M),  # key: value
    re.compile(r"\b(version|endpoint|port|repo|owner|deadline|budget)\b", re.IGNORECASE),
]

# Phrases whose truth depends on when they were written.
VOLATILE_PATTERNS = [
    re.compile(
        r"\b(currently|right now|at the moment|as of (?:today|now)|this (?:week|month|quarter|sprint)"
        r"|for now|temporarily|at present|these days|nowadays)\b",
        re.IGNORECASE,
    ),
    re.compile(r"\b(latest|newest|most recent|upcoming|soon|next release)\b", re.IGNORECASE),
]

DATE_PATTERN = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")

WORD_PATTERN = re.compile(r"[a-z0-9]+")


def _fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(3)


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}" if count == 1 else f"{count} {noun}s"


def estimate_tokens(text: str) -> int:
    """Rough token estimate. Deliberately crude -- ~4 chars per token."""
    return max(1, len(text) // 4)


def _mask_code_fences(text: str) -> str:
    """Blank out fenced code bodies so '# comment' inside them is not a heading.

    Same length is preserved, so offsets into the masked copy still index the
    original text correctly.
    """
    masked = list(text)
    fence = re.compile(r"^[ \t]*(`{3,}|~{3,})", re.M)
    positions = [match.start() for match in fence.finditer(text)]
    for index in range(0, len(positions) - 1, 2):
        start, end = positions[index], positions[index + 1]
        for offset in range(start, min(end, len(masked))):
            if masked[offset] != "\n":
                masked[offset] = " "
    return "".join(masked)


def split_records(text: str, source: str) -> list[dict]:
    """Split a document into records on markdown headings, else blank lines."""
    records = []
    heading = re.compile(r"^(#{1,6})\s+(.*)$", re.M)
    # Detect headings on a code-masked copy, but slice bodies from the original.
    matches = list(heading.finditer(_mask_code_fences(text)))

    if len(matches) >= 2:
        for index, match in enumerate(matches):
            start = match.end()
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            body = text[start:end].strip()
            # A heading with a near-empty body is a section marker, not a
            # memory record. Admitting it would inflate every count below.
            if len(body.split()) >= MIN_RECORD_WORDS:
                records.append(
                    {
                        "source": source,
                        "title": match.group(2).strip(),
                        "text": body,
                    }
                )
        return records

    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if len(block) >= 40:
            records.append({"source": source, "title": "", "text": block})
    return records


def _score(patterns: list, text: str) -> int:
    return sum(1 for pattern in patterns if pattern.search(text))


def classify(text: str) -> tuple[str, dict]:
    """Classify a record as LOG, SKILL, FACT, or PROSE with its signal counts.

    A record is only called LOG when it carries a positive event signal.
    Records with no signal at all are PROSE, not LOG -- narrative documentation
    is neither an event log nor a retrievable fact, and calling it LOG would
    fire the log-heavy finding on every prose-shaped store.
    """
    signals = {
        "log": _score(LOG_PATTERNS, text),
        "skill": _score(SKILL_PATTERNS, text),
        "fact": _score(FACT_PATTERNS, text),
    }
    # LOG wins ties: mistaking an event for knowledge is the costly direction.
    if signals["log"] > 0 and signals["log"] >= max(signals["skill"], signals["fact"]):
        return "LOG", signals
    if signals["skill"] > signals["fact"]:
        return "SKILL", signals
    if signals["fact"] > 0:
        return "FACT", signals
    return "PROSE", signals


def shingles(text: str) -> set:
    words = WORD_PATTERN.findall(text.lower())
    if len(words) < SHINGLE_SIZE:
        return {" ".join(words)} if words else set()
    return {
        " ".join(words[i : i + SHINGLE_SIZE])
        for i in range(len(words) - SHINGLE_SIZE + 1)
    }


def jaccard(left: set, right: set) -> float:
    if not left or not right:
        return 0.0
    intersection = len(left & right)
    union = len(left | right)
    return intersection / union if union else 0.0


def find_duplicates(records):
    """Pairwise near-duplicate detection over word shingles.

    Returns (pairs, participants, redundant, scanned, skipped).

    Two distinct counts, because they answer different questions and reporting
    one under the other's name is misleading:

      participants -- records having at least one near-duplicate. BOTH members
                      of a matching pair count. This is what "N records have a
                      near-duplicate" means, and it drives duplicate_share.
      redundant    -- copies that could actually be deleted: participants minus
                      one survivor per connected cluster. For a cluster of k
                      mutually-duplicate records this is k-1, not k.

    Clusters are resolved with union-find rather than by counting pair
    endpoints: a 3-record cluster produces pairs (i,j), (i,k), (j,k), so any
    endpoint-counting shortcut gets the redundant count wrong.
    """
    fingerprints = [shingles(record["text"]) for record in records]
    # Only records long enough to have a meaningful fingerprint are compared;
    # short fragments share shingle sets trivially.
    eligible_ix = [
        i
        for i, record in enumerate(records)
        if len(record["text"].split()) >= MIN_DUPLICATE_WORDS
    ]

    # Comparison is O(n^2). Cap it, and report the cap rather than truncating
    # silently -- a quiet cap reads as "no duplicates found".
    skipped = 0
    if len(eligible_ix) > MAX_DUPLICATE_SCAN:
        skipped = len(eligible_ix) - MAX_DUPLICATE_SCAN
        eligible_ix = eligible_ix[:MAX_DUPLICATE_SCAN]

    parent = {i: i for i in eligible_ix}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    pairs = []
    participants = set()
    for pos, i in enumerate(eligible_ix):
        for j in eligible_ix[pos + 1 :]:
            score = jaccard(fingerprints[i], fingerprints[j])
            if score >= DUPLICATE_THRESHOLD:
                pairs.append(
                    {
                        "similarity": round(score, 3),
                        "a": {
                            "source": records[i]["source"],
                            "title": records[i].get("title", ""),
                        },
                        "b": {
                            "source": records[j]["source"],
                            "title": records[j].get("title", ""),
                        },
                    }
                )
                participants.add(i)
                participants.add(j)
                union(i, j)

    clusters = {find(i) for i in participants}
    redundant = len(participants) - len(clusters)
    return pairs, len(participants), redundant, len(eligible_ix), skipped


def newest_date(text: str):
    newest = None
    for match in DATE_PATTERN.finditer(text):
        try:
            found = datetime(
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3)),
                tzinfo=timezone.utc,
            )
        except ValueError:
            continue
        if newest is None or found > newest:
            newest = found
    return newest


def load_records(args) -> list[dict]:
    records = []
    if args.jsonl:
        try:
            with open(args.jsonl, "r", encoding="utf-8") as handle:
                for number, line in enumerate(handle, start=1):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        payload = json.loads(line)
                    except json.JSONDecodeError as exc:
                        _fail(f"{args.jsonl}:{number} is not valid JSON: {exc}")
                    if not isinstance(payload, dict) or "text" not in payload:
                        _fail(f"{args.jsonl}:{number} must be an object with a 'text' field")
                    records.append(
                        {
                            "source": payload.get("source", f"{args.jsonl}:{number}"),
                            "title": payload.get("title", ""),
                            "text": str(payload["text"]),
                        }
                    )
        except FileNotFoundError:
            _fail(f"jsonl file not found: {args.jsonl}")
        return records

    if not os.path.isdir(args.dir):
        _fail(f"not a directory: {args.dir}")
    for root, dirnames, filenames in os.walk(args.dir):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for filename in sorted(filenames):
            if os.path.splitext(filename)[1].lower() not in TEXT_SUFFIXES:
                continue
            path = os.path.join(root, filename)
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as handle:
                    content = handle.read()
            except OSError:
                continue
            relative = os.path.relpath(path, args.dir)
            records.extend(split_records(content, relative))
    return records


def audit(records: list[dict], stale_days: int) -> dict:
    if not records:
        _fail("no records found -- check the path, or that files are .md/.txt")

    now = datetime.now(timezone.utc)
    counts = {"FACT": 0, "SKILL": 0, "LOG": 0, "PROSE": 0}
    total_tokens = 0
    stale = []
    volatile = []

    for record in records:
        kind, signals = classify(record["text"])
        record["kind"] = kind
        record["signals"] = signals
        tokens = estimate_tokens(record["text"])
        record["tokens"] = tokens
        counts[kind] += 1
        total_tokens += tokens

        found = newest_date(record["text"])
        if found is not None:
            age = (now - found).days
            record["age_days"] = age
            if age > stale_days:
                stale.append(
                    {
                        "source": record["source"],
                        "title": record.get("title", ""),
                        "age_days": age,
                    }
                )
        if any(pattern.search(record["text"]) for pattern in VOLATILE_PATTERNS):
            volatile.append(
                {
                    "source": record["source"],
                    "title": record.get("title", ""),
                    "why": "contains time-relative wording that rots silently",
                }
            )

    (
        duplicate_pairs,
        duplicate_records,
        redundant_copies,
        scanned,
        skipped,
    ) = find_duplicates(records)
    total = len(records)
    knowledge = counts["FACT"] + counts["SKILL"]
    log_share = counts["LOG"] / total
    duplicate_share = duplicate_records / total
    density = knowledge / (total_tokens / 1000.0) if total_tokens else 0.0

    findings = []
    if log_share > LOG_HEAVY_SHARE:
        findings.append(
            {
                "code": "LOG_HEAVY",
                "severity": "high",
                "detail": (
                    f"{counts['LOG']}/{total} records ({log_share:.0%}) read as "
                    "event logs rather than facts or skills."
                ),
                "action": (
                    "Extract the facts and skills out of these transcripts, "
                    "then drop the transcripts. Storing the event is what makes "
                    "retrieval drown."
                ),
            }
        )
    if duplicate_share > DUPLICATE_SHARE:
        findings.append(
            {
                "code": "DUPLICATE_BLOATED",
                "severity": "high",
                "detail": (
                    f"{duplicate_records}/{total} records ({duplicate_share:.0%}) "
                    f"have a near-duplicate at >= {DUPLICATE_THRESHOLD:.0%} "
                    f"similarity; {redundant_copies} of them are redundant "
                    "copies that could be deleted."
                ),
                "action": (
                    "Dedup at write time. Duplicates do not just waste tokens -- "
                    "they let a stale copy outrank a corrected one."
                ),
            }
        )
    if stale:
        findings.append(
            {
                "code": "STALE_RECORDS",
                "severity": "medium",
                "detail": (
                    f"{len(stale)} records carry a date older than {stale_days} "
                    "days."
                ),
                "action": "Re-verify or expire them. A memory that was true is still wrong.",
            }
        )
    prose_share = counts["PROSE"] / total
    if prose_share > PROSE_HEAVY_SHARE:
        findings.append(
            {
                "code": "PROSE_HEAVY",
                "severity": "medium",
                "detail": (
                    f"{counts['PROSE']}/{total} records ({prose_share:.0%}) carry "
                    "no fact, skill, or event signal -- they read as narrative "
                    "documentation."
                ),
                "action": (
                    "Prose is what a human re-reads, not what an agent "
                    "retrieves. Distill each block into the fact or the skill "
                    "it is trying to convey, or move it out of the memory "
                    "store and into docs."
                ),
            }
        )

    if volatile:
        findings.append(
            {
                "code": "VOLATILE_WORDING",
                "severity": "medium",
                "detail": (
                    f"{_plural(len(volatile), 'record')} "
                    f"{'uses' if len(volatile) == 1 else 'use'} time-relative "
                    "wording ('currently', 'latest') that becomes false without "
                    "editing."
                ),
                "action": (
                    "Rewrite with an explicit date or version, so staleness is "
                    "detectable instead of invisible."
                ),
            }
        )

    if any(f["severity"] == "high" for f in findings):
        verdict = "LOG-HEAVY" if log_share > LOG_HEAVY_SHARE else "DUPLICATE-BLOATED"
    elif prose_share > PROSE_HEAVY_SHARE:
        verdict = "PROSE-HEAVY"
    elif findings:
        verdict = "NEEDS-MAINTENANCE"
    else:
        verdict = "KNOWLEDGE-DENSE"

    return {
        "verdict": verdict,
        "totals": {
            "records": total,
            "estimated_tokens": total_tokens,
            "fact": counts["FACT"],
            "skill": counts["SKILL"],
            "log": counts["LOG"],
            "prose": counts["PROSE"],
            "log_share": round(log_share, 4),
            "prose_share": round(prose_share, 4),
        },
        "density": {
            "knowledge_records_per_1k_tokens": round(density, 3),
            "note": (
                "Optimize decision-relevant information per token of context "
                "it costs, not how much you managed to store."
            ),
        },
        "duplicates": {
            "records_with_a_duplicate": duplicate_records,
            "redundant_copies": redundant_copies,
            "share": round(duplicate_share, 4),
            "scanned": scanned,
            "skipped_over_scan_cap": skipped,
            "pairs": duplicate_pairs[:20],
            "pairs_truncated": max(0, len(duplicate_pairs) - 20),
        },
        "stale_records": stale[:20],
        "volatile_records": volatile[:20],
        "findings": findings,
    }


def render(report: dict) -> str:
    lines = []
    totals = report["totals"]
    lines.append("MEMORY DENSITY AUDIT")
    lines.append("=" * 68)
    lines.append(f"VERDICT: {report['verdict']}")
    lines.append("")
    lines.append("What the store actually holds")
    lines.append("-" * 68)
    lines.append(f"  records            {totals['records']}")
    lines.append(f"  estimated tokens   {totals['estimated_tokens']:,}")
    lines.append(f"  FACT               {totals['fact']}")
    lines.append(f"  SKILL              {totals['skill']}")
    lines.append(
        f"  LOG                {totals['log']}  ({totals['log_share']:.0%} of records)"
    )
    lines.append(
        f"  PROSE              {totals['prose']}  "
        f"({totals['prose_share']:.0%} of records, no signal either way)"
    )
    lines.append("")
    lines.append(
        f"Knowledge density: "
        f"{report['density']['knowledge_records_per_1k_tokens']} "
        "fact-or-skill records per 1k tokens"
    )
    lines.append("")

    duplicates = report["duplicates"]
    if duplicates["records_with_a_duplicate"]:
        lines.append(
            f"Near-duplicates: "
            f"{_plural(duplicates['records_with_a_duplicate'], 'record')} "
            f"({duplicates['share']:.0%}), of which "
            f"{duplicates['redundant_copies']} redundant"
        )
        for pair in duplicates["pairs"][:5]:
            left = f"{pair['a']['source']} {pair['a']['title']}".strip()
            right = f"{pair['b']['source']} {pair['b']['title']}".strip()
            lines.append(f"  {pair['similarity']:.2f}  {left}  <->  {right}")
        if duplicates["pairs_truncated"]:
            lines.append(f"  ... {duplicates['pairs_truncated']} more pairs")
        if duplicates["skipped_over_scan_cap"]:
            lines.append(
                f"  NOTE: {duplicates['skipped_over_scan_cap']} eligible records "
                f"were not scanned (cap {MAX_DUPLICATE_SCAN}); duplicate counts "
                "are a lower bound."
            )
        lines.append("")

    if report["findings"]:
        lines.append(f"Findings ({len(report['findings'])})")
        lines.append("-" * 68)
        for finding in report["findings"]:
            lines.append(f"  [{finding['severity'].upper()}] {finding['code']}")
            lines.append(f"    {finding['detail']}")
            lines.append(f"    -> {finding['action']}")
            lines.append("")
    else:
        lines.append("No findings. This store is holding knowledge, not history.")
        lines.append("")

    return "\n".join(lines)


SAMPLE_RECORDS = [
    {
        "source": "sample/onboarding.md",
        "title": "Deploy procedure",
        "text": (
            "To deploy the api service, run `make release` from main. Always "
            "wait for the migration job to report green before promoting. "
            "Never deploy on a Friday after 16:00 UTC.\n"
            "1. Tag the release\n2. Run the migration\n3. Promote"
        ),
    },
    {
        "source": "sample/infra.md",
        "title": "Service ownership",
        "text": (
            "The billing service is owned by the payments team. Its production "
            "endpoint is https://api.internal/billing and it runs on port 8443. "
            "Repo: org/billing-service."
        ),
    },
    {
        "source": "sample/session-2024-01-14.md",
        "title": "Debugging session",
        "text": (
            "2024-01-14 09:12 User: the billing job is failing again\n"
            "Assistant: let me look at the logs\n"
            "Then I ran the migration by hand and it worked. The user said "
            "they would file a ticket about it later."
        ),
    },
    {
        "source": "sample/session-2024-02-02.md",
        "title": "Another debugging session",
        "text": (
            "2024-02-02 14:40 User: billing job failing\n"
            "Assistant: checking the logs now\n"
            "Then I ran the migration by hand and it worked. The user said "
            "they would file a ticket about it later."
        ),
    },
    {
        "source": "sample/stack.md",
        "title": "Current stack",
        "text": (
            "We are currently on Postgres 14 and the latest Redis. This is the "
            "most recent setup as of now."
        ),
    },
    {
        # The same fact written twice in two files -- the most common way a
        # memory store bloats, and the way a stale copy outranks a fixed one.
        "source": "sample/teams.md",
        "title": "Billing ownership",
        "text": (
            "The billing service is owned by the payments team. Its production "
            "endpoint is https://api.internal/billing and it runs on port 8443. "
            "Repo: org/billing-service."
        ),
    },
]


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Classify memory records as FACT / SKILL / LOG, find near-duplicates "
            "and staleness, and score knowledge density."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  memory_density_auditor.py --sample\n"
            "  memory_density_auditor.py --dir ~/.claude/memory\n"
            "  memory_density_auditor.py --jsonl records.jsonl --output json\n"
        ),
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--dir", help="directory of markdown/text memory files")
    source.add_argument("--jsonl", help="JSONL file of records with a 'text' field")
    source.add_argument(
        "--sample",
        action="store_true",
        help="audit the built-in sample store (no input needed)",
    )
    parser.add_argument(
        "--stale-days",
        type=int,
        default=DEFAULT_STALE_DAYS,
        help=f"age in days past which a dated record is stale (default: {DEFAULT_STALE_DAYS})",
    )
    parser.add_argument(
        "--output",
        choices=["text", "json"],
        default="text",
        help="output format (default: text)",
    )
    args = parser.parse_args()

    if args.stale_days < 1:
        _fail("--stale-days must be >= 1")

    records = list(SAMPLE_RECORDS) if args.sample else load_records(args)
    report = audit(records, args.stale_days)

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(render(report))

    return 2 if report["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
