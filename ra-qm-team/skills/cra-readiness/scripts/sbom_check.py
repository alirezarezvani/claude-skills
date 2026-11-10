#!/usr/bin/env python3
"""Check that an SBOM meets the CRA floor: machine-readable, commonly used format, top-level dependencies covered.

Annex I Part II(1) of Regulation (EU) 2024/2847 requires manufacturers to
identify and document vulnerabilities and components, "including by drawing up
a software bill of materials in a commonly used and machine-readable format
covering at the very least the top-level dependencies of the products". The
SBOM goes in the technical documentation (Annex VII(2), and on request (8)).
This script reads a CycloneDX JSON or SPDX 2.x JSON file and checks that floor,
plus the fields you need to match components against vulnerability feeds.

Findings
  UNKNOWN_FORMAT          not CycloneDX JSON or SPDX JSON: not a commonly used machine-readable SBOM    BLOCKER
  NO_PRIMARY_COMPONENT    the SBOM does not say which product it describes                              BLOCKER
  NO_TOP_LEVEL_DEPENDENCIES  no dependency relationship from the product to its components            BLOCKER
  NO_COMPONENTS           no components listed                                                         BLOCKER
  MISSING_VERSION         components without a version: vulnerabilities cannot be matched              HIGH
  DANGLING_REFERENCE      a dependency points at a component that is not in the SBOM                   HIGH
  LOW_IDENTIFIER_COVERAGE fewer than --min-id-coverage of components carry a purl or CPE              MEDIUM
  NO_SUPPLIER             components without a supplier or author                                      MEDIUM
  NO_TIMESTAMP            no creation timestamp: you cannot tell which build it describes              MEDIUM
  NO_HASHES               no component carries a hash                                                  INFO

The CRA does not prescribe a format yet; the Commission may by implementing act
(Art 13(24)). Field expectations here follow common practice (NTIA minimum
elements, BSI TR-03183-2). Deterministic, stdlib only, no network.

Exit codes:
    0  PASS
    2  findings below BLOCKER
    3  invalid input (not JSON, unreadable)
    4  FAIL (a BLOCKER)
"""

import argparse
import json
import sys

SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.6",
    "metadata": {
        "timestamp": "2026-11-02T10:00:00Z",
        "component": {"type": "firmware", "bom-ref": "pkg:generic/clinic-gateway@4.2.1",
                      "name": "clinic-gateway", "version": "4.2.1",
                      "supplier": {"name": "Example GmbH"}},
    },
    "components": [
        {"bom-ref": "pkg:generic/openssl@3.0.15", "name": "openssl", "version": "3.0.15",
         "purl": "pkg:generic/openssl@3.0.15", "supplier": {"name": "OpenSSL Foundation"},
         "hashes": [{"alg": "SHA-256", "content": "23c666d0edf20f14249b3d8f0368acaee9ab585b09e1de82107c66e1f3ec9533"}]},
        {"bom-ref": "pkg:generic/busybox@1.36.1", "name": "busybox", "version": "1.36.1",
         "purl": "pkg:generic/busybox@1.36.1"},
        {"bom-ref": "pkg:generic/vendor-blob", "name": "wifi-firmware-blob"},
    ],
    "dependencies": [
        {"ref": "pkg:generic/clinic-gateway@4.2.1",
         "dependsOn": ["pkg:generic/openssl@3.0.15", "pkg:generic/busybox@1.36.1", "pkg:generic/vendor-blob"]},
        {"ref": "pkg:generic/busybox@1.36.1", "dependsOn": ["pkg:generic/musl@1.2.4"]},
    ],
}


