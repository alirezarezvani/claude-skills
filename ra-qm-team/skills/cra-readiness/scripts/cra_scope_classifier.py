#!/usr/bin/env python3
"""Classify a product portfolio under the EU Cyber Resilience Act (Regulation (EU) 2024/2847).

For every product in the inventory this answers the questions a CRA programme
has to settle before anything else: is it in scope, who is the manufacturer,
which class is it (default, important class I or II, critical), which
conformity assessment routes are open, is it a legacy product that only owes
Article 14 reporting, is the support period long enough, and which CSIRT
receives its Article 14 reports.

Findings
  ROUTE_NOT_ALLOWED        planned conformity route is not open for the class (Art 32)          BLOCKER
  SUPPORT_TOO_SHORT        support period under 5 years while expected use is 5+ (Art 13(8))     BLOCKER
  REPORTING_CSIRT_UNKNOWN  no Member State to route Article 14 reports to (Art 14(7))           BLOCKER
  NO_PLANNED_ROUTE         in-scope product with no conformity route chosen yet                  HIGH
  SUPPORT_BELOW_USE        support period shorter than the expected use time (Art 13(8))         HIGH
  SUPPORT_NOT_JUSTIFIED    support period set with no written basis (Art 13(8), Annex VII 4)     MEDIUM
  CORE_FUNCTION_UNCLEAR    Annex III/IV category given without saying it is the core function    MEDIUM
  TREATED_AS_MANUFACTURER  importer, distributor or modifier takes manufacturer duties (Art 21/22) INFO
  STEWARD_DUTIES           open-source steward: Art 24 policy, limited Art 14 duties             INFO
  LEGACY_REPORTING_ONLY    placed before 11 Dec 2027, not substantially modified: Art 14 only     INFO
  OUT_OF_SCOPE             excluded by Art 2 or not supplied in a commercial activity            INFO

Inventory CSV columns (one row per product; blank means unknown):
  product, role, sector_regulation, data_connection, commercial, annex_category,
  core_function, harmonised_standards_full, eucc_substantial, foss_docs_public,
  planned_route, placed_on_market, substantially_modified, support_years,
  expected_use_years, support_basis, main_establishment, authorised_rep_ms,
  importer_ms, distributor_ms, most_users_ms

  role               manufacturer | importer | distributor | own_brand | modifier | steward
  sector_regulation  none | mdr | ivdr | vehicle | aviation | marine | defence | classified | spare_part
  commercial         yes | no      (no = not made available in a commercial activity, e.g. non-monetised FOSS)
  annex_category     an id from --list-categories, e.g. III-I-11 (operating systems), III-II-2, IV-3
  planned_route      A | B+C | H | EUCC

Deterministic, stdlib only, no network. Classification is the manufacturer's
own determination; a notified body or market surveillance authority can read a
borderline category differently, so every class call names the Annex entry.

Exit codes:
    0  no findings above INFO
    2  HIGH or MEDIUM findings
    3  invalid input
    4  at least one BLOCKER
"""

import argparse
import csv
import datetime as dt
import io
import json
import sys

APPLICATION_DATE = dt.date(2027, 12, 11)   # Art 71(2): general application
REPORTING_DATE = dt.date(2026, 9, 11)      # Art 71(2): Article 14 applies
MIN_SUPPORT_YEARS = 5                      # Art 13(8), third subparagraph

