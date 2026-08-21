"""Deterministic document-extraction library for the book-to-skill converter.

Vendored and adapted from virgiliojr94/book-to-skill (MIT). The CLI entry point
lives one directory up in ``extract_document.py`` — this package is a library
only, so importing it never prints, prompts, or installs anything.

Every format degrades to a standard-library parser; optional third-party
packages (docling, pypdf, pdfminer.six, ebooklib, beautifulsoup4, python-docx,
striprtf) only raise extraction quality. MOBI/AZW/AZW3 are the single exception
— they need Calibre's ``ebook-convert`` on PATH and have no fallback.
"""

from book_to_skill.exceptions import ExtractionError
from book_to_skill.utils import (
    detect_structure,
    estimate_tokens,
    extract_single_file,
    resolve_input_files,
)

__all__ = [
    "ExtractionError",
    "detect_structure",
    "estimate_tokens",
    "extract_single_file",
    "resolve_input_files",
]
