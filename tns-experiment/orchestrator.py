"""
TNS Orchestrator — C3 condition: cross-modal autobiographer synthesis.

Given experience fragments from C1 (text) and C2 (image), the autobiographer
synthesizes a unified causal narrative that integrates both modalities.

Usage:
    orch = Orchestrator()
    synthesis = orch.synthesize(text_fragment, image_fragment)
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


class Orchestrator:
    """Cross-modal autobiographer — synthesizes text + image fragments."""

    def __init__(self, model: str = ""):
        self.model = model or TEXT_MODEL
        self.api_key = SILICONFLOW_API_KEY
        self.base_url = SILICONFLOW_BASE_URL.rstrip("/")
        self._call_count = 0
        self._total_tokens = 0

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def synthesize(self, text_fragment: dict, image_fragment: dict) -> dict:
        """Synthesize two single-modality fragments into a cross-modal narrative.

        Returns:
            {
                "source": "tns",
                "modalities": ["text", "image"],
                "shared_observations": [...],       # confirmed by both modalities
                "text_only_observations": [...],    # only in text
                "image_only_observations": [...],   # only in image
                "contradictions": [...],            # where modalities disagree
                "causal_hypothesis": "str",         # unified root cause
                "confidence": 0.0,
                "modal_weights": {"text": 0.0, "image": 0.0},
                "synthesis_narrative": "str",       # ~2-3 sentence narrative
                "missing_info": [...],
            }
        """
        prompt = self._synthesis_prompt(text_fragment, image_fragment)
        raw = self._call_api(prompt)
        return self._parse_synthesis(raw)

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _synthesis_prompt(self, text: dict, image: dict) -> str:
        return f"""You are the AUTOBIOGRAPHER — the chief agent in a Temporal Narrative Synthesis (TNS) experiment. Your role is to read experience fragments from two modality-specific agents (text-only and image-only) and synthesize them into a unified causal diagnosis.

## TEXT AGENT FRAGMENT
Observations: {json.dumps(text.get("observations", []), ensure_ascii=False)}
Hypothesis: {text.get("causal_hypothesis", "")}
Confidence: {text.get("confidence", 0)}
Missing info: {json.dumps(text.get("missing_info", []), ensure_ascii=False)}

## IMAGE AGENT FRAGMENT
Observations: {json.dumps(image.get("observations", []), ensure_ascii=False)}
Hypothesis: {image.get("causal_hypothesis", "")}
Confidence: {image.get("confidence", 0)}
Missing info: {json.dumps(image.get("missing_info", []), ensure_ascii=False)}

## YOUR TASK
Synthesize these two fragments. Output a JSON object:
- "shared_observations": facts both agents independently observed
- "text_only_observations": facts only the text agent could see
- "image_only_observations": facts only the image agent could see
- "contradictions": any points where the two agents disagree
- "causal_hypothesis": one unified root-cause sentence
- "confidence": 0.0-1.0 (should be higher than either single modality if they agree, lower if they contradict)
- "modal_weights": {{"text": 0.0-1.0, "image": 0.0-1.0}} — how much each modality contributed to the final diagnosis
- "synthesis_narrative": 2-3 sentence narrative describing what happened, integrating both modalities' evidence
- "missing_info": what neither modality could determine

Output ONLY the JSON object."""

    def _call_api(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": MAX_OUTPUT_TOKENS * 2,  # synthesis needs more tokens
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
                    print(f"    [TNS retry {attempt+1}/{RETRY_MAX}] timeout, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"TNS API timeout after {RETRY_MAX} attempts")

            elapsed = time.time() - t0

            if resp.status_code == 429:
                if attempt < RETRY_MAX - 1:
                    import random
                    delay = RETRY_BASE_DELAY ** (attempt + 1) + random.uniform(0, 2)
                    print(f"    [TNS retry {attempt+1}/{RETRY_MAX}] 429, waiting {delay:.0f}s")
                    time.sleep(delay)
                    continue
                raise RuntimeError(f"TNS rate limited after {RETRY_MAX} attempts")

            if not resp.ok:
                raise RuntimeError(f"API error {resp.status_code}: {resp.text[:500]}")
            break

        data = resp.json()
        self._call_count += 1
        usage = data.get("usage", {})
        self._total_tokens += usage.get("total_tokens", 0)

        content = data["choices"][0]["message"]["content"]
        print(f"[TNS] {self.model} | {elapsed:.1f}s | "
              f"tokens: {usage.get('total_tokens', '?')}")
        return content

    def _parse_synthesis(self, raw: str) -> dict:
        text = raw.strip()
        m = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
        if m:
            text = m.group(1).strip()

        try:
            result = json.loads(text)
        except json.JSONDecodeError:
            m = re.search(r"\{.*\}", text, re.DOTALL)
            if m:
                try:
                    result = json.loads(m.group())
                except json.JSONDecodeError:
                    result = self._raw_fallback(raw)
            else:
                result = self._raw_fallback(raw)

        # Validate required fields
        defaults = {
            "source": "tns",
            "modalities": ["text", "image"],
            "shared_observations": [],
            "text_only_observations": [],
            "image_only_observations": [],
            "contradictions": [],
            "causal_hypothesis": "",
            "confidence": 0.0,
            "modal_weights": {"text": 0.0, "image": 0.0},
            "synthesis_narrative": "",
            "missing_info": [],
        }
        for k, v in defaults.items():
            if k not in result:
                result[k] = v
        return result

    def _raw_fallback(self, raw: str) -> dict:
        return {"source": "tns", "modalities": ["text", "image"],
                "shared_observations": [], "text_only_observations": [],
                "image_only_observations": [], "contradictions": [],
                "causal_hypothesis": "", "confidence": 0.0,
                "modal_weights": {"text": 0.0, "image": 0.0},
                "synthesis_narrative": raw[:2000], "missing_info": ["parse failure"]}

    @property
    def stats(self) -> dict:
        return {"model": self.model, "calls": self._call_count,
                "total_tokens": self._total_tokens}
