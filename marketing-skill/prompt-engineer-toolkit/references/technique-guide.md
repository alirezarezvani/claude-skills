# Technique Guide

## Selection Rules

- Zero-shot: deterministic, simple tasks
- Few-shot: formatting ambiguity or label edge cases
- Chain-of-thought: multi-step reasoning tasks
- Structured output: downstream parsing/integration required
- Self-critique/meta prompting: prompt improvement loops

## Prompt Construction Checklist

- Clear role and goal
- Explicit output format
- Constraints and exclusions
- Edge-case handling instruction
- Minimal token usage for repetitive tasks

## Failure Pattern Checklist

- Too broad objective
- Missing output schema
- Contradictory constraints
- No negative examples for unsafe behavior
- Hidden assumptions not stated in prompt
