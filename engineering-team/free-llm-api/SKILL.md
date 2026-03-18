---
name: "free-llm-api"
description: "Set up and use free or low-cost LLM API endpoints compatible with the OpenAI SDK. Use when the user wants to reduce API costs, access GPT/Claude/DeepSeek/Gemini for free, configure an OpenAI-compatible proxy, set up API key rotation, build a cloud provider fallback pool, manage LLM API keys centrally, or when they mention ChatAnywhere, Groq, Cerebras, OpenRouter, Mistral free tier, free ChatGPT API, llm-mux, one-api, or turning a Claude Pro/GitHub Copilot/Gemini subscription into a local API."
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: engineering
  updated: 2026-03-17
---

# Free & Low-Cost LLM APIs

You are an expert in configuring cost-effective LLM API access. Your goal is to help developers get GPT-4o, DeepSeek, Claude, and other frontier models for free or near-free — using OpenAI-compatible endpoints that drop into any existing codebase with a one-line change.

## Before Starting

Gather this context (ask if not provided):

### 1. Current Setup
- What SDK/library are you using? (openai Python/Node, LangChain, LiteLLM, raw HTTP)
- Which models do you need? (GPT-4o, DeepSeek, Claude, Gemini, etc.)
- Location: inside China or outside? (affects which relay to use)

### 2. Goals
- Zero cost, or willing to pay small amounts?
- Need high rate limits or is 200 req/day sufficient?
- Production or development/research use?

---

## How This Skill Works

### Mode 1: Free Tier Setup
Get free API access with a GitHub account — zero credit card required.

### Mode 2: Provider Rotation Pool
Build a fault-tolerant pool that rotates across free providers on rate limit errors.

### Mode 3: Drop-in Replacement
Swap base URL in existing code — no other changes required.

---

## Free Providers at a Glance

| Provider | Free Tier | Models | Rate Limit | Location |
|----------|-----------|--------|------------|----------|
| **llm-mux** | Unlimited (uses your subscriptions) | Claude Pro, Copilot GPT-5, Gemini, Codex | Subscription quota | Local (`localhost:8317`) |
| **One API** | Self-hosted key manager | Any provider you configure | Your quotas | Local or remote (`localhost:3000`) |
| **ChatAnywhere** | 200 req/day (GitHub login) | GPT-4o-mini, GPT-4o, DeepSeek-v3, Claude, Gemini | 200/day/IP+Key | Global (CN relay available) |
| **Groq** | Free tier | Llama-3.3-70b, Mixtral, Gemma | ~30 RPM | Global |
| **Cerebras** | Free tier | Llama-3.1-8b, 70b | ~30 RPM | Global |
| **Mistral** | Free tier | mistral-small, mistral-7b | ~1 RPM | Global |
| **OpenRouter** | Free models (`:free` suffix) | Llama, Mistral, Gemma variants | Varies | Global |
| **Google AI Studio** | 15 RPM free | Gemini 1.5 Flash, Pro | 15 RPM | Global |

All providers use the OpenAI-compatible `/v1/chat/completions` endpoint.

---

## Setup: llm-mux (Best if You Have Existing Subscriptions)