# Annex III (important products) and Annex IV (critical products), Regulation (EU) 2024/2847.
# Technical descriptions: Commission Implementing Regulation (EU) 2025/2392.
CATEGORIES = {
    "III-I-1": ("IMPORTANT_I", "Identity management systems and privileged access management software and hardware, incl. authentication and access control readers (incl. biometric)"),
    "III-I-2": ("IMPORTANT_I", "Standalone and embedded browsers"),
    "III-I-3": ("IMPORTANT_I", "Password managers"),
    "III-I-4": ("IMPORTANT_I", "Software that searches for, removes, or quarantines malicious software"),
    "III-I-5": ("IMPORTANT_I", "Products with digital elements with the function of virtual private network (VPN)"),
    "III-I-6": ("IMPORTANT_I", "Network management systems"),
    "III-I-7": ("IMPORTANT_I", "Security information and event management (SIEM) systems"),
    "III-I-8": ("IMPORTANT_I", "Boot managers"),
    "III-I-9": ("IMPORTANT_I", "Public key infrastructure and digital certificate issuance software"),
    "III-I-10": ("IMPORTANT_I", "Physical and virtual network interfaces"),
    "III-I-11": ("IMPORTANT_I", "Operating systems"),
    "III-I-12": ("IMPORTANT_I", "Routers, modems intended for the connection to the internet, and switches"),
    "III-I-13": ("IMPORTANT_I", "Microprocessors with security-related functionalities"),
    "III-I-14": ("IMPORTANT_I", "Microcontrollers with security-related functionalities"),
    "III-I-15": ("IMPORTANT_I", "ASICs and FPGAs with security-related functionalities"),
    "III-I-16": ("IMPORTANT_I", "Smart home general purpose virtual assistants"),
    "III-I-17": ("IMPORTANT_I", "Smart home products with security functionalities (smart door locks, security cameras, baby monitoring systems, alarm systems)"),
    "III-I-18": ("IMPORTANT_I", "Internet connected toys (Directive 2009/48/EC) with social interactive or location tracking features"),
    "III-I-19": ("IMPORTANT_I", "Personal wearables with health monitoring (not covered by Reg 2017/745 or 2017/746) or intended for use by and for children"),
    "III-II-1": ("IMPORTANT_II", "Hypervisors and container runtime systems that support virtualised execution of operating systems and similar environments"),
    "III-II-2": ("IMPORTANT_II", "Firewalls, intrusion detection and prevention systems"),
    "III-II-3": ("IMPORTANT_II", "Tamper-resistant microprocessors"),
    "III-II-4": ("IMPORTANT_II", "Tamper-resistant microcontrollers"),
    "IV-1": ("CRITICAL", "Hardware Devices with Security Boxes"),
    "IV-2": ("CRITICAL", "Smart meter gateways within smart metering systems and other devices for advanced security purposes, incl. secure cryptoprocessing"),
    "IV-3": ("CRITICAL", "Smartcards or similar devices, including secure elements"),
}

EXCLUSIONS = {
    "mdr": "Art 2(2): medical devices under Regulation (EU) 2017/745. Cybersecurity is regulated there instead (MDR Annex I, 17.2 and 17.4)",
    "ivdr": "Art 2(2): in vitro diagnostic devices under Regulation (EU) 2017/746 (IVDR Annex I, 16.2 and 16.4)",
    "vehicle": "Art 2(2): products covered by Regulation (EU) 2019/2144 (vehicle type-approval)",
    "aviation": "Art 2(3): products certified under Regulation (EU) 2018/1139",
    "marine": "Art 2(4): equipment within Directive 2014/90/EU (marine equipment)",
    "defence": "Art 2(7): developed or modified exclusively for national security or defence",
    "classified": "Art 2(7): specifically designed to process classified information",
    "spare_part": "Art 2(6): spare part replacing an identical component, made to the same specifications",
}

ROUTES = {
    # Art 32(1): default products; Art 32(2): class I; Art 32(3): class II; Art 32(4): critical
    "DEFAULT": {"A", "B+C", "H", "EUCC"},
    "IMPORTANT_I": {"B+C", "H", "EUCC"},          # + A only with full harmonised standards / common specs / EUCC substantial
    "IMPORTANT_II": {"B+C", "H", "EUCC"},
    "CRITICAL": {"EUCC", "B+C", "H"},             # EUCC under Art 8(1) where a delegated act requires it; else Art 32(3)
}

