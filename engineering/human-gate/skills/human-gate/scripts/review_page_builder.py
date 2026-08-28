#!/usr/bin/env python3
"""Build a single-file HTML review page for a Markdown or HTML artifact.

The page opens straight off the filesystem (file://) — there is no server, no
socket, and no network fetch of any kind. Every block of the artifact gets a
stable id; the reviewer clicks one, picks a severity, and types. Work is kept
in localStorage, and "Export feedback" writes the sidecar Markdown that
feedback_parser.py reads back.

That export format is hand-writable on purpose. A reviewer with no browser can
skip this script entirely and write the sidecar in an editor — the loop still
closes. This page is the comfortable path, not the required one.

Exit codes
----------
    0  page written
    1  usage error / unreadable input
    2  artifact has no reviewable blocks
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

BLOCK_TAGS = {
    "p", "h1", "h2", "h3", "h4", "h5", "h6", "ul", "ol", "pre", "blockquote",
    "table", "hr", "section", "figure", "div",
}

# Dropped entirely from a reviewed HTML artifact. script/style/head/link/meta
# are chrome the review page supplies itself; iframe/object/embed/frame would
# execute or fetch third-party content inside a page the reviewer trusts.
DROP_TAGS = {
    "script", "style", "head", "link", "meta",
    "iframe", "object", "embed", "frame", "frameset", "base", "applet",
}

# Attributes carrying a URL, which must clear the same scheme allowlist the
# Markdown path uses. Everything named on* is an event handler and is dropped.
# xlink:href is the legacy SVG form and is still honoured by browsers, so an
# <svg><a xlink:href="javascript:..."> would bypass a plain "href" check.
URL_ATTRS = {
    "href", "src", "action", "formaction", "poster", "cite", "background",
    "xlink:href", "xlink:role", "xlink:arcrole",
}
# `style` joins these because `background-image:url(https://...)` fires a request
# the moment the reviewer opens the page — no script needed. The <style> *tag* was
# already dropped, so keeping the attribute was inconsistent as well as leaky.
DROP_ATTRS = {"srcdoc", "srcset", "style"}

# data-hg is this tool's own block anchor. If a reviewed artifact carries one,
# the builder would append a second, and the browser keeps the FIRST — so the
# click handler reads the artifact's value, not ours. Attribute values may hold
# raw newlines, so a crafted one becomes extra "## APPROVE" lines in the
# exported sidecar: a forged sign-off smuggled in by the content under review.
# The page's own element ids are reserved for the same collision reason.
RESERVED_ATTRS = {"data-hg"}
RESERVED_IDS = {
    "doc", "items", "hint", "counts", "reviewer", "add-note", "copy",
    "export", "toast",
}

SAMPLE_HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<base href="/">
<link rel="stylesheet" href="style.css">
<title>Landing</title>
</head><body>
<h1>Ship faster</h1>
<p>One usable slice per week.</p>
<ul><li>Onboarding rewrite</li><li>Retire the importer</li></ul>
<p><a href="//cdn.example.com/pricing">protocol-relative link</a> and an
<img src="https://img.example.com/hero.png" alt="own asset"> both survive on
purpose, while <a href="javascript:alert(1)">this</a> does not.</p>
</body></html>
"""

SAMPLE_MD = """# Quarterly plan

We expect a 40% lift in activation.

## Bets

- Ship the onboarding rewrite
- Retire the legacy importer

## Risks

The team will endeavour to deliver incremental value. The page template uses
__TITLE__ and __CONFIG__ as slots, and reviewing a doc that says so must not
corrupt the page — that is a regression this fixture guards.
"""


# --------------------------------------------------------------- markdown

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)\)")
LINK = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")


