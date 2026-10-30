/*
 * design-qa rendered snapshot collector.
 *
 * Reads computed values from the page as the browser actually rendered it and
 * returns JSON for scripts/rendered_audit.py. Read-only: it focuses elements to
 * probe the focus indicator but never clicks, types or sends anything.
 *
 * Use it one of two ways:
 *   1. DevTools console: paste this file, then run
 *        copy(JSON.stringify(designQaSnapshot(), null, 1))
 *      and save the clipboard to snapshot.json. Focus results from the console
 *      are "unverified" because script focus does not always trigger
 *      :focus-visible; use way 2 for a real keyboard pass.
 *   2. assets/capture_snapshot.mjs (Playwright) injects this file, presses Tab
 *      through the page with real key events and merges the focus results.
 */
(function (global) {
  const INTERACTIVE = 'a[href], button, input:not([type="hidden"]), select, textarea, summary, ' +
    '[role="button"], [role="link"], [role="checkbox"], [role="radio"], [role="switch"], [role="tab"], ' +
    '[role="menuitem"], [role="option"], [tabindex]:not([tabindex="-1"]), [contenteditable="true"]';
  const FOCUS_PROPS = ['outlineStyle', 'outlineWidth', 'outlineColor', 'boxShadow', 'borderColor',
    'backgroundColor', 'textDecorationLine', 'color'];

  function parseColor(c) {
    const m = c && c.match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    const p = m[1].split(/[,\s/]+/).filter(Boolean).map(Number);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function rgb(c) { return `rgb(${Math.round(c.r)}, ${Math.round(c.g)}, ${Math.round(c.b)})`; }

  // Composite what the eye sees at an element: its text (optional) over its own
  // background, then each ancestor's background, with every element's `opacity`
  // applied to its whole subtree, over a white canvas. Premultiplied alpha.
  // Any background image or gradient on the way makes the result unknown.
  const pm = c => ({ r: c.r * c.a, g: c.g * c.a, b: c.b * c.a, a: c.a });
  const over = (s, d) => ({ r: s.r + d.r * (1 - s.a), g: s.g + d.g * (1 - s.a), b: s.b + d.b * (1 - s.a), a: s.a + d.a * (1 - s.a) });
  const scale = (c, o) => ({ r: c.r * o, g: c.g * o, b: c.b * o, a: c.a * o });
  function compositeAt(el, fg) {
    let acc = fg ? pm(fg) : { r: 0, g: 0, b: 0, a: 0 };
    for (let n = el; n && n.nodeType === 1; n = n.parentElement) {
      const s = getComputedStyle(n);
      if (s.backgroundImage && s.backgroundImage !== 'none') return { value: null, reason: 'background image or gradient' };
      const c = parseColor(s.backgroundColor);
      if (c && c.a > 0) acc = over(acc, pm(c));
      acc = scale(acc, parseFloat(s.opacity));
    }
    const out = over(acc, { r: 255, g: 255, b: 255, a: 1 });
    return { value: { r: out.r, g: out.g, b: out.b, a: 1 }, reason: null };
  }

  function accessibleName(el) {
    const by = el.getAttribute('aria-labelledby');
    if (by) return by.split(/\s+/).map(id => (document.getElementById(id) || {}).textContent || '').join(' ').trim();
    const al = el.getAttribute('aria-label');
    if (al && al.trim()) return al.trim();
    if (el.labels && el.labels.length) return Array.from(el.labels).map(l => l.textContent).join(' ').trim();
    if (el.tagName === 'IMG') return (el.getAttribute('alt') || '').trim();
    const t = (el.innerText || el.textContent || '').trim();
    if (t) return t.slice(0, 120);
    const img = el.querySelector('img[alt], svg[aria-label], [aria-label]');
    if (img) return (img.getAttribute('alt') || img.getAttribute('aria-label') || '').trim();
    return (el.getAttribute('title') || el.getAttribute('placeholder') || el.value || '').toString().trim();
  }

  function selectorFor(el) {
    if (el.id) return '#' + CSS.escape(el.id);
    const parts = [];
    for (let n = el; n && n.nodeType === 1 && parts.length < 4; n = n.parentElement) {
      let p = n.tagName.toLowerCase();
      if (n.parentElement) {
        const sib = Array.from(n.parentElement.children).filter(x => x.tagName === n.tagName);
        if (sib.length > 1) p += `:nth-of-type(${sib.indexOf(n) + 1})`;
      }
      parts.unshift(p);
      if (n.id) { parts[0] = '#' + CSS.escape(n.id); break; }
    }
    return parts.join(' > ');
  }

  function visible(el, s, r) {
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && parseFloat(s.opacity) > 0;
  }

  function isInline(el) {
    // A target inside running text (WCAG 2.5.8 "Inline" exception).
    const p = el.parentElement;
    if (!p || el.tagName !== 'A') return false;
    const ps = getComputedStyle(p);
    const text = Array.from(p.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
    return ps.display !== 'flex' && ps.display !== 'grid' && text.length > 20;
  }

  function focusProbe(el) {
    const before = {}; const s0 = getComputedStyle(el);
    FOCUS_PROPS.forEach(k => { before[k] = s0[k]; });
    el.focus({ preventScroll: false });
    if (document.activeElement !== el) return { indicator: null, obscured: null, how: 'not focusable by script' };
    const s1 = getComputedStyle(el);
    const changed = FOCUS_PROPS.filter(k => before[k] !== s1[k]);
    const outlineOn = s1.outlineStyle !== 'none' && parseFloat(s1.outlineWidth) > 0;
    const shadowOn = s1.boxShadow && s1.boxShadow !== 'none';
    let indicator = outlineOn || shadowOn || changed.length > 0;
    const how = el.matches(':focus-visible') ? 'focus-visible' : 'script-focus';
    if (!indicator && how !== 'focus-visible') indicator = null; // cannot tell without a real keyboard pass
    const r = el.getBoundingClientRect();
    const pts = [[r.left + r.width / 2, r.top + r.height / 2], [r.left + 2, r.top + 2], [r.right - 2, r.top + 2],
      [r.left + 2, r.bottom - 2], [r.right - 2, r.bottom - 2]];
    const inView = pts.filter(([x, y]) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight);
    const seen = inView.some(([x, y]) => { const t = document.elementFromPoint(x, y); return t && (t === el || el.contains(t)); });
    el.blur();
    return { indicator: indicator, obscured: inView.length ? !seen : null, how: how, changed: changed };
  }

  function snapshot(opts) {
    opts = Object.assign({ focus: true, maxText: 400 }, opts || {});
    const out = {
      tool: 'design-qa/collect_snapshot.js', version: 1, url: location.href, captured_at: new Date().toISOString(),
      viewport: { width: innerWidth, height: innerHeight },
      page: { scrollWidth: document.documentElement.scrollWidth, clientWidth: document.documentElement.clientWidth },
      elements: [],
    };
    const interactive = new Set(document.querySelectorAll(INTERACTIVE));
    const textEls = Array.from(document.body.querySelectorAll('*')).filter(el =>
      Array.from(el.childNodes).some(n => n.nodeType === 3 && n.textContent.trim().length > 0)).slice(0, opts.maxText);
    const all = Array.from(new Set([...interactive, ...textEls]));
    const scrollY = window.scrollY;
    all.forEach(el => {
      const s = getComputedStyle(el); const r = el.getBoundingClientRect();
      if (!visible(el, s, r)) return;
      const bg = compositeAt(el, null); const fg = parseColor(s.color);
      const fgOver = fg && bg.value ? compositeAt(el, fg).value : null;
      const ownText = Array.from(el.childNodes).filter(n => n.nodeType === 3).map(n => n.textContent).join(' ').trim();
      const clipX = el.scrollWidth > el.clientWidth + 1 && /hidden|clip/.test(s.overflowX);
      const clipY = el.scrollHeight > el.clientHeight + 1 && /hidden|clip/.test(s.overflowY);
      const e = {
        id: selectorFor(el), tag: el.tagName.toLowerCase(), role: el.getAttribute('role') || '',
        interactive: interactive.has(el), name: interactive.has(el) ? accessibleName(el) : '',
        text: ownText.slice(0, 80),
        rect: { x: Math.round(r.left), y: Math.round(r.top + scrollY), w: Math.round(r.width * 10) / 10, h: Math.round(r.height * 10) / 10 },
        color: fgOver ? rgb(fgOver) : null, bg: bg.value ? rgb(bg.value) : null, bg_unknown: bg.reason,
        fontSize: parseFloat(s.fontSize), fontWeight: parseInt(s.fontWeight, 10) || 400,
        clipped: (clipX || clipY) && ownText.length > 0, ellipsis: s.textOverflow === 'ellipsis' || parseInt(s.webkitLineClamp, 10) > 0,
        inline: isInline(el), disabled: !!el.disabled || el.getAttribute('aria-disabled') === 'true',
      };
      if (e.interactive) { e.rest = {}; FOCUS_PROPS.forEach(k => { e.rest[k] = s[k]; }); }
      if (e.interactive && opts.focus && !e.disabled) e.focus = focusProbe(el);
      out.elements.push(e);
    });
    window.scrollTo(0, scrollY);
    return out;
  }

  global.designQaSnapshot = snapshot;
  global.designQaFocusProbe = function () {
    const el = document.activeElement;
    if (!el || el === document.body) return null;
    const r = focusProbeActive(el);
    return Object.assign({ id: selectorFor(el) }, r);
  };
  // Probe the element that real keyboard focus is already on (no script focus).
  function focusProbeActive(el) {
    const s1 = getComputedStyle(el);
    const outlineOn = s1.outlineStyle !== 'none' && parseFloat(s1.outlineWidth) > 0;
    const shadowOn = s1.boxShadow && s1.boxShadow !== 'none';
    const after = {}; FOCUS_PROPS.forEach(k => { after[k] = s1[k]; });
    const r = el.getBoundingClientRect();
    const pts = [[r.left + r.width / 2, r.top + r.height / 2], [r.left + 2, r.top + 2], [r.right - 2, r.bottom - 2]];
    const inView = pts.filter(([x, y]) => x >= 0 && y >= 0 && x < innerWidth && y < innerHeight);
    const seen = inView.some(([x, y]) => { const t = document.elementFromPoint(x, y); return t && (t === el || el.contains(t)); });
    return { outlineOn: outlineOn, shadowOn: shadowOn, styles: after, obscured: inView.length ? !seen : null };
  }
})(typeof window !== 'undefined' ? window : this);
