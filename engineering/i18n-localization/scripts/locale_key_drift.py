#!/usr/bin/env python3
"""locale_key_drift — detect drift between i18n locale files.

Compares every locale file against a base locale and reports:
  - missing keys   (in base, absent from a translation -> silent fallback gap)
  - extra keys     (in a translation, absent from base -> dead/renamed key)
  - empty values   (key present but value is "" / null)
  - placeholder mismatches ({{var}} / {var} tokens differ from the base)

Stdlib only. CLI-first. Exit codes: 0 = in sync, 1 = drift found, 2 = error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

# Matches {{var}} (i18next/handlebars) and {var} (ICU / format) interpolation tokens.
_TOKEN_RE = re.compile(r"\{\{\s*([\w.-]+)\s*\}\}|\{\s*([\w.-]+)\s*\}")


def flatten(obj, prefix=""):
    """Flatten a nested dict into {dot.path: value}. Lists are treated as leaf values."""
    out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                out.update(flatten(value, path))
            else:
                out[path] = value
    else:
        out[prefix] = obj
    return out


def tokens(value):
    """Return the set of interpolation token names in a string value."""
    if not isinstance(value, str):
        return set()
    return {m.group(1) or m.group(2) for m in _TOKEN_RE.finditer(value)}


def discover_files(path):
    """Resolve the input path to a sorted list of locale JSON files."""
    if os.path.isdir(path):
        return sorted(
            os.path.join(path, f) for f in os.listdir(path) if f.lower().endswith(".json")
        )
    if os.path.isfile(path):
        return [path]
    return []


def pick_base(files, base_arg):
    """Choose the base file: explicit --base (stem or path), else 'en', else first."""
    if base_arg:
        for f in files:
            stem = os.path.splitext(os.path.basename(f))[0]
            if base_arg in (stem, f, os.path.basename(f)):
                return f
        return None
    for f in files:
        if os.path.splitext(os.path.basename(f))[0].lower() in ("en", "en-us", "en_us"):
            return f
    return files[0]


def analyze(files, base_file, ignore_empty):
    """Compare every non-base file to the base; return a results dict."""
    loaded = {}
    errors = []
    for f in files:
        try:
            with open(f, encoding="utf-8") as fh:
                loaded[f] = flatten(json.load(fh))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append({"file": f, "error": str(exc)})

    base_keys = set(loaded.get(base_file, {}))
    base_map = loaded.get(base_file, {})
    locales = []
    for f, flat in loaded.items():
        if f == base_file:
            continue
        keys = set(flat)
        missing = sorted(base_keys - keys)
        extra = sorted(keys - base_keys)
        empty = (
            []
            if ignore_empty
            else sorted(k for k, v in flat.items() if v is None or v == "")
        )
        placeholder = []
        for k in sorted(base_keys & keys):
            bt, lt = tokens(base_map[k]), tokens(flat[k])
            if bt != lt:
                placeholder.append(
                    {"key": k, "base_tokens": sorted(bt), "locale_tokens": sorted(lt)}
                )
        locales.append(
            {
                "file": os.path.basename(f),
                "missing": missing,
                "extra": extra,
                "empty": empty,
                "placeholder_mismatch": placeholder,
                "in_sync": not (missing or extra or empty or placeholder),
            }
        )
    return {
        "base": os.path.basename(base_file) if base_file else None,
        "base_key_count": len(base_keys),
        "locales": locales,
        "errors": errors,
    }


def render_text(report):
    lines = [f"Base locale: {report['base']} ({report['base_key_count']} keys)", ""]
    for loc in report["locales"]:
        status = "OK" if loc["in_sync"] else "DRIFT"
        lines.append(f"[{status}] {loc['file']}")
        for label in ("missing", "extra", "empty"):
            if loc[label]:
                shown = ", ".join(loc[label][:10])
                more = f" (+{len(loc[label]) - 10} more)" if len(loc[label]) > 10 else ""
                lines.append(f"    {label}: {len(loc[label])} -> {shown}{more}")
        for pm in loc["placeholder_mismatch"][:10]:
            lines.append(
                f"    placeholder: {pm['key']} base={pm['base_tokens']} locale={pm['locale_tokens']}"
            )
    for err in report["errors"]:
        lines.append(f"[ERROR] {err['file']}: {err['error']}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Detect drift (missing/extra/empty keys, placeholder mismatches) across i18n locale files."
    )
    parser.add_argument("path", help="Directory of locale JSON files, or a single JSON file")
    parser.add_argument(
        "--base", help="Base locale to compare against (stem like 'en' or a path). Default: en, else first."
    )
    parser.add_argument(
        "--ignore-empty", action="store_true", help="Do not flag empty-string / null values"
    )
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    args = parser.parse_args()

    files = discover_files(args.path)
    if not files:
        msg = {"error": f"no locale JSON files found at {args.path!r}"}
        print(json.dumps(msg) if args.json else f"error: {msg['error']}", file=sys.stderr)
        return 2
    if len(files) < 2:
        msg = {"error": "need at least 2 locale files to compare"}
        print(json.dumps(msg) if args.json else f"error: {msg['error']}", file=sys.stderr)
        return 2

    base_file = pick_base(files, args.base)
    if base_file is None:
        msg = {"error": f"base locale {args.base!r} not found among files"}
        print(json.dumps(msg) if args.json else f"error: {msg['error']}", file=sys.stderr)
        return 2

    report = analyze(files, base_file, args.ignore_empty)
    print(json.dumps(report, indent=2) if args.json else render_text(report))

    if report["errors"]:
        return 2
    return 0 if all(loc["in_sync"] for loc in report["locales"]) else 1


if __name__ == "__main__":
    sys.exit(main())