def _safe_href(url, image=False):
    """Allow relative URLs and http/https/mailto; data: only for inline images.

    Control characters are stripped before the scheme is read, so
    `java\\tscript:alert(1)` cannot smuggle a scheme past the check.
    """
    probe = re.sub(r"[\x00-\x20\x7f]+", "", url)
    match = re.match(r"^([a-zA-Z][a-zA-Z0-9+.\-]*):", probe)
    if not match:
        # No scheme: a relative or protocol-relative ("//host/x") URL. Both are
        # allowed deliberately — neither can execute, and a reviewed artifact's
        # own assets must still resolve for the review to be faithful.
        return url
    scheme = match.group(1).lower()
    if scheme in ("http", "https", "mailto"):
        return url
    if image and re.match(
        r"^data:image/(?:avif|gif|jpe?g|png|webp);base64,", probe, re.IGNORECASE
    ):
        return url
    return None


def inline(text):
    """Escape first, then apply inline markup. Never trusts raw HTML."""
    out = html.escape(text, quote=False)
    out = INLINE_CODE.sub(lambda m: "<code>%s</code>" % m.group(1), out)
    out = BOLD.sub(lambda m: "<strong>%s</strong>" % m.group(1), out)
    out = ITALIC.sub(lambda m: "<em>%s</em>" % m.group(1), out)

    def image(match):
        src = _safe_href(html.unescape(match.group(2)), image=True)
        if src is None:
            return match.group(1)
        return '<img src="%s" alt="%s">' % (
            html.escape(src, quote=True), html.escape(match.group(1), quote=True)
        )

    out = IMAGE.sub(image, out)

    def link(match):
        href = _safe_href(html.unescape(match.group(2)))
        if href is None:
            return match.group(1)
        return '<a href="%s" rel="noreferrer noopener">%s</a>' % (
            html.escape(href, quote=True),
            match.group(1),
        )

    return LINK.sub(link, out)


def markdown_blocks(text):
    """Split Markdown into renderable block dicts. Deliberately a subset."""
    lines = text.replace("\r\n", "\n").split("\n")
    blocks = []
    index = 0
    total = len(lines)

    while index < total:
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            body = []
            index += 1
            while index < total and not lines[index].strip().startswith("```"):
                body.append(lines[index])
                index += 1
            index += 1
            blocks.append({"type": "code", "lang": lang, "text": "\n".join(body)})
            continue

        heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading:
            blocks.append(
                {
                    "type": "heading",
                    "level": len(heading.group(1)),
                    "text": heading.group(2).strip(),
                }
            )
            index += 1
            continue

        if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
            blocks.append({"type": "hr", "text": ""})
            index += 1
            continue

        if stripped.startswith(">"):
            body = []
            while index < total and lines[index].strip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[index]))
                index += 1
            blocks.append({"type": "quote", "text": "\n".join(body).strip()})
            continue

        if stripped.startswith("|") and index + 1 < total and re.match(
            r"^\s*\|[\s:|-]+\|\s*$", lines[index + 1]
        ):
            rows = []
            while index < total and lines[index].strip().startswith("|"):
                rows.append(lines[index].strip())
                index += 1
            blocks.append({"type": "table", "rows": rows, "text": "\n".join(rows)})
            continue

        bullet = re.match(r"^\s*([-*+]|\d+[.)])\s+", line)
        if bullet:
            ordered = not bullet.group(1) in ("-", "*", "+")
            items = []
            while index < total and re.match(r"^\s*([-*+]|\d+[.)])\s+", lines[index]):
                items.append(re.sub(r"^\s*([-*+]|\d+[.)])\s+", "", lines[index]))
                index += 1
            blocks.append(
                {"type": "list", "ordered": ordered, "items": items,
                 "text": "\n".join(items)}
            )
            continue

        body = []
        while index < total and lines[index].strip() and not re.match(
            r"^\s*(#{1,6}\s|>|```|\||[-*+]\s|\d+[.)]\s|-{3,}$)", lines[index]
        ):
            body.append(lines[index].strip())
            index += 1
        if not body:  # defensive: never spin on an unconsumed line
            body = [stripped]
            index += 1
        blocks.append({"type": "para", "text": " ".join(body)})

    return blocks


