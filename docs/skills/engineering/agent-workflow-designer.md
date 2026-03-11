---
title: "Agent Workflow Designer"
description: "Agent Workflow Designer - Claude Code skill from the Engineering - POWERFUL domain."
---

# Agent Workflow Designer

<div class="page-meta" markdown>
<span class="meta-badge">:material-rocket-launch: Engineering - POWERFUL</span>
<span class="meta-badge">:material-identifier: `agent-workflow-designer`</span>
<span class="meta-badge">:material-github: <a href="https://github.com/alirezarezvani/claude-skills/tree/main/engineering/agent-workflow-designer/SKILL.md">Source</a></span>
</div>

<div class="install-banner" markdown>
<span class="install-label">Install:</span> <code>claude /plugin install engineering-advanced-skills</code>
</div>


**Tier:** POWERFUL  
**Category:** Engineering  
**Domain:** Multi-Agent Systems / AI Orchestration

---

## Overview

Design production-grade multi-agent orchestration systems. Covers five core patterns (sequential pipeline, parallel fan-out/fan-in, hierarchical delegation, event-driven, consensus), platform-specific implementations, handoff protocols, state management, error recovery, context window budgeting, and cost optimization.

---

## Core Capabilities

- Pattern selection guide for any orchestration requirement
- Handoff protocol templates (structured context passing)
- State management patterns for multi-agent workflows
- Error recovery and retry strategies
- Context window budget management
- Cost optimization strategies per platform
- Platform-specific configs: Claude Code Agent Teams, OpenClaw, CrewAI, AutoGen

---

## When to Use

- Building a multi-step AI pipeline that exceeds one agent's context capacity
- Parallelizing research, generation, or analysis tasks for speed
- Creating specialist agents with defined roles and handoff contracts
- Designing fault-tolerant AI workflows for production

---

## Pattern Selection Guide

```
Is the task sequential (each step needs previous output)?
  YES → Sequential Pipeline
  NO  → Can tasks run in parallel?
          YES → Parallel Fan-out/Fan-in
          NO  → Is there a hierarchy of decisions?
                  YES → Hierarchical Delegation
                  NO  → Is it event-triggered?
                          YES → Event-Driven
                          NO  → Need consensus/validation?
                                  YES → Consensus Pattern
```

---

## Pattern 1: Sequential Pipeline

**Use when:** Each step depends on the previous output. Research → Draft → Review → Polish.

```python
# sequential_pipeline.py
from dataclasses import dataclass
from typing import Callable, Any
import anthropic

@dataclass
class PipelineStage:
    name: "str"
    system_prompt: str
    input_key: str      # what to take from state
    output_key: str     # what to write to state
    model: str = "claude-3-5-sonnet-20241022"
    max_tokens: int = 2048

class SequentialPipeline:
    def __init__(self, stages: list[PipelineStage]):
        self.stages = stages
        self.client = anthropic.Anthropic()
    
    def run(self, initial_input: str) -> dict:
        state = {"input": initial_input}
        
        for stage in self.stages:
            print(f"[{stage.name}] Processing...")
            
            stage_input = state.get(stage.input_key, "")
            
            response = self.client.messages.create(
                model=stage.model,
                max_tokens=stage.max_tokens,
                system=stage.system_prompt,
                messages=[{"role": "user", "content": stage_input}],
            )
            
            state[stage.output_key] = response.content[0].text
            state[f"{stage.name}_tokens"] = response.usage.input_tokens + response.usage.output_tokens
            
            print(f"[{stage.name}] Done. Tokens: {state[f'{stage.name}_tokens']}")
        
        return state

# Example: Blog post pipeline
pipeline = SequentialPipeline([
    PipelineStage(
        name="researcher",
        system_prompt="You are a research specialist. Given a topic, produce a structured research brief with: key facts, statistics, expert perspectives, and controversy points.",
        input_key="input",
        output_key="research",
    ),
    PipelineStage(
        name="writer",
        system_prompt="You are a senior content writer. Using the research provided, write a compelling 800-word blog post with a clear hook, 3 main sections, and a strong CTA.",
        input_key="research",
        output_key="draft",
    ),
    PipelineStage(
        name="editor",
        system_prompt="You are a copy editor. Review the draft for: clarity, flow, grammar, and SEO. Return the improved version only, no commentary.",
        input_key="draft",
        output_key="final",
    ),
])
```

---

## Pattern 2: Parallel Fan-out / Fan-in

**Use when:** Independent tasks that can run concurrently. Research 5 competitors simultaneously.

