#!/usr/bin/env python3
"""Lint UI source for unfinished work: controls that do nothing, placeholder copy, removed focus rings and template defaults.

A screen can pass review in a static screenshot and still ship broken: a button
wired to `() => {}`, a link to `#`, "Lorem ipsum" in an empty state, or
`outline: none` with nothing in its place. These are objective, so they block.
Generic "template" styling is a judgment, so it only warns: the brief may ask
for exactly that look.

Findings
  INERT_HANDLER       click handler that does nothing (`() => {}`, `null`, only logs or alerts)   BLOCKER
  DEAD_LINK           <a> with href "#", "" or "javascript:" and no click handler              BLOCKER
  PLACEHOLDER_COPY    lorem ipsum, TODO, TBD, "[Insert ...]", "your text here", XX values      BLOCKER
  FOCUS_REMOVED       outline removed with no :focus-visible / ring / box-shadow replacement     BLOCKER
  BUTTON_NO_ACTION    <button> with no handler, no submit/reset type and no enclosing <form>      HIGH
  SAMPLE_DATA         John/Jane Doe, Acme, example.com addresses, 555 numbers in markup           WARN
  TOKEN_DRIFT         more distinct raw hex colors / arbitrary values than --max-raw-colors       WARN
  TEMPLATE_DEFAULT    one finding per template trait found (see references/generic_ui_defaults.md) WARN

Accessibility source checks (alt text, labels, ARIA, headings) belong to the
a11y-audit skill; this linter does not repeat them.

Suppress a line with a comment containing `design-qa: allow CODE`.
Deterministic, stdlib only, no network.
"""
import argparse
import json
import os
import re
import sys

UI_EXT = {".html", ".htm", ".jsx", ".tsx", ".js", ".ts", ".vue", ".svelte", ".astro"}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
SKIP_DIRS = {"node_modules", "dist", "build", ".next", ".nuxt", "out", "coverage", ".git", "vendor", "__snapshots__"}
TEST_RE = re.compile(r"\.(test|spec|stories|story|fixture)\.|/(tests?|__tests__|e2e|fixtures)/", re.I)
TOKEN_FILE_RE = re.compile(r"(token|theme|variables|palette|colors?|tailwind\.config)", re.I)
SEV_ORDER = {"BLOCKER": 0, "HIGH": 1, "WARN": 2}
EXIT = {"BLOCKED": 4, "FINDINGS": 2, "CLEAN": 0}

HANDLER_ATTR = r"(?:onClick|onPress|onSubmit|onclick|@click|v-on:click|on:click|\(click\))"
INERT_PATTERNS = [
    (re.compile(HANDLER_ATTR + r"\s*=\s*\{\s*\(\s*[\w,\s]*\)\s*=>\s*(?:\{\s*\}|null|undefined|void 0|\{\s*return;?\s*\})\s*\}"), "empty arrow function"),
    (re.compile(HANDLER_ATTR + r"\s*=\s*\{\s*(?:undefined|null|noop|\(\)\s*=>\s*noop\(\))\s*\}"), "handler is undefined/null/noop"),
    (re.compile(HANDLER_ATTR + r"\s*=\s*\{\s*\(\s*[\w,\s]*\)\s*=>\s*\{?\s*(?:console\.(?:log|info|debug)|alert)\s*\([^)]*\)\s*;?\s*\}?\s*\}"), "handler only logs or alerts"),
    (re.compile(r"(?:onclick|@click|v-on:click|on:click|\(click\))\s*=\s*([\"'])\s*(?:void\(0\);?|return false;?|)\s*\1"), "empty inline handler"),
    (re.compile(HANDLER_ATTR + r"\s*=\s*\{[^}]*(?:TODO|FIXME|not implemented|coming soon)", re.I), "handler marked TODO"),
]
DEAD_HREF = re.compile(r"<a\b[^>]*\bhref\s*=\s*(?:([\"'])\s*(?:#|javascript:[^\"']*|)\s*\1|\{\s*[\"']#?[\"']\s*\})[^>]*>", re.I)
PLACEHOLDER = re.compile(
    r"lorem ipsum|dolor sit amet|\bTODO\b|\bTBD\b|\bFIXME\b|\[\s*insert[^\]]*\]|your (?:text|title|copy|headline|description) here|"
    r"placeholder (?:text|copy|title)|text goes here|\$\s?XX|\bXX(?:\.XX)?\s?%|\bXXX\b|coming soon", re.I)
