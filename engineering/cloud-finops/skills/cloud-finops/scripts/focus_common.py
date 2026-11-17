"""Shared FOCUS loading and the sample dataset for the cloud-finops scripts.

FOCUS (FinOps Open Cost and Usage Specification) is the open billing-data
format that AWS, Microsoft Azure, Google Cloud and Oracle Cloud export. Column
names follow FOCUS 1.x (verified against v1.4 on 2026-11-17). Stdlib only.
"""
import csv
import datetime as dt
import io
import json
import random

RULES_VERIFIED = "2026-11-17"
NEEDED = ["BilledCost", "EffectiveCost", "ListCost", "ChargeCategory", "ChargePeriodStart", "BillingCurrency"]


def num(v):
    v = (v or "").strip()
    if not v:
        return 0.0
    return float(v)


def parse_tags(raw):
    raw = (raw or "").strip()
    if not raw:
        return {}
    try:
        val = json.loads(raw)
    except json.JSONDecodeError:
        # tolerate key=value;key=value exports
        out = {}
        for part in raw.replace(",", ";").split(";"):
            if "=" in part:
                k, v = part.split("=", 1)
                out[k.strip()] = v.strip()
        return out
    return {str(k): ("" if v is None else str(v)) for k, v in val.items()} if isinstance(val, dict) else {}


def day(raw):
    raw = (raw or "").strip()
    if not raw:
        raise ValueError("empty ChargePeriodStart")
    return dt.date.fromisoformat(raw[:10])


def load(text, need=NEEDED):
    reader = csv.DictReader(io.StringIO(text))
    cols = reader.fieldnames or []
    missing = [c for c in need if c not in cols]
    if missing:
        raise ValueError("not a FOCUS export, missing column(s): " + ", ".join(missing))
    rows = []
    for i, r in enumerate(reader, 2):
        try:
            for c in ("BilledCost", "EffectiveCost", "ListCost", "ContractedCost"):
                if c in r:
                    r[c] = num(r[c])
            r["_day"] = day(r.get("ChargePeriodStart"))
        except ValueError as exc:
            raise ValueError(f"row {i}: {exc}")
        r["_tags"] = parse_tags(r.get("Tags"))
        rows.append(r)
    if not rows:
        raise ValueError("no rows")
    currencies = {r.get("BillingCurrency") for r in rows}
    if len(currencies) > 1:
        raise ValueError(f"mixed billing currencies {sorted(currencies)}; split the export per currency")
    return rows


def read_input(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def sample_csv(days=28, seed=7, spike_day=24):
    """Deterministic synthetic FOCUS export: compute with a savings plan, storage, a database, untagged items and one spike."""
    rng = random.Random(seed)
    start = dt.date(2026, 10, 1)
    cols = ["ChargePeriodStart", "BillingCurrency", "ChargeCategory", "ServiceCategory", "ServiceName", "SubAccountName",
            "ResourceId", "PricingCategory", "CommitmentDiscountId", "CommitmentDiscountStatus",
            "ListCost", "BilledCost", "EffectiveCost", "Tags"]
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(cols)
    tags_ok = json.dumps({"team": "checkout", "env": "prod", "cost-center": "CC-410"})
    tags_case = json.dumps({"team": "Checkout", "env": "Prod"})
    sp = "arn:aws:savingsplans::111:savingsplan/sp-1"
    for d in range(days):
        date = (start + dt.timedelta(days=d)).isoformat() + "T00:00:00Z"
        weekend = (start + dt.timedelta(days=d)).weekday() >= 5
        load = 0.75 if weekend else 1.0
        # compute: 24 instance-hours/day; 18 covered by the savings plan on weekdays, fewer on weekends
        covered = 18 if not weekend else 14
        w.writerow([date, "USD", "Usage", "Compute", "Amazon EC2", "prod", "i-0a1", "Committed", sp, "Used",
                    round(covered * 4.0, 2), 0, round(covered * 2.6, 2), tags_ok])
        if covered < 18:
            w.writerow([date, "USD", "Usage", "Compute", "Amazon EC2", "prod", "", "Committed", sp, "Unused",
                        0, 0, round((18 - covered) * 2.6, 2), ""])
        od = round(rng.uniform(5, 8) * 4.0 * load, 2)
        w.writerow([date, "USD", "Usage", "Compute", "Amazon EC2", "prod", "i-0b2", "Standard", "", "", od, od, od, tags_case])
        db = round(310 * load + rng.uniform(-10, 10), 2)
        w.writerow([date, "USD", "Usage", "Databases", "Amazon RDS", "prod", "db-main", "Standard", "", "", db, db, db, tags_ok])
        st = round(95 + d * 0.8 + rng.uniform(-3, 3), 2)
        w.writerow([date, "USD", "Usage", "Storage", "Amazon S3", "shared", "logs-bucket", "Standard", "", "", st, st, st, ""])
        nat = round(42 + rng.uniform(-4, 4), 2)
        if d == spike_day:
            nat = round(nat * 6.5, 2)
        w.writerow([date, "USD", "Usage", "Networking", "Amazon VPC", "prod", "nat-0c3", "Standard", "", "", nat, nat, nat, ""])
        if d == 0:
            w.writerow([date, "USD", "Purchase", "Compute", "Savings Plans for AWS Compute usage", "prod", "", "Committed", sp, "",
                        0, round(18 * 2.6 * days, 2), 0, ""])
    return out.getvalue()
