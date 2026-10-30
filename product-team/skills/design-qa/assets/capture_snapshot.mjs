// design-qa: capture a rendered snapshot with a real keyboard focus pass.
//
// Needs Node 18+ and Playwright in the project you run it from
// (npm i -D playwright && npx playwright install chromium). Runs locally against
// the URL you give it; sends nothing anywhere else.
//
//   node capture_snapshot.mjs <url> [--width 1440] [--height 900] [--tabs 200] [--out snapshot.json]
//
// Run it at least twice: once at --width 320 (reflow, WCAG 1.4.10) and once at
// your main desktop width. Then: python scripts/rendered_audit.py --snapshot snapshot.json
import { readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

// Resolve Playwright from the project you run this in (this file usually lives in
// a plugin cache with no node_modules of its own).
const req = createRequire(join(process.cwd(), 'noop.js'));
let chromium;
for (const mod of ['playwright', '@playwright/test', 'playwright-core']) {
  try { ({ chromium } = req(mod)); break; } catch { /* try the next one */ }
}
if (!chromium) {
  console.error('Playwright not found from ' + process.cwd() + '. Run: npm i -D playwright && npx playwright install chromium');
  process.exit(3);
}

const args = process.argv.slice(2);
const url = args.find(a => !a.startsWith('--'));
const opt = (name, dflt) => { const i = args.indexOf('--' + name); return i >= 0 ? args[i + 1] : dflt; };
if (!url) { console.error('usage: node capture_snapshot.mjs <url> [--width N] [--height N] [--tabs N] [--out FILE]'); process.exit(3); }
const width = Number(opt('width', 1440)); const height = Number(opt('height', 900));
const tabs = Number(opt('tabs', 200)); const outFile = opt('out', `snapshot-${width}.json`);
const collector = readFileSync(join(dirname(fileURLToPath(import.meta.url)), 'collect_snapshot.js'), 'utf8');

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width, height } });
  await page.goto(url, { waitUntil: 'networkidle' });
  await page.addScriptTag({ content: collector });
  const snap = await page.evaluate(() => window.designQaSnapshot({ focus: false }));
  const byId = new Map(snap.elements.map(e => [e.id, e]));
  const PROPS = ['outlineStyle', 'outlineWidth', 'outlineColor', 'boxShadow', 'borderColor', 'backgroundColor', 'textDecorationLine', 'color'];
  const seen = new Set(); let wrapped = false;
  await page.mouse.move(0, 0);
  for (let i = 0; i < tabs; i++) {
    await page.keyboard.press('Tab');
    const probe = await page.evaluate(() => window.designQaFocusProbe());
    if (!probe) continue;
    if (seen.has(probe.id)) { wrapped = true; break; } // wrapped around
    seen.add(probe.id);
    const el = byId.get(probe.id);
    if (!el) continue;
    const changed = el.rest ? PROPS.filter(k => el.rest[k] !== probe.styles[k]) : [];
    el.focus = { indicator: probe.outlineOn || probe.shadowOn || changed.length > 0, obscured: probe.obscured, how: 'keyboard', changed };
  }
  for (const e of snap.elements) if (e.interactive && !e.disabled && !e.focus) e.focus = { indicator: null, obscured: null, how: 'not reached by Tab' };
  snap.keyboard_pass = { reached: seen.size, wrapped };
  writeFileSync(outFile, JSON.stringify(snap, null, 1));
  console.log(`wrote ${outFile}: ${snap.elements.length} elements, ${seen.size} reached by Tab`);
} finally {
  await browser.close();
}