def render_block(block, block_id):
    attr = ' data-hg="%s"' % block_id
    kind = block["type"]
    if kind == "heading":
        return "<h%d%s>%s</h%d>" % (
            block["level"], attr, inline(block["text"]), block["level"]
        )
    if kind == "para":
        return "<p%s>%s</p>" % (attr, inline(block["text"]))
    if kind == "code":
        return '<pre%s><code>%s</code></pre>' % (
            attr, html.escape(block["text"], quote=False)
        )
    if kind == "quote":
        return "<blockquote%s>%s</blockquote>" % (attr, inline(block["text"]))
    if kind == "hr":
        return "<hr%s>" % attr
    if kind == "list":
        tag = "ol" if block["ordered"] else "ul"
        items = "".join("<li>%s</li>" % inline(i) for i in block["items"])
        return "<%s%s>%s</%s>" % (tag, attr, items, tag)
    if kind == "table":
        rows = [
            [cell.strip() for cell in row.strip().strip("|").split("|")]
            for row in block["rows"]
        ]
        head, body = rows[0], rows[2:]
        out = ["<table%s><thead><tr>" % attr]
        out += ["<th>%s</th>" % inline(c) for c in head]
        out.append("</tr></thead><tbody>")
        for row in body:
            out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in row) + "</tr>")
        out.append("</tbody></table>")
        return "".join(out)
    return "<p%s>%s</p>" % (attr, inline(block.get("text", "")))


# ------------------------------------------------------------------- html


def sanitize_attrs(attrs):
    """Strip event handlers and unsafe URL schemes from a reviewed HTML tag.

    The Markdown path scheme-allowlists every link through _safe_href. Raw HTML
    input has to clear the same bar: without this an artifact containing
    `<img src=x onerror=...>` or `<a href="javascript:...">` executes inside the
    review page the moment the reviewer opens it — and reviewing a landing-page
    draft is a documented use of this skill.
    """
    kept = []
    names = {n.lower() for n, _ in attrs}
    blank_target = any(
        n.lower() == "target" and (v or "").lower() == "_blank" for n, v in attrs
    )
    for name, value in attrs:
        lower = name.lower()
        if lower.startswith("on") or lower in DROP_ATTRS:
            continue
        if lower in RESERVED_ATTRS:
            continue
        if lower == "id" and (value or "").strip().lower() in RESERVED_IDS:
            continue
        if lower in URL_ATTRS:
            safe = _safe_href(value or "", image=(lower in ("src", "poster", "background")))
            if safe is None:
                continue
            value = safe
        kept.append((name, value))
    # Same hardening the Markdown path already applies to its own anchors.
    if blank_target and "rel" not in names:
        kept.append(("rel", "noreferrer noopener"))
    return kept


