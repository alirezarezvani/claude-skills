#!/usr/bin/env python3
"""LLM judge for content quality (headlines, titles, descriptions).
Uses the user's existing CLI tool (claude, codex, gemini) for evaluation.
DO NOT MODIFY after experiment starts — this is the fixed evaluator."""

import subprocess
import sys
from pathlib import Path

# --- CONFIGURE THESE ---
TARGET_FILE = "content/titles.md"  # File being optimized
CLI_TOOL = "claude"                # or: codex, gemini
# --- END CONFIG ---

# The judge prompt is FIXED — the agent cannot change how it's evaluated
JUDGE_PROMPT = """You are a content quality evaluator. Score the following content strictly.

Criteria (each scored 1-10):

1. CURIOSITY GAP — Does this make you want to click? Is there an information gap
   that can only be resolved by reading? Generic titles score 1-3. Specific,
   intriguing titles score 7-10.

2. SPECIFICITY — Are there concrete numbers, tools, or details? "How I improved
   performance" = 2. "How I reduced API latency from 800ms to 185ms" = 9.

3. EMOTIONAL PULL — Does it trigger curiosity, surprise, fear of missing out,
   or recognition? Flat titles score 1-3. Emotionally charged score 7-10.

4. SCROLL-STOP POWER — Would this stop someone scrolling through a feed or
   search results? Would they pause on this headline? Rate honestly.

5. SEO KEYWORD PRESENCE — Are searchable, high-intent terms present naturally?
   Keyword-stuffed = 3. Natural integration of search terms = 8-10.

Output EXACTLY this format (nothing else):
curiosity: <score>
specificity: <score>
emotional: <score>
scroll_stop: <score>
seo: <score>
ctr_score: <average of all 5 scores>

Be harsh. Most content is mediocre (4-6 range). Only exceptional content scores 8+."""

try:
    content = Path(TARGET_FILE).read_text()
except FileNotFoundError:
    print(f"Target file not found: {TARGET_FILE}", file=sys.stderr)
    sys.exit(1)

full_prompt = f"{JUDGE_PROMPT}\n\n---\n\nContent to evaluate:\n\n{content}"

# Call the user's CLI tool
result = subprocess.run(
    [CLI_TOOL, "-p", full_prompt],
    capture_output=True, text=True, timeout=120
)

if result.returncode != 0:
    print(f"LLM judge failed: {result.stderr[:200]}", file=sys.stderr)
    sys.exit(1)

# Parse output — look for ctr_score line
output = result.stdout
for line in output.splitlines():
    line = line.strip()
    if line.startswith("ctr_score:"):
        print(line)
    elif line.startswith(("curiosity:", "specificity:", "emotional:", "scroll_stop:", "seo:")):
        print(line)

# Verify ctr_score was found
if "ctr_score:" not in output:
    print("Could not parse ctr_score from LLM output", file=sys.stderr)
    print(f"Raw output: {output[:500]}", file=sys.stderr)
    sys.exit(1)
