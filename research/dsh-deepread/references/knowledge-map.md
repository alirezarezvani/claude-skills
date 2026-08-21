# Evidence-Centered Knowledge Map

Use this reference for `map` mode. A useful map preserves reasoning, not just headings.

## Node Types

- `THESIS`: the central claim or explanatory model.
- `CLAIM`: a supporting or opposing proposition.
- `REASON`: a logical bridge between claims.
- `EVIDENCE`: an observation, quotation, record, or study.
- `DATA`: numerical evidence with unit, population, period, and baseline.
- `EXAMPLE`: an illustration that does not by itself establish generality.
- `CONCEPT`: a term whose definition matters to the argument.
- `ASSUMPTION`: an unstated premise.
- `COUNTERARGUMENT`: an alternative conclusion or explanation.
- `LIMITATION`: a boundary on scope or confidence.
- `QUESTION`: an unresolved issue or retrieval prompt.

## Edge Labels

Every edge must use a meaningful label: `supports`, `explains`, `defines`, `illustrates`, `depends on`, `qualifies`, `contradicts`, or `raises`.

Never use unlabeled proximity as a substitute for a relationship.

## Required Metadata

For evidence and data nodes, include:

- source location;
- the claim they connect to;
- confidence label;
- missing context or caveat.

## Markdown Output

```text
THESIS: [central claim]
├── supports → CLAIM: [supporting claim]
│   ├── because → REASON: [logical bridge]
│   ├── supports → EVIDENCE: [evidence] ([location])
│   └── qualifies → LIMITATION: [boundary]
├── depends on → ASSUMPTION: [unstated premise]
└── contradicted by → COUNTERARGUMENT: [strong alternative]
```

When the user requests FreeMind or XMind-compatible output, render the same hierarchy as valid FreeMind XML and escape all source-derived text used in XML attributes.

## Quality Check

Before delivering the map, verify:

1. Every major claim connects to the thesis.
2. Every evidence node connects to a specific claim.
3. Examples are labeled as examples.
4. Contradictions and limitations remain visible.
5. The map contains no conclusion that exists only because of layout.
