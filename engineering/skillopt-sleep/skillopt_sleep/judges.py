"""SkillOpt-Sleep — rule-based judges (gbrain-evals compatible).

Implements the programmatic check operators used by gbrain-evals'
skillopt-v1 benchmark so we can score skill outputs locally, with NO judge
API call:

  * section_present <name>   — a markdown heading containing <name> exists
  * regex <pattern>          — the pattern matches the response
  * max_chars <n>            — response length <= n
  * min_chars <n>            — response length >= n
  * contains <text>          — substring present (case-insensitive)
  * tool_called <name>       — a tool with <name> was invoked (needs a tool loop;
                               in single-shot replay we approximate via an
                               explicit "TOOL_CALL: <name>" marker the agent emits)

A task whose judge is {"kind": "rule", "checks": [...]} passes (hard=1.0) iff
ALL checks pass; soft = fraction of checks passed. This mirrors gbrain's
all-checks-must-pass rule scoring and gives the gate a smooth signal.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


def _section_present(response: str, name: str) -> bool:
    # a markdown heading line (#, ##, ...) or bold line that contains `name`
    pat = re.compile(
        r"(?im)^\s{0,3}(#{1,6}\s*.*%s|\*\*.*%s.*\*\*\s*:?)\s*$" % (re.escape(name), re.escape(name))
    )
    if pat.search(response or ""):
        return True
    # also accept "Name:" style label at line start
    label = re.compile(r"(?im)^\s*%s\s*:" % re.escape(name))
    return bool(label.search(response or ""))


def _check(op: str, arg: Any, response: str, tools_called: List[str]) -> bool:
    r = response or ""
    if op == "section_present":
        return _section_present(r, str(arg))
    if op == "regex":
        try:
            return bool(re.search(str(arg), r))
        except re.error:
            return False
    if op == "max_chars":
        return len(r) <= int(arg)
    if op == "min_chars":
        return len(r) >= int(arg)
    if op == "contains":
        return str(arg).lower() in r.lower()
    if op == "tool_called":
        name = str(arg).lower()
        if any(name == t.lower() for t in tools_called):
            return True
        # single-shot approximation: the agent emits an explicit marker
        return bool(re.search(r"(?i)\btool_call\s*:\s*%s\b" % re.escape(name), r))
    # unknown op: do not block
    return True


def score_rule_judge(
    judge: Dict[str, Any],
    response: str,
    tools_called: List[str] | None = None,
) -> Tuple[float, float, str]:
    """Return (hard, soft, rationale) for a gbrain-style rule judge."""
    checks = (judge or {}).get("checks", []) or []
    if not checks:
        return 0.0, 0.0, "no checks"
    tools_called = tools_called or []
    passed = 0
    failed_desc: List[str] = []
    for c in checks:
        ok = _check(c.get("op", ""), c.get("arg"), response, tools_called)
        if ok:
            passed += 1
        else:
            failed_desc.append(f"{c.get('op')}={c.get('arg')}")
    soft = passed / len(checks)
    hard = 1.0 if passed == len(checks) else 0.0
    rationale = "all checks passed" if hard else "failed: " + ", ".join(failed_desc)
    return hard, soft, rationale
