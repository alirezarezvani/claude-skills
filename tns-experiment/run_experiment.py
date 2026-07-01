"""
P1 TNS Experiment Runner — 4-condition cross-modal causal discovery.

Conditions:
  C1: text-only       → DeepSeek V3.2 reads bug report body
  C2: image-only      → Qwen VLM reads ALL screenshots (no body text)
  C3: Vanilla MM      → Qwen VLM reads ALL screenshots + full body text
  C4: TNS             → autobiographer synthesizes C1 + C2 fragments

Output: results/{run_id}/ with per-issue JSON + summary CSV

Usage:
    python run_experiment.py                          # full run on cached issues
    python run_experiment.py --dry-run                # 1 issue, no API calls
    python run_experiment.py --count 5                # 5 issues only
"""
import argparse
import json
import sys
import time
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import requests as req

sys.path.insert(0, str(Path(__file__).parent))

from config import DATA_DIR, RESULTS_DIR, N_ISSUES, ISSUE_DELAY
from text_client import TextClient
from vlm_client import VLMClient
from orchestrator import Orchestrator


# ------------------------------------------------------------------
# Image download helpers (dedup'd, one download → C2 + C3 share)
# ------------------------------------------------------------------

def _download_images(image_urls: list[str]) -> list[str]:
    """Download all unique image URLs → list of temp file paths.

    Deduplicates URLs first. Retries each URL up to 3 times with
    backoff. Returns list of paths on success; raises on any failure.
    """
    unique = list(dict.fromkeys(image_urls))  # preserve order, dedup
    paths = []
    for url in unique:
        last_err = None
        for attempt in range(3):
            try:
                resp = req.get(url, timeout=30, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://github.com/",
                    "Accept": "image/avif,image/webp,image/png,image/*;q=0.8",
                })
                if resp.ok and len(resp.content) > 1000:
                    break
                if resp.ok:
                    last_err = f"response too small ({len(resp.content)} bytes)"
                else:
                    last_err = f"HTTP {resp.status_code}"
            except Exception as e:
                last_err = str(e)
            time.sleep(2 ** attempt)

        if resp is None or not resp.ok or len(resp.content) <= 1000:
            raise RuntimeError(
                f"Failed to download {url[:80]}... after 3 attempts ({last_err})"
            )

        suffix = ".png"
        ct = resp.headers.get("content-type", "")
        if "jpeg" in ct or "jpg" in ct:
            suffix = ".jpg"
        elif "gif" in ct:
            suffix = ".gif"
        elif "webp" in ct:
            suffix = ".webp"

        tmp = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
        tmp.write(resp.content)
        tmp.close()
        paths.append(tmp.name)

    return paths


def _cleanup(paths: list[str]):
    for p in paths:
        Path(p).unlink(missing_ok=True)


# ------------------------------------------------------------------
# Core experiment
# ------------------------------------------------------------------

def load_issues() -> list[dict]:
    """Load cached SWE-bench issues, newest first."""
    files = sorted(DATA_DIR.glob("swebench_verified_*.json"), reverse=True)
    if not files:
        print("[ERROR] No issue cache found. Run: python fetch_issues.py")
        return []
    with open(files[0], "r", encoding="utf-8") as f:
        return json.load(f)


