#!/usr/bin/env python3
"""Audit a rendered-page snapshot for defects that only show up in the browser: contrast, target size, focus, clipping and reflow.

Source linters guess at what the page will look like; this reads what it did
look like. The input is a JSON snapshot taken by assets/collect_snapshot.js
(DevTools console) or assets/capture_snapshot.mjs (Playwright, with a real
keyboard focus pass), so contrast is measured on the actual background, targets
on their actual box, and focus on the actual focused style.

Findings (WCAG 2.2 Level AA unless noted)
  TEXT_CONTRAST         text below 4.5:1, or 3:1 for large text (1.4.3)                       BLOCKER
  NO_FOCUS_INDICATOR    focused control shows no visible change (2.4.7)                        BLOCKER
  FOCUS_OBSCURED        focused control entirely hidden by other content (2.4.11)              BLOCKER
  REFLOW_SCROLL         horizontal scrolling at a 320 CSS px viewport (1.4.10)                 BLOCKER
  NO_ACCESSIBLE_NAME    control with an empty computed name (4.1.2)                            BLOCKER
  TARGET_TOO_SMALL      pointer target under 24x24 CSS px without the spacing exception (2.5.8) BLOCKER
  NOT_KEYBOARD_REACHED  control never reached by a full Tab pass (2.1.1)                       HIGH
  TEXT_CLIPPED          text cut off by overflow hidden with no ellipsis                       HIGH
  PAGE_SCROLLS_X        horizontal scrolling at a wider viewport                               HIGH
  CONTRAST_UNVERIFIED   text on an image or gradient: check by eye or with a picker            WARN
  FOCUS_UNVERIFIED      focus not proven (script focus only, or not reached)                   WARN
  TRUNCATED             text truncated with an ellipsis: confirm the full value is reachable   WARN

Waive a finding the spec allows (e.g. the 2.5.8 Equivalent or Essential
exceptions) with --waivers CSV: id, code, reason. A waiver without a reason is
rejected.

Deterministic, stdlib only, no network.
"""
import argparse
import csv
import json
import math
import re
import sys

SEV_ORDER = {"BLOCKER": 0, "HIGH": 1, "WARN": 2}
EXIT = {"BLOCKED": 4, "FINDINGS": 2, "CLEAN": 0}
MIN_TARGET = 24.0


def _rgb(s):
    m = re.match(r"rgba?\(\s*([\d.]+)[,\s]+([\d.]+)[,\s]+([\d.]+)", s or "")
    if not m:
        m2 = re.match(r"#([0-9a-fA-F]{6})$", s or "")
        if not m2:
            return None
        h = m2.group(1)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    return tuple(float(x) for x in m.groups())


def luminance(c):
    def ch(v):
        v /= 255.0
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def is_large(px, weight):
    # 18pt = 24 CSS px; 14pt bold = 18.67 CSS px (WCAG "large scale").
    return px >= 24 or (px >= 18.66 and weight >= 700)


def _dist_point_rect(px, py, r):
    dx = max(r["x"] - px, 0, px - (r["x"] + r["w"]))
    dy = max(r["y"] - py, 0, py - (r["y"] + r["h"]))
    return math.hypot(dx, dy)


def spacing_ok(t, targets):
    """2.5.8 spacing exception: a 24 px circle centred on the target's box must not
    intersect another target, or the circle of another undersized target."""
    cx, cy = t["rect"]["x"] + t["rect"]["w"] / 2, t["rect"]["y"] + t["rect"]["h"] / 2
    for o in targets:
        if o is t:
            continue
        r = o["rect"]
        undersized = r["w"] < MIN_TARGET or r["h"] < MIN_TARGET
        if undersized:
            ox, oy = r["x"] + r["w"] / 2, r["y"] + r["h"] / 2
            if math.hypot(cx - ox, cy - oy) < MIN_TARGET:
                return False
        elif _dist_point_rect(cx, cy, r) < MIN_TARGET / 2:
            return False
    return True


