---
id: tool-explosion
status: avoid
evidence:
  - scripts-for-determinism
---
# Tool explosion

The model sees many near-duplicate operations or performs a long mechanical loop through tool calls.

## Symptoms

- one task calls the same tool shape dozens of times;
- tool descriptions overlap;
- raw outputs dominate context;
- partial failures are hard to reconcile;
- the model sorts, joins, or counts manually.

## Better boundary

Batch exact work in code. Expose meaningful operations that return compact structured evidence. Keep direct calls only when each result needs new semantic judgment.

## Example

Replace 80 `fetch-item` calls plus model-side sorting with one `collect-and-rank-items` operation that reports missing items and source IDs.

## Proof required

Compare task success, calls, latency, tokens, truncation, and error handling. See [Lab 02](../labs/02-tool-overload/README.md).

**Evidence:** `scripts-for-determinism`
