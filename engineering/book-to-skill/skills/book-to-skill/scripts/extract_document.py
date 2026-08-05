#!/usr/bin/env python3
"""extract_document.py — deterministic document -> clean text + metadata.

Stage 1 of the book-to-skill pipeline. Takes one or more files, folders, or glob
patterns, extracts their text, sanitizes invisible Unicode (document-borne
prompt injection), detects chapter structure, and writes two artifacts the
agent then reasons over:

    <workdir>/full_text.txt   combined text with per-source banners
    <workdir>/metadata.json   sizes, token estimate, chapter/ToC detection

The workdir defaults to ``<tempdir>/book_skill_work`` and can be pointed
somewhere else with ``--workdir`` or ``BOOK_SKILL_WORKDIR``.

Runs on the standard library alone. Optional packages (docling, pypdf,
pdfminer.six, ebooklib, beautifulsoup4, python-docx, striprtf) raise extraction
quality where installed; ``--check`` reports what is present and prints the
exact install command for what is not. MOBI/AZW/AZW3 are the one format with no
stdlib fallback — they need Calibre's ``ebook-convert`` on PATH.

Nothing is installed unless you explicitly pass ``--install-missing yes``.

Exit codes:
    0  extraction succeeded (or --check / --sample completed)
    1  no usable input, or every source failed extraction
    2  bad invocation

Adapted from virgiliojr94/book-to-skill (MIT). See ../../../LICENSE.

Usage:
    python3 extract_document.py BOOK.pdf --mode technical
    python3 extract_document.py ./docs/ '*.epub' --output json
    python3 extract_document.py --check
    python3 extract_document.py --sample
"""

from __future__ import annotations

import argparse
import contextlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_to_skill.config import (  # noqa: E402
    OUTPUT_DIR,
    OUTPUT_META,
    OUTPUT_TEXT,
    supported_formats_message,
)
from book_to_skill.dependencies import (  # noqa: E402
    INSTALL_MODES,
    normalize_install_mode,
    run_dependency_check,
)
from book_to_skill.exceptions import ExtractionError  # noqa: E402
from book_to_skill.utils import (  # noqa: E402
    detect_structure,
    estimate_tokens,
    extract_single_file,
    resolve_input_files,
)

SAMPLE_DOCUMENT = """Table of Contents

Chapter 1: The Discovery Loop Tax
Chapter 2: Extract Structure, Not Summaries

Chapter 1: The Discovery Loop Tax

An agent that reads a PDF to answer one question pays for the table of
contents, the chapter it guessed at, and the chapter it backtracks to for a
missing definition. Structuring the source once makes every later query cost
what the answer costs, not what the book costs.

Chapter 2: Extract Structure, Not Summaries

A skill is not a book report. Capture named frameworks with their exact
formulations, the decision rules the author commits to, and the anti-patterns
they warn against. "The 5 Whys" is not interchangeable with "ask why a few
times" — the name is the interface.
"""


def _resolve_workdir(explicit: str | None) -> Path:
    return Path(explicit).expanduser() if explicit else OUTPUT_DIR


def _extract_all(input_files, extraction_mode: str, install_mode: str):
    """Extract every resolved file. Returns (sources, errors)."""
    sources, errors = [], []
    for file_path in input_files:
        try:
            sources.append(extract_single_file(file_path, extraction_mode, install_mode))
        except ExtractionError as exc:
            print(f"WARNING: skipping {file_path.name}: {exc}", file=sys.stderr)
            errors.append((file_path, str(exc)))
    return sources, errors


def _build_metadata(sources: list[dict], consolidated_text: str, extraction_mode: str,
                    text_path: Path) -> dict:
    total_tokens = estimate_tokens(consolidated_text)
    # Structure is detected on source text only: the per-source banners in
    # full_text.txt are rows of "=", which would otherwise register as phantom
    # setext headings and make the result depend on how long the paths are.
    structure = detect_structure("\n\n".join(src["text"] for src in sources))
    multi = len(sources) > 1
    return {
        "source_file": "Consolidated from multiple sources" if multi else sources[0]["source_file"],
        "filename": "multi-source" if multi else sources[0]["filename"],
        "format": "mixed" if multi else sources[0]["format"],
        "extraction_method": "multi-method" if multi else sources[0]["extraction_method"],
        "extraction_mode": extraction_mode,
        "file_size_mb": round(sum(src["file_size_mb"] for src in sources), 2),
        "pages": sum(src["pages"] for src in sources),
        "chars": len(consolidated_text),
        "words": len(consolidated_text.split()),
        "estimated_tokens": total_tokens,
        "estimated_tokens_human": f"~{total_tokens // 1000}K",
        "output_text": str(text_path),
        "total_sources": len(sources),
        "sources": [
            {key: src[key] for key in (
                "source_file", "filename", "format", "extraction_method",
                "file_size_mb", "pages", "pages_label", "chars", "words",
                "estimated_tokens", "chapters_detected", "has_toc",
            )}
            for src in sources
        ],
        **structure,
    }


