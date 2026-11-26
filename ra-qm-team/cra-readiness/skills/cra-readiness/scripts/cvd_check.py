#!/usr/bin/env python3
"""Check the vulnerability-reporting front door: security.txt (RFC 9116) and the CVD policy.

The CRA asks every manufacturer to put in place and enforce a coordinated vulnerability
disclosure policy (Annex I Part II(5)), to provide a contact address for vulnerability
reports (Annex I Part II(6)), and to tell users where both are (Annex II(2)). These are
ids P2-5, P2-6 and UI-2 in annex_i_gap_check.py. RFC 9116 security.txt is the common,
machine-readable way to publish the contact and point to the policy; this script checks
the file you will publish, and optionally the policy text it points to. It reads local
files only and makes no network calls.

security.txt (RFC 9116)
  NO_CONTACT          no Contact field (required, RFC 9116 2.5.3)              BLOCKER
  BAD_CONTACT         Contact is not a mailto:, https: or tel: URI              BLOCKER
  NO_EXPIRES          no Expires field (required, exactly once, 2.5.5)          BLOCKER
  EXPIRED             Expires is in the past: reporters must treat the file as stale BLOCKER
  BAD_EXPIRES         Expires is not an RFC 3339 date-time, or appears twice    BLOCKER
  NO_POLICY           no Policy field: nothing points reporters to the CVD policy HIGH
  INSECURE_URI        an http:// URI (RFC 9116 requires https for web URIs)     HIGH
  EXPIRES_FAR         Expires more than a year ahead (RFC 9116 recommends less) WARN
  NO_CANONICAL        no Canonical field (lets a reader confirm the file's home) WARN
  NOT_WELL_KNOWN      the file is not at .well-known/security.txt (2.3, 3)      WARN
  UNSIGNED            no OpenPGP cleartext signature (optional, 2.3)            INFO
  UNKNOWN_FIELD       a field RFC 9116 does not define (typo?)                  WARN
  DUPLICATE_FIELD     Preferred-Languages or Expires given more than once       BLOCKER

CVD policy (--policy, a text or markdown file)
  POLICY_NO_CHANNEL   says nowhere how to report (email, form, URL)             HIGH
  POLICY_NO_ACK       no acknowledgement time for a report                       WARN
  POLICY_NO_TIMELINE  no disclosure / remediation timeline                       WARN
  POLICY_NO_SAFE_HARBOR no statement on good-faith research                     WARN
  POLICY_NO_SCOPE     no products or versions in scope                           WARN
  POLICY_NO_ADVISORY  no word on publishing fixed vulnerabilities (Part II(4))  WARN

The policy checks are keyword heuristics: a WARN means "a reader cannot find this", not
"the policy is non-compliant". Exit codes: 0 pass, 2 findings, 3 bad input, 4 blocked.
Deterministic, stdlib only.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

EXIT = {"PASS": 0, "FINDINGS": 2, "BAD_INPUT": 3, "BLOCKED": 4}
KNOWN = {"acknowledgments", "canonical", "contact", "encryption", "expires", "hiring", "policy",
         "preferred-languages", "csaf"}  # CSAF: field added by OASIS CSAF 2.0 for provider metadata
ONCE = {"expires", "preferred-languages"}
URI_FIELDS = {"acknowledgments", "canonical", "contact", "encryption", "hiring", "policy", "csaf"}
SEV_ORDER = {"BLOCKER": 0, "HIGH": 1, "WARN": 2, "INFO": 3}

SAMPLE_TXT = """Contact: mailto:security@example.com
Contact: http://example.com/report
Expires: 2026-01-31T00:00:00Z
Preferred-Languages: en, de
Hiring: https://example.com/jobs
Polcy: https://example.com/cvd
"""
SAMPLE_POLICY = """# Reporting security issues
Email security@example.com with a description and steps to reproduce.
We acknowledge every report within 3 business days.
"""

POLICY_RULES = [
    ("POLICY_NO_CHANNEL", "HIGH", r"(mailto:|@[\w-]+\.\w+|https://|report (it |them )?(via|through|using|at|to)|form)",
     "Say exactly where to send a report: an address or a form, the same one as security.txt Contact."),
    ("POLICY_NO_ACK", "WARN", r"\backnowledg\w*\b.{0,60}\b(\d+|one|two|three|five|seven|ten)\s*(business |working )?(hours?|days?)\b|\bwithin \d+\s*(business |working )?(hours?|days?)\b",
     "State how soon a reporter hears back, e.g. 'we acknowledge reports within 5 business days'."),
    ("POLICY_NO_TIMELINE", "WARN", r"\b(\d+|ninety)[- ]days?\b.{0,80}\b(disclos\w*|publish\w*|fix\w*|remediat\w*|patch\w*)\b|\b(disclos\w*|embargo)\b.{0,80}\b(\d+|ninety)[- ]days?\b|\bcoordinated (vulnerability )?disclosure\b.{0,120}\b(timeline|deadline)\b",
     "Give the coordinated disclosure timeline (e.g. 90 days) and what happens if a fix takes longer."),
    ("POLICY_NO_SAFE_HARBOR", "WARN", r"\b(safe harbou?r|good[- ]faith|will not (pursue|take) legal action|no legal action|authori[sz]ed research)\b",
     "Say that good-faith research within the policy will not be pursued legally."),
    ("POLICY_NO_SCOPE", "WARN", r"\b(in[- ]scope|out[- ]of[- ]scope|scope|applies to|covers?)\b",
     "List the products, versions and services the policy covers, and what is out of scope."),
    ("POLICY_NO_ADVISORY", "WARN", r"\b(advisor(y|ies)|security bulletin|cve|csaf|publicly disclos\w*|publish\w* (details|information))\b",
     "Say that fixed vulnerabilities are published (advisory, CVE, CSAF): Annex I Part II(4) requires it."),
]


def parse_rfc3339(v):
    v = v.strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}:\d{2}(\.\d+)?([Zz]|[+-]\d{2}:\d{2})$", v):
        raise ValueError(v)
    return dt.datetime.fromisoformat(v.replace("Z", "+00:00").replace("z", "+00:00"))


def check_security_txt(text, path, now):
    f = []
    add = lambda code, sev, msg: f.append({"code": code, "severity": sev, "message": msg})
    signed = "-----BEGIN PGP SIGNED MESSAGE-----" in text
    body = text
    if signed:
        body = text.split("-----BEGIN PGP SIGNATURE-----")[0]
    fields = []
    for n, raw in enumerate(body.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("-----") or line.lower().startswith("hash:"):
            continue
        if ":" not in line:
            add("UNKNOWN_FIELD", "WARN", f"line {n} is not 'Field: value': {line[:60]}")
            continue
        name, value = line.split(":", 1)
        fields.append((name.strip().lower(), value.strip(), n))
    names = [x[0] for x in fields]
    for name, value, n in fields:
        if name not in KNOWN:
            hint = " (did you mean Policy?)" if name.startswith("pol") else ""
            add("UNKNOWN_FIELD", "WARN", f"line {n}: '{name}' is not an RFC 9116 field{hint}")
        if name in URI_FIELDS and value.lower().startswith("http://"):
            add("INSECURE_URI", "HIGH", f"line {n}: {name} uses http://, RFC 9116 requires https for web URIs")
    for name in ONCE:
        if names.count(name) > 1:
            add("DUPLICATE_FIELD", "BLOCKER", f"{name} appears {names.count(name)} times; it must appear at most once")
    contacts = [v for k, v, _ in fields if k == "contact"]
    if not contacts:
        add("NO_CONTACT", "BLOCKER", "no Contact field: reporters have no address (CRA Annex I Part II(6))")
    for c in contacts:
        if not re.match(r"^(mailto:[^@\s]+@[^@\s]+|https://\S+|tel:\+?[\d\-. ()]+)$", c, re.I) and not c.lower().startswith("http://"):
            add("BAD_CONTACT", "BLOCKER", f"Contact '{c}' is not a mailto:, https: or tel: URI")
    exp = [v for k, v, _ in fields if k == "expires"]
    if not exp:
        add("NO_EXPIRES", "BLOCKER", "no Expires field (required by RFC 9116)")
    else:
        try:
            when = parse_rfc3339(exp[0])
            if when <= now:
                add("EXPIRED", "BLOCKER", f"Expires {exp[0]} is in the past; renew it and set a reminder")
            elif when - now > dt.timedelta(days=366):
                add("EXPIRES_FAR", "WARN", f"Expires {exp[0]} is over a year ahead; RFC 9116 recommends less than a year")
        except ValueError:
            add("BAD_EXPIRES", "BLOCKER", f"Expires '{exp[0]}' is not an RFC 3339 date-time like 2027-06-30T23:59:59Z")
    if "policy" not in names:
        add("NO_POLICY", "HIGH", "no Policy field pointing to the CVD policy (CRA Annex I Part II(5), Annex II(2))")
    if "canonical" not in names:
        add("NO_CANONICAL", "WARN", "no Canonical field with the URL this file is published at")
    if path and not path.replace(os.sep, "/").endswith(".well-known/security.txt"):
        add("NOT_WELL_KNOWN", "WARN", f"{path} must be served at /.well-known/security.txt")
    if not signed:
        add("UNSIGNED", "INFO", "not OpenPGP-signed (optional; signing lets readers verify the file)")
    summary = {"contacts": contacts, "expires": exp[0] if exp else None,
               "policy": next((v for k, v, _ in fields if k == "policy"), None), "signed": signed}
    return f, summary


def check_policy(text):
    out = []
    for code, sev, rx, fix in POLICY_RULES:
        if not re.search(rx, text, re.I | re.S):
            out.append({"code": code, "severity": sev, "message": fix})
    return out


def run(sec_text, sec_path, policy_text, now):
    findings, summary = check_security_txt(sec_text, sec_path, now) if sec_text is not None else ([], {})
    if policy_text is not None:
        for p in check_policy(policy_text):
            p["source"] = "policy"
            findings.append(p)
    findings.sort(key=lambda x: SEV_ORDER[x["severity"]])
    sevs = {x["severity"] for x in findings}
    verdict = "BLOCKED" if "BLOCKER" in sevs else "FINDINGS" if sevs & {"HIGH", "WARN"} else "PASS"
    counts = {s: sum(1 for x in findings if x["severity"] == s) for s in SEV_ORDER}
    return {"verdict": verdict, "checked_at": now.isoformat(timespec="seconds"), "security_txt": summary,
            "counts": counts, "findings": findings,
            "maps_to": ["P2-5 (CVD policy)", "P2-6 (contact address)", "UI-2 (where users find them)"],
            "evidence_note": "Record 'cvd_check.py PASS <date>' as evidence for P2-5, P2-6 and UI-2 in the Annex I assessment."}


def render(res):
    lines = [f"CVD front door: {res['verdict']}  " + " · ".join(f"{k} {v}" for k, v in res["counts"].items() if v)]
    s = res["security_txt"]
    if s:
        lines.append(f"  contacts {', '.join(s['contacts']) or 'none'} · expires {s['expires'] or 'none'} · "
                     f"policy {s['policy'] or 'none'} · signed {'yes' if s['signed'] else 'no'}")
    for x in res["findings"]:
        src = "policy" if x.get("source") else "security.txt"
        lines.append(f"  [{x['severity']}] {x['code']} ({src}): {x['message']}")
    lines.append(f"  Maps to {', '.join(res['maps_to'])}. {res['evidence_note']}")
    return "\n".join(lines)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                 epilog="Exit codes: 0 pass, 2 findings, 3 bad input, 4 blocked.")
    ap.add_argument("--security-txt", help="security.txt file, or a web root containing .well-known/security.txt")
    ap.add_argument("--policy", help="CVD policy as text or markdown")
    ap.add_argument("--now", help="check time as RFC 3339 (default: now, UTC)")
    ap.add_argument("--sample", action="store_true", help="run on a built-in example")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    a = ap.parse_args(argv)
    try:
        now = parse_rfc3339(a.now) if a.now else dt.datetime.now(dt.timezone.utc)
        if a.sample:
            res = run(SAMPLE_TXT, "public/security.txt", SAMPLE_POLICY, parse_rfc3339("2026-11-26T12:00:00Z"))
        else:
            if not a.security_txt and not a.policy:
                raise ValueError("give --security-txt and/or --policy (or --sample)")
            sec_text = sec_path = pol = None
            if a.security_txt:
                sec_path = a.security_txt
                if os.path.isdir(sec_path):
                    sec_path = os.path.join(sec_path, ".well-known", "security.txt")
                with open(sec_path, encoding="utf-8") as fh:
                    sec_text = fh.read()
            if a.policy:
                with open(a.policy, encoding="utf-8") as fh:
                    pol = fh.read()
            res = run(sec_text, sec_path, pol, now)
    except (OSError, ValueError) as exc:
        print(json.dumps({"verdict": "BAD_INPUT", "error": str(exc)}) if a.output == "json" else f"BAD_INPUT: {exc}")
        return EXIT["BAD_INPUT"]
    print(json.dumps(res, indent=2) if a.output == "json" else render(res))
    return EXIT[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
