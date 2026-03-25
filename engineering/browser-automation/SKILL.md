---
name: "browser-automation"
description: "Use when the user asks to automate browser tasks, scrape websites, fill forms, capture screenshots, extract structured data from web pages, or build web automation workflows. NOT for testing — use playwright-pro for that."
---

# Browser Automation - POWERFUL

## Overview

The Browser Automation skill provides comprehensive tools and knowledge for building production-grade web automation workflows using Playwright. This skill covers data extraction, form filling, screenshot capture, session management, and anti-detection patterns for reliable browser automation at scale.

**When to use this skill:**
- Scraping structured data from websites (tables, listings, search results)
- Automating multi-step browser workflows (login, fill forms, download files)
- Capturing screenshots or PDFs of web pages
- Extracting data from SPAs and JavaScript-heavy sites
- Building repeatable browser-based data pipelines

**When NOT to use this skill:**
- Writing browser tests or E2E test suites — use **playwright-pro** instead
- Testing API endpoints — use **api-test-suite-builder** instead
- Load testing or performance benchmarking — use **performance-profiler** instead

**Why Playwright over Selenium or Puppeteer:**
- **Auto-wait built in** — no explicit `sleep()` or `waitForElement()` needed for most actions
- **Multi-browser from one API** — Chromium, Firefox, WebKit with zero config changes
- **Network interception** — block ads, mock responses, capture API calls natively
- **Browser contexts** — isolated sessions without spinning up new browser instances
- **Codegen** — `playwright codegen` records your actions and generates scripts
- **Async-first** — Python async/await for high-throughput scraping

## Core Competencies

### 1. Web Scraping Patterns

#### DOM Extraction with CSS Selectors
CSS selectors are the primary tool for element targeting. Prefer them over XPath for readability and performance.

**Selector priority (most to least reliable):**
1. `data-testid`, `data-id`, or custom data attributes — stable across redesigns
2. `#id` selectors — unique but may change between deploys
3. Semantic selectors: `article`, `nav`, `main`, `section` — resilient to CSS changes
4. Class-based: `.product-card`, `.price` — brittle if classes are generated (e.g., CSS modules)
5. Positional: `nth-child()`, `nth-of-type()` — last resort, breaks on layout changes

**Compound selectors for precision:**
```python
# Product cards within a specific container
page.query_selector_all("div.search-results > article.product-card")

# Price inside a product card (scoped)
card.query_selector("span[data-field='price']")

# Links with specific text content
page.locator("a", has_text="Next Page")
```

#### XPath for Complex Traversal
Use XPath only when CSS cannot express the relationship:
```python
# Find element by text content (XPath strength)
page.locator("//td[contains(text(), 'Total')]/following-sibling::td[1]")

# Navigate up the DOM tree
page.locator("//span[@class='price']/ancestor::div[@class='product']")
```

#### Pagination Patterns
- **Next-button pagination**: Click "Next" until disabled or absent
- **URL-based pagination**: Increment `?page=N` or `&offset=N` in URL
- **Infinite scroll**: Scroll to bottom, wait for new content, repeat until no change
- **Load-more button**: Click button, wait for DOM mutation, repeat

#### Infinite Scroll Handling
```python
async def scroll_to_bottom(page, max_scrolls=50, pause_ms=1500):
    previous_height = 0
    for i in range(max_scrolls):
        current_height = await page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            break
        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        await page.wait_for_timeout(pause_ms)
        previous_height = current_height
    return i + 1  # number of scrolls performed
```

### 2. Form Filling & Multi-Step Workflows

#### Login Flows
```python
async def login(page, url, username, password):
    await page.goto(url)
    await page.fill("input[name='username']", username)
    await page.fill("input[name='password']", password)
    await page.click("button[type='submit']")
    # Wait for navigation to complete (post-login redirect)
    await page.wait_for_url("**/dashboard**")
```

#### Multi-Page Forms
Break multi-step forms into discrete functions per step. Each function:
1. Fills the fields for that step
2. Clicks the "Next" or "Continue" button
3. Waits for the next step to load (URL change or DOM element)

```python
async def fill_step_1(page, data):
    await page.fill("#first-name", data["first_name"])
    await page.fill("#last-name", data["last_name"])
    await page.select_option("#country", data["country"])
    await page.click("button:has-text('Continue')")
    await page.wait_for_selector("#step-2-form")

async def fill_step_2(page, data):
    await page.fill("#address", data["address"])
    await page.fill("#city", data["city"])
    await page.click("button:has-text('Continue')")
    await page.wait_for_selector("#step-3-form")
```

