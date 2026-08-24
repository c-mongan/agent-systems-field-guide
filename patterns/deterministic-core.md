---
id: deterministic-core
status: recommended
evidence:
  - scripts-for-determinism
---
# Deterministic core

Use normal code for exact data work and let the model reason over the compact result.

## Pattern

```text
large or repetitive input
          ↓
script / typed tool
parse • filter • join • validate • rank
          ↓
compact evidence with source IDs
          ↓
agent judgment
```

## Use when

- one correct calculation exists;
- the same operation repeats across many items;
- a raw result is much larger than the useful result;
- correctness can be checked with fixtures;
- the operation is safer in a sandboxed process.

## Design rules

- define input and output schemas;
- preserve evidence IDs;
- distinguish empty data from failed retrieval;
- set timeouts and truncation rules;
- expose partial failures;
- make writes idempotent;
- keep the scoring formula visible.

## Example

The [release example](../examples/release-engineering/README.md) calculates version propagation and topological publish order in Python. The agent judges semantic version bumps and release risk. A workflow controls publishing.

## Proof

Compare model-only and deterministic-core variants. Track task success, tool calls, input tokens, latency, and calculation errors.

**Evidence:** `scripts-for-determinism`
