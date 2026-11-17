#!/usr/bin/env python3
"""Classify entities under NIS2 (Directive (EU) 2022/2555): out of scope, important or essential.

NIS2 applies to medium-sized and large entities in the sectors of Annex I and
Annex II (Art 2(1)), plus a list of entities caught regardless of size (Art
2(2)-(4)). Which category an entity lands in decides how it is supervised
(ex ante for essential, ex post for important, Arts 32-33) and the fine ceiling
(Art 34(4)-(5)). This script reads an entity list and returns, per entity, the
category, the article that put it there, where it is supervised, and what to
do next. It never guesses a size: an entity with no headcount and no financials
is blocked, not called small.

Size test (Commission Recommendation 2003/361/EC, Annex Art 2, as NIS2 Art 2(1) refers to it)
  small or micro      fewer than 50 staff AND (turnover <= EUR 10m OR balance sheet <= EUR 10m)
  medium              not small, and fewer than 250 staff AND (turnover <= EUR 50m OR balance sheet <= EUR 43m)
  large               250+ staff OR (turnover > EUR 50m AND balance sheet > EUR 43m)
  Partner and linked enterprises count (Annex Art 6); fill the columns with group-adjusted data.

Categories
  ESSENTIAL   Art 3(1): large Annex I entity; qualified trust service provider, TLD registry or DNS
              provider of any size; medium-sized public e-communications provider; central public
              administration; CER critical entity; entity a Member State designates as essential
  IMPORTANT   Art 3(2): every other in-scope Annex I or II entity
  LIMITED     domain name registration services: Art 2(4) brings them in only for Arts 3(3) and 28
  OUT         small or micro entity with no size-independent ground
  MS_OPTION   regional public administration, education: in scope only if the Member State says so (Art 2(2)(f)(ii), 2(5))

DORA overlap (Art 4, recital 28; Regulation (EU) 2022/2554 Art 1(2)): for financial entities under
DORA, DORA replaces the NIS2 risk-management (Art 21) and reporting (Art 23) duties. The entity can
still be on the national NIS2 list. Flagged as DORA_LEX_SPECIALIS.

Entity CSV columns
  name, sector (key; --list-sectors), employees, turnover_eur_m, balance_eur_m,
  special (semicolon list; --list-special), member_states (space separated), main_establishment,
  dora_entity (yes|no)

Deterministic, stdlib only, no network. Not legal advice: national transposition decides the
details (for Germany, BSIG as amended by NIS2UmsuCG, in force 6 December 2025).

Exit codes:
    0  every entity classified, no findings
    2  classified with findings to act on
    3  invalid input
    4  an entity cannot be classified (unknown sector or no size data)
"""

import argparse
import csv
import io
import json
import sys

ANNEX_I = {
    "energy-electricity": "Energy: electricity", "energy-district-heating": "Energy: district heating and cooling",
    "energy-oil": "Energy: oil", "energy-gas": "Energy: gas", "energy-hydrogen": "Energy: hydrogen",
    "transport-air": "Transport: air", "transport-rail": "Transport: rail", "transport-water": "Transport: water",
    "transport-road": "Transport: road", "banking": "Banking (credit institutions)",
    "financial-market-infrastructure": "Financial market infrastructures (trading venues, CCPs)",
    "health": "Health (healthcare providers, EU reference labs, medicinal-product R&D and manufacture, critical medical devices in a public health emergency)",
    "drinking-water": "Drinking water", "waste-water": "Waste water",
    "digital-infrastructure": "Digital infrastructure (IXPs, DNS, TLD registries, cloud, data centres, CDNs, trust services, public e-communications)",
    "ict-service-management": "ICT service management B2B (managed service and managed security service providers)",
    "public-administration": "Public administration", "space": "Space",
}
ANNEX_II = {
    "postal-courier": "Postal and courier services", "waste-management": "Waste management",
    "chemicals": "Manufacture, production and distribution of chemicals",
    "food": "Production, processing and distribution of food",
    "manufacturing-medical-devices": "Manufacturing: medical devices and in vitro diagnostic medical devices",
    "manufacturing-electronics": "Manufacturing: computer, electronic and optical products",
    "manufacturing-electrical": "Manufacturing: electrical equipment",
    "manufacturing-machinery": "Manufacturing: machinery and equipment n.e.c.",
    "manufacturing-motor-vehicles": "Manufacturing: motor vehicles, trailers and semi-trailers",
    "manufacturing-other-transport": "Manufacturing: other transport equipment",
    "digital-providers": "Digital providers (online marketplaces, search engines, social networking platforms)",
    "research": "Research organisations",
}
NONE_SECTOR = {"none": "No Annex I or II sector"}