llm-mux ([github.com/nghyane/llm-mux](https://github.com/nghyane/llm-mux)) turns existing Claude Pro, GitHub Copilot, and Gemini subscriptions into a local OpenAI-compatible API. No API keys — OAuth login only. Runs at `localhost:8317`.

**Supported subscriptions:**
| Provider | Login command | Models unlocked |
|----------|--------------|----------------|
| Claude Pro/Max | `llm-mux login claude` | claude-sonnet-4, claude-opus-4 |
| GitHub Copilot | `llm-mux login copilot` | gpt-4o, gpt-4.1, gpt-5, gpt-5.1, gpt-5.2 |
| Google Gemini | `llm-mux login antigravity` | gemini-2.5-pro, gemini-2.5-flash |
| ChatGPT Plus/Pro | `llm-mux login codex` | gpt-5 series |
| Alibaba Cloud | `llm-mux login qwen` | qwen models |
| AWS/Amazon Q | `llm-mux login kiro` | Amazon Q models |

### Install

```bash
curl -fsSL https://raw.githubusercontent.com/nghyane/llm-mux/main/install.sh | bash
```

### Login and Start

```bash
# Login to one or more providers
llm-mux login claude       # Claude Pro subscription
llm-mux login copilot      # GitHub Copilot subscription
llm-mux login antigravity  # Google Gemini

# Start the gateway (runs on localhost:8317)
llm-mux
```

### Use in Code

```python
from openai import OpenAI

client = OpenAI(
    api_key="unused",                        # llm-mux ignores API key
    base_url="http://localhost:8317/v1",
)

response = client.chat.completions.create(
    model="claude-sonnet-4-20250514",        # or gpt-4o, gemini-2.5-pro, etc.
    messages=[{"role": "user", "content": "Hello"}],
)
```

### Check Available Models

```bash
curl http://localhost:8317/v1/models
```

### Multi-Account Load Balancing

Login multiple accounts — llm-mux auto-rotates and handles quota limits:

```bash
llm-mux login claude    # Account 1
llm-mux login claude    # Account 2 (rotates automatically)
```

### Run as Background Service (macOS)

```bash
# Install as launchd service
llm-mux service install
llm-mux service start

# Check status
llm-mux service status
```

### Config File (`~/.config/llm-mux/config.yaml`)

```yaml
port: 8317
disable-auth: true        # No API key required for local use
request-retry: 3
stream-timeout: 300
```

---

## Setup: One API (Best for Teams / Multi-Provider Management)

One API ([github.com/songquanpeng/one-api](https://github.com/songquanpeng/one-api), 30k+ stars) is a self-hosted LLM API gateway with a full web UI. Add all your provider API keys once, then hand out unified tokens to teammates or apps — with quota limits, usage tracking, and automatic load balancing across channels.

**When to use One API vs llm-mux:**
| | One API | llm-mux |
|-|---------|---------|
| Setup | Web UI + Docker | CLI binary |
| Auth | API key tokens you issue | OAuth subscription |
| Best for | Teams, multi-app, billing control | Personal, subscription-based |
| Web dashboard | Yes | No |
| User management | Yes | No |

### Quick Start (Docker)

```bash
docker run --name one-api -d --restart always \
  -p 3000:3000 \
  -e TZ=Asia/Shanghai \
  -v /data/one-api:/data \
  justsong/one-api
```

Open `http://localhost:3000` — default credentials: `root` / `123456` (change immediately).

### Docker Compose (with MySQL for persistence)

```yaml
version: '3'
services:
  one-api:
    image: justsong/one-api
    ports:
      - "3000:3000"
    environment:
      - SQL_DSN=root:password@tcp(mysql:3306)/oneapi
      - SESSION_SECRET=change_me
      - INITIAL_ROOT_TOKEN=your-root-token
    depends_on:
      - mysql
    restart: always

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: oneapi
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### Configuration

1. **Add channels** (Channels page): Add your API keys for OpenAI, Azure, Claude, Gemini, DeepSeek, etc.
2. **Create tokens** (Tokens page): Generate tokens with optional quota limits and expiry.
3. **Use the token** as your API key — set base URL to your One API instance.

### Use in Code

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-one-api-token",          # Token from One API Tokens page
    base_url="http://localhost:3000/v1",   # Or your remote One API URL
)

# Works with any model you've configured in channels
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
)
```

### Target a Specific Channel

```bash
# Append channel ID to token: TOKEN-CHANNEL_ID
Authorization: Bearer sk-your-token-123
```

### Key Environment Variables

| Variable | Purpose | Example |
|----------|---------|---------|
| `SQL_DSN` | MySQL instead of SQLite | `root:pass@tcp(localhost:3306)/oneapi` |
| `SESSION_SECRET` | Stable session across restarts | `random_string` |
| `INITIAL_ROOT_TOKEN` | Pre-set root token on first start | `sk-my-root-token` |
| `REDIS_CONN_STRING` | Redis for rate limiting | `redis://localhost:6379` |
| `RELAY_PROXY` | Outbound proxy for API calls | `http://proxy:8080` |

### Supported Providers
OpenAI, Azure OpenAI, Anthropic Claude, Google Gemini/PaLM, Baidu Wenxin, Alibaba Qwen, Zhipu ChatGLM, DeepSeek, and more — anything with an OpenAI-compatible endpoint can be added as a custom channel.

---

## Setup: ChatAnywhere (Best Free Option)

ChatAnywhere ([github.com/chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free)) provides free API keys backed by real OpenAI/DeepSeek/Claude accounts.

### 1. Get a Free Key
1. Visit: `https://api.chatanywhere.tech/v1/oauth/free/render`
2. Log in with GitHub
3. Copy your free API key (starts with `sk-`)

### 2. Configure

```bash
# .env
CHATANYWHERE_API_KEY=sk-your-key-here

# Base URLs
# Inside China (lower latency):  https://api.chatanywhere.tech
# Outside China:                  https://api.chatanywhere.org
```

### 3. Use in Code

**Python (openai SDK)**
```python
from openai import OpenAI

client = OpenAI(
    api_key="sk-your-key-here",
    base_url="https://api.chatanywhere.tech/v1",
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
)
print(response.choices[0].message.content)
```

**Environment variable method**
```bash
export OPENAI_API_KEY=sk-your-key-here
export OPENAI_BASE_URL=https://api.chatanywhere.tech/v1
# Existing code using openai.OpenAI() now routes through ChatAnywhere
```

**Node.js**
```js
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.CHATANYWHERE_API_KEY,
  baseURL: "https://api.chatanywhere.tech/v1",
});
```

### Supported Models (Free Tier)
- `gpt-4o-mini`, `gpt-3.5-turbo`, `gpt-4.1-mini` — 200/day
- `gpt-4o`, `gpt-5` — 5/day
- `deepseek-r1`, `deepseek-v3` — 30/day
- `text-embedding-3-small` — 200/day

---

## Setup: Groq (Fastest Free Inference)

```python
from openai import OpenAI

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)
# Use: llama-3.3-70b-versatile, mixtral-8x7b-32768, gemma2-9b-it
```

Get key: `https://console.groq.com/keys`

---

## Setup: OpenRouter (100+ Free Models)

```python
client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)
# Free models end with :free — e.g. "meta-llama/llama-3.3-70b-instruct:free"
```

Get key: `https://openrouter.ai/keys`
Free models list: `https://openrouter.ai/models?q=free`

---

## Provider Rotation Pool (Recommended)

Build a fault-tolerant pool that automatically rotates on 429 rate limit errors:

```python
import os, requests

_CLOUD_POOL = [
    # (base_url, api_key, model)
    ("http://localhost:8317",               "unused",                             "gpt-4o"),             # llm-mux local — falls through if not running
    (os.getenv("ONE_API_BASE","localhost:3000"), os.getenv("ONE_API_KEY",""),     "gpt-4o"),             # one-api self-hosted gateway
    ("https://api.groq.com/openai",        os.getenv("GROQ_API_KEY", ""),        "llama-3.3-70b-versatile"),
    ("https://api.cerebras.ai",             os.getenv("CEREBRAS_API_KEY", ""),    "llama3.1-8b"),
    ("https://api.mistral.ai",              os.getenv("MISTRAL_API_KEY", ""),     "mistral-small-latest"),
    ("https://api.chatanywhere.tech",       os.getenv("CHATANYWHERE_API_KEY",""), "gpt-4o-mini"),
    ("https://openrouter.ai/api",           os.getenv("OPENROUTER_API_KEY", ""),  "meta-llama/llama-3.3-70b-instruct:free"),
]

def llm_call(prompt: str, max_tokens: int = 100, timeout: int = 30) -> str:
    for base_url, api_key, model in _CLOUD_POOL:
        if not api_key:
            continue
        try:
            r = requests.post(
                f"{base_url}/v1/chat/completions",
                headers={"Authorization": f"Bearer {api_key}",
                         "Content-Type": "application/json"},
                json={"model": model,
                      "messages": [{"role": "user", "content": prompt}],
                      "max_tokens": max_tokens,
                      "temperature": 0},
                timeout=timeout,
            )
            if r.status_code == 429:
                continue        # rate limited — try next
            r.raise_for_status()
            return r.json()["choices"][0]["message"]["content"].strip()
        except Exception:
            continue
    raise RuntimeError("All LLM providers failed or rate-limited")
```

---

## LangChain / LiteLLM Integration

**LangChain**
```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=os.getenv("CHATANYWHERE_API_KEY"),
    openai_api_base="https://api.chatanywhere.tech/v1",
)
```

**LiteLLM (universal proxy)**
```python
import litellm

response = litellm.completion(
    model="openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello"}],
    api_key=os.getenv("CHATANYWHERE_API_KEY"),
    api_base="https://api.chatanywhere.tech/v1",
)
```

---

## Rate Limit Strategy

| Situation | Strategy |
|-----------|----------|
| 429 from one provider | Rotate to next in pool immediately |
| All providers 429 | Exponential backoff: 2s, 4s, 8s |
| Daily limit reached | Fall back to local Ollama or next-day reset |
| Need more than 200/day | Use Groq (higher RPM) or buy paid ChatAnywhere key |

```python
import time

def llm_call_with_backoff(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            return llm_call(prompt)
        except RuntimeError:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    raise RuntimeError("All retries exhausted")
```

---

## Proactive Triggers

- **`OPENAI_API_KEY` in code with no `base_url`** → suggest ChatAnywhere or Groq to avoid billing
- **Single provider, no fallback** → suggest rotation pool to prevent downtime
- **Hardcoded API key in source** → flag as security issue, suggest env vars
- **`gpt-4` or `gpt-4-turbo` on a budget** → suggest `gpt-4o-mini` (98% cheaper, similar quality for most tasks)
- **Embedding costs** → suggest `text-embedding-3-small` via ChatAnywhere free tier

---

## Output Artifacts

| When you ask for... | You get... |
|---------------------|------------|
| Quick setup | `.env` template + one-file integration code |
| Rotation pool | Drop-in `llm_call()` function with all free providers |
| LangChain setup | ChatOpenAI config snippet for chosen provider |
| Cost estimate | Comparison of free vs paid tiers for your use case |
| Troubleshooting | Diagnostic checklist for 401/429/timeout errors |

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `401 Unauthorized` | Wrong key or key not activated | Re-generate key at provider dashboard |
| `429 Too Many Requests` | Rate limit hit | Rotate provider or wait for reset |
| `404 Not Found` | Wrong base URL or model name | Check model list for that provider |
| No response / timeout | Network block or wrong endpoint | Try alternate base URL (`chatanywhere.org` vs `.tech`) |
| `model not found` | Model not available on free tier | Check provider's free model list |

---

## Related Skills

| Skill | Use instead when... |
|-------|---------------------|
| `claude-api` | Building production apps with Anthropic's Claude API directly |
| `senior-backend` | Full API integration architecture beyond just LLM calls |
| `env-secrets-manager` | Managing API keys securely across environments |

---

## Reference

→ [references/providers.md](references/providers.md) — full model lists, rate limits, and pricing for each provider
