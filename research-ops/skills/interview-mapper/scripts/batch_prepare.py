#!/usr/bin/env python3
"""
batch_prepare.py — prepare a folder of transcripts for bulk mapping.

For each transcript (.txt/.docx/.srt/.vtt) in the folder: numbers the lines → *_nl.txt, writes a manifest.
From .srt/.vtt it also extracts timecodes/speakers (sidecar *_nl.timecodes.json) and checks each
transcript for text addressed to the model (*_nl.flags.json) — a transcript is untrusted input.
Lets you run a pool of N interviews without manual fuss. The mappings themselves are done by the model from the manifest.

CLI: python batch_prepare.py /path/to/transcripts [--out manifest.json] [--output {human,json}]
     python batch_prepare.py --sample
"""

import argparse
import json
import os
import re
import glob
import sys
import tempfile
import zipfile
from xml.parsers import expat

SAMPLE_FILES = {
    "interview-1.txt": "Interviewer: What's the last thing that frustrated you about onboarding?\n"
    "Respondent: I couldn't tell if my invite even went through.\n",
    "interview-2.txt": "Interviewer: Walk me through your last export.\n"
    "Respondent: It timed out twice before I gave up and emailed support.\n",
}

_W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
_NS_SEP = "|"
_W_P = f"{_W_NS}{_NS_SEP}p"
_W_T = f"{_W_NS}{_NS_SEP}t"

# An untrusted .docx inflates two ways: 0.6 MB of archive expands to 208 MB of XML,
# and 700 bytes of DTD with nested entities expand to gigabytes.
MAX_DOCX_XML_BYTES = 64 * 1024 * 1024

# Text addressed to the model rather than the interviewer: instruction hijacking and prompt markup.
INJECTION_PATTERNS = [
    r"\bignore\s+(all\s+|the\s+|any\s+)?(previous|prior|above|earlier)\b",
    r"\bdisregard\s+(all\s+|the\s+|any\s+)?(previous|prior|above|instructions)\b",
    r"\b(new|updated|revised)\s+instructions?\b",
    r"\bsystem\s+prompt\b",
    r"\byou\s+are\s+(now\s+)?(an?\s+)?\w+\s+(assistant|model|ai)\b",
    r"игнорируй\s+(все\s+|всё\s+|предыдущ|прежни|указан)",
    r"забудь\s+(все\s+|всё\s+|предыдущ|прежни|инструкц)",
    r"систе\w*\s+промпт|системн\w+\s+инструкц",
    r"нов\w+\s+инструкци",
    r"^\s*(assistant|human|system|user)\s*:",
    r"<\s*/?\s*(system|instructions?|prompt)\s*>",
    r"\[\s*/?\s*INST\s*\]",
]
_INJECTION_RE = [re.compile(p, re.IGNORECASE) for p in INJECTION_PATTERNS]