SAMPLE = re.compile(r"\b(?:John|Jane) Doe\b|\bAcme(?: Inc| Corp)?\b|[\w.]+@example\.(?:com|org)|\b555[- .]\d{4}\b|\b123 Main St", re.I)
TEXT_NODE = re.compile(r">([^<>{}]+)<")
TEXT_ATTR = re.compile(r"\b(?:placeholder|alt|title|aria-label|label|value)\s*=\s*([\"'])([^\"']*)\1")
STRING_LIT = re.compile(r"([\"'`])((?:(?!\1).){3,200})\1")
CSS_RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")
OUTLINE_OFF = re.compile(r"outline(?:-style)?\s*:\s*(?:none|0(?:px)?)\b", re.I)
FOCUS_REPLACEMENT = re.compile(r"box-shadow|outline-offset|border(?:-color)?\s*:|text-decoration|background(?:-color)?\s*:", re.I)
TW_OUTLINE_OFF = re.compile(r"(?<![\w-])(?:focus:)?outline-none(?![\w-])")
TW_FOCUS_OK = re.compile(r"focus(?:-visible)?:(?:ring|outline-(?!none)|shadow|border|underline|bg-)")
HEX = re.compile(r"#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")
ARBITRARY = re.compile(r"\b(?:text|bg|border|p[xytrbl]?|m[xytrbl]?|w|h|gap|top|left|right|bottom|rounded)-\[[^\]]+\]")
SUPPRESS = re.compile(r"design-qa:\s*allow\s+([A-Z_ ,]+)")

TEMPLATE_TRAITS = [
    ("gradient_wash", "decorative gradient wash (purple/indigo/pink family)",
     re.compile(r"(?:from|via|to)-(?:purple|violet|indigo|fuchsia|pink)-\d{2,3}|linear-gradient\([^)]*(?:#(?:6366f1|8b5cf6|a855f7|7c3aed|4f46e5|ec4899)|purple|violet|indigo)", re.I)),
    ("card_kit", "identical soft-shadow rounded cards",
     re.compile(r"rounded-(?:xl|2xl|3xl)[^\"'`]*shadow-(?:md|lg|xl)|shadow-(?:md|lg|xl)[^\"'`]*rounded-(?:xl|2xl|3xl)|box-shadow:\s*0[^;]*rgba\(0,\s*0,\s*0,\s*0?\.1\)", re.I)),
    ("eyebrow_caps", "tracked-out ALL-CAPS eyebrow label",
     re.compile(r"uppercase[^\"'`]*tracking-(?:wide|wider|widest)|tracking-(?:wide|wider|widest)[^\"'`]*uppercase|text-transform:\s*uppercase[^}]*letter-spacing", re.I)),
    ("arrow_suffix", "'→' appended to link or button text", re.compile(r"\s(?:→|-&gt;|&rarr;)\s*<")),
    ("middot_meta", "meta strings joined with middle dots", re.compile(r"\w\s·\s\w[^<]*\s·\s\w")),
    ("numbered_markers", "01 / 02 / 03 numbered markers", re.compile(r">\s*0[1-3]\s*<|[\"'`]0[1-3][\"'`]")),
    ("entrance_motion", "fade-and-slide-up entrance on sections",
     re.compile(r"fade-?(?:in-?)?up|data-aos=[\"']fade-up|initial=\{\{\s*opacity:\s*0,\s*y:\s*\d+", re.I)),
    ("hover_lift", "hover lift/scale on every card", re.compile(r"hover:(?:-translate-y-\d|scale-10[2-5])")),
    ("hero_cliche", "stock hero copy",
     re.compile(r"\b(?:unlock the (?:power|potential)|supercharge|revolutioni[sz]e|seamless(?:ly)?|elevate your|empower(?:s|ing)? (?:your|teams)|next[- ]gen(?:eration)?|game[- ]chang|all-in-one|effortless(?:ly)?)\b", re.I)),
]
TRAIT_WARN_AT = 4