def run_issue(issue: dict, text_client: TextClient, vlm_client: VLMClient,
              orchestrator: Orchestrator) -> dict:
    """Run all 4 conditions on a single issue."""
    instance_id = issue["instance_id"]
    title = issue["title"]
    body = issue["body"]
    image_urls = issue.get("image_urls", [])
    has_image = bool(image_urls)

    result = {
        "instance_id": instance_id,
        "repo": issue.get("repo", ""),
        "title": title,
        "has_image": has_image,
        "n_image_urls": len(image_urls),
        "c1_text": None,
        "c2_image": None,
        "c3_vanilla_mm": None,
        "c4_tns": None,
        "error": None,
    }

    tmp_paths = []

    try:
        # --- C1: Text-Only ---
        print(f"  [C1] text-only...")
        result["c1_text"] = text_client.analyze_bug_report(title, body)

        # --- Download images once (shared by C2 + C3) ---
        if has_image:
            unique_urls = list(dict.fromkeys(image_urls))
            if len(unique_urls) < len(image_urls):
                print(f"  [IMG] dedup'd {len(image_urls)}→{len(unique_urls)} urls")
            print(f"  [IMG] downloading {len(unique_urls)} images...")
            tmp_paths = _download_images(unique_urls)
            print(f"  [IMG] downloaded {len(tmp_paths)}/{len(unique_urls)}")

        # --- C2: Image-Only (ALL images, no body text) ---
        if tmp_paths:
            print(f"  [C2] image-only ({len(tmp_paths)} images)...")
            result["c2_image"] = vlm_client.analyze_images_only(tmp_paths, title)
        else:
            result["c2_image"] = {"skipped": True, "reason": "no images in issue"}

        # --- C3: Vanilla Multimodal (ALL images + full text) ---
        if tmp_paths:
            print(f"  [C3] vanilla multimodal ({len(tmp_paths)} images + text)...")
            result["c3_vanilla_mm"] = vlm_client.analyze_multimodal(
                tmp_paths, title, body
            )
        else:
            result["c3_vanilla_mm"] = {"skipped": True, "reason": "no images in issue"}

        # --- C4: TNS Synthesis ---
        c1_ok = result["c1_text"] and isinstance(result["c1_text"], dict)
        c2_ok = result["c2_image"] and not result["c2_image"].get("skipped")
        if c1_ok and c2_ok:
            print(f"  [C4] TNS synthesis...")
            result["c4_tns"] = orchestrator.synthesize(
                result["c1_text"], result["c2_image"]
            )
        else:
            result["c4_tns"] = {"skipped": True, "reason": "C1 or C2 unavailable"}

    except Exception as e:
        result["error"] = str(e)
        print(f"  [ERR] {instance_id}: {e}")
    finally:
        _cleanup(tmp_paths)

    return result


# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------

def print_summary(results: list[dict], elapsed: float):
    """Print 4-condition summary with key comparisons."""
    n = len(results)
    n_errors = sum(1 for r in results if r["error"])
    n_with_img = sum(1 for r in results if r["has_image"])

    def _conf(r, key):
        d = r.get(key)
        return d.get("confidence", 0) if isinstance(d, dict) else 0

    def _ok(r, key):
        d = r.get(key)
        return isinstance(d, dict) and not d.get("skipped")

    n_c1 = sum(1 for r in results if _ok(r, "c1_text"))
    n_c2 = sum(1 for r in results if _ok(r, "c2_image"))
    n_c3 = sum(1 for r in results if _ok(r, "c3_vanilla_mm"))
    n_c4 = sum(1 for r in results if _ok(r, "c4_tns"))

    c1_confs = [_conf(r, "c1_text") for r in results if _ok(r, "c1_text")]
    c2_confs = [_conf(r, "c2_image") for r in results if _ok(r, "c2_image")]
    c3_confs = [_conf(r, "c3_vanilla_mm") for r in results if _ok(r, "c3_vanilla_mm")]
    c4_confs = [_conf(r, "c4_tns") for r in results if _ok(r, "c4_tns")]

    def avg(xs): return sum(xs) / len(xs) if xs else 0

    # TNS uplift: C4 confidence vs best single modality (max of C1, C2)
    paired = [
        (r, _conf(r, "c4_tns"), max(_conf(r, "c1_text"), _conf(r, "c2_image")))
        for r in results if _ok(r, "c4_tns") and _ok(r, "c1_text") and _ok(r, "c2_image")
    ]
    tns_uplift = [tns - best for _, tns, best in paired]
    avg_uplift = sum(tns_uplift) / len(tns_uplift) if tns_uplift else 0

    # TNS vs Vanilla MM (THE key comparison)
    tns_vs_vanilla = [
        _conf(r, "c4_tns") - _conf(r, "c3_vanilla_mm")
        for r in results if _ok(r, "c4_tns") and _ok(r, "c3_vanilla_mm")
    ]
    avg_tns_vs_vanilla = sum(tns_vs_vanilla) / len(tns_vs_vanilla) if tns_vs_vanilla else 0

    # Vanilla MM uplift over best single modality
    vanilla_vs_best = [
        _conf(r, "c3_vanilla_mm") - max(_conf(r, "c1_text"), _conf(r, "c2_image"))
        for r in results
        if _ok(r, "c3_vanilla_mm") and _ok(r, "c1_text") and _ok(r, "c2_image")
    ]
    avg_vanilla_vs_best = sum(vanilla_vs_best) / len(vanilla_vs_best) if vanilla_vs_best else 0

    print(f"\n{'='*60}")
    print(f"  Experiment Summary (4 conditions)")
    print(f"{'='*60}")
    print(f"  Issues:            {n} ({n_with_img} with images)")
    print(f"  Errors:            {n_errors}")
    print(f"")
    print(f"  C1 (text) OK:      {n_c1}  avg conf={avg(c1_confs):.2f}")
    print(f"  C2 (image) OK:     {n_c2}  avg conf={avg(c2_confs):.2f}")
    print(f"  C3 (vanilla MM) OK:{n_c3}  avg conf={avg(c3_confs):.2f}")
    print(f"  C4 (TNS) OK:       {n_c4}  avg conf={avg(c4_confs):.2f}")
    print(f"")
    print(f"  --- Key Comparisons ---")
    print(f"  Vanilla MM vs best single: {avg_vanilla_vs_best:+.3f} Δconf")
    print(f"  TNS vs best single:        {avg_uplift:+.3f} Δconf")
    print(f"  TNS vs Vanilla MM:         {avg_tns_vs_vanilla:+.3f} Δconf  ★ primary")
    print(f"  Paired samples (TNS vs Vanilla): {len(tns_vs_vanilla)}")
    print(f"")
    print(f"  Total time:  {elapsed:.0f}s ({elapsed/60:.1f}m)")
    print(f"{'='*60}")