#### File Uploads
```python
# Single file
await page.set_input_files("input[type='file']", "/path/to/file.pdf")

# Multiple files
await page.set_input_files("input[type='file']", [
    "/path/to/file1.pdf",
    "/path/to/file2.pdf"
])

# Drag-and-drop upload zones (no visible input element)
async with page.expect_file_chooser() as fc_info:
    await page.click("div.upload-zone")
file_chooser = await fc_info.value
await file_chooser.set_files("/path/to/file.pdf")
```

#### Dropdown and Select Handling
```python
# Native <select> element
await page.select_option("#country", value="US")
await page.select_option("#country", label="United States")

# Custom dropdown (div-based)
await page.click("div.dropdown-trigger")
await page.click("div.dropdown-option:has-text('United States')")
```

### 3. Screenshot & PDF Capture

#### Screenshot Strategies
```python
# Full page (scrolls automatically)
await page.screenshot(path="full-page.png", full_page=True)

# Viewport only (what's visible)
await page.screenshot(path="viewport.png")

# Specific element
element = page.locator("div.chart-container")
await element.screenshot(path="chart.png")

# With custom viewport for consistency
context = await browser.new_context(viewport={"width": 1920, "height": 1080})
```

#### PDF Generation
```python
# Only works in Chromium
await page.pdf(
    path="output.pdf",
    format="A4",
    margin={"top": "1cm", "right": "1cm", "bottom": "1cm", "left": "1cm"},
    print_background=True
)
```

#### Visual Regression Baselines
Take screenshots at known states and compare pixel-by-pixel. Store baselines in version control. Use naming conventions: `{page}_{viewport}_{state}.png`.

### 4. Structured Data Extraction

#### Tables to JSON
```python
async def extract_table(page, selector):
    headers = await page.eval_on_selector_all(
        f"{selector} thead th",
        "elements => elements.map(e => e.textContent.trim())"
    )
    rows = await page.eval_on_selector_all(
        f"{selector} tbody tr",
        """rows => rows.map(row => {
            return Array.from(row.querySelectorAll('td'))
                .map(cell => cell.textContent.trim())
        })"""
    )
    return [dict(zip(headers, row)) for row in rows]
```

#### Listings to Arrays
```python
async def extract_listings(page, container_sel, field_map):
    """
    field_map example: {"title": "h3.title", "price": "span.price", "url": "a::attr(href)"}
    """
    items = []
    cards = await page.query_selector_all(container_sel)
    for card in cards:
        item = {}
        for field, sel in field_map.items():
            if "::attr(" in sel:
                attr_sel, attr_name = sel.split("::attr(")
                attr_name = attr_name.rstrip(")")
                el = await card.query_selector(attr_sel)
                item[field] = await el.get_attribute(attr_name) if el else None
            else:
                el = await card.query_selector(sel)
                item[field] = (await el.text_content()).strip() if el else None
        items.append(item)
    return items
```

#### Nested Data Extraction
For threaded content (comments with replies), use recursive extraction:
```python
async def extract_comments(page, parent_selector):
    comments = []
    elements = await page.query_selector_all(f"{parent_selector} > .comment")
    for el in elements:
        text = await (await el.query_selector(".comment-body")).text_content()
        author = await (await el.query_selector(".author")).text_content()
        replies = await extract_comments(el, ".replies")
        comments.append({
            "author": author.strip(),
            "text": text.strip(),
            "replies": replies
        })
    return comments
```

### 5. Cookie & Session Management

#### Save and Restore Sessions
```python
import json

# Save cookies after login
cookies = await context.cookies()
with open("session.json", "w") as f:
    json.dump(cookies, f)

# Restore session in new context
with open("session.json", "r") as f:
    cookies = json.load(f)
context = await browser.new_context()
await context.add_cookies(cookies)
```

#### Storage State (Cookies + Local Storage)
```python
# Save full state (cookies + localStorage + sessionStorage)
await context.storage_state(path="state.json")

# Restore full state
context = await browser.new_context(storage_state="state.json")
```

**Best practice:** Save state after login, reuse across scraping sessions. Check session validity before starting a long job — make a lightweight request to a protected page and verify you are not redirected to login.

### 6. Anti-Detection Patterns

Modern websites detect automation through multiple vectors. Address all of them:

