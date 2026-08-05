import os
import tempfile
from pathlib import Path

# Artifact filenames. The *directory* they land in is resolved per invocation by
# extract_document.py — deliberately NOT a module-level constant.
#
# Upstream defaulted to a fixed `<tempdir>/book_skill_work`. On a shared host
# that is CWE-377/CWE-59: any local user can pre-create the directory in a
# world-writable /tmp (the sticky bit stops deletion, not creation) and plant a
# symlink named full_text.txt or metadata.json pointing at a file the victim can
# write — Path.write_text follows symlinks. Two concurrent runs also silently
# clobber each other. See resolve_workdir() in extract_document.py: the default
# is now a per-invocation mkdtemp (0700 by construction, unpredictable name),
# and an explicitly requested directory is symlink-checked and mode-restricted.
OUTPUT_TEXT_NAME = "full_text.txt"
OUTPUT_META_NAME = "metadata.json"

# Permissions for everything the extractor creates. Extracted book text is the
# user's own document content; it does not belong to the host's other users.
WORKDIR_MODE = 0o700
ARTIFACT_MODE = 0o600


def workdir_from_env() -> str | None:
    """The BOOK_SKILL_WORKDIR override, if set. Read at call time, not import."""
    return os.environ.get("BOOK_SKILL_WORKDIR") or None


def make_private_tempdir() -> Path:
    """A fresh, unpredictable, owner-only working directory for one invocation."""
    return Path(tempfile.mkdtemp(prefix="book_skill_work_"))


# Token caps the converter's workflow commits to (SKILL.md Steps 7-9). Shared so
# book_skill_validator.py and token_budget_estimator.py — which both gate on
# these numbers — cannot drift apart.
SKILL_FILE_BUDGETS = {
    "SKILL.md": 4_000,
    "glossary.md": 1_500,
    "patterns.md": 2_000,
    "cheatsheet.md": 1_200,
}
# Not a target: chapters scale by book type and depth (Step 7). This is the
# runaway detector — at this size one chapter costs as much as the whole core.
CHAPTER_TOKEN_CEILING = 3_500

WORDS_PER_TOKEN = 0.75  # approximate (Latin / whitespace-delimited text)
# CJK scripts carry little or no whitespace, so word-splitting under-counts them
# by orders of magnitude. Count CJK codepoints directly against this
# chars-per-token ratio instead (see estimate_tokens in utils.py).
CJK_CHARS_PER_TOKEN = 1.5  # approximate for cl100k-style tokenizers

TEXT_EXTENSIONS = {".txt", ".text", ".md", ".markdown", ".rst", ".adoc", ".asciidoc"}
HTML_EXTENSIONS = {".html", ".htm", ".xhtml"}
CALIBRE_EBOOK_EXTENSIONS = {".mobi", ".azw", ".azw3"}
SUPPORTED_EXTENSIONS = {
    ".pdf", ".epub", ".docx", ".rtf",
    *TEXT_EXTENSIONS,
    *HTML_EXTENSIONS,
    *CALIBRE_EBOOK_EXTENSIONS,
}

PYTHON_DEPENDENCIES = {
    "docling": "docling",
    "pypdf": "pypdf",
    "pdfminer": "pdfminer.six",
    "ebooklib": "ebooklib",
    "bs4": "beautifulsoup4",
    "docx": "python-docx",
    "striprtf": "striprtf",
}


def supported_formats_message() -> str:
    return ", ".join(sorted(SUPPORTED_EXTENSIONS))