class BlockTagger(HTMLParser):
    """Re-emit an HTML body, tagging top-level block elements with data-hg ids."""

    # The complete HTML void-element set. A hand-picked subset is how <base>
    # kept swallowing the body after the <meta>/<link> fix: any DROP_TAGS entry
    # missing from here never fires handle_endtag, so its skip counter is never
    # released. Spec list, so the class cannot recur one tag at a time.
    VOID = (
        "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr", "frame",
    )

    def __init__(self, fragment=False):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.depth = 0
        self.count = 0
        self.blocks = []
        self._capture = None
        # A fragment with no <body> is all body: start capturing immediately.
        self._in_body = fragment
        self._skip = 0
        # Name of the last unterminated drop-tag, for a diagnosable warning
        # rather than a silent truncation (an unclosed <script> legitimately
        # swallows the rest per HTML parsing, but the user deserves to know).
        self._skipping = []

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self._in_body = True
            return
        if tag in DROP_TAGS:
            # A void drop-tag (<meta>, <link>, <base>) never fires a matching
            # handle_endtag, so bumping _skip here would strand it above zero
            # for the rest of the parse and silently swallow the entire body.
            # Every real HTML5 head has a bare <meta charset>, so this is the
            # common case, not an edge case.
            if tag not in self.VOID:
                self._skip += 1
                self._skipping.append(tag)
            return
        if self._skip:
            return
        # Depth is measured *inside* the body only. Counting the wrapping
        # <html> would push every real block to depth 1, and nothing would
        # ever be tagged.
        if not self._in_body:
            return
        rebuilt = "".join(
            ' %s="%s"' % (k, html.escape(v or "", quote=True))
            for k, v in sanitize_attrs(attrs)
        )
        if self.depth == 0 and tag in BLOCK_TAGS:
            self.count += 1
            block_id = "b%d" % self.count
            self._capture = {"id": block_id, "text": []}
            rebuilt += ' data-hg="%s"' % block_id
        self.out.append("<%s%s>" % (tag, rebuilt))
        if tag not in self.VOID:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag == "body":
            self._in_body = False
            return
        if tag in DROP_TAGS:
            self._skip = max(0, self._skip - 1)
            if self._skipping and self._skipping[-1] == tag:
                self._skipping.pop()
            return
        if self._skip or not self._in_body:
            return
        if tag in self.VOID:
            return
        self.depth = max(0, self.depth - 1)
        self.out.append("</%s>" % tag)
        if self.depth == 0 and self._capture:
            self.blocks.append(
                {"id": self._capture["id"],
                 "text": " ".join("".join(self._capture["text"]).split())}
            )
            self._capture = None

    def handle_startendtag(self, tag, attrs):
        if self._skip or not self._in_body:
            return
        if tag in DROP_TAGS:
            return
        rebuilt = "".join(
            ' %s="%s"' % (k, html.escape(v or "", quote=True))
            for k, v in sanitize_attrs(attrs)
        )
        if self.depth == 0 and tag in BLOCK_TAGS:
            self.count += 1
            rebuilt += ' data-hg="b%d"' % self.count
            self.blocks.append({"id": "b%d" % self.count, "text": ""})
        self.out.append("<%s%s>" % (tag, rebuilt))

    def handle_data(self, data):
        if self._skip or not self._in_body:
            return
        self.out.append(html.escape(data, quote=False))
        if self._capture:
            self._capture["text"].append(data)

    def handle_entityref(self, name):
        if self._in_body and not self._skip:
            self.out.append("&%s;" % name)

    def handle_charref(self, name):
        if self._in_body and not self._skip:
            self.out.append("&#%s;" % name)


def build_content(source_text, is_markdown):
    """Return (content_html, [{'id','text'}, ...])."""
    if is_markdown:
        blocks = markdown_blocks(source_text)
        rendered, index = [], []
        for position, block in enumerate(blocks, start=1):
            block_id = "b%d" % position
            rendered.append(render_block(block, block_id))
            index.append({"id": block_id, "text": " ".join(block.get("text", "").split())})
        return "\n".join(rendered), index

    fragment = not re.search(r"<body\b", source_text, re.IGNORECASE)
    tagger = BlockTagger(fragment=fragment)
    tagger.feed(source_text)
    tagger.close()
    if tagger._skipping:
        sys.stderr.write(
            "Warning: unterminated <%s> in the source — everything after it was "
            "dropped. Close the tag if that content should be reviewable.\n"
            % tagger._skipping[0]
        )
    body = "".join(tagger.out).strip()
    if not tagger.blocks and body:
        body = '<div data-hg="b1">%s</div>' % body
        tagger.blocks = [{"id": "b1", "text": " ".join(re.sub(r"<[^>]+>", " ", body).split())}]
    return body, tagger.blocks