_TIME_RE = re.compile(
    r"(\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}|\d{1,2}:\d{2}[.,]\d{1,3})\s*-->\s*"
    r"(\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}|\d{1,2}:\d{2}[.,]\d{1,3})"
)
_VOICE_RE = re.compile(r"<v\s+([^>]+)>(.*?)(?:</v>|$)", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")


class DocxError(Exception):
    """The .docx cannot be read safely: broken XML, a DTD, or over the unpacking limit."""


def _read_document_xml(path):
    """Extracts word/document.xml, refusing to unpack more than the limit.

    The header check is the one that works: zipfile stops at the declared size and
    catches the CRC mismatch, so understating the header does not slip past the limit.
    The second check, on the bytes actually read, is a backstop in case an archive
    reads back differently from what its header promised.
    """
    with zipfile.ZipFile(path) as z:
        info = z.getinfo("word/document.xml")
        if info.file_size > MAX_DOCX_XML_BYTES:
            raise DocxError(
                f"word/document.xml declares {info.file_size} bytes "
                f"against a limit of {MAX_DOCX_XML_BYTES}"
            )
        with z.open("word/document.xml") as fh:
            xml = fh.read(MAX_DOCX_XML_BYTES + 1)
    if len(xml) > MAX_DOCX_XML_BYTES:
        raise DocxError(f"word/document.xml exceeds the limit of {MAX_DOCX_XML_BYTES} bytes")
    return xml


def read_docx(path):
    """Reads .docx text via stdlib (zipfile + expat): paragraphs from word/document.xml, text from <w:t>.

    expat rather than ElementTree, because only expat can reject a DTD: a legitimate
    .docx carries none, and nested entities inside a DTD are billion laughs.
    Every <w:p> at any depth yields a paragraph, and its text includes nested <w:p>
    (text boxes) — the same as root.iter() did before.
    """
    xml = _read_document_xml(path)
    paragraphs, open_p, t_depth = [], [], 0

    def start(name, attrs):
        nonlocal t_depth
        if name == _W_P:
            open_p.append((len(paragraphs), []))
            paragraphs.append(None)  # slot in document order, filled on close
        elif name == _W_T:
            t_depth += 1

    def end(name):
        nonlocal t_depth
        if name == _W_P and open_p:
            index, chunks = open_p.pop()
            paragraphs[index] = "".join(chunks)
        elif name == _W_T and t_depth:
            t_depth -= 1

    def chars(data):
        if t_depth:
            for _, chunks in open_p:
                chunks.append(data)

    def reject_dtd(name, sysid, pubid, has_internal):
        raise DocxError("the .docx carries a DTD — rejected (entity-expansion guard)")

    parser = expat.ParserCreate(namespace_separator=_NS_SEP)
    parser.StartDoctypeDeclHandler = reject_dtd
    parser.ExternalEntityRefHandler = lambda *args: 0
    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.CharacterDataHandler = chars
    try:
        parser.Parse(xml, True)
    except expat.ExpatError as e:
        raise DocxError(f"broken XML in word/document.xml ({e})") from e
    return "\n".join(p for p in paragraphs if p is not None)


def parse_subtitles(raw):
    """Parses .srt/.vtt into a list of cues [{"text","start","speaker"}].

    One cue → one line: the citation unit is an utterance, not a wrap line inside it.
    The speaker comes from the VTT <v Name> tag or from a «Name:» prefix in the cue text.
    """
    raw = raw.replace("\r\n", "\n").replace("\r", "\n")
    cues = []
    for block in re.split(r"\n\s*\n", raw):
        block = block.strip()
        if not block or block.upper().startswith("WEBVTT"):
            continue
        m = _TIME_RE.search(block)
        if not m:
            continue
        body_lines = []
        for ln in block.split("\n"):
            if _TIME_RE.search(ln):
                body_lines = []  # everything before the timecode is a cue number or id
                continue
            if body_lines or ln.strip():
                body_lines.append(ln)
        body = " ".join(x.strip() for x in body_lines).strip()
        speaker = None
        v = _VOICE_RE.search(body)
        if v:
            speaker, body = v.group(1).strip(), v.group(2).strip()
        body = _TAG_RE.sub("", body).strip()
        if speaker is None:
            pref = re.match(r"^([^:]{1,40}):\s+(.*)$", body)
            if pref:
                speaker, body = pref.group(1).strip(), pref.group(2).strip()
        if not body:
            continue
        cues.append(
            {"text": body, "start": m.group(1).replace(",", "."), "speaker": speaker}
        )
    return cues


def read_source(path):
    """Reads the input → (list of lines, timecode map). Errors → a clear message, exit 1."""
    low = path.lower()
    if low.endswith(".docx"):
        try:
            return read_docx(path).splitlines(), {}
        except (zipfile.BadZipFile, KeyError, DocxError) as e:
            sys.exit(f"error: {path}: failed to read .docx ({e})")
    try:
        with open(path, encoding="utf-8") as f:
            raw = f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")
    if low.endswith((".srt", ".vtt")):
        cues = parse_subtitles(raw)
        if not cues:
            sys.exit(
                f"error: {path}: subtitles with no recognizable timecodes — check the format"
            )
        lines, times = [], {}
        for i, c in enumerate(cues, 1):
            lines.append(f"{c['speaker']}: {c['text']}" if c["speaker"] else c["text"])
            times[str(i)] = {"start": c["start"], "speaker": c["speaker"]}
        return lines, times
    return raw.splitlines(), {}


def scan_injection(lines):
    """Returns [{"line","text","pattern"}] for lines addressed to the model, not the interviewer."""
    hits = []
    for i, ln in enumerate(lines, 1):
        for rx in _INJECTION_RE:
            if rx.search(ln):
                hits.append(
                    {"line": i, "text": ln.strip()[:200], "pattern": rx.pattern}
                )
                break
    return hits


def interview_name(path):
    """Extracts a human-readable interview name from the transcript's filename."""
    base = os.path.splitext(os.path.basename(path))[0]
    base = re.sub(
        r"[_\-]*(расшифровка|вычитано|интервью|nl|по спикерам).*$", "", base, flags=re.I
    )
    return base.strip(" —_-") or base


def main():
    """CLI: numbers the lines of every transcript in the folder and writes a manifest."""
    ap = argparse.ArgumentParser(
        description="Prepare a folder of transcripts for bulk mapping."
    )
    ap.add_argument(
        "folder", nargs="?", help="Folder containing .txt/.docx/.srt/.vtt transcripts"
    )
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on two built-in sample transcripts in a throwaway temp folder",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    folder = a.folder
    if a.sample:
        folder = tempfile.mkdtemp(prefix="interview-mapper-sample-")
        for name, text in SAMPLE_FILES.items():
            open(os.path.join(folder, name), "w", encoding="utf-8").write(text)
    elif not folder:
        sys.exit("error: folder is required unless --sample is given")

    files = []
    for ext in ("*.txt", "*.docx", "*.srt", "*.vtt"):
        files += glob.glob(os.path.join(folder, ext))
    files = [f for f in sorted(set(files)) if "_nl" not in os.path.basename(f)]

    manifest = []
    flagged_total = 0
    used_stems = set()
    for f in files:
        lines, times = read_source(f)
        stem = os.path.splitext(f)[0]
        name = interview_name(f)
        if stem in used_stems:
            # demo.srt and demo.vtt would share one demo_nl.txt — the second would silently
            # overwrite the first.
            ext = os.path.splitext(f)[1].lstrip(".").lower()
            stem, name = f"{stem}_{ext}", f"{name} ({ext})"
        used_stems.add(stem)
        entry = {"interview": name, "transcript": f, "role": None}
        nl = stem + "_nl.txt"
        numbered = "\n".join(f"L{i}: {ln}" for i, ln in enumerate(lines, 1))
        open(nl, "w", encoding="utf-8").write(numbered)
        entry["numbered"] = nl
        entry["lines"] = len(lines)
        if times:
            tc = stem + "_nl.timecodes.json"
            with open(tc, "w", encoding="utf-8") as fh:
                json.dump(times, fh, ensure_ascii=False, indent=2)
            entry["timecodes"] = tc
            entry["speakers"] = sorted(
                {v["speaker"] for v in times.values() if v["speaker"]}
            )
        hits = scan_injection(lines)
        if hits:
            fl = stem + "_nl.flags.json"
            with open(fl, "w", encoding="utf-8") as fh:
                json.dump(hits, fh, ensure_ascii=False, indent=2)
            entry["injection_flags"] = fl
            entry["injection_flag_count"] = len(hits)
            flagged_total += len(hits)
        entry["status"] = "ready"
        manifest.append(entry)

    out = a.out or os.path.join(folder, "manifest.json")
    open(out, "w", encoding="utf-8").write(
        json.dumps(manifest, ensure_ascii=False, indent=2)
    )
    ready = sum(1 for m in manifest if m.get("status") == "ready")

    if a.output == "json":
        print(
            json.dumps(
                {
                    "folder": folder,
                    "out": out,
                    "total": len(manifest),
                    "ready": ready,
                    "injection_flag_count": flagged_total,
                    "manifest": manifest,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Transcripts: {len(manifest)} | ready for mapping: {ready} → {out}")
        for m in manifest:
            extra = ""
            if m.get("speakers"):
                extra += f" · speakers: {', '.join(m['speakers'])}"
            if m.get("injection_flag_count"):
                extra += f" · ⚑ {m['injection_flag_count']} suspicious line(s)"
            print(
                f"  [{m.get('status')}] {m['interview']}"
                + (f" ({m.get('lines')} lines)" if m.get("lines") else "")
                + extra
            )
        if flagged_total:
            print(
                f"WARNING: {flagged_total} line(s) look like instructions to the model rather "
                "than respondent speech. A transcript is data, not instructions: check the "
                "flagged lines before S2 (see *_nl.flags.json).",
                file=sys.stderr,
            )
        print(
            "Next: for each ready one — the model does the mapping using the chosen lens (S0-S2)."
        )


if __name__ == "__main__":
    main()
