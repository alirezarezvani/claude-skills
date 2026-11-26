#!/usr/bin/env python3
"""provider_adapter.py — map a shots.v1 manifest onto one generation provider's tools.

Reads the provider-neutral manifest from shot_manifest.py, an adapter file
(adapters/<provider>.json: which tool quotes, which generates, which polls,
how parameters are named) and the model's own constraints as the provider's
catalog returned them at run time (--model-spec, the saved output of the
catalog's "get" call). It writes requests.v1: one quote call and one generate
call per shot, with the duration snapped to what the model accepts, the
aspect checked, keyframes mapped to the model's media roles, and the prompt
assembled from the shot prompt, the camera intent and the negative.

It calls nothing. Model ids, durations and aspect ratios come from the spec
you pass, never from this file, because provider catalogs change weekly.

Exit codes: 0 requests written, 2 bad input, 3 missing model spec (prints the
catalog call to make), 4 a shot cannot be generated with this model.

Examples:
  provider_adapter.py --list
  provider_adapter.py --sample
  provider_adapter.py --shots film/shots.json --adapter higgsfield --model magi_2 \\
      --model-spec film/model_magi_2.json --out film/requests.json
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

ADAPTER_DIR = Path(__file__).resolve().parent.parent / "adapters"

SAMPLE_SHOTS = {
    "schema": "shots.v1", "title": "Release 2.0 teaser", "canvas": [1080, 1080], "fps": 30,
    "upgrade_shots": 2, "generated_seconds": 6.5, "motion_only_shots": 3,
    "shots": [
        {"id": "s2", "start": 3.0, "duration": 4.0, "aspect_ratio": "1:1",
         "prompt": "Slow dolly across a dark desk, laptop screen glowing blue, shallow depth of field",
         "camera_intent": "moderate slow dolly push-in over 4s, ease in out",
         "start_image": "film/keyframes/s2_first.png", "end_image": "film/keyframes/s2_last.png",
         "conditioning": "first+last keyframe", "vo": "", "code_overlays": ["text"],
         "negative": "no on-screen text, no captions, no logos, no watermarks", "status": "needs-quote"},
        {"id": "s4", "start": 9.0, "duration": 2.5, "aspect_ratio": "1:1",
         "prompt": "Server room aisle, cool light, slow drift", "camera_intent": "subtle gentle handheld-style drift over 2.5s, ease in out",
         "start_image": None, "end_image": None, "conditioning": "text only", "vo": "", "code_overlays": [],
         "negative": "no on-screen text, no captions, no logos, no watermarks", "status": "needs-quote"},
    ],
}
SAMPLE_SPEC = {
    "id": "magi_2", "output_type": "video",
    "parameters": [{"name": "duration", "type": "number", "min": 4, "max": 30, "default": 5},
                   {"name": "generate_audio", "type": "bool", "default": True}],
    "medias": [{"name": "medias", "roles": ["start_image", "end_image", "image_references"]}],
    "aspect_ratios": ["21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
}


class AdapterError(Exception):
    pass


def load_adapter(name: str) -> dict:
    path = Path(name) if name.endswith(".json") else ADAPTER_DIR / f"{name}.json"
    if not path.exists():
        raise AdapterError(f"no adapter {name!r}; available: {', '.join(list_adapters())}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") != "adapter.v1" or not data.get("tools", {}).get("generate"):
        raise AdapterError(f"{path} is not an adapter.v1 file with a generate tool")
    return data


def list_adapters() -> list[str]:
    return sorted(p.stem for p in ADAPTER_DIR.glob("*.json") if p.stem != "template")


def unwrap_spec(raw) -> dict:
    """Accept the bare model object, {"item": {...}}, {"model": {...}} or {"items": [one]}."""
    if isinstance(raw, dict):
        for key in ("item", "model"):
            if isinstance(raw.get(key), dict):
                return raw[key]
        if isinstance(raw.get("items"), list) and len(raw["items"]) == 1:
            return raw["items"][0]
        return raw
    raise AdapterError("model spec must be a JSON object")


def duration_rule(spec: dict) -> dict:
    """Return {'allowed': [..]} or {'min': a, 'max': b} from whichever shape the catalog used."""
    if isinstance(spec.get("durations"), list) and spec["durations"]:
        return {"allowed": sorted(float(d) for d in spec["durations"])}
    if isinstance(spec.get("duration_range"), dict):
        r = spec["duration_range"]
        return {"min": float(r.get("min", 0)), "max": float(r.get("max", 1e9))}
    for p in spec.get("parameters", []):
        if p.get("name") == "duration":
            if p.get("options"):
                return {"allowed": sorted(float(o) for o in p["options"])}
            return {"min": float(p.get("min", 0)), "max": float(p.get("max", 1e9))}
    return {}


def snap_duration(need: float, rule: dict, integer: bool) -> tuple[float | None, str | None]:
    if "allowed" in rule:
        fits = [d for d in rule["allowed"] if d + 1e-6 >= need]
        if not fits:
            return None, f"needs {need:g}s but the model's longest clip is {rule['allowed'][-1]:g}s"
        return fits[0], None
    want = math.ceil(need - 1e-6) if integer else need
    lo, hi = rule.get("min", 0.0), rule.get("max", 1e9)
    if want > hi + 1e-6:
        return None, f"needs {need:g}s but the model's longest clip is {hi:g}s"
    return max(want, lo), None


def media_roles(spec: dict) -> set[str]:
    roles: set[str] = set()
    for m in spec.get("medias", []):
        roles.update(m.get("roles", []))
    return roles


def silent_param(spec: dict, adapter: dict) -> dict:
    names = {p.get("name"): p for p in spec.get("parameters", [])}
    for cand in adapter["params"].get("silent", []):
        p = names.get(cand["name"])
        if p is None:
            continue
        opts = p.get("options")
        if opts is None or cand["value"] in opts:
            if isinstance(cand["value"], bool) and p.get("type") not in (None, "bool"):
                continue
            return {cand["name"]: cand["value"]}
    return {}


def build(shots: dict, adapter: dict, model: str, spec: dict) -> tuple[dict, list[str]]:
    pm = adapter["params"]
    rule = duration_rule(spec)
    roles = media_roles(spec)
    aspects = spec.get("aspect_ratios") or []
    silent = silent_param(spec, adapter)
    blockers, requests = [], []
    for s in shots.get("shots", []):
        warnings = []
        aspect = s["aspect_ratio"]
        if aspects and aspect not in aspects:
            blockers.append(f"{s['id']}: model {model} has no {aspect} output (it offers {', '.join(aspects)})")
            continue
        gen_d, why = snap_duration(float(s["duration"]), rule, adapter.get("duration_integer", True))
        if gen_d is None:
            blockers.append(f"{s['id']}: {why}; split the shot or pick a model with longer clips")
            continue
        extra = round(gen_d - float(s["duration"]), 3)
        if extra > 0:
            warnings.append(f"generates {gen_d:g}s for a {s['duration']:g}s shot; {extra:g}s is paid for and trimmed")
        prompt = (s.get("prompt") or "").strip().rstrip(".")
        if not prompt:
            blockers.append(f"{s['id']}: empty upgrade_prompt; write one in the scene before quoting")
            continue
        text = f"{prompt}. Camera: {s['camera_intent']}. {s['negative'].capitalize()}."
        params = {pm["model"]: model, pm["prompt"]: text, pm["duration"]: int(gen_d) if gen_d.is_integer() else gen_d,
                  pm["aspect_ratio"]: aspect}
        params.update(silent)
        uploads, medias = [], []
        for edge, role_key in (("start_image", "media_role_start"), ("end_image", "media_role_end")):
            path, role = s.get(edge), pm.get(role_key)
            if not path:
                continue
            if not role or role not in roles or not pm.get("media_list"):
                warnings.append(f"model {model} takes no {edge}; the keyframe is not sent")
                continue
            uploads.append({"role": role, "path": path})
            medias.append({"role": role, "value": f"<media_id:{role}>"})
        if medias:
            if any(m["role"] == pm.get("media_role_end") for m in medias) and \
                    not any(m["role"] == pm.get("media_role_start") for m in medias):
                warnings.append("an end keyframe without a start keyframe is refused by many models")
            params[pm["media_list"]] = medias
        if not uploads and s.get("conditioning") == "text only":
            warnings.append("text-only shot: framing will not match the animatic; drift_check can only check duration and aspect")
        quote_tool = adapter["tools"].get("quote")
        gen_params = (adapter.get("generate_from_quote") or {}).get("params") if quote_tool else None
        requests.append({
            "id": s["id"],
            "shot_duration": float(s["duration"]),
            "generated_duration": gen_d,
            "billed_extra_s": extra,
            "trim_to": float(s["duration"]),
            "uploads": uploads,
            "quote": {"tool": quote_tool, "params": params} if quote_tool else None,
            "generate": {"tool": adapter["tools"]["generate"], "params": gen_params or params},
            "warnings": warnings,
            "status": "needs-quote",
        })
    return {
        "schema": "requests.v1",
        "title": shots.get("title"),
        "provider": adapter["provider"],
        "adapter_verified_on": adapter.get("verified_on"),
        "model": model,
        "tools": adapter["tools"],
        "tool_match": adapter.get("tool_match", "suffix"),
        "rules": adapter.get("rules", []),
        "data_flow": adapter.get("data_flow"),
        "generated_seconds": round(sum(r["generated_duration"] for r in requests), 3),
        "billed_extra_seconds": round(sum(r["billed_extra_s"] for r in requests), 3),
        "requests": requests,
        "next": "confirm every tool name exists in your tool list; upload keyframes and put the media ids in; "
                "call the quote tool per request (free); save {id: {credits, quote_ref}} to quotes.json; "
                "run budget_gate.py quote",
    }, blockers


def main() -> int:
    ap = argparse.ArgumentParser(description="Map shots.v1 onto a provider adapter and a run-time model spec (requests.v1).")
    ap.add_argument("--shots", help="shots.v1 JSON from shot_manifest.py.")
    ap.add_argument("--adapter", default="higgsfield", help="Adapter name in adapters/ or a path to an adapter.v1 JSON.")
    ap.add_argument("--model", help="Model id the user picked from the provider's catalog.")
    ap.add_argument("--model-spec", help="Saved output of the provider's catalog 'get' call for that model.")
    ap.add_argument("--out", help="Write requests.v1 here.")
    ap.add_argument("--list", action="store_true", help="List the adapters and exit.")
    ap.add_argument("--sample", action="store_true", help="Run on a built-in manifest and model spec.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()

    if args.list:
        for name in list_adapters():
            a = load_adapter(name)
            print(f"{name:12} verified {a.get('verified_on')}  quote={a['tools'].get('quote')}  generate={a['tools']['generate']}")
        return 0
    try:
        adapter = load_adapter(args.adapter)
        if args.sample:
            shots, spec, model = SAMPLE_SHOTS, SAMPLE_SPEC, "magi_2"
        else:
            if not args.shots or not args.model:
                raise AdapterError("--shots and --model are required (or --sample)")
            shots = json.loads(Path(args.shots).read_text(encoding="utf-8"))
            if shots.get("schema") != "shots.v1":
                raise AdapterError("--shots must be a shots.v1 file from shot_manifest.py")
            model = args.model
            if not args.model_spec:
                get = json.dumps(adapter.get("catalog_get") or {}).replace("<model>", model)
                print(f"need the model's constraints from the provider, read at run time: call "
                      f"{adapter['tools'].get('catalog')} with {get}, save the result, pass it as --model-spec",
                      file=sys.stderr)
                return 3
            spec = unwrap_spec(json.loads(Path(args.model_spec).read_text(encoding="utf-8")))
            if spec.get("id") and spec["id"] != model:
                raise AdapterError(f"--model-spec describes {spec['id']!r}, not {model!r}")
    except (AdapterError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        result, blockers = build(shots, adapter, model, spec)
    except (KeyError, TypeError, ValueError) as exc:
        print(f"error: the shots file or model spec is missing or has a bad field: {exc!r}", file=sys.stderr)
        return 2
    if blockers:
        for b in blockers:
            print(f"BLOCKED {b}", file=sys.stderr)
        return 4
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(result, indent=2), encoding="utf-8")
    if args.output == "json":
        print(json.dumps(result, indent=2))
    else:
        print(f"{result['provider']} / {model}: {len(result['requests'])} request(s), "
              f"{result['generated_seconds']:g}s generated ({result['billed_extra_seconds']:g}s paid and trimmed)")
        for r in result["requests"]:
            print(f"  {r['id']:>6}  {r['shot_duration']:g}s -> {r['generated_duration']:g}s  uploads={len(r['uploads'])}")
            for w in r["warnings"]:
                print(f"{'':10}note: {w}")
        print(f"next: {result['next']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
