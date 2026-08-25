#!/usr/bin/env python3
"""
batch_prepare.py — prepare a folder of transcripts for bulk mapping.

For each transcript (.txt/.docx) in the folder: numbers the lines → *_nl.txt, writes a manifest.
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
from xml.etree import ElementTree as ET

SAMPLE_FILES = {
    "interview-1.txt": "Interviewer: What's the last thing that frustrated you about onboarding?\n"
    "Respondent: I couldn't tell if my invite even went through.\n",
    "interview-2.txt": "Interviewer: Walk me through your last export.\n"
    "Respondent: It timed out twice before I gave up and emailed support.\n",
}

_W_NS = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


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


def read_text(path):
    """Reads .txt or .docx (stdlib parsing); OSError → a clear error, exit 1."""
    if path.lower().endswith(".docx"):
        try:
            return read_docx(path)
        except (zipfile.BadZipFile, KeyError, ET.ParseError) as e:
            sys.exit(f"error: {path}: failed to read .docx ({e})")
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")


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
        "folder", nargs="?", help="Folder containing .txt/.docx transcripts"
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
    for ext in ("*.txt", "*.docx"):
        files += glob.glob(os.path.join(folder, ext))
    files = [f for f in sorted(set(files)) if "_nl" not in os.path.basename(f)]

    manifest = []
    for f in files:
        text = read_text(f)
        entry = {"interview": interview_name(f), "transcript": f, "role": None}
        nl = os.path.splitext(f)[0] + "_nl.txt"
        numbered = "\n".join(f"L{i}: {ln}" for i, ln in enumerate(text.splitlines(), 1))
        open(nl, "w", encoding="utf-8").write(numbered)
        entry["numbered"] = nl
        entry["lines"] = len(text.splitlines())
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
                    "manifest": manifest,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Transcripts: {len(manifest)} | ready for mapping: {ready} → {out}")
        for m in manifest:
            print(
                f"  [{m.get('status')}] {m['interview']}"
                + (f" ({m.get('lines')} lines)" if m.get("lines") else "")
            )
        print(
            "Next: for each ready one — the model does the mapping using the chosen lens (S0-S2)."
        )


if __name__ == "__main__":
    main()