def _suppressed(line):
    m = SUPPRESS.search(line)
    return set(c.strip() for c in m.group(1).replace(",", " ").split()) if m else set()


def _finding(out, path, ln, code, sev, msg, fix, snippet, line):
    if code in _suppressed(line):
        return
    out.append({"file": path, "line": ln, "code": code, "severity": sev,
                "message": msg, "fix": fix, "snippet": snippet.strip()[:140]})


def _visible_text(line):
    parts = [m.group(1) for m in TEXT_NODE.finditer(line)]
    parts += [m.group(2) for m in TEXT_ATTR.finditer(line)]
    return " ".join(parts)


def _strip_comments(line):
    line = re.sub(r"<!--.*?-->|/\*.*?\*/|\{/\*.*?\*/\}", "", line)
    if re.match(r"\s*(//|\*|/\*)", line):
        return ""
    return line


def lint_markup(path, text, findings, traits, raw_colors):
    lines = text.splitlines()
    form_depth = 0
    for ln, raw in enumerate(lines, 1):
        line = _strip_comments(raw)
        if not line.strip():
            continue
        for rx, why in INERT_PATTERNS:
            if rx.search(line):
                _finding(findings, path, ln, "INERT_HANDLER", "BLOCKER", f"Control does nothing ({why}).",
                         "Wire the real action, or remove the control until it works; a disabled state needs a visible reason.",
                         line, raw)
                break
        for m in DEAD_HREF.finditer(line):
            if not re.search(HANDLER_ATTR, m.group(0)):
                _finding(findings, path, ln, "DEAD_LINK", "BLOCKER", "Link goes nowhere (href is '#', empty or javascript:).",
                         "Point it at a real route or anchor; if it performs an action, make it a <button>.", m.group(0), raw)
        visible = _visible_text(line)
        if path.endswith((".js", ".ts", ".jsx", ".tsx", ".vue", ".svelte")):
            visible += " " + " ".join(m.group(2) for m in STRING_LIT.finditer(line)
                                      if not re.search(r"[/\\.]\w+$|^[\w-]+$|className|import", m.group(2)))
        m = PLACEHOLDER.search(visible)
        if m:
            _finding(findings, path, ln, "PLACEHOLDER_COPY", "BLOCKER", f"Unfinished copy on screen: '{m.group(0)}'.",
                     "Write the real copy; for an empty state, say what happened and the next action.", line, raw)
        else:
            m = SAMPLE.search(visible)
            if m:
                _finding(findings, path, ln, "SAMPLE_DATA", "WARN", f"Sample data in markup: '{m.group(0)}'.",
                         "Confirm it is intentional demo content, otherwise bind real data.", line, raw)
        form_depth += len(re.findall(r"<form\b", line, re.I)) - len(re.findall(r"</form>", line, re.I))
        for b in re.finditer(r"<button\b([^>]*)>", line):
            attrs = b.group(1)
            if form_depth > 0 or re.search(HANDLER_ATTR + r"|type\s*=\s*[\"'](?:submit|reset)|\{\s*\.\.\.|\bdisabled\b|formAction|form=|popovertarget|commandfor|data-(?:bs-)?toggle", attrs):
                continue
            _finding(findings, path, ln, "BUTTON_NO_ACTION", "HIGH", "<button> has no handler, no submit/reset type and no enclosing form on this line range.",
                     "Attach the handler or confirm it is wired elsewhere (then suppress with design-qa: allow BUTTON_NO_ACTION).",
                     b.group(0), raw)
        if TW_OUTLINE_OFF.search(line):
            cls = " ".join(re.findall(r"(?:class|className)\s*=\s*[{\"'`]([^\"'`}]*)", line)) or line
            if not TW_FOCUS_OK.search(cls):
                _finding(findings, path, ln, "FOCUS_REMOVED", "BLOCKER", "outline-none with no focus-visible replacement on the same element.",
                         "Add a visible focus style, e.g. focus-visible:ring-2 focus-visible:ring-offset-2 (WCAG 2.4.7).", line, raw)
        _collect_traits(path, ln, line, traits)
        raw_colors.update(h.lower() for h in HEX.findall(line))
        raw_colors.update(ARBITRARY.findall(line))
    if re.search(r"<style\b", text, re.I):
        for block in re.findall(r"<style\b[^>]*>(.*?)</style>", text, re.S | re.I):
            offset = text[:text.find(block)].count("\n")
            lint_css(path, block, findings, traits, raw_colors, offset)


