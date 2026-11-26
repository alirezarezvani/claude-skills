"""Shared loading for the metric-contracts scripts.

Reads metric definitions from two sources and normalises both into one record
per metric, so the lint and diff rules are written once:

1. dbt's ``target/semantic_manifest.json`` (written by ``dbt parse``). Both
   shapes are read: the legacy spec (measures on semantic models, simple
   metrics point at a measure through ``type_params.measure``) and the
   dbt 1.12 spec (simple metrics carry ``type_params.metric_aggregation_params``).
   Shapes verified against artifacts written by dbt-core 1.12.7 on 2026-11-26.
2. A plain contract file for any other tool (Cube, LookML, a BI tool, a
   spreadsheet): JSON, or YAML when PyYAML is installed. Schema in
   ``references/metric_contract_spec.md``.

Stdlib only. No network, no warehouse access.
"""
import json
import os

VERIFIED = "2026-11-26"
ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")
TYPES = {"simple", "ratio", "derived", "cumulative", "conversion"}
AGGS = {"sum", "count", "count_distinct", "average", "min", "max", "median", "percentile", "sum_boolean"}

# Fields whose change changes the numbers a metric returns. Anything else
# (description, label, owner, unit text) is cosmetic.
NUMERIC_FIELDS = ["type", "agg", "expr", "filter", "time_dimension", "relation", "numerator",
                  "denominator", "inputs", "non_additive", "window", "grain_to_date", "percentile",
                  "conversion", "fill_nulls_with", "join_to_timespine"]


class BadInput(Exception):
    pass


def asset(name):
    return os.path.normpath(os.path.join(ASSETS, name))


def _read(path):
    if not os.path.isfile(path):
        raise BadInput(f"{path}: file not found")
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if path.endswith((".yml", ".yaml")):
        try:
            import yaml  # optional
        except ImportError:
            raise BadInput(f"{path}: YAML input needs the optional PyYAML package; or pass the JSON form "
                           "(for dbt, target/semantic_manifest.json from `dbt parse`)")
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise BadInput(f"{path}: not valid YAML: {e}")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise BadInput(f"{path}: not valid JSON: {e}")


def _filters(raw):
    """Return a sorted tuple of filter strings from any of the shapes in use."""
    if raw is None or raw == "":
        return ()
    if isinstance(raw, str):
        return (" ".join(raw.split()),)
    if isinstance(raw, dict):
        wf = raw.get("where_filters")
        if wf is not None:
            return tuple(sorted(" ".join(str(w.get("where_sql_template", "")).split()) for w in wf))
        if "where_sql_template" in raw:
            return (" ".join(str(raw["where_sql_template"]).split()),)
    if isinstance(raw, list):
        out = []
        for item in raw:
            out.extend(_filters(item))
        return tuple(sorted(out))
    return (" ".join(str(raw).split()),)


def _ref(raw):
    """A metric input: name, filter, alias, offset. Accepts a bare string."""
    if raw is None:
        return None
    if isinstance(raw, str):
        return {"name": raw, "filter": (), "alias": None, "offset": None}
    if not isinstance(raw, dict) or not raw.get("name"):
        return None
    offs = {k: raw.get(k) for k in ("offset_window", "offset_to_grain", "offset") if raw.get(k) is not None}
    return {"name": raw["name"], "filter": _filters(raw.get("filter")), "alias": raw.get("alias"),
            "offset": json.dumps(offs, sort_keys=True, default=str) if offs else None}


def _meta(m):
    meta = {}
    for src in (m.get("meta"), (m.get("config") or {}).get("meta")):
        if isinstance(src, dict):
            meta.update(src)
    return meta


def _record(**kw):
    rec = {f: None for f in NUMERIC_FIELDS}
    rec.update({"name": None, "description": "", "label": None, "owner": None, "version": None,
                "unit": None, "consumers": [], "semantic_model": None, "measure": None, "source": None})
    rec.update(kw)
    rec["filter"] = tuple(rec["filter"] or ())
    rec["inputs"] = rec["inputs"] or []
    return rec


