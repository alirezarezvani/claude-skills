#!/usr/bin/env python3
"""timeline_compiler.py — compile a scene.v1 file into one self-contained HTML page.

The page holds every shot and layer and exposes one deterministic function,
window.__seek(t), that draws the exact frame at time t (seconds). Nothing
animates on its own clock, so a renderer can capture frame N at t = N / fps
and get the same pixels every run. Opened in a browser without ?render=1, the
page shows a preview with play/pause and a scrubber.

Add ?plateonly=1 to the URL to hide every layer except images and plates
(used to render clean keyframes for AI shot upgrades).

Modes (meta.mode):
  greybox  the animatic: images and AI plates become labelled grey boxes, so
           the cut can be judged on timing and framing before anything is spent
  final    images, chart colours and plate videos (layer "src") are drawn as is

Data: a chart layer takes inline "data" ([[label, value], ...]) or "csv"
(a two-column file, read at compile time, path relative to the scene file).

Exit codes: 0 compiled, 2 bad input (scene invalid or unreadable).

Examples:
  timeline_compiler.py --sample --out /tmp/animatic.html
  timeline_compiler.py --scene film/scene.json --out film/animatic.html
  timeline_compiler.py --scene film/scene.json --aspect 9:16 --mode final --out film/vertical.html
"""
from __future__ import annotations

import argparse
import csv
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene_model import (ASPECTS, SAMPLE_SCENE, SceneError, load_scene,  # noqa: E402
                         normalize, timeline, total_duration)

