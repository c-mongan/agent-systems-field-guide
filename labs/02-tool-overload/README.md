# Lab 02 — Tool overload

## Question

Is a catalogue of six tools too large, or are overlapping descriptions the real problem?

## Controlled change

Both variants expose the same six tool names and capabilities.

- **Baseline:** every description broadly claims code, dependencies, incidents, releases, security, and documentation.
- **Candidate:** each tool owns one operation and evidence domain.

## Result

| Metric | Baseline | Candidate |
|---|---:|---:|
| catalogue items | 6 | 6 |
| routing accuracy | 0.50 | 1.00 |
| ambiguity rate | 0.583 | 0.000 |
| max pairwise overlap | 0.643 | 0.056 |

The item count does not change. The boundaries do.

## Run

```bash
agent-guide lab run 02-tool-overload --root .
```

## Limit

The router is deterministic. Use live model runs before generalizing the exact accuracy values.