def analyse(snap, waivers=None):
    if not isinstance(snap, dict) or not isinstance(snap.get("elements"), list):
        raise ValueError("not a design-qa snapshot (no 'elements' list); capture it with assets/collect_snapshot.js")
    els = snap["elements"]
    if not els:
        raise ValueError("snapshot has no elements; was the page rendered when it was captured?")
    vw = (snap.get("viewport") or {}).get("width")
    waivers = waivers or {}
    findings, used = [], set()

    def add(el_id, code, sev, msg, fix):
        key = (el_id, code)
        if key in waivers:
            used.add(key)
            return
        findings.append({"id": el_id, "code": code, "severity": sev, "message": msg, "fix": fix})

    page = snap.get("page") or {}
    if page.get("scrollWidth") and page.get("clientWidth") and page["scrollWidth"] > page["clientWidth"] + 1:
        over = page["scrollWidth"] - page["clientWidth"]
        code = "REFLOW_SCROLL" if vw and vw <= 320 else "PAGE_SCROLLS_X"
        wide = [e for e in els if e["rect"]["x"] + e["rect"]["w"] > page["clientWidth"] + 1]
        waived = [e for e in wide if (e["id"], code) in waivers]
        used.update((e["id"], code) for e in waived)
        wide = sorted((e for e in wide if e not in waived), key=lambda e: -(e["rect"]["x"] + e["rect"]["w"]))[:3]
        culprits = ", ".join(e["id"] for e in wide) or "unknown"
        if waived and not wide:
            pass  # every overflowing element carries a waiver (e.g. a data table, WCAG 1.4.10 exception)
        elif code == "REFLOW_SCROLL":
            add("page", "REFLOW_SCROLL", "BLOCKER", f"page scrolls horizontally by {over}px at {vw}px wide; widest: {culprits}",
                "Let the widest elements wrap or shrink (max-width:100%, min-width:0 on flex children, overflow-wrap:anywhere).")
        else:
            add("page", "PAGE_SCROLLS_X", "HIGH", f"page scrolls horizontally by {over}px at {vw}px wide; widest: {culprits}",
                "Find the overflowing element; it usually has a fixed width or an unbreakable string.")

    targets = [e for e in els if e.get("interactive") and not e.get("disabled")]
    pass_info = snap.get("keyboard_pass") or {}
    for e in els:
        eid = e.get("id", "?")
        if e.get("text"):
            fg, bg = _rgb(e.get("color")), _rgb(e.get("bg"))
            if e.get("bg_unknown") or not bg:
                add(eid, "CONTRAST_UNVERIFIED", "WARN", f"text '{e['text'][:40]}' sits on {e.get('bg_unknown') or 'an unknown background'}",
                    "Check the lightest and darkest point under the text with a color picker; add a scrim if it dips below the threshold.")
            elif fg and not e.get("disabled"):
                ratio = contrast(fg, bg)
                need = 3.0 if is_large(e.get("fontSize", 16), e.get("fontWeight", 400)) else 4.5
                if ratio + 1e-9 < need:
                    add(eid, "TEXT_CONTRAST", "BLOCKER",
                        f"'{e['text'][:40]}' is {ratio:.2f}:1 ({e.get('color')} on {e.get('bg')}, {e.get('fontSize')}px/{e.get('fontWeight')}); needs {need}:1",
                        "Darken the text or lighten the background until it passes; check the token, not just this element.")
        if e.get("clipped"):
            if e.get("ellipsis"):
                add(eid, "TRUNCATED", "WARN", f"'{e.get('text', '')[:40]}' is truncated with an ellipsis",
                    "Make sure the full value is reachable (title, tooltip or detail view).")
            else:
                add(eid, "TEXT_CLIPPED", "HIGH", f"'{e.get('text', '')[:40]}' is cut off by overflow hidden",
                    "Let it wrap, give the box room, or truncate deliberately with an ellipsis and a way to read the rest.")
        if not (e.get("interactive") and not e.get("disabled")):
            continue
        if not (e.get("name") or "").strip():
            add(eid, "NO_ACCESSIBLE_NAME", "BLOCKER", f"<{e.get('tag')}> has no accessible name in the rendered page",
                "Give it visible text, aria-label or aria-labelledby; icon-only buttons need a label.")
        r = e["rect"]
        if (r["w"] < MIN_TARGET or r["h"] < MIN_TARGET) and not e.get("inline") and not spacing_ok(e, targets):
            add(eid, "TARGET_TOO_SMALL", "BLOCKER",
                f"target is {r['w']:g}x{r['h']:g} CSS px and too close to its neighbours",
                "Make the hit area at least 24x24 (padding or a pseudo-element), or space targets so 24px circles do not overlap.")
        f = e.get("focus")
        if f is None:
            add(eid, "FOCUS_UNVERIFIED", "WARN", "no focus data in the snapshot",
                "Capture with assets/capture_snapshot.mjs for a real keyboard pass.")
            continue
        if f.get("how") == "not reached by Tab":
            if pass_info.get("wrapped"):
                add(eid, "NOT_KEYBOARD_REACHED", "HIGH", "a full Tab pass never reached this control",
                    "Remove tabindex=-1 or make it a native control; mouse-only controls fail WCAG 2.1.1.")
            else:
                add(eid, "FOCUS_UNVERIFIED", "WARN", "the Tab pass stopped before reaching this control",
                    "Re-run capture_snapshot.mjs with a higher --tabs.")
            continue
        if f.get("indicator") is False:
            add(eid, "NO_FOCUS_INDICATOR", "BLOCKER", f"focused <{e.get('tag')}> '{(e.get('name') or '')[:30]}' shows no visible change",
                "Add a :focus-visible outline or ring with at least 3:1 contrast against its surroundings.")
        elif f.get("indicator") is None:
            add(eid, "FOCUS_UNVERIFIED", "WARN", f"focus indicator not proven ({f.get('how', 'unknown')})",
                "Capture with assets/capture_snapshot.mjs for a real keyboard pass.")
        if f.get("obscured") is True:
            add(eid, "FOCUS_OBSCURED", "BLOCKER", "when focused, this control is entirely covered by other content",
                "Check sticky headers, cookie banners and chat widgets; add scroll-padding-top equal to the sticky header height.")

    unused = [f"{k[0]}:{k[1]}" for k in waivers if k not in used]
    groups = {}
    for f in findings:
        g = groups.setdefault((f["code"], pattern_of(f["id"])), {
            "code": f["code"], "severity": f["severity"], "pattern": pattern_of(f["id"]),
            "count": 0, "examples": [], "message": f["message"], "fix": f["fix"]})
        g["count"] += 1
        if len(g["examples"]) < 3:
            g["examples"].append(f["id"])
    findings.sort(key=lambda x: (SEV_ORDER[x["severity"]], x["code"], x["id"]))
    counts = {k: sum(1 for x in findings if x["severity"] == k) for k in SEV_ORDER}
    verdict = "BLOCKED" if counts["BLOCKER"] else ("FINDINGS" if findings else "CLEAN")
    return {"verdict": verdict, "url": snap.get("url"), "viewport": snap.get("viewport"),
            "elements": len(els), "interactive": len(targets),
            "keyboard_pass": "keyboard" if pass_info else "script-or-none",
            "counts": counts, "waived": len(used), "unused_waivers": unused,
            "groups": sorted(groups.values(), key=lambda g: (SEV_ORDER[g["severity"]], -g["count"], g["code"])),
            "findings": findings}


