#!/usr/bin/env python3
"""Check a SOUP / third-party component register against IEC 62304, IEC 81001-5-1 and FDA 524B, and against the SBOM.

SOUP (software of unknown provenance) is the usual place a 62304 file falls
apart: an entry with no version, a class C product whose SOUP has no stated
requirements, an anomaly list nobody read since the last release, a library
past end of support with no plan, and an SBOM that lists different components
than the register.

Checks per register row
  8.1.2   every SOUP item: title, manufacturer, unique designator (version)    all classes
  5.3.3   functional and performance requirements the item must meet           class B, C
  5.3.4   system hardware and software the item needs                          class B, C
  7.1.3   published anomaly list evaluated (date of last review)               class B, C
  81001-5-1 4.1.5 / 4.3  third-party item category: maintained | supported | required (nested
          categories per Interpretation Sheet 1:2025; the narrowest that is true)
  524B(b)(1)/(3) cyber devices: vulnerability monitoring in place, item in the SBOM

CSV columns (header required)
  id, name, version, supplier, used_in_class (A|B|C), functional_requirements,
  hw_sw_requirements, anomaly_list_source, anomaly_review_date (YYYY-MM-DD),
  support_category (maintained|supported|required), end_of_support (YYYY-MM-DD or ''),
  eos_plan, vuln_monitoring (yes|no), purl

Findings
  NO_VERSION            no unique designator: the item cannot be identified (8.1.2)        BLOCKER
  MISSING_REQUIREMENTS  class B/C item with no functional/performance or HW/SW requirements  BLOCKER
  ANOMALIES_NOT_REVIEWED class B/C item with no anomaly-list review (7.1.3)                  BLOCKER
  PAST_END_OF_SUPPORT   end of support passed and no plan recorded                          BLOCKER
  NO_VULN_MONITORING    cyber device (--cyber-device) item without vulnerability monitoring  BLOCKER
  STALE_ANOMALY_REVIEW  anomaly review older than --max-review-days (default 180)           HIGH
  EOS_SOON              end of support within --eos-warn-days (default 365)                 HIGH
  NO_SUPPORT_CATEGORY   no 81001-5-1 risk-transfer category                                  HIGH
  CATEGORY_STALE        past end of support but still 'maintained'/'supported' (ISH1:2025)    HIGH
  NOT_IN_SBOM           register item missing from the SBOM (--sbom)                         HIGH
  NOT_IN_REGISTER       SBOM component missing from the register (--sbom)                    HIGH
  NO_PURL               no package URL / identifier for vulnerability matching               INFO

The review-age and end-of-support windows are this skill's defaults, not
values from any standard: set them to your SOP. Deterministic, stdlib only, no
network; it never queries a vulnerability database.

Exit codes:
    0  PASS
    2  FINDINGS
    3  invalid input
    4  BLOCKED
"""

import argparse
import csv
import datetime as dt
import io
import json
import sys

COLUMNS = ["id", "name", "version", "supplier", "used_in_class", "functional_requirements", "hw_sw_requirements",
           "anomaly_list_source", "anomaly_review_date", "support_category", "end_of_support", "eos_plan",
           "vuln_monitoring", "purl"]
CATS = {"maintained", "supported", "required"}
SEV = {"BLOCKER": 4, "HIGH": 2, "INFO": 0}
UNVERSIONED = {"", "latest", "*", "any", "unknown", "n/a", "na"}

SAMPLE = """id,name,version,supplier,used_in_class,functional_requirements,hw_sw_requirements,anomaly_list_source,anomaly_review_date,support_category,end_of_support,eos_plan,vuln_monitoring,purl
S1,openssl,3.0.13,OpenSSL Project,C,TLS 1.2+ for device-cloud link; handshake < 500 ms,Linux 5.x; 4 MB RAM,https://openssl-library.org/news/vulnerabilities/,2026-10-02,maintained,2026-09-07,,yes,pkg:generic/openssl@3.0.13
S2,sqlite,3.45.1,SQLite,C,,,https://www.sqlite.org/cves.html,2025-11-20,maintained,,,yes,pkg:generic/sqlite@3.45.1
S3,qt-base,latest,The Qt Company,B,render UI at 30 fps,ARM Cortex-A53; GPU ES 2.0,https://bugreports.qt.io,,supported,2027-03-31,,no,
S4,zlib,1.3.1,zlib,A,,,,,maintained,,,yes,pkg:generic/zlib@1.3.1
"""

