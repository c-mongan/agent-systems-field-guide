# Lab 05 — Premature subagents

## Question

What happens when exact or tiny steps are implemented as separate agents?

## Controlled change

Both variants use the same frozen spawn cost, coordination cost, script cost, and worker failure probability.

- **Baseline:** every step becomes an agent.
- **Candidate:** deterministic steps use scripts and only genuinely independent reasoning uses a worker.

## Result

| Metric | Baseline | Candidate |
|---|---:|---:|
| mean agent count | 9.3 | 1.2 |
| mean input-token model | 11,160 | 1,804.5 |
| mean latency model | 1,598.5 ms | 1,239.5 ms |
| expected success probability | 0.807 | 0.971 |

## Run

```bash
agent-guide lab run 05-premature-subagents --root .
```

## Limit

This is a frozen discrete-event cost model, not measured provider latency. Change the fixture parameters to match a real system before using it for capacity planning.
