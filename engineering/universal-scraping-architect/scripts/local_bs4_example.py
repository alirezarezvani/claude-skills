"""
Universal Scraping Architect: Traditional / Local Scraping Example
==================================================================
Extracts a data table from a static HTML page using Requests and BeautifulSoup,
then validates, cleans, and saves to CSV.

Demonstrates:
  - Safe HTTP fetching with headers, timeouts, and retry logic
  - HTML table parsing with pandas
  - Column name normalisation to snake_case
  - Required field validation before saving
  - Structured error handling at every stage
  - Clean, logged output

Usage:
  pip install -r requirements.txt
  python scripts/local_bs4_example.py
"""

import sys
import time
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

# =============================================================================
# CONFIG — Edit these for your task
# =============================================================================
TARGET_URL = "https://example.com/macroeconomic-indicators/energy-prices"
OUTPUT_FILE = "energy_price_data.csv"
LOG_FILE = "local_scrape_run.log"

# HTTP settings
USER_AGENT = "UniversalScrapingArchitect/1.0 (contact: your@email.com)"
TIMEOUT_SECONDS = 15
MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 2

# Validation
REQUIRED_COLUMNS = ["date", "price_index", "yoy_change"]
TABLE_SELECTOR = {"id": "indicator-data"}     # Edit to match your target table's HTML attributes


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


def safe_get(url: str) -> str:
    """
    Fetches HTML from a URL with polite headers, a timeout, and retry logic.
    Raises on non-2xx status.
    """
    headers = {"User-Agent": USER_AGENT}

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            log(f"Attempt {attempt}/{MAX_RETRIES}: GET {url}")
            response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
            response.raise_for_status()
            log(f"HTTP {response.status_code} — content length: {len(response.text):,} chars.")
            return response.text
        except requests.exceptions.HTTPError as e:
            log(f"HTTP error on attempt {attempt}: {e}", level="ERROR")
        except requests.exceptions.ConnectionError as e:
            log(f"Connection error on attempt {attempt}: {e}", level="ERROR")
        except requests.exceptions.Timeout:
            log(f"Timeout on attempt {attempt} after {TIMEOUT_SECONDS}s.", level="WARNING")
        except requests.exceptions.RequestException as e:
            log(f"Request failed on attempt {attempt}: {e}", level="ERROR")

        if attempt < MAX_RETRIES:
            log(f"Waiting {RETRY_DELAY_SECONDS}s before retry...")
            time.sleep(RETRY_DELAY_SECONDS)

    raise RuntimeError(f"All {MAX_RETRIES} attempts failed for URL: {url}")


def find_table(html: str) -> BeautifulSoup:
    """
    Parses the HTML and returns the target table element.
    Adjust TABLE_SELECTOR to match the table you need.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", TABLE_SELECTOR)
    if not table:
        raise ValueError(
            f"Target table not found. Selector used: {TABLE_SELECTOR}. "
            "Inspect the page source and update TABLE_SELECTOR in CONFIG."
        )
    log("Target table found in HTML.")
    return table


def parse_table(table) -> pd.DataFrame:
    """Converts a BeautifulSoup table element into a pandas DataFrame."""
    df = pd.read_html(str(table))[0]
    log(f"Parsed table: {len(df)} rows, {len(df.columns)} columns.")
    return df


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Normalises all column names to snake_case."""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
        .str.replace(r"[^\w]", "", regex=True)
    )
    log(f"Columns after normalisation: {list(df.columns)}")
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Applies general cleaning rules.
    Extend this function for your task-specific cleaning needs.
    """
    # Strip whitespace from string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    # Drop fully empty rows
    before = len(df)
    df = df.dropna(how="all")
    dropped = before - len(df)
    if dropped:
        log(f"Dropped {dropped} fully empty rows.", level="WARNING")

    return df


def validate(df: pd.DataFrame) -> bool:
    """
    Checks that the DataFrame is non-empty and contains all required columns.
    Returns True if valid, False otherwise.
    """
    if df.empty:
        log("Validation failed: DataFrame is empty.", level="ERROR")
        return False

    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        log(
            f"Validation failed: missing required columns: {missing}. "
            f"Available columns: {list(df.columns)}",
            level="ERROR"
        )
        return False

    log(f"Validation passed. {len(df)} rows, {len(df.columns)} columns.")
    return True


def save_output(df: pd.DataFrame, path: str):
    """Saves the validated DataFrame to CSV."""
    df.to_csv(path, index=False, encoding="utf-8")
    log(f"Output saved to: {path}")


# =============================================================================
# MAIN
# =============================================================================

def main():
    log("=" * 60)
    log("Universal Scraping Architect — Traditional / Local Scraping")
    log("=" * 60)

    # Step 1: Fetch
    try:
        html = safe_get(TARGET_URL)
    except RuntimeError as e:
        log(str(e), level="ERROR")
        sys.exit(1)

    # Step 2: Find table
    try:
        table = find_table(html)
    except ValueError as e:
        log(str(e), level="ERROR")
        sys.exit(1)

    # Step 3: Parse
    try:
        df = parse_table(table)
    except Exception as e:
        log(f"Failed to parse table into DataFrame: {e}", level="ERROR")
        sys.exit(1)

    # Step 4: Clean
    df = clean_column_names(df)
    df = clean_data(df)

    # Step 5: Validate
    if not validate(df):
        sys.exit(1)

    # Step 6: Save
    save_output(df, OUTPUT_FILE)

    # Step 7: Final summary
    log("=" * 60)
    log("EXTRACTION COMPLETE")
    log(f"  Source URL   : {TARGET_URL}")
    log(f"  Output file  : {OUTPUT_FILE}")
    log(f"  Rows saved   : {len(df)}")
    log(f"  Columns      : {list(df.columns)}")
    log(f"  Log file     : {LOG_FILE}")
    log("=" * 60)
    log("Customisable: TARGET_URL, OUTPUT_FILE, TABLE_SELECTOR, REQUIRED_COLUMNS.")


if __name__ == "__main__":
    main()