SAMPLE_SBOM = {"bomFormat": "CycloneDX", "specVersion": "1.5",
               "components": [{"name": "openssl", "version": "3.0.13"}, {"name": "sqlite", "version": "3.45.1"},
                              {"name": "zlib", "version": "1.3.1"}, {"name": "libcurl", "version": "8.5.0"}]}


def date(v, field, rid):
    v = (v or "").strip()
    if not v:
        return None
    try:
        return dt.date.fromisoformat(v)
    except ValueError:
        raise ValueError(f"{rid}: {field} must be YYYY-MM-DD, got {v!r}")


def sbom_components(doc):
    out = set()
    if isinstance(doc, dict) and doc.get("bomFormat") == "CycloneDX":
        stack = list(doc.get("components") or [])
        while stack:
            c = stack.pop()
            out.add(((c.get("name") or "").lower(), (c.get("version") or "").strip()))
            stack.extend(c.get("components") or [])
    elif isinstance(doc, dict) and "spdxVersion" in doc:
        for pk in doc.get("packages") or []:
            out.add(((pk.get("name") or "").lower(), (pk.get("versionInfo") or "").strip()))
    else:
        raise ValueError("SBOM must be CycloneDX or SPDX JSON")
    return out


def run(text, today, max_review, eos_warn, cyber, sbom):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("no rows")
    missing = [c for c in COLUMNS if c not in rows[0]]
    if missing:
        raise ValueError(f"missing columns: {', '.join(missing)}")
    findings, items = [], []
    seen = set()
    for n, r in enumerate(rows, 2):
        r = {k: (v or "").strip() for k, v in r.items() if k}
        rid = r["id"] or f"line{n}"
        if rid in seen:
            raise ValueError(f"line {n}: duplicate id {rid}")
        seen.add(rid)
        cls = r["used_in_class"].upper()
        if cls not in ("A", "B", "C"):
            raise ValueError(f"line {n}: used_in_class must be A, B or C")
        label = f"{r['name'] or '?'}@{r['version'] or '?'}"
        if r["version"].lower() in UNVERSIONED or not r["name"] or not r["supplier"]:
            findings.append(("BLOCKER", "NO_VERSION", rid,
                             f"{label}: SOUP needs title, manufacturer and a unique designator (8.1.2); pin an exact version"))
        if cls in ("B", "C"):
            gaps = [k for k, ref in (("functional_requirements", "5.3.3"), ("hw_sw_requirements", "5.3.4")) if not r[k]]
            if gaps:
                findings.append(("BLOCKER", "MISSING_REQUIREMENTS", rid,
                                 f"{label} in class {cls}: missing {', '.join(gaps)} (5.3.3 / 5.3.4)"))
            rev = date(r["anomaly_review_date"], "anomaly_review_date", rid)
            if not rev:
                findings.append(("BLOCKER", "ANOMALIES_NOT_REVIEWED", rid,
                                 f"{label} in class {cls}: published anomaly list never evaluated (7.1.3)"))
            elif (today - rev).days > max_review:
                findings.append(("HIGH", "STALE_ANOMALY_REVIEW", rid,
                                 f"{label}: anomaly list last reviewed {rev} ({(today - rev).days} days ago; policy {max_review})"))
        eos = date(r["end_of_support"], "end_of_support", rid)
        if eos and eos < today and not r["eos_plan"]:
            findings.append(("BLOCKER", "PAST_END_OF_SUPPORT", rid,
                             f"{label}: end of support {eos} passed with no recorded plan (replace, take over maintenance, or accept with risk rationale)"))
        elif eos and (eos - today).days <= eos_warn and eos >= today:
            findings.append(("HIGH", "EOS_SOON", rid, f"{label}: end of support {eos} within {eos_warn} days"))
        cat = r["support_category"].lower()
        if eos and eos < today and cat in ("maintained", "supported"):
            findings.append(("HIGH", "CATEGORY_STALE", rid,
                             f"{label}: past end of support but categorised '{cat}'; with no upstream updates it is "
                             "'required' in practice (81001-5-1 4.3, ISH1:2025): re-evaluate 6.3.x and tell operators"))
        if cat not in CATS:
            findings.append(("HIGH", "NO_SUPPORT_CATEGORY", rid,
                             f"{label}: give the IEC 81001-5-1 risk-transfer category (maintained, supported or required)"))
        if cyber and r["vuln_monitoring"].lower() not in ("yes", "y", "true"):
            findings.append(("BLOCKER", "NO_VULN_MONITORING", rid,
                             f"{label}: cyber device under 524B(b)(1) needs postmarket vulnerability monitoring for every component"))
        if not r["purl"]:
            findings.append(("INFO", "NO_PURL", rid, f"{label}: no purl/CPE, so vulnerability feeds cannot be matched automatically"))
        items.append({"id": rid, "name": r["name"], "version": r["version"], "class": cls, "category": cat or None})
    if sbom is not None:
        comps = sbom_components(sbom)
        reg = {(i["name"].lower(), i["version"]) for i in items}
        for i in items:
            if (i["name"].lower(), i["version"]) not in comps:
                findings.append(("HIGH", "NOT_IN_SBOM", i["id"], f"{i['name']}@{i['version']} is in the register but not the SBOM"))
        for name, ver in sorted(comps - reg):
            findings.append(("HIGH", "NOT_IN_REGISTER", name,
                             f"{name}@{ver} is in the SBOM but not the SOUP register: assess it or remove it from the build"))
    worst = max([SEV[f[0]] for f in findings] or [0])
    verdict = {4: "BLOCKED", 2: "FINDINGS", 0: "PASS"}[worst]
    order = {"BLOCKER": 0, "HIGH": 1, "INFO": 2}
    findings.sort(key=lambda f: (order[f[0]], f[2]))
    return {"verdict": verdict, "as_of": today.isoformat(), "items": len(items), "cyber_device": cyber,
            "sbom_checked": sbom is not None,
            "findings": [{"severity": s, "code": c, "id": i, "detail": d} for s, c, i, d in findings],
            "note": "Windows (review age, end-of-support warning) are policy defaults; set them to your SOP. "
                    "No vulnerability database is queried."}