SPECIAL = {
    "public-ecomms": ("provider of public electronic communications networks or publicly available services", "Art 2(2)(a)"),
    "qtsp": ("qualified trust service provider", "Art 2(2)(a)"),
    "tsp": ("non-qualified trust service provider", "Art 2(2)(a)"),
    "tld-registry": ("top-level domain name registry", "Art 2(2)(a)"),
    "dns": ("DNS service provider (root name server operators excluded)", "Art 2(2)(a), Art 6(20)"),
    "domain-registrar": ("domain name registration services", "Art 2(4)"),
    "sole-provider": ("sole provider in a Member State of a service essential to societal or economic activities", "Art 2(2)(b)"),
    "disruption-impact": ("disruption could significantly affect public safety, security or health, or induce significant systemic risk", "Art 2(2)(c)-(d)"),
    "critical-importance": ("critical because of specific importance at national or regional level", "Art 2(2)(e)"),
    "critical-entity": ("identified as critical entity under Directive (EU) 2022/2557 (CER)", "Art 2(3), Art 3(1)(f)"),
    "public-admin-central": ("public administration entity of central government", "Art 2(2)(f)(i), Art 3(1)(d)"),
    "public-admin-regional": ("public administration entity at regional level", "Art 2(2)(f)(ii)"),
    "education": ("education institution carrying out critical research activities", "Art 2(5)(b)"),
    "designated-essential": ("designated essential by the Member State", "Art 3(1)(e)"),
    "ose-nis1": ("identified as operator of essential services under NIS1 before 16 January 2023", "Art 3(1)(g)"),
}
# Art 26(1)(b): these are supervised in the Member State of their main establishment.
MAIN_ESTABLISHMENT_SECTORS = {"digital-infrastructure", "ict-service-management", "digital-providers"}
YES = {"yes", "y", "true", "1"}
SEVERITY_ORDER = ["BLOCKER", "HIGH", "MEDIUM", "INFO"]

SAMPLE = """name,sector,employees,turnover_eur_m,balance_eur_m,special,member_states,main_establishment,dora_entity
Stadtwerke Nord GmbH,energy-electricity,420,180,210,critical-entity,DE,DE,no
CloudNest SaaS GmbH,digital-infrastructure,85,14,11,,DE AT FR,DE,no
OrthoParts Manufacturing,manufacturing-medical-devices,130,28,19,,DE,DE,no
TrustSign QTSP,digital-infrastructure,12,2,1,qtsp,DE NL,DE,no
Regionalbank Mitte AG,banking,900,310,4200,,DE,DE,yes
Kleine Praxis Software,health,18,3,2,,DE,DE,no
FreshFood Logistik,food,,,,,DE,DE,no
"""


def norm(v):
    return (v or "").strip()


def num(v, field, line):
    v = norm(v)
    if not v:
        return None
    try:
        x = float(v)
    except ValueError:
        raise ValueError(f"row {line} {field}: '{v}' is not a number")
    if x < 0:
        raise ValueError(f"row {line} {field}: must not be negative")
    return x


