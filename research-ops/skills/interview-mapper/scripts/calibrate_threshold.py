#!/usr/bin/env python3
"""
calibrate_threshold.py — calibrate the verbatim threshold against a gold-set.

Problem: the fuzzy threshold (88) and coverage (0.6) in verify_quotes.py are calibrated on synthetic data only. They need to be
calibrated on LABELED data, not taken from tutorials (the only documented threshold is difflib 0.6).

Input gold.json — a list of manually labeled examples:
  [{"quote":"...", "is_verbatim": true},   # the quote really exists in the source (even with ASR noise)
   {"quote":"...", "is_verbatim": false}]  # fabrication/heavy paraphrase not present in the source
Plus a transcript. The script runs verify_quotes at different thresholds and computes precision/recall/F1,
proposing the threshold that maximizes F1 (or precision with --prefer-precision).

CLI:
  python calibrate_threshold.py --transcript T.txt --gold gold.json
        [--min 70 --max 98 --step 2] [--min-coverage 0.6] [--prefer-precision] [--output {human,json}]
  python calibrate_threshold.py --sample
"""

import argparse
import json
import subprocess
import sys
import os
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
VERIFY = os.path.join(HERE, "verify_quotes.py")

SAMPLE_TRANSCRIPT = (
    "L1: Interviewer: Tell me about the last time you tried to reconcile the budget.\n"
    "L2: Respondent: Honestly, I opened three tabs and gave up after twenty minutes.\n"
    "L3: Interviewer: What made you give up?\n"
    "L4: Respondent: The export didn't match what I saw on screen, so I stopped trusting it.\n"
)
SAMPLE_GOLD = [
    {
        "quote": "I opened three tabs and gave up after twenty minutes",
        "is_verbatim": True,
    },
    {"quote": "The export didn't match what I saw on screen", "is_verbatim": True},
    {
        "quote": "I have never once opened a spreadsheet in my life",
        "is_verbatim": False,
    },
]


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


def run_verify(transcript, claims, threshold, min_cov):
    """Runs verify_quotes.py as a subprocess at the given threshold and returns results.

    The claims file lives in a throwaway TemporaryDirectory so cleanup is automatic on
    context exit — no explicit delete call on a path we'd otherwise have to re-validate.
    """
    with tempfile.TemporaryDirectory(prefix="interview-mapper-calibrate-") as td:
        cpath = os.path.join(td, "claims.json")
        with open(cpath, "w", encoding="utf-8") as f:
            json.dump(claims, f, ensure_ascii=False)
        try:
            out = subprocess.run(
                [
                    sys.executable,
                    VERIFY,
                    "--transcript",
                    transcript,
                    "--claims",
                    cpath,
                    "--threshold",
                    str(threshold),
                    "--min-coverage",
                    str(min_cov),
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout
        except subprocess.CalledProcessError as e:
            sys.exit(f"error: verify_quotes.py failed: {e.stderr or e}")
    return json.loads(out)["results"]


def prf(gold, results):
    """Computes precision/recall/F1 for a pair (gold labels, verify_quotes results)."""
    tp = fp = tn = fn = 0
    for g, r in zip(gold, results):
        pred = r["status"].startswith("verified")
        truth = bool(g["is_verbatim"])
        if pred and truth:
            tp += 1
        elif pred and not truth:
            fp += 1
        elif not pred and not truth:
            tn += 1
        else:
            fn += 1
    prec = tp / (tp + fp) if (tp + fp) else 0.0
    rec = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0
    return dict(
        tp=tp,
        fp=fp,
        tn=tn,
        fn=fn,
        precision=round(prec, 3),
        recall=round(rec, 3),
        f1=round(f1, 3),
    )


def main():
    """CLI: sweeps thresholds, computes P/R/F1 against the gold-set, and recommends the best one."""
    ap = argparse.ArgumentParser(
        description="Calibrate the verify_quotes.py fuzzy threshold against a gold-set."
    )
    ap.add_argument(
        "--transcript", default=None, help="Required unless --sample is given"
    )
    ap.add_argument("--gold", default=None, help="Required unless --sample is given")
    ap.add_argument("--min", type=float, default=70)
    ap.add_argument("--max", type=float, default=98)
    ap.add_argument("--step", type=float, default=2)
    ap.add_argument("--min-coverage", type=float, default=0.6)
    ap.add_argument(
        "--prefer-precision",
        action="store_true",
        help="Choose the threshold by precision (fewer false quotes), not by F1",
    )
    ap.add_argument(
        "--sample",
        action="store_true",
        help="Run on a built-in sample transcript + gold-set",
    )
    ap.add_argument(
        "--output", choices=["human", "json"], default="human", help="Output format"
    )
    a = ap.parse_args()

    sample_dir = None
    if a.sample:
        gold = SAMPLE_GOLD
        sample_dir = tempfile.TemporaryDirectory(
            prefix="interview-mapper-calibrate-sample-"
        )
        transcript_path = os.path.join(sample_dir.name, "transcript.txt")
        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(SAMPLE_TRANSCRIPT)
    else:
        if not a.transcript or not a.gold:
            sys.exit(
                "error: --transcript and --gold are required unless --sample is given"
            )
        gold = _read_json(a.gold)
        transcript_path = a.transcript
    claims = [{"cell": "gold", "claim": "", "quote": g["quote"]} for g in gold]

    rows, best = [], None
    t = a.min
    try:
        while t <= a.max + 1e-9:
            res = run_verify(transcript_path, claims, t, a.min_coverage)
            m = prf(gold, res)
            m["threshold"] = t
            rows.append(m)
            key = (
                (m["precision"], m["f1"])
                if a.prefer_precision
                else (m["f1"], m["precision"])
            )
            if best is None or key > best[0]:
                best = (key, m)
            t += a.step
    finally:
        if sample_dir:
            sample_dir.cleanup()

    b = best[1]
    if a.output == "json":
        print(
            json.dumps(
                {
                    "sweep": rows,
                    "recommended": b,
                    "criterion": "precision" if a.prefer_precision else "F1",
                    "n_gold": len(gold),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print("thresh  P     R     F1    (tp/fp/fn)")
        for m in rows:
            print(
                f"{m['threshold']:5.0f}  {m['precision']:.2f}  {m['recall']:.2f}  {m['f1']:.2f}"
                f"   ({m['tp']}/{m['fp']}/{m['fn']})"
            )
        print(
            f"\nRECOMMENDED threshold: {b['threshold']:.0f}  "
            f"(P={b['precision']} R={b['recall']} F1={b['f1']}; "
            f"criterion: {'precision' if a.prefer_precision else 'F1'})"
        )
        print(
            "N gold:",
            len(gold),
            "| few examples → threshold is approximate, expand the gold-set.",
        )


if __name__ == "__main__":
    main()