def _from_dbt(doc, source):
    models, measures = {}, {}
    for sm in doc.get("semantic_models") or []:
        rel = (sm.get("node_relation") or {}).get("relation_name")
        default_time = (sm.get("defaults") or {}).get("agg_time_dimension")
        models[sm.get("name")] = {"relation": rel, "time": default_time,
                                  "entities": {e.get("expr") or e.get("name"): e.get("type")
                                               for e in sm.get("entities") or []}}
        for ms in sm.get("measures") or []:
            measures[ms.get("name")] = dict(ms, _model=sm.get("name"))
    out = []
    for m in doc.get("metrics") or []:
        tp = m.get("type_params") or {}
        meta = _meta(m)
        rec = dict(name=m.get("name"), type=m.get("type"), description=m.get("description") or "",
                   label=m.get("label"), owner=meta.get("owner"), version=meta.get("version"),
                   unit=meta.get("unit"), source=source, filter=_filters(m.get("filter")),
                   window=json.dumps(tp.get("window"), sort_keys=True) if tp.get("window") else None,
                   grain_to_date=tp.get("grain_to_date"), fill_nulls_with=tp.get("fill_nulls_with"),
                   join_to_timespine=tp.get("join_to_timespine") or None)
        map_ = tp.get("metric_aggregation_params")
        meas = tp.get("measure")
        if map_:  # dbt 1.12 simple metric
            smn = map_.get("semantic_model")
            nad = map_.get("non_additive_dimension")
            pct = (map_.get("agg_params") or {}).get("percentile")
            rec.update(agg=map_.get("agg"), expr=tp.get("expr") or m.get("name"), semantic_model=smn,
                       time_dimension=map_.get("agg_time_dimension") or models.get(smn, {}).get("time"),
                       non_additive=(nad or {}).get("name"), percentile=pct)
        elif meas:  # legacy spec: resolve through the measure
            ref = _ref(meas)
            ms = measures.get(ref["name"]) if ref else None
            rec["measure"] = ref["name"] if ref else None
            rec["filter"] = tuple(sorted(rec["filter"] + (ref["filter"] if ref else ())))
            if not ms and ref:
                # keep the dangling name in the signature so a change to it is still a change (lint MC03 flags it)
                rec["expr"] = f"<unresolved measure {ref['name']}>"
            if ms:
                smn = ms["_model"]
                nad = ms.get("non_additive_dimension")
                rec.update(agg=ms.get("agg"), expr=ms.get("expr") or ms.get("name"), semantic_model=smn,
                           time_dimension=ms.get("agg_time_dimension") or models.get(smn, {}).get("time"),
                           non_additive=(nad or {}).get("name"),
                           percentile=(ms.get("agg_params") or {}).get("percentile"))
            if isinstance(meas, dict):
                if meas.get("fill_nulls_with") is not None:
                    rec["fill_nulls_with"] = meas["fill_nulls_with"]
                if meas.get("join_to_timespine"):
                    rec["join_to_timespine"] = True
        else:
            rec["expr"] = tp.get("expr")
        rec["numerator"] = _ref(tp.get("numerator"))
        rec["denominator"] = _ref(tp.get("denominator"))
        inputs = [_ref(x) for x in tp.get("metrics") or []]
        cum = tp.get("cumulative_type_params") or {}
        if cum.get("metric"):
            inputs.append(_ref(cum["metric"]))
            if cum.get("window"):
                rec["window"] = json.dumps(cum["window"], sort_keys=True)
            rec["grain_to_date"] = cum.get("grain_to_date") or rec["grain_to_date"]
        conv = tp.get("conversion_type_params")
        if conv:
            rec["conversion"] = json.dumps(conv, sort_keys=True, default=str)
            for k in ("base_metric", "conversion_metric"):
                if conv.get(k):
                    inputs.append(_ref(conv[k]))
        rec["inputs"] = [x for x in inputs if x]
        if rec.get("semantic_model"):
            rec["relation"] = models.get(rec["semantic_model"], {}).get("relation")
        out.append(_record(**rec))
    return out, models, set(measures)


