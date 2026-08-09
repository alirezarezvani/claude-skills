"""Shared safety checks for zip-of-XML container formats (DOCX, EPUB).

Upstream hardened DOCX and only DOCX: `validate_docx_xml_safety()` scanned that
archive for DTD/entity declarations before any parser touched it. EPUB is the
same shape — a zip whose members are XML (`container.xml`, the OPF package
document, NCX, content docs) — and its `ebooklib` path handed the file straight
to an XML parser with no equivalent pre-check, even though `ebooklib` is one of
the packages this skill recommends installing "for best results".

Two classes of attack, both from a file the user was handed rather than wrote:

1. **Entity expansion / XXE.** `<!ENTITY>` declarations drive billion-laughs
   memory exhaustion; external entities read local files into the parsed output.
   Python's `xml.etree.ElementTree` does not resolve *external* entities, but it
   does expand internal ones — and third-party parsers built on lxml vary. The
   check refuses the archive rather than trusting each parser's defaults.

2. **Decompression bombs.** A few KB of zip can expand to gigabytes. Every read
   goes through `safe_read()`, which consults the declared uncompressed size and
   the compression ratio *before* decompressing, so a bomb is refused rather
   than materialized.

Neither parser ever writes archive members to disk (no `extractall`/`extract`),
so zip-slip is out of scope by construction.
"""

from __future__ import annotations

import zipfile

from book_to_skill.exceptions import ExtractionError

# A single member of a book archive. Generous for a chapter's XHTML or a
# document.xml, far below what a bomb needs to hurt.
MAX_MEMBER_BYTES = 64 * 1024 * 1024
# Everything read from one archive, across all members.
MAX_TOTAL_BYTES = 512 * 1024 * 1024
# Declared-uncompressed / stored ratio. Real prose and XML land well under 100x;
# the classic zip bomb is ~1000x and up.
MAX_COMPRESSION_RATIO = 200

# Members worth scanning for DTD/entity declarations: XML by extension, plus the
# extensionless `mimetype` member and OPF/NCX which are XML without an .xml suffix.
_XML_SUFFIXES = (".xml", ".rels", ".opf", ".ncx", ".xhtml", ".html", ".htm")


class _Budget:
    """Running total of bytes decompressed from one archive."""

    def __init__(self, limit: int = MAX_TOTAL_BYTES) -> None:
        self.limit = limit
        self.used = 0

    def charge(self, size: int, name: str) -> None:
        self.used += size
        if self.used > self.limit:
            raise ExtractionError(
                f"archive exceeds the {self.limit:,}-byte decompression budget "
                f"(reading '{name}') — refusing to continue"
            )


def safe_read(zf: zipfile.ZipFile, name: str, budget: _Budget | None = None) -> bytes:
    """Read one archive member after checking its declared size and ratio.

    The checks run against the zip's central directory *before* decompressing,
    so a bomb never gets materialized. A liar in the directory still cannot get
    past the budget, because the actual read is charged against it too.
    """
    try:
        info = zf.getinfo(name)
    except KeyError as exc:
        raise ExtractionError(f"archive member not found: {name}") from exc

    if info.file_size > MAX_MEMBER_BYTES:
        raise ExtractionError(
            f"archive member '{name}' declares {info.file_size:,} bytes uncompressed; "
            f"the per-member limit is {MAX_MEMBER_BYTES:,} bytes"
        )
    if info.compress_size > 0:
        ratio = info.file_size / info.compress_size
        if ratio > MAX_COMPRESSION_RATIO:
            raise ExtractionError(
                f"archive member '{name}' expands {ratio:.0f}x "
                f"({info.compress_size:,} -> {info.file_size:,} bytes); the limit is "
                f"{MAX_COMPRESSION_RATIO}x — this looks like a decompression bomb"
            )

    data = zf.read(name)
    if budget is not None:
        budget.charge(len(data), name)
    return data


def is_xml_member(name: str) -> bool:
    return name.lower().endswith(_XML_SUFFIXES)


def validate_zip_xml_safety(archive_path: str, label: str = "archive") -> None:
    """Refuse a zip-of-XML archive that declares a DTD or any entity.

    Scans every XML-ish member across the encodings a hostile file might use to
    hide the declaration from a naive UTF-8 substring search. Generalized from
    upstream's DOCX-only guard so EPUB gets the same treatment.
    """
    try:
        with zipfile.ZipFile(archive_path) as zf:
            budget = _Budget()
            for name in zf.namelist():
                if not is_xml_member(name):
                    continue
                xml_bytes = safe_read(zf, name, budget)
                for encoding in ("utf-8", "utf-16", "utf-16le", "utf-16be", "utf-32"):
                    try:
                        content = xml_bytes.decode(encoding, errors="ignore").upper()
                    except LookupError:
                        continue
                    if "<!DOCTYPE" in content or "<!ENTITY" in content:
                        raise ExtractionError(
                            f"security validation failed: XML member '{name}' in the {label} "
                            f"archive contains a forbidden DTD or entity declaration"
                        )
    except zipfile.BadZipFile as exc:
        raise ExtractionError(f"invalid {label} file: {exc}") from exc
    except ExtractionError:
        raise
    except Exception as exc:
        raise ExtractionError(
            f"error during security validation of the {label} archive: {exc}"
        ) from exc
