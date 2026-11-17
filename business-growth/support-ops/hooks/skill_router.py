#!/usr/bin/env python3
"""Skill router: a UserPromptSubmit hook that points the model at a skill.

Why this exists: the 2026-11 trigger evals found skills that never fire on
prompts squarely inside their scope. On those prompts no other skill fired
either; the model answered directly. Two rounds of description rewrites did
not move them, so wording is not the lever. This hook is.

What it does: matches the user's prompt against hand-written, high-precision
patterns in skill_routes.json (next to this file). On a match it adds one line
of context naming the skill; on no match it prints nothing. It never blocks a
prompt and never calls a model.

Noise rules:
  * at most one skill per plugin per prompt (highest score wins)
  * each skill is suggested at most once per session
  * prompts that start with "/" are skipped (the user picked a command)
  * fails open: any error means no output, exit 0

Disable with SKILL_ROUTER=0 (all plugins) or SKILL_ROUTER_<PLUGIN>=0, where
<PLUGIN> is the plugin name upper-cased with "-" as "_".

Every plugin that ships this hook carries an identical copy of this file;
scripts/check_skill_router.py keeps the copies in sync.
"""
from __future__ import annotations

import json
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROUTES = os.path.join(HERE, "skill_routes.json")
HEAD_TAIL = 1500  # long pastes: look only at the start and the end


def _compile(patterns):
    return [re.compile(p, re.I) for p in patterns or []]


def load_routes(path=ROUTES):
    with open(path, encoding="utf-8") as fh:
        cfg = json.load(fh)
    routes = []
    for r in cfg["routes"]:
        routes.append({
            "skill": r["skill"],
            "why": r["why"],
            "any": _compile(r.get("any")),
            "pairs": [(_compile(a), _compile(b)) for a, b in r.get("pairs", [])],
            "not": _compile(r.get("not")),
        })
    return cfg["plugin"], routes


def _hit(regexes, text):
    return any(rx.search(text) for rx in regexes)


def score(route, text):
    if _hit(route["not"], text):
        return 0
    s = sum(1 for rx in route["any"] if rx.search(text))
    s += sum(1 for a, b in route["pairs"] if _hit(a, text) and _hit(b, text))
    return s


def best_route(routes, prompt):
    text = prompt if len(prompt) <= 2 * HEAD_TAIL else prompt[:HEAD_TAIL] + "\n" + prompt[-HEAD_TAIL:]
    best, best_s = None, 0
    for r in routes:
        s = score(r, text)
        if s > best_s:
            best, best_s = r, s
    return best


def _state_file(session_id, plugin):
    safe = re.sub(r"[^A-Za-z0-9_-]", "", session_id or "nosession")[:80]
    d = os.path.join(tempfile.gettempdir(), "claude-skill-router")
    os.makedirs(d, mode=0o700, exist_ok=True)
    return os.path.join(d, f"{safe}-{plugin}.json")


def already_suggested(session_id, plugin, skill):
    """Record the suggestion; return True if this session already had it."""
    try:
        path = _state_file(session_id, plugin)
        seen = []
        if os.path.exists(path):
            with open(path, encoding="utf-8") as fh:
                seen = json.load(fh)
        if skill in seen:
            return True
        seen.append(skill)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(seen, fh)
    except Exception:
        pass
    return False


def main():
    if os.environ.get("SKILL_ROUTER", "1") == "0":
        return 0
    try:
        data = json.load(sys.stdin)
        plugin, routes = load_routes()
    except Exception:
        return 0
    if os.environ.get("SKILL_ROUTER_" + plugin.upper().replace("-", "_"), "1") == "0":
        return 0
    prompt = (data.get("prompt") or "").strip()
    if not prompt or prompt.startswith("/"):
        return 0
    route = best_route(routes, prompt)
    if route is None:
        return 0
    if already_suggested(data.get("session_id", ""), plugin, route["skill"]):
        return 0
    name = f"{plugin}:{route['skill']}"
    msg = (f"Skill hint ({plugin} plugin): this request fits the `{name}` skill "
           f"({route['why']}). Load it with the Skill tool first, before you answer or ask "
           f"for missing input, unless the request is outside that scope or a more specific "
           f"skill fits better.")
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit", "additionalContext": msg}}))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        sys.exit(0)