def cyclonedx(doc):
    meta = doc.get("metadata") or {}
    primary = meta.get("component") or {}
    comps = doc.get("components") or []
    root = primary.get("bom-ref")
    refs = {c.get("bom-ref") for c in comps if c.get("bom-ref")}
    if root:
        refs.add(root)
    deps = doc.get("dependencies") or []
    top = []
    for d in deps:
        if root and d.get("ref") == root:
            top = list(d.get("dependsOn") or [])
    dangling = sorted({t for d in deps for t in (d.get("dependsOn") or []) if t not in refs})
    items = []
    for c in comps:
        items.append({"name": c.get("name") or "?", "version": c.get("version"),
                      "identified": bool(c.get("purl") or c.get("cpe")),
                      "supplier": bool(c.get("supplier") or c.get("author") or c.get("authors") or c.get("manufacturer")),
                      "hashed": bool(c.get("hashes"))})
    return {"format": f"CycloneDX {doc.get('specVersion', '?')}", "primary": primary.get("name") if primary else None,
            "primary_ref": root, "timestamp": meta.get("timestamp"), "components": items,
            "top_level": top, "dangling": dangling}


def spdx(doc):
    pkgs = doc.get("packages") or []
    rels = doc.get("relationships") or []
    ids = {p.get("SPDXID") for p in pkgs}
    described = list(doc.get("documentDescribes") or [])
    described += [r.get("relatedSpdxElement") for r in rels
                  if r.get("spdxElementId") == "SPDXRef-DOCUMENT" and r.get("relationshipType") == "DESCRIBES"]
    root = described[0] if described else None
    top = []
    for r in rels:
        t = r.get("relationshipType")
        if root and r.get("spdxElementId") == root and t in {"DEPENDS_ON", "CONTAINS", "STATIC_LINK", "DYNAMIC_LINK"}:
            top.append(r.get("relatedSpdxElement"))
        if root and r.get("relatedSpdxElement") == root and t in {"DEPENDENCY_OF", "CONTAINED_BY"}:
            top.append(r.get("spdxElementId"))
    dangling = sorted({r.get(k) for r in rels for k in ("spdxElementId", "relatedSpdxElement")
                       if r.get(k) and r.get(k) != "SPDXRef-DOCUMENT" and r.get(k) not in ids
                       and not str(r.get(k)).startswith("DocumentRef-") and r.get(k) not in {"NOASSERTION", "NONE"}})
    items = []
    for p in pkgs:
        if p.get("SPDXID") == root:
            continue
        refs = p.get("externalRefs") or []
        items.append({"name": p.get("name") or "?", "version": p.get("versionInfo"),
                      "identified": any(r.get("referenceType") in {"purl", "cpe22Type", "cpe23Type"} for r in refs),
                      "supplier": bool(p.get("supplier") and p.get("supplier") != "NOASSERTION"),
                      "hashed": bool(p.get("checksums"))})
    root_pkg = next((p for p in pkgs if p.get("SPDXID") == root), None)
    return {"format": doc.get("spdxVersion", "SPDX"), "primary": root_pkg.get("name") if root_pkg else root,
            "primary_ref": root, "timestamp": (doc.get("creationInfo") or {}).get("created"),
            "components": items, "top_level": top, "dangling": dangling}