def size_class(staff, turnover, balance):
    """Return micro/small, medium, large or None if undeterminable."""
    if staff is None and (turnover is None or balance is None):
        return None, "no headcount and incomplete financials"
    if staff is not None and staff >= 250:
        return "large", "250 or more staff"
    if turnover is not None and balance is not None and turnover > 50 and balance > 43:
        return "large", "turnover > EUR 50m and balance sheet > EUR 43m"
    if staff is not None and staff >= 50:
        return "medium", "50-249 staff"
    if turnover is not None and balance is not None and turnover > 10 and balance > 10:
        return "medium", "turnover and balance sheet both > EUR 10m"
    if staff is None:
        return "small", "financials at or under the small ceilings (headcount not given: confirm it is under 50)"
    return "small", "under 50 staff and turnover or balance sheet at or under EUR 10m"


def classify(row, line):
    name = norm(row.get("name")) or f"row {line}"
    sector = norm(row.get("sector")).lower() or "none"
    specials = [s.strip().lower() for s in norm(row.get("special")).replace(",", ";").split(";") if s.strip()]
    findings = []

    def add(sev, code, msg, ref):
        findings.append({"severity": sev, "code": code, "message": msg, "ref": ref})

    out = {"name": name, "sector": sector, "annex": None, "size": None, "category": None,
           "basis": [], "supervision": None, "member_states": norm(row.get("member_states")).split(),
           "main_establishment": norm(row.get("main_establishment")), "findings": findings}
    if sector in ANNEX_I:
        out["annex"] = "I"
    elif sector in ANNEX_II:
        out["annex"] = "II"
    elif sector != "none":
        add("BLOCKER", "UNKNOWN_SECTOR", f"sector '{sector}' is not a key from --list-sectors; map it to an Annex I/II sector or 'none'", "Annex I, Annex II")
        out["category"] = "UNCLASSIFIED"
        return out
    for s in specials:
        if s not in SPECIAL:
            add("BLOCKER", "UNKNOWN_SPECIAL", f"special flag '{s}' is not a key from --list-special", "Art 2")
    if any(f["code"] == "UNKNOWN_SPECIAL" for f in findings):
        out["category"] = "UNCLASSIFIED"
        return out

    staff = num(row.get("employees"), "employees", line)
    turnover = num(row.get("turnover_eur_m"), "turnover_eur_m", line)
    balance = num(row.get("balance_eur_m"), "balance_eur_m", line)
    size, why = size_class(staff, turnover, balance)
    out["size"] = size

    size_independent = [s for s in specials if s not in {"domain-registrar", "public-admin-regional", "education", "ose-nis1"}]
    if size is None and not size_independent:
        add("BLOCKER", "SIZE_UNKNOWN", f"{why}: the size cap decides scope, so it cannot be skipped. Give headcount (FTE/AWU) and turnover and balance sheet, including partner and linked enterprises", "Art 2(1); Rec 2003/361/EC Annex Arts 2-6")
        out["category"] = "UNCLASSIFIED"
        return out
    out["basis"].append(f"size: {size or 'unknown'} ({why})")

    def basis(key):
        out["basis"].append(f"{SPECIAL[key][0]} ({SPECIAL[key][1]})")

    essential, important = [], []
    if "critical-entity" in specials:
        essential.append("Art 3(1)(f)"); basis("critical-entity")
    if "public-admin-central" in specials:
        essential.append("Art 3(1)(d)"); basis("public-admin-central")
    for k in ("qtsp", "tld-registry", "dns"):
        if k in specials:
            essential.append("Art 3(1)(b)"); basis(k)
    if "designated-essential" in specials:
        essential.append("Art 3(1)(e)"); basis("designated-essential")
    if "public-ecomms" in specials:
        basis("public-ecomms")
        if size == "large":
            essential.append("Art 3(1)(a)")
        elif size == "medium":
            essential.append("Art 3(1)(c)")
        else:
            important.append("Art 2(2)(a), Art 3(2)")
    if "tsp" in specials:
        basis("tsp")
        (essential if size == "large" else important).append("Art 3(1)(a)" if size == "large" else "Art 2(2)(a), Art 3(2)")
    for k in ("sole-provider", "disruption-impact", "critical-importance"):
        if k in specials:
            basis(k); important.append(f"{SPECIAL[k][1]}, Art 3(2) (or Art 3(1)(e) if the Member State designates it essential)")
    if out["annex"] and size in {"medium", "large"}:
        if out["annex"] == "I" and size == "large":
            essential.append("Art 3(1)(a)")
        else:
            important.append("Art 2(1), Art 3(2)")
    if "ose-nis1" in specials:
        basis("ose-nis1")
        add("MEDIUM", "OSE_NIS1", "former NIS1 operator of essential services: essential only if the Member State used the Art 3(1)(g) option; check national law", "Art 3(1)(g)")

    if essential:
        out["category"], out["basis"] = "ESSENTIAL", out["basis"] + [f"category: {', '.join(dict.fromkeys(essential))}"]
    elif important:
        out["category"], out["basis"] = "IMPORTANT", out["basis"] + [f"category: {', '.join(dict.fromkeys(important))}"]
    elif "domain-registrar" in specials:
        basis("domain-registrar")
        out["category"] = "LIMITED"
        add("MEDIUM", "REGISTRATION_DATA_ONLY", "domain name registration services: keep accurate, complete registration data, publish it and answer access requests within 72 hours; the rest of NIS2 does not apply on this ground", "Art 2(4), Art 28")
    elif "public-admin-regional" in specials or "education" in specials:
        for k in ("public-admin-regional", "education"):
            if k in specials:
                basis(k)
        out["category"] = "MS_OPTION"
        add("MEDIUM", "MEMBER_STATE_OPTION", "in scope only where the Member State's transposition includes it; read the national act", "Art 2(2)(f)(ii), Art 2(5)")
    else:
        out["category"] = "OUT"
        if out["annex"]:
            add("INFO", "BELOW_SIZE_CAP", f"Annex {out['annex']} sector but {size}: out unless a Member State designates it under Art 2(2)(b)-(e). Re-check when headcount or financials grow, and check whether customers in scope pass Art 21(2)(d) supply-chain clauses down to you", "Art 2(1), Art 2(2)")

    if norm(row.get("dora_entity")).lower() in YES and out["category"] in {"ESSENTIAL", "IMPORTANT"}:
        add("HIGH", "DORA_LEX_SPECIALIS", "DORA financial entity: DORA's ICT risk management and major-incident reporting replace NIS2 Arts 21 and 23. Run dora-readiness; the national NIS2 list and registration may still apply", "NIS2 Art 4, recital 28; DORA Art 1(2)")

    if out["category"] in {"ESSENTIAL", "IMPORTANT"}:
        ms = out["member_states"]
        if sector in MAIN_ESTABLISHMENT_SECTORS:
            main = out["main_establishment"]
            out["supervision"] = f"Member State of main establishment: {main or '?'} (Art 26(1)(b))"
            if not main:
                add("HIGH", "MAIN_ESTABLISHMENT_MISSING", "this sector is supervised where the main establishment is; record where cybersecurity risk-management decisions are taken", "Art 26(1)(b), 26(2)")
        elif "public-ecomms" in specials:
            out["supervision"] = f"each Member State where services are provided: {' '.join(ms) or '?'} (Art 26(1)(a))"
        else:
            out["supervision"] = f"each Member State where established: {' '.join(ms) or '?'} (Art 26(1))"
        out["regime"] = ("ex ante supervision (audits, on-site inspections, security scans), fines up to at least EUR 10m or 2% of worldwide turnover"
                         if out["category"] == "ESSENTIAL" else
                         "ex post supervision (after evidence of non-compliance), fines up to at least EUR 7m or 1.4% of worldwide turnover")
        out["regime_ref"] = "Arts 32, 34(4)" if out["category"] == "ESSENTIAL" else "Arts 33, 34(5)"
        add("HIGH", "REGISTER", "submit name, address, contacts, sector and Member States to the national authority and report changes within two weeks" +
            ("; digital infrastructure and digital providers also give IP ranges and main establishment for the ENISA registry (Art 27)" if sector in MAIN_ESTABLISHMENT_SECTORS else "") +
            ("; Germany: register with the BSI within three months of becoming an entity (BSIG section 33)" if "DE" in ms else ""),
            "Art 3(4), Art 27")
        add("INFO", "MANAGEMENT_ACCOUNTABLE", "management body approves the Art 21 measures, oversees them, can be held liable and must take training", "Art 20")
    return out