# -------------------------------------------------------------- page shell

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Review — __TITLE__</title>
<style>
:root {
  --bg:#fdfcfa; --surface:#fff; --border:#e4e2db; --text:#1b1a16; --muted:#6b6862;
  --accent:#295fcc; --blocker:#b3261e; --major:#a45c00; --minor:#3d6b2e; --nit:#6b6862;
}
@media (prefers-color-scheme: dark) {
  :root { --bg:#16151a; --surface:#1e1d24; --border:#33313c; --text:#eceaf2;
          --muted:#a5a1b0; --accent:#8ab0ff; --blocker:#ff8a80; --major:#f0b357;
          --minor:#8fd07a; --nit:#a5a1b0; }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--text); font:16px/1.65 -apple-system,
  BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; }
header { position:sticky; top:0; z-index:20; display:flex; gap:12px; align-items:center;
  flex-wrap:wrap; padding:10px 16px; background:var(--surface);
  border-bottom:1px solid var(--border); }
header h1 { font-size:15px; margin:0; font-weight:600; }
header .sp { flex:1; }
input, select, textarea, button { font:inherit; color:inherit; background:var(--surface);
  border:1px solid var(--border); border-radius:6px; padding:5px 8px; }
button { cursor:pointer; }
button.primary { background:var(--accent); border-color:var(--accent); color:#fff;
  font-weight:600; }
#counts { font-size:13px; color:var(--muted); }
main { display:grid; grid-template-columns:minmax(0,1fr) 380px; gap:0; align-items:start; }
#doc { padding:32px 28px 120px; max-width:78ch; }
#doc [data-hg] { position:relative; border-radius:6px; transition:background .12s; }
#doc [data-hg]:hover { background:color-mix(in srgb, var(--accent) 7%, transparent); }
#doc [data-hg].tagged { box-shadow:inset 3px 0 0 var(--accent); padding-left:10px; }
#doc [data-hg].active { background:color-mix(in srgb, var(--accent) 14%, transparent); }
#doc h1,#doc h2,#doc h3 { line-height:1.25; margin:1.5em 0 .5em; }
#doc h2 { border-bottom:1px solid var(--border); padding-bottom:.2em; }
#doc pre { background:color-mix(in srgb, var(--text) 6%, transparent); padding:12px 14px;
  border-radius:8px; overflow-x:auto; }
#doc code { font:.88em/1.5 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace; }
#doc table { border-collapse:collapse; width:100%; }
#doc th,#doc td { border:1px solid var(--border); padding:6px 10px; text-align:left; }
#doc blockquote { margin:1em 0; padding:.1em 1em; border-left:3px solid var(--border);
  color:var(--muted); }
#doc img { max-width:100%; height:auto; }
aside { position:sticky; top:53px; height:calc(100vh - 53px); overflow-y:auto;
  border-left:1px solid var(--border); background:var(--surface); padding:14px; }
.item { border:1px solid var(--border); border-radius:8px; padding:10px; margin-bottom:10px; }
.item .row { display:flex; gap:6px; align-items:center; margin-bottom:6px; }
.item .row select { flex:0 0 auto; }
.item .blk { font:12px ui-monospace,monospace; color:var(--muted); flex:1; }
.item textarea { width:100%; min-height:64px; resize:vertical; }
.item blockquote { margin:0 0 6px; padding:4px 8px; border-left:2px solid var(--accent);
  font-size:13px; color:var(--muted); max-height:4.5em; overflow:hidden; }
.sev-BLOCKER { color:var(--blocker); font-weight:700; }
.sev-MAJOR { color:var(--major); font-weight:600; }
.sev-MINOR { color:var(--minor); }
.sev-NIT, .sev-EDIT, .sev-NOTE { color:var(--nit); }
.empty { color:var(--muted); font-size:14px; padding:8px 4px; }
#toast { position:fixed; bottom:18px; left:50%; transform:translateX(-50%);
  background:var(--text); color:var(--bg); padding:9px 16px; border-radius:8px;
  font-size:14px; opacity:0; pointer-events:none; transition:opacity .2s; }
#toast.on { opacity:1; }
@media (max-width:900px) {
  main { grid-template-columns:1fr; }
  aside { position:static; height:auto; border-left:0; border-top:1px solid var(--border); }
}
</style>
</head>
<body>
<header>
  <h1>Review: __TITLE__</h1>
  <span id="counts">no feedback yet</span>
  <span class="sp"></span>
  <label>Reviewer <input id="reviewer" placeholder="your name" size="14"></label>
  <button id="add-note">Overall note</button>
  <button id="copy">Copy</button>
  <button id="export" class="primary">Export feedback</button>
