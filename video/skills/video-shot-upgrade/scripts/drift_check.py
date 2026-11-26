#!/usr/bin/env python3
"""drift_check.py — does a generated plate keep the animatic's framing?

For each upgraded shot it compares the plate (an MP4 from the provider) with
the shot's clean animatic keyframes (frame_renderer.py --keyframes):

  duration   the plate must be at least as long as the shot it fills
  aspect     width/height within 2% of the scene aspect
  framing    luma and edge layout of the plate's first and last frames
             against the keyframes, downscaled to 32x32 (Pearson r)
  palette    mean colour of a 4x4 grid against the keyframe (0 = identical)

Verdicts: HOLDS (use it), REVIEW (a human looks: text-only shots have no
keyframe to compare, or framing is borderline), DRIFTED (do not cut it in;
re-prompt or keep the shot as motion graphics). The thresholds are starting
points, not ground truth; they are printed with every result so a reviewer can
see why.

With --scene and --scene-out it writes a copy of the scene where every HOLDS
plate (and REVIEW plates with --accept-review) becomes the shot's plate src,
ready for timeline_compiler.py --mode final.

Needs ffmpeg and ffprobe on PATH. Stdlib only otherwise.

Exit codes: 0 all hold, 2 bad input, 3 needs review or ffmpeg missing,
4 at least one plate drifted.

Examples:
  drift_check.py --sample
  drift_check.py --requests film/requests.json --shots film/shots.json --plates film/plates
  drift_check.py --requests film/requests.json --shots film/shots.json --plates film/plates \\
      --scene film/scene.json --scene-out film/scene.final.json
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GRID = 32
COLOR_GRID = 4
FRAMING_HOLDS = 0.55
FRAMING_DRIFT = 0.30
PALETTE_DRIFT = 0.25
ASPECT_TOL = 0.02


def need_ffmpeg() -> None:
    for tool in ("ffmpeg", "ffprobe"):
        if not shutil.which(tool):
            raise RuntimeError(f"{tool} not found on PATH; install ffmpeg")


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    data = json.loads(out)
    st = data["streams"][0]
    return {"width": int(st["width"]), "height": int(st["height"]),
            "duration": float(data.get("format", {}).get("duration") or 0)}


def grab(path: Path, size: int, pix: str, at_end: bool = False) -> bytes:
    cmd = ["ffmpeg", "-v", "error"]
    if at_end:
        cmd += ["-sseof", "-0.25"]
    cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"format={pix},scale={size}:{size}:flags=area",
            "-f", "rawvideo", "-pix_fmt", pix, "-"]
    data = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = size * size * (3 if pix == "rgb24" else 1)
    if len(data) < n:
        raise RuntimeError(f"could not read a frame from {path}")
    return data[-n:] if at_end else data[:n]


def pearson(a: list[float], b: list[float]) -> float:
    ma, mb = sum(a) / len(a), sum(b) / len(b)
    da, db = [x - ma for x in a], [y - mb for y in b]
    den = math.sqrt(sum(x * x for x in da) * sum(y * y for y in db))
    return 1.0 if den == 0 and da == db else (sum(x * y for x, y in zip(da, db)) / den if den else 0.0)


def edges(luma: list[float]) -> list[float]:
    g = []
    for y in range(GRID):
        for x in range(GRID):
            c = luma[y * GRID + x]
            r = luma[y * GRID + min(x + 1, GRID - 1)]
            d = luma[min(y + 1, GRID - 1) * GRID + x]
            g.append(abs(r - c) + abs(d - c))
    return g


def compare(plate: Path, still: Path, at_end: bool) -> dict:
    pl = list(grab(plate, GRID, "gray", at_end))
    kf = list(grab(still, GRID, "gray"))
    framing = round(0.5 * pearson(pl, kf) + 0.5 * pearson(edges(pl), edges(kf)), 3)
    pc, kc = grab(plate, COLOR_GRID, "rgb24", at_end), grab(still, COLOR_GRID, "rgb24")
    dist = sum(math.sqrt(sum((pc[i + k] - kc[i + k]) ** 2 for k in range(3)))
               for i in range(0, len(pc), 3)) / (COLOR_GRID * COLOR_GRID)
    return {"framing_r": framing, "palette_distance": round(dist / 441.673, 3)}


def check(shot_id: str, plate: Path, req: dict, man: dict, canvas: tuple[int, int]) -> dict:
    res = {"id": shot_id, "plate": str(plate), "findings": [], "metrics": {}}
    if not plate.exists():
        res.update(verdict="DRIFTED", findings=["no plate file"])
        return res
    info = probe(plate)
    res["metrics"].update(info)
    verdict = "HOLDS"
    need = float(req.get("trim_to") or man.get("duration") or 0)
    if info["duration"] + 0.05 < need:
        verdict = "DRIFTED"
        res["findings"].append(f"plate is {info['duration']:.2f}s, the shot needs {need:g}s")
    if info["width"] <= 0 or info["height"] <= 0:
        raise RuntimeError(f"{plate}: ffprobe reports no picture size; re-download the plate")
    want, got = canvas[0] / canvas[1], info["width"] / info["height"]
    if abs(got - want) / want > ASPECT_TOL:
        verdict = "DRIFTED"
        res["findings"].append(f"aspect {info['width']}x{info['height']} does not match the scene's {canvas[0]}x{canvas[1]}")
    stills = [(e, man.get(k)) for e, k in (("first", "start_image"), ("last", "end_image")) if man.get(k)]
    if not stills:
        if verdict == "HOLDS":
            verdict = "REVIEW"
        res["findings"].append("no keyframe to compare (text-only shot): a human checks the framing")
    for edge, still in stills:
        if not Path(still).exists():
            res["findings"].append(f"{edge} keyframe {still} is missing; framing not measured")
            verdict = "REVIEW" if verdict == "HOLDS" else verdict
            continue
        m = compare(plate, Path(still), at_end=(edge == "last"))
        res["metrics"][edge] = m
        if m["framing_r"] < FRAMING_DRIFT:
            verdict = "DRIFTED"
            res["findings"].append(f"{edge} frame framing r={m['framing_r']} (below {FRAMING_DRIFT}): composition left the animatic")
        elif m["framing_r"] < FRAMING_HOLDS and verdict == "HOLDS":
            verdict = "REVIEW"
            res["findings"].append(f"{edge} frame framing r={m['framing_r']} (between {FRAMING_DRIFT} and {FRAMING_HOLDS})")
        if m["palette_distance"] > PALETTE_DRIFT:
            if m["framing_r"] < FRAMING_HOLDS:
                verdict = "DRIFTED"
            elif verdict == "HOLDS":
                verdict = "REVIEW"
            res["findings"].append(f"{edge} frame palette distance {m['palette_distance']} (above {PALETTE_DRIFT})")
    res["verdict"] = verdict
    return res


def apply_to_scene(scene: dict, results: list[dict], accept_review: bool) -> list[str]:
    ok = {r["id"]: r["plate"] for r in results
          if r["verdict"] == "HOLDS" or (accept_review and r["verdict"] == "REVIEW")}
    applied = []
    for shot in scene.get("shots", []):
        if shot.get("id") in ok:
            for layer in shot.get("layers", []):
                if layer.get("type") == "plate":
                    layer["src"] = ok[shot["id"]]
                    applied.append(shot["id"])
                    break
    return applied


def run(args) -> tuple[list[dict], dict]:
    req = json.loads(Path(args.requests).read_text(encoding="utf-8"))
    man = json.loads(Path(args.shots).read_text(encoding="utf-8"))
    if req.get("schema") != "requests.v1" or man.get("schema") != "shots.v1":
        raise ValueError("--requests must be requests.v1 and --shots shots.v1")
    by_id = {s["id"]: s for s in man["shots"]}
    canvas = tuple(man["canvas"])
    only = {s.strip() for s in args.only.split(",")} if args.only else None
    results = []
    for r in req["requests"]:
        if only and r["id"] not in only:
            continue
        results.append(check(r["id"], Path(args.plates) / f"{r['id']}.mp4", r, by_id.get(r["id"], {}), canvas))
    return results, req


def sample() -> int:
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        (d / "plates").mkdir()
        ff = ["ffmpeg", "-v", "error", "-y"]
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc2=size=540x540:rate=24:duration=4", "-pix_fmt", "yuv420p",
                             str(d / "plates" / "s2.mp4")], check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "testsrc2=size=540x540:rate=24:duration=4", "-frames:v", "1",
                             str(d / "s2_first.png")], check=True)
        subprocess.run(ff + ["-sseof", "-0.25", "-i", str(d / "plates" / "s2.mp4"), "-frames:v", "1", str(d / "s2_last.png")],
                       check=True)
        subprocess.run(ff + ["-f", "lavfi", "-i", "mandelbrot=size=960x540:rate=24", "-t", "2", "-pix_fmt", "yuv420p",
                             str(d / "plates" / "s3.mp4")], check=True)
        man = {"schema": "shots.v1", "canvas": [1080, 1080], "shots": [
            {"id": "s2", "duration": 4, "start_image": str(d / "s2_first.png"), "end_image": str(d / "s2_last.png")},
            {"id": "s3", "duration": 3, "start_image": str(d / "s2_first.png"), "end_image": None},
            {"id": "s4", "duration": 2, "start_image": None, "end_image": None}]}
        req = {"schema": "requests.v1", "requests": [{"id": "s2", "trim_to": 4}, {"id": "s3", "trim_to": 3},
                                                     {"id": "s4", "trim_to": 2}]}
        subprocess.run(ff + ["-f", "lavfi", "-i", "color=c=gray:size=1080x1080:rate=24:duration=2.5", "-pix_fmt", "yuv420p",
                             str(d / "plates" / "s4.mp4")], check=True)
        (d / "shots.json").write_text(json.dumps(man))
        (d / "req.json").write_text(json.dumps(req))
        ns = argparse.Namespace(requests=str(d / "req.json"), shots=str(d / "shots.json"), plates=str(d / "plates"), only=None)
        results, _ = run(ns)
        report(results)
    print("expected: s2 HOLDS (same framing), s3 DRIFTED (wrong aspect, too short, different picture), s4 REVIEW (no keyframe)")
    return 0


def report(results: list[dict]) -> None:
    for r in results:
        m = r["metrics"]
        fr = " ".join(f"{e}: r={m[e]['framing_r']} pal={m[e]['palette_distance']}" for e in ("first", "last") if e in m)
        print(f"  {r['id']:>6}  {r['verdict']:<8} {fr}")
        for f in r["findings"]:
            print(f"{'':10}- {f}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Compare generated plates with the animatic keyframes: duration, aspect, framing, palette.")
    ap.add_argument("--requests", help="requests.v1 from provider_adapter.py (trim lengths).")
    ap.add_argument("--shots", help="shots.v1 from shot_manifest.py (keyframe paths, canvas).")
    ap.add_argument("--plates", help="Directory holding <shot id>.mp4 plates.")
    ap.add_argument("--only", help="Comma-separated shot ids.")
    ap.add_argument("--scene", help="scene.v1 to copy with plate src set for plates that hold.")
    ap.add_argument("--scene-out", help="Where to write that copy (never overwrites --scene).")
    ap.add_argument("--accept-review", action="store_true", help="Also use REVIEW plates the user looked at and accepted.")
    ap.add_argument("--sample", action="store_true", help="Build three synthetic plates with ffmpeg and check them.")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()
    if not args.sample and not (args.requests and args.shots and args.plates):
        print("error: --requests, --shots and --plates are required (or --sample)", file=sys.stderr)
        return 2
    try:
        need_ffmpeg()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 3
    if args.sample:
        return sample()
    try:
        results, _ = run(args)
        applied = None
        if args.scene:
            if not args.scene_out or Path(args.scene_out).resolve() == Path(args.scene).resolve():
                raise ValueError("--scene needs a different --scene-out; the approved scene is never overwritten")
            scene = json.loads(Path(args.scene).read_text(encoding="utf-8"))
            applied = apply_to_scene(scene, results, args.accept_review)
            if applied:
                scene.setdefault("meta", {})["mode"] = "final"
            Path(args.scene_out).write_text(json.dumps(scene, indent=2), encoding="utf-8")
    except (OSError, ValueError, KeyError, json.JSONDecodeError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.output == "json":
        print(json.dumps({"schema": "drift.v1", "thresholds": {"framing_holds": FRAMING_HOLDS, "framing_drift": FRAMING_DRIFT,
                                                                "palette_drift": PALETTE_DRIFT, "aspect_tol": ASPECT_TOL},
                          "results": results, "applied": applied}, indent=2))
    else:
        report(results)
        if applied is not None:
            print(f"plates set in {args.scene_out}: {', '.join(applied) or 'none'}")
    verdicts = {r["verdict"] for r in results}
    return 4 if "DRIFTED" in verdicts else (3 if "REVIEW" in verdicts else 0)


if __name__ == "__main__":
    sys.exit(main())
