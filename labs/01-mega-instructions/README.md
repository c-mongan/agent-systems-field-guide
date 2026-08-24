# Lab 01 — Mega instructions

## Question

What happens when eight specialist procedures are always loaded instead of selected on demand?

## Controlled change

Both variants contain the same core rules and the same eight procedure blocks.

- **Baseline:** eager mode loads all blocks.
- **Candidate:** on-demand mode loads only the block expected by the case.

The frozen cases include incident triage, migration planning, release work, documentation, data analysis, security, PR review, and customer response.

## Result

| Metric | Baseline | Candidate |
|---|---:|---:|
| mean loaded estimate | 344.0 | 84.3 |
| mean irrelevant estimate | 259.7 | 0.0 |
| mean conflict hits | 0.9 | 0.0 |
| structural success | 0.30 | 1.00 |

## Run

```bash
agent-guide lab run 01-mega-instructions --root .
```

## Limit

The token values use the repository's documented text estimate. The success rule is deterministic and fixture-specific. The result demonstrates context and rule-conflict mechanics, not live model quality.
