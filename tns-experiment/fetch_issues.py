"""
SWE-bench Issue Fetcher — downloads verified issues from HuggingFace.

The SWE-bench Verified subset contains 500 hand-validated issues with patches.
We sample N_ISSUES randomly from the verified set, prioritizing issues that have
both text descriptions AND linked screenshots/images in the body.

Usage:
    python fetch_issues.py              # fetch and cache to data/
    python fetch_issues.py --count 10   # sample 10 instead of config default
"""
import argparse
import json
import re
import sys
from pathlib import Path
from random import Random

sys.path.insert(0, str(Path(__file__).parent))
from config import DATA_DIR, N_ISSUES

SWE_BENCH_DATASET = "princeton-nlp/SWE-bench_Verified"


def has_images(text: str) -> bool:
    """Check if issue body contains image links."""
    if not text:
        return False
    patterns = [
        r"!\[.*?\]\(.*?\)",           # markdown image
        r"https?://\S+\.(?:png|jpg|jpeg|gif|webp)",  # direct image URL
        r"<img\s",                    # HTML img tag
        r"screenshot",                # mentions screenshot
    ]
    return any(re.search(p, text, re.IGNORECASE) for p in patterns)


def extract_image_urls(text: str) -> list[str]:
    """Extract image URLs from issue body."""
    urls = []
    # Markdown images: ![alt](url)
    urls.extend(re.findall(r"!\[.*?\]\((https?://\S+)\)", text, re.IGNORECASE))
    # Direct image URLs
    urls.extend(re.findall(r"(https?://\S+\.(?:png|jpg|jpeg|gif|webp))", text, re.IGNORECASE))
    return urls


def fetch_issues(count: int = N_ISSUES, seed: int = 42) -> list[dict]:
    """Fetch SWE-bench verified issues, preferring those with images."""
    try:
        from datasets import load_dataset
    except ImportError:
        print("[ERROR] datasets not installed. Run: python -m pip install datasets")
        return []

    print(f"Loading {SWE_BENCH_DATASET} ...")
    ds = load_dataset(SWE_BENCH_DATASET, split="test")
    print(f"  {len(ds)} verified issues total")

    # Split: issues with images vs without
    with_images, without_images = [], []
    for row in ds:
        body = row.get("problem_statement", "") or row.get("issue_body", "") or ""
        entry = {
            "instance_id": row.get("instance_id", ""),
            "repo": row.get("repo", ""),
            "title": row.get("issue_title", "") or row.get("problem_statement", "")[:100],
            "body": body,
            "base_commit": row.get("base_commit", ""),
            "has_images": has_images(body),
            "image_urls": extract_image_urls(body),
        }
        if entry["has_images"]:
            with_images.append(entry)
        else:
            without_images.append(entry)

    print(f"  with images: {len(with_images)}, without: {len(without_images)}")

    # Sample: 70% from with-images, 30% from without-images
    rng = Random(seed)
    n_img = min(len(with_images), int(count * 0.7))
    n_noimg = count - n_img

    sampled = (
        rng.sample(with_images, n_img) +
        rng.sample(without_images, n_noimg)
    )
    rng.shuffle(sampled)

    print(f"  sampled: {n_img} with images + {n_noimg} without = {len(sampled)}")
    return sampled


def main():
    parser = argparse.ArgumentParser(description="Fetch SWE-bench verified issues")
    parser.add_argument("--count", type=int, default=N_ISSUES,
                        help=f"Number of issues to sample (default: {N_ISSUES})")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    issues = fetch_issues(count=args.count, seed=args.seed)
    if not issues:
        return 1

    out_path = DATA_DIR / f"swebench_verified_n{len(issues)}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(issues, f, ensure_ascii=False, indent=2)

    n_img = sum(1 for i in issues if i["has_images"])
    n_urls = sum(len(i["image_urls"]) for i in issues)
    print(f"\nSaved: {out_path}")
    print(f"  issues: {len(issues)} ({n_img} with images, {n_urls} image URLs)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