</header>
<main>
  <div id="doc">__CONTENT__</div>
  <aside><div id="items"></div><div class="empty" id="hint">
    Click any block in the document to leave feedback on it.</div></aside>
</main>
<div id="toast"></div>
<script>
const CFG = __CONFIG__;
const KEY = "human-gate:" + CFG.target;
const SEV = ["BLOCKER","MAJOR","MINOR","NIT","EDIT"];
let state = { reviewer:"", items:[], note:"" };

try { const saved = localStorage.getItem(KEY); if (saved) state = JSON.parse(saved); }
catch (e) { /* private mode or corrupt entry — start clean */ }

const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch(e){} };
const blockText = id => (CFG.blocks.find(b => b.id === id) || {}).text || "";

function toast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg; el.classList.add("on");
  setTimeout(() => el.classList.remove("on"), 1600);
}

function render() {
  const wrap = document.getElementById("items");
  wrap.innerHTML = "";
  document.querySelectorAll("#doc [data-hg]").forEach(el => el.classList.remove("tagged"));

  state.items.forEach((item, i) => {
    const node = document.getElementById("doc").querySelector('[data-hg="'+item.block+'"]');
    if (node) node.classList.add("tagged");

    const box = document.createElement("div");
    box.className = "item";

    const row = document.createElement("div");
    row.className = "row";
    const sel = document.createElement("select");
    SEV.forEach(s => {
      const opt = document.createElement("option");
      opt.value = s; opt.textContent = s;
      if (s === item.severity) opt.selected = true;
      sel.appendChild(opt);
    });
    sel.className = "sev-" + item.severity;
    sel.onchange = () => { item.severity = sel.value; save(); render(); };
    const blk = document.createElement("span");
    blk.className = "blk"; blk.textContent = item.block;
    blk.onclick = () => node && node.scrollIntoView({behavior:"smooth", block:"center"});
    const del = document.createElement("button");
    del.textContent = "×"; del.title = "remove";
    del.onclick = () => { state.items.splice(i,1); save(); render(); };
    row.append(sel, blk, del);
    box.appendChild(row);

    if (item.quote) {
      const q = document.createElement("blockquote");
      q.textContent = item.quote;
      box.appendChild(q);
    }

    if (item.severity === "EDIT") {
      const before = document.createElement("textarea");
      before.placeholder = "before (exact current text)";
      before.value = item.before || "";
      before.oninput = () => { item.before = before.value; save(); };
      const after = document.createElement("textarea");
      after.placeholder = "after (your exact replacement — carried across verbatim)";
      after.value = item.after || "";
      after.oninput = () => { item.after = after.value; save(); };
      box.append(before, after);
    } else {
      const body = document.createElement("textarea");
      body.placeholder = "what needs to change, and why";
      body.value = item.feedback || "";
      body.oninput = () => { item.feedback = body.value; save(); update(); };
      box.appendChild(body);
    }
    wrap.appendChild(box);
  });

  const noteBox = document.createElement("div");
  noteBox.className = "item";
  const noteLabel = document.createElement("div");
  noteLabel.className = "row"; noteLabel.innerHTML = "<span class='blk'>OVERALL NOTE</span>";
  const note = document.createElement("textarea");
  note.placeholder = "unanchored commentary (optional)";
  note.value = state.note || "";
  note.oninput = () => { state.note = note.value; save(); };
  noteBox.append(noteLabel, note);
  wrap.appendChild(noteBox);

  document.getElementById("hint").style.display = state.items.length ? "none" : "block";
  update();
}

function update() {
  const tally = {};
  state.items.forEach(i => { tally[i.severity] = (tally[i.severity]||0) + 1; });
  const parts = SEV.filter(s => tally[s]).map(s => tally[s] + " " + s);
  document.getElementById("counts").textContent =
    parts.length ? parts.join(" · ") : "no feedback yet";
}