```python
# parallel_fanout.py
import asyncio
import anthropic
from typing import Any

async def run_agent(client, task_name: "str-system-str-user-str-model-str"claude-3-5-sonnet-20241022") -> dict:
    """Single async agent call"""
    loop = asyncio.get_event_loop()
    
    def _call():
        return client.messages.create(
            model=model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
    
    response = await loop.run_in_executor(None, _call)
    return {
        "task": task_name,
        "output": response.content[0].text,
        "tokens": response.usage.input_tokens + response.usage.output_tokens,
    }

async def parallel_research(competitors: list[str], research_type: str) -> dict:
    """Fan-out: research all competitors in parallel. Fan-in: synthesize results."""
    client = anthropic.Anthropic()
    
    # FAN-OUT: spawn parallel agent calls
    tasks = [
        run_agent(
            client,
            task_name=competitor,
            system=f"You are a competitive intelligence analyst. Research {competitor} and provide: pricing, key features, target market, and known weaknesses.",
            user=f"Analyze {competitor} for comparison with our product in the {research_type} market.",
        )
        for competitor in competitors
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    # Handle failures gracefully
    successful = [r for r in results if not isinstance(r, Exception)]
    failed = [r for r in results if isinstance(r, Exception)]
    
    if failed:
        print(f"Warning: {len(failed)} research tasks failed: {failed}")
    
    # FAN-IN: synthesize
    combined_research = "\n\n".join([
        f"## {r['task']}\n{r['output']}" for r in successful
    ])
    
    synthesis = await run_agent(
        client,
        task_name="synthesizer",
        system="You are a strategic analyst. Synthesize competitor research into a concise comparison matrix and strategic recommendations.",
        user=f"Synthesize these competitor analyses:\n\n{combined_research}",
        model="claude-3-5-sonnet-20241022",
    )
    
    return {
        "individual_analyses": successful,
        "synthesis": synthesis["output"],
        "total_tokens": sum(r["tokens"] for r in successful) + synthesis["tokens"],
    }
```

---

## Pattern 3: Hierarchical Delegation

**Use when:** Complex tasks with subtask discovery. Orchestrator breaks down work, delegates to specialists.

```python
# hierarchical_delegation.py
import json
import anthropic

ORCHESTRATOR_SYSTEM = """You are an orchestration agent. Your job is to:
1. Analyze the user's request
2. Break it into subtasks
3. Assign each to the appropriate specialist agent
4. Collect results and synthesize

Available specialists:
- researcher: finds facts, data, and information
- writer: creates content and documents  
- coder: writes and reviews code
- analyst: analyzes data and produces insights

Respond with a JSON plan:
{
  "subtasks": [
    {"id": "1", "agent": "researcher", "task": "...", "depends_on": []},
    {"id": "2", "agent": "writer", "task": "...", "depends_on": ["1"]}
  ]
}"""

SPECIALIST_SYSTEMS = {
    "researcher": "You are a research specialist. Find accurate, relevant information and cite sources when possible.",
    "writer": "You are a professional writer. Create clear, engaging content in the requested format.",
    "coder": "You are a senior software engineer. Write clean, well-commented code with error handling.",
    "analyst": "You are a data analyst. Provide structured analysis with evidence-backed conclusions.",
}

class HierarchicalOrchestrator:
    def __init__(self):
        self.client = anthropic.Anthropic()
    
    def run(self, user_request: str) -> str:
        # 1. Orchestrator creates plan
        plan_response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            system=ORCHESTRATOR_SYSTEM,
            messages=[{"role": "user", "content": user_request}],
        )
        
        plan = json.loads(plan_response.content[0].text)
        results = {}
        
        # 2. Execute subtasks respecting dependencies
        for subtask in self._topological_sort(plan["subtasks"]):
            context = self._build_context(subtask, results)
            specialist = SPECIALIST_SYSTEMS[subtask["agent"]]
            
            result = self.client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=2048,
                system=specialist,
                messages=[{"role": "user", "content": f"{context}\n\nTask: {subtask['task']}"}],
            )
            results[subtask["id"]] = result.content[0].text
        
        # 3. Final synthesis
        all_results = "\n\n".join([f"### {k}\n{v}" for k, v in results.items()])
        synthesis = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2048,
            system="Synthesize the specialist outputs into a coherent final response.",
            messages=[{"role": "user", "content": f"Original request: {user_request}\n\nSpecialist outputs:\n{all_results}"}],
        )
        return synthesis.content[0].text
    
    def _build_context(self, subtask: dict, results: dict) -> str:
        if not subtask.get("depends_on"):
            return ""
        deps = [f"Output from task {dep}:\n{results[dep]}" for dep in subtask["depends_on"] if dep in results]
        return "Previous results:\n" + "\n\n".join(deps) if deps else ""
    
    def _topological_sort(self, subtasks: list) -> list:
        # Simple ordered execution respecting depends_on
        ordered, remaining = [], list(subtasks)
        completed = set()
        while remaining:
            for task in remaining:
                if all(dep in completed for dep in task.get("depends_on", [])):
                    ordered.append(task)
                    completed.add(task["id"])
                    remaining.remove(task)
                    break
        return ordered
```

