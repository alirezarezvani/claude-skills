"""
TNS Experiment Config — centralized model settings and paths.
Loads from .env, falls back to defaults.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).parent
load_dotenv(ROOT / ".env")

# === API ===
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY", "")
SILICONFLOW_BASE_URL = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1")

# === Models ===
VLM_MODEL = os.getenv("VLM_MODEL", "Qwen/Qwen3.5-397B-A17B")  # MoE 17B active
VLM_MODEL_FALLBACK = "Qwen/Qwen3-VL-32B-Instruct"             # dedicated VLM
TEXT_MODEL = os.getenv("TEXT_MODEL", "deepseek-ai/DeepSeek-V3.2")

# === Experiment ===
N_ISSUES = 30                # SWE-bench issues to sample
MAX_OUTPUT_TOKENS = 1024     # per VLM/call
TEMPERATURE = 0.0            # greedy decoding for reproducibility
TIMEOUT = 180                # seconds per API call (VLM is slow)
RETRY_MAX = 4                # exponential backoff on 429
RETRY_BASE_DELAY = 2.0       # seconds (2→4→8→16)
API_SEED = 42                # seed for reproducible API outputs
ISSUE_DELAY = 3.0            # seconds between issues (rate-limit courtesy)

# === Output ===
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
DATA_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

# === Experience Fragment Schema ===
FRAGMENT_SCHEMA = {
    "source": "image",                    # "text" | "image"
    "observations": ["str"],              # what the model sees
    "causal_hypothesis": "str",           # inferred cause → effect
    "confidence": 0.0,                    # 0.0–1.0
    "missing_info": ["str"],              # what's not visible in the image
}
