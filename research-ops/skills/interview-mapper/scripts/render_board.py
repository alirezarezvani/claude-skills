#!/usr/bin/env python3
"""
render_board.py — a standalone HTML board of insights from provenance.json (or scored.json).

One self-contained .html: insight cards with a filter by status/role, each piece of evidence
with interview/line and a verified/support mark. Loads nothing from the network — the data is embedded.

CLI: python render_board.py provenance.json [--out board.html] [--title "Insights: Museum"]
"""

import argparse
import json
import html
import sys


def _read_json(path):
    """Read a JSON file; broken JSON or a missing file → a clear error, exit 1."""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except OSError as e:
        sys.exit(f"error: {path}: {e.strerror or e}")
    except UnicodeDecodeError as e:
        sys.exit(f"error: {path}: not UTF-8 ({e.reason})")
    except json.JSONDecodeError as e:
        sys.exit(
            f"error: {path}: invalid JSON — line {e.lineno}, column {e.colno} ({e.msg})"
        )


def get_clusters(data):
    """Extracts the list of clusters from either provenance.json or scored.json."""
    if "provenance" in data:
        return data["provenance"]
    return data.get("clusters", [])


TPL = """<!doctype html><html lang=en><meta charset=utf-8>
<title>{title}</title>
<style>
:root{{--paper:#fdfbf7;--ink:#1a1a1a;--pencil:#5a564c;--faint:#8a8578;--line:#e0ddd3;--rule:#c9c5b8;--flag:#a8402e}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.6 Georgia,Charter,"Times New Roman",serif}}
header{{padding:22px 28px 16px;border-bottom:1px solid var(--ink)}}
h1{{margin:0 0 4px;font-size:19px;font-weight:700;letter-spacing:.2px}}
.sub{{color:var(--pencil);font-size:12.5px;font-style:italic}}
.bar{{padding:12px 28px;display:flex;gap:6px;flex-wrap:wrap;align-items:center;border-bottom:1px solid var(--line);
 font-family:"Courier New",monospace;font-size:11px;text-transform:uppercase;letter-spacing:.4px}}
.bar button{{background:none;color:var(--pencil);border:1px solid var(--rule);border-radius:0;padding:3px 9px;cursor:pointer;
 font:inherit;text-transform:inherit;letter-spacing:inherit}}
.bar button.on{{background:var(--ink);color:var(--paper);border-color:var(--ink)}}
.bar .sep{{color:var(--rule);padding:0 2px}}
.wrap{{padding:22px 28px;display:grid;gap:24px 28px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}
.card{{border-top:1px solid var(--ink);padding-top:10px}}
.card.watchlist{{border-top-color:var(--rule)}}
.card.weak{{border-top:1px dashed var(--rule)}}
.head{{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:6px}}
.title{{font-weight:700;font-size:15px}}
.card.weak .title{{color:var(--faint);font-weight:400}}
.n{{font-family:"Courier New",monospace;font-size:10.5px;color:var(--pencil)}}
.status{{font-family:"Courier New",monospace;font-size:10.5px;text-transform:uppercase;letter-spacing:.5px;
 display:inline-block;border-bottom:2px solid var(--ink);padding-bottom:2px;margin-bottom:6px}}
.card.watchlist .status{{border-bottom-color:var(--rule);color:var(--pencil)}}
.card.weak .status{{border-bottom:2px dashed var(--rule);color:var(--faint)}}
.ten{{font-style:italic;font-size:12px;color:var(--pencil);margin-bottom:6px}}
.meta{{color:var(--pencil);font-size:12px;margin-bottom:6px}}
.card.weak .meta{{color:var(--faint)}}
.ev{{border-top:1px solid var(--line);padding:9px 0;font-size:13.5px}}
.card.weak .ev{{border-top-style:dashed;color:var(--pencil)}}
.who{{font-family:"Courier New",monospace;color:var(--faint);font-size:10.5px;margin-top:4px}}
.bad{{color:var(--flag);border-bottom:1px solid var(--flag)}}.ok{{color:var(--pencil)}}
</style>
<header><h1>{title}</h1><div class=sub>{sub}</div></header>
<div class=bar id=filters></div>
<div class=wrap id=wrap></div>
<script>
const DATA={data};
const wrap=document.getElementById('wrap'),filters=document.getElementById('filters');
let statusF='all',roleF='all';
const roles=[...new Set(DATA.flatMap(c=>c.roles||[]))];
function mk(el,cls,txt){{const e=document.createElement(el);if(cls)e.className=cls;if(txt!=null)e.textContent=txt;return e;}}
function btn(label,active,fn){{const b=mk('button',active?'on':'',label);b.onclick=fn;return b;}}
function renderFilters(){{filters.replaceChildren();
 ['all','insight','watchlist','weak'].forEach(s=>filters.append(btn(s,statusF===s,()=>{{statusF=s;draw();}})));
 filters.append(mk('span','sep','·'));
 ['all',...roles].forEach(r=>filters.append(btn(r,roleF===r,()=>{{roleF=r;draw();}})));
}}
function draw(){{renderFilters();wrap.replaceChildren();
 DATA.filter(c=>(statusF==='all'||c.status===statusF)&&(roleF==='all'||(c.roles||[]).includes(roleF)))
 .forEach(c=>{{
  const card=mk('div','card '+c.status);
  const head=mk('div','head');
  head.append(mk('span','title',c.title||c.cluster));
  const n=[];
  if(c.prevalence)n.push('prev '+c.prevalence);
  if(c.severity!=null)n.push('sev '+c.severity);
  head.append(mk('span','n',n.join(' · ')));
  card.append(head);
  card.append(mk('div','status',c.status+(c.triangulated?' · triangulated':'')));
  if(c.tension)card.append(mk('div','ten','⚡ tension'));
  card.append(mk('div','meta','roles: '+((c.roles||[]).join(', '))));
  (c.evidence||[]).forEach(e=>{{
   const ev=mk('div','ev');
   ev.append(mk('div','','«'+(e.quote||'')+'»'));
   const w=mk('div','who',(e.interview||'?')+(e.role?' · '+e.role:'')+(e.line?' · L'+e.line:''));
   if(e.verified===false)w.append(mk('span','bad',' ⚠ not verified'));
   if(e.support==='no')w.append(mk('span','bad',' ⚠ does not support'));
   if(e.support==='yes')w.append(mk('span','ok',' ⊨'));
   ev.append(w);card.append(ev);
  }});
  wrap.append(card);
 }});
 if(!wrap.children.length)wrap.append(mk('div','sub','Nothing matches the filter.'));
}}
draw();
</script></html>"""

