from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_with_ebook_convert(input_path: str) -> str | None:
    """Convert MOBI/AZW/AZW3 via Calibre's ebook-convert.

    The intermediate file goes in a private per-call temp directory rather than
    upstream's fixed `<tempdir>/book_skill_work/ebook-convert-output.txt`. Two
    reasons: a fixed, world-guessable output path that a subprocess writes to is
    the CWE-377 shape, and the module-level constant upstream used ignored the
    caller's --workdir entirely, so the scratch file escaped the directory the
    caller asked for.
    """
    if not shutil.which("ebook-convert"):
        return None
    try:
        input_path = os.path.abspath(input_path)
        with tempfile.TemporaryDirectory(prefix="book_skill_calibre_") as scratch:
            output_path = Path(scratch) / "ebook-convert-output.txt"
            result = subprocess.run(
                ["ebook-convert", input_path, str(output_path)],
                capture_output=True, text=True, timeout=300
            )
            if result.returncode == 0 and output_path.exists():
                text = output_path.read_text(encoding="utf-8", errors="replace")
                if text.strip():
                    return text
    except Exception as e:
        print(f"  [warn] extract_with_ebook_convert failed: {type(e).__name__}: {e}", file=sys.stderr)
    return None
