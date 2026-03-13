# Experiment Domains Guide

## Domain 1: ML Training (Karpathy-style)

**Best for:** LLM/neural net training optimization on a single GPU

**Requirements:**
- NVIDIA GPU (H100 recommended, A100/RTX also work)
- CUDA + PyTorch
- `uv` package manager
- ~50GB disk (training data)

**Setup:**
```bash
# Clone autoresearch repo (the ML training environment)
git clone https://github.com/karpathy/autoresearch my-ml-research
cd my-ml-research
uv sync
uv run prepare.py  # one-time data download + tokenizer (~2 min)

# Initialize autoresearch skill
cp -r ~/.claude/skills/autoresearch-agent/scripts ./scripts

# Configure
python scripts/setup_experiment.py --domain ml --tag mar13
```

**Metric:** `val_bpb` — validation bits per byte. Lower = better model.

**What the agent can change in `train.py`:**
- Model depth, width, attention heads
- Learning rate, scheduler, warmup
- Optimizer (Muon, AdamW, variants)
- Batch size, gradient accumulation
- Architecture (attention patterns, FFN type)

**Tip for smaller GPUs (Mac M-series, RTX 3090 etc):**
Karpathy recommends forks for non-H100 hardware. Lower `DEPTH` to 4, use TinyStories dataset, lower `MAX_SEQ_LEN` to 256.

---

## Domain 2: Prompt Engineering

**Best for:** Optimizing system prompts for quality/accuracy/tone

**Requirements:**
- LLM API access (OpenAI, Anthropic, etc.)
- Test cases with expected outputs
- An LLM judge for scoring (can be same model)

**Setup:**
```bash
mkdir my-prompt-research && cd my-prompt-research
git init

# Create prompt.md (the thing being optimized)
echo "You are a helpful assistant." > prompt.md

# Create evaluate.py (fixed — never modify)
cat > evaluate.py << 'EOF'
#!/usr/bin/env python3
# Fixed evaluation harness — DO NOT MODIFY
import json, sys
from pathlib import Path

PROMPT = Path("prompt.md").read_text()
# Load test cases
TEST_CASES = json.loads(Path("tests/cases.json").read_text())

# Run prompt against test cases, score with LLM judge
# ... (customize for your LLM + scoring logic)
total = sum(score_case(PROMPT, case) for case in TEST_CASES)
score = total / len(TEST_CASES) * 100
print(f"eval_score: {score:.2f}")
EOF

# Initialize
python scripts/setup_experiment.py --domain prompt --tag mar13
```

**Metric:** `eval_score` (0-100). Higher = better prompt.

---

## Domain 3: Code Performance

**Best for:** Optimizing a specific hot module for speed

**Requirements:**
- A Python module with measurable performance
- Existing tests (correctness must not regress)
- A benchmark harness

**Setup:**
```bash
cd my-project

# Create benchmark.py (fixed — never modify)
cat > benchmark.py << 'EOF'
#!/usr/bin/env python3
# Fixed benchmark — DO NOT MODIFY
import time, statistics
from src.module import your_function
from tests.test_module import run_tests

# Correctness check first
if not run_tests():
    print("TESTS FAILED")
    sys.exit(1)

# Benchmark
data = generate_test_data(n=10000)
times = []
for _ in range(10):
    t0 = time.perf_counter()
    your_function(data)
    times.append((time.perf_counter() - t0) * 1000)

p50 = statistics.median(times)
print(f"p50_ms: {p50:.2f}")
print(f"p95_ms: {statistics.quantiles(times, n=20)[18]:.2f}")
EOF

python scripts/setup_experiment.py --domain code \
  --target src/module.py \
  --tag mar13
```

**Metric:** `p50_ms` — median latency. Lower = faster.

---

## Domain 4: Agent Skill Optimization

**Best for:** Improving the quality of claude-skills SKILL.md files

**Requirements:**
- A SKILL.md to optimize
- A task evaluation suite (15-20 standardized tasks)
- An LLM judge for scoring

**Setup:**
```bash
# Create a new skill research project
mkdir skill-research-{skill-name} && cd skill-research-{skill-name}
git init

# Copy the skill to optimize
cp ~/.claude/skills/{skill-name}/SKILL.md .

# Create evaluate.py
cat > scripts/skill_evaluator.py << 'EOF'
#!/usr/bin/env python3
# Fixed evaluator — DO NOT MODIFY
# Runs SKILL.md against 15 standardized tasks using LLM judge
# Outputs: pass_rate: 0.80 (etc.)
EOF

python scripts/setup_experiment.py --domain skill --tag mar13
```

**Metric:** `pass_rate` (0-1). Higher = better skill.

---

## Choosing Your Domain

| Question | Recommendation |
|----------|---------------|
| Do I have a GPU and want to improve an LLM? | ML Training |
| Do I want to improve a prompt/system message? | Prompt Engineering |
| Do I have slow Python code I want to speed up? | Code Performance |
| Do I want to improve one of my claude-skills? | Skill Optimization |

**First time?** Start with **Prompt Engineering** — no GPU required, fast experiments (2 min each), immediately applicable results.
