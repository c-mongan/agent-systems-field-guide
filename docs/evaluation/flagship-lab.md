# Flagship lab — overlapping skills

This lab answers one narrow question:

> What changes when six skills keep the same jobs but their descriptions become less overlapping?

## Controlled variables

Held constant:

- six skill names;
- six capabilities;
- 24 prompts;
- deterministic router;
- weighting and scoring logic;
- acceptance policy.

Changed:

- description wording;
- positive intent boundaries;
- negative neighbour boundaries.

## Result

| Metric | Baseline | Candidate | Direction |
|---|---:|---:|---:|
| top-1 accuracy | 0.375 | 0.958 | higher is better |
| ambiguity rate | 0.708 | 0.125 | lower is better |
| mean pairwise overlap | 0.377 | 0.021 | lower is better |
| maximum pairwise overlap | 0.600 | 0.120 | lower is better |
| mean decision margin | 0.592 | 3.840 | higher is better |

## Why this lab is fairer than a renamed catalogue

A weak routing demo often changes both labels and capabilities. The baseline then cannot produce the expected answer by design.

This lab keeps the same six skill IDs and jobs. Only the descriptions and boundaries change. A baseline success remains possible.

## Two live harness contracts

The lab also contains:

- a Claude Code structured-output fixture;
- a Codex JSONL event fixture;
- a shared output schema;
- command builders and parsers tested in CI.

These fixtures verify the adapter contract. No live model result is committed because this environment did not run fixed-model provider benchmarks.

## Reproduce

```bash
agent-guide lab run 04-overlapping-skills --root .
```

Inspect:

- [`cases.jsonl`](../../labs/04-overlapping-skills/cases.jsonl)
- [`baseline.json`](../../labs/04-overlapping-skills/baseline.json)
- [`candidate.json`](../../labs/04-overlapping-skills/candidate.json)
- [`results/comparison.json`](../../labs/04-overlapping-skills/results/comparison.json)
- [`results/manifest.json`](../../labs/04-overlapping-skills/results/manifest.json)

Then run the same cases through a live provider using the [live provider protocol](live-provider-protocol.md).