def pattern_of(el_id):
    """Repeated components (table rows, list items) differ only in :nth-of-type
    indices; dropping them groups 90 identical row buttons into one finding."""
    return re.sub(r":nth-of-type\(\d+\)", "", el_id)


def load_waivers(path):
    out = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for i, r in enumerate(csv.DictReader(fh), 2):
            r = {(k or "").strip().lower(): (v or "").strip() for k, v in r.items()}
            if not r.get("id") or not r.get("code"):
                raise ValueError(f"waivers row {i}: needs id and code")
            if not r.get("reason"):
                raise ValueError(f"waivers row {i}: a waiver needs a reason (which WCAG exception applies?)")
            out[(r["id"], r["code"].upper())] = r["reason"]
    return out


def render(out):
    vp = out.get("viewport") or {}
    lines = [f"design-qa rendered audit: {out['verdict']}  ({out.get('url')}, {vp.get('width')}x{vp.get('height')}; "
             f"{out['elements']} elements, {out['interactive']} interactive; focus data: {out['keyboard_pass']}; "
             f"{out['counts']['BLOCKER']} blocker, {out['counts']['HIGH']} high, {out['counts']['WARN']} warn; {out['waived']} waived)", ""]
    for g in out["groups"]:
        if g["count"] == 1:
            lines.append(f"[{g['severity']}] {g['code']}  {g['examples'][0]}")
            lines.append(f"    {g['message']}")
        else:
            lines.append(f"[{g['severity']}] {g['code']}  x{g['count']}  {g['pattern']}")
            lines.append(f"    e.g. {g['examples'][0]}: {g['message']}")
        lines.append(f"    fix: {g['fix']}")
    for w in out["unused_waivers"]:
        lines.append(f"[note] waiver {w} matched nothing; remove it")
    return "\n".join(lines)