ENGINE_JS = r"""
(function () {
  const SCENE = __SCENE_JSON__;
  const W = SCENE.meta.width, H = SCENE.meta.height;
  const MODE = SCENE.meta.mode;
  const TH = SCENE.theme;
  const RENDER = new URLSearchParams(location.search).has('render');
  const PLATEONLY = new URLSearchParams(location.search).has('plateonly');
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, p) => a + (b - a) * p;
  const EASE = {
    'linear': p => p,
    'ease-in': p => p * p * p,
    'ease-out': p => 1 - Math.pow(1 - p, 3),
    'ease-in-out': p => p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2,
    'back-out': p => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2); },
    'expo-out': p => p === 1 ? 1 : 1 - Math.pow(2, -10 * p)
  };
  const color = c => (c && TH[c]) ? TH[c] : (c || TH.fg);
  const STYLE = {
    title:    {size: 0.085, weight: 800, font: 'heading', track: '-0.02em'},
    subtitle: {size: 0.048, weight: 600, font: 'heading', track: '-0.01em'},
    body:     {size: 0.038, weight: 400, font: 'body', track: '0'},
    caption:  {size: 0.032, weight: 500, font: 'body', track: '0'},
    kicker:   {size: 0.026, weight: 700, font: 'body', track: '0.12em', upper: true}
  };
  const short = Math.min(W, H);

  const stage = document.getElementById('stage');
  stage.style.width = W + 'px'; stage.style.height = H + 'px';
  stage.style.background = TH.bg;

  let t0 = 0;
  const shots = SCENE.shots.map((s, i) => {
    const el = document.createElement('div');
    el.className = 'shot'; el.dataset.id = s.id;
    el.style.background = s.bg ? color(s.bg) : TH.bg;
    const cam = document.createElement('div'); cam.className = 'cam';
    const hud = document.createElement('div'); hud.className = 'hud';
    el.appendChild(cam); el.appendChild(hud); stage.appendChild(el);
    const layers = s.layers.map(L => build(L, s, L.fixed || L.type === 'lower_third' ? hud : cam));
    if (SCENE.meta.captions && s.vo) layers.push(build({type: 'text', text: s.vo, style: 'caption',
      x: 0.5, y: 0.9, in: 0, out: s.duration, anim: 'none', box: true}, s, hud));
    const rec = {s, el, cam, layers, start: t0, end: t0 + s.duration, i};
    t0 += s.duration;
    return rec;
  });
  const TOTAL = t0;

  function place(node, L, anchorCenter = true) {
    node.style.position = 'absolute';
    node.style.left = ((L.x ?? 0.5) * W) + 'px';
    node.style.top = ((L.y ?? 0.5) * H) + 'px';
    node.dataset.base = anchorCenter ? 'translate(-50%,-50%)' : '';
  }

  function build(L, s, parent) {
    const n = document.createElement('div');
    const rec = {L, n, kind: L.type, extra: {}};
    if (L.type === 'text') {
      const st = STYLE[L.style || 'body'] || STYLE.body;
      const size = (L.size || st.size) * short;
      n.className = 'txt';
      n.style.fontFamily = (st.font === 'heading' ? TH.font_heading : TH.font_body) + ', system-ui, sans-serif';
      n.style.fontSize = size + 'px'; n.style.fontWeight = L.weight || st.weight;
      n.style.letterSpacing = st.track; n.style.color = color(L.color);
      n.style.textAlign = L.align || 'center';
      n.style.maxWidth = ((L.w || 0.82) * W) + 'px';
      if (st.upper) n.style.textTransform = 'uppercase';
      if (L.box) { n.style.background = 'rgba(0,0,0,0.62)'; n.style.padding = '0.25em 0.6em'; n.style.borderRadius = '0.2em'; }
      const text = L.text || '';
      if (L.anim === 'words') {
        rec.extra.words = text.split(/(\s+)/).map(w => { const sp = document.createElement('span'); sp.textContent = w; sp.style.display = 'inline-block'; sp.style.whiteSpace = 'pre'; n.appendChild(sp); return sp; });
      } else { n.textContent = text; }
      rec.extra.text = text;
      place(n, L);
    } else if (L.type === 'shape') {
      n.className = 'shp';
      n.style.width = ((L.w || 0.2) * W) + 'px'; n.style.height = ((L.h || 0.2) * H) + 'px';
      n.style.background = color(L.color || 'accent');
      if (L.shape === 'circle') n.style.borderRadius = '50%';
      if (L.shape === 'line') n.style.height = Math.max(2, (L.h || 0.004) * H) + 'px';
      if (L.radius) n.style.borderRadius = (L.radius * short) + 'px';
      place(n, L);
    } else if (L.type === 'image' || L.type === 'plate') {
      const full = L.type === 'plate';
      const box = full ? {x: 0.5, y: 0.5, w: 1, h: 1} : L;
      n.style.width = ((box.w || 0.4) * W) + 'px'; n.style.height = ((box.h || 0.4) * H) + 'px';
      n.style.overflow = 'hidden';
      const label = L.label || L.src || (full ? (s.upgrade_prompt || 'AI plate') : 'image');
      if (MODE === 'greybox' || !L.src) {
        n.className = full ? 'grey plate' : 'grey';
        n.innerHTML = '<span>' + (full ? 'PLATE · ' : 'IMG · ') + escapeHtml(label) + '</span>';
        n.querySelector('span').style.fontSize = (0.024 * short) + 'px';
      } else if (/\.(mp4|webm|mov)$/i.test(L.src)) {
        const v = document.createElement('video');
        v.src = L.src; v.muted = true; v.preload = 'auto'; v.playsInline = true;
        v.style.width = '100%'; v.style.height = '100%'; v.style.objectFit = L.fit || 'cover';
        n.appendChild(v); rec.extra.video = v;
      } else {
        const im = document.createElement('img'); im.src = L.src;
        im.style.width = '100%'; im.style.height = '100%'; im.style.objectFit = L.fit || 'cover';
        n.appendChild(im); rec.extra.img = im;
      }
      place(n, box);
    } else if (L.type === 'chart') {
      const cw = (L.w || 0.6) * W, ch = (L.h || 0.45) * H;
      n.style.width = cw + 'px'; n.style.height = ch + 'px';
      const NS = 'http://www.w3.org/2000/svg';
      const svg = document.createElementNS(NS, 'svg');
      svg.setAttribute('width', cw); svg.setAttribute('height', ch);
      n.appendChild(svg);
      const data = L.data || [];
      const max = Math.max(...data.map(d => +d[1]), 1);
      const fs = 0.024 * short;
      const top = (L.title ? fs * 2.2 : fs * 0.5) + fs * 1.8, bottom = fs * 2.0;
      if (L.title) { const tt = document.createElementNS(NS, 'text'); tt.textContent = L.title; tt.setAttribute('x', cw / 2); tt.setAttribute('y', fs * 1.2); tt.setAttribute('text-anchor', 'middle'); tt.setAttribute('fill', TH.muted); tt.setAttribute('font-size', fs); tt.setAttribute('font-family', TH.font_body + ', system-ui'); svg.appendChild(tt); }
      const plotH = ch - top - bottom;
      const fill = MODE === 'greybox' ? '#c9cdd6' : color(L.color || 'accent');
      rec.extra.bars = []; rec.extra.vals = [];
      if ((L.kind || 'bar') === 'bar') {
        const gap = cw / data.length;
        data.forEach((d, k) => {
          const r = document.createElementNS(NS, 'rect');
          const bw = gap * 0.62;
          r.setAttribute('x', k * gap + (gap - bw) / 2); r.setAttribute('width', bw); r.setAttribute('fill', fill); r.setAttribute('rx', bw * 0.06);
          svg.appendChild(r);
          const lab = document.createElementNS(NS, 'text'); lab.textContent = d[0]; lab.setAttribute('x', k * gap + gap / 2); lab.setAttribute('y', ch - bottom + fs * 1.3); lab.setAttribute('text-anchor', 'middle'); lab.setAttribute('fill', TH.fg); lab.setAttribute('font-size', fs); lab.setAttribute('font-family', TH.font_body + ', system-ui'); svg.appendChild(lab);
          const val = document.createElementNS(NS, 'text'); val.setAttribute('x', k * gap + gap / 2); val.setAttribute('text-anchor', 'middle'); val.setAttribute('fill', TH.fg); val.setAttribute('font-size', fs * 1.1); val.setAttribute('font-weight', 700); val.setAttribute('font-family', TH.font_body + ', system-ui'); svg.appendChild(val);
          rec.extra.bars.push({r, val, v: +d[1], h: plotH * (+d[1] / max), base: top + plotH});
        });
      } else {
        const pl = document.createElementNS(NS, 'polyline');
        const pts = data.map((d, k) => [(k / Math.max(1, data.length - 1)) * cw, top + plotH - plotH * (+d[1] / max)]);
        pl.setAttribute('points', pts.map(p => p.join(',')).join(' '));
        pl.setAttribute('fill', 'none'); pl.setAttribute('stroke', fill); pl.setAttribute('stroke-width', 0.008 * short);
        pl.setAttribute('stroke-linejoin', 'round'); pl.setAttribute('stroke-linecap', 'round');
        svg.appendChild(pl);
        let len = 0; for (let k = 1; k < pts.length; k++) len += Math.hypot(pts[k][0] - pts[k - 1][0], pts[k][1] - pts[k - 1][1]);
        pl.style.strokeDasharray = len; rec.extra.line = {pl, len};
      }
      place(n, L);
    } else if (L.type === 'counter') {
      const st = STYLE[L.style || 'title'] || STYLE.title;
      n.className = 'txt';
      n.style.fontFamily = TH.font_heading + ', system-ui, sans-serif';
      n.style.fontSize = ((L.size || st.size) * short) + 'px'; n.style.fontWeight = st.weight;
      n.style.color = color(L.color || 'accent'); n.style.fontVariantNumeric = 'tabular-nums';
      place(n, L);
    } else if (L.type === 'lower_third') {
      n.className = 'l3';
      const bar = document.createElement('div'); bar.className = 'l3bar'; bar.style.background = color(L.color || 'accent');
      const t1 = document.createElement('div'); t1.textContent = L.title || ''; t1.style.fontSize = (0.036 * short) + 'px'; t1.style.fontWeight = 700;
      const t2 = document.createElement('div'); t2.textContent = L.subtitle || ''; t2.style.fontSize = (0.024 * short) + 'px'; t2.style.color = TH.muted;
      const txt = document.createElement('div'); txt.appendChild(t1); txt.appendChild(t2);
      n.appendChild(bar); n.appendChild(txt);
      n.style.fontFamily = TH.font_body + ', system-ui'; n.style.color = TH.fg;
      n.style.gap = (0.016 * short) + 'px';
      bar.style.width = (0.008 * short) + 'px';
      place(n, {x: L.x ?? 0.07, y: L.y ?? 0.8}, false);
      n.dataset.base = 'translate(0,-50%)';
    }
    parent.appendChild(n);
    return rec;
  }

  function escapeHtml(s) { return String(s).replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c])); }

  function fmt(v, L) {
    const d = L.decimals || 0;
    const num = Number(v).toLocaleString('en-US', {minimumFractionDigits: d, maximumFractionDigits: d});
    return (L.prefix || '') + num + (L.suffix || '');
  }

  function drawLayer(rec, lt, sdur) {
    const L = rec.L, n = rec.n;
    const inDur = L.dur || (L.anim === 'type' || L.anim === 'words' ? Math.max(0.6, (rec.extra.text || '').length * 0.03) : 0.7);
    const ease = EASE[L.ease] || EASE['expo-out'];
    const visible = lt >= L.in && lt < L.out && !(PLATEONLY && L.type !== 'plate' && L.type !== 'image');
    n.style.visibility = visible ? 'visible' : 'hidden';
    if (!visible) return;
    const p = ease(clamp((lt - L.in) / inDur, 0, 1));
    const outFade = L.out < sdur ? clamp((L.out - lt) / 0.3, 0, 1) : 1;
    let tf = n.dataset.base || '', op = 1;
    switch (L.anim) {
      case 'fade': op = p; break;
      case 'rise': op = p; tf += ` translateY(${(1 - p) * 0.04 * H}px)`; break;
      case 'slide': op = p; tf += ` translateX(${(1 - p) * -0.06 * W}px)`; break;
      case 'scale': op = p; tf += ` scale(${lerp(0.86, 1, p)})`; break;
      case 'draw': tf += ` scaleX(${p})`; break;
      case 'kenburns': tf += ` scale(${lerp(1, 1.08, clamp((lt - L.in) / Math.max(0.01, L.out - L.in), 0, 1))})`; op = clamp((lt - L.in) / 0.4, 0, 1); break;
      case 'type': n.textContent = rec.extra.text.slice(0, Math.round(rec.extra.text.length * clamp((lt - L.in) / inDur, 0, 1))); break;
      case 'words': {
        const ws = rec.extra.words, k = ws.length;
        ws.forEach((sp, i) => { const q = ease(clamp(((lt - L.in) - i * (inDur / Math.max(1, k)) * 0.8) / 0.45, 0, 1)); sp.style.opacity = q; sp.style.transform = `translateY(${(1 - q) * 0.3}em)`; });
        break;
      }
      default: break;
    }
    if (L.type === 'lower_third') { op = p; tf += ` translateX(${(1 - p) * -0.05 * W}px)`; }
    if (L.type === 'counter') {
      const q = ease(clamp((lt - L.in) / (L.dur || 1.4), 0, 1));
      n.textContent = fmt(lerp(L.from || 0, L.to || 0, q), L); op = clamp((lt - L.in) / 0.25, 0, 1);
    }
    if (L.type === 'chart') {
      const q = clamp((lt - L.in) / (L.dur || 1.4), 0, 1);
      if (rec.extra.bars.length) {
        rec.extra.bars.forEach((b, i) => {
          const qi = ease(clamp(q * 1.4 - i * 0.12, 0, 1));
          const hh = b.h * qi;
          b.r.setAttribute('y', b.base - hh); b.r.setAttribute('height', Math.max(0, hh));
          b.val.setAttribute('y', b.base - hh - 0.012 * short); b.val.textContent = qi > 0.02 ? fmt(b.v * qi, L) : '';
        });
      } else if (rec.extra.line) {
        rec.extra.line.pl.style.strokeDashoffset = rec.extra.line.len * (1 - ease(q));
      }
    }
    n.style.opacity = op * outFade;
    n.style.transform = tf.trim();
  }

  function camera(rec, lt) {
    const c = rec.s.camera || {}, a = c.amount ?? 0.06;
    const p = (EASE[c.ease] || EASE['ease-in-out'])(clamp(lt / rec.s.duration, 0, 1));
    let tf = '';
    switch (c.move) {
      case 'push-in': tf = `scale(${1 + a * p})`; break;
      case 'pull-out': tf = `scale(${1 + a * (1 - p)})`; break;
      case 'pan-left': tf = `scale(${1 + a}) translateX(${lerp(a / 2, -a / 2, p) * W}px)`; break;
      case 'pan-right': tf = `scale(${1 + a}) translateX(${lerp(-a / 2, a / 2, p) * W}px)`; break;
      case 'tilt-up': tf = `scale(${1 + a}) translateY(${lerp(-a / 2, a / 2, p) * H}px)`; break;
      case 'tilt-down': tf = `scale(${1 + a}) translateY(${lerp(a / 2, -a / 2, p) * H}px)`; break;
      case 'drift': tf = `scale(${1 + a}) translate(${Math.sin(p * Math.PI) * a * 0.3 * W}px, ${(p - 0.5) * a * 0.4 * H}px)`; break;
      default: tf = '';
    }
    rec.cam.style.transform = tf;
  }

  async function seek(t) {
    t = clamp(t, 0, Math.max(0, TOTAL - 1e-6));
    const waits = [];
    shots.forEach((rec, i) => {
      const s = rec.s, td = s.transition_duration || 0;
      const next = shots[i + 1];
      const holdForNext = next && next.s.transition === 'fade' ? (next.s.transition_duration || 0) : 0;
      let lt = t - rec.start, op = 0;
      if (t >= rec.start && t < rec.end) {
        op = 1;
        if (s.transition === 'fade' && i > 0) op = clamp(lt / Math.max(0.001, td), 0, 1);
        if (s.transition === 'dip' && i > 0) op = clamp((lt - td / 2) / Math.max(0.001, td / 2), 0, 1);
      } else if (t >= rec.end && t < rec.end + holdForNext) {
        op = 1; lt = s.duration - 1e-6;
      }
      if (next && next.s.transition === 'dip' && t >= rec.end - (next.s.transition_duration || 0) / 2 && t < rec.end) {
        op = Math.min(op, clamp((rec.end - t) / Math.max(0.001, (next.s.transition_duration || 0) / 2), 0, 1));
      }
      rec.el.style.opacity = op;
      rec.el.style.visibility = op > 0 ? 'visible' : 'hidden';
      rec.el.style.zIndex = i;
      if (op > 0) {
        camera(rec, lt);
        rec.layers.forEach(l => {
          drawLayer(l, lt, s.duration);
          const v = l.extra.video;
          if (v) waits.push(new Promise(res => { const target = clamp(lt - l.L.in, 0, (v.duration || 1e9) - 0.001); if (Math.abs(v.currentTime - target) < 1e-3) return res(); v.addEventListener('seeked', () => res(), {once: true}); v.currentTime = target; }));
        });
      }
    });
    if (document.fonts && document.fonts.ready) waits.push(document.fonts.ready);
    await Promise.all(waits);
    return t;
  }

  window.__scene = SCENE;
  window.__duration = TOTAL;
  window.__seek = seek;
  window.__ready = (async () => {
    const imgs = [...document.images].map(im => im.complete ? 1 : new Promise(r => { im.onload = im.onerror = r; }));
    await Promise.all(imgs);
    if (document.fonts && document.fonts.ready) await document.fonts.ready;
    await seek(0);
    return true;
  })();

  if (!RENDER) {
    document.body.classList.add('preview');
    const fit = () => { const sc = Math.min((innerWidth - 32) / W, (innerHeight - 96) / H, 1); stage.style.transform = `scale(${sc})`; document.getElementById('wrap').style.height = (H * sc) + 'px'; document.getElementById('wrap').style.width = (W * sc) + 'px'; };
    addEventListener('resize', fit); fit();
    const bar = document.getElementById('scrub'), lab = document.getElementById('time'), btn = document.getElementById('play');
    bar.max = TOTAL; let playing = false, last = 0, cur = 0;
    const show = () => { lab.textContent = cur.toFixed(2) + ' / ' + TOTAL.toFixed(2) + 's'; bar.value = cur; };
    bar.addEventListener('input', () => { cur = +bar.value; seek(cur); show(); });
    const tick = now => { if (!playing) return; cur += (now - last) / 1000; last = now; if (cur >= TOTAL) { cur = 0; } seek(cur); show(); requestAnimationFrame(tick); };
    btn.addEventListener('click', () => { playing = !playing; btn.textContent = playing ? 'Pause' : 'Play'; last = performance.now(); if (playing) requestAnimationFrame(tick); });
    addEventListener('keydown', e => { if (e.code === 'Space') { e.preventDefault(); btn.click(); } });
    show();
  }
})();
"""

PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
__FONTS__
<style>
  html, body { margin: 0; padding: 0; background: #000; }
  body.preview { background: #15171c; color: #e8eaef; font: 14px system-ui, sans-serif;
    display: flex; flex-direction: column; align-items: center; padding: 16px; box-sizing: border-box; }
  #wrap { position: relative; overflow: hidden; }
  #stage { position: relative; overflow: hidden; transform-origin: 0 0; }
  .shot, .cam, .hud { position: absolute; inset: 0; }
  .cam { transform-origin: 50% 50%; will-change: transform; }
  .txt { white-space: pre-wrap; line-height: 1.12; }
  .grey { display: flex; align-items: center; justify-content: center; text-align: center;
    background: repeating-linear-gradient(45deg, #3a3f4a 0 24px, #343843 24px 48px);
    color: #d6d9e0; border: 2px dashed #8a93a6; box-sizing: border-box; font-family: system-ui, sans-serif; }
  .grey.plate { align-items: flex-start; justify-content: flex-start; }
  .grey.plate span { margin: 2.5%; }
  .grey span { background: rgba(0,0,0,0.55); padding: 0.4em 0.8em; border-radius: 0.3em; max-width: 80%; }
  .l3 { display: flex; align-items: stretch; }
  .l3bar { border-radius: 2px; }
  #controls { display: none; gap: 12px; align-items: center; margin-top: 12px; width: min(100%, 960px); }
  body.preview #controls { display: flex; }
  #scrub { flex: 1; }
  button { font: inherit; padding: 6px 14px; border-radius: 6px; border: 1px solid #4a5060; background: #252830; color: inherit; cursor: pointer; }
  #time { font-variant-numeric: tabular-nums; min-width: 9em; text-align: right; }
  @media (prefers-reduced-motion: reduce) { body.preview #play { display: none; } }
</style>
</head>
<body>
<div id="wrap"><div id="stage"></div></div>
<div id="controls"><button id="play">Play</button><input id="scrub" type="range" min="0" step="0.01" value="0"><span id="time"></span></div>
<script>
__ENGINE__
</script>
</body>
</html>
"""

GOOGLE_SAFE = {"Inter", "Roboto", "Open Sans", "Lato", "Montserrat", "Poppins", "Source Sans 3",
               "IBM Plex Sans", "IBM Plex Serif", "Playfair Display", "Merriweather", "Space Grotesk",
               "DM Sans", "Manrope", "JetBrains Mono"}


def read_csv_data(path: Path) -> list:
    rows = []
    with path.open(newline="", encoding="utf-8") as fh:
        for i, row in enumerate(csv.reader(fh)):
            if len(row) < 2:
                continue
            try:
                rows.append([row[0], float(row[1])])
            except ValueError:
                if i == 0:
                    continue  # header row
                raise SceneError(f"{path}: row {i + 1} value is not a number: {row[1]!r}")
    if not rows:
        raise SceneError(f"{path}: no numeric rows")
    return rows


def resolve_assets(scene: dict, base: Path) -> dict:
    """Inline chart CSVs and make relative media paths relative to the output page."""
    for shot in scene["shots"]:
        for layer in shot["layers"]:
            if layer["type"] == "chart" and layer.get("csv") and not layer.get("data"):
                layer["data"] = read_csv_data((base / layer["csv"]).resolve())
            if layer["type"] == "chart" and not layer.get("data"):
                raise SceneError(f"shot {shot['id']}: chart layer needs data or csv")
    return scene


def fonts_link(theme: dict, offline: bool) -> str:
    if offline:
        return ""
    fams = []
    for key in ("font_heading", "font_body"):
        f = theme.get(key)
        if f in GOOGLE_SAFE and f not in fams:
            fams.append(f)
    if not fams:
        return ""
    q = "&".join("family=" + f.replace(" ", "+") + ":wght@400;500;600;700;800" for f in fams)
    return f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{q}&display=block">'


def compile_scene(scene: dict, offline: bool = False) -> str:
    payload = json.dumps(scene, ensure_ascii=False).replace("<", "\\u003c")  # no </script>, <!-- or <script in the page
    engine = ENGINE_JS.replace("__SCENE_JSON__", payload)
    return (PAGE.replace("__TITLE__", html.escape(scene["meta"].get("title", "Animatic")))
                .replace("__FONTS__", fonts_link(scene["theme"], offline))
                .replace("__ENGINE__", engine))


def main() -> int:
    ap = argparse.ArgumentParser(description="Compile a scene.v1 JSON file into a self-contained, seekable HTML animatic.")
    ap.add_argument("--scene", help="Path to scene.v1 JSON.")
    ap.add_argument("--sample", action="store_true", help="Compile the built-in sample scene.")
    ap.add_argument("--out", help="Output HTML path (default: animatic.html next to the scene, or stdout summary only with --sample).")
    ap.add_argument("--aspect", choices=sorted(ASPECTS), help="Override meta.aspect (re-frame the same scene).")
    ap.add_argument("--mode", choices=["greybox", "final"], help="Override meta.mode.")
    ap.add_argument("--offline", action="store_true", help="Do not link Google Fonts (system fonts only).")
    ap.add_argument("--output", choices=["text", "json"], default="text", help="Summary format.")
    args = ap.parse_args()

    try:
        if args.sample or not args.scene:
            raw = json.loads(json.dumps(SAMPLE_SCENE))
            base = Path.cwd()
        else:
            raw = json.loads(Path(args.scene).read_text(encoding="utf-8"))
            base = Path(args.scene).resolve().parent
        if args.aspect:
            raw.setdefault("meta", {})["aspect"] = args.aspect
            raw["meta"].pop("width", None)
            raw["meta"].pop("height", None)
        if args.mode:
            raw.setdefault("meta", {})["mode"] = args.mode
        scene = resolve_assets(normalize(raw), base)
    except (SceneError, FileNotFoundError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    page = compile_scene(scene, offline=args.offline)
    out = args.out
    if out is None and not (args.sample or not args.scene):
        out = str(Path(args.scene).resolve().parent / "animatic.html")
    if out:
        Path(out).parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(page, encoding="utf-8")

    summary = {
        "html": out,
        "bytes": len(page.encode("utf-8")),
        "mode": scene["meta"]["mode"],
        "canvas": [scene["meta"]["width"], scene["meta"]["height"]],
        "fps": scene["meta"]["fps"],
        "duration": total_duration(scene),
        "shots": timeline(scene),
        "next": "open the HTML in a browser to preview, then frame_renderer.py to render frames",
    }
    if args.output == "json":
        print(json.dumps(summary, indent=2))
    else:
        print(f"compiled {len(scene['shots'])} shots, {summary['duration']:.2f}s, "
              f"{summary['canvas'][0]}x{summary['canvas'][1]} @ {summary['fps']}fps, mode={summary['mode']}")
        print(f"html: {out or '(not written; pass --out)'} ({summary['bytes']} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
