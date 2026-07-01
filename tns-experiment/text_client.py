"""
Text-Only Client — C1 condition: DeepSeek V3 analyzes bug reports as plain text.
Uses SiliconFlow's OpenAI-compatible API. Outputs experience fragments.

Usage:
    client = TextClient()
    fragment = client.analyze_bug_report(issue_title, issue_body)
"""
import json
import re
import time

import requests

from config import (
    SILICONFLOW_API_KEY,
    SILICONFLOW_BASE_URL,
    TEXT_MODEL,
    MAX_OUTPUT_TOKENS,
    TEMPERATURE,
    TIMEOUT,
    RETRY_MAX,
    RETRY_BASE_DELAY,
    API_SEED,
)


class TextClient:
    """SiliconFlow text-only client for bug report analysis (C1 condition)."""

    def __init__(self, model: str = ""):
        self.model = model or TEXT_MODEL
        self.api_key = SILICONFLOW_API_KEY
        self.base_url = SILICONFLOW_BASE_URL.rstrip("/")
        self._call_count = 0
        self._total_tokens = 0

        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY not set in .env")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def analyze_bug_report(self, title: str, body: str) -> dict:
        """Analyze a bug report (title + body) → experience fragment.

        Returns dict matching FRAGMENT_SCHEMA with source="text".
        """
        prompt = self._text_diagnosis_prompt(title, body)
        raw = self._call_api(prompt)
        return self._parse_fragment(raw)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _text_diagnosis_prompt(self, title: str, body: str) -> str:
        return f"""You are a senior software engineer diagnosing a bug from its text report.

Analyze this bug report and output a JSON object with these fields:
- "observations": list of strings describing what you observe from the text
  (symptoms, error messages, environment clues, reproduction steps mentioned,
  affected components, version info, referenced files/lines)
- "causal_hypothesis": one sentence describing the most likely root cause
- "confidence": number 0.0-1.0 indicating how confident you are in the hypothesis
- "missing_info": list of strings describing what you CANNOT determine from
  text alone (e.g., "actual runtime behavior", "screenshots/visual evidence",
  "exact configuration values")

Output ONLY the JSON object, no markdown fences, no preamble.

BUG REPORT
Title: {title}

Body:
{body[:4000]}"""

    def _call_api(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_OUTPUT_TOKENS,
            "temperature": TEMPERATURE,
            "seed": API_SEED,
            "stream": False,
        }

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
                if attempt < RETRY_MAX - 1:
                    delay = RETRY_BASE_DELAY ** attempt
                    print(f"    [TEXT retry {attempt+1}/{RETRY_MAX}] timeout, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Text API timeout after {RETRY_MAX} attempts")

            elapsed = time.time() - t0

            if resp.status_code == 429:
                if attempt < RETRY_MAX - 1:
                    import random
                    delay = RETRY_BASE_DELAY ** (attempt + 1) + random.uniform(0, 2)
                    print(f"    [TEXT retry {attempt+1}/{RETRY_MAX}] 429, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"Text rate limited after {RETRY_MAX} attempts")

            if not resp.ok:
                raise RuntimeError(f"API error {resp.status_code}: {resp.text[:500]}")
            break

        data = resp.json()
        self._call_count += 1
        usage = data.get("usage", {})
        self._total_tokens += usage.get("total_tokens", 0)

        content = data["choices"][0]["message"]["content"]
        print(f"[TEXT] {self.model} | {elapsed:.1f}s | "
              f"tokens: {usage.get('total_tokens', '?')}")
        return content

    def _parse_fragment(self, raw: str) -> dict:
        text = raw.strip()
        # Extract from ```json ... ``` fence
        m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if m:
            text = m.group(1).strip()

        try:
            fragment = json.loads(text)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                try:
                    fragment = json.loads(m.group())
                except json.JSONDecodeError:
                    fragment = self._raw_fallback(raw)
            else:
                fragment = self._raw_fallback(raw)

        for key in ["observations", "causal_hypothesis", "confidence", "missing_info"]:
            if key not in fragment:
                fragment[key] = [] if key in ("observations", "missing_info") else (
                    0.0 if key == "confidence" else ""
                )
        fragment["source"] = "text"
        return fragment

    def _raw_fallback(self, raw: str) -> dict:
        return {
            "source": "text",
            "observations": [raw[:2000]],
            "causal_hypothesis": "",
            "confidence": 0.0,
            "missing_info": ["JSON parse failed — see raw observations"],
        }

    @property
    def stats(self) -> dict:
        return {"model": self.model, "calls": self._call_count,
                "total_tokens": self._total_tokens}