SAMPLE_DATA = {
    "summary": {"insights": {"total_interviews": 3}},
    "provenance": [
        {
            "cluster": "export-distrust",
            "status": "insight",
            "prevalence": "3/3",
            "roles": ["customer"],
            "severity": 4.0,
            "triangulated": True,
            "tension": False,
            "evidence": [
                {
                    "interview": "P1",
                    "role": "customer",
                    "line": 4,
                    "verified": True,
                    "support": "yes",
                    "quote": "The export didn't match what I saw on screen, so I stopped trusting it",
                },
            ],
        }
    ],
}


def main():
    """CLI: builds a standalone HTML insight board from provenance/scored JSON."""
    ap = argparse.ArgumentParser(
        description="Build a standalone HTML insight board from provenance/scored JSON."
    )
    ap.add_argument(
        "data", nargs="?", help="Output of build_provenance.py or score_insights.py"
    )
    ap.add_argument("--out", default=None)
    ap.add_argument("--title", default="Insights from interviews")
    ap.add_argument(
        "--sample", action="store_true", help="Run on built-in sample provenance data"
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    if a.sample:
        data = SAMPLE_DATA
    else:
        if not a.data:
            sys.exit("error: data is required unless --sample is given")
        data = _read_json(a.data)
    clusters = get_clusters(data)
    summary = data.get("summary", {}) or {}
    # provenance.json: summary.insights is a dict with its own total_interviews;
    # scored.json: summary.insights is an int, interviews live in summary.total_interviews.
    insights = summary.get("insights")
    if isinstance(insights, dict):
        n_iv = insights.get("total_interviews", "?")
    else:
        n_iv = summary.get("total_interviews", "?")
    sub = f"clusters: {len(clusters)} · interviews: {n_iv} · solid=insight, thin=watchlist, dashed=weak"
    htmlout = TPL.format(
        title=html.escape(a.title),
        sub=html.escape(str(sub)),
        data=json.dumps(clusters, ensure_ascii=False),
    )

    out_path = None
    if a.out or not a.sample:
        out_path = a.out or "board.html"
        open(out_path, "w", encoding="utf-8").write(htmlout)

    if a.output == "json":
        print(
            json.dumps(
                {
                    "out": out_path,
                    "card_count": len(clusters),
                    "interviews": n_iv,
                    "html_bytes": len(htmlout),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(
            f"Board: {len(clusters)} cards → {out_path or '(sample, no --out given)'}"
        )


if __name__ == "__main__":
    main()