def render(out):
    lines = [f"SOUP register check: {out['verdict']} ({out['items']} items, as of {out['as_of']}"
             + (", cyber device" if out["cyber_device"] else "") + (", SBOM compared" if out["sbom_checked"] else "") + ")", ""]
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']} {f['id']}: {f['detail']}")
    lines += ["", out["note"]]
    return "\n".join(lines)


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter,
                                epilog="Exit codes: 0 pass, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--register", help="SOUP register CSV (columns in module docstring)")
    p.add_argument("--sbom", help="CycloneDX or SPDX JSON to compare against the register")
    p.add_argument("--cyber-device", action="store_true", help="the device is a 524B cyber device")
    p.add_argument("--today", help="evaluate as of this date (YYYY-MM-DD); default today")
    p.add_argument("--max-review-days", type=int, default=180, help="anomaly review age policy (default 180)")
    p.add_argument("--eos-warn-days", type=int, default=365, help="end-of-support warning window (default 365)")
    p.add_argument("--template", action="store_true", help="print the CSV header and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in register and SBOM")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.template:
        print(",".join(COLUMNS))
        return 0
    try:
        today = dt.date.fromisoformat(a.today) if a.today else dt.date.today()
        sbom = None
        if a.sample:
            text, sbom, a.cyber_device = SAMPLE, SAMPLE_SBOM, True
            if not a.today:
                today = dt.date(2026, 11, 11)
        else:
            if not a.register:
                p.print_usage(sys.stderr)
                print("error: give --register, --template or --sample", file=sys.stderr)
                return 3
            with open(a.register, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            if a.sbom:
                with open(a.sbom, encoding="utf-8") as fh:
                    sbom = json.load(fh)
        out = run(text, today, a.max_review_days, a.eos_warn_days, a.cyber_device, sbom)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return {"BLOCKED": 4, "FINDINGS": 2, "PASS": 0}[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
