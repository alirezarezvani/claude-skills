# Prompt Templates

## 1) Structured Extractor

```text
You are an extraction assistant.
Return ONLY valid JSON matching this schema:
{{schema}}

Input:
{{input}}
```

## 2) Classifier

```text
Classify input into one of: {{labels}}.
Return only the label.

Input: {{input}}
```

## 3) Summarizer

```text
Summarize the input in {{max_words}} words max.
Focus on: {{focus_area}}.
Input:
{{input}}
```

## 4) Rewrite With Constraints

```text
Rewrite for {{audience}}.
Constraints:
- Tone: {{tone}}
- Max length: {{max_len}}
- Must include: {{must_include}}
- Must avoid: {{must_avoid}}

Input:
{{input}}
```

## 5) QA Pair Generator

```text
Generate {{count}} Q/A pairs from input.
Output JSON array: [{"question":"...","answer":"..."}]

Input:
{{input}}
```

## 6) Issue Triage

```text
Classify issue severity: P1/P2/P3/P4.
Return JSON: {"severity":"...","reason":"...","owner":"..."}
Input:
{{input}}
```

## 7) Code Review Summary

```text
Review this diff and return:
1. Risks
2. Regressions
3. Missing tests
4. Suggested fixes

Diff:
{{input}}
```

## 8) Persona Rewrite

```text
Respond as {{persona}}.
Goal: {{goal}}
Format: {{format}}
Input: {{input}}
```

## 9) Policy Compliance Check

```text
Check input against policy.
Return JSON: {"pass":bool,"violations":[...],"recommendations":[...]}
Policy:
{{policy}}
Input:
{{input}}
```

## 10) Prompt Critique

```text
Critique this prompt for clarity, ambiguity, constraints, and failure modes.
Return concise recommendations and an improved version.
Prompt:
{{input}}
```
