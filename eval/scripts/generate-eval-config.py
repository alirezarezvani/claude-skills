#!/usr/bin/env python3
"""Generate a promptfoo eval config for any skill.

Usage:
    python eval/scripts/generate-eval-config.py marketing-skill/copywriting
    python eval/scripts/generate-eval-config.py c-level-advisor/cto-advisor --force
"""

import os
import re
import sys
import textwrap


def parse_frontmatter(skill_path):
    """Extract name and description from SKILL.md YAML frontmatter."""
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Match YAML frontmatter between --- delimiters
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, None

    frontmatter = match.group(1)
    name = None
    description = None

    for line in frontmatter.split("\n"):
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip().strip("'\"")
        elif line.startswith("description:"):
            # Handle multi-line descriptions
            desc = line.split(":", 1)[1].strip().strip("'\"")
            description = desc

    return name, description


def generate_config(skill_dir, force=False):
    """Generate a promptfoo eval YAML config for the given skill directory."""
    # Resolve SKILL.md path
    skill_md = os.path.join(skill_dir, "SKILL.md")
    if not os.path.exists(skill_md):
        print(f"Error: {skill_md} not found", file=sys.stderr)
        sys.exit(1)

    name, description = parse_frontmatter(skill_md)
    if not name:
        print(f"Error: Could not parse frontmatter from {skill_md}", file=sys.stderr)
        sys.exit(1)

    # Output path
    output_path = os.path.join("eval", "skills", f"{name}.yaml")
    if os.path.exists(output_path) and not force:
        print(f"Eval config already exists: {output_path}")
        print("Use --force to overwrite.")
        sys.exit(0)

    # Calculate relative path from eval/skills/ to the skill
    rel_path = os.path.relpath(skill_md, os.path.join("eval", "skills"))

    # Generate test prompts based on description
    desc_lower = (description or "").lower()

    # Default test prompts
    prompts = [
        f"I need help with {name.replace('-', ' ')}. Give me a comprehensive approach for a mid-stage B2B SaaS startup.",
        f"Act as an expert in {name.replace('-', ' ')} and review my current approach. I'm a solo founder building a developer tool.",
    ]

    # Add domain-specific third prompt
    if any(w in desc_lower for w in ["marketing", "content", "seo", "copy"]):
        prompts.append(
            "Create a 90-day plan with specific deliverables, metrics, and milestones."
        )
    elif any(w in desc_lower for w in ["engineer", "architect", "code", "technical"]):
        prompts.append(
            "Design a technical solution with architecture diagram, tech stack recommendations, and implementation plan."
        )
    elif any(w in desc_lower for w in ["advisor", "executive", "strategic", "leader"]):
        prompts.append(
            "Help me prepare a board presentation on this topic with key metrics and strategic recommendations."
        )
    else:
        prompts.append(
            f"What are the top 5 mistakes people make with {name.replace('-', ' ')} and how to avoid them?"
        )

    # Build YAML
    config = textwrap.dedent(f"""\
    # Eval: {name}
    # Source: {skill_dir}/SKILL.md
    # Run: npx promptfoo@latest eval -c eval/skills/{name}.yaml
    # Auto-generated — customize test prompts and assertions for better coverage

    description: "Evaluate {name} skill"

    prompts:
      - |
        You are an expert AI assistant. You have the following skill loaded:

        ---BEGIN SKILL---
        {{{{skill_content}}}}
        ---END SKILL---

        Now complete this task: {{{{task}}}}

    providers:
      - id: anthropic:messages:claude-sonnet-4-6
        config:
          max_tokens: 4096
          temperature: 0.7

    tests:
    """)

    for i, prompt in enumerate(prompts):
        test_block = textwrap.dedent(f"""\
      - vars:
          skill_content: file://{rel_path}
          task: "{prompt}"
        assert:
          - type: llm-rubric
            value: "Response demonstrates specific expertise in {name.replace('-', ' ')}, not generic advice"
          - type: llm-rubric
            value: "Response is actionable with concrete steps or deliverables"
          - type: javascript
            value: "output.length > 300"
    """)
        config += test_block

    # Write
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(config)

    print(f"✅ Generated: {output_path}")
    print(f"   Skill: {name}")
    print(f"   Tests: {len(prompts)}")
    print(f"   Edit the file to customize prompts and assertions.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python eval/scripts/generate-eval-config.py <skill-directory>")
        print("       python eval/scripts/generate-eval-config.py marketing-skill/copywriting --force")
        sys.exit(1)

    skill_dir = sys.argv[1].rstrip("/")
    force = "--force" in sys.argv

    generate_config(skill_dir, force)
