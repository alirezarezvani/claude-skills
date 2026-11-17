#!/usr/bin/env python3
"""frame_renderer.py — render a compiled animatic page to numbered PNG frames.

Frame N is captured at t = N / fps by calling the page's window.__seek(t), so
renders are deterministic: the same scene gives the same frames every run, and
you can re-render only the shots you changed (--shots s2,s4) without touching
the rest. Writes render.json (canvas, fps, frame count, each shot's first and
last frame) next to the frames; video-conform and shot_manifest read it.

Backends (--backend auto tries them in this order):
  python   Playwright for Python
  node     Playwright for Node (node must be on PATH)
No backend found → exit 3, pointing at the install steps in the skill's SKILL.md. Nothing here calls a paid
service; Google Fonts is the only network fetch, and only if the scene asks
for a Google font (compile with --offline to skip it).

Exit codes: 0 rendered (or planned with --dry-run), 2 bad input, 3 no backend,
4 render failed.

Examples:
  frame_renderer.py --sample                      # dry-run plan for the sample, no browser
  frame_renderer.py --html film/animatic.html --out film/frames
  frame_renderer.py --html film/animatic.html --out film/frames --fps 12   # quick animatic
  frame_renderer.py --html film/animatic.html --out film/frames --shots s2 --mp4 film/cut.mp4
  frame_renderer.py --html film/animatic.html --out film/keyframes --keyframes   # plate-only first/last frame of upgrade shots
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from scene_model import SAMPLE_SCENE, normalize, timeline, total_duration  # noqa: E402

STEP_TIMEOUT = 3600  # seconds; a stuck browser or encode fails with exit 4 instead of hanging
SCENE_RE = re.compile(r"const SCENE = (\{.*?\});\n", re.S)

# Network policy for the render browser: local files, inline data and the Google Fonts the
# compiler links are allowed; any other http(s) request is blocked unless --allow-remote,
# so a shared scene.json cannot make the renderer fetch arbitrary hosts.
FONT_HOSTS = ("fonts.googleapis.com", "fonts.gstatic.com")


def request_allowed(url: str, allow_remote: bool) -> bool:
    from urllib.parse import urlsplit
    parts = urlsplit(url)
    if parts.scheme in ("file", "data", "blob", "about"):
        return True
    if parts.scheme in ("http", "https"):
        return allow_remote or parts.hostname in FONT_HOSTS
    return False


NODE_RUNNER = r"""
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const job = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: job.width, height: job.height }, deviceScaleFactor: 1 });
  await page.route('**/*', route => {
    const u = new URL(route.request().url());
    const ok = ['file:', 'data:', 'blob:', 'about:'].includes(u.protocol) ||
      (['http:', 'https:'].includes(u.protocol) && (job.allowRemote || job.fontHosts.includes(u.hostname)));
    if (ok) return route.continue();
    console.log('BLOCKED ' + u.href);
    return route.abort();
  });
  await page.goto(job.url, { waitUntil: 'load' });
  await page.evaluate(() => window.__ready);
  for (const f of job.frames) {
    await page.evaluate(t => window.__seek(t), f.t);
    await page.screenshot({ path: f.path, clip: { x: 0, y: 0, width: job.width, height: job.height } });
  }
  await browser.close();
})().catch(e => { console.error(e && e.stack || e); process.exit(4); });
"""


def scene_from_html(html_path: Path) -> dict:
    text = html_path.read_text(encoding="utf-8")
    m = SCENE_RE.search(text)
    if not m:
        raise ValueError(f"{html_path} is not a timeline_compiler.py page (no SCENE block)")
    return json.loads(m.group(1).replace("<\\/", "</"))


def plan_frames(scene: dict, fps: float, out_dir: Path, only: set[str] | None) -> tuple[list, list]:
    total = total_duration(scene)
    n = max(1, int(math.floor(total * fps + 1e-6)))
    shots = []
    for row in timeline(scene):
        first = int(math.ceil(row["start"] * fps - 1e-6))
        last = min(n - 1, int(math.ceil(row["end"] * fps - 1e-6)) - 1)
        shots.append({**row, "first_frame": first, "last_frame": max(first, last)})
    frames = []
    for i in range(n):
        if only:
            owner = next((s for s in shots if s["first_frame"] <= i <= s["last_frame"]), None)
            # a fade into the next shot changes this shot's tail too, so render both
            if owner is None or owner["id"] not in only:
                continue
        frames.append({"i": i, "t": round(i / fps, 6), "path": str(out_dir / f"frame_{i:05d}.png")})
    return frames, shots


def pick_backend(choice: str) -> str | None:
    def has_python() -> bool:
        try:
            import playwright.sync_api  # noqa: F401
            return True
        except ImportError:
            return False

    def has_node() -> bool:
        if not shutil.which("node"):
            return False
        # probe from a clean dir: the runner lives in a temp dir, so resolve the same way and
        # never load a node_modules planted in the user's working directory
        with tempfile.TemporaryDirectory() as tmp:
            r = subprocess.run(["node", "-e", "require('playwright')"], capture_output=True, cwd=tmp)
        return r.returncode == 0

    if choice == "python":
        return "python" if has_python() else None
    if choice == "node":
        return "node" if has_node() else None
    if has_python():
        return "python"
    if has_node():
        return "node"
    return None


def render_python(url: str, width: int, height: int, frames: list, allow_remote: bool) -> list:
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
        blocked: list = []

        def gate(route):
            if request_allowed(route.request.url, allow_remote):
                route.continue_()
            else:
                blocked.append(route.request.url)
                route.abort()

        page.route("**/*", gate)
        page.goto(url, wait_until="load")
        page.evaluate("() => window.__ready")
        for f in frames:
            page.evaluate("t => window.__seek(t)", f["t"])
            page.screenshot(path=f["path"], clip={"x": 0, "y": 0, "width": width, "height": height})
        browser.close()
    return blocked


def render_node(url: str, width: int, height: int, frames: list, allow_remote: bool) -> list:
    with tempfile.TemporaryDirectory() as tmp:
        runner = Path(tmp) / "runner.cjs"
        job = Path(tmp) / "job.json"
        runner.write_text(NODE_RUNNER, encoding="utf-8")
        job.write_text(json.dumps({"url": url, "width": width, "height": height, "frames": frames,
                                    "allowRemote": allow_remote, "fontHosts": list(FONT_HOSTS)}), encoding="utf-8")
        r = subprocess.run(["node", str(runner), str(job)], capture_output=True, text=True, cwd=tmp,
                           timeout=STEP_TIMEOUT)
        if r.returncode != 0:
            raise RuntimeError(r.stderr.strip()[-2000:] or "node renderer failed")
        return [ln[8:] for ln in r.stdout.splitlines() if ln.startswith("BLOCKED ")]


def encode_mp4(frames_dir: Path, fps: float, mp4: Path) -> list:
    return ["ffmpeg", "-y", "-loglevel", "error", "-framerate", f"{fps:g}",
            "-i", str(frames_dir / "frame_%05d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
            "-crf", "18", "-movflags", "+faststart", str(mp4)]


def main() -> int:
    ap = argparse.ArgumentParser(description="Render a compiled animatic HTML page to deterministic PNG frames (Playwright).")
    ap.add_argument("--html", help="Page written by timeline_compiler.py.")
    ap.add_argument("--out", help="Frames directory (default: frames/ next to the page).")
    ap.add_argument("--fps", type=float, help="Override the scene fps (12 is plenty for a review animatic).")
    ap.add_argument("--shots", help="Comma-separated shot ids to re-render; other frames are left as they are.")
    ap.add_argument("--backend", choices=["auto", "python", "node"], default="auto")
    ap.add_argument("--keyframes", action="store_true",
                    help="Render only the first and last frame of each upgrade shot, plates and images only, as <shot>_first.png / <shot>_last.png.")
    ap.add_argument("--mp4", help="Also encode the frames to this MP4 (H.264, no audio; use video-conform for the real cut).")
    ap.add_argument("--allow-remote", action="store_true",
                    help="Let the page fetch remote http(s) media; by default only local files and Google Fonts load.")
    ap.add_argument("--dry-run", action="store_true", help="Print the frame plan without launching a browser.")
    ap.add_argument("--sample", action="store_true", help="Dry-run plan for the built-in sample scene.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()

    try:
        if args.sample or not args.html:
            scene = normalize(SAMPLE_SCENE)
            html_path = Path("animatic.html")
            args.dry_run = True
        else:
            html_path = Path(args.html).resolve()
            scene = normalize(scene_from_html(html_path))
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    fps = args.fps or float(scene["meta"]["fps"])
    if fps <= 0 or fps > 120:
        print("error: --fps must be between 0 and 120", file=sys.stderr)
        return 2
    out_dir = Path(args.out).resolve() if args.out else html_path.parent / "frames"
    only = {s.strip() for s in args.shots.split(",")} if args.shots else None
    if only:
        unknown = only - {s["id"] for s in scene["shots"]}
        if unknown:
            print(f"error: unknown shot ids: {sorted(unknown)}", file=sys.stderr)
            return 2
    frames, shots = plan_frames(scene, fps, out_dir, only)
    query = "?render=1"
    if args.keyframes:
        query += "&plateonly=1"
        frames = []
        for sh in shots:
            if sh["upgrade"] and (not only or sh["id"] in only):
                frames.append({"i": sh["first_frame"], "t": round(sh["start"] + 1e-3, 6),
                               "path": str(out_dir / f"{sh['id']}_first.png")})
                frames.append({"i": sh["last_frame"], "t": round(sh["end"] - 1e-3, 6),
                               "path": str(out_dir / f"{sh['id']}_last.png")})
        if not frames:
            print("error: --keyframes found no shots with upgrade:true", file=sys.stderr)
            return 2
    w, h = scene["meta"]["width"], scene["meta"]["height"]
    report = {
        "schema": "render.v1",
        "html": str(html_path),
        "frames_dir": str(out_dir),
        "pattern": "frame_%05d.png",
        "width": w, "height": h, "fps": fps,
        "duration": total_duration(scene),
        "frame_count": max(1, int(math.floor(total_duration(scene) * fps + 1e-6))),
        "rendered": len(frames),
        "shots": shots,
        "mode": scene["meta"]["mode"],
    }

    if args.dry_run:
        report["backend"] = None
        report["dry_run"] = True
    else:
        backend = pick_backend(args.backend)
        if backend is None:
            print("error: no renderer found. Install Playwright for Python or Node with its Chromium build;\n"
                  "  the video-animatic SKILL.md 'Portability' line has the exact steps.", file=sys.stderr)
            return 3
        out_dir.mkdir(parents=True, exist_ok=True)
        url = html_path.as_uri() + query
        try:
            if backend == "python":
                blocked = render_python(url, w, h, frames, args.allow_remote)
            else:
                blocked = render_node(url, w, h, frames, args.allow_remote)
        except Exception as exc:  # renderer errors come from the browser, keep the message
            print(f"error: render failed ({backend}): {exc}", file=sys.stderr)
            return 4
        report["backend"] = backend
        if blocked:
            report["blocked_requests"] = sorted(set(blocked))
            print(f"warning: blocked {len(report['blocked_requests'])} remote request(s), e.g. "
                  f"{report['blocked_requests'][0]}; use local files or pass --allow-remote", file=sys.stderr)
        report["keyframes"] = bool(args.keyframes)
        (out_dir / ("keyframes.json" if args.keyframes else "render.json")).write_text(json.dumps(report, indent=2), encoding="utf-8")
        if args.mp4:
            if not shutil.which("ffmpeg"):
                print("error: ffmpeg not found for --mp4", file=sys.stderr)
                return 3
            try:
                r = subprocess.run(encode_mp4(out_dir, fps, Path(args.mp4)), capture_output=True, text=True,
                                   timeout=STEP_TIMEOUT)
            except subprocess.TimeoutExpired:
                print(f"error: ffmpeg did not finish within {STEP_TIMEOUT}s", file=sys.stderr)
                return 4
            if r.returncode != 0:
                print(f"error: ffmpeg failed: {r.stderr.strip()[-800:]}", file=sys.stderr)
                return 4
            report["mp4"] = str(Path(args.mp4).resolve())

    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        verb = "planned" if report.get("dry_run") else f"rendered with {report['backend']}"
        print(f"{verb}: {report['rendered']}/{report['frame_count']} frames, {w}x{h} @ {fps:g}fps → {out_dir}")
        for s in shots:
            print(f"  {s['id']:>6}  frames {s['first_frame']:>5}–{s['last_frame']:<5} {s['start']:.2f}–{s['end']:.2f}s"
                  f"{'  [upgrade]' if s['upgrade'] else ''}")
        if report.get("mp4"):
            print(f"mp4: {report['mp4']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