def lint_css(path, text, findings, traits, raw_colors, line_offset=0):
    clean = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    focus_visible_present = ":focus-visible" in clean
    for m in CSS_RULE.finditer(clean):
        selector, body = m.group(1).strip(), m.group(2)
        ln = clean[:m.start(2)].count("\n") + 1 + line_offset
        raw = text.splitlines()[min(ln - 1 - line_offset, len(text.splitlines()) - 1)] if text else ""
        if OUTLINE_OFF.search(body):
            replaced = FOCUS_REPLACEMENT.search(body) or ":focus-visible" in selector
            if not replaced and not (":focus" in selector and focus_visible_present and ":focus-visible" not in selector
                                     and ":not(:focus-visible)" in selector):
                _finding(findings, path, ln, "FOCUS_REMOVED", "BLOCKER",
                         f"Focus outline removed on '{selector[:60]}' with no replacement in the rule.",
                         "Keep the outline, or replace it in a :focus-visible rule with an outline or box-shadow of 3:1 contrast (WCAG 2.4.7).",
                         selector + " { " + body.strip()[:60], raw)
        raw_colors.update(h.lower() for h in HEX.findall(body))
        _collect_traits(path, ln, selector + "{" + body + "}", traits)


def _collect_traits(path, ln, line, traits):
    for key, label, rx in TEMPLATE_TRAITS:
        if rx.search(line):
            traits.setdefault(key, {"label": label, "hits": []})
            if len(traits[key]["hits"]) < 5:
                traits[key]["hits"].append(f"{path}:{ln}")


def iter_files(root, include_tests):
    if os.path.isfile(root):
        yield root
        return
    for d, dirs, files in os.walk(root):
        dirs[:] = sorted(x for x in dirs if x not in SKIP_DIRS and not x.startswith("."))
        for f in sorted(files):
            p = os.path.join(d, f)
            if os.path.splitext(f)[1].lower() not in UI_EXT | STYLE_EXT:
                continue
            if not include_tests and TEST_RE.search(p.replace(os.sep, "/")):
                continue
            yield p


def analyse(paths, include_tests=False, max_raw_colors=12, sources=None):
    findings, traits, raw_colors, scanned = [], {}, set(), 0
    items = sources if sources is not None else [
        (p, None) for root in paths for p in iter_files(root, include_tests)]
    for p, text in items:
        if text is None:
            try:
                with open(p, encoding="utf-8", errors="replace") as fh:
                    text = fh.read()
            except OSError as e:
                raise ValueError(f"cannot read {p}: {e}")
        scanned += 1
        colors = set() if TOKEN_FILE_RE.search(os.path.basename(p)) else raw_colors
        if os.path.splitext(p)[1].lower() in STYLE_EXT:
            lint_css(p, text, findings, traits, colors)
        else:
            lint_markup(p, text, findings, traits, colors)
    if scanned == 0:
        raise ValueError("no UI source files found (.html .jsx .tsx .vue .svelte .astro .css ...)")
    if len(raw_colors) > max_raw_colors:
        sample = sorted(raw_colors)[:10]
        findings.append({"file": "*", "line": 0, "code": "TOKEN_DRIFT", "severity": "WARN",
                         "message": f"{len(raw_colors)} distinct raw colors/arbitrary values outside token files (limit {max_raw_colors}).",
                         "fix": "Move repeated values into design tokens; one-off values usually mean the screen drifted from the system.",
                         "snippet": ", ".join(sample)})
    for key, t in sorted(traits.items()):
        findings.append({"file": t["hits"][0].rsplit(":", 1)[0], "line": int(t["hits"][0].rsplit(":", 1)[1]),
                         "code": "TEMPLATE_DEFAULT", "severity": "WARN",
                         "message": f"Template default: {t['label']} ({len(t['hits'])}+ places).",
                         "fix": "Keep it only if the brief asks for it; otherwise make a choice specific to this product.",
                         "snippet": ", ".join(t["hits"])})
    findings.sort(key=lambda f: (SEV_ORDER[f["severity"]], f["file"], f["line"]))
    counts = {s: sum(1 for f in findings if f["severity"] == s) for s in SEV_ORDER}
    verdict = "BLOCKED" if counts["BLOCKER"] else ("FINDINGS" if findings else "CLEAN")
    return {"verdict": verdict, "files_scanned": scanned, "counts": counts,
            "template_traits": len(traits),
            "generic_risk": "HIGH" if len(traits) >= TRAIT_WARN_AT else ("MEDIUM" if len(traits) >= 2 else "LOW"),
            "findings": findings}