def run(text):
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows:
        raise ValueError("entity list has no rows")
    missing = {"name", "sector"} - set(rows[0].keys())
    if missing:
        raise ValueError(f"missing columns: {', '.join(sorted(missing))}")
    ents = [classify(r, i + 2) for i, r in enumerate(rows)]
    counts = {s: 0 for s in SEVERITY_ORDER}
    for e in ents:
        for f in e["findings"]:
            counts[f["severity"]] += 1
    cats = {}
    for e in ents:
        cats[e["category"]] = cats.get(e["category"], 0) + 1
    verdict = "BLOCKED" if counts["BLOCKER"] else "FINDINGS" if counts["HIGH"] or counts["MEDIUM"] else "CLEAR"
    return {"verdict": verdict, "summary": {"entities": len(ents), "categories": cats, "findings": counts}, "entities": ents}


def render(out):
    lines = [f"NIS2 scope: {out['verdict']}", ""]
    for e in out["entities"]:
        annex = f"Annex {e['annex']}" if e["annex"] else "no annex sector"
        lines.append(f"- {e['name']}: {e['category']}  [{e['sector']}, {annex}, size {e['size'] or '?'}]")
        for b in e["basis"]:
            lines.append(f"    {b}")
        if e.get("supervision"):
            lines.append(f"    supervised: {e['supervision']}")
            lines.append(f"    regime: {e['regime']} [{e['regime_ref']}]")
        for f in sorted(e["findings"], key=lambda f: SEVERITY_ORDER.index(f["severity"])):
            lines.append(f"    {f['severity']:<7} {f['code']}: {f['message']} [{f['ref']}]")
    s = out["summary"]
    lines += ["", f"{s['entities']} entities: " + ", ".join(f"{k} {v}" for k, v in s["categories"].items()),
              "Findings: " + ", ".join(f"{k} {v}" for k, v in s["findings"].items()),
              "Next: art21_gap_check.py for each in-scope entity; nis2_incident_clock.py when an incident is live."]
    return "\n".join(lines)


EXIT = {"CLEAR": 0, "FINDINGS": 2, "BLOCKED": 4}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clear, 2 findings, 3 invalid input, 4 cannot classify.")
    p.add_argument("--entities", help="entity CSV (columns in the module docstring)")
    p.add_argument("--list-sectors", action="store_true", help="print the Annex I/II sector keys")
    p.add_argument("--list-special", action="store_true", help="print the size-independent and other special flags")
    p.add_argument("--sample", action="store_true", help="run on a built-in example list")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    if a.list_sectors:
        for title, d in (("Annex I (high criticality)", ANNEX_I), ("Annex II (other critical)", ANNEX_II), ("", NONE_SECTOR)):
            if title:
                print(title)
            for k, v in d.items():
                print(f"  {k:<32} {v}")
        return 0
    if a.list_special:
        for k, (v, ref) in SPECIAL.items():
            print(f"  {k:<22} {v} [{ref}]")
        return 0
    try:
        if a.sample:
            text = SAMPLE
        else:
            if not a.entities:
                p.print_usage(sys.stderr)
                print("error: give --entities or --sample", file=sys.stderr)
                return 3
            with open(a.entities, newline="", encoding="utf-8-sig") as fh:
                text = fh.read()
        out = run(text)
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
