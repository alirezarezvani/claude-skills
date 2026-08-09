#!/usr/bin/env python3
"""token_budget_estimator.py — what the conversion costs, and what it saves.

Two modes, both deterministic and standard-library only.

**Pre-flight** (`--full-text`): before spending a token on generation, model
the cost of answering one targeted question about the source three ways —

  context-dump    the whole source stays resident and is re-billed every turn
  discovery-loop  a live document-reading agent navigates: table of contents,
                  then the chapter it guessed at, then a backtrack for a
                  definition it turns out to need
  book-to-skill   a small resident core plus one compiled chapter, on demand

The discovery-loop figure is a *model with stated assumptions*, not a
measurement of any particular agent — but it is built from the real token sizes
of this source's own ToC and chapters, so it is an estimate you can argue with
rather than a number pulled from a marketing page.

**Post-flight** (`--skill-dir`): audit a generated skill file-by-file against
the token budgets the converter commits to, so overflow is caught before
compaction silently truncates the master file's indexes.

Given both, it does both and cross-references them.

Token counts use the same deterministic heuristic as the extractor (words/0.75,
with a separate CJK codepoint ratio), so every number in the pipeline agrees.
The estimate is an estimate: it is stable and comparable, not a BPE count.

Exit codes:
    0  report produced
    1  the source has no detectable chapters (nothing to model)
    2  bad invocation, or a path that does not exist / is not a compiled skill

Adapted from virgiliojr94/book-to-skill's discovery_tax.py (MIT), rewritten to
drop the optional tiktoken path and to add the post-flight budget audit.
See ../../../LICENSE.

Usage:
    python3 token_budget_estimator.py --full-text "$WORKDIR/full_text.txt"
    python3 token_budget_estimator.py --skill-dir ~/.claude/skills/meadows-systems
    python3 token_budget_estimator.py --full-text FT.txt --skill-dir SKILL_DIR --target-chapter 5
    python3 token_budget_estimator.py --sample
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_to_skill.config import (  # noqa: E402
    CHAPTER_TOKEN_CEILING,
    SKILL_FILE_BUDGETS,
)
from book_to_skill.utils import _chapter_number as chapter_number  # noqa: E402
from book_to_skill.utils import estimate_tokens  # noqa: E402

# Shared with book_skill_validator.py via config — see the note there.
BUDGETS = SKILL_FILE_BUDGETS
CHAPTER_CEILING = CHAPTER_TOKEN_CEILING
DEFAULT_CORE_TOKENS = 4_000
DEFAULT_COMPILED_CHAPTER = 1_000

_TOC_RE = re.compile(
    r"^\s*(?:table of contents|contents|sum[áa]rio|[íi]ndice|目录|目錄|目次|"
    r"table des matières|inhaltsverzeichnis|inhoudsopgave)\s*$",
    re.IGNORECASE | re.MULTILINE,
)


def split_chapters(text: str) -> list[tuple[int | None, str, str]]:
    """Return [(number, heading, body)], one segment per heading occurrence.

    Text before the first heading is the leading front-matter segment
    (number=None). A chapter number can appear twice — once in the table of
    contents and once as the real heading — so callers pick the largest body.
    """
    segments: list[tuple[int | None, str, list[str]]] = [(None, "__front__", [])]
    for line in text.splitlines():
        number = chapter_number(line)
        if number is not None:
            segments.append((number, line.strip(), []))
        segments[-1][2].append(line)
    return [(n, h, "\n".join(b)) for n, h, b in segments]


def best_chapter(chapters, number: int) -> tuple[str, int] | None:
    """(heading, body_tokens) for a chapter number, taking the largest body —
    the real chapter, not its one-line table-of-contents entry."""
    candidates = [(h, estimate_tokens(b)) for n, h, b in chapters if n == number]
    return max(candidates, key=lambda item: item[1]) if candidates else None


def extract_toc(front_matter: str) -> str:
    match = _TOC_RE.search(front_matter)
    # No explicit ToC heading: assume the agent skims the whole front matter.
    return front_matter[match.start():] if match else front_matter


class InputError(RuntimeError):
    """A path given on the command line cannot be used."""


def audit_skill_dir(skill_dir: Path) -> dict:
    """File-by-file token audit of a generated skill against the budgets.

    Refuses a directory that does not exist or has no SKILL.md. Without that
    check a typo'd --skill-dir produced a full, plausible-looking audit — every
    row "missing", every cap satisfied, exit 0 — which reads as a pass. A gate
    that reports success for a path that isn't there is worse than no gate.
    """
    if not skill_dir.exists():
        raise InputError(f"no such skill directory: {skill_dir}")
    if not skill_dir.is_dir():
        raise InputError(f"not a directory: {skill_dir}")
    if not (skill_dir / "SKILL.md").is_file():
        raise InputError(
            f"{skill_dir} has no SKILL.md — this is not a compiled skill. "
            f"Point --skill-dir at the generated skill folder."
        )

    rows, over = [], []
    for filename, cap in BUDGETS.items():
        path = skill_dir / filename
        if not path.is_file():
            rows.append({"file": filename, "tokens": None, "cap": cap, "status": "missing"})
            continue
        tokens = estimate_tokens(path.read_text(encoding="utf-8-sig"))
        status = "over" if tokens > cap else "ok"
        rows.append({"file": filename, "tokens": tokens, "cap": cap, "status": status})
        if status == "over":
            over.append(filename)

    chapter_dir = skill_dir / "chapters"
    chapters = sorted(chapter_dir.glob("*.md")) if chapter_dir.is_dir() else []
    chapter_tokens = [estimate_tokens(p.read_text(encoding="utf-8-sig")) for p in chapters]
    for path, tokens in zip(chapters, chapter_tokens):
        status = "over" if tokens > CHAPTER_CEILING else "ok"
        rows.append({"file": f"chapters/{path.name}", "tokens": tokens,
                     "cap": CHAPTER_CEILING, "status": status})
        if status == "over":
            over.append(f"chapters/{path.name}")

    resident = next((r["tokens"] for r in rows if r["file"] == "SKILL.md" and r["tokens"]), 0)
    return {
        "rows": rows,
        "chapters": len(chapters),
        "resident_tokens": resident,
        "chapter_tokens_avg": sum(chapter_tokens) // len(chapter_tokens) if chapter_tokens else 0,
        "chapter_tokens_total": sum(chapter_tokens),
        "over_budget": over,
    }


def model_discovery(full_text: str, target: int, core_tokens: int,
                    compiled_chapter: int) -> dict | None:
    segments = split_chapters(full_text)
    front, chapters = segments[0][2], segments[1:]
    if not chapters:
        return None

    distinct = sorted({n for n, _, _ in chapters if n is not None})
    number = target
    chosen = best_chapter(chapters, number)
    if chosen is None and distinct:
        number = distinct[min(target - 1, len(distinct) - 1)]
        chosen = best_chapter(chapters, number)
    if chosen is None:
        return None

    heading, target_raw = chosen
    prior = best_chapter(chapters, number - 1)
    toc_tokens = estimate_tokens(extract_toc(front))
    skill_cost = core_tokens + compiled_chapter

    return {
        "chapters_detected": len(distinct),
        "target_chapter": number,
        "target_heading": heading[:80],
        "source_total_tokens": estimate_tokens(full_text),
        "toc_tokens": toc_tokens,
        "target_chapter_raw_tokens": target_raw,
        "prior_chapter_raw_tokens": prior[1] if prior else 0,
        "cost_context_dump": estimate_tokens(full_text),
        "cost_discovery_best": toc_tokens + target_raw,
        "cost_discovery_loop": toc_tokens + target_raw + (prior[1] if prior else 0),
        "cost_book_to_skill": skill_cost,
        "core_tokens": core_tokens,
        "compiled_chapter_tokens": compiled_chapter,
        # Conversion is not free: it costs a full generation pass up front. It
        # pays back only when the source is large enough that reading it (or
        # navigating it) repeatedly dwarfs the resident core. Below roughly 3x
        # the compiled cost, just hand the agent the document.
        "worth_converting": estimate_tokens(full_text) >= 3 * skill_cost,
    }


SAMPLE_SOURCE = """Table of Contents

