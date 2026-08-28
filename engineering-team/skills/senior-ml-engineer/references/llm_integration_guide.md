# LLM Integration Guide

Production patterns for integrating Large Language Models into applications.

---

## Table of Contents

- [API Integration Patterns](#api-integration-patterns)
- [Prompt Engineering](#prompt-engineering)
- [Token Optimization](#token-optimization)
- [Cost Management](#cost-management)
- [Error Handling](#error-handling)

---

## API Integration Patterns

### Provider Abstraction Layer

```python
from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    def complete(self, prompt: str, **kwargs) -> str:
        pass

    @abstractmethod
    def chat(self, messages: List[Dict], **kwargs) -> str:
        pass

class OpenAIProvider(LLMProvider):
    # No default model: a hardcoded default is the thing that goes stale.
    # Pass the model your deployment is pinned to, from config.
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def complete(self, prompt: str, **kwargs) -> str:
        response = self.client.completions.create(
            model=self.model,
            prompt=prompt,
            **kwargs
        )
        return response.choices[0].text

class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = "claude-opus-5"):
        self.client = Anthropic(api_key=api_key)
        self.model = model

    def chat(self, messages: List[Dict], **kwargs) -> str:
        response = self.client.messages.create(
            model=self.model,
            messages=messages,
            **kwargs
        )
        return response.content[0].text
```

### Retry and Fallback Strategy

```python
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10)
)
def call_llm_with_retry(provider: LLMProvider, prompt: str) -> str:
    """Call LLM with exponential backoff retry."""
    return provider.complete(prompt)

def call_with_fallback(
    primary: LLMProvider,
    fallback: LLMProvider,
    prompt: str
) -> str:
    """Try primary provider, fall back on failure."""
    try:
        return call_llm_with_retry(primary, prompt)
    except Exception as e:
        logger.warning(f"Primary provider failed: {e}, using fallback")
        return call_llm_with_retry(fallback, prompt)
```

---

## Prompt Engineering

### Prompt Templates

| Pattern | Use Case | Structure |
|---------|----------|-----------|
| Zero-shot | Simple tasks | Task description + input |
| Few-shot | Complex tasks | Examples + task + input |
| Chain-of-thought | Reasoning | "Think step by step" + task |
| Role-based | Specialized output | System role + task |

### Few-Shot Template

```python
FEW_SHOT_TEMPLATE = """
You are a sentiment classifier. Classify the sentiment as positive, negative, or neutral.

Examples:
Input: "This product is amazing, I love it!"
Output: positive

Input: "Terrible experience, waste of money."
Output: negative

Input: "The product arrived on time."
Output: neutral

Now classify:
Input: "{user_input}"
Output:"""

def classify_sentiment(text: str, provider: LLMProvider) -> str:
    prompt = FEW_SHOT_TEMPLATE.format(user_input=text)
    response = provider.complete(prompt, max_tokens=10, temperature=0)
    return response.strip().lower()
```

### System Prompts for Consistency

```python
SYSTEM_PROMPT = """You are a helpful assistant that answers questions about our product.

Guidelines:
- Be concise and direct
- Use bullet points for lists
- If unsure, say "I don't have that information"
- Never make up information
- Keep responses under 200 words

Product context:
{product_context}
"""

def create_chat_messages(user_query: str, context: str) -> List[Dict]:
    return [
        {"role": "system", "content": SYSTEM_PROMPT.format(product_context=context)},
        {"role": "user", "content": user_query}
    ]
```

---

## Token Optimization

### Token Counting

```python
import tiktoken

def count_tokens(text: str, encoding_name: str = "cl100k_base") -> int:
    """Count tokens for a given text.

    Takes an encoding name rather than a model name: encodings change far more
    slowly than model IDs, and tiktoken.encoding_for_model() raises KeyError on
    any model it has not shipped a mapping for yet.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    return len(encoding.encode(text))

def truncate_to_token_limit(text: str, max_tokens: int, encoding_name: str = "cl100k_base") -> str:
    """Truncate text to fit within token limit."""
    encoding = tiktoken.get_encoding(encoding_name)
    tokens = encoding.encode(text)

    if len(tokens) <= max_tokens:
        return text

    return encoding.decode(tokens[:max_tokens])
```

### Context Window Management

Query the model's advertised context window at runtime rather than table it
here; every fixed number in this position has gone stale within a year.

The rule that does not change: reserve headroom for the response. Budget
roughly 75-90% of the window for input and leave the remainder for output,
then cap output explicitly with `max_tokens` so a runaway generation cannot
overflow the window or the bill.

### Chunking Strategy

```python
def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
    """Split text into overlapping chunks."""
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap

    return chunks
```

---

## Cost Management

### Cost Calculation

Prices move several times a year, so this guide does not carry a rate table.
Pull the current per-million-token input and output prices from your
provider's pricing page and inject them as configuration.

### Cost Tracking

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMUsage:
    input_tokens: int
    output_tokens: int
    model: str
    cost: float

def calculate_cost(
    input_tokens: int,
    output_tokens: int,
    input_price_per_mtok: float,
    output_price_per_mtok: float,
) -> float:
    """Calculate cost from caller-supplied rates (USD per million tokens).

    Rates are parameters, not constants. A hardcoded price table is wrong
    within a year and silently produces a confidently incorrect business case.
    Load these from config so they can be updated without a code change.
    """
    input_cost = (input_tokens / 1_000_000) * input_price_per_mtok
    output_cost = (output_tokens / 1_000_000) * output_price_per_mtok

    return input_cost + output_cost
```

### Cost Optimization Strategies

1. **Use smaller models for simple tasks** - small tier for classification, large tier for reasoning
2. **Cache common responses** - Store results for repeated queries
3. **Batch requests** - Combine multiple items in single prompt
4. **Truncate context** - Only include relevant information
5. **Set max_tokens limit** - Prevent runaway responses

---

## Error Handling

### Common Error Types

| Error | Cause | Handling |
|-------|-------|----------|
| RateLimitError | Too many requests | Exponential backoff |
| InvalidRequestError | Bad input | Validate before sending |
| AuthenticationError | Invalid API key | Check credentials |
| ServiceUnavailable | Provider down | Fallback to alternative |
| ContextLengthExceeded | Input too long | Truncate or chunk |

### Error Handling Pattern

```python
from openai import RateLimitError, APIError

def safe_llm_call(provider: LLMProvider, prompt: str, max_retries: int = 3) -> str:
    """Safely call LLM with comprehensive error handling."""
    for attempt in range(max_retries):
        try:
            return provider.complete(prompt)

        except RateLimitError:
            wait_time = 2 ** attempt
            logger.warning(f"Rate limited, waiting {wait_time}s")
            time.sleep(wait_time)

        except APIError as e:
            if e.status_code >= 500:
                logger.warning(f"Server error: {e}, retrying...")
                time.sleep(1)
            else:
                raise

    raise Exception(f"Failed after {max_retries} attempts")
```

### Response Validation

```python
import json
from pydantic import BaseModel, ValidationError

class StructuredResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]

def parse_structured_response(response: str) -> StructuredResponse:
    """Parse and validate LLM JSON response."""
    try:
        data = json.loads(response)
        return StructuredResponse(**data)
    except json.JSONDecodeError:
        raise ValueError("Response is not valid JSON")
    except ValidationError as e:
        raise ValueError(f"Response validation failed: {e}")
```