# ------------------------------------------------------------------
# Main
# ------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="P1 TNS Cross-Modal Experiment (4 conditions)")
    parser.add_argument("--count", type=int, default=N_ISSUES,
                        help=f"Issues to process (default: {N_ISSUES})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Validate clients without API calls")
    args = parser.parse_args()

    # Create run directory
    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = RESULTS_DIR / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    # Init clients
    print("Initializing clients...")
    try:
        text_client = TextClient()
        vlm_client = VLMClient()
        orchestrator = Orchestrator()
    except ValueError as e:
        print(f"[FATAL] {e}")
        return 1

    print(f"  Text model: {text_client.model}")
    print(f"  VLM model:  {vlm_client.model}")
    print(f"  TNS model:  {orchestrator.model}")
    print(f"  Run dir:    {run_dir}")

    if args.dry_run:
        print("\n[Dry-run] Clients initialized OK. No API calls made.")
        return 0

    # Load + slice issues
    issues = load_issues()
    if not issues:
        return 1
    issues = issues[:args.count]
    print(f"\nLoaded {len(issues)} issues")

    # Run experiment
    results = []
    t0 = time.time()
    for i, issue in enumerate(issues):
        print(f"\n--- [{i+1}/{len(issues)}] {issue['instance_id']} ---")
        result = run_issue(issue, text_client, vlm_client, orchestrator)
        results.append(result)

        # Save incrementally (every 5 issues)
        if (i + 1) % 5 == 0:
            interim_path = run_dir / f"results_partial_{i+1}.json"
            with open(interim_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)

        # Rate-limit courtesy: pause between issues
        if i < len(issues) - 1:
            time.sleep(ISSUE_DELAY)

    elapsed = time.time() - t0

    # Final save
    out_path = run_dir / "results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    # Stats
    ts = text_client.stats
    vs = vlm_client.stats
    os_ = orchestrator.stats
    print(f"\nAPI usage:")
    print(f"  Text: {ts['calls']} calls, {ts['total_tokens']} tokens")
    print(f"  VLM:  {vs['calls']} calls, {vs['total_tokens']} tokens")
    print(f"  TNS:  {os_['calls']} calls, {os_['total_tokens']} tokens")

    print_summary(results, elapsed)
    print(f"\nResults saved: {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