#### User Agent Rotation
Never use the default Playwright user agent. Rotate through real browser user agents:
```python
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]
```

#### Viewport and Screen Size
Set realistic viewport dimensions. The default 800x600 is a red flag:
```python
context = await browser.new_context(
    viewport={"width": 1920, "height": 1080},
    screen={"width": 1920, "height": 1080},
    user_agent=random.choice(USER_AGENTS),
)
```

#### WebDriver Flag Removal
Playwright sets `navigator.webdriver = true`. Remove it:
```python
await page.add_init_script("""
    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
""")
```

#### Request Throttling
Add human-like delays between actions:
```python
import random

async def human_delay(min_ms=500, max_ms=2000):
    delay = random.randint(min_ms, max_ms)
    await page.wait_for_timeout(delay)
```

#### Proxy Support
```python
browser = await playwright.chromium.launch(
    proxy={"server": "http://proxy.example.com:8080"}
)
# Or per-context:
context = await browser.new_context(
    proxy={"server": "http://proxy.example.com:8080",
           "username": "user", "password": "pass"}
)
```

### 7. Dynamic Content Handling

#### SPA Rendering
SPAs render content client-side. Wait for the actual content, not the page load:
```python
await page.goto(url)
# Wait for the data to render, not just the shell
await page.wait_for_selector("div.product-list article", state="attached")
```

#### AJAX / Fetch Waiting
Intercept and wait for specific API calls:
```python
async with page.expect_response("**/api/products*") as response_info:
    await page.click("button.load-more")
response = await response_info.value
data = await response.json()  # You can use the API data directly
```

#### Shadow DOM Traversal
```python
# Playwright pierces open Shadow DOM automatically with >>
await page.locator("custom-element >> .inner-class").click()
```

#### Lazy-Loaded Images
Scroll elements into view to trigger lazy loading:
```python
images = await page.query_selector_all("img[data-src]")
for img in images:
    await img.scroll_into_view_if_needed()
    await page.wait_for_timeout(200)
```

### 8. Error Handling & Retry Logic

#### Retry Decorator Pattern
```python
import asyncio

async def with_retry(coro_factory, max_retries=3, backoff_base=2):
    for attempt in range(max_retries):
        try:
            return await coro_factory()
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            wait = backoff_base ** attempt
            print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait}s...")
            await asyncio.sleep(wait)
```

#### Handling Common Failures
```python
from playwright.async_api import TimeoutError as PlaywrightTimeout

try:
    await page.click("button.submit", timeout=5000)
except PlaywrightTimeout:
    # Element did not appear — page structure may have changed
    # Try fallback selector
    await page.click("[type='submit']", timeout=5000)
except Exception as e:
    # Network error, browser crash, etc.
    await page.screenshot(path="error-state.png")
    raise
```

#### Rate Limit Detection
```python
async def check_rate_limit(response):
    if response.status == 429:
        retry_after = response.headers.get("retry-after", "60")
        wait_seconds = int(retry_after)
        print(f"Rate limited. Waiting {wait_seconds}s...")
        await asyncio.sleep(wait_seconds)
        return True
    return False
```

## Workflows

### Workflow 1: Single-Page Data Extraction

**Scenario:** Extract product data from a single page with JavaScript-rendered content.

**Steps:**
1. Launch browser in headed mode during development (`headless=False`), switch to headless for production
2. Navigate to URL and wait for content selector
3. Extract data using `query_selector_all` with field mapping
4. Validate extracted data (check for nulls, expected types)
5. Output as JSON

```python
async def extract_single_page(url, selectors):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1920, "height": 1080},
            user_agent="Mozilla/5.0 ..."
        )
        page = await context.new_page()
        await page.goto(url, wait_until="networkidle")
        data = await extract_listings(page, selectors["container"], selectors["fields"])
        await browser.close()
    return data
```

### Workflow 2: Multi-Page Scraping with Pagination

**Scenario:** Scrape search results across 50+ pages.

