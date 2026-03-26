# AI Red Teaming

Adversarial security testing of AI and ML systems: prompt injection, jailbreaks, model inversion, and data poisoning.

## When to use

- You need to test an LLM application's resistance to prompt injection
- You want to assess jailbreak susceptibility of a deployed model
- You need to evaluate whether training data can be extracted via inference
- You are assessing a RAG pipeline for indirect prompt injection via retrieved documents

**Authorization required.** Never run AI red teaming without explicit written authorization from the AI system owner.

## Quick Start

```bash
python scripts/ai-red-teaming_tool.py --help
python scripts/ai-red-teaming_tool.py --output json
```

## Skill Level: L4

This skill can recommend actions that affect AI system configuration and may expose sensitive model information. All findings require human review before disclosure.

## References

- [Workflow Guide](references/workflow.md)
- [MITRE ATLAS](https://atlas.mitre.org/)
