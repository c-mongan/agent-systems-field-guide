# Lab 03 — Mega skill

## Question

When should one skill move specialist knowledge into references?

## Controlled change

Both variants contain the same authentication guidance for OAuth, webhooks, service accounts, and mobile apps.

- **Baseline:** monolith mode loads all domain guidance.
- **Candidate:** reference mode identifies one trust boundary and loads only that domain.

## Result

| Metric | Baseline | Candidate |
|---|---:|---:|
| mean loaded estimate | 270.0 | 87.25 |
| mean irrelevant estimate | 191.25 | 2.5 |
| structural success | 0.25 | 1.00 |

## Run

```bash
agent-guide lab run 03-mega-skill --root .
```

## Design lesson

Move material into references when it is conditional and the core skill can state a clear read rule. Do not hide universal security invariants in optional files.

## Limit

The lab models reference selection with frozen domain labels. A live skill eval must test whether the harness actually selects the correct reference.