def check(doc, min_cov):
    findings = []

    def add(sev, code, msg):
        findings.append({"severity": sev, "code": code, "message": msg})

    if not isinstance(doc, dict):
        add("BLOCKER", "UNKNOWN_FORMAT", "top level is not a JSON object")
        return {"verdict": "FAIL", "format": None, "findings": findings}
    if doc.get("bomFormat") == "CycloneDX":
        info = cyclonedx(doc)
    elif str(doc.get("spdxVersion", "")).startswith("SPDX-2"):
        info = spdx(doc)
    else:
        add("BLOCKER", "UNKNOWN_FORMAT", "neither CycloneDX JSON (bomFormat) nor SPDX 2.x JSON (spdxVersion); export one of them")
        return {"verdict": "FAIL", "format": None, "findings": findings}

    comps = info["components"]
    n = len(comps)
    if not info["primary_ref"]:
        add("BLOCKER", "NO_PRIMARY_COMPONENT", "no metadata.component (CycloneDX) or DESCRIBES relationship (SPDX): the SBOM does not name the product")
    if n == 0:
        add("BLOCKER", "NO_COMPONENTS", "no components listed")
    if info["primary_ref"] and not info["top_level"]:
        add("BLOCKER", "NO_TOP_LEVEL_DEPENDENCIES", "nothing links the product to its components; Annex I Part II(1) requires at least the top-level dependencies")
    if info["dangling"]:
        add("HIGH", "DANGLING_REFERENCE", f"{len(info['dangling'])} referenced component(s) not described: {', '.join(info['dangling'][:5])}")
    no_ver = [c["name"] for c in comps if not c["version"]]
    if no_ver:
        add("HIGH", "MISSING_VERSION", f"{len(no_ver)} of {n} components have no version: {', '.join(no_ver[:5])}")
    cov = sum(c["identified"] for c in comps) / n if n else 0.0
    if n and cov < min_cov:
        add("MEDIUM", "LOW_IDENTIFIER_COVERAGE", f"{cov:.0%} of components carry a purl or CPE (want {min_cov:.0%}); unidentified components cannot be matched to advisories")
    no_sup = sum(not c["supplier"] for c in comps)
    if no_sup:
        add("MEDIUM", "NO_SUPPLIER", f"{no_sup} of {n} components have no supplier or author")
    if not info["timestamp"]:
        add("MEDIUM", "NO_TIMESTAMP", "no creation timestamp")
    if n and not any(c["hashed"] for c in comps):
        add("INFO", "NO_HASHES", "no component hashes; integrity cannot be checked against the shipped artefacts")

    findings.sort(key=lambda f: SEVERITY_ORDER.index(f["severity"]))
    sev = {f["severity"] for f in findings}
    verdict = "FAIL" if "BLOCKER" in sev else "FINDINGS" if sev & {"HIGH", "MEDIUM"} else "PASS"
    return {"verdict": verdict, "format": info["format"], "product": info["primary"],
            "summary": {"components": n, "top_level_dependencies": len(info["top_level"]),
                        "identifier_coverage": round(cov, 3), "with_version": n - len(no_ver)},
            "findings": findings}


def render(out):
    lines = [f"SBOM check: {out['verdict']}  ({out.get('format') or 'unknown format'}"
             + (f", product: {out['product']})" if out.get("product") else ")")]
    if "summary" in out:
        s = out["summary"]
        lines.append(f"{s['components']} components, {s['top_level_dependencies']} top-level dependencies, "
                     f"{s['identifier_coverage']:.0%} with purl/CPE, {s['with_version']} with version")
    lines.append("")
    for f in out["findings"]:
        lines.append(f"{f['severity']:<7} {f['code']}: {f['message']}")
    if not out["findings"]:
        lines.append("Meets the Annex I Part II(1) floor. Keep it with the technical documentation (Annex VII(2)).")
    return "\n".join(lines)


EXIT = {"PASS": 0, "FINDINGS": 2, "FAIL": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 pass, 2 findings, 3 invalid input, 4 fail.")
    p.add_argument("--sbom", help="CycloneDX JSON or SPDX 2.x JSON file")
    p.add_argument("--min-id-coverage", type=float, default=0.9, help="share of components that need a purl or CPE (default 0.9)")
    p.add_argument("--sample", action="store_true", help="run on a built-in CycloneDX example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if not 0 <= a.min_id_coverage <= 1:
        print("error: --min-id-coverage must be between 0 and 1", file=sys.stderr)
        return 3
    try:
        if a.sample:
            doc = SAMPLE
        else:
            if not a.sbom:
                p.print_usage(sys.stderr)
                print("error: give --sbom or --sample", file=sys.stderr)
                return 3
            with open(a.sbom, encoding="utf-8-sig") as fh:
                doc = json.load(fh)
    except (OSError, json.JSONDecodeError) as e:
        msg = f"cannot read SBOM as JSON: {e}"
        print(json.dumps({"verdict": "INVALID_INPUT", "errors": [msg]}, indent=2) if a.output == "json" else f"error: {msg}",
              file=sys.stdout if a.output == "json" else sys.stderr)
        return 3
    out = check(doc, a.min_id_coverage)
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
