# Lab 06 — Eager context

## Question

What is the structural context cost of preloading six full skills and their references?

## Controlled change

Both variants use the same six skill sizes, reference sizes, catalogue sizes, cases, and 16,000-token budget.

- **Baseline:** eager mode loads every skill body and reference.
- **Candidate:** progressive mode loads catalogue metadata, one selected skill, and only required reference content.

## Result

| Metric | Baseline | Candidate |
|---|---:|---:|
| mean initial estimate | 12,000 | 388 |
| mean total estimate | 46,600 | 3,963 |
| mean irrelevant estimate | 43,025 | 388 |
| budget overflow rate | 1.00 | 0.00 |

## Run

```bash
agent-guide lab run 06-eager-context --root .
```

## Limit

The token values are explicit fixture parameters, not provider billing counts. Some harness configurations intentionally preload a small set of skills; measure the real startup context before changing them.
