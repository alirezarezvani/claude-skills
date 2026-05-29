"""
Universal Scraping Architect: Firecrawl Example (Path C — Repeatable Deliverable)
===================================================================================
Extracts clean markdown content from a target URL using the Firecrawl SDK.

Demonstrates:
  - Safe API key loading from environment
  - Token budget tracking before LLM processing
  - Firecrawl quota awareness logging
  - Structured error handling
  - Clean output saving with validation

Usage:
  export FIRECRAWL_API_KEY="fc-YOUR_KEY_HERE"     # Linux/macOS
  $env:FIRECRAWL_API_KEY = "fc-YOUR_KEY_HERE"     # Windows PowerShell
  python scripts/firecrawl_example.py
"""

import os
import sys
from datetime import datetime
from firecrawl import FirecrawlApp

# =============================================================================
# CONFIG — Edit these for your task
# =============================================================================
TARGET_URL = "https://example.com/research-data"
OUTPUT_FILE = "clean_extraction.md"
LOG_FILE = "firecrawl_run.log"

# Firecrawl / Token settings
FIRECRAWL_API_KEY_ENV = "FIRECRAWL_API_KEY"
TOKEN_CONTEXT_LIMIT = 100_000     # Adjust to your model's context window
RESERVED_OUTPUT_TOKENS = 4_000    # Tokens held back for the model's response


# =============================================================================
# HELPERS
# =============================================================================

def log(message: str, level: str = "INFO"):
    """Prints a timestamped log line and appends it to the log file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def check_environment() -> str:
    """Loads the Firecrawl API key from the environment. Fails fast if missing."""
    api_key = os.getenv(FIRECRAWL_API_KEY_ENV)
    if not api_key:
        log(
            f"Missing environment variable: {FIRECRAWL_API_KEY_ENV}. "
            "Set it before running this script.",
            level="ERROR"
        )
        sys.exit(1)
    log("API key loaded successfully from environment.")
    return api_key


def estimate_tokens(text: str) -> int:
    """Rough token estimate based on character count (characters / 4)."""
    return len(text) // 4


def check_token_budget(text: str) -> bool:
    """
    Estimates token usage and warns if over budget.
    Returns True if within budget, False if over.
    """
    estimated = estimate_tokens(text)
    available = TOKEN_CONTEXT_LIMIT - RESERVED_OUTPUT_TOKENS
    log(f"Token estimate: {estimated:,} / {available:,} available tokens.")
    if estimated > available:
        log(
            f"OVER TOKEN BUDGET by {estimated - available:,} tokens. "
            "Consider chunking the output before passing to an LLM.",
            level="WARNING"
        )
        return False
    log("Within token budget.")
    return True


def validate_content(content: str) -> bool:
    """Basic validation — checks the response is non-empty."""
    if not content or not content.strip():
        log("Validation failed: empty content received from Firecrawl.", level="ERROR")
        return False
    log(f"Validation passed. Content length: {len(content):,} characters.")
    return True


def save_output(content: str, path: str):
    """Saves validated content to the output path."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    log(f"Output saved to: {path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    log("=" * 60)
    log("Universal Scraping Architect — Firecrawl Path C")
    log("=" * 60)

    # Step 1: Environment check
    api_key = check_environment()

    # Step 2: Initialise Firecrawl client
    app = FirecrawlApp(api_key=api_key)
    log(f"Firecrawl client initialised. Target: {TARGET_URL}")

    # Step 3: Scrape
    try:
        log("Starting scrape...")
        result = app.scrape_url(TARGET_URL, params={"formats": ["markdown"]})
        markdown_content = result.get("markdown", "")
    except Exception as e:
        log(f"Firecrawl scrape failed: {e}", level="ERROR")
        log(
            "Tip: if this is a quota or auth error, check your FIRECRAWL_API_KEY "
            "and run `firecrawl --status` to inspect account state.",
            level="WARNING"
        )
        sys.exit(1)

    # Step 4: Validate
    if not validate_content(markdown_content):
        sys.exit(1)

    # Step 5: Token budget check
    check_token_budget(markdown_content)

    # Step 6: Save clean output
    save_output(markdown_content, OUTPUT_FILE)

    # Step 7: Final summary
    log("=" * 60)
    log("EXTRACTION COMPLETE")
    log(f"  Source URL  : {TARGET_URL}")
    log(f"  Output file : {OUTPUT_FILE}")
    log(f"  Characters  : {len(markdown_content):,}")
    log(f"  Est. tokens : {estimate_tokens(markdown_content):,}")
    log(f"  Log file    : {LOG_FILE}")
    log("=" * 60)
    log("Customisable: TARGET_URL, OUTPUT_FILE, TOKEN_CONTEXT_LIMIT, formats.")


if __name__ == "__main__":
    main()