**Steps:**
1. Launch browser with anti-detection settings
2. Navigate to first page
3. Extract data from current page
4. Check if "Next" button exists and is enabled
5. Click next, wait for new content to load (not just navigation)
6. Repeat until no next page or max pages reached
7. Deduplicate results by unique key
8. Write output incrementally (don't hold everything in memory)

```python
async def scrape_paginated(base_url, selectors, max_pages=100):
    all_data = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await (await browser.new_context()).new_page()
        await page.goto(base_url)

        for page_num in range(max_pages):
            items = await extract_listings(page, selectors["container"], selectors["fields"])
            all_data.extend(items)

            next_btn = page.locator(selectors["next_button"])
            if await next_btn.count() == 0 or await next_btn.is_disabled():
                break

            await next_btn.click()
            await page.wait_for_selector(selectors["container"])
            await human_delay(800, 2000)

        await browser.close()
    return all_data
```

### Workflow 3: Authenticated Workflow Automation

**Scenario:** Log into a portal, navigate a multi-step form, download a report.

**Steps:**
1. Check for existing session state file
2. If no session, perform login and save state
3. Navigate to target page using saved session
4. Fill multi-step form with provided data
5. Wait for download to trigger
6. Save downloaded file to target directory

```python
async def authenticated_workflow(credentials, form_data, download_dir):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        state_file = "session_state.json"

        # Restore or create session
        if os.path.exists(state_file):
            context = await browser.new_context(storage_state=state_file)
        else:
            context = await browser.new_context()
            page = await context.new_page()
            await login(page, credentials["url"], credentials["user"], credentials["pass"])
            await context.storage_state(path=state_file)

        page = await context.new_page()
        await page.goto(form_data["target_url"])

        # Fill form steps
        for step_fn in [fill_step_1, fill_step_2]:
            await step_fn(page, form_data)

        # Handle download
        async with page.expect_download() as dl_info:
            await page.click("button:has-text('Download Report')")
        download = await dl_info.value
        await download.save_as(os.path.join(download_dir, download.suggested_filename))

        await browser.close()
```

## Tools Reference

| Script | Purpose | Key Flags | Output |
|--------|---------|-----------|--------|
| `scraping_toolkit.py` | Generate Playwright scraping script skeleton | `--url`, `--selectors`, `--paginate`, `--output` | Python script or JSON config |
| `form_automation_builder.py` | Generate form-fill automation script from field spec | `--fields`, `--url`, `--output` | Python automation script |
| `anti_detection_checker.py` | Audit a Playwright script for detection vectors | `--file`, `--verbose` | Risk report with score |

All scripts are stdlib-only. Run `python3 <script> --help` for full usage.

## Anti-Patterns

### Hardcoded Waits
**Bad:** `await page.wait_for_timeout(5000)` before every action.
**Good:** Use `wait_for_selector`, `wait_for_url`, `expect_response`, or `wait_for_load_state`. Hardcoded waits are flaky and slow.

### No Error Recovery
**Bad:** Linear script that crashes on first failure.
**Good:** Wrap each page interaction in try/except. Take error-state screenshots. Implement retry with exponential backoff.

### Ignoring robots.txt
**Bad:** Scraping without checking robots.txt directives.
**Good:** Fetch and parse robots.txt before scraping. Respect `Crawl-delay`. Skip disallowed paths. Add your bot name to User-Agent if running at scale.

### Storing Credentials in Scripts
**Bad:** Hardcoding usernames and passwords in Python files.
**Good:** Use environment variables, `.env` files (gitignored), or a secrets manager. Pass credentials via CLI arguments.

### No Rate Limiting
**Bad:** Hammering a site with 100 requests/second.
**Good:** Add random delays between requests (1-3s for polite scraping). Monitor for 429 responses. Implement exponential backoff.

### Selector Fragility
**Bad:** Relying on auto-generated class names (`.css-1a2b3c`) or deep nesting (`div > div > div > span:nth-child(3)`).
**Good:** Use data attributes, semantic HTML, or text-based locators. Test selectors in browser DevTools first.

### Not Cleaning Up Browser Instances
**Bad:** Launching browsers without closing them, leading to resource leaks.
**Good:** Always use `try/finally` or async context managers to ensure `browser.close()` is called.

### Running Headed in Production
**Bad:** Using `headless=False` in production/CI.
**Good:** Develop with headed mode for debugging, deploy with `headless=True`. Use environment variable to toggle: `headless = os.environ.get("HEADLESS", "true") == "true"`.

## Cross-References

- **playwright-pro** — Browser testing skill. Use for E2E tests, test assertions, test fixtures. Browser Automation is for data extraction and workflow automation, not testing.
- **api-test-suite-builder** — When the website has a public API, hit the API directly instead of scraping the rendered page. Faster, more reliable, less detectable.
- **performance-profiler** — If your automation scripts are slow, profile the bottlenecks before adding concurrency.
- **env-secrets-manager** — For securely managing credentials used in authenticated automation workflows.