function addItem(blockId, quote) {
  state.items.push({ block:blockId, severity:"MINOR", quote:quote||"", feedback:"",
                     before:"", after:"" });
  save(); render();
  const boxes = document.querySelectorAll("#items .item textarea");
  if (boxes.length) boxes[boxes.length - 2] && boxes[boxes.length - 2].focus();
}

document.getElementById("doc").addEventListener("click", event => {
  if (event.target.closest("a")) return;
  const node = event.target.closest("[data-hg]");
  if (!node) return;
  const picked = String(window.getSelection());
  addItem(node.getAttribute("data-hg"), picked.trim() || "");
});

document.getElementById("reviewer").oninput = e => { state.reviewer = e.target.value; save(); };
document.getElementById("add-note").onclick = () => {
  document.querySelector("#items .item:last-child textarea").focus();
};

function sidecar() {
  const lines = [];
  lines.push("# Review feedback: " + CFG.target);
  lines.push("<!-- human-gate:v1 target=" + CFG.target + " round=" + CFG.round + " -->");
  lines.push("");
  lines.push("reviewer: " + (state.reviewer || ""));
  lines.push("");
  state.items.forEach(item => {
    lines.push("## " + item.severity + " " + item.block);
    if (item.quote) {
      String(item.quote).split("\\n").forEach(l => lines.push("> " + l));
    }
    if (item.severity === "EDIT") {
      lines.push("- before: " + (item.before || ""));
      lines.push("+ after: " + (item.after || ""));
      if (item.feedback) lines.push(item.feedback);
    } else if (item.feedback) {
      lines.push(item.feedback);
    }
    lines.push("");
  });
  if (state.note && state.note.trim()) {
    lines.push("## NOTE");
    lines.push(state.note.trim());
    lines.push("");
  }
  return lines.join("\\n");
}

document.getElementById("copy").onclick = async () => {
  const text = sidecar();
  try { await navigator.clipboard.writeText(text); toast("Copied — paste into " + CFG.sidecar); }
  catch (e) {
    const ta = document.createElement("textarea");
    ta.value = text; document.body.appendChild(ta); ta.select();
    document.execCommand("copy"); ta.remove();
    toast("Copied — paste into " + CFG.sidecar);
  }
};

document.getElementById("export").onclick = () => {
  const blob = new Blob([sidecar()], {type:"text/markdown"});
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = CFG.sidecar.split("/").pop();
  a.click();
  URL.revokeObjectURL(a.href);
  toast("Saved — move it next to the artifact as " + CFG.sidecar);
};