def _print_report(metadata: dict, errors: list, text_path: Path, meta_path: Path) -> None:
    print("\nExtraction complete:")
    print(f"   Sources : {metadata['total_sources']} processed")
    print(f"   Size    : {metadata['file_size_mb']:.2f} MB")
    print(f"   Pages   : {metadata['pages']}")
    print(f"   Words   : {metadata['words']:,}")
    print(f"   Tokens  : {metadata['estimated_tokens_human']}")
    print(f"   Chapters: {metadata['chapters_detected']} detected overall")
    print(f"   ToC     : {'yes' if metadata['has_toc'] else 'not detected'}")
    if not metadata["has_toc"]:
        print("   WARN    : no table of contents detected — chapter mapping falls back to a "
              "heading scan, which may miss or duplicate sections.")
    print(f"\n   Text -> {text_path}")
    print(f"   Meta -> {meta_path}")
    if errors:
        print(f"\n   WARNING: {len(errors)} source(s) skipped:")
        for path, err in errors:
            print(f"     - {path.name}: {err}")


def run_sample(as_json: bool) -> int:
    """Extract a built-in two-chapter document so the pipeline can be smoke-tested
    without supplying a real book."""
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        sample = Path(tmp) / "sample-book.md"
        sample.write_text(SAMPLE_DOCUMENT, encoding="utf-8")
        workdir = Path(tmp) / "work"
        return run_extraction(
            input_paths=[str(sample)],
            extraction_mode="text",
            install_mode="report",
            workdir=workdir,
            as_json=as_json,
            keep=False,
        )


def run_extraction(*, input_paths: list[str], extraction_mode: str, install_mode: str,
                   workdir: Path, as_json: bool, keep: bool = True) -> int:
    input_files = resolve_input_files(input_paths)
    if not input_files:
        print(f"ERROR: no supported files found matching: {', '.join(input_paths)}", file=sys.stderr)
        print(f"Supported formats: {supported_formats_message()}", file=sys.stderr)
        return 1

    workdir.mkdir(parents=True, exist_ok=True)
    text_path = workdir / OUTPUT_TEXT.name
    meta_path = workdir / OUTPUT_META.name

    # The vendored extractors narrate progress on stdout. When the caller asked
    # for JSON, that narration would corrupt the payload — send it to stderr so
    # stdout carries the document metadata and nothing else.
    sink = contextlib.redirect_stdout(sys.stderr) if as_json else contextlib.nullcontext()
    with sink:
        sources, errors = _extract_all(input_files, extraction_mode, install_mode)

    if not sources:
        print(f"ERROR: all {len(errors)} source(s) failed extraction:", file=sys.stderr)
        for path, err in errors:
            print(f"  - {path.name}: {err}", file=sys.stderr)
        return 1

    consolidated_text = "".join(
        f"\n\n{'=' * 80}\nSOURCE: {src['filename']} (Path: {src['source_file']})\n{'=' * 80}\n\n"
        + src["text"]
        for src in sources
    ).strip()

    text_path.write_text(consolidated_text, encoding="utf-8")
    metadata = _build_metadata(sources, consolidated_text, extraction_mode, text_path)
    # encoding="utf-8" is load-bearing, not cosmetic: the payload is dumped with
    # ensure_ascii=False, so a non-ASCII chapter heading or path reaches the
    # encoder verbatim and would raise on a cp1252 host or under LC_ALL=C.
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")

    if as_json:
        print(json.dumps(metadata, indent=2, ensure_ascii=False))
    else:
        _print_report(metadata, errors, text_path, meta_path)
        if not keep:
            print("\n(sample run — the temporary workdir was discarded)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="extract_document.py",
        description="Extract clean text + metadata from books and documents.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Supported formats: {supported_formats_message()}",
    )
    parser.add_argument("paths", nargs="*",
                        help="file(s), folder(s), or glob pattern(s) to extract")
    parser.add_argument("--mode", choices=("text", "technical"), default="text",
                        help="technical preserves tables/code via docling when installed; "
                             "text uses the fastest suitable extractor (default: text)")
    parser.add_argument("--workdir", help="where to write full_text.txt + metadata.json "
                                          "(default: $BOOK_SKILL_WORKDIR or a temp folder)")
    parser.add_argument("--install-missing", choices=INSTALL_MODES, default=None,
                        help="report prints the pip command and uses the stdlib fallback "
                             "(default); ask prompts on a TTY; yes installs without asking")
    parser.add_argument("--output", choices=("text", "json"), default="text",
                        help="text prints a human report; json prints the metadata document")
    parser.add_argument("--check", action="store_true",
                        help="report which extractors are installed, then exit")
    parser.add_argument("--sample", action="store_true",
                        help="run the pipeline on a built-in sample document, then exit")
    args = parser.parse_args(argv)

    for stream in (sys.stdout, sys.stderr):
        with contextlib.suppress(AttributeError, ValueError):
            stream.reconfigure(encoding="utf-8")

    if args.check:
        return run_dependency_check()
    if args.sample:
        return run_sample(as_json=args.output == "json")
    if not args.paths:
        parser.print_usage(sys.stderr)
        print("ERROR: no input document, folder, or glob pattern given "
              "(use --sample to try the pipeline).", file=sys.stderr)
        return 2

    return run_extraction(
        input_paths=args.paths,
        extraction_mode=args.mode,
        install_mode=normalize_install_mode(args.install_missing),
        workdir=_resolve_workdir(args.workdir or os.environ.get("BOOK_SKILL_WORKDIR")),
        as_json=args.output == "json",
    )


if __name__ == "__main__":
    sys.exit(main())
