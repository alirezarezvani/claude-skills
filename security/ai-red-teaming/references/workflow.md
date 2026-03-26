# AI Red Teaming Workflow

## Pre-Engagement

1. Obtain written authorization specifying: target system, scope, test categories, time window
2. Confirm emergency abort contacts
3. Document baseline model behavior before testing begins

## Phase 1: Reconnaissance

1. Identify model type (LLM, classifier, embedding, generative)
2. Map all input/output interfaces
3. Determine access level (black-box, gray-box, white-box)
4. Identify RAG pipelines, fine-tuning interfaces, and training data sources if in scope

## Phase 2: Prompt Injection Testing

1. Attempt direct instruction overrides
2. Test indirect injection via tool outputs and retrieved documents
3. Test multi-turn context accumulation
4. Document success rate and bypass confidence threshold

## Phase 3: Jailbreak Testing

1. Apply known jailbreak patterns from public research
2. Develop novel jailbreaks based on model behavior observations
3. Test safety guardrail bypass rate
4. Document which categories of harmful content can be elicited

## Phase 4: Model Inversion

1. Repeated inference with varied inputs to probe training data
2. System prompt extraction attempts
3. Membership inference testing

## Phase 5: Findings Documentation

1. Map all findings to MITRE ATLAS
2. Score by exploitability and business impact
3. Produce technical findings + executive summary
4. Submit for human review before disclosure
