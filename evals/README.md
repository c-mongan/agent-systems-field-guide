# Portable evaluation records

This directory defines a small provider-neutral trace contract and one frozen paired comparison.

```text
evals/
├── schema/trace.schema.json
├── fixtures/baseline.jsonl
├── fixtures/candidate.jsonl
└── results/architecture-comparison.json
```

## Trace schema

Each row records one case, success result, latency, token counts, tool calls, and metadata. Real provider traces should also store the exact model, settings, tool policy, input snapshot, and architecture version.

See the full [trace contract](../docs/evaluation/traces.md).

## Paired comparison

The comparison CLI requires the same `case_id` set on both sides. It reports quality and cost deltas without hiding missing cases.

```bash
agent-guide eval compare \
  evals/fixtures/baseline.jsonl \
  evals/fixtures/candidate.jsonl \
  --output evals/results/architecture-comparison.json
```

The committed fixture demonstrates the comparison machinery. It is synthetic and is not a model benchmark.

## Add a real evaluation

1. Create immutable case IDs.
2. Write an acceptance policy before running.
3. Freeze model, settings, permissions, data, timeout, and retries.
4. Run baseline and candidate under the same policy.
5. Store all successes, failures, timeouts, and parse errors.
6. Grade blindly where practical.
7. Publish raw or redacted traces with a run specification.

Use the [live provider protocol](../docs/evaluation/live-provider-protocol.md) for Claude Code, Codex, or Gemini CLI runs.