document.getElementById("reviewer").value = state.reviewer || "";
render();
</script>
</body>
</html>
"""


def build_page(source_text, target_name, sidecar_name, is_markdown, round_number=1):
    content, blocks = build_content(source_text, is_markdown)
    if not blocks:
        return None, []
    config = {
        "target": target_name,
        "sidecar": sidecar_name,
        "round": round_number,
        "blocks": blocks,
    }
    # One pass, so a value that happens to contain another token — a document
    # about this very skill mentioning __TITLE__, or a block whose text lands
    # in the JSON config — can never be re-substituted. Sequential replaces
    # injected the whole config object into the visible body for such a doc.
    slots = {
        "__CONTENT__": content,
        "__TITLE__": html.escape(target_name, quote=False),
        # json.dumps output is embedded in a <script>; neutralise any "</script>"
        "__CONFIG__": json.dumps(config).replace("</", "<\\/"),
    }
    page = re.sub(
        r"__(?:CONTENT|TITLE|CONFIG)__", lambda m: slots[m.group(0)], PAGE
    )
    return page, blocks


def run_sample(output_dir=None):
    """Build both built-in fixtures and report block counts.

    The HTML fixture is a full DOCTYPE document with a bare <meta charset> and
    <link rel=stylesheet> — the shape every real HTML5 page has, and the exact
    shape that once silently produced zero blocks. Exercising it here means a
    regression fails loudly instead of surfacing as "No reviewable blocks".

    Writes into a temp dir unless --output names one, so a sample run never
    litters the caller's working directory.
    """
    import tempfile

    target_dir = output_dir or tempfile.mkdtemp(prefix="human-gate-sample-")
    os.makedirs(target_dir, exist_ok=True)

    # Each fixture asserts a block count plus the URL-handling contract: what
    # must survive sanitization and what must not. The allowances are as much a
    # decision as the blocks are, so they are pinned here rather than left to
    # prose — a reviewed artifact's own assets have to load for the review to be
    # faithful, and a protocol-relative URL cannot execute.
    fixtures = [
        ("quarterly-plan.md", SAMPLE_MD, True, 6, [], []),
        ("landing.html", SAMPLE_HTML, False, 4,
         ['href="//cdn.example.com/pricing"', 'src="https://img.example.com/hero.png"'],
         ["javascript:"]),
    ]
    failures = []
    for name, source, is_md, expected, must_keep, must_drop in fixtures:
        sidecar = os.path.splitext(name)[0] + ".review.md"
        page, blocks = build_page(source, name, sidecar, is_md, 1)
        out_path = os.path.join(target_dir, os.path.splitext(name)[0] + ".review.html")
        if page is None:
            print("  %-20s FAIL — no reviewable blocks" % name)
            failures.append(name)
            continue
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(page)
        problems = []
        if len(blocks) != expected:
            problems.append("expected %d blocks" % expected)
        problems += ["dropped %s" % k for k in must_keep if k not in page]
        problems += ["kept %s" % d for d in must_drop if d in page]
        status = "ok" if not problems else "FAIL — " + "; ".join(problems)
        if problems:
            failures.append(name)
        print("  %-20s %d blocks, %5.1f KB  %s"
              % (name, len(blocks), len(page.encode("utf-8")) / 1024.0, status))

    print("")
    print("Wrote to %s" % target_dir)
    if failures:
        sys.stderr.write("Sample regression: %s\n" % ", ".join(failures))
        return 2
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Build a single-file HTML review page for a Markdown or HTML artifact.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("artifact", nargs="?", help="path to the .md or .html file")
    parser.add_argument("--output", help="where to write the review page")
    parser.add_argument("--round", type=int, default=1, help="review round number")
    parser.add_argument(
        "--sidecar", help="sidecar filename to advertise (default <artifact>.review.md)"
    )
    parser.add_argument(
        "--launch", action="store_true", help="open the page in the default browser"
    )
    parser.add_argument(
        "--sample", action="store_true",
        help="build both built-in fixtures (Markdown + a full HTML5 doc) and check them"
    )
    args = parser.parse_args(argv)

    if args.sample:
        return run_sample(args.output)
    if args.artifact:
        try:
            with open(args.artifact, "r", encoding="utf-8") as handle:
                source = handle.read()
        except OSError as err:
            parser.error("cannot read %s: %s" % (args.artifact, err))
            return 1
        name = os.path.basename(args.artifact)
        is_md = os.path.splitext(name)[1].lower() in (".md", ".markdown")
        base = os.path.splitext(args.artifact)[0]
        out_path = args.output or (base + ".review.html")
    else:
        parser.error("provide an artifact path or --sample")
        return 1

    sidecar = args.sidecar or (os.path.splitext(name)[0] + ".review.md")
    page, blocks = build_page(source, name, sidecar, is_md, args.round)
    if page is None:
        sys.stderr.write("No reviewable blocks found in %s\n" % name)
        return 2

    try:
        with open(out_path, "w", encoding="utf-8") as handle:
            handle.write(page)
    except OSError as err:
        parser.error("cannot write %s: %s" % (out_path, err))
        return 1

    size_kb = len(page.encode("utf-8")) / 1024.0
    print("Review page: %s" % out_path)
    print("Blocks:      %d" % len(blocks))
    print("Size:        %.1f KB (single file, no network requests)" % size_kb)
    print("Sidecar:     %s  <- export lands here, or write it by hand" % sidecar)

    if args.launch:
        import webbrowser

        webbrowser.open("file://" + os.path.abspath(out_path))

    return 0


if __name__ == "__main__":
    sys.exit(main())