ROLES = {"manufacturer", "importer", "distributor", "own_brand", "modifier", "steward"}
YES = {"yes", "y", "true", "1"}
NO = {"no", "n", "false", "0"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = """product,role,sector_regulation,data_connection,commercial,annex_category,core_function,harmonised_standards_full,eucc_substantial,foss_docs_public,planned_route,placed_on_market,substantially_modified,support_years,expected_use_years,support_basis,main_establishment,authorised_rep_ms,importer_ms,distributor_ms,most_users_ms
GaitCam Home (consumer fall-alert camera),manufacturer,none,yes,yes,III-I-17,yes,no,no,,A,2028-03-01,,5,8,,DE,,,,
GaitCam Pro (MDR class IIa software),manufacturer,mdr,yes,yes,,,,,,,2024-05-01,,,,,DE,,,,
Clinic Gateway Router,manufacturer,none,yes,yes,III-I-12,yes,no,no,,B+C,2028-06-01,,7,7,Router fleet data: median 7.2 years in field,DE,,,,
EdgeGuard Firewall (rebranded OEM),own_brand,none,yes,yes,III-II-2,yes,no,no,,A,2028-01-15,,5,5,,,,AT,,
Sensor SDK v3 (legacy),manufacturer,none,yes,yes,,,,,,,2025-02-01,no,3,6,,,,,,
Community parser library,steward,none,yes,no,,,,,,,,,,,,NL,,,,
"""


def norm(v):
    return (v or "").strip()


def yes(v):
    return norm(v).lower() in YES


def no(v):
    return norm(v).lower() in NO


def parse_date(v, field):
    v = norm(v)
    if not v:
        return None
    try:
        return dt.date.fromisoformat(v)
    except ValueError:
        raise ValueError(f"{field}: '{v}' is not a YYYY-MM-DD date")


def parse_num(v, field):
    v = norm(v)
    if not v:
        return None
    try:
        n = float(v)
    except ValueError:
        raise ValueError(f"{field}: '{v}' is not a number")
    if n < 0:
        raise ValueError(f"{field}: '{v}' is negative")
    return n


def reporting_csirt(row):
    """Art 14(7): main establishment, then authorised representative, importer, distributor, most users."""
    for col, basis in (("main_establishment", "main establishment in the Union"),
                       ("authorised_rep_ms", "authorised representative (no EU main establishment)"),
                       ("importer_ms", "importer (no EU establishment or authorised representative)"),
                       ("distributor_ms", "distributor (no EU establishment, representative or importer)"),
                       ("most_users_ms", "Member State with the most users")):
        ms = norm(row.get(col)).upper()
        if ms:
            return ms, basis
    return None, None


def classify(row, line, as_of):
    name = norm(row.get("product")) or f"row {line}"
    role = norm(row.get("role")).lower() or "manufacturer"
    if role not in ROLES:
        raise ValueError(f"row {line} ({name}): role '{role}' is not one of {sorted(ROLES)}")
    findings = []

    def add(sev, code, msg, ref):
        findings.append({"severity": sev, "code": code, "message": msg, "ref": ref})

    result = {"product": name, "role": role, "in_scope": True, "class": None, "allowed_routes": [],
              "legacy": False, "reporting_csirt": None, "obligations": [], "findings": findings}

    sector = norm(row.get("sector_regulation")).lower() or "none"
    if sector != "none":
        if sector not in EXCLUSIONS:
            raise ValueError(f"row {line} ({name}): sector_regulation '{sector}' is not one of none, {', '.join(EXCLUSIONS)}")
        result["in_scope"] = False
        add("INFO", "OUT_OF_SCOPE", EXCLUSIONS[sector], "Art 2")
        return result
    if no(row.get("data_connection")):
        result["in_scope"] = False
        add("INFO", "OUT_OF_SCOPE", "no direct or indirect logical or physical data connection to a device or network", "Art 2(1)")
        return result

    if role == "steward":
        result["in_scope"] = False
        result["class"] = "STEWARD"
        result["obligations"] = ["Art 24(1) documented cybersecurity policy", "Art 24(2) cooperate with market surveillance",
                                 "Art 14(1) report actively exploited vulnerabilities to the extent involved in development",
                                 "Art 14(3) and 14(8) for severe incidents on infrastructure the steward provides"]
        add("INFO", "STEWARD_DUTIES", "open-source software steward: no CE marking; Article 24 duties apply from 11 Dec 2027, and Art 64 fines do not apply to stewards (Art 64(10)(b))", "Art 24, Art 64(10)(b)")
        csirt, basis = reporting_csirt(row)
        result["reporting_csirt"] = {"member_state": csirt, "basis": basis} if csirt else None
        return result
    if no(row.get("commercial")):
        result["in_scope"] = False
        add("INFO", "OUT_OF_SCOPE", "not made available in the course of a commercial activity (e.g. FOSS not monetised by its publisher); re-check if you charge, gate updates or monetise data", "Art 3(22), recitals 18-19")
        return result

    if role in {"own_brand", "modifier"} or (role in {"importer", "distributor"} and yes(row.get("substantially_modified"))):
        ref = "Art 21" if role in {"own_brand", "importer", "distributor"} else "Art 22"
        add("INFO", "TREATED_AS_MANUFACTURER", f"role '{role}' carries the manufacturer's obligations (Arts 13 and 14)", ref)
        result["role"] = f"{role} (manufacturer duties)"
    elif role == "importer":
        result["obligations"].append("Art 19: check CE marking, EU DoC, technical documentation and manufacturer contact before placing on the market")
    elif role == "distributor":
        result["obligations"].append("Art 20: check CE marking and that manufacturer and importer met their duties before making available")

    # Class (Art 7, Art 8, Annex III/IV)
    cat = norm(row.get("annex_category")).upper()
    klass = "DEFAULT"
    if cat:
        if cat not in CATEGORIES:
            raise ValueError(f"row {line} ({name}): annex_category '{cat}' unknown; see --list-categories")
        if no(row.get("core_function")):
            add("INFO", "INTEGRATED_ONLY", f"{cat} is integrated but is not the core function: integration alone does not make the host product important", "Art 7(1)")
        else:
            klass = CATEGORIES[cat][0]
            if not yes(row.get("core_function")):
                add("MEDIUM", "CORE_FUNCTION_UNCLEAR", f"{cat} assumed to be the core function; confirm against the technical description", "Art 7(1), Implementing Reg (EU) 2025/2392")
    result["class"] = klass
    result["annex_entry"] = f"{cat}: {CATEGORIES[cat][1]}" if cat else None

    # Legacy (Art 69(2)-(3))
    placed = parse_date(row.get("placed_on_market"), f"row {line} placed_on_market")
    if placed and placed < APPLICATION_DATE and not yes(row.get("substantially_modified")):
        result["legacy"] = True
        add("INFO", "LEGACY_REPORTING_ONLY", f"placed on the market {placed}, before 11 Dec 2027: only Article 14 reporting applies unless substantially modified from that date. Units of the same type first placed after 11 Dec 2027 need full conformity", "Art 69(2)-(3)")

    # Conformity route (Art 32)
    if not result["legacy"]:
        allowed = set(ROUTES[klass])
        if klass == "IMPORTANT_I" and (yes(row.get("harmonised_standards_full")) or yes(row.get("eucc_substantial"))):
            allowed.add("A")
        if klass in {"IMPORTANT_I", "IMPORTANT_II"} and yes(row.get("foss_docs_public")):
            allowed.add("A")
        result["allowed_routes"] = sorted(allowed)
        route = norm(row.get("planned_route")).upper().replace(" ", "")
        if not route:
            add("HIGH", "NO_PLANNED_ROUTE", f"choose a conformity route before {APPLICATION_DATE}; open routes: {', '.join(sorted(allowed))}", "Art 32")
        elif route not in {"A", "B+C", "H", "EUCC"}:
            raise ValueError(f"row {line} ({name}): planned_route '{route}' is not A, B+C, H or EUCC")
        elif route not in allowed:
            why = {"IMPORTANT_I": "module A needs harmonised standards, common specifications or an EUCC scheme at 'substantial' applied in full; none is applied in full",
                   "IMPORTANT_II": "class II always needs a notified body (B+C or H) or an EUCC certificate at 'substantial'",
                   "CRITICAL": "critical products need EUCC where a delegated act under Art 8(1) requires it, otherwise B+C or H"}.get(klass, "")
            add("BLOCKER", "ROUTE_NOT_ALLOWED", f"planned route {route} is not open for {klass}: {why}", "Art 32(2)-(4)")
        result["obligations"] += ["Annex I Part I and Part II", "technical documentation (Annex VII)", "EU declaration of conformity and CE marking (Arts 28, 30)", "user information (Annex II)"]

    # Support period (Art 13(8))
    support = parse_num(row.get("support_years"), f"row {line} support_years")
    use = parse_num(row.get("expected_use_years"), f"row {line} expected_use_years")
    if support is not None and not result["legacy"]:
        if support < MIN_SUPPORT_YEARS and (use is None or use >= MIN_SUPPORT_YEARS):
            add("BLOCKER", "SUPPORT_TOO_SHORT", f"support period {support:g} years is under the 5-year minimum and the expected use time is {'unknown' if use is None else f'{use:g} years'}", "Art 13(8)")
        elif use is not None and support < use:
            add("HIGH", "SUPPORT_BELOW_USE", f"support period {support:g} years is shorter than the expected use time of {use:g} years; the period must reflect expected use", "Art 13(8), second subparagraph")
        if not norm(row.get("support_basis")):
            add("MEDIUM", "SUPPORT_NOT_JUSTIFIED", "record the information used to set the support period (expected use, comparable products, component support)", "Art 13(8), Annex VII point 4")

    # Reporting route (Art 14(7)) -- live since 11 Sep 2026 for every in-scope product, legacy included
    csirt, basis = reporting_csirt(row)
    if csirt:
        result["reporting_csirt"] = {"member_state": csirt, "basis": basis}
    else:
        sev = "BLOCKER" if as_of >= REPORTING_DATE else "HIGH"
        add(sev, "REPORTING_CSIRT_UNKNOWN", "no Member State given for main establishment, authorised representative, importer, distributor or most users; Article 14 reports cannot be routed", "Art 14(7)")
    result["obligations"].insert(0, "Art 14 reporting (actively exploited vulnerabilities, severe incidents) via the ENISA Single Reporting Platform")
    return result


def run(text, as_of):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("inventory has no rows")
    if "product" not in (rows[0].keys() if rows else []):
        raise ValueError("inventory needs at least a 'product' column")
    products = [classify(r, i + 2, as_of) for i, r in enumerate(rows)]
    counts = {s: 0 for s in SEVERITY_ORDER}
    for p in products:
        for f in p["findings"]:
            counts[f["severity"]] += 1
    verdict = "BLOCKED" if counts["BLOCKER"] else "FINDINGS" if counts["HIGH"] or counts["MEDIUM"] else "CLEAR"
    classes = {}
    for p in products:
        key = p["class"] if p["in_scope"] else ("STEWARD" if p["class"] == "STEWARD" else "OUT_OF_SCOPE")
        classes[key] = classes.get(key, 0) + 1
    return {"verdict": verdict, "as_of": as_of.isoformat(),
            "days_to_full_application": (APPLICATION_DATE - as_of).days,
            "reporting_in_force": as_of >= REPORTING_DATE,
            "summary": {"products": len(products), "classes": classes, "findings": counts},
            "products": products}


def render(out):
    lines = [f"CRA scope: {out['verdict']}  (as of {out['as_of']}; "
             f"{'Art 14 reporting IN FORCE' if out['reporting_in_force'] else 'Art 14 not yet in force'}; "
             f"{out['days_to_full_application']} days to 11 Dec 2027)", ""]
    for p in out["products"]:
        scope = p["class"] if p["in_scope"] else ("STEWARD" if p["class"] == "STEWARD" else "OUT OF SCOPE")
        tag = " [legacy: Art 14 only]" if p["legacy"] else ""
        lines.append(f"- {p['product']}: {scope}{tag}  role={p['role']}")
        if p.get("annex_entry"):
            lines.append(f"    annex: {p['annex_entry']}")
        if p["allowed_routes"]:
            lines.append(f"    open routes: {', '.join(p['allowed_routes'])}")
        if p["reporting_csirt"]:
            lines.append(f"    Art 14 reports: CSIRT of {p['reporting_csirt']['member_state']} ({p['reporting_csirt']['basis']})")
        for f in sorted(p["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['products']} products: " + ", ".join(f"{k} {v}" for k, v in sorted(s["classes"].items())),
              "Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              "Self-classification only: a notified body or market surveillance authority may read a borderline category differently."]
    return "\n".join(lines)


EXIT = {"CLEAR": 0, "FINDINGS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clear, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--inventory", help="product inventory CSV (columns in the module docstring)")
    p.add_argument("--as-of", help="evaluation date YYYY-MM-DD (default: today)")
    p.add_argument("--list-categories", action="store_true", help="print the Annex III/IV category ids and exit")
    p.add_argument("--sample", action="store_true", help="run on a built-in example portfolio")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list_categories:
        if a.output == "json":
            print(json.dumps({k: {"class": c, "name": n} for k, (c, n) in CATEGORIES.items()}, indent=2))
        else:
            for k, (c, n) in CATEGORIES.items():
                print(f"{k:<10} {c:<13} {n}")
        return 0
    try:
        if a.sample:
            text, as_of = SAMPLE, dt.date(2026, 11, 10)
        else:
            if not a.inventory:
                p.print_usage(sys.stderr)
                print("error: give --inventory, --list-categories or --sample", file=sys.stderr)
                return 3
            with open(a.inventory, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
            as_of = parse_date(a.as_of, "--as-of") or dt.date.today()
        out = run(text, as_of)
    except (OSError, ValueError, csv.Error) as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
