"""
SiliconFlow VLM Client — OpenAI-compatible chat completions for vision models.

Usage:
    client = VLMClient()
    fragment = client.analyze_bug_screenshot("screenshot.png")
"""
import base64
import json
import time
from pathlib import Path
from typing import Optional

import requests

from config import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_BASE_URL,
    VLM_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
    TIMEOUT,
    RETRY_MAX,
    RETRY_BASE_DELAY,
    API_SEED,
)


class VLMClient:
    """Minimal SiliconFlow VLM client for bug screenshot analysis."""

    def __init__(self, model: str = VLM_MODEL, api_key: str = "", base_url: str = ""):
        self.model = model
        self.api_key = api_key or SILICONFLOW_API_KEY
        self.base_url = (base_url or SILICONFLOW_BASE_URL).rstrip("/")
        self._call_count = 0
        self._total_tokens = 0

        if not self.api_key:
            raise ValueError(
                "API key not set. Copy .env.example to .env and fill in "
                "SILICONFLOW_API_KEY from https://cloud.siliconflow.cn/account/ak"
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_images_only(
        self,
        image_paths: list[str | Path],
        title: str = "",
    ) -> dict:
        """C2: VLM sees ALL screenshots but NOT the bug report body.

        Mirrors the text-only condition: one modality, one fragment.
        The VLM gets the issue title for grounding but no body text —
        it must diagnose purely from visual evidence.
        """
        b64s = [self._encode_image(p) for p in image_paths]
        prompt = self._image_diagnosis_prompt(title)
        raw = self._call_api(b64s, prompt)
        return self._parse_fragment(raw)

    def analyze_bug_screenshot(
        self,
        image_path: str | Path,
        extra_context: str = "",
    ) -> dict:
        """Analyze a bug screenshot → experience fragment.

        Args:
            image_path: path to PNG/JPEG screenshot
            extra_context: optional issue title or description for grounding

        Returns:
            dict matching FRAGMENT_SCHEMA: {source, observations,
            causal_hypothesis, confidence, missing_info}
        """
        b64 = self._encode_image(image_path)
        prompt = self._bug_diagnosis_prompt(extra_context)
        raw = self._call_api([b64], prompt)
        return self._parse_fragment(raw)

    def analyze_multimodal(
        self,
        image_paths: list[str | Path],
        title: str = "",
        body: str = "",
    ) -> dict:
        """Vanilla multimodal: give VLM all images + full text → fragment.

        This is the STANDARD approach baseline — one model sees everything at once.
        """
        b64s = [self._encode_image(p) for p in image_paths]
        prompt = self._multimodal_diagnosis_prompt(title, body)
        raw = self._call_api(b64s, prompt)
        return self._parse_fragment(raw)

    def call(self, image_path: str | Path, prompt: str) -> str:
        """Raw VLM call — image + free-text prompt → model response."""
        b64 = self._encode_image(image_path)
        return self._call_api([b64], prompt)

    def analyze_image_url(self, image_url: str, extra_context: str = "") -> dict:
        """Download an image URL → analyze → experience fragment."""
        import tempfile
        import time
        import requests as req

        print(f"  [VLM] downloading image: {image_url[:80]}...")

        # GitHub CDN often rate-limits; retry with backoff + proper headers
        resp = None
        last_err = None
        for attempt in range(3):
            try:
                resp = req.get(image_url, timeout=30, headers={
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
            time.sleep(2 ** attempt)  # 1s, 2s, 4s backoff

        if resp is None or not resp.ok or len(resp.content) <= 1000:
            raise RuntimeError(
                f"Failed to download image after 3 attempts ({last_err}): {image_url}"
            )

        suffix = ".png"
        content_type = resp.headers.get("content-type", "")
        if "jpeg" in content_type or "jpg" in content_type:
            suffix = ".jpg"
        elif "gif" in content_type:
            suffix = ".gif"
        elif "webp" in content_type:
            suffix = ".webp"

        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
            f.write(resp.content)
            tmp_path = f.name

        try:
            fragment = self.analyze_bug_screenshot(tmp_path, extra_context)
        finally:
            Path(tmp_path).unlink(missing_ok=True)

        return fragment

    # ------------------------------------------------------------------
    # Prompts (calibrated against text_client.py for fair comparison)
    # ------------------------------------------------------------------

    def _bug_diagnosis_prompt(self, context: str = "") -> str:
        """C2 single-image prompt (kept for backward compat — analyze_image_url)."""
        return self._image_diagnosis_prompt(context)

    def _image_diagnosis_prompt(self, title: str = "") -> str:
        """C2 prompt: diagnose from screenshots ONLY, no text body.

        Matches the detail level of text_client._text_diagnosis_prompt
        for fair single-modality comparison.
        """
        base = f"""You are a senior software engineer diagnosing a bug from screenshots ONLY.
You CANNOT read the bug report text — you only see images.

Analyze these screenshots and output a JSON object with these fields:
- "observations": list of strings describing what you OBSERVE VISUALLY
  (UI anomalies, error messages visible on screen, unexpected states,
  layout issues, missing elements, stack traces in screenshots,
  code snippets visible, terminal output, browser devtools, etc.)
- "causal_hypothesis": one sentence describing the most likely root cause
  based on visual evidence alone
- "confidence": number 0.0-1.0 — how confident you are given visual-only evidence
- "missing_info": list of strings describing what you CANNOT determine from
  images alone (e.g., "exact code logic", "runtime state not visible",
  "configuration values", "what happened before the screenshot")

Output ONLY the JSON object, no markdown fences, no preamble."""
        if title:
            base += f"\n\nIssue title (for context only — the body text is HIDDEN from you): {title}"
        return base

    def _multimodal_diagnosis_prompt(self, title: str, body: str) -> str:
        """C3 prompt: diagnose from BOTH screenshots AND full bug report text.

        This is the STANDARD multimodal approach — one model sees everything.
        Prompt matches the combined detail of C1 + C2 prompts.
        """
        return f"""You are a senior software engineer diagnosing a bug from BOTH screenshots AND the full bug report text.

Analyze ALL evidence (images + text) together and output a JSON object:
- "observations": list of strings describing KEY FINDINGS from BOTH modalities
  (include what you see in screenshots AND what you read in the text —
  error messages, visual anomalies, reproduction steps, environment clues,
  affected components, version info, referenced files/lines, stack traces)
- "causal_hypothesis": one sentence describing the most likely root cause,
  integrating evidence from BOTH text and images
- "confidence": number 0.0-1.0 — how confident you are in the integrated diagnosis
- "missing_info": list of strings describing what NEITHER text nor images reveal
  (e.g., "exact runtime state at crash point", "specific config values",
  "upstream dependency behavior")

Output ONLY the JSON object, no markdown fences, no preamble.

BUG REPORT
Title: {title}

Body:
{body[:4000]}"""

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _encode_image(self, path: str | Path, max_size: int = 1024) -> str:
        """Encode image to base64 data URL, optionally resizing to save bandwidth."""
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(f"Image not found: {p}")

        ext = p.suffix.lower()
        mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg",
                "webp": "image/webp", "gif": "image/gif"}.get(ext, "image/png")

        data = p.read_bytes()
        orig_size = len(data)

        # Resize large images to reduce VLM latency
        try:
            from io import BytesIO
            from PIL import Image
            img = Image.open(BytesIO(data))
            w, h = img.size
            if max(w, h) > max_size:
                scale = max_size / max(w, h)
                new_size = (int(w * scale), int(h * scale))
                img = img.resize(new_size, Image.LANCZOS)
                buf = BytesIO()
                fmt = "JPEG" if ext in (".jpg", ".jpeg") else "PNG"
                img.save(buf, format=fmt, optimize=True)
                data = buf.getvalue()
                print(f"  [VLM] resized {w}x{h} → {new_size[0]}x{new_size[1]} "
                      f"({orig_size}→{len(data)} bytes)")
        except ImportError:
            pass  # PIL not available, send original

        b64 = base64.b64encode(data).decode("ascii")
        return f"data:{mime};base64,{b64}"

    def _call_api(self, image_data_urls: list[str], prompt: str) -> str:
        """Single-turn VLM chat completion with 1+ images + retry on 429."""
        content_parts = []
        for url in image_data_urls:
            content_parts.append({"type": "image_url", "image_url": {"url": url}})
        content_parts.append({"type": "text", "text": prompt})

        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": content_parts}],
            "max_tokens": MAX_OUTPUT_TOKENS,
            "temperature": TEMPERATURE,
            "seed": API_SEED,
            "stream": False,
        }

        last_err = None
        for attempt in range(RETRY_MAX):
            t0 = time.time()
            try:
                resp = requests.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json",
                    },
                    timeout=TIMEOUT,
                )
            except requests.Timeout:
                last_err = f"timeout after {TIMEOUT}s"
                if attempt < RETRY_MAX - 1:
                    delay = RETRY_BASE_DELAY ** attempt
                    print(f"    [VLM retry {attempt+1}/{RETRY_MAX}] {last_err}, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"VLM API timeout after {RETRY_MAX} attempts")

            elapsed = time.time() - t0

            if resp.status_code == 429:
                last_err = f"rate limited (429): {resp.text[:200]}"
                if attempt < RETRY_MAX - 1:
                    import random
                    delay = RETRY_BASE_DELAY ** (attempt + 1) + random.uniform(0, 2)
                    print(f"    [VLM retry {attempt+1}/{RETRY_MAX}] 429, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"VLM rate limited after {RETRY_MAX} attempts")

            if not resp.ok:
                raise RuntimeError(
                    f"API error {resp.status_code}: {resp.text[:500]}"
                )
            break  # success

        data = resp.json()
        self._call_count += 1
        usage = data.get("usage", {})
        self._total_tokens += usage.get("total_tokens", 0)

        content = data["choices"][0]["message"]["content"]
        # Diagnose empty-content responses (some models split reasoning vs output)
        if not content or not content.strip():
            reasoning = data["choices"][0]["message"].get("reasoning_content", "")
            finish_reason = data["choices"][0].get("finish_reason", "?")
            print(f"[VLM] WARNING: empty content! finish_reason={finish_reason}, "
                  f"reasoning_len={len(reasoning)}")
            if not content:
                content = reasoning or ""
        print(f"[VLM] {self.model} | {elapsed:.1f}s | "
              f"tokens: {usage.get('total_tokens', '?')} | "
              f"content_len: {len(content)}")
        return content

    def _parse_fragment(self, raw: str) -> dict:
        """Extract JSON fragment from model output, with multi-strategy fallback."""
        import re

        text = raw.strip()

        # Strategy 1: extract from ```json / ``` fence (many small VLMs ignore
        # "no fences" instruction — handle it anyway)
        m = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
        if m:
            text = m.group(1).strip()

        # Strategy 2: try direct parse
        try:
            fragment = json.loads(text)
        except json.JSONDecodeError:
            # Strategy 3: find outermost {...} — greedy, handles nested objects
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                try:
                    fragment = json.loads(m.group())
                except json.JSONDecodeError:
                    fragment = self._raw_fallback(raw)
            else:
                fragment = self._raw_fallback(raw)

        # Validate required fields
        for key in ["observations", "causal_hypothesis", "confidence", "missing_info"]:
            if key not in fragment:
                fragment[key] = [] if key in ("observations", "missing_info") else (
                    0.0 if key == "confidence" else ""
                )

        fragment["source"] = "image"

        # Debug: log raw output when parsing fell through to fallback
        if fragment["confidence"] == 0.0 and not fragment["observations"]:
            print(f"  [VLM DEBUG] parse fallback triggered. Raw output (first 300 chars):")
            print(f"    {raw[:300]}")

        return fragment

    def _raw_fallback(self, raw: str) -> dict:
        """When JSON parsing fails, wrap raw text as observations."""
        return {
            "source": "image",
            "observations": [raw[:2000]],
            "causal_hypothesis": "",
            "confidence": 0.0,
            "missing_info": ["JSON parse failed — see raw observations"],
        }

    @property
    def stats(self) -> dict:
        return {
            "model": self.model,
            "calls": self._call_count,
            "total_tokens": self._total_tokens,
        }
