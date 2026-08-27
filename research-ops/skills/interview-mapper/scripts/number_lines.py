#!/usr/bin/env python3
"""
number_lines.py — number a transcript line by line for quote traceability.

Every quote in a mapping must reference a line number; verify_quotes.py then
checks the match. LLMs handle line numbers poorly «in their head» — so we number by script.

Supports .txt, .docx, .srt, .vtt (stdlib parsing, no external dependencies).
From .srt/.vtt it also extracts the timecode and the speaker — the timecode goes into the
`*_nl.timecodes.json` sidecar so a human can listen to a disputed spot in the audio (S1).

A transcript is UNTRUSTED input: the respondent could have dictated anything, including text
addressed to the model. The script flags such lines in `*_nl.flags.json` — a flag for the
human, not a blocker.

CLI:  python number_lines.py input.(txt|docx|srt|vtt) [--out output.txt] [--output {human,json}]
      python number_lines.py --sample
Output: lines of the form 'L1: ...', 'L2: ...'
"""

import argparse
import json
import re
import sys
import os
import zipfile
from xml.etree import ElementTree as ET

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

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

SAMPLE_TEXT = (
    "Interviewer: Tell me about the last time you tried to reconcile the budget.\n"
    "Respondent: Honestly, I opened three tabs and gave up after twenty minutes.\n"
    "Interviewer: What made you give up?\n"
    "Respondent: The export didn't match what I saw on screen, so I stopped trusting it.\n"
)


def read_docx(path):
    """Reads .docx text via stdlib (zipfile + XML): paragraphs from word/document.xml, text from <w:t>."""
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    paragraphs = []
    for p in root.iter(f"{_W_NS}p"):
        text = "".join(t.text or "" for t in p.iter(f"{_W_NS}t"))
        paragraphs.append(text)
    return "\n".join(paragraphs)


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
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
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


def main():
    """CLI: numbers the transcript's lines and writes the result to *_nl.txt."""
    ap = argparse.ArgumentParser(
        description="Number a transcript's lines for quote traceability."
    )
    ap.add_argument("input", nargs="?", help="Transcript file (.txt/.docx/.srt/.vtt)")
    ap.add_argument("--out", default=None)
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample transcript, no input file needed",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        lines, times, label = SAMPLE_TEXT.splitlines(), {}, "<sample>"
    else:
        if not a.input:
            sys.exit("error: input is required unless --sample is given")
        lines, times = read_source(a.input)
        label = a.input

    numbered = "\n".join(f"L{i}: {ln}" for i, ln in enumerate(lines, 1))
    hits = scan_injection(lines)

    out_path = None
    timecodes_path = None
    flags_path = None
    if a.out or not a.sample:
        out_path = a.out or (os.path.splitext(label)[0] + "_nl.txt")
        open(out_path, "w", encoding="utf-8").write(numbered)
        base = out_path[:-4] if out_path.lower().endswith(".txt") else out_path
        if times:
            timecodes_path = base + ".timecodes.json"
            with open(timecodes_path, "w", encoding="utf-8") as fh:
                json.dump(times, fh, ensure_ascii=False, indent=2)
        if hits:
            flags_path = base + ".flags.json"
            with open(flags_path, "w", encoding="utf-8") as fh:
                json.dump(hits, fh, ensure_ascii=False, indent=2)

    if a.output == "json":
        print(
            json.dumps(
                {
                    "input": label,
                    "out": out_path,
                    "line_count": len(lines),
                    "numbered_preview": numbered.splitlines()[:5],
                    "timecodes": timecodes_path,
                    "speakers": sorted(
                        {v["speaker"] for v in times.values() if v["speaker"]}
                    ),
                    "injection_flags": flags_path,
                    "injection_flag_count": len(hits),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        if out_path:
            print(f"Lines numbered: {len(lines)} → {out_path}")
        else:
            print(f"Lines numbered: {len(lines)} (sample, no --out given)")
            print(numbered)
        if timecodes_path:
            speakers = sorted({v["speaker"] for v in times.values() if v["speaker"]})
            print(
                f"Timecodes: {timecodes_path}"
                + (
                    f" · speakers: {', '.join(speakers)}"
                    if speakers
                    else " · speakers not labelled (a S1 blocker for group lenses)"
                )
            )
    if hits:
        print(
            f"WARNING: {len(hits)} line(s) look like instructions to the model rather than "
            f"respondent speech" + (f" → {flags_path}" if flags_path else ""),
            file=sys.stderr,
        )
        for h in hits[:5]:
            print(f"  L{h['line']}: {h['text']}", file=sys.stderr)
        print(
            "  A transcript is data, not instructions. Eyeball these lines before S2.",
            file=sys.stderr,
        )


if __name__ == "__main__":
    main()