Chapter 1: Framing
Chapter 2: Leverage Points
Chapter 3: Failure Modes

Chapter 1: Framing

""" + ("A system is a set of elements interconnected in a way that produces a "
       "characteristic pattern of behaviour over time. " * 900) + """

Chapter 2: Leverage Points

""" + ("Places within a complex system where a small shift in one thing produces "
       "big changes in everything. The list runs from parameters, the weakest, to "
       "paradigms, the strongest. " * 1200) + """

Chapter 3: Failure Modes

""" + ("Policy resistance, the tragedy of the commons, drift to low performance, "
       "escalation, and seeking the wrong goal. " * 900)


def run_sample(as_json: bool) -> int:
    with tempfile.TemporaryDirectory() as tmp:
        source = Path(tmp) / "full_text.txt"
        source.write_text(SAMPLE_SOURCE, encoding="utf-8")
        return run(full_text_path=source, skill_dir=None, target=2,
                   core_tokens=DEFAULT_CORE_TOKENS, as_json=as_json)


def _ratio(a: int, b: int) -> str:
    return f"{a / b:.1f}x" if b else "n/a"


def _print_discovery(model: dict) -> None:
    print("Discovery Loop Tax — modelled on this source\n")
    print(f"  chapters detected : {model['chapters_detected']}")
    print(f"  target            : chapter {model['target_chapter']} ({model['target_heading']})")
    print(f"  source total      : {model['source_total_tokens']:,} tokens\n")
    print("  Cost to answer ONE targeted question (tokens entering context):\n")
    print(f"    context-dump      : {model['cost_context_dump']:>9,}   resident, re-billed EVERY turn")
    print(f"    discovery (best)  : {model['cost_discovery_best']:>9,}   ToC ({model['toc_tokens']:,}) "
          f"+ raw target chapter ({model['target_chapter_raw_tokens']:,})")
    print(f"    discovery (loop)  : {model['cost_discovery_loop']:>9,}   + one backtrack chapter "
          f"({model['prior_chapter_raw_tokens']:,})")
    print(f"    book-to-skill     : {model['cost_book_to_skill']:>9,}   core ({model['core_tokens']:,}) "
          f"+ compiled chapter ({model['compiled_chapter_tokens']:,})\n")
    print("  book-to-skill advantage:")
    print(f"    vs context-dump   : {_ratio(model['cost_context_dump'], model['cost_book_to_skill'])} fewer tokens")
    print(f"    vs discovery best : {_ratio(model['cost_discovery_best'], model['cost_book_to_skill'])} fewer tokens")
    print(f"    vs discovery loop : {_ratio(model['cost_discovery_loop'], model['cost_book_to_skill'])} fewer tokens")
    print("\n  Read this honestly: the discovery figures are a model built from this source's real")
    print("  ToC and chapter sizes, and they are a one-time read. context-dump is the recurring one.")
    if model["worth_converting"]:
        print(f"\n  VERDICT: worth converting — the source is {_ratio(model['cost_context_dump'], model['cost_book_to_skill'])} "
              f"the size of the compiled skill.")
    else:
        print(f"\n  VERDICT: probably not worth converting — at {model['source_total_tokens']:,} tokens this source")
        print(f"  is smaller than ~3x the compiled skill ({model['cost_book_to_skill']:,}). Hand the agent the document.")


def _print_audit(audit: dict) -> None:
    print("\nGenerated-skill budget audit\n")
    print(f"  {'file':<34} {'tokens':>8} {'cap':>8}  status")
    for row in audit["rows"]:
        tokens = f"{row['tokens']:,}" if row["tokens"] is not None else "—"
        print(f"  {row['file']:<34} {tokens:>8} {row['cap']:>8,}  {row['status']}")
    print(f"\n  resident core    : {audit['resident_tokens']:,} tokens (loaded every session)")
    print(f"  chapters         : {audit['chapters']} files, "
          f"~{audit['chapter_tokens_avg']:,} tokens each, "
          f"{audit['chapter_tokens_total']:,} total (on demand)")
    if audit["over_budget"]:
        print(f"\n  OVER BUDGET: {', '.join(audit['over_budget'])}")
        print("  SKILL.md overflow is the one that bites: compaction truncates from the end, so the")
        print("  Chapter and Topic indexes — the navigation this skill exists for — go first.")


def run(*, full_text_path: Path | None, skill_dir: Path | None, target: int,
        core_tokens: int, as_json: bool) -> int:
    audit = audit_skill_dir(skill_dir) if skill_dir else None
    model = None

    if full_text_path:
        if not full_text_path.is_file():
            raise InputError(
                f"no such extracted-text file: {full_text_path}\n"
                "Pass the full_text.txt path that extract_document.py printed "
                "(it is also metadata.json's `output_text`)."
            )
        text = full_text_path.read_text(encoding="utf-8", errors="ignore")
        # A measured skill beats the design cap: use its real resident size and
        # its real average chapter size when we have them.
        core = audit["resident_tokens"] if audit and audit["resident_tokens"] else core_tokens
        chapter = (audit["chapter_tokens_avg"] if audit and audit["chapter_tokens_avg"]
                   else DEFAULT_COMPILED_CHAPTER)
        model = model_discovery(text, target, core, chapter)
        if model is None:
            print("No chapters detected — nothing to model. The source may be a technical PDF "
                  "whose headings were flattened by text extraction; try --mode technical.",
                  file=sys.stderr)
            return 1

    if as_json:
        print(json.dumps({"discovery_model": model, "budget_audit": audit},
                         indent=2, ensure_ascii=False))
        return 0

    print("Token counts use the extractor's words/0.75 heuristic (with a CJK codepoint ratio) — "
          "stable and comparable, not a BPE count.\n")
    if model:
        _print_discovery(model)
    if audit:
        _print_audit(audit)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="token_budget_estimator.py",
        description="Model conversion savings pre-flight and audit skill budgets post-flight.",
    )
    parser.add_argument("--full-text", help="extractor output full_text.txt (pre-flight model)")
    parser.add_argument("--skill-dir", help="generated skill folder (post-flight budget audit)")
    parser.add_argument("--target-chapter", type=int, default=5,
                        help="chapter number the modelled question is about (default: 5)")
    parser.add_argument("--core-tokens", type=int, default=DEFAULT_CORE_TOKENS,
                        help="assumed resident SKILL.md size when --skill-dir is not given")
    parser.add_argument("--output", choices=("text", "json"), default="text")
    parser.add_argument("--sample", action="store_true",
                        help="run the model on a built-in three-chapter sample source")
    args = parser.parse_args(argv)

    if args.sample:
        return run_sample(args.output == "json")
    if not args.full_text and not args.skill_dir:
        parser.print_usage(sys.stderr)
        print("ERROR: give --full-text, --skill-dir, or both (or use --sample).", file=sys.stderr)
        return 2

    try:
        return run(
            full_text_path=Path(args.full_text) if args.full_text else None,
            skill_dir=Path(args.skill_dir) if args.skill_dir else None,
            target=args.target_chapter,
            core_tokens=args.core_tokens,
            as_json=args.output == "json",
        )
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        # `tool | head` closes the pipe while this is still writing. Exit quietly
        # instead of dumping a traceback: redirect stdout to devnull first so the
        # interpreter's shutdown flush cannot re-raise. 141 = 128 + SIGPIPE.
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        sys.exit(141)