def _from_contract(doc, source):
    out = []
    for m in doc.get("metrics") or []:
        if not isinstance(m, dict):
            raise BadInput(f"{source}: every entry under metrics must be an object")
        rec = dict(name=m.get("name"), type=m.get("type", "simple"), description=m.get("description") or "",
                   label=m.get("label"), owner=m.get("owner"), version=m.get("version"), unit=m.get("unit"),
                   agg=m.get("agg"), expr=m.get("expr"), filter=_filters(m.get("filter")),
                   time_dimension=m.get("time_dimension"), relation=m.get("source_table"),
                   semantic_model=m.get("source_table"),
                   numerator=_ref(m.get("numerator")), denominator=_ref(m.get("denominator")),
                   inputs=[x for x in (_ref(i) for i in m.get("inputs") or []) if x],
                   non_additive=m.get("non_additive_dimension"), window=m.get("window"),
                   grain_to_date=m.get("grain_to_date"), percentile=m.get("percentile"),
                   consumers=list(m.get("consumers") or []), source=source)
        out.append(_record(**rec))
    return out, {}, set()


def load(path):
    """Return (metrics, semantic_models, measure_names, kind) for one file."""
    doc = _read(path)
    if not isinstance(doc, dict):
        raise BadInput(f"{path}: expected a JSON/YAML object at the top level")
    try:
        if "semantic_models" in doc or "project_configuration" in doc:
            mets, models, meas = _from_dbt(doc, path)
            kind = "dbt-semantic-manifest"
        elif "metrics" in doc:
            mets, models, meas = _from_contract(doc, path)
            kind = "contract"
        else:
            mets = None
    except (AttributeError, TypeError, KeyError) as e:
        raise BadInput(f"{path}: unexpected structure ({type(e).__name__}: {e}); is this an unmodified "
                       "semantic_manifest.json or a contract file?")
    if mets is None and "nodes" in doc and "exposures" in doc:
        raise BadInput(f"{path}: this is target/manifest.json; pass target/semantic_manifest.json "
                       "(pass manifest.json to metric_diff.py --manifest for exposures)")
    if mets is None:
        raise BadInput(f"{path}: no 'metrics' or 'semantic_models' key; not a metric definition file")
    for r in mets:
        if not r["name"]:
            raise BadInput(f"{path}: a metric has no name")
    return mets, models, meas, kind


def load_many(paths):
    metrics, models, measures, kinds = [], {}, set(), set()
    for p in paths:
        m, sm, ms, k = load(p)
        metrics += m
        models.update(sm)
        measures |= ms
        kinds.add(k)
    return metrics, models, measures, kinds


def signature(rec):
    """The fields that decide what number the metric returns, as a comparable value."""
    sig = {f: rec.get(f) for f in NUMERIC_FIELDS}
    if sig.get("inputs"):  # a derived metric's expr names its inputs, so their order cannot change the number
        sig["inputs"] = sorted(sig["inputs"], key=lambda r: json.dumps(r, sort_keys=True, default=str))
    return json.dumps(sig, sort_keys=True,
                      default=lambda o: sorted(o, key=str) if isinstance(o, (set, frozenset)) else str(o))


def refs(rec):
    """Names of the metrics this metric is computed from."""
    names = [r["name"] for r in (rec.get("numerator"), rec.get("denominator")) if r]
    return names + [r["name"] for r in rec.get("inputs") or []]


def load_exposures(path):
    """Map metric name -> [consumer labels] from a dbt manifest.json (or a trimmed copy)."""
    doc = _read(path)
    exposures = doc.get("exposures") if isinstance(doc, dict) else None
    if not isinstance(exposures, dict):
        raise BadInput(f"{path}: no 'exposures' object; pass dbt's target/manifest.json")
    out = {}
    for ex in exposures.values():
        if not isinstance(ex, dict):
            raise BadInput(f"{path}: an exposure is not an object")
        owner = ex.get("owner") or {}
        who = owner.get("name") or owner.get("email") or "no owner"
        label = f"{ex.get('type', 'exposure')} {ex.get('name')} ({who})"
        for node in (ex.get("depends_on") or {}).get("nodes") or []:
            if node.startswith("metric."):
                out.setdefault(node.split(".")[-1], []).append(label)
    return out


def emit(result, fmt, render):
    if fmt == "json":
        print(json.dumps(result, indent=2, default=list))
    else:
        print(render(result))