---

## Handoff Protocol Template

```python
# Standard handoff context format — use between all agents
@dataclass
class AgentHandoff:
    """Structured context passed between agents in a workflow."""
    task_id: str
    workflow_id: str
    step_number: int
    total_steps: int
    
    # What was done
    previous_agent: str
    previous_output: str
    artifacts: dict  # {"filename": "content"} for any files produced
    
    # What to do next
    current_agent: str
    current_task: str
    constraints: list[str]  # hard rules for this step
    
    # Metadata
    context_budget_remaining: int  # tokens left for this agent
    cost_so_far_usd: float
    
    def to_prompt(self) -> str:
        return f"""
# Agent Handoff — Step {self.step_number}/{self.total_steps}

## Your Task
{self.current_task}

## Constraints
{chr(10).join(f'- {c}' for c in self.constraints)}

## Context from Previous Step ({self.previous_agent})
{self.previous_output[:2000]}{"... [truncated]" if len(self.previous_output) > 2000 else ""}

## Context Budget
You have approximately {self.context_budget_remaining} tokens remaining. Be concise.
"""
```

---

## Error Recovery Patterns

```python
import time
from functools import wraps

def with_retry(max_attempts=3, backoff_seconds=2, fallback_model=None):
    """Decorator for agent calls with exponential backoff and model fallback."""
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(max_attempts):
                try:
                    return fn(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if attempt < max_attempts - 1:
                        wait = backoff_seconds * (2 ** attempt)
                        print(f"Attempt {attempt+1} failed: {e}. Retrying in {wait}s...")
                        time.sleep(wait)
                        
                        # Fall back to cheaper/faster model on rate limit
                        if fallback_model and "rate_limit" in str(e).lower():
                            kwargs["model"] = fallback_model
            raise last_error
        return wrapper
    return decorator

@with_retry(max_attempts=3, fallback_model="claude-3-haiku-20240307")
def call_agent(model, system, user):
    ...
```

---

## Context Window Budgeting

```python
# Budget context across a multi-step pipeline
# Rule: never let any step consume more than 60% of remaining budget

CONTEXT_LIMITS = {
    "claude-3-5-sonnet-20241022": 200_000,
    "gpt-4o": 128_000,
}

class ContextBudget:
    def __init__(self, model: str, reserve_pct: float = 0.2):
        total = CONTEXT_LIMITS.get(model, 128_000)
        self.total = total
        self.reserve = int(total * reserve_pct)  # keep 20% as buffer
        self.used = 0
    
    @property
    def remaining(self):
        return self.total - self.reserve - self.used
    
    def allocate(self, step_name: "str-requested-int-int"
        allocated = min(requested, int(self.remaining * 0.6))  # max 60% of remaining
        print(f"[Budget] {step_name}: allocated {allocated:,} tokens (remaining: {self.remaining:,})")
        return allocated
    
    def consume(self, tokens_used: int):
        self.used += tokens_used

def truncate_to_budget(text: str, token_budget: int, chars_per_token: float = 4.0) -> str:
    """Rough truncation — use tiktoken for precision."""
    char_budget = int(token_budget * chars_per_token)
    if len(text) <= char_budget:
        return text
    return text[:char_budget] + "\n\n[... truncated to fit context budget ...]"
```

---

## Cost Optimization Strategies

| Strategy | Savings | Tradeoff |
|---|---|---|
| Use Haiku for routing/classification | 85-90% | Slightly less nuanced judgment |
| Cache repeated system prompts | 50-90% | Requires prompt caching setup |
| Truncate intermediate outputs | 20-40% | May lose detail in handoffs |
| Batch similar tasks | 50% | Latency increases |
| Use Sonnet for most, Opus for final step only | 60-70% | Final quality may improve |
| Short-circuit on confidence threshold | 30-50% | Need confidence scoring |

---

## Common Pitfalls

- **Circular dependencies** — agents calling each other in loops; enforce DAG structure at design time
- **Context bleed** — passing entire previous output to every step; summarize or extract only what's needed
- **No timeout** — a stuck agent blocks the whole pipeline; always set max_tokens and wall-clock timeouts
- **Silent failures** — agent returns plausible but wrong output; add validation steps for critical paths
- **Ignoring cost** — 10 parallel Opus calls is $0.50 per workflow; model selection is a cost decision
- **Over-orchestration** — if a single prompt can do it, it should; only add agents when genuinely needed
