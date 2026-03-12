# Skill Evaluation Pipeline

Automated quality evaluation for skills using [promptfoo](https://promptfoo.dev).

## Quick Start

```bash
# Run a single skill eval
npx promptfoo@latest eval -c eval/skills/copywriting.yaml

# View results in browser
npx promptfoo@latest view

# Run all pilot skill evals
for config in eval/skills/*.yaml; do
  npx promptfoo@latest eval -c "$config" --no-cache
done
```

## Requirements

- Node.js 18+
- `ANTHROPIC_API_KEY` environment variable set
- No additional dependencies (promptfoo runs via npx)

## How It Works

Each skill has an eval config in `eval/skills/<skill-name>.yaml` that:

1. Loads the skill's `SKILL.md` content as context
2. Sends realistic task prompts to an LLM with the skill loaded
3. Evaluates outputs against quality assertions (LLM rubrics + programmatic checks)
4. Reports pass/fail per assertion

### CI/CD Integration

The GitHub Action (`.github/workflows/skill-eval.yml`) runs automatically when:
- A PR to `dev` changes any `SKILL.md` file
- The changed skill has an eval config in `eval/skills/`
- Results are posted as PR comments

Currently **non-blocking** — evals are informational, not gates.

## Adding Evals for a New Skill

### Option 1: Auto-generate

```bash
python eval/scripts/generate-eval-config.py marketing-skill/my-new-skill
```

This creates a boilerplate config with default prompts and assertions. **Always customize** the generated config with domain-specific test cases.

### Option 2: Manual

Copy an existing config and modify:

```bash
cp eval/skills/copywriting.yaml eval/skills/my-skill.yaml
```

### Eval Config Structure

```yaml
description: "What this eval tests"

prompts:
  - |
    You are an expert AI assistant with this skill:
    ---BEGIN SKILL---
    {{skill_content}}
    ---END SKILL---
    Task: {{task}}

providers:
  - id: anthropic:messages:claude-sonnet-4-6
    config:
      max_tokens: 4096

tests:
  - vars:
      skill_content: file://../../path/to/SKILL.md
      task: "A realistic user request"
    assert:
      - type: llm-rubric
        value: "What good output looks like"
      - type: javascript
        value: "output.length > 200"
```

### Assertion Types

| Type | Use For | Example |
|------|---------|---------|
| `llm-rubric` | Qualitative checks (expertise, relevance) | `"Response includes actionable next steps"` |
| `contains` | Required terms | `"React"` |
| `javascript` | Programmatic checks | `"output.length > 500"` |
| `similar` | Semantic similarity | Compare against reference output |

## Reading Results

```bash
# Terminal output (after eval)
npx promptfoo@latest eval -c eval/skills/copywriting.yaml

# Web UI (interactive)
npx promptfoo@latest view

# JSON output (for scripting)
npx promptfoo@latest eval -c eval/skills/copywriting.yaml --output results.json
```

## File Structure

```
eval/
├── promptfooconfig.yaml      # Master config (reference)
├── skills/                   # Per-skill eval configs
│   ├── copywriting.yaml      # ← 10 pilot skills
│   ├── cto-advisor.yaml
│   └── ...
├── assertions/
│   └── skill-quality.js      # Reusable assertion helpers
├── scripts/
│   └── generate-eval-config.py  # Config generator
└── README.md                 # This file
```

## Running Locally vs CI

| | Local | CI |
|---|---|---|
| **Command** | `npx promptfoo@latest eval -c eval/skills/X.yaml` | Automatic on PR |
| **Results** | Terminal + web viewer | PR comment + artifact |
| **Caching** | Enabled (faster iteration) | Disabled (`--no-cache`) |
| **Cost** | Your API key | Repo secret `ANTHROPIC_API_KEY` |

## Cost Estimate

Each skill eval runs 2-3 test cases × ~4K tokens output = ~12K tokens per skill.  
At Sonnet pricing (~$3/M input, $15/M output): **~$0.05-0.10 per skill eval**.  
Full 10-skill pilot batch: **~$0.50-1.00 per run**.