def render(out):
    lines = [f"design-qa finish lint: {out['verdict']}  ({out['files_scanned']} files; "
             f"{out['counts']['BLOCKER']} blocker, {out['counts']['HIGH']} high, {out['counts']['WARN']} warn; "
             f"template traits {out['template_traits']} -> generic risk {out['generic_risk']})", ""]
    for f in out["findings"]:
        lines.append(f"[{f['severity']}] {f['code']}  {f['file']}:{f['line']}")
        lines.append(f"    {f['message']}")
        lines.append(f"    fix: {f['fix']}")
        if f["snippet"]:
            lines.append(f"    > {f['snippet']}")
    if not out["findings"]:
        lines.append("No finish defects found. This does not test the rendered page: run rendered_audit.py next.")
    return "\n".join(lines)


SAMPLE_SRC = [("sample/Pricing.tsx", """
export function Pricing({ plans }) {
  return (
    <section className="bg-gradient-to-br from-indigo-500 to-purple-600">
      <p className="text-xs uppercase tracking-widest">Pricing</p>
      <h1>Unlock the power of seamless billing</h1>
      {plans.map(p => (
        <div className="rounded-2xl shadow-lg hover:-translate-y-1 p-[13px]">
          <h3>{p.name}</h3>
          <p>Lorem ipsum dolor sit amet</p>
          <button className="focus:outline-none" onClick={() => {}}>Choose plan</button>
        </div>
      ))}
      <a href="#">Compare all features →</a>
      <button>Contact sales</button>
      <a href="/contact" className="outline-none focus-visible:ring-2">Talk to us</a>
    </section>
  );
}
"""), ("sample/site.css", """
button:focus { outline: none; }
a:focus { outline: none; box-shadow: 0 0 0 3px #1d4ed8; }
""")]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0],
                                epilog="Exit codes: 0 clean, 2 findings, 3 invalid input, 4 blocked.")
    p.add_argument("paths", nargs="*", help="files or directories with UI source")
    p.add_argument("--include-tests", action="store_true", help="also scan tests, stories and fixtures")
    p.add_argument("--max-raw-colors", type=int, default=12, help="distinct raw colors before TOKEN_DRIFT (default 12)")
    p.add_argument("--sample", action="store_true", help="run on a built-in example")
    p.add_argument("--output", choices=["text", "json"], default="text")
    p.add_argument("--json", action="store_true", help="shorthand for --output json")
    a = p.parse_args(argv)
    if a.json:
        a.output = "json"
    try:
        if a.sample:
            out = analyse([], sources=SAMPLE_SRC, max_raw_colors=a.max_raw_colors)
        elif a.paths:
            for x in a.paths:
                if not os.path.exists(x):
                    raise ValueError(f"path not found: {x}")
            out = analyse(a.paths, a.include_tests, a.max_raw_colors)
        else:
            p.print_usage(sys.stderr)
            print("error: give one or more paths, or --sample", file=sys.stderr)
            return 3
    except ValueError as e:
        if a.output == "json":
            print(json.dumps({"verdict": "INVALID_INPUT", "errors": [str(e)]}, indent=2))
        else:
            print(f"error: {e}", file=sys.stderr)
        return 3
    print(json.dumps(out, indent=2) if a.output == "json" else render(out))
    return EXIT[out["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
