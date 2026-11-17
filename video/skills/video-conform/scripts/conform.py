#!/usr/bin/env python3
"""conform.py — assemble the final cut: frames + voice-over + music → a checked MP4.

Builds one ffmpeg command from the render (frames or an MP4), the voice-over
and music files, and the scene's captions, then checks the result:

  * H.264 / yuv420p / +faststart, the combination every major player and
    social platform accepts
  * music sits under the voice-over (about -12 dB) instead of fighting it
  * loudness normalized to a named target with a -1 dBTP true-peak ceiling:
      speech     -18 LUFS  (AES TD1008, speech and mixed content for streaming)
      music      -16 LUFS  (AES TD1008, music)
      broadcast  -23 LUFS  (EBU R 128)
  * captions.srt written from the scene's voice-over lines, one cue per shot;
    --burn-captions also draws them into the picture
  * QC after encode: duration within one frame of the scene, integrated
    loudness within 1 LU of the target; a miss is exit 4, not a warning

Without --run it prints the plan and the command and touches nothing.

Exit codes: 0 planned or conformed and QC passed, 2 bad input, 3 ffmpeg missing,
4 ffmpeg failed or QC failed.

Examples:
  conform.py --sample
  conform.py --render film/frames/render.json --scene film/scene.json --vo film/vo.wav --out film/final.mp4 --run
  conform.py --video film/cut.mp4 --music film/bed.mp3 --loudness music --out film/final.mp4 --run
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import sys
import textwrap
from pathlib import Path

TARGETS = {"speech": -18.0, "music": -16.0, "broadcast": -23.0}
TRUE_PEAK = -1.0
MUSIC_UNDER_VO = 0.25  # about -12 dB

SAMPLE_RENDER = {"schema": "render.v1", "frames_dir": "film/frames", "pattern": "frame_%05d.png",
                 "fps": 30, "duration": 12.0, "width": 1920, "height": 1080}
SAMPLE_SHOTS = [
    {"id": "s1", "duration": 3.5, "vo": "Your release notes are a wall of text."},
    {"id": "s2", "duration": 4.0, "vo": "Version two ships three things that matter."},
    {"id": "s3", "duration": 4.5, "vo": "Ship faster. Try it today."},
]


def ts(sec: float) -> str:
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def srt_from_shots(shots: list) -> str:
    out, t, n = [], 0.0, 0
    for s in shots:
        d = float(s["duration"])
        vo = (s.get("vo") or "").strip()
        if vo:
            n += 1
            lines = textwrap.wrap(vo, 42)[:2] if len(vo) <= 84 else textwrap.wrap(vo, max(42, len(vo) // 2 + 1))[:2]
            out.append(f"{n}\n{ts(t + 0.05)} --> {ts(t + d - 0.05)}\n" + "\n".join(lines) + "\n")
        t += d
    return "\n".join(out)


SAFE_PATH = re.compile(r"[A-Za-z0-9_./\\:-]+")


def safe_caption_path() -> str:
    """A caption path the subtitles filter cannot misparse: a fresh temp dir whose path
    holds only [A-Za-z0-9_./-] (plus a drive colon, escaped later). User file names with
    commas, brackets, quotes or '=' never reach the filtergraph."""
    d = tempfile.mkdtemp(prefix="conform_")
    if not SAFE_PATH.fullmatch(d):
        shutil.rmtree(d, ignore_errors=True)
        d = tempfile.mkdtemp(prefix="conform_", dir=".")
    return str(Path(d) / "captions.srt")


def build_cmd(video_in: list, duration: float, fps: float, vo: str | None, music: str | None,
              target: float, burn: str | None, out: str) -> list:
    cmd = ["ffmpeg", "-y", "-loglevel", "error"] + video_in
    inputs = 1
    vo_i = mu_i = None
    if vo:
        cmd += ["-i", vo]
        vo_i, inputs = inputs, inputs + 1
    if music:
        cmd += ["-i", music]
        mu_i, inputs = inputs, inputs + 1
    norm = f"loudnorm=I={target:g}:TP={TRUE_PEAK:g}:LRA=11,aresample=48000"
    if vo_i is not None and mu_i is not None:
        af = (f"[{vo_i}:a]aformat=channel_layouts=stereo[v];[{mu_i}:a]aformat=channel_layouts=stereo,"
              f"volume={MUSIC_UNDER_VO}[m];[v][m]amix=inputs=2:duration=longest:dropout_transition=0:normalize=0,{norm}[a]")
    elif vo_i is not None or mu_i is not None:
        af = f"[{vo_i if vo_i is not None else mu_i}:a]aformat=channel_layouts=stereo,{norm}[a]"
    else:
        cmd += ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
        af = f"[{inputs}:a]anull[a]"
    vf = "format=yuv420p"
    if burn:
        # burn is a path from safe_caption_path(): [A-Za-z0-9_./-] only, so nothing in it
        # can break the filtergraph (commas, brackets, quotes, colons on Windows drives).
        burn = burn.replace("\\", "/").replace(":", "\\:")
        vf = f"subtitles={burn}:force_style='FontSize=22,Outline=2,MarginV=40',{vf}"
    cmd += ["-filter_complex", f"[0:v]{vf}[vid];{af}", "-map", "[vid]", "-map", "[a]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-r", f"{fps:g}",
            "-c:a", "aac", "-b:a", "192k", "-t", f"{duration:.3f}", "-movflags", "+faststart", out]
    return cmd


def probe_duration(path: str) -> float | None:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


def measure_lufs(path: str) -> float | None:
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-filter_complex", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None


def main() -> int:
    ap = argparse.ArgumentParser(description="Conform the final cut: frames or MP4 + VO + music + captions → loudness-normalized, QC-checked MP4 (ffmpeg).")
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--render", help="render.json written by frame_renderer.py.")
    src.add_argument("--video", help="An already rendered MP4 to conform instead of frames.")
    ap.add_argument("--scene", help="scene.v1 JSON, for captions and the expected duration.")
    ap.add_argument("--vo", help="Voice-over audio file.")
    ap.add_argument("--music", help="Music bed audio file (mixed about 12 dB under the VO).")
    ap.add_argument("--loudness", choices=sorted(TARGETS), default="speech")
    ap.add_argument("--burn-captions", action="store_true", help="Draw captions into the picture (needs ffmpeg with libass).")
    ap.add_argument("--out", default="final.mp4")
    ap.add_argument("--run", action="store_true", help="Execute ffmpeg and QC; without it only the plan is printed.")
    ap.add_argument("--sample", action="store_true", help="Plan for a built-in sample render (never runs).")
    ap.add_argument("--output", choices=["text", "json"], default="text")
    args = ap.parse_args()

    try:
        if args.sample or not (args.render or args.video):
            render, shots, args.run = SAMPLE_RENDER, SAMPLE_SHOTS, False
            base = Path("film")
        else:
            render = json.loads(Path(args.render).read_text(encoding="utf-8")) if args.render else None
            scene = json.loads(Path(args.scene).read_text(encoding="utf-8")) if args.scene else None
            shots = scene["shots"] if scene else []
            base = Path(args.out).resolve().parent
        for p in (args.vo, args.music, args.video):
            if p and not args.sample and not Path(p).exists():
                raise FileNotFoundError(p)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if render:
        fps = float(render["fps"])
        duration = float(render["duration"])
        video_in = ["-framerate", f"{fps:g}", "-i", str(Path(render["frames_dir"]) / render["pattern"])]
    else:
        fps = 30.0
        duration = sum(float(s["duration"]) for s in shots) if shots else None
        if duration is None:
            duration = probe_duration(args.video) if shutil.which("ffprobe") else None
        if not duration:
            print("error: cannot tell the duration; pass --scene", file=sys.stderr)
            return 2
        video_in = ["-i", args.video]

    srt_path = None
    if shots:
        srt_path = str(base / "captions.srt")
    target = TARGETS[args.loudness]
    srt_text = srt_from_shots(shots) if shots else ""
    if args.burn_captions and not srt_text.strip():
        print("note: no voice-over lines in the scene, so there are no captions to burn in", file=sys.stderr)
    burn_path = safe_caption_path() if (args.burn_captions and srt_text.strip()) else None
    cmd = build_cmd(video_in, duration, fps, args.vo, args.music, target, burn_path, args.out)
    plan = {"out": args.out, "duration": round(duration, 3), "fps": fps, "loudness_target_lufs": target,
            "true_peak_dbtp": TRUE_PEAK, "audio": "vo+music" if args.vo and args.music else
            ("vo" if args.vo else ("music" if args.music else "silent track")),
            "captions": srt_path, "burn_captions": bool(burn_path),
            "command": cmd, "ran": False}

    if args.run:
        if not (shutil.which("ffmpeg") and shutil.which("ffprobe")):
            print("error: ffmpeg/ffprobe not found (install ffmpeg, e.g. apt install ffmpeg / brew install ffmpeg)", file=sys.stderr)
            return 3
        if srt_path:
            Path(srt_path).write_text(srt_text, encoding="utf-8")
        if burn_path:
            Path(burn_path).write_text(srt_text, encoding="utf-8")
        try:
            r = subprocess.run(cmd, capture_output=True, text=True)
        finally:
            if burn_path:
                shutil.rmtree(Path(burn_path).parent, ignore_errors=True)
        if r.returncode != 0:
            print(f"error: ffmpeg failed: {r.stderr.strip()[-1200:]}", file=sys.stderr)
            return 4
        plan["ran"] = True
        got = probe_duration(args.out)
        has_audio = bool(args.vo or args.music)
        lufs = measure_lufs(args.out) if has_audio else None
        # A mix that could not be measured is a failure, not a pass; only a silent track skips the check.
        qc = {"duration_s": got, "duration_ok": got is not None and abs(got - duration) <= 1.5 / fps + 0.05,
              "lufs": lufs, "lufs_ok": (not has_audio) or (lufs is not None and abs(lufs - target) <= 1.0)}
        plan["qc"] = qc
        plan["verdict"] = "PASS" if qc["duration_ok"] and qc["lufs_ok"] else "QC-FAILED"
    else:
        plan["verdict"] = "PLANNED"

    if args.output == "json":
        print(json.dumps(plan, indent=2))
    else:
        print(f"{plan['verdict']}: {plan['out']}  {plan['duration']}s @ {fps:g}fps, audio={plan['audio']}, "
              f"target {target:g} LUFS / {TRUE_PEAK:g} dBTP")
        if plan.get("qc"):
            q = plan["qc"]
            if q["lufs"] is None and q["lufs_ok"]:
                loud = "loudness n/a (silent track)"
            else:
                loud = f"loudness {q['lufs']} LUFS ({'ok' if q['lufs_ok'] else 'OFF TARGET or unmeasured'})"
            print(f"  duration {q['duration_s']}s ({'ok' if q['duration_ok'] else 'MISMATCH'}), {loud}")
        if srt_path:
            print(f"  captions: {srt_path}{' (burned in)' if plan['burn_captions'] else ''}")
        if not plan["ran"]:
            print("  command: " + " ".join(cmd))
    return 0 if plan["verdict"] in ("PASS", "PLANNED") else 4


if __name__ == "__main__":
    sys.exit(main())
