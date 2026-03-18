# Free LLM Provider Reference

## llm-mux (Local Gateway)

**Source:** [github.com/nghyane/llm-mux](https://github.com/nghyane/llm-mux)

**What it is:** A Go binary that turns existing AI subscriptions into a local OpenAI-compatible API server. No API keys — uses OAuth to authenticate with provider accounts you already pay for.

**Install:**
```bash
curl -fsSL https://raw.githubusercontent.com/nghyane/llm-mux/main/install.sh | bash
```

**Base URL:** `http://localhost:8317` (configurable via `LLM_MUX_PORT`)

**Supported providers and models:**

| Provider | Subscription needed | Login command | Key models |
|----------|-------------------|--------------|-----------|
| Claude | Claude Pro/Max | `llm-mux login claude` | claude-sonnet-4-20250514, claude-opus-4-5-20251101 |
| GitHub Copilot | Copilot subscription | `llm-mux login copilot` | gpt-4o, gpt-4.1, gpt-5, gpt-5.1, gpt-5.2 |
| Google Gemini | Google One AI Premium or free | `llm-mux login antigravity` | gemini-2.5-pro, gemini-2.5-flash |
| OpenAI Codex | ChatGPT Plus/Pro | `llm-mux login codex` | gpt-5 series |
| Qwen | Alibaba Cloud account | `llm-mux login qwen` | qwen models |
| Kiro | AWS/Amazon Q Developer | `llm-mux login kiro` | Amazon Q models |
| Cline | Cline subscription | `llm-mux login cline` | Cline models |

**Key features:**
- Multi-account load balancing — login multiple accounts, auto-rotates
- Auto-retry on quota limits across accounts
- Anthropic + Gemini + Ollama compatible endpoints (not just OpenAI)
- Run as a background service (`llm-mux service install`)
- Management API for usage stats

**Config file:** `~/.config/llm-mux/config.yaml`
**Token storage:** `~/.config/llm-mux/auth/`

---

## ChatAnywhere

**Source:** [github.com/chatanywhere/GPT_API_free](https://github.com/chatanywhere/GPT_API_free) (36k+ stars)

**Get key:** `https://api.chatanywhere.tech/v1/oauth/free/render` (GitHub login required)

**Base URLs:**
- `https://api.chatanywhere.tech` — China relay (lower latency inside CN)
- `https://api.chatanywhere.org` — Global endpoint

**Free tier limits:** 200 req/day per IP+Key combination

**Free models:**
| Model | Daily Limit |
|-------|------------|
| gpt-4o-mini | 200/day |
| gpt-3.5-turbo | 200/day |
| gpt-4.1-mini | 200/day |
| gpt-4.1-nano | 200/day |
| gpt-5-mini | 200/day |
| gpt-4o | 5/day |
| gpt-5 | 5/day |
| gpt-5.1 | 5/day |
| deepseek-r1 | 30/day |
| deepseek-v3 | 30/day |
| text-embedding-3-small | 200/day |
| text-embedding-3-large | 200/day |

**Notes:** Free key requires personal/educational/non-commercial use only. No commercial use.

---

## Groq

**Get key:** `https://console.groq.com/keys`

**Base URL:** `https://api.groq.com/openai/v1`

**Free tier:** Generous free tier, no credit card required

**Models (free):**
| Model | Context | Speed |
|-------|---------|-------|
| llama-3.3-70b-versatile | 128k | Very fast |
| llama-3.1-8b-instant | 128k | Fastest |
| mixtral-8x7b-32768 | 32k | Fast |
| gemma2-9b-it | 8k | Fast |
| deepseek-r1-distill-llama-70b | 128k | Fast |

**Rate limits (free tier):**
- 30 RPM (requests per minute)
- 6,000 TPM (tokens per minute) for large models
- 14,400 RPD (requests per day)

---

## Cerebras

**Get key:** `https://cloud.cerebras.ai/`

**Base URL:** `https://api.cerebras.ai/v1`

**Free tier:** Free with account

**Models (free):**
| Model | Notes |
|-------|-------|
| llama3.1-8b | Very fast inference |
| llama3.1-70b | Fast inference |
| llama-3.3-70b | Latest Llama |

**Advantage:** World's fastest inference (wafer-scale chip) — great for high-volume low-latency tasks.

---

## Mistral AI

**Get key:** `https://console.mistral.ai/api-keys/`

**Base URL:** `https://api.mistral.ai/v1`

**Free tier:** `mistral-small-latest` and open-weight models at 1 RPM free

**Models (free/open-weight):**
| Model | Notes |
|-------|-------|
| mistral-small-latest | 1 RPM free |
| open-mistral-7b | Free |
| open-mixtral-8x7b | Free |
| open-mistral-nemo | Free |

---

## OpenRouter

**Get key:** `https://openrouter.ai/keys`

**Base URL:** `https://openrouter.ai/api/v1`

**Free models:** 100+ models available for free (`:free` suffix)

**Best free models:**
| Model | Context |
|-------|---------|
| meta-llama/llama-3.3-70b-instruct:free | 128k |
| google/gemma-3-27b-it:free | 8k |
| mistralai/mistral-7b-instruct:free | 32k |
| deepseek/deepseek-r1:free | 64k |
| microsoft/phi-3-medium-128k-instruct:free | 128k |

**Notes:** Free models may have higher latency. Rate limits vary by model.

---

## Google AI Studio (Gemini)

**Get key:** `https://aistudio.google.com/app/apikey`

**Base URL:** `https://generativelanguage.googleapis.com/v1beta/openai/` (OpenAI-compatible)

**Free tier:**
| Model | Free RPM | Free RPD |
|-------|---------|---------|
| gemini-1.5-flash | 15 | 1,500 |
| gemini-1.5-pro | 2 | 50 |
| gemini-2.0-flash | 15 | 1,500 |

```python
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
```

---

## Cohere

**Get key:** `https://dashboard.cohere.com/api-keys`

**Base URL:** `https://api.cohere.ai/compatibility/v1` (OpenAI-compatible)

**Free tier:** Trial key, 20 RPM

**Best free model:** `command-r` — great for RAG and tool use

---

## Quick Comparison

| Provider | Best for | Free limit | Signup friction |
|----------|---------|-----------|----------------|
| ChatAnywhere | GPT-4o access, CN users | 200/day | GitHub login |
| Groq | Speed, Llama models | 14,400/day | Email |
| Cerebras | Ultra-fast inference | Generous | Email |
| OpenRouter | Model variety | 100+ free models | Email |
| Google AI Studio | Gemini models | 1,500/day | Google account |
| Mistral | European models | Low (1 RPM) | Email |