SAMPLE = {
    "tool": "design-qa/collect_snapshot.js", "version": 1, "url": "http://localhost:3000/invoices",
    "viewport": {"width": 320, "height": 640}, "page": {"scrollWidth": 412, "clientWidth": 320},
    "keyboard_pass": {"reached": 3, "wrapped": True},
    "elements": [
        {"id": "h1", "tag": "h1", "interactive": False, "text": "Invoices", "rect": {"x": 16, "y": 20, "w": 288, "h": 32},
         "color": "rgb(17, 24, 39)", "bg": "rgb(255, 255, 255)", "fontSize": 28, "fontWeight": 700},
        {"id": "p.hint", "tag": "p", "interactive": False, "text": "Showing invoices from the last 30 days",
         "rect": {"x": 16, "y": 60, "w": 288, "h": 18}, "color": "rgb(156, 163, 175)", "bg": "rgb(255, 255, 255)",
         "fontSize": 14, "fontWeight": 400},
        {"id": "table.invoices", "tag": "table", "interactive": False, "text": "INV-2026-0042", "rect": {"x": 16, "y": 100, "w": 396, "h": 300},
         "color": "rgb(17, 24, 39)", "bg": "rgb(255, 255, 255)", "fontSize": 14, "fontWeight": 400},
        {"id": "td.customer", "tag": "td", "interactive": False, "text": "Northwind Traders Internatio", "clipped": True, "ellipsis": False,
         "rect": {"x": 120, "y": 140, "w": 90, "h": 20}, "color": "rgb(17, 24, 39)", "bg": "rgb(255, 255, 255)", "fontSize": 14, "fontWeight": 400},
        {"id": "button.send", "tag": "button", "interactive": True, "name": "Send", "text": "Send",
         "rect": {"x": 16, "y": 420, "w": 80, "h": 36}, "color": "rgb(255, 255, 255)", "bg": "rgb(37, 99, 235)",
         "fontSize": 14, "fontWeight": 600, "focus": {"indicator": False, "obscured": False, "how": "keyboard"}},
        {"id": "button.more", "tag": "button", "interactive": True, "name": "", "text": "",
         "rect": {"x": 97, "y": 426, "w": 20, "h": 20}, "color": "rgb(75, 85, 99)", "bg": "rgb(255, 255, 255)",
         "fontSize": 14, "fontWeight": 400, "focus": {"indicator": True, "obscured": False, "how": "keyboard"}},
        {"id": "a.export", "tag": "a", "interactive": True, "name": "Export", "text": "Export",
         "rect": {"x": 124, "y": 426, "w": 44, "h": 20}, "color": "rgb(37, 99, 235)", "bg": "rgb(255, 255, 255)",
         "fontSize": 14, "fontWeight": 400, "focus": {"indicator": True, "obscured": True, "how": "keyboard"}},
        {"id": "div.row-menu", "tag": "div", "role": "button", "interactive": True, "name": "Row actions", "text": "",
         "rect": {"x": 280, "y": 140, "w": 24, "h": 24}, "focus": {"indicator": None, "obscured": None, "how": "not reached by Tab"}},
        {"id": "section.hero > p", "tag": "p", "interactive": False, "text": "Paid on time, every time", "bg_unknown": "background image or gradient",
         "rect": {"x": 16, "y": 480, "w": 288, "h": 20}, "color": "rgb(255, 255, 255)", "bg": None, "fontSize": 16, "fontWeight": 400},
    ],
}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clean, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("--snapshot", help="snapshot JSON from assets/collect_snapshot.js or capture_snapshot.mjs")
    p.add_argument("--waivers", help="CSV of allowed exceptions: id, code, reason")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            snap = SAMPLE
        elif a.snapshot:
            with open(a.snapshot, encoding="utf-8") as fh:
                snap = json.load(fh)
        else:
            p.print_usage(sys.stderr)
            print("error: give --snapshot FILE or --sample", file=sys.stderr)
            return 3
        out = analyse(snap, load_waivers(a.waivers) if a.waivers else None)
    except (OSError, ValueError, KeyError, TypeError) as e:
        msg = f"{type(e).__name__}: {e}" if isinstance(e, (KeyError, TypeError)) else str(e)
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [msg]}, indent=2))
        else:
            print(f"error: {msg}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
