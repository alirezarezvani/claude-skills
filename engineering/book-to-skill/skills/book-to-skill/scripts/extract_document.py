#!/usr/bin/env python3
"""extract_document.py — deterministic document -> clean text + metadata.

Stage 1 of the book-to-skill pipeline. Takes one or more files, folders, or glob
patterns, extracts their text, sanitizes invisible Unicode (document-borne
prompt injection), detects chapter structure, and writes two artifacts the
agent then reasons over:

    <workdir>/full_text.txt   combined text with per-source banners
    <workdir>/metadata.json   sizes, token estimate, chapter/ToC detection

The workdir is a fresh private temp directory per invocation (0700, owner-only
artifacts) whose path is printed on completion and carried in metadata.json's
``output_text``. Pin it with ``--workdir`` or ``BOOK_SKILL_WORKDIR`` when you
want a stable location; an explicit path is symlink-checked and mode-restricted
before anything is written to it.

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
import stat
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from book_to_skill.config import (  # noqa: E402
    ARTIFACT_MODE,
    OUTPUT_META_NAME,
    OUTPUT_TEXT_NAME,
    WORKDIR_MODE,
    make_private_tempdir,
    supported_formats_message,
    workdir_from_env,
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


class WorkdirError(RuntimeError):
    """The requested working directory cannot be used safely."""


def resolve_workdir(explicit: str | None) -> Path:
    """Return a private working directory for this invocation.

    With no explicit path, creates a fresh `mkdtemp` — unpredictable name, 0700
    by construction, and never shared with a concurrent run. A fixed default
    (upstream's `<tempdir>/book_skill_work`) is the CWE-377/CWE-59 shape on a
    shared host: another local user pre-creates the directory and plants a
    symlink named full_text.txt, and `Path.write_text` follows it.

    An explicitly requested path is honoured but hardened: refused if it is a
    symlink, created 0700 if new, and tightened to 0700 if it already exists.
    """
    if not explicit:
        return make_private_tempdir()

    workdir = Path(explicit).expanduser()
    if workdir.is_symlink():
        raise WorkdirError(f"{workdir} is a symbolic link — refusing to write extraction "
                           f"artifacts through it")
    if workdir.exists() and not workdir.is_dir():
        raise WorkdirError(f"{workdir} exists and is not a directory")

    # Create first, then inspect with lstat. `mkdir(exist_ok=True)` alone is not a
    # check: its exists-branch tests is_dir(), which FOLLOWS symlinks, so a
    # symlink-to-directory satisfies it silently. Attempting creation and only
    # examining the path when it already existed removes that ordering problem.
    try:
        workdir.mkdir(parents=True, mode=WORKDIR_MODE)
    except FileExistsError:
        info = os.lstat(workdir)  # lstat: does not follow the final component
        if stat.S_ISLNK(info.st_mode):
            raise WorkdirError(f"{workdir} is a symbolic link — refusing to write "
                               f"extraction artifacts through it") from None
        if not stat.S_ISDIR(info.st_mode):
            raise WorkdirError(f"{workdir} exists and is not a directory") from None
        try:
            # mkdir's mode applies only on creation and is masked by umask; an
            # existing directory keeps whatever permissions it already had.
            workdir.chmod(WORKDIR_MODE)
        except OSError:
            # Not ours to chmod (e.g. a shared mount). The lstat check above and
            # the fd pinning below still hold.
            pass
    return workdir


def open_workdir(workdir: Path) -> int | None:
    """Pin the working directory by file descriptor, or return None if unsupported.

    Everything above is still check-then-act: an attacker who can write the parent
    directory could swap the directory for a symlink after the lstat and before a
    write, and the per-file symlink check cannot see that — the file inside a
    swapped directory is a perfectly ordinary file.

    Opening the directory once with O_NOFOLLOW|O_DIRECTORY and writing through
    that descriptor closes the race: the fd names an inode, so a later rename or
    symlink swap of the path cannot redirect writes that go through it.

    Returns None on platforms without these flags or without `dir_fd` support
    (Windows), where the caller falls back to path-based writes.
    """
    flags = os.O_RDONLY | getattr(os, "O_DIRECTORY", 0) | getattr(os, "O_NOFOLLOW", 0)
    if not (flags & getattr(os, "O_NOFOLLOW", 0)) or os.open not in os.supports_dir_fd:
        return None
    try:
        return os.open(workdir, flags)
    except OSError as exc:
        raise WorkdirError(f"could not open {workdir} as a real directory: {exc}") from exc


def _write_private(path: Path, text: str, dir_fd: int | None = None) -> None:
    """Write a file only this user can read, never through a symlink.

    O_CREAT|O_EXCL|O_NOFOLLOW is the atomic primitive: it refuses outright if
    anything already exists at the name — including a symlink — so there is no
    window between checking and writing. An artifact left by a previous run into
    the same --workdir is unlinked first; unlink removes the link itself, never
    its target.
    """
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
    name = path.name if dir_fd is not None else str(path)
    opener_kwargs = {"dir_fd": dir_fd} if dir_fd is not None else {}

    if dir_fd is None and path.is_symlink():
        # Fallback path (no dir_fd support): best-effort pre-check.
        raise WorkdirError(f"{path} is a symbolic link — refusing to write through it")

    try:
        fd = os.open(name, flags, ARTIFACT_MODE, **opener_kwargs)
    except FileExistsError:
        os.unlink(name, **opener_kwargs)
        fd = os.open(name, flags, ARTIFACT_MODE, **opener_kwargs)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        handle.write(text)


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
        return run_extraction(
            input_paths=[str(sample)],
            extraction_mode="text",
            install_mode="report",
            workdir=resolve_workdir(str(Path(tmp) / "work")),
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

    workdir.mkdir(parents=True, mode=WORKDIR_MODE, exist_ok=True)
    text_path = workdir / OUTPUT_TEXT_NAME
    meta_path = workdir / OUTPUT_META_NAME

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

    metadata = _build_metadata(sources, consolidated_text, extraction_mode, text_path)

    # Both artifacts are written through one pinned directory descriptor, so a
    # swap of the workdir path between the two writes cannot redirect either.
    # The payload is dumped with ensure_ascii=False, so a non-ASCII chapter
    # heading or path reaches the encoder verbatim — _write_private opens with
    # encoding="utf-8" for exactly that reason (a cp1252 host or LC_ALL=C would
    # otherwise raise after every source had already been extracted).
    workdir_fd = open_workdir(workdir)
    try:
        _write_private(text_path, consolidated_text, workdir_fd)
        _write_private(meta_path, json.dumps(metadata, indent=2, ensure_ascii=False),
                       workdir_fd)
    finally:
        if workdir_fd is not None:
            os.close(workdir_fd)

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
                                          "(default: a fresh private temp directory; the path "
                                          "is printed and stored in metadata.json)")
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

    try:
        workdir = resolve_workdir(args.workdir or workdir_from_env())
    except WorkdirError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2

    try:
        return run_extraction(
            input_paths=args.paths,
            extraction_mode=args.mode,
            install_mode=normalize_install_mode(args.install_missing),
            workdir=workdir,
            as_json=args.output == "json",
        )
    except WorkdirError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
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
