"""
Quick smoke test: verify VLM connection and basic bug screenshot analysis.
Generates a synthetic bug screenshot if no real one is available.

Usage:
    python test_vlm.py                        # uses synthetic test image
    python test_vlm.py path/to/screenshot.png # uses your screenshot
"""
import sys
from pathlib import Path

# Ensure we can import from the experiment dir
sys.path.insert(0, str(Path(__file__).parent))

from vlm_client import VLMClient


def make_synthetic_bug_image(path: str = "test_bug.png"):
    """Generate a minimal synthetic error screenshot for testing."""
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[SKIP] Pillow not installed. Run: pip install Pillow")
        print("       Then pass a real screenshot: python test_vlm.py image.png")
        return None

    img = Image.new("RGB", (800, 400), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Simulate a terminal/console error
    lines = [
        ("$ pytest tests/test_auth.py", (0, 255, 0)),
        ("", None),
        ("FAILED tests/test_auth.py::test_login_redirect - assert 200 == 302", (255, 80, 80)),
        ("", None),
        ("    def test_login_redirect():", (200, 200, 200)),
        ("        resp = client.post('/login', data=creds)", (200, 200, 200)),
        (">       assert resp.status_code == 302", (255, 80, 80)),
        ("E       assert 200 == 302", (255, 80, 80)),
        ("", None),
        ("tests/test_auth.py:47: AssertionError", (255, 200, 100)),
    ]

    y = 40
    try:
        font = ImageFont.truetype("consola.ttf", 16)
    except Exception:
        font = ImageFont.load_default()

    for text, color in lines:
        if text:
            draw.text((30, y), text, fill=color or (200, 200, 200), font=font)
        y += 26

    img.save(path)
    print(f"[OK] Synthetic bug screenshot saved: {path}")
    return path


def main():
    print("=" * 50)
    print("  TNS VLM Smoke Test — Qwen3.5-4B via SiliconFlow")
    print("=" * 50)

    # 1. Init client
    print("\n[1/3] Initializing client...")
    try:
        client = VLMClient()
        print(f"  model : {client.model}")
        print(f"  base  : {client.base_url}")
    except ValueError as e:
        print(f"\n  [FAIL] {e}")
        print("\n  Fix: cp .env.example .env  →  fill your API key from")
        print("       https://cloud.siliconflow.cn/account/ak")
        return 1

    # 2. Prepare test image
    print("\n[2/3] Preparing test image...")
    image_path = sys.argv[1] if len(sys.argv) > 1 else None
    if image_path and Path(image_path).exists():
        print(f"  using: {image_path}")
    else:
        if image_path:
            print(f"  [WARN] '{image_path}' not found, generating synthetic...")
        image_path = make_synthetic_bug_image()
        if not image_path:
            return 1

    # 3. Analyze
    print("\n[3/3] Analyzing screenshot...")
    try:
        fragment = client.analyze_bug_screenshot(image_path)
    except Exception as e:
        print(f"\n  [FAIL] API call failed: {e}")
        return 1

    # Results
    print("\n" + "=" * 50)
    print("  Experience Fragment")
    print("=" * 50)
    print(f"\n  Source:     {fragment['source']}")
    print(f"  Confidence: {fragment['confidence']}")
    print(f"\n  Observations:")
    for obs in fragment.get("observations", []):
        print(f"    - {obs}")
    print(f"\n  Causal Hypothesis:")
    print(f"    {fragment['causal_hypothesis']}")
    print(f"\n  Missing Info:")
    for m in fragment.get("missing_info", []):
        print(f"    - {m}")

    # Stats
    s = client.stats
    print(f"\n{'=' * 50}")
    print(f"  Calls: {s['calls']} | Tokens: {s['total_tokens']} | Cost: free")
    print(f"{'=' * 50}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
